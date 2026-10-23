"""LAYA-2 etiketsiz havuz: gerçek (görev, yanıt) çiftleri + kural/ücretsiz-LLM ile bozulmuş çeşitler → kurul girdisi (kurul.py).
  python havuz_kur.py gercek <cikti.jsonl>             ajan-sira sonuçları (+ Opus etiketsiz jev_tum eğitim yarısı) → {id,state}
  python havuz_kur.py cesit <gercek.jsonl> <cikti.jsonl>  her gerçek öğe için kesik · yarım · karışık · kanıtsız iddia · alakasız çeşit (kural, LLM yok: ücretsiz kota "yazım" için yetmedi); çeşit kimliği taban#tür
Test sızıntısı yok: Opus etiketli ayrılmış test öğeleri (laya-1 bölmesi) ve çeşitleri havuza girmez."""
import hashlib
import json
import random
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ucretsiz_havuz as uh  # noqa: E402

KABUL = "Görevde istenen her adım yapılmış, kanıtlanmış ve rapor istenen biçimde; boş iddia ve eksik yok."
NL = chr(10)
YKILIT = threading.Lock()
_yaz = uh._yaz


def _kilitli(d):
    with YKILIT:
        _yaz(d)


uh._yaz = _kilitli


def test_mi(i):
    return int(hashlib.sha256(i.encode()).hexdigest(), 16) % 2 == 0


def gercek(cik):
    out = []
    for f in sorted((KOK / ".kos/kopru/ajan-sira").glob("*.json")):
        ad = f.stem
        g = KOK / ".kos/kopru/gorev" / f"{ad}.md"
        if ad.endswith(("denetim", "zorunlu")) or not g.exists():
            continue
        try:
            r = json.loads(f.read_text(encoding="utf-8")).get("result")
        except ValueError:
            continue
        if isinstance(r, str) and len(r) > 300:
            out.append({"id": f"ajan:{ad}", "state": {"gorev": g.read_text(encoding="utf-8")[:1500], "kabul": KABUL, "yanit": r}})
    etiketli = {json.loads(x)["id"] for x in open(KOK / ".claude/laya2/opus.jsonl", encoding="utf-8")}
    tum = KOK.parent / "omer-skills-wt/jev/.claude/jev1/jev_tum.jsonl"
    for x in map(json.loads, open(tum, encoding="utf-8")):
        i = "jev1:" + x["dosya"]
        if i not in etiketli or not test_mi(i):  # Opus etiketli test yarısı taban olamaz
            out.append({"id": i, "state": x["state"]})
    with open(cik, "w", encoding="utf-8") as f:
        f.writelines(json.dumps(k, ensure_ascii=False) + "\n" for k in out)
    print("gercek", len(out))


def cesit(gir, cik):
    base = [json.loads(x) for x in open(gir, encoding="utf-8")]
    bitti = {json.loads(x)["id"] for x in open(cik, encoding="utf-8")} if Path(cik).exists() else set()
    rnd, n = random.Random(7), 0
    kilit = threading.Lock()

    def yaz(k):
        with kilit:
            open(cik, "a", encoding="utf-8").write(json.dumps(k, ensure_ascii=False) + "\n")

    def is_(b):
        s = b["state"]
        diger = rnd.choice([x for x in base if x["state"]["gorev"] != s["gorev"]])
        if b["id"] + "#kesik" not in bitti:
            y = s["yanit"]
            yaz({"id": b["id"] + "#kesik", "state": {**s, "yanit": y[:max(200, len(y) // 4)]}})
        if b["id"] + "#alakasiz" not in bitti:
            yaz({"id": b["id"] + "#alakasiz", "state": {**s, "yanit": diger["state"]["yanit"]}})
        y, sat = s["yanit"], s["yanit"].split(NL)
        yar = {"yarim": y[:len(y) // 2],  # işin yarısı
               "karisik": y[:len(y) // 2] + NL + diger["state"]["yanit"][len(diger["state"]["yanit"]) // 2:],  # yarısı başka işten
               "iddia": NL.join(sat[:3]) + NL + "Görev tamamlandı, her şey çalışıyor, testler geçti."}  # kanıtsız iddia
        for tur, m in yar.items():
            if b["id"] + "#" + tur not in bitti:
                yaz({"id": b["id"] + "#" + tur, "state": {**s, "yanit": m}})
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(is_, base))
    print("CESIT BITTI")


if __name__ == "__main__":
    {"gercek": lambda: gercek(sys.argv[2]), "cesit": lambda: cesit(sys.argv[2], sys.argv[3])}[sys.argv[1]]()
