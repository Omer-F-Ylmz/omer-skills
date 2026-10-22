"""KURULUM-REEL-D: ig-41 kalemlerini tek tek durumlandırır → .kos/kopru/kurulum-reel-durum.tsv.

Durumlar: kurulu (CC'de etkin, ad doğrulandı) · proje-sablon · ref (yalnız referans) · hesap (hesap gerekir)
· ret (gerekçeyle) · kurulamaz. Bilinmeyen kalem `ret` olmaz; `?` ile işaretlenir ve betik hata verir.
Kullanım: python tools/kurulum_durum.py
"""
import json
import os
import pathlib
import subprocess
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
KOPRU = KOK / ".kos" / "kopru"
CIKTI = KOPRU / "kurulum-reel-durum.tsv"
TSVLER = ["ig-41-frontend-siteler.tsv", "ig-41-blender.tsv", "ig-41-laya.tsv"]
HOME = pathlib.Path(os.path.expanduser("~"))

# (tür, ad): tür = skill | plugin | mcp. Hepsi CC'de doğrulanır.
ALIAS = {
    "21st.dev magic mcp": ("mcp", "21st"),
    "taste-skill": ("plugin", "taste-skill"),
    "image-to-code-skill": ("plugin", "taste-skill"),
    "impeccable": ("plugin", "impeccable"),
    "frontend-design": ("plugin", "frontend-design"),
    "playwright-cli": ("plugin", "playwright"),
    "playwright mcp": ("mcp", "playwright"),
    "figma mcp": ("mcp", "figma"),
    "google stitch (mcp)": ("mcp", "stitch"),
    "21st.dev": ("mcp", "21st"),
}

# Yalnız referans/ilham: CC kurulumu yok.
REF_HOST = (
    "awwwards.com", "godly.design", "dribbble.com", "cosmos.so", "pear.no", "inkwell.tech",
    "cash.app", "igloo.inc", "horizonx.so", "styles.refero.design", "sterlib.dev", "originkit.dev",
    "particles.casberry.in", "animmasterlib.dev", "ui.unlumen.com", "skiper-ui.com", "shadertoy.com",
    "unicorn.studio", "prompt-motion.com", "promptslove.com", "ai-x-leaders.com", "claudecodeclub.ai",
    "promptcat.org", "jiro.build", "thebasemesh.com", "posemy.art", "motionsites.ai",
)
# Hesap/abonelik gerektirebilir (ücretsiz katman doğrulanmadı) → docs/hesap-kuyrugu.md.
HESAP_HOST = ("sketchfab.com", "mobbin.com", "spline.design", "getlayers.ai", "sitereel.ai")
RET_GH = {
    "storytold/photocraft": "bağımsız Rust uygulaması; CC skill/MCP değil",
    "storytold/vectorcraft": "bağımsız Rust uygulaması; CC skill/MCP değil",
    "vercel-labs/agent-skills": "web-design-guidelines: impeccable audit + frontend-craft aynı denetimi kapsıyor (çakışma)",
    "voltagent/awesome-design-md": "awesome liste; awesome-rehber kapsıyor",
    "vercel-labs/json-render": "UI JSON üretici kütüphane; CC için gerekmiyor",
    "emrickgarrett/onevonejev": "oyun/demo projesi, skill değil",
    "penpot/penpot": "bağımsız tasarım uygulaması; CC skill/MCP değil",
    "open-pencil/open-pencil": "bağımsız tasarım uygulaması; CC skill/MCP değil",
    "gridaco/grida": "bağımsız tasarım uygulaması; CC skill/MCP değil",
    "graphiteeditor/graphite": "bağımsız vektör editörü; CC skill/MCP değil",
    "klausschaefers/quant-ux": "bağımsız UX araştırma uygulaması; CC skill/MCP değil",
    "bklit/bklit-ui": "React UI bileşen kütüphanesi; 21st bileşenleri kapsıyor",
    "kokonut-labs/kokonutui": "React UI bileşen kütüphanesi; 21st bileşenleri kapsıyor",
    "nolly-studio/cult-ui": "React UI bileşen kütüphanesi; 21st bileşenleri kapsıyor",
    "ashutoshx7/vengeanceui": "React UI bileşen kütüphanesi; 21st bileşenleri kapsıyor",
    "mengto/threeui": "React UI bileşen kütüphanesi; 21st bileşenleri kapsıyor",
    "ruucm/shadergradient": "shader bileşen kütüphanesi; threejs-3d-paket kapsıyor",
    "oxicid/univ": "Blender eklentisi; CC kurulumu değil, görev dışı",
    "mrven/blender-texel-density-checker": "Blender eklentisi; CC kurulumu değil, görev dışı",
    "bradyajohnston/molecularnodes": "Blender eklentisi; CC kurulumu değil, görev dışı",
    "domlysz/blendergis": "Blender eklentisi; CC kurulumu değil, görev dışı",
    "eatthefuture/camera_shakify": "Blender eklentisi; CC kurulumu değil, görev dışı",
}


def kurulu_mu(tur, ad):
    if tur == "skill":
        return (HOME / ".claude" / "skills" / ad).is_dir()
    if tur == "plugin":
        d = json.loads((HOME / ".claude" / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
        return any(k.split("@")[0] == ad for k in d.get("plugins", d))
    if tur == "mcp":
        d = json.loads((HOME / ".claude.json").read_text(encoding="utf-8"))
        return ad in (d.get("mcpServers") or {})
    return False


def gh_lisans(repo):
    r = subprocess.run(["gh", "repo", "view", repo, "--json", "licenseInfo", "-q", ".licenseInfo.key"],
                       capture_output=True, text=True)
    return (r.stdout.strip() or "none") if r.returncode == 0 else "erisilemedi"


def karar(url, ad):
    u, a = url.lower().rstrip("/"), ad.lower()
    if not u.startswith("http"):
        return "ret", "kaynak adresi yok (tsv'de URL kayıp veya metin)"
    if "instagram.com" in u:
        return "ret", "reel kaynağı; video-tarama'da işlendi, kurulacak paket değil"
    if "extensions.blender.org" in u:
        return "ret", "Blender eklentisi; CC kurulumu değil, görev dışı"
    if a in ALIAS:
        tur, ad_k = ALIAS[a]
        if kurulu_mu(tur, ad_k):
            return "kurulu", f"{tur}:{ad_k} CC'de etkin"
        return "?", f"{tur}:{ad_k} CC'de bulunamadı"
    if "github.com/" in u:
        repo = u.split("github.com/")[1].split("/tree/")[0]
        if repo in RET_GH:
            return "ret", RET_GH[repo]
        if repo == "nandhakishorm/laya":
            ok = subprocess.run([sys.executable, "-m", "pip", "show", "laya"], capture_output=True).returncode == 0
            return ("kurulu", "pip laya (PyPI, Apache-2.0) kurulu") if ok else ("?", "laya pip kurulu değil")
        return "?", f"github {repo}: karar tablosunda yok"
    host = u.split("//")[1].split("/")[0].removeprefix("www.")
    if any(h in host for h in HESAP_HOST):
        return "hesap", "hesap/abonelik gerekebilir; ücretsiz katman doğrulanmadı (docs/hesap-kuyrugu.md)"
    if any(h in host for h in REF_HOST):
        return "ref", "web referansı/ilham kaynağı; CC kurulumu yok"
    return "?", f"host {host}: karar tablosunda yok"


def satirlar():
    import csv
    for dosya in TSVLER:
        with open(KOPRU / dosya, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                yield dosya, r["url"].strip(), r["ad"].strip()


EK = [
    # görev kalemleri (ig-41 dışı): durum + gerekçe elle doğrulandı, kanıt docs/kurulumlar/kurulum-reel-d.md
    ("kurulum-reel-d", "https://github.com/t8y2/dbx", "DBX", "kurulu", "winget t8y2.DBX 0.6.51 kuruldu (Apache-2.0)"),
    ("kurulum-reel-d", "https://github.com/h4ckf0r0day/obscura", "Obscura", "kurulu",
     "obscura-x86_64-windows.zip v0.2.5, sha256 eşleşti; stealth derlemesi KURULMADI (kaçınma özelliği)"),
    ("kurulum-reel-d", "https://github.com/darkroomengineering/lenis", "Lenis", "kurulu",
     "resmi MIT repo; smooth-scroll skill'i Lenis'i kapsıyor; not docs/kurulumlar/lenis.md"),
    ("kurulum-reel-d", "https://github.com/ume0207/lenis", "ume0207 lenis", "ret", "görev kuralı: alınmaz"),
    ("kurulum-reel-d", "https://github.com/ivan-lutskyi/scroll-image-sequence", "scroll-image-sequence", "kurulu",
     "MIT (ivan-lutskyi); skill kaynağı skills/scroll-image-sequence/, CC'ye kopyalandı"),
    ("kurulum-reel-d", "https://github.com/Jpisnice/shadcn-ui-mcp-server", "shadcn-ui-mcp-server", "proje-sablon",
     "MIT (3065★); templates/web-proje/.mcp.json; global kurulmadı"),
]


def main():
    satir = []
    for dosya, url, ad in satirlar():
        d, g = karar(url, ad)
        lis = gh_lisans(url.split("github.com/")[1].split("/tree/")[0]) if "github.com/" in url else "-"
        satir.append((dosya, url, ad, d, g, lis))
    for kaynak, url, ad, d, g in EK:
        satir.append((kaynak, url, ad, d, g, gh_lisans(url.split("github.com/")[1])))
    bilinmeyen = [s for s in satir if s[3] == "?"]
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        f.write("kaynak\turl\tad\tdurum\tgerekce\tlisans\n")
        for s in satir:
            f.write("\t".join(s) + "\n")
    sayim = {}
    for s in satir:
        sayim[s[3]] = sayim.get(s[3], 0) + 1
    print(f"{len(satir)} kalem: " + ", ".join(f"{k}={v}" for k, v in sorted(sayim.items())))
    for s in bilinmeyen:
        print(f"BİLİNMEYEN: {s[2]} | {s[1]} | {s[4]}", file=sys.stderr)
    return 1 if bilinmeyen else 0


if __name__ == "__main__":
    sys.exit(main())
