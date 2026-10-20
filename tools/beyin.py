"""BEYIN-1 arama: `beyin ara "<soru>" --k 5` → birebir parça + kaynak yolu:satır (özet yok, model yok).

qmd'nin FTS5 indeksini salt-okur sorgular: qmd search katı AND olduğundan doğal dil
sorusu boş döner; burada terimler OR + önek (Türkçe ek için) ile BM25 sıralanır.
"""
import argparse
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


def katla(s):
    return s.translate(TR).lower()


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


def parca(yol, ts):
    metin = Path(yol).read_text(encoding="utf-8", errors="replace").split("\n")
    if metin[0] != "---":
        return None
    son = metin.index("---", 1)
    fm = dict(s.split(": ", 1) for s in metin[1:son] if ": " in s)
    if fm.get("gecersiz") == "true":
        return None
    govde = metin[son + 1:]
    while govde and (not govde[-1].strip() or govde[-1].startswith("[[")):
        govde.pop()
    if not govde:
        return None
    puan = [sum(t in katla(s) for t in ts) for s in govde]
    i = max(range(len(govde)), key=lambda j: puan[j])
    bas, bit = max(0, i - 1), min(len(govde), i + 3)
    no = int(fm.get("satir", 1)) + i
    return fm.get("kaynak", yol), no, [pencere(s, ts) for s in govde[bas:bit]]


def ara(soru, k=5, koleksiyon="beyin", indeks=INDEKS):
    ts = terimler(soru)
    if not ts:
        return []
    sorgu = " OR ".join(f'"{t}"*' for t in ts)
    c = sqlite3.connect(f"file:{indeks}?mode=ro", uri=True)
    kok = c.execute("select path from store_collections where name=?", (koleksiyon,)).fetchone()
    if not kok:
        sys.exit(f"qmd koleksiyonu yok: {koleksiyon} (önce python tools/beyin_al.py)")
    satirlar = c.execute(
        "select d.path from documents_fts f join documents d on d.id=f.rowid "
        "where documents_fts match ? and d.collection=? and d.active=1 "
        "order by bm25(documents_fts, 1.0, 2.0, 1.0) limit ?", (sorgu, koleksiyon, k * 3)).fetchall()
    sonuc = []
    for (yol,) in satirlar:
        p = parca(os.path.join(kok[0], yol), ts)
        if p:
            sonuc.append(p)
        if len(sonuc) == k:
            break
    return sonuc


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
