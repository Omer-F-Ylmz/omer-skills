"""BEYIN-1 arama: `beyin ara "<soru>" --k 5` → birebir parça + kaynak yolu:satır (özet yok, model yok).

qmd'nin FTS5 indeksini salt-okur sorgular: qmd search katı AND olduğundan doğal dil
sorusu boş döner; burada terimler OR + önek (Türkçe ek için) ile BM25 sıralanır.
"""
import argparse
import itertools
import math
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
KAYNAK_TAVAN = 2  # ilk k parçada aynı kaynaktan en çok bu kadar
SNAP = 120  # pencerenin cümle sınırına genişleyebileceği en çok karakter
KAR_JETON = 3  # shortcut: Türkçe için ~3 karakter/jeton varsayımı, ölçüm sapıtırsa değiştir
KOMSU = 3 # arama sonucuna eklenen en fazla wikilink komşusu
# TR↔EN eş anlam (katlanmış kök → karşılık); kaynakların bir kısmı İngilizce (bellek, global CLAUDE.md)
# shortcut: elle küçük liste, yeni ıska sınıfı çıktıkça genişlet
ES = [("afis", "banner"), ("bayra", "flag"), ("esik", "threshold"), ("esig", "threshold"),
      ("kural", "rule"), ("oturu", "session"), ("kurul", "install"), ("komut", "command"),
      ("sinir", "limit"), ("tavan", "ceiling"), ("yasak", "never"), ("oncel", "priority"),
      ("sira", "order"), ("hata", "error"), ("onbel", "cache"), ("belle", "memory"),
      ("arali", "break"), ("degis", "change"), ("silme", "delete"), ("cakis", "conflict"),
      ("ozet", "summary"), ("yanit", "response"), ("arac", "tool"), ("okuma", "read"),
      ("arada", "break"), ("uzun", "long"), ("yeni", "new"), ("sonra", "after"),
      # ajan-sira sonuçları çoğunlukla İngilizce
      ("artim", "increment"), ("gunce", "update"), ("filtr", "filter"), ("acikl", "descript"),
      ("kopya", "duplic"), ("birle", "merg"), ("envan", "inventor"), ("kart", "card"),
      ("sonuc", "result"), ("maliy", "cost"), ("sure", "time"), ("sure", "duration"),
      ("olcum", "measur"), ("olcul", "measur"), ("kabul", "accept"), ("tohum", "seed"),
      ("kapi", "gate"), ("hakem", "judge"), ("soru", "question"), ("dogru", "correct"),
      ("yanli", "wrong"), ("hedef", "target"), ("tepe", "peak"), ("daral", "narrow"),
      ("alan", "area"), ("ilk", "first"), ("karar", "decision"), ("girdi", "input"),
      ("cikti", "output"), ("istek", "request"), ("surum", "version"), ("toplam", "total"),
      ("varsa", "default"), ("hasat", "harvest"), ("gorev", "task"), ("genis", "wide"), ("havuz", "pool"),
      ("secen", "option"), ("aday", "candidate"), ("secil", "pick"), ("secil", "select"), ("zinci", "chain"),
      ("ucret", "free"), ("dosya", "file"), ("satir", "line"), ("boyut", "size")]
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


def kimlikler(soru):
    """Sorudaki görev adı (ATLAS-1, ogren-4-d2) ve aşama (d1, g5, k13); katlanmış."""
    k = katla(soru)
    return list(dict.fromkeys(re.findall(r"\w+(?:-\w+)+", k) + re.findall(r"\b[dgk]\d+[a-z]?\b", k)))


def kimlik_puan(slug, ks, ids):
    """Not adında tam eşleşme 2, önek (d1→d1e) 1; gövdede birebir geçiş 1."""
    p = g = 0
    for i in ids:
        e = re.escape(i)
        p += 2 if re.search(rf"(?:^|-){e}(?:-|$)", slug) else 1 if re.search(rf"(?:^|-){e}", slug) else 0
        g += bool(re.search(rf"(?<![\w-]){e}(?![\w-])", ks))
    return p, g  # gövde geçişi içerik puanından sonra: aynı kaynağın başlık satırı kimlik geçen parçası içerik eşleşen parçayı ezmesin


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
    e = b + PENCERE
    # pencere cümleyi ortadan kesmesin: başı önceki cümle başına, sonu cümle sonuna ≤SNAP karakter genişler
    if b and (c := list(re.finditer(r"[.!?]\s+(?=[A-ZÇĞİÖŞÜ\d(`\"'*-])", satir[max(0, b - SNAP):b]))):
        b = max(0, b - SNAP) + c[-1].end()
    if e < len(satir) and (c := re.search(r"[.!?](?=\s)", satir[e:e + SNAP])):
        e += c.end()
    return ("… " if b else "") + satir[b:e] + (" …" if e < len(satir) else "")


def esle(x, ks):
    """Sayı terimi tam sayı olarak (2011 içinde 11 sayılmaz), diğerleri alt dize."""
    return bool(re.search(rf"(?<!\d){x}(?!\d)", ks)) if x.isdigit() else x in ks


def incele(yol, soru, ids=()):
    """Not → (frontmatter, gövde, katlanmış gövde, kavramlar, kimlik puanı, "kaç" mı) ya da None (geçersiz/MOC/boş)."""
    ts = terimler(soru)
    kav = [[t] + es(t) + [b for a, b in SATIR_ES if t.startswith(a)] for t in ts]
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
    kg = [katla(s) for s in govde]
    slug = re.sub(r"--\d+$", "", katla(Path(yol).stem))
    return fm, govde, kg, kav, kimlik_puan(slug, "\n".join(kg), ids), re.search(r"\bka[çc]", soru.lower()) is not None


def agirlik(notlar):
    """Kavram ağırlığı = ln(1 + N/df): adayların hepsinde geçen kavram (görev adı) az, nadir kavram çok sayılır."""
    n = len(notlar)
    return [math.log(1 + n / max(1, sum(any(esle(x, s) for s in d[2] for x in k) for d in notlar)))
            for k in (notlar[0][3] if notlar else [])]


def puanla(n, w):
    """Satır puanı = eşleşen kavramların ağırlık toplamı; "kaç" sorusunda rakamlı satıra yarım puan."""
    _, govde, kg, kav, _, sayisal = n
    return [sum(wi for wi, k in zip(w, kav) if any(esle(x, s) for x in k)) + (sayisal and bool(re.search(r"\d", g))) / 2
            for s, g in zip(kg, govde)]


def parca(yol, soru, esik=0, ids=()):
    """Notta en iyi pencereler: en yüksek puanlı satır ±, puanı ≥ en iyi−1 olan en fazla 2 ek satır; bölüm başlığı öne."""
    n = incele(yol, soru, ids)
    return n and pencereler(yol, n, puanla(n, [1.0] * len(n[3])), esik)


def pencereler(yol, n, puan, esik=0):
    fm, govde, _, kav, *_ = n
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
    out = [(fm.get("kaynak", yol), ilk + i, [pencere(s, hepsi) for s in govde[b:e]]) for b, e, i in birlesik]
    if birlesik[0][0] and govde[0].startswith("#"):  # pencere bölümün başında değil: başlığı öne ekle
        out[0][2].insert(0, govde[0])
    return out


def ara(soru, k=5, koleksiyon="beyin", indeks=INDEKS):
    vs = [v for v in varyantlar(soru) if v]
    if not vs:
        return []
    ids = kimlikler(soru)
    c = sqlite3.connect(f"file:{indeks}?mode=ro", uri=True)
    kok = c.execute("select path from store_collections where name=?", (koleksiyon,)).fetchone()
    if not kok:
        sys.exit(f"qmd koleksiyonu yok: {koleksiyon} (önce python tools/beyin_al.py)")
    listeler = [[y for (y,) in c.execute(
        "select d.path from documents_fts f join documents d on d.id=f.rowid "
        "where documents_fts match ? and d.collection=? and d.active=1 "
        "order by bm25(documents_fts, 3.0, 2.0, 1.0) limit ?",
        (" OR ".join(f'"{t}"*' for t in v), koleksiyon, k * 8))] for v in vs]
    # sırayla birleştirme (RRF değil): azınlık varyantın (EN) birincisi de ilk k'ya girer
    sira = dict.fromkeys(y for grup in itertools.zip_longest(*listeler) for y in grup if y)
    # görev adı not adında geçiyorsa (atlas-1 → ajan-atlas-1-d1e--2) FTS'e bakmadan aday
    for i in (i for i in ids if "-" in i):
        for (y,) in c.execute("select path from documents where collection=? and active=1 and path like ? limit 60",
                              (koleksiyon, f"%{i}%")):
            sira.setdefault(y, len(sira))
    havuz = [(yol, n) for yol in sira if (n := incele(os.path.join(kok[0], yol), soru, ids))]
    w = agirlik([n for _, n in havuz])
    degerli = []
    for pos, (yol, n) in enumerate(havuz):
        puan = puanla(n, w)
        tarih = int(re.sub(r"\D", "", n[0].get("guncellenme", "")) or 0)
        degerli.append(((-n[4][0], -max(puan), -n[4][1], -tarih, pos), yol, n, puan))
    degerli.sort(key=lambda x: x[0])
    sonuc, secilen, sayac = [], [], {}
    # aynı kaynaktan en çok KAYNAK_TAVAN parça: parçalanmış tek uzun kaynak ilk k'yı doldurup ikinci kaynağı (çok-notlu soru) dışarıda bırakmasın
    sec = []
    for x in degerli:
        s = x[2][0].get("kaynak", x[1])
        if len(sec) < k and sayac.get(s, 0) < KAYNAK_TAVAN:
            sayac[s] = sayac.get(s, 0) + 1
            sec.append(x)
    for _, yol, n, puan in sec + [x for x in degerli if x not in sec][:max(0, k - len(sec))]:
        sonuc += pencereler(yol, n, puan)
        secilen.append(Path(kok[0], yol))
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


def sigdir(sonuc, jeton):
    """Bütçe parçayı kesmez, parça sayısını sınırlar: ilk parça her zaman tam, sonrakiler yalnız bütünüyle sığarsa."""
    kalan, out = jeton * KAR_JETON, []
    for kaynak, no, satirlar in sonuc:
        metin = f"## {kaynak}:{no}\n" + "\n".join(satirlar)
        if out and len(metin) > kalan:
            continue
        out.append(metin)
        kalan -= len(metin)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="beyin")
    alt = ap.add_subparsers(dest="komut", required=True)
    a = alt.add_parser("ara")
    a.add_argument("soru")
    a.add_argument("--k", type=int, default=3)
    a.add_argument("--butce", type=int, help="çıktı jeton tavanı (varsayılan 200×k)")
    a.add_argument("-c", "--koleksiyon", default="beyin")
    ns = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    # "(1) … (2) …" çok parçalı soru: her parça ayrı aranır, sonuçlar sırayla birleşir (tek sorgu ikinci kaynağı dışarıda bırakır)
    parcalar = [p for p in re.split(r"\(\d+\)\s*", ns.soru) if p.strip()] if re.search(r"\(1\).*\(2\)", ns.soru, re.S) else [ns.soru]
    listeler = [ara(p, ns.k, ns.koleksiyon) for p in parcalar]
    gorulen, sonuc = set(), []
    for x in (x for grup in itertools.zip_longest(*listeler) for x in grup if x):
        if (x[0], x[1]) not in gorulen:
            gorulen.add((x[0], x[1]))
            sonuc.append(x)
    ns.butce = (ns.butce or 200 * ns.k) * len(parcalar)
    if not sonuc:
        print("sonuç yok")
    for metin in sigdir(sonuc, ns.butce or 200 * ns.k):
        print(metin + "\n")


if __name__ == "__main__":
    main()
