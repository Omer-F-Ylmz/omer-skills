"""TASARIM-1 (1a): video-tarama raporlarindan web tasarimi adaylarini toplar.
Kullanim: python -I kaynak_cikar.py <cikti.tsv> <rapor_dizini>...
Cikti: ham aday listesi (kaynak_video, bolum, ad, tur, link, ne) -- elle ayiklama girdisi.
"""
import pathlib
import re
import sys

KW = re.compile(
    r"web ?site|site\b|sitesi|landing|açılış sayfa|arayüz|\bui\b|\bux\b|frontend|front-end|ön ?yüz|ön ?uç|"
    r"tasarım|design|şablon|template|bileşen|component|tailwind|shadcn|figma|framer|spline|gsap|three\.?js|"
    r"webgl|lovable|\bv0\b|stitch|21st|aceternity|magic ?ui|animasyon|animation|tipograf|typograph|\bfont|"
    r"palet|palette|\bicon|ikon|\bcss\b|dribbble|awwwards|mobbin|godly|lottie|\brive\b|webflow|bolt\.new|"
    r"portfol|hero|parallax|scroll|motion|uiverse|codepen|unicorn|relume|wix|squarespace|wordpress|"
    r"mockup|wireframe|prototip|prototype|daisyui|chakra|radix|mantine|material ui|mui\b|bootstrap|"
    r"react bits|reactbits|magicui|cult ui|origin ui|hyperui|flowbite|land-book|lapa|saaspo|onepagelove|"
    r"siteinspire|refero|pageflows|cosmos\.so|pinterest|behance|kokonut|skiper|ui ?kit|tema\b|theme",
    re.I,
)
URL = re.compile(r"(?:https?://)?(?:[a-z0-9-]+\.)+[a-z]{2,}(?:/[^\s|)\]>\"'`]*)?", re.I)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def sections(lines):
    cur, out = None, {}
    for ln in lines:
        if ln.startswith("## "):
            cur = ln[3:].strip()
            out.setdefault(cur, [])
        elif cur:
            out[cur].append(ln)
    return out


def vid(p):
    s = p.stem
    s = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", s)
    return s


def main():
    out = pathlib.Path(sys.argv[1])
    rows, seen, nrep = [], set(), 0
    for root in sys.argv[2:]:
        for p in sorted(pathlib.Path(root).rglob("*.md")):
            txt = p.read_text(encoding="utf-8", errors="replace")
            sec = sections(txt.splitlines())
            if "Adaylar" not in sec:
                continue
            nrep += 1
            v = vid(p)
            for ln in sec.get("Adaylar", []):
                c = cells(ln)
                if len(c) < 5 or c[0] in ("ad", "") or set(c[0]) <= set("-"):
                    continue
                ad, tur, link, ne = c[0], c[2], c[3], c[4]
                if KW.search(" ".join((ad, link, ne))):
                    rows.append((v, "aday", ad, tur, "" if link == "yok" else link, ne))
            for ln in sec.get("URL'ler", []):
                c = cells(ln)
                if c and URL.fullmatch(c[0]):
                    rows.append((v, "url", "", "", c[0], ""))
            for ln in sec.get("Açıklama bağlantıları", []):
                for u in URL.findall(ln):
                    rows.append((v, "aciklama", "", "", u, ln.strip()[:160]))
            for name in ("Promptlar", "ek: tasarım"):
                for ln in sec.get(name, []):
                    s = ln.strip()
                    if s and s != "- yok" and not s.startswith("ikinci göz") and KW.search(s):
                        rows.append((v, name, "", "", "", s[:300]))
    uniq = []
    for r in rows:
        k = (r[0], r[2].lower(), r[4].lower(), r[5])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    out.write_bytes(
        ("\n".join("\t".join(x.replace("\t", " ") for x in r) for r in uniq) + "\n").encode("utf-8")
    )
    print(f"rapor={nrep} satir={len(uniq)}")


if __name__ == "__main__":
    main()
