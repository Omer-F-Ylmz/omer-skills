"""KURULUM-GH-1 (Ömer onayı 1 Kas 21:46): ana-liste GitHub klonlarını CC'ye kurar, token düzenimize bağlayarak.
- marketplace.json olan repo → claude plugin marketplace add + plugin install. Kanca (hooks) ya da MCP taşıyan plugin
  kurulur ama DEVRE DIŞI (Ömer listeden seçer; açılınca MCP'si paylaşımlı vekile/ToolSearch'e bağlanır).
- Plugin'siz repo → SKILL.md klasörleri ~/.claude/skills altına (çakışırsa sahip-ad).
- Token düzeni: eklenen HER skill (plugin skill'i dahil) settings.json skillOverrides'a "name-only" yazılır (mevcut değer
  korunur); ajan dosyaları ~/.claude/agents-katalog'a (lazy, ajan-getir) — global agents'e değil.
- settings.json önce yedeklenir (settings.json.yedek-kurulum-gh-<zaman>); hiçbir şey silinmez.
Kullanım: python tools/kurulum_gh_uygula.py [--kuru] [--sinir N]"""
import csv, hashlib, json, re, shutil, subprocess, sys, io, time
from pathlib import Path
KOK = Path(__file__).resolve().parents[1] / "docs/video-tarama"
EV = Path.home() / ".claude"
SK = EV / "skills"
AK = EV / "agents-katalog"
AYAR = EV / "settings.json"
CLAUDE = str(Path.home() / ".local/bin/claude.exe")
NW = 0x08000000
ATLA = re.compile(r"[\\/](node_modules|\.git|tests?|__tests__|fixtures|examples?|templates?|vendor|dist|build)[\\/]", re.I)
KURU = "--kuru" in sys.argv
SINIR = int(sys.argv[sys.argv.index("--sinir") + 1]) if "--sinir" in sys.argv else 10**9
CIK, YENI_SKILL = [], {}


def kos(a, t=300):
    if KURU:
        return 0, "KURU"
    try:
        r = subprocess.run([CLAUDE] + a, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=t, creationflags=NW)
        return r.returncode, (r.stdout + r.stderr).strip()[-300:].replace("\n", " ").replace("\t", " ")
    except Exception as e:
        return -1, str(e)[:200]


def hash_dir(p):
    import os
    h = hashlib.sha1()
    for k, ds, fs in sorted(os.walk(p, onerror=lambda e: None)):
        ds[:] = sorted(d for d in ds if d not in (".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"))
        for ad in sorted(fs):
            f = Path(k) / ad
            try:
                if f.stat().st_size < 1_000_000:
                    h.update(ad.encode()); h.update(f.read_bytes())
            except OSError:
                pass
    return h.hexdigest()


def fm_ad(md):
    t = md.read_text(encoding="utf-8", errors="ignore")[:800]
    m = re.search(r"^name:\s*['\"]?([^'\"\n]+)", t, re.M)
    return m.group(1).strip() if t.startswith("---") and m else None


def plugin_dizin(repo, kaynak):
    if isinstance(kaynak, dict) or not isinstance(kaynak, str) or kaynak.startswith(("http", "git")):
        return None
    d = (repo / kaynak).resolve()
    return d if d.exists() else None


def risk(d):
    if not d:
        return "uzak-kaynak"
    n = set()
    if (d / "hooks").exists() or any(d.glob("**/hooks.json")):
        n.add("hooks")
    pj = d / ".claude-plugin/plugin.json"
    t = pj.read_text(encoding="utf-8", errors="ignore") if pj.exists() else ""
    if '"hooks"' in t:
        n.add("hooks")
    if '"mcpServers"' in t or (d / ".mcp.json").exists():
        n.add("mcp")
    return ",".join(sorted(n))


def kayitli_market():
    f = EV / "plugins/known_marketplaces.json"
    try:
        return set(json.loads(f.read_text(encoding="utf-8")).keys())
    except Exception:
        return set()


KAYITLI = kayitli_market()
BUYUK = 10


def plugin_kur(repo, gh):
    mj = json.loads((repo / ".claude-plugin/marketplace.json").read_text(encoding="utf-8", errors="ignore"))
    mp = mj.get("name") or repo.name
    pl = mj.get("plugins", [])
    if mp in KAYITLI:
        CIK.append([gh, "MARKETPLACE", mp, "ZATEN-KAYITLI", f"{len(pl)} plugin; kaynak degistirilmedi"])
        return
    k, o = kos(["plugin", "marketplace", "add", str(repo)])
    CIK.append([gh, "MARKETPLACE", mp, "TAMAM" if k == 0 or "already" in o.lower() else "HATA", o[:150]])
    if len(pl) > BUYUK:
        CIK.append([gh, "MARKETPLACE", mp, "MARKET-YALNIZ", f"{len(pl)} plugin; tek tek kurulmadi, /plugin ile secilir"])
        return
    for p in pl:
        ad = p.get("name")
        if not ad:
            continue
        d = plugin_dizin(repo, p.get("source", ""))
        r = risk(d)
        k, o = kos(["plugin", "install", f"{ad}@{mp}"])
        durum = "TAMAM" if k == 0 or "already" in o.lower() else "HATA"
        if durum == "TAMAM" and r:
            k2, _ = kos(["plugin", "disable", f"{ad}@{mp}"])
            durum = "KURULDU-KAPALI" if k2 == 0 else "KURULDU-KAPATILAMADI"
        if durum != "HATA" and d:
            for s in d.rglob("SKILL.md"):
                n = fm_ad(s)
                if n:
                    YENI_SKILL[f"{ad}:{n}"] = "name-only"
        CIK.append([gh, "PLUGIN", f"{ad}@{mp}", durum, (r + " " + o)[:150]])


def guvenli_glob(kok, ad):
    import os
    for k, ds, fs in os.walk(kok, onerror=lambda e: None):
        ds[:] = [d for d in ds if d not in (".git", "node_modules")]
        if ad in fs:
            yield Path(k) / ad


def skill_kur(repo, gh):
    sahip = gh.split("/")[0].lower()
    for f in guvenli_glob(repo, "SKILL.md"):
        if ATLA.search(str(f.relative_to(repo.parent))):
            continue
        try:
            src, n = f.parent, fm_ad(f)
        except OSError as e:
            CIK.append([gh, "SKILL", f.parent.name, "ATLANDI-OKUNAMADI", str(e)[:100]]); continue
        if not n:
            CIK.append([gh, "SKILL", src.name, "ATLANDI-FRONTMATTER", str(src)[-120:]]); continue
        ad = re.sub(r"[^\w.-]+", "-", n).strip("-").lower()[:60]
        hedef = SK / ad
        if hedef.exists():
            try:
                ayni_md = (hedef / "SKILL.md").read_bytes() == f.read_bytes()
            except OSError:
                ayni_md = False
            if ayni_md:
                CIK.append([gh, "SKILL", ad, "ZATEN-KURULU", ""]); continue
            hedef = SK / f"{sahip}-{ad}"[:70]
            if hedef.exists():
                CIK.append([gh, "SKILL", hedef.name, "ZATEN-KURULU", ""]); continue
        if not KURU:
            try:
                shutil.copytree(src, hedef, ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"), ignore_dangling_symlinks=True)
            except shutil.Error:
                pass
            except OSError as e:
                CIK.append([gh, "SKILL", hedef.name, "HATA-KOPYA", str(e)[:100]]); continue
        YENI_SKILL[hedef.name] = "name-only"
        CIK.append([gh, "SKILL", hedef.name, "KURULDU", str(src)[-120:]])


def ajan_kur(repo, gh):
    sahip = gh.split("/")[0].lower()
    for f in repo.rglob("agents/*.md"):
        if ATLA.search(str(f.relative_to(repo.parent))) or not re.match(r"---\r?\n.*?\bname:", f.read_text(encoding="utf-8", errors="ignore")[:600], re.S):
            continue
        h = AK / f"{sahip}-{f.stem}.md"
        if h.exists():
            continue
        if not KURU:
            AK.mkdir(exist_ok=True); shutil.copy2(f, h)
        CIK.append([gh, "AJAN", h.stem, "KATALOGA", ""])


def ayar_yaz():
    if not YENI_SKILL:
        return 0
    j = json.loads(AYAR.read_text(encoding="utf-8"))
    so = j.setdefault("skillOverrides", {})
    n = 0
    for k, v in YENI_SKILL.items():
        if k not in so:
            so[k] = v; n += 1
    if n and not KURU:
        shutil.copy2(AYAR, AYAR.with_name(f"settings.json.yedek-kurulum-gh-{time.strftime('%m%d%H%M')}"))
        AYAR.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    return n


def main():
    R = [r for r in csv.DictReader(open(KOK / "gh-klon.tsv", encoding="utf-8"), delimiter="\t") if r["yol"] and not r["durum"].startswith(("HATA", "GUVENLIK", "DISK"))]
    tara = {r["gercek"]: r for r in csv.DictReader(open(KOK / "gh-tara.tsv", encoding="utf-8"), delimiter="\t")}
    if "--sadece" in sys.argv:
        s = set(sys.argv[sys.argv.index("--sadece") + 1].lower().split(","))
        R = [r for r in R if r["gh"].lower() in s]
    for r in R[:SINIR]:
        repo = Path(r["yol"])
        try:
            if (repo / ".claude-plugin/marketplace.json").exists():
                plugin_kur(repo, r["gh"])
            else:
                if int(tara.get(r["gh"], {}).get("skill") or 0):
                    skill_kur(repo, r["gh"])
                if int(tara.get(r["gh"], {}).get("agent") or 0):
                    ajan_kur(repo, r["gh"])
                if not int(tara.get(r["gh"], {}).get("skill") or 0) and not int(tara.get(r["gh"], {}).get("agent") or 0):
                    CIK.append([r["gh"], "KAYNAK", repo.name, "KLON-KAYNAK", "skill/plugin yok; kod/CLI kurulumu ayrı tur"])
        except Exception as e:
            CIK.append([r["gh"], "?", repo.name, "HATA", str(e)[:150]])
    n = ayar_yaz()
    ad = "kurulum-gh-sonuc" + ("-kuru" if KURU else "") + ("-ek" if "--sadece" in sys.argv else "") + ".tsv"
    with open(KOK / ad, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["gh", "tur", "ad", "durum", "not"]); w.writerows(CIK)
    from collections import Counter
    print("BITTI", "name-only eklenen", n, Counter((c[1], c[3]) for c in CIK).most_common())


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
