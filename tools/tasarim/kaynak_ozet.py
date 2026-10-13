"""TASARIM-1 (1b): ham.tsv -> kaynak.tsv (tekil ad, video sayisi, sinif, link, ne, ornek video).
Kullanim: python -I kaynak_ozet.py <ham.tsv> <kaynak.tsv>
"""
import collections
import re
import sys

SINIF = [  # ilk eslesen kazanir
    ("font", r"\b(inter|geist|dm sans|outfit|poppins|montserrat|jetbrains mono|satoshi|manrope|fraunces|"
             r"playfair|space grotesk|instrument serif|general sans|clash|cabinet grotesk|ibm plex|google fonts|fontshare)\b"),
    ("galeri", r"awwwards|godly|dribbble|behance|pinterest|mobbin|land-book|lapa|saaspo|onepagelove|siteinspire|"
               r"refero|pageflows|cosmos|recent\.design|codrops|designprompts|httpster|minimal\.gallery"),
    ("skill/prompt", r"skill|design\.md|impeccable|taste|ui ux pro max|ui-ux-pro-max|prompt|frontend-design|claude design"),
    ("bilesen", r"shadcn|aceternity|magic ?ui|motion primitives|react bits|reactbits|origin ui|hyperui|flowbite|"
                r"daisyui|radix|mantine|chakra|cult ui|kokonut|skiper|uiverse|21st|lucide|heroicons|tabler|phosphor|ui kit"),
    ("hareket/3b", r"gsap|scrolltrigger|framer motion|motion\b|lenis|three|webgl|spline|lottie|rive|r3f|react three|"
                   r"unicorn|barba|locomotive|ogl|shader|tsparticles|anime\.js"),
    ("uretici", r"lovable|\bv0\b|stitch|bolt|framer\b|webflow|relume|figma|uizard|galileo|wix|durable|10web|replit"),
    ("css/cati", r"tailwind|css|next\.js|astro|svelte|vite|react|vue|nuxt|remix"),
]
DIS = re.compile(r"^(claude.*|chatgpt|github|npm|javascript|typescript|codex|cursor|opus.*|gemini.*|youtube|"
                 r"wordpress|canva|hostinger|elementor|astra|iclone.*|cascadeur|blender|remotion.*|starter templates|"
                 r"node\.?js|python|html|vs ?code|n8n|supabase|vercel|netlify)$")


def sinif(s):
    for ad, rx in SINIF:
        if re.search(rx, s, re.I):
            return ad
    return ""


def main():
    rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    g = collections.defaultdict(lambda: {"v": set(), "link": "", "ne": "", "tur": collections.Counter()})
    for r in rows:
        if r[1] != "aday":
            continue
        k = r[2].lower().strip()
        if DIS.match(k):
            continue
        d = g[k]
        d["v"].add(r[0])
        d["tur"][r[3]] += 1
        d["link"] = d["link"] or r[4]
        d["ne"] = d["ne"] or r[5][:140]
        d["ad"] = d.get("ad") or r[2]
    # tasarim depolarini url satirlarindan da al
    for r in rows:
        if r[1] in ("url", "aciklama"):
            m = re.match(r"(?:https?://)?(?:www\.)?github\.com/([\w.-]+/[\w.-]+)", r[4], re.I)
            if m and sinif(m.group(1)):
                k = m.group(1).lower().rstrip(".")
                d = g[k]
                d["v"].add(r[0])
                d["link"] = d["link"] or "https://github.com/" + m.group(1)
                d["ad"] = d.get("ad") or m.group(1)
                d["tur"]["repo"] += 1
    out = []
    for k, d in g.items():
        s = sinif(" ".join((k, d["link"], d["ne"])))
        if s and len(d["v"]) >= 2:
            out.append((d["ad"], str(len(d["v"])), s, d["tur"].most_common(1)[0][0], d["link"], d["ne"],
                        sorted(d["v"])[0]))
    out.sort(key=lambda x: (x[2], -int(x[1])))
    hdr = "ad\tvideo\tsinif\ttur\tlink\tne\tornek_video\n"
    open(sys.argv[2], "wb").write((hdr + "\n".join("\t".join(x) for x in out) + "\n").encode("utf-8"))
    print(f"satir={len(out)}", collections.Counter(x[2] for x in out))


if __name__ == "__main__":
    main()
