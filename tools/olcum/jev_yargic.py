"""JEV-1 (a): kosucu yanıt metinlerini Jev ile puanlar — regex rubriğin yanına anlamsal kalite (0-10).
  python tools/olcum/jev_yargic.py <olcum-dizini>... [--en-fazla N] [--istek-tavan N] [--jsonl yol] [--kuru]
Her <dizin>/<GID>-<tekrar>.md için state = görev istemi + kabul ölçütü + yanıt; tek score sorusu (6 seviye → 0-10).
Ücret: Jev girdi $0.042/M token (≈ yanıt başına $0.0001); --en-fazla batch çağrı tavanı (200 yanıt/çağrı)."""
import argparse
import json
import re
import sys
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
sys.path.insert(0, str(DIZIN.parents[0] / "jev"))
sys.path.insert(0, str(DIZIN))
from kosucu import puanla  # noqa: E402

SEVIYE = ["Hiç karşılamıyor / alakasız", "Çok zayıf", "Kısmen, önemli eksik", "Çoğunlukla, küçük eksik",
          "Tam karşılıyor", "Tam ve örnek nitelikte"]
SORU = {"kalite": {"type": "score", "criteria": SEVIYE,
                   "instructions": "`yanit`, `gorev` isteğini `kabul` ölçütüne göre ne kadar karşılıyor? "
                                   "Yalnız yanıtın içeriğini yargıla; biçim/uzunluk değil, doğruluk ve kabul ölçütü."}}


def veri(dizinler):
    gorev = {g["id"]: g for g in json.loads((DIZIN / "gorevler.json").read_text(encoding="utf-8"))}
    out = []
    for d in map(Path, dizinler):
        for f in sorted(d.glob("*.md")):
            m = re.fullmatch(r"([A-Z]\d+)-(\d+)", f.stem)
            if not m or m[1] not in gorev:
                continue
            g, metin = gorev[m[1]], f.read_text(encoding="utf-8", errors="replace")
            out.append({"dosya": f"{d.name}/{f.name}", "gorev": m[1], "regex": puanla(metin, g["rubrik"]),
                        "state": {"gorev": g["istem"], "kabul": g["kabul"], "yanit": metin}})
    return out


def jev_puanla(kayitlar, tasiyici):
    for k, c in zip(kayitlar, tasiyici.yargila([k["state"] for k in kayitlar], SORU)):
        k["jev"] = round(c["kalite"]["score"] * 2, 1)  # 0-5 → 0-10
        k["guven"] = c["kalite"].get("confidence")
    return kayitlar


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("dizinler", nargs="+")
    ap.add_argument("--en-fazla", type=int, default=2)
    ap.add_argument("--jsonl")
    ap.add_argument("--istek-tavan", type=int, default=250, help="API arka ucunda yanıt başına 1 HTTP isteği (tekrarlar dahil)")
    ap.add_argument("--kuru", action="store_true", help="ağa çıkmadan yalnız veri + regex")
    ns = ap.parse_args(argv)
    kayitlar = veri(ns.dizinler)
    if not ns.kuru:
        from jev.cekirdek import Tasiyici
        t = Tasiyici(en_fazla=ns.en_fazla, istek_tavan=ns.istek_tavan)
        jev_puanla(kayitlar, t)
        usd = sum(u.get("cost") or 0 for u in t.kullanim)
        print(f"jev: {len(kayitlar)} yanıt · {t.cagri} çağrı · {t.istek} istek · ${usd:.4f} · backend {t.b['ad']}")
    for k in kayitlar:
        print(f"{k['dosya']}\tregex {k['regex']}\tjev {k.get('jev', '-')}\tgüven {k.get('guven', '-')}")
    if ns.jsonl:
        Path(ns.jsonl).write_text("".join(json.dumps(k, ensure_ascii=False) + "\n" for k in kayitlar), encoding="utf-8")


if __name__ == "__main__":
    main()
