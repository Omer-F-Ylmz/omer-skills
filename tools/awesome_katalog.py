"""AWESOME-1: sindresorhus/awesome (CC0) → docs/kaynak/awesome/katalog.tsv + bizim alanların alt liste önbelleği (<liste>.tsv).
  python tools/awesome_katalog.py            → eksik dosyaları üretir (var olana dokunmaz; önbellek)
  python tools/awesome_katalog.py --yenile   → README'leri ve yıldız/son push'u yeniden çeker
Ağ: yalnız `gh api` (README: REST raw; yıldız: GraphQL, 100 repo/çağrı → ~8 çağrı). Alt listelerin lisansı çoğunlukla CC0
değil → yalnız ad + url + ≤15 kelime açıklama alınır, metin kopyalanmaz."""
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
DIZIN = KOK / "docs/kaynak/awesome"
ATLA_ANA = {"Contents", "Related"}
ATLA_ALT = re.compile(r"contents|licen[cs]e|contribut|related|credits|footnote|sponsor|support", re.I)
OGE = re.compile(r"^(\s*)[-*+]\s+(?::\w+:\s*)*(?:\*\*)?\[([^\]]+)\]\(([^)\s]+)\)(?:\*\*)?(.*)$")
# Bizim alanlar → katalogdaki gerçek liste repoları (katalog.tsv'den seçildi)
ALANLAR = {
    "dotnet": ["quozd/awesome-dotnet", "thangchung/awesome-dotnet-core"],
    "python": ["vinta/awesome-python"],
    "js-ts": ["sorrycc/awesome-javascript", "sindresorhus/awesome-nodejs"],
    "react-next": ["enaqx/awesome-react", "unicodeveloper/awesome-nextjs"],
    "css-perf-a11y": ["awesome-css-group/awesome-css", "davidsonfellipe/awesome-wpo"],  # awesome-a11y topics/*.md'ye bölünmüş → önbelleksiz
    "webgl-3d": ["sjfricke/awesome-webgl", "terkelg/awesome-creative-coding"],  # katalogda Blender/Three.js listesi yok
    "tasarim-ui": ["klaufel/awesome-design-systems", "sergey-pimenov/awesome-web-animation"],
    "oyun": ["ellisonleao/magictools", "godotengine/awesome-godot", "awesome-roblox/awesome-roblox"],  # Unity listesi yok
    "guvenlik": ["qazbnm456/awesome-web-security", "carpedm20/awesome-hacking"],  # awesome-appsec öğeleri başlık biçiminde → önbelleksiz
    "test": ["TheJambo/awesome-testing", "mxschmitt/awesome-playwright"],
    "veritabani": ["dhamaniasad/awesome-postgres", "mgramin/awesome-db-tools"],
    "devops": ["veggiemonk/awesome-docker", "sdras/awesome-actions"],
    "video": ["transitive-bullshit/awesome-ffmpeg"],
    "otomasyon": ["awesome-selfhosted/awesome-selfhosted"],
    "llm-ajan": ["hesreallyhim/awesome-claude-code", "steven2358/awesome-generative-ai", "sindresorhus/awesome-chatgpt"],
    "cli-windows": ["agarrharr/awesome-cli-apps", "0pandadev/awesome-windows", "alebcay/awesome-shell"],
    "gizlilik": ["bakke92/awesome-gdpr"],
}


def _repo(url):
    m = re.match(r"https://github\.com/([^/#?]+/[^/#?]+)", url)
    return m.group(1) if m else url.removesuffix("#readme")


def _acik(kalan):
    kalan = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", kalan)  # iç bağlantı → yalnız metni
    return re.sub(r"^\s*(?:[-–—:]\s*)+", "", kalan).replace("\t", " ").strip()


def ayristir(md):
    """Ana README → (bolum, alt_bolum, liste_adi, repo, aciklama)."""
    satirlar, bolum, ebeveyn = [], None, ""
    for s in md.splitlines():
        if s.startswith("## "):
            bolum, ebeveyn = s[3:].strip(), ""
            continue
        if bolum is None or bolum in ATLA_ANA or not s.lstrip().startswith("- "):
            continue
        ic = s[0] in " \t"
        m = OGE.match(s)
        if not m:
            if not ic:  # bağlantısız grup başlığı: "- Linux" / "- macOS - açıklama"
                ebeveyn = s[2:].split(" - ")[0].strip()
            continue
        _, ad, url, kalan = m.groups()
        satirlar.append((bolum, ebeveyn if ic else "", ad, _repo(url), _acik(kalan)))
        if not ic:
            ebeveyn = ad
    return satirlar


def _kisalt(metin, n=15):
    k = metin.split()
    return metin if len(k) <= n else " ".join(k[:n]) + "…"


def alt_ayristir(md):
    """Alt liste README → (ad, url, ≤15 kelime açıklama, 'H2 / H3')."""
    satirlar, yigin, baslik_var = [], [], False  # yigin: (düzey, başlık); belge başlığı (ilk H1) sayılmaz
    for s in md.splitlines():
        b = re.match(r"^(#{1,6})\s+(.+)$", s)
        if b:
            d = len(b.group(1))
            yigin = [h for h in yigin if h[0] < d]
            if baslik_var or d > 1:
                yigin.append((d, b.group(2).strip()))
            baslik_var = True
            continue
        m = OGE.match(s)
        if not m or not yigin or ATLA_ALT.search(yigin[-1][1]) or m.group(3).startswith("#"):
            continue
        _, ad, url, kalan = m.groups()
        satirlar.append((ad.strip(), url, _kisalt(_acik(kalan)), " / ".join(h for _, h in yigin[-2:])))
    return satirlar


def _gh(*arg):
    return subprocess.run(["gh", "api", *arg], capture_output=True, text=True, encoding="utf-8").stdout


def readme(repo):
    return _gh(f"repos/{repo}/readme", "-H", "Accept: application/vnd.github.raw")


def meta(repolar):
    """repo → (yıldız, son push günü); GraphQL toplu, bulunamayan repo boş kalır."""
    sonuc = {}
    gh = [r for r in repolar if "/" in r and not r.startswith("http")]
    for i in range(0, len(gh), 100):
        parca = gh[i:i + 100]
        govde = " ".join(f'r{j}: repository(owner: "{r.split("/")[0]}", name: "{r.split("/")[1]}") {{ stargazerCount pushedAt }}'
                         for j, r in enumerate(parca))
        veri = (json.loads(_gh("graphql", "-f", f"query={{ {govde} }}") or "{}").get("data") or {})
        for j, r in enumerate(parca):
            d = veri.get(f"r{j}")
            if d:
                sonuc[r] = (str(d["stargazerCount"]), (d["pushedAt"] or "")[:10])
    return sonuc


def _yaz(yol, baslik, satirlar):
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_bytes(("\n".join(["\t".join(baslik)] + ["\t".join(r) for r in satirlar]) + "\n").encode("utf-8"))


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    yenile = "--yenile" in argv
    kat = DIZIN / "katalog.tsv"
    if yenile or not kat.exists():
        satirlar = ayristir(readme("sindresorhus/awesome"))
        m = meta([r[3] for r in satirlar])
        _yaz(kat, ("bolum", "alt_bolum", "liste_adi", "repo", "aciklama", "yildiz", "son_push"),
             [r + m.get(r[3], ("", "")) for r in satirlar])
    satirlar = [s.split("\t") for s in kat.read_text(encoding="utf-8").splitlines()[1:]]
    print(f"katalog: {len({s[0] for s in satirlar})} bölüm · {len(satirlar)} liste")
    for alan, repolar in ALANLAR.items():
        for repo in repolar:
            yol = DIZIN / f"{repo.split('/')[1].lower()}.tsv"
            if yenile or not yol.exists():
                _yaz(yol, ("ad", "url", "aciklama", "bolum"), alt_ayristir(readme(repo)))
            print(f"{alan}: {yol.name} {len(yol.read_text(encoding='utf-8').splitlines()) - 1} öğe")


if __name__ == "__main__":
    main(sys.argv[1:])
