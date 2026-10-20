"""BEYIN-1 arama: `beyin ara "<soru>" --k 5` → birebir parça + kaynak yolu:satır (özet yok, model yok).

qmd'nin FTS5 indeksini salt-okur sorgular: qmd search katı AND olduğundan doğal dil
sorusu boş döner; burada terimler OR + önek (Türkçe ek için) ile BM25 sıralanır.
"""
import argparse
import itertools
import os
import re
import sqlite3
import sys
from pathlib import Path

INDEKS = Path.home() / ".cache/qmd/index.sqlite"
DUR = set("""ne neyi nedir neler mi mı mu mü midir mıdır hangi hangisi nasıl kaç için ile ve veya
ya da de bir bu şu o olan olarak neden nerede nereye kim ise gibi daha en çok var yok mevcut
the a an of to is what which how""".split())
TR = str.maketrans("ıİçÇğĞöÖşŞüÜâÂîÎ", "iiccggoossuuaaii")
PENCERE = 400  # uzun satırda gösterilen karakter
KOMSU = 3  # arama sonucuna eklenen en fazla wikilink komşusu
# TR↔EN eş anlam (katlanmış kök → karşılık); kaynakların bir kısmı İngilizce (bellek, global CLAUDE.md)
# shortcut: elle küçük liste, yeni ıska sınıfı çıktıkça genişlet
ES = [("afis", "banner"), ("bayra", "flag"), ("esik", "threshold"), ("esig", "threshold"),
      ("kural", "rule"), ("oturu", "session"), ("kurul", "install"), ("komut", "command"),
      ("sinir", "limit"), ("tavan", "ceiling"), ("yasak", "never"), ("oncel", "priority"),
      ("sira", "order"), ("hata", "error"), ("onbel", "cache"), ("belle", "memory"),
      ("arali", "break"), ("degis", "change"), ("silme", "delete"), ("cakis", "conflict"),
      ("ozet", "summary"), ("yanit", "response"), ("arac", "tool"), ("okuma", "read"),
      ("arada", "break"), ("uzun", "long"), ("yeni", "new"), ("sonra", "after")]
SATIR_ES = [("fazla", "≤"), ("tavan", "≤")]  # yalnız satır puanında; FTS'de simge yok


def katla(s):
    return s.translate(TR).lower()


def es(t):
    return [b for a, b in ES if t.startswith(a)] + [a for a, b in ES if t.startswith(b)]


def varyantlar(soru):
    """[özgün terimler, 4 harf kökler, terimler + eş anlamlar] — her biri ayrı FTS sorgusu."""
    ts = terimler(soru)
    kok = list(dict.fromkeys(t[:4] if len(t) > 4 and t.isalpha() else t for t in ts))
    # 4.: eş anlamı olan TR terim yerine EN karşılığı (İngilizce kaynak BM25'te TR terimlerle boğulmasın)
    en = list(dict.fromkeys(e for t in ts for e in es(t)))
    # FTS unicode61 'ı'yı katlamaz (ş/ç/ğ katlanır): 'ı'lı soruda katlanmamış terimler de sorulur
    ham = [w[:5] for w in re.findall(r"\w+", soru.lower()) if "ı" in w and w not in DUR]
    return [ts, kok, list(dict.fromkeys(ts + [e for t in ts for e in es(t)])), en] + ([ham] if ham else [])


def terimler(soru):
    out = []
    for w in re.findall(r"\w+", soru.lower()):
        if w in DUR or (len(w) < 3 and not any(c.isdigit() for c in w)):
            continue
        k = katla(w)
        k = k[:5] if len(k) > 5 and not any(c.isdigit() for c in k) else k
        if k not in out:
            out.append(k)
    return out


def pencere(satir, ts):
    if len(satir) <= PENCERE:
        return satir
    ks = katla(satir)
    konum = [m.start() for t in ts for m in re.finditer(re.escape(t), ks)]
    if not konum:
        return satir[:PENCERE] + " …"
    # terimlerin en yoğun olduğu yeri merkez al
    m = max(konum, key=lambda p: sum(abs(q - p) < PENCERE // 2 for q in konum))
    b = max(0, m - PENCERE // 2)
    return ("… " if b else "") + satir[b:b + PENCERE] + (" …" if b + PENCERE < len(satir) else "")


def parca(yol, soru, esik=0):
    """Notta en iyi pencereler: en yüksek puanlı satır ±, puanı ≥ en iyi−1 olan en fazla 2 ek satır."""
    ts = terimler(soru)
    kav = [[t] + es(t) + [b for a, b in SATIR_ES if t.startswith(a)] for t in ts]
    sayisal = re.search(r"\bka[çc]", soru.lower()) is not None
    metin = Path(yol).read_text(encoding="utf-8", errors="replace").split("\n")
    if metin[0] != "---":
        return None
    son = metin.index("---", 1)
    fm = dict(s.split(": ", 1) for s in metin[1:son] if ": " in s)
    if fm.get("gecersiz") == "true" or fm.get("tur") == "moc":
        return None
    govde = metin[son + 1:]
    while govde and (not govde[-1].strip() or govde[-1].startswith(("[[", "Bağlar:"))):
        govde.pop()
    if not govde:
        return None
    # satır puanı = eşleşen kavram sayısı; "kaç" sorusunda rakamlı satıra yarım puan
    puan = [sum(any(x in katla(s) for x in k) for k in kav) + (sayisal and bool(re.search(r"\d", s))) / 2
            for s in govde]
    sira = sorted(range(len(govde)), key=lambda j: (-puan[j], j))
    if puan[sira[0]] < esik:
        return None
    secim = [sira[0]] + [j for j in sira[1:3] if puan[j] > 0 and puan[j] >= puan[sira[0]] - 1]
    # ilk pencere i-1..i+2, ekler i..i+1; çakışan/bitişik birleşir; numara = en iyi isabet satırı
    araliklar = sorted([max(0, i - (n == 0)), min(len(govde), i + (3 if n == 0 else 2)), i]
                       for n, i in enumerate(secim))
    birlesik = [araliklar[0]]
    for b, e, i in araliklar[1:]:
        if b <= birlesik[-1][1]:
            birlesik[-1][1] = max(birlesik[-1][1], e)
            birlesik[-1][2] = min(birlesik[-1][2], i, key=lambda j: (-puan[j], j))
        else:
            birlesik.append([b, e, i])
    ilk = int(fm.get("satir", 1))
    hepsi = [x for k in kav for x in k]
    return [(fm.get("kaynak", yol), ilk + i, [pencere(s, hepsi) for s in govde[b:e]])
            for b, e, i in birlesik]


def ara(soru, k=5, koleksiyon="beyin", indeks=INDEKS):
    vs = [v for v in varyantlar(soru) if v]
    if not vs:
        return []
    c = sqlite3.connect(f"file:{indeks}?mode=ro", uri=True)
    kok = c.execute("select path from store_collections where name=?", (koleksiyon,)).fetchone()
    if not kok:
        sys.exit(f"qmd koleksiyonu yok: {koleksiyon} (önce python tools/beyin_al.py)")
    listeler = [[y for (y,) in c.execute(
        "select d.path from documents_fts f join documents d on d.id=f.rowid "
        "where documents_fts match ? and d.collection=? and d.active=1 "
        "order by bm25(documents_fts, 1.0, 2.0, 1.0) limit ?",
        (" OR ".join(f'"{t}"*' for t in v), koleksiyon, k * 3))] for v in vs]
    # sırayla birleştirme (RRF değil): azınlık varyantın (EN) birincisi de ilk k'ya girer
    sira = dict.fromkeys(y for grup in itertools.zip_longest(*listeler) for y in grup if y)
    sonuc, secilen = [], []
    for yol in sira:
        p = parca(os.path.join(kok[0], yol), soru)
        if p:
            sonuc += p
            secilen.append(Path(kok[0], yol))
        if len(secilen) == k:
            break
    # 1 adım wikilink komşusu: seçilen notların "Bağlar:" hedefleri, soruyla ≥1 kavram eşleşirse
    adlar = {p.stem.lower(): p for p in Path(kok[0]).rglob("*.md")}
    gorulen = {str(p).lower() for p in secilen}
    n = 0
    for yol in secilen:
        for ad in baglar(yol):
            p = adlar.get(ad.lower())
            if n == KOMSU or not p or str(p).lower() in gorulen:
                continue
            gorulen.add(str(p).lower())
            r = parca(p, soru, esik=1)
            if r:
                sonuc += r
                n += 1
    return sonuc


def baglar(yol):
    for s in reversed(Path(yol).read_text(encoding="utf-8", errors="replace").split("\n")):
        if s.startswith("Bağlar:"):
            return re.findall(r"\[\[([^\]|#]+)", s)
    return []


def main(argv=None):
    ap = argparse.ArgumentParser(prog="beyin")
    alt = ap.add_subparsers(dest="komut", required=True)
    a = alt.add_parser("ara")
    a.add_argument("soru")
    a.add_argument("--k", type=int, default=5)
    a.add_argument("-c", "--koleksiyon", default="beyin")
    ns = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    sonuc = ara(ns.soru, ns.k, ns.koleksiyon)
    if not sonuc:
        print("sonuç yok")
    for kaynak, no, satirlar in sonuc:
        print(f"## {kaynak}:{no}")
        print("\n".join(satirlar))
        print()


if __name__ == "__main__":
    main()
