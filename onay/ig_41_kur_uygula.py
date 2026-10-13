"""IG-41-KUR onay betiği — Desktop/Ömer koşar. ig_40_kur_uygula iskeleti; farklar: skill'ler kopyalanmadan önce
SkillSpector --no-llm kapısı (UYARLA #147), sürüm güncellemeleri (uv/plugin/gstack) ve sha256 sabitli taşınabilir zip'ler.

  python onay/ig_41_kur_uygula.py --kuru   # plan: ne kurulu, ne kurulacak/güncellenecek (varsayılan)
  python onay/ig_41_kur_uygula.py uygula   # eksikleri kurar, eskileri günceller (idempotent); yedek ~/.claude/ig41-kur-yedek
  python onay/ig_41_kur_uygula.py --geri   # yalnız BU betiğin eklediklerini kaldırır, güncellenenleri eski sürüme döndürür
Tarama (gitleaks · semgrep p/security-audit · SkillSpector --no-llm): wt igkur41 `.claude/igkur41/tarama*.tsv`.
INCELENDI: SkillSpector HIGH bulguları elle bakılıp yanlış pozitif bulunan kimlikler; yeni bir HIGH kimliği çıkarsa skill kurulmaz.
Önceden kurulu hiçbir şey kaldırılmaz/kapatılmaz; MCP listesi önce=sonra değilse rc=1.
"""
import hashlib, json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

EV = Path.home()
PLUGIN = [("Jakeschincariol/youtube-agent-skill", "youtube-agent@youtube-agent-skill"),
          ("anthropics/claude-for-legal", "commercial-legal@claude-for-legal"),
          ("anthropics/claude-for-legal", "privacy-legal@claude-for-legal")]
NPM = ["skills"]  # vercel-labs/skills: `npx skills find` kayıt defteri araması
SKILL = [("wheresryan22/anatomy", ".", "anatomy"), ("lucasmarkes/hairline", "skills/hairline-create", "hairline-create"),
         ("img2threejs/img2threejs", ".", "img2threejs")]
INCELENDI = {"anatomy": {"AE1", "AS1", "PE3", "SC3", "P6"},
             # d3: AE1 = SKILL.md kendi forge/*.py hattını çağırır; E2/AS1/PE3 testler, .gitignore, docs; AR2 ekran görüntüsü alanı; P2 PR şablonu yorumu
             "img2threejs": {"AE1", "AR2", "AS1", "E2", "P2", "PE3"},
             "hairline-create": {"OH1", "PE3"}}  # d3: ikisi de skills/ dışında (publish.yml .npmrc, site kopyala düğmesi)
# (ad, repo, etiket, varlık, sha256) — Ev/Apps/<ad> altına açılır
ZIP = [("dbx", "t8y2/dbx", "v0.6.42", "DBX_0.6.42_x64-portable.zip",
        "4e0a917f3612843750d2595dc9eebb5dc7e3dd42ee9152029c674b586d55fc73"),
       ("obscura", "h4ckf0r0day/obscura", "v0.2.4", "obscura-x86_64-windows.zip",
        "8e5428bf8c101f1439c53a9dcb52d7d09bb22599206b49f6420028d93d01189b")]
UV_GUNCEL = {"graphifyy": "graphifyy[sql]==0.9.57", "headroom-ai": "headroom-ai[all]==0.37.0"}  # ad → geri dönüş belirteci
PLUGIN_GUNCEL = {"ponytail@ponytail": "e3ba2aa6", "humanizer@humanizer": "9862685f",
                 "marketing-skills@marketingskills": "1efedbc5"}  # ad → 13 Eki kurulu commit
GSTACK = EV / ".claude" / "skills" / "gstack"


def bildirim(ev):
    return ev / ".claude" / "ig41-kur-eklenen.json"


def yedek(ev):
    return ev / ".claude" / "ig41-kur-yedek"


def kos(*a, cwd=None):
    a = (shutil.which(a[0]) or a[0], *a[1:])  # npm Windows'ta npm.cmd
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd,
                          creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def mcp_var_mi(ev=EV):
    """~/.claude.json'daki MCP sunucu adları (değer yazdırılmaz, yalnız adlar)."""
    try:
        j = json.loads((ev / ".claude.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    adlar = set(j.get("mcpServers") or {})
    for p in (j.get("projects") or {}).values():
        adlar |= set((p or {}).get("mcpServers") or {})
    return adlar


def plugin_json(ev=EV):
    try:
        return json.loads((ev / ".claude" / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))["plugins"]
    except (OSError, ValueError, KeyError):
        return {}


def kurulu_uv():
    return {s.split()[0]: s.split()[1] for s in kos("uv", "tool", "list").stdout.splitlines() if s and not s.startswith("-")}


def kurulu_npm():
    try:
        return set(json.loads(kos("npm", "ls", "-g", "--depth=0", "--json").stdout).get("dependencies") or {})
    except ValueError:
        return set()


def ss_gecer(ad, dizin):
    """SkillSpector --no-llm kapısı: HIGH/CRITICAL kimlikleri INCELENDI'nin alt kümesiyse geçer."""
    with tempfile.TemporaryDirectory() as t:
        cik = Path(t) / "ss.json"
        kos("skillspector", "scan", str(dizin), "--no-llm", "--format", "json", "--output", str(cik))
        try:
            j = json.loads(cik.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False, "skillspector çıktısı yok"
    yuksek = {i.get("id") for i in j.get("issues") or [] if i.get("severity") in ("HIGH", "CRITICAL")}
    yeni = yuksek - INCELENDI.get(ad, set())
    return (not yeni, "temiz" if not yeni else "incelenmemiş HIGH: " + ",".join(sorted(map(str, yeni))))


def sha_tamam(dosya, beklenen):
    return hashlib.sha256(Path(dosya).read_bytes()).hexdigest() == beklenen


def plan(ev=EV):
    """[(tür, ad, kurulu_mu)] — kurulum yapmaz. Güncellemelerde kurulu_mu = güncel mi."""
    p, u, n = plugin_json(ev), kurulu_uv(), kurulu_npm()
    return ([("plugin", ad, ad in p) for _, ad in PLUGIN] + [("npm", ad, ad in n) for ad in NPM]
            + [("skill", ad, (ev / ".claude" / "skills" / ad).exists()) for _, _, ad in SKILL]
            + [("zip", ad, (ev / "Apps" / ad).exists()) for ad, *_ in ZIP]
            + [("uv-guncel", ad, u.get(ad, "").lstrip("v") != b.split("==")[1]) for ad, b in UV_GUNCEL.items()]
            + [("plugin-guncel", ad, not p.get(ad, [{}])[0].get("gitCommitSha", "").startswith(c))
               for ad, c in PLUGIN_GUNCEL.items()]
            + [("gstack-guncel", str(GSTACK), not (GSTACK / ".git").exists())])


def uygula(ev=EV):
    once, eklenen = mcp_var_mi(ev), []
    var = {(t, ad) for t, ad, k in plan(ev) if k}
    y = yedek(ev)
    y.mkdir(parents=True, exist_ok=True)
    for repo, ad in PLUGIN:
        if ("plugin", ad) in var:
            continue
        kos("claude", "plugin", "marketplace", "add", repo)
        if kos("claude", "plugin", "install", ad).returncode == 0:
            eklenen.append(["plugin", ad])
    for ad in NPM:
        if ("npm", ad) not in var and kos("npm", "install", "-g", ad).returncode == 0:
            eklenen.append(["npm", ad])
    for repo, alt, ad in SKILL:
        if ("skill", ad) in var:
            continue
        with tempfile.TemporaryDirectory() as t:
            if kos("git", "clone", "--depth", "1", "-c", "core.hooksPath=NUL", f"https://github.com/{repo}", t + "/r").returncode:
                print("klon başarısız", ad)
                continue
            gecer, neden = ss_gecer(ad, Path(t) / "r" / alt)
            if not gecer:
                print("KURULMADI", ad, neden)
                continue
            shutil.copytree(Path(t) / "r" / alt, ev / ".claude" / "skills" / ad, ignore=shutil.ignore_patterns(".git"))
            eklenen.append(["skill", ad])
    for ad, repo, etiket, varlik, sha in ZIP:
        if ("zip", ad) in var:
            continue
        with tempfile.TemporaryDirectory() as t:
            kos("gh", "release", "download", etiket, "-R", repo, "-p", varlik, "-D", t)
            if not (Path(t) / varlik).exists() or not sha_tamam(Path(t) / varlik, sha):
                print("KURULMADI", ad, "indirme yok ya da sha256 tutmadı")
                continue
            zipfile.ZipFile(Path(t) / varlik).extractall(ev / "Apps" / ad)
            eklenen.append(["zip", str(ev / "Apps" / ad)])
    for ad, geri_belirtec in UV_GUNCEL.items():
        if ("uv-guncel", ad) not in var and kos("uv", "tool", "upgrade", ad).returncode == 0:
            eklenen.append(["uv-guncel", geri_belirtec])
    pj = ev / ".claude" / "plugins"
    for f in ("installed_plugins.json", "known_marketplaces.json"):
        if (pj / f).exists() and not (y / f).exists():
            shutil.copy2(pj / f, y / f)
    eski_plugin = plugin_json(ev)
    for ad in PLUGIN_GUNCEL:
        if ("plugin-guncel", ad) in var or ad not in eski_plugin:
            continue
        yol = Path(eski_plugin[ad][0]["installPath"])
        if yol.exists() and not (y / "cache" / yol.name / ad).exists():
            shutil.copytree(yol, y / "cache" / yol.name / ad)
        kos("claude", "plugin", "marketplace", "update", ad.split("@")[1])
        if kos("claude", "plugin", "update", ad).returncode == 0:
            eklenen.append(["plugin-guncel", ad, str(yol)])
    if ("gstack-guncel", str(GSTACK)) not in var:
        onceki = kos("git", "-C", str(GSTACK), "rev-parse", "HEAD").stdout.strip()
        if kos("git", "-C", str(GSTACK), "pull", "--ff-only", "origin", "main").returncode == 0:
            kos("bash", "./setup", cwd=str(GSTACK))
            eklenen.append(["gstack-guncel", onceki])
    eski = json.loads(bildirim(ev).read_text(encoding="utf-8")) if bildirim(ev).exists() else []
    bildirim(ev).write_text(json.dumps(eski + eklenen, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in eklenen:
        print("eklendi", *e[:2])
    return once == mcp_var_mi(ev)


def geri(ev=EV):
    once = mcp_var_mi(ev)
    if not bildirim(ev).exists():
        print("bildirim yok: geri alınacak bir şey yok")
        return True
    y, liste = yedek(ev), json.loads(bildirim(ev).read_text(encoding="utf-8"))
    for t, ad, *ek in reversed(liste):
        if t == "plugin":
            kos("claude", "plugin", "uninstall", ad)
        elif t == "npm":
            kos("npm", "uninstall", "-g", ad)
        elif t == "skill":
            shutil.rmtree(ev / ".claude" / "skills" / ad, ignore_errors=True)
        elif t == "zip":
            shutil.rmtree(ad, ignore_errors=True)
        elif t == "uv-guncel":
            kos("uv", "tool", "install", "--force", ad)
        elif t == "plugin-guncel":
            yol = Path(ek[0])
            if not yol.exists() and (y / "cache" / yol.name / ad).exists():
                shutil.copytree(y / "cache" / yol.name / ad, yol)
        elif t == "gstack-guncel":
            kos("git", "-C", str(GSTACK), "reset", "--hard", ad)
            kos("bash", "./setup", cwd=str(GSTACK))
        print("geri", t, ad)
    for f in ("installed_plugins.json", "known_marketplaces.json"):
        if any(e[0] == "plugin-guncel" for e in liste) and (y / f).exists():
            shutil.copy2(y / f, ev / ".claude" / "plugins" / f)
    bildirim(ev).unlink()
    return once == mcp_var_mi(ev)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    if kip == "uygula":
        ok = uygula()
    elif kip == "--geri":
        ok = geri()
    else:
        for t, ad, k in plan():
            print(f"{t}\t{ad}\t{'kurulu/güncel (atlanır)' if k else 'yapılacak'}")
        ok = True
    print("mcp önce=sonra" if ok else "HATA: MCP listesi değişti")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
