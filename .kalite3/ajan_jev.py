"""KALİTE-3 Faz 4 pilot: ajan ↔ ana kolu yanıtlarını Jev ile puanlar (kol/jev jev_yargic.SORU ile aynı soru).
kabul = görev rubriğinin terimleri (iki kola aynı). Çıktı: kalite3-ajan-pilot.tsv + jev sütunu → kalite3-ajan-pilot-jev.tsv
Önceki jev tsv'deki (ajan, kol, sure) aynı satırlar yeniden puanlanmaz. Karar (Desktop 03:10): geçti = Jev ≥ ana VE regex ≥ ana
VE $ ≤ ana × 1.1 — ajan $'ı toplam usd; haiku ajanda (ana oturum sonnet) alt_usd. Geçenler stdout'ta "GECTI ad".
python .kalite3/ajan_jev.py   (Jev en fazla 2 batch çağrı; yanıt başına ≈ $0.0001)"""
import csv, json, os, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, "C:/Projeler/omer-skills/tools/jev")
from jev.cekirdek import ANAHTAR_ADLARI, Tasiyici  # noqa: E402


def ortam():
    """os.environ + süreçte olmayan anahtar adları HKCU\\Environment'tan (salt okuma). Kök neden (d11): anahtarlar
    kullanıcı ortamına CC başladıktan sonra yazıldı → CC ve arka plan çocukları onları miras almıyor."""
    env = dict(os.environ)
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            for ad in ANAHTAR_ADLARI:
                if not env.get(ad):
                    try:
                        env[ad] = winreg.QueryValueEx(k, ad)[0]
                    except OSError:
                        pass
    except ImportError:
        pass
    return env

SEVIYE = ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik", "Çoğunlukla, küçük eksik",
          "Tam karşılıyor", "Tam ve örnek nitelikte"]
SORU = {"kalite": {"type": "score", "criteria": SEVIYE,
                   "instructions": "`yanit`, `gorev` isteğini `kabul` ölçütüne göre ne kadar karşılıyor? "
                                   "Yalnız yanıtın içeriğini yargıla; biçim/uzunluk değil, doğruluk ve kabul ölçütü."}}


def karar(satir):
    """{ajan: geçti mi} — iki kolu da sayısal puanlı ajanlar."""
    kol = {(s["ajan"], s["kol"]): s for s in satir}
    sonuc = {}
    for (ad, k), a in kol.items():
        n = kol.get((ad, "ana"))
        if k != "ajan" or not n or "" in (a["jev"], n["jev"]) or "hata" in (a["puan"], n["puan"]):
            continue
        usd = float(a["alt_usd"]) if a.get("alt_usd") and a["alt_model"] == "claude-haiku-5-5" else float(a["usd"])
        sonuc[ad] = (float(a["jev"]) >= float(n["jev"]) and float(a["puan"]) >= float(n["puan"])
                     and usd <= float(n["usd"]) * 1.1)
    return sonuc


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    gorev = {g["ajan"]: g for g in json.loads((KOK / "ajanlar/kalite3/gorevler.json").read_text(encoding="utf-8"))}
    tsv = KOK / "docs/kutuphane/olcum/kalite3-ajan-pilot.tsv"
    cikti = tsv.with_name("kalite3-ajan-pilot-jev.tsv")
    satir = list(csv.DictReader(tsv.open(encoding="utf-8"), delimiter="\t", restval=""))
    eski = {(s["ajan"], s["kol"], s["sure"]): s["jev"] for s in csv.DictReader(cikti.open(encoding="utf-8"), delimiter="\t")} \
        if cikti.exists() else {}
    yeni, state = [], []
    for s in satir:
        s["jev"] = eski.get((s["ajan"], s["kol"], s["sure"]), "")
        if s["jev"] != "":
            continue
        g = gorev[s["ajan"]]
        kabul = "Yanıt şunları kapsamalı: " + "; ".join(
            f"{re.sub(r'^[(][?]i[)]', '', r['regex'])} ({r['puan']} puan)" for r in g["rubrik"])
        yanit = (KOK / ".kalite3/ajan-yanit" / f"{s['ajan']}-{s['kol']}.md").read_text(encoding="utf-8", errors="replace")
        yeni.append(s)
        state.append({"gorev": g["istem"], "kabul": kabul, "yanit": yanit})
    if state:
        for s, c in zip(yeni, Tasiyici(env=ortam(), en_fazla=2, istek_tavan=len(state) + 10).yargila(state, SORU)):
            s["jev"] = round(c["kalite"]["score"] * 2, 1) if c else ""
    with cikti.open("w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=list(satir[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(satir)
    k = karar(satir)
    print(cikti, len(yeni), "yeni puanlandı ·", sum(1 for s in satir if s["jev"] != ""), "/", len(satir))
    print("karar:", sum(k.values()), "/", len(k), "geçti")
    for ad, ok in sorted(k.items()):
        if ok:
            print("GECTI", ad)


if __name__ == "__main__":
    main()
