"""AJAN-AKIS-1 ÖLÇÜM: egitim-1'in 60 görevi (kod·çıkarım·mantık) × katman (ücretsiz · Haiku · Sonnet) × kol (önce=çekirdeksiz · sonra=çekirdekli).
Doğrulama betikle (tools/ogret/kapi.py DOGRU). Dış çağrı tavanı: ücretsiz ≤120, Haiku ≤120, Sonnet ≤120 (60 görev × 2 kol).
python tools/olcum/akis_olc.py [--katman=ucretsiz,haiku,sonnet] [--tur=kod,cikarim,mantik] → .kos/kopru/akis/olcum.json
Çıktı: katman/kol → doğru/n, sonuçsuz, giriş jetonu (usage: girdi+önbellek yazma+okuma), maliyet $."""
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / "tools/ogret"))
import ajan_cekirdek as AC  # noqa: E402
import kapi as K  # noqa: E402  (görev üreticileri + DOGRU)
import ucretsiz_havuz as H  # noqa: E402

arg = lambda ad, v: next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{ad}=")), v)  # noqa: E731
KATMAN, TURLER = arg("katman", "ucretsiz,haiku,sonnet").split(","), arg("tur", "kod,cikarim,mantik").split(",")
TAVAN = 120
MODEL = dict(haiku="claude-haiku-5-5", sonnet="claude-sonnet-5-5")
CIKTI = KOK / ".kos/kopru/akis/olcum.json"
ONEK = AC.onek()


def claude(istem, model):
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
    p = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json", "--max-turns", "1", "--tools", "", "--setting-sources", ""],
                       input=istem, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
                       creationflags=H.NW, cwd=H.DIZIN, env=env)
    j = json.loads(p.stdout)
    if j.get("is_error") or not (j.get("result") or "").strip():
        raise RuntimeError(str(j.get("result"))[:80])
    u = j.get("usage") or {}
    return j["result"].strip(), u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0), j.get("total_cost_usd", 0)


def kos(g, katman, kol):
    try:
        if katman == "ucretsiz":
            y, model, _ = H.cagir("yazim", g["istem"], max_tokens=2500, zaman=70)  # kol=once: ajan_cekirdek.onek boş yamalı (aşağıda); sonra: normal
            jeton, usd = (len(g["istem"]) + (len(ONEK) if kol == "sonra" else 0)) // 3, 0
        else:
            y, jeton, usd = claude((ONEK if kol == "sonra" else "") + g["istem"], MODEL[katman])
    except Exception as x:  # noqa: BLE001
        return dict(id=g["id"], katman=katman, kol=kol, ok=None, jeton=0, usd=0, hata=type(x).__name__)
    if y is None:
        return dict(id=g["id"], katman=katman, kol=kol, ok=None, jeton=0, usd=0)
    return dict(id=g["id"], katman=katman, kol=kol, ok=K.DOGRU[g["tur"]](g, y), jeton=jeton, usd=usd)


def main():
    gorevler = [g for t in TURLER for g in K.GOREV[t]()]
    sonuc = []
    for kol in ("once", "sonra"):
        # once: çekirdek HİÇ girmesin → ücretsiz havuzun otomatik eklediği çekirdek bu kol için boşaltılır
        AC.onek = (lambda zor=False: "") if kol == "once" else (lambda zor=False, _o=ONEK: _o)
        isler = [(g, k, kol) for k in KATMAN for g in gorevler]
        assert sum(1 for _, k, _ in isler if k == "ucretsiz") <= TAVAN and sum(1 for _, k, _ in isler if k == "haiku") <= TAVAN and sum(1 for _, k, _ in isler if k == "sonnet") <= TAVAN
        with cf.ThreadPoolExecutor(4) as ex:
            sonuc += list(ex.map(lambda a: kos(*a), isler))
    ozet = {}
    for k in KATMAN:
        for kol in ("once", "sonra"):
            r = [s for s in sonuc if s["katman"] == k and s["kol"] == kol]
            ozet[f"{k}/{kol}"] = dict(n=len(r), dogru=sum(1 for s in r if s["ok"]), sonucsuz=sum(1 for s in r if s["ok"] is None), jeton=sum(s["jeton"] for s in r), usd=round(sum(s["usd"] for s in r), 3))
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text(json.dumps(dict(ozet=ozet, sonuc=sonuc, zaman=time.strftime("%Y-%m-%d %H:%M")), ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in ozet.items():
        print(k, v)


if __name__ == "__main__":
    main()
