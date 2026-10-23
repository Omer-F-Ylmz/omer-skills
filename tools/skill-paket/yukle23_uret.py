"""SKILL-YUKLE-1: envanter-fark.tsv'deki eksik skill'leri aile paketlerine (plugin başına, kişisel skill'ler 40'lık) sıkıştırır,
20'şerli grup klasörlerine koyar, YUKLE.md ve eşleme TSV'sini yazar.
Kullanım: python yukle23_uret.py <envanter-fark.tsv> <cikti_dizini>"""
import csv, re, sys, shutil, pathlib, collections

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from paketle import buyuk
from zip_denetle import denetle


def ad_temiz(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-").replace("claude", "cc").replace("anthropic", "anth")
    return s[:40]


def main(argv):
    tsv, cikti = argv[0], pathlib.Path(argv[1])
    satirlar = list(csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t"))
    aile = collections.OrderedDict()
    kisisel = []
    for r in satirlar:
        if r["kaynak"].startswith("~"):
            kisisel.append(r)
        else:
            aile.setdefault(r["kaynak"].split("@")[0], []).append(r)
    for i in range(0, len(kisisel), 40):
        aile[f"kisisel-{i // 40 + 1}"] = kisisel[i:i + 40]
    ham = cikti / "_ham"
    shutil.rmtree(ham, ignore_errors=True)
    for eski in cikti.glob("grup-*"):
        shutil.rmtree(eski, ignore_errors=True)
    sonuc, esle = [], []
    for k, uyeler in aile.items():
        ad = "y23-" + ad_temiz(k)
        uyeler = [u for u in uyeler if "SKILL.md" in {x.name for x in pathlib.Path(u["yol"]).iterdir()}]
        # aynı dizin adı iki kez olamaz: tekrarları ayrı alt gruplara dağıt
        gruplar = []
        for u in uyeler:
            ad_u = pathlib.Path(u["yol"]).name
            for g in gruplar:
                if ad_u not in {pathlib.Path(x["yol"]).name for x in g}:
                    g.append(u); break
            else:
                gruplar.append([u])
        for gi, g in enumerate(gruplar):
            ad_g = ad if len(gruplar) == 1 else f"{ad}-d{gi + 1}"
            try:
                for zp, n in buyuk(ad_g, f"{k} eklentisi, {len(g)} skill", [u["yol"] for u in g], ham):
                    sonuc.append((pathlib.Path(zp), n, k, len(g)))
            except Exception as e:
                print("HATA", k, str(e)[:120])
                sonuc.append((None, 0, k, len(g), str(e)[:200]))
        for u in uyeler:
            esle.append((u["ad"], k, ad))
    zipler = sorted(s[0] for s in sonuc if s[0])
    govde = ["# SKILL-YUKLE-1 · claude.ai yükleme sırası", "",
             "Her grup klasörü ≤20 zip; sırayla yükle. Hepsi YENİ paket (y23- öneki); mevcut paketleri etkilemez.", ""]
    for gi in range(0, len(zipler), 20):
        g = cikti / f"grup-{gi // 20 + 1:02d}"
        g.mkdir(parents=True, exist_ok=True)
        govde.append(f"## grup-{gi // 20 + 1:02d}")
        for z in zipler[gi:gi + 20]:
            shutil.copy2(z, g / z.name)
            s = next(x for x in sonuc if x[0] == z)
            govde.append(f"- {z.name} ({s[2]}, {s[3]} skill)")
        govde.append("")
    hata = [s for s in sonuc if not s[0]]
    if hata:
        govde += ["## YÜKLENEMEYEN (paketlenemedi)"] + [f"- {s[2]}: {s[4]}" for s in hata]
    (cikti / "YUKLE.md").write_text("\n".join(govde) + "\n", encoding="utf-8")
    with open(cikti / "esleme.tsv", "w", encoding="utf-8", newline="") as o:
        w = csv.writer(o, delimiter="\t", lineterminator="\n")
        w.writerow(["skill", "aile", "paket"])
        w.writerows(esle)
    print(f"skill {len(satirlar)} · aile {len(aile)} · zip {len(zipler)} · hata {len(hata)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
