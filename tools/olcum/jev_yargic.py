"""JEV-1 (a): kosucu yanıt metinlerini Jev ile puanlar — regex rubriğin yanına anlamsal kalite (0-10).
  python tools/olcum/jev_yargic.py <olcum-dizini>... [--en-fazla N] [--istek-tavan N] [--jsonl yol] [--tsv-yaz] [--kuru]
Her <dizin>/<GID>-<tekrar>.md için state = görev istemi + kabul ölçütü + yanıt; tek score sorusu (6 seviye → 0-10).
Ücret: Jev girdi $0.042/M token (≈ yanıt başına $0.0001); --en-fazla batch çağrı tavanı (200 yanıt/çağrı)."""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import threading
import time
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
            out.append({"dosya": f"{d.name}/{f.name}", "gorev": m[1], "tekrar": m[2], "regex": puanla(metin, g["rubrik"]),
                        "state": {"gorev": g["istem"], "kabul": g["kabul"], "yanit": metin}})
    return out


ONBELLEK = Path.home() / ".cache" / "jev-yargic.json"
OB_TAVAN = 50_000  # bellek/disk tavanı: en eski girdiler düşer
PARCA_OB = 50  # her parça sonrası önbelleğe yazılır: kopukluk önceki parçaları kaybettirmez
AG_BEKLE = (30, 60, 120, 300, 600)  # ağ kopuk: duraklama sırası (sn, toplam ~18 dk), sonra BaglantiHata


def _ob_yaz(ob, yeni):
    """Birleştirip atomik yazar: paralel koşular birbirinin girdisini silmez, yarım dosya kalmaz."""
    tablo = json.loads(ob.read_text(encoding="utf-8")) if ob.exists() else {}
    tablo.update(yeni)
    for a in list(tablo)[:max(0, len(tablo) - OB_TAVAN)]:
        del tablo[a]
    ob.parent.mkdir(parents=True, exist_ok=True)
    gecici = ob.with_name(f"{ob.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    gecici.write_text(json.dumps(tablo, ensure_ascii=False), encoding="utf-8")
    os.replace(gecici, ob)


def yargila(states, questions, tasiyici=None, onbellek=None, parca=PARCA_OB, ag_bekle=AG_BEKLE, uyu=time.sleep):
    """Ortak yargıç (JEV-2 a): toplu çağrı; aynı (soru, state) ikinci kez ücretlenmez (önbellek). Cevapsız (None) önbelleğe girmez.
    Parça parça ilerler, her parça önbelleğe yazılır. Ağ kopukluğunda (BaglantiHata) ag_bekle sırasıyla duraklayıp aynı parçayı
    yeniden dener; tükenirse BaglantiHata yükselir — biten parçalar önbellekte kalır, çağıran öğeyi geri kuyruklar (kalite3_hiz.geri).
    Diğer JevHata o parçayı None bırakır (geri kuyruk: sonraki koşu yalnız onları ücretler); TavanHata yükselir."""
    from jev.cekirdek import BaglantiHata, JevHata, TavanHata
    ob = Path(onbellek or ONBELLEK)
    tablo = json.loads(ob.read_text(encoding="utf-8")) if ob.exists() else {}
    q = json.dumps(questions, sort_keys=True, ensure_ascii=False)
    anahtar = [hashlib.sha256((q + "\0" + json.dumps(s, sort_keys=True, ensure_ascii=False)).encode()).hexdigest()
               for s in states]
    eksik, yeni = list({a: s for a, s in zip(anahtar, states) if a not in tablo}.items()), {}
    if eksik and tasiyici is None:
        from jev.cekirdek import Tasiyici
        tasiyici = Tasiyici()
    for i in range(0, len(eksik), parca):
        p = eksik[i:i + parca]
        for bekle in (*ag_bekle, None):
            try:
                cevap = tasiyici.yargila([s for _, s in p], questions)
                break
            except BaglantiHata:
                if bekle is None:
                    raise
                uyu(bekle)
            except TavanHata:
                raise
            except JevHata:
                cevap = [None] * len(p)
                break
        yeni.update(zip((a for a, _ in p), cevap))
        if any(c is not None for c in cevap):
            _ob_yaz(ob, {a: c for (a, _), c in zip(p, cevap) if c is not None})
    return [tablo.get(a, yeni.get(a)) for a in anahtar]


class Onbellekli:
    """Tasiyici yerine geçer (JEV-2 d5): doğrudan `Tasiyici(...).yargila` çağıranlar (kalite3_hiz, fable_ajan_tablo,
    video parti) tek satırla ortak önbelleğe geçer. Sözleşme korunur: cevapsız öğe varsa JevHata (biten öğeler önbellekte)."""

    def __init__(self, tasiyici, onbellek=None):
        self.t, self.onbellek = tasiyici, onbellek

    def __getattr__(self, ad):
        return getattr(self.t, ad)

    def yargila(self, states, questions):
        from jev.cekirdek import JevHata
        cevap = yargila(states, questions, self.t, self.onbellek)
        if None in cevap:
            raise JevHata(f"{cevap.count(None)}/{len(cevap)} cevapsız (geri kuyruk)")
        return cevap


RAPOR_SORU = {"kalite": {"type": "score", "criteria": SEVIYE,
                         "instructions": "Bu kısa video (shorts) tarama raporu, videodaki iddiaları ve araç/skill adaylarını "
                                         "kanıta (kare/transkript) dayanarak, somut ve uygulanabilir biçimde çıkarmış mı? "
                                         "Uydurma, genel geçer ya da kanıtsız aday puanı düşürür; biçim/uzunluk değil içerik."}}


def rapor_onyargi(raporlar, tasiyici=None, onbellek=None, esik=6.0):
    """JEV-2 (b) video ön-yargıcı arayüzü (entegrasyonu VİDEO-16 seçer): rapor metni başına {jev 0-10, guven, karar}.
    karar: "gec" (jev ≥ esik) | "yeniden" | None (cevapsız → geri kuyruk, sonraki çağrı yalnız bunu ücretler)."""
    out = []
    for c in yargila([{"rapor": r} for r in raporlar], RAPOR_SORU, tasiyici, onbellek):
        if c is None:
            out.append({"jev": None, "guven": None, "karar": None})
            continue
        j = round(c["kalite"]["score"] * 2, 1)
        out.append({"jev": j, "guven": c["kalite"].get("confidence"), "karar": "gec" if j >= esik else "yeniden"})
    return out


def jev_puanla(kayitlar, tasiyici, onbellek=None):
    for k, c in zip(kayitlar, yargila([k["state"] for k in kayitlar], SORU, tasiyici, onbellek)):
        if c is None:  # geri kuyruk: puansız kalır, sonraki koşu yalnız bunu sorar
            continue
        k["jev"] = round(c["kalite"]["score"] * 2, 1)  # 0-5 → 0-10
        k["guven"] = c["kalite"].get("confidence")
    return kayitlar


def belirsiz(jevler, oran=0.2, merkez=7.0):
    """Karma yargı (JEV-2 d5): Jev puanı (0-10) merkeze en yakın ⌈oran·n⌉ öğenin indeksi — yalnız bunlar Opus'a yükseltilir.
    JEV-1 n=50 opus ref (örneklem içi): %20 → ρ 0.43→0.62 (merkez 6-8 arası hep ≥0.57; rastgele %20: 0.60), Opus çağrısı %80 az.
    %10'da merkeze duyarlı (0.50-0.57). Puansız (None) atlanır."""
    puanli = [i for i, j in enumerate(jevler) if j is not None]
    return sorted(puanli, key=lambda i: abs(jevler[i] - merkez))[:math.ceil(oran * len(puanli))]


def tsv_doldur(tsv, kayitlar):
    """<dizin>.tsv'nin jev/jev_guven sütunlarını (gorev, tekrar) eşleşmesiyle doldurur; eski başlığa sütun eklenir, puansız satır boş kalır."""
    L = Path(tsv).read_text(encoding="utf-8").splitlines()
    b = L[0].split("\t")
    if "jev" not in b:
        b += ["jev", "jev_guven"]
    i = b.index("jev")
    p = {(k["gorev"], k["tekrar"]): k for k in kayitlar if "jev" in k}
    out = ["\t".join(b)]
    for s in L[1:]:
        r = s.split("\t")
        r += [""] * (len(b) - len(r))
        if (r[0], r[1]) in p:
            k = p[(r[0], r[1])]
            r[i:i + 2] = [str(k["jev"]), "" if k.get("guven") is None else str(k["guven"])]
        out.append("\t".join(r))
    Path(tsv).write_text("\n".join(out) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("dizinler", nargs="+")
    ap.add_argument("--en-fazla", type=int, default=2)
    ap.add_argument("--jsonl")
    ap.add_argument("--istek-tavan", type=int, default=250, help="API arka ucunda yanıt başına 1 HTTP isteği (tekrarlar dahil)")
    ap.add_argument("--tsv-yaz", action="store_true", help="puanları kardeş <dizin>.tsv'ye jev/jev_guven sütunu olarak yaz")
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
    if ns.tsv_yaz and not ns.kuru:
        for d in map(Path, ns.dizinler):
            if (d.parent / f"{d.name}.tsv").exists():
                tsv_doldur(d.parent / f"{d.name}.tsv", [k for k in kayitlar if k["dosya"].startswith(f"{d.name}/")])
    if ns.jsonl:
        Path(ns.jsonl).write_text("".join(json.dumps(k, ensure_ascii=False) + "\n" for k in kayitlar), encoding="utf-8")


if __name__ == "__main__":
    main()
