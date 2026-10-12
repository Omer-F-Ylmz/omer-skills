"""birlesik.tsv + metab.tsv → sirali.tsv: değer = kullanım alanı etkisi × kurulum kolaylığı × güven (deterministik).
Kurulu satırlar ayrı (karar KUR/kurulu); sıralama yalnız yeni adaylar için anlamlı."""
import math, pathlib, re

D = pathlib.Path(__file__).parent
TUR = {"skill": 3, "plugin": 3, "MCP": 3, "CLI": 2.5, "kütüphane": 2, "iş akışı": 2, "prompt": 1.5, "site": 1, "teknik": 1}
ETKI = [(r"claude code|\bcc\b|token|context|bağlam|skill|subagent|alt ajan|\bagent|ajan|mcp|hook|prompt cach|maliyet|cost", 2.0),
        (r"frontend|\bui\b|tasarım|design|three|\b3d\b|blender|animasyon|animation|video|ffmpeg|\.net|c#|dotnet|test|güvenlik|security", 1.5)]
IZINLI = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0", "CC0-1.0", "Unlicense", "0BSD"}
DEVIR = {  # devir_on.py ile aynı sıra/kalıp
    "blender": r"blender|\b3d\b|glb|gltf|mesh|render|hunyuan3d|meshy|tripo",
    "router": r"router|yönlendir|model seç|model routing|openrouter|litellm",
    "fable": r"fable|düşünme|thinking|ajan protokol|agent protocol|persona",
    "animasyon": r"animasyon|animation|motion|gsap|lottie|rive|efekt|effect|scroll|remotion|shader|parallax",
    "tasarim": r"tasarım|design|\bui\b|\bux\b|landing|site|figma|tailwind|font|tipograf|renk|color|stitch|v0|lovable|slop|görsel prompt|image prompt",
}


def puan(tur, metin, n_gonderi, m):
    etki = next((k for r, k in ETKI if re.search(r, metin)), 1.0)
    if m is None or m[4] == "bulunamadı":
        guven, kolay = 0.5, 0.5  # repo çözülmedi: kurulamaz hâli
    else:
        lisans, yildiz, push, arsiv = m[5], m[6], m[7], m[8]
        guven = (1.0 if lisans in IZINLI else 0.6) + math.log10(int(re.sub(r"\D", "", yildiz) or 0) + 1) / 5
        guven += 0.2 if push >= "2026-07-12" else 0
        guven *= 0.2 if arsiv not in ("-", "", "h") else 1
        kolay = 1.0
    return TUR.get(tur, 1) * etki * min(1 + 0.5 * (n_gonderi - 1), 3) * guven * kolay


def main():
    meta = {h[0]: h + ["-"] * (12 - len(h)) for h in (s.split("\t") for s in (D / "metab.tsv").read_text(encoding="utf-8").splitlines())}
    satirlar = [s.split("\t") for s in (D / "birlesik.tsv").read_text(encoding="utf-8").splitlines()[1:]]
    cikti = []
    for anahtar, ad, tur, link, gonderi, iddia in satirlar:
        m = meta.get(anahtar)
        metin = f"{ad} {iddia}".lower()
        devir = next((a for a, r in DEVIR.items() if re.search(r, metin)), "-")
        bizde = m[10] if m and m[10] != "yok" else "yok"
        repo = m[3] if m and m[4] != "bulunamadı" else "-"
        p = puan(tur, metin, len(gonderi.split(",")), m)
        cikti.append((p, [anahtar, ad, tur, repo, m[5] if repo != "-" else "-", m[6] if repo != "-" else "-",
                          bizde, devir, gonderi, iddia]))
    # sıra: yeni + devirsiz önce (bu oturumun işi), sonra devir, en son kurulu
    grup = lambda r: 2 if r[6] != "yok" else (1 if r[7] != "-" else 0)
    cikti.sort(key=lambda x: (grup(x[1]), -x[0]))
    bas = "sira\tpuan\tanahtar\tad\ttur\trepo\tlisans\tyildiz\tbizde\tdevir\tgonderi\tiddia\n"
    (D / "sirali.tsv").write_text(bas + "".join(f"{i}\t{p:.2f}\t" + "\t".join(r) + "\n" for i, (p, r) in enumerate(cikti, 1)),
                                  encoding="utf-8", newline="\n")
    from collections import Counter
    print(len(cikti), Counter(grup(r) for _, r in cikti))


if __name__ == "__main__":
    assert puan("skill", "claude code token", 1, None) > puan("teknik", "genel", 1, None)
    main()
