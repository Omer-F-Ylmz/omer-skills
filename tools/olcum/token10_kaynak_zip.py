"""TOKEN-10 iş 5: esleme.tsv'deki sıkışmış description'ı repo kaynaklarına (ajanlar/**, skills/departman-*/ajanlar/**) ve
claude.ai departman zip'lerine yazar; başka bayt değişmez.
  python token10_kaynak_zip.py kaynak   → wt kaynak dosyaları (yalnız açıklaması canlı 'eski' ile aynı olanlar)
  python token10_kaynak_zip.py zip      → <ana repo>/dist/token-10/*.zip + LISTE.md (taban: yukle-kapi25, yoksa skill-secim-1/kendi)"""
import io, sys, zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
sys.path.insert(0, str(Path(__file__).parent))
from ajan_aciklama import aciklama, aciklama_degistir, kaynaklar

WT = Path(__file__).resolve().parents[2]
DIST = Path("C:/Projeler/omer-skills/dist")
ES = {s.split("\t")[0]: s.split("\t")[1:3] for s in (WT / "docs/token-10/esleme.tsv").read_text(encoding="utf8").splitlines()[1:]}


def kaynak():
    n = farkli = 0
    for ad, yollar in kaynaklar(WT).items():
        if ad not in ES:
            continue
        for p in yollar:
            m = p.read_bytes().decode("utf8")
            if aciklama(m) != ES[ad][0]:
                farkli += 1  # kaynak canlıdan ayrışmış: B'de sınanan metin bu değil, dokunulmaz
                continue
            p.write_bytes(aciklama_degistir(m, ES[ad][1]).encode("utf8"))
            n += 1
    print("kaynak değişen", n, "· canlıdan farklı (dokunulmadı)", farkli)


def zipler():
    cik = DIST / "token-10"
    cik.mkdir(exist_ok=True)
    taban = {z.name: z for z in (DIST / "skill-secim-1/kendi").glob("*.zip")}
    taban.update({z.name: z for z in (DIST / "yukle-kapi25").glob("*.zip")})
    liste = ["# TOKEN-10 departman zip'leri — yalnız ajanlar/*.md frontmatter description satırı değişti, dosya kaybı 0", "",
             "zip · taban · dosya · değişen açıklama · taban açıklaması canlıdan farklı"]
    for ad, z in sorted(taban.items()):
        buf, deg, fark = io.BytesIO(), 0, 0
        with zipfile.ZipFile(z) as zi, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zo:
            for bi in zi.infolist():
                veri = zi.read(bi)
                st = Path(bi.filename).stem
                if "/ajanlar/" in bi.filename and bi.filename.endswith(".md") and st in ES:
                    m = veri.decode("utf8")
                    fark += aciklama(m) != ES[st][0]
                    y = aciklama_degistir(m, ES[st][1])
                    deg += y != m
                    veri = y.encode("utf8")
                zo.writestr(bi, veri)
        (cik / ad).write_bytes(buf.getvalue())
        with zipfile.ZipFile(z) as a, zipfile.ZipFile(cik / ad) as b:  # öz-denetim: ad listesi aynı, ajan dışı bayt aynı
            assert a.namelist() == b.namelist(), ad
            assert all(a.read(x) == b.read(x) for x in a.namelist() if "/ajanlar/" not in x), ad
        liste.append(f"- {ad} · {z.parent.name} · {len(zi.namelist())} · {deg} · {fark}")
    (cik / "LISTE.md").write_text("\n".join(liste) + "\n", encoding="utf8")
    print("\n".join(liste[2:]))


if __name__ == "__main__":
    {"kaynak": kaynak, "zip": zipler}[sys.argv[1]]()
