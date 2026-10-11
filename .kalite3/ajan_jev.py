"""KALİTE-3 Faz 4 pilot: ajan ↔ ana kolu yanıtlarını Jev ile puanlar (kol/jev jev_yargic.SORU ile aynı soru).
kabul = görev rubriğinin terimleri (iki kola aynı). Çıktı: kalite3-ajan-pilot.tsv + jev sütunu → kalite3-ajan-pilot-jev.tsv
python .kalite3/ajan_jev.py   (Jev en fazla 2 batch çağrı; yanıt başına ≈ $0.0001)"""
import csv, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, "C:/Projeler/omer-skills/tools/jev")
from jev.cekirdek import Tasiyici  # noqa: E402

SEVIYE = ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik", "Çoğunlukla, küçük eksik",
          "Tam karşılıyor", "Tam ve örnek nitelikte"]
SORU = {"kalite": {"type": "score", "criteria": SEVIYE,
                   "instructions": "`yanit`, `gorev` isteğini `kabul` ölçütüne göre ne kadar karşılıyor? "
                                   "Yalnız yanıtın içeriğini yargıla; biçim/uzunluk değil, doğruluk ve kabul ölçütü."}}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    gorev = {g["ajan"]: g for g in json.loads((KOK / "ajanlar/kalite3/gorevler.json").read_text(encoding="utf-8"))}
    tsv = KOK / "docs/kutuphane/olcum/kalite3-ajan-pilot.tsv"
    satir = list(csv.DictReader(tsv.open(encoding="utf-8"), delimiter="\t"))
    state = []
    for s in satir:
        g = gorev[s["ajan"]]
        kabul = "Yanıt şunları kapsamalı: " + "; ".join(
            f"{re.sub(r'^[(][?]i[)]', '', r['regex'])} ({r['puan']} puan)" for r in g["rubrik"])
        yanit = (KOK / ".kalite3/ajan-yanit" / f"{s['ajan']}-{s['kol']}.md").read_text(encoding="utf-8", errors="replace")
        state.append({"gorev": g["istem"], "kabul": kabul, "yanit": yanit})
    for s, c in zip(satir, Tasiyici(en_fazla=2, istek_tavan=len(state) + 10).yargila(state, SORU)):
        s["jev"] = round(c["kalite"]["score"] * 2, 1) if c else ""
    cikti = tsv.with_name("kalite3-ajan-pilot-jev.tsv")
    with cikti.open("w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=list(satir[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(satir)
    print(cikti, sum(1 for s in satir if s["jev"] != ""), "/", len(satir), "puanlandı")


if __name__ == "__main__":
    main()
