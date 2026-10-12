"""birlesik.tsv + metab.tsv → .kos/kopru/devir/<alan>.tsv ön sınıflama (anahtar kelime; kararı ilgili ajan verir)."""
import pathlib, re

D = pathlib.Path(__file__).parent
OUT = pathlib.Path(r"C:\Projeler\omer-skills\.kos\kopru\devir")
ALAN = {  # sıra önemli: ilk eşleşen alan
    "blender-2": r"blender|\b3d\b|glb|gltf|mesh|render|hunyuan3d|meshy|tripo",
    "router-1": r"router|yönlendir|model seç|model routing|openrouter|litellm",
    "fable-1": r"fable|düşünme|thinking|ajan protokol|agent protocol|persona",
    "animasyon-1": r"animasyon|animation|motion|gsap|lottie|rive|efekt|effect|scroll|remotion|shader|parallax",
    "tasarim-1": r"tasarım|design|\bui\b|\bux\b|landing|site|figma|tailwind|font|tipograf|renk|color|stitch|v0|lovable|slop|görsel prompt|image prompt",
}
meta = {}
for s in (D / "metab.tsv").read_text(encoding="utf-8").splitlines():
    h = s.split("\t")
    meta[h[0]] = h + ["-"] * (12 - len(h))
satirlar = [s.split("\t") for s in (D / "birlesik.tsv").read_text(encoding="utf-8").splitlines()[1:]]
cikti = {a: [] for a in ALAN}
for h in satirlar:
    anahtar, ad, tur, link, gonderi, iddia = (h + [""] * 6)[:6]
    metin = f"{ad} {iddia}".lower()
    alan = next((a for a, r in ALAN.items() if re.search(r, metin)), None)
    if not alan:
        continue
    m = meta.get(anahtar)
    repo, lisans, yildiz, push, arsiv = (m[3], m[5], m[6], m[7], m[8]) if m and m[4] != "bulunamadı" else ("-",) * 5
    cikti[alan].append("\t".join([anahtar, ad, tur, link or (f"https://github.com/{repo}" if repo != "-" else "-"),
                                  gonderi, iddia, repo, lisans, yildiz, push, arsiv, "on-sinif:anahtar-kelime"]))
bas = "anahtar\tad\ttur\tlink\tgonderi\tiddia\trepo\tlisans\tyildiz\tpush\tarsiv\tnot\n"
for a, L in cikti.items():
    (OUT / f"{a}.tsv").write_text(bas + "\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(a, len(L))
print("devir toplam", sum(map(len, cikti.values())), "/", len(satirlar))
