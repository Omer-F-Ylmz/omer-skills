"""YUKLE-12b: dist/yukle-12 aciklamalarini <=110'a indirir, cift skill'leri _cift'e ayirir, partileri 20'serli yeniden numaralar.
Girdi: .kos/kopru/y12b/rows.json (orijinal aciklamalar) + out*.json (yeni aciklamalar). Eski partiler dist/yukle-12-eski'ye tasinir."""
import json, re, shutil, zipfile
from pathlib import Path
K = Path(r"C:\Projeler\omer-skills"); D = K / "dist/yukle-12"; W = K / ".kos/kopru/y12b"
ESKI = K / "dist/yukle-12-eski"; YENI = K / "dist/yukle-12-yeni"
CIFT = {"skill-tdd": "tdd", "skill-council": "council", "deploy": "azure-deploy", "prepare": "azure-prepare"}
MAX = 110

rows = json.load(open(W / "rows.json", encoding="utf-8"))
yeni = {}
for f in W.glob("out*.json"):
    yeni.update(json.load(open(f, encoding="utf-8")))


def yaz_md(raw, ad, kisa, orig):
    t = raw.decode("utf-8")
    nl = "\r\n" if "\r\n" in t[:400] else "\n"
    m = re.match(r"^(\ufeff?---[ \t]*\r?\n)(.*?)(\r?\n---[ \t]*\r?\n)", t, re.S)
    sat = m.group(2).split("\n")
    out, i, atla = [], 0, False
    for s in sat:
        if s.startswith("description:"):
            out.append("description: " + json.dumps(kisa, ensure_ascii=False)); atla = True
        elif atla and s[:1] in (" ", "\t"):
            continue
        else:
            atla = False; out.append(s.rstrip("\r"))
    govde = t[m.end():]
    tam = "Tam açıklama: " + orig + nl + nl
    # ilk bos satirlardan sonra gelen govdenin basina ekle
    govde = govde.lstrip("\r\n")
    return (m.group(1) + nl.join(out) + m.group(3) + nl + tam + govde).encode("utf-8")


def main():
    for p in (YENI,):
        if p.exists(): shutil.rmtree(p)
    kalan, cift, eksik = [], [], []
    for r in rows:
        (cift if r["ad"] in CIFT else kalan).append(r)
    (D / "_cift").mkdir(exist_ok=True)
    for r in cift:
        shutil.copy2(D / r["parti"] / r["zip"], D / "_cift" / r["zip"])
    satir, once, sonra = [], 0, 0
    for i, r in enumerate(kalan):
        kisa = yeni.get(r["zip"])
        if not kisa:
            eksik.append(r["zip"]); kisa = r["orig"]
        if len(kisa) > MAX:  # ajan siniri asti: sozcuk sinirinda kes
            eksik.append(r["zip"]); kisa = kisa[:MAX + 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
        parti = "parti-%d" % (i // 20 + 1)
        (YENI / parti).mkdir(parents=True, exist_ok=True)
        zin = zipfile.ZipFile(D / r["parti"] / r["zip"])
        with zipfile.ZipFile(YENI / parti / r["zip"], "w", zipfile.ZIP_DEFLATED) as zo:
            for it in zin.infolist():
                b = zin.read(it.filename)
                if it.filename == r["ad"] + "/SKILL.md":
                    b = yaz_md(b, r["ad"], kisa, r["orig"])
                zo.writestr(it, b) if it.is_dir() else zo.writestr(it.filename, b)
        once += len(r["ad"]) + len(r["cur"].strip('"')); sonra += len(r["ad"]) + len(kisa)
        satir.append("\t".join([parti, r["kat"], r["plugin"], r["ad"], r["zip"], str(len(kisa))]))
    (YENI / "_satirlar.tsv").write_text("parti\tkat\tplugin\tad\tzip\tadaciklama_kar\n" + "\n".join(satir), encoding="utf-8")
    (YENI / "_cift.txt").write_text("\n".join("%s\t(tutulan: %s)" % (r["zip"], CIFT[r["ad"]]) for r in cift), encoding="utf-8")
    print("zip", len(kalan), "cift", len(cift), "parti", (len(kalan) + 19) // 20, "eksik/uzun", len(eksik), eksik[:5], "kar once", once, "sonra", sonra)


main()
