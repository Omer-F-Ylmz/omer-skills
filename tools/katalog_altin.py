"""ENVANTER-2 d5: havuzlanmış altın küme + kesinlik/geri çağırma ölçüsü (20 ayar / 10 sınama iş).
python tools/katalog_altin.py havuz      → .claude/envanter2-altin/parti{k}.tsv (kör, karışık aday havuzu)
python tools/katalog_altin.py birlestir  → okuyucu a/b (+c) işaretleri → docs/katalog/altin.jsonl (+ anlaşmazlık partisi c.tsv)
python tools/katalog_altin.py olc        → ayar/sınama kesinlik + geri çağırma
Okuyucu çıktısı: .claude/envanter2-altin/{a,b,c}{k}.tsv, satır "kimlik<TAB>1|0<TAB>gerekçe".
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
import katalog_ara  # noqa: E402
from test_katalog_ara import ISLER  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
GECICI = KOK / ".claude" / "envanter2-altin"
ALTIN = KOK / "docs" / "katalog" / "altin.jsonl"
PARTI, BM25_ILK, TUR_ILK = 6, 80, 10


def anahtar(o):
    return f"{o['tur']}:{o['ad']}"


def kume(i):
    return "sinama" if i % 3 == 2 else "ayar"


def satirlar():
    return [json.loads(s) for s in katalog_ara.KATALOG.read_text(encoding="utf8").splitlines()]


def havuz():
    rows = satirlar()
    GECICI.mkdir(parents=True, exist_ok=True)
    for k in range(0, len(ISLER), PARTI):
        cikti = []
        for i in range(k, min(k + PARTI, len(ISLER))):
            q, beklenen = ISLER[i]
            puan = [o for _, _, o in katalog_ara.puanla(q, satirlar=rows)[0]]
            aday = {anahtar(o): o for o in puan[:BM25_ILK] + katalog_ara.ara(q, satirlar=rows)}
            aday |= {anahtar(o): o for o in rows if o["ad"] in beklenen}
            for t in katalog_ara.GRUP:
                aday |= {anahtar(o): o for o in [o for o in puan if o["tur"] == t][:TUR_ILK]}
            sira = sorted(aday)
            random.Random(i).shuffle(sira)  # kör: kaynak (BM25/beklenen/çıktı) sırayla sızmasın
            cikti.append(f"### İŞ {i}: {q}")
            cikti += [f"{i}.{n}\t{aday[a]['tur']}\t{aday[a]['ad']}\t{(aday[a]['is'] or aday[a]['metin'])[:200]}"
                      for n, a in enumerate(sira)]
        (GECICI / f"parti{k // PARTI}.tsv").write_text("\n".join(cikti) + "\n", encoding="utf8")
        print(f"parti{k // PARTI}: {sum(1 for s in cikti if not s.startswith('###'))} aday")


def isaretler(harf):
    d = {}
    for f in GECICI.glob(f"{harf}[0-9]*.tsv"):
        for s in f.read_text(encoding="utf8").splitlines():
            p = s.split("\t")
            if len(p) >= 2 and p[1].strip() in ("0", "1"):
                d[p[0].strip()] = p[1].strip() == "1"
    return d


def birlestir():
    aday = {}
    for f in sorted(GECICI.glob("parti*.tsv")):
        for s in f.read_text(encoding="utf8").splitlines():
            if not s.startswith("###"):
                kim, tur, ad, metin = s.split("\t")
                aday[kim] = (f"{tur}:{ad}", s)
    a, b, c = isaretler("a"), isaretler("b"), isaretler("c")
    eksik = [k for k in aday if k not in a or k not in b]
    ayri = [k for k in aday if k in a and k in b and a[k] != b[k]]
    acik = [k for k in ayri if k not in c]
    if acik:
        (GECICI / "c.tsv").write_text("\n".join(aday[k][1] for k in acik) + "\n", encoding="utf8")
    print(f"aday {len(aday)} · eksik işaret {len(eksik)} · anlaşma {1 - len(ayri) / max(len(aday) - len(eksik), 1):.3f}"
          f" · ayrışan {len(ayri)} · 3. okuyucu bekleyen {len(acik)}")
    if eksik or acik:
        return
    satir = []
    for i, (q, _) in enumerate(ISLER):
        kendi = [k for k in aday if k.split(".")[0] == str(i)]
        karar = {k: (c[k] if k in ayri else a[k]) for k in kendi}
        satir.append(json.dumps({"i": i, "is": q, "kume": kume(i),
                                 "altin": sorted(aday[k][0] for k in kendi if karar[k]),
                                 "degil": sorted(aday[k][0] for k in kendi if not karar[k])}, ensure_ascii=False))
    ALTIN.write_text("\n".join(satir) + "\n", encoding="utf8")
    print(f"{ALTIN.name}: ort. altın {sum(len(json.loads(s)['altin']) for s in satir) / len(satir):.1f}/iş")


def olc(ara=None, yaz=True):
    """Mikro kesinlik = Σ|sonuç∩altın|/Σ|sonuç|, geri çağırma = Σ|sonuç∩altın|/Σ|altın|; havuz dışı sonuç ilgisiz sayılır."""
    rows, ara = satirlar(), ara or (lambda q, rows: katalog_ara.ara(q, satirlar=rows))
    t = {k: [0, 0, 0, 0] for k in ("ayar", "sinama")}  # kesişim, sonuç, altın, yargısız
    for s in ALTIN.read_text(encoding="utf8").splitlines():
        g = json.loads(s)
        sonuc, altin = {anahtar(o) for o in ara(g["is"], rows)}, set(g["altin"])
        for j, v in enumerate((len(sonuc & altin), len(sonuc), len(altin), len(sonuc - altin - set(g["degil"])))):
            t[g["kume"]][j] += v
        if yaz and "-v" in sys.argv:
            print(f"{g['i']:2} K {len(sonuc & altin)}/{len(sonuc)} G {len(sonuc & altin)}/{len(altin)} · eksik {sorted(altin - sonuc)[:4]}")
    sonuc = {k: (v[0] / max(v[1], 1), v[0] / max(v[2], 1), v[3]) for k, v in t.items()}
    if yaz:
        for k, (p, r, y) in sonuc.items():
            print(f"{k}: kesinlik {p:.3f} · geri çağırma {r:.3f} · yargısız sonuç {y}")
    return sonuc


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"havuz": havuz, "birlestir": birlestir, "olc": olc}[sys.argv[1]]()
