import csv, collections, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
KOK = r"C:\Projeler\omer-skills\docs\video-tarama"
rows = list(csv.DictReader(open(KOK + r"\ana-liste.tsv", encoding="utf-8"), delimiter="\t"))
HEDEF = ("KURULMADI-SIRADA", "KURULU-KANITSIZ")
CLAUDE = ("claude.ai", "claude.com", "anthropic.com", "docs.anthropic.com", "anthropics")
PAKET = re.compile(r"^(npx|npm|pnpm|bunx|pip|pipx|uv|uvx|brew|winget|choco|cargo|go install|docker|claude (plugin|mcp))\b", re.I)
YOL = re.compile(r"(^\.{0,2}/[\w.-]+/|\.(json|sh|md|py|ts|js|yaml|yml|toml|txt|ps1)$|^\.[a-z])", re.I)
CC_YERLESIK = {"/clear","/compact","/config","/context","/cost","/help","/init","/btw","/add-dir","/agents","/branch","/model","/memory","/resume","/review","/plugin","/mcp","/hooks","/permissions","/status","/doctor","/login","/logout","/export","/rewind","/usage","/statusline","/terminal-setup","/vim","/goal","/advisor","/design-sync","/output-style","/security-review","/todos","/ide","/bashes","/upgrade"}

def host(u):
    return re.sub(r"^https?://(www\.)?", "", u.strip()).split("/")[0].lower()

def gh_norm(u):
    m = re.search(r"github\.com/([\w.-]+)/([\w.-]+)", u, re.I)
    return (m.group(1) + "/" + re.sub(r"\.git$", "", m.group(2))).lower() if m else ""

def sinif(r):
    k, u = r["kalem"].strip(), r["repo_link"].strip()
    if u:
        if "github.com" in u.lower() and gh_norm(u):
            return "GH"
        h = host(u)
        if any(c in h for c in CLAUDE) or h in ("skills",):
            return "CLAUDE-RESMI"
        if h in ("bit.ly", "t.co", "lnkd.in", "inkd.in"):
            return "KISA-LINK"
        return "URL-URUN"
    kl = k.lower().split()[0] if k else ""
    if k.startswith("/"):
        return "CC-YERLESIK" if kl in CC_YERLESIK or kl.replace(" komutu", "") in CC_YERLESIK else "SLASH"
    if PAKET.match(k):
        return "PAKET-KOMUT"
    if YOL.search(k):
        return "GURULTU-YOL"
    return "AD"

out = []
say = collections.Counter()
for r in rows:
    if r["durum"] not in HEDEF:
        continue
    s = sinif(r)
    say[(r["durum"], s)] += 1
    out.append({"kalem": r["kalem"], "durum": r["durum"], "tur": r["tur"], "sinif": s,
                "gh": gh_norm(r["repo_link"]), "repo_link": r["repo_link"],
                "video_sayi": len([x for x in r["kaynak_video_idleri"].split(",") if x])})
with open(KOK + r"\kurulum-sinif.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter="\t")
    w.writeheader(); w.writerows(out)
for (d, s), n in sorted(say.items()):
    print(d, s, n)
gh = {o["gh"] for o in out if o["gh"]}
print("tekil gh", len(gh))
for s in ("AD", "SLASH", "URL-URUN", "PAKET-KOMUT"):
    ornek = sorted([o for o in out if o["sinif"] == s], key=lambda o: -o["video_sayi"])[:20]
    print("\n#", s, [o["kalem"] + ":" + str(o["video_sayi"]) for o in ornek])
