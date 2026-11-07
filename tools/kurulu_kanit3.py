"""KANIT-KATEGORI-1 is 2: rapor/kurulum-omer-sonuc.tsv KURULDU satirlari (bugun kurulan) icin calistirma kaniti.
Cikti docs/video-tarama/kurulu-kanit-yeni.tsv (kalem,yontem,paket,sonuc,tur,ayrinti). SKILL: SKILL.md frontmatter; NPM/UV: bin --version|--help. husky benzeri argumana duyarli bin cagrilmaz."""
import csv, re, shutil, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kurulu_kanit2 as K2
R = K2.R; H = K2.H
def oku_bom(p): return list(csv.DictReader(open(p, encoding="utf-8-sig"), delimiter="\t"))
def skill_yol(ad):
    for base in (H / ".claude/skills", H / ".claude/plugins"):
        d = base / ad
        if (d / "SKILL.md").exists(): return d
    import glob
    g = sorted(glob.glob(str(H / f".claude/plugins/**/skills/{ad}/SKILL.md"), recursive=True))
    return Path(g[0]).parent if g else None
def bins_of(pkgdir):
    try: b = json.loads((pkgdir / "package.json").read_text(encoding="utf-8")).get("bin", {})
    except Exception: return []
    return list(b) if isinstance(b, dict) else [json.loads((pkgdir / "package.json").read_text(encoding="utf-8"))["name"].split("/")[-1]]
YASAK = {"husky"}
def npm_kanit(pkg):
    name = re.sub(r"@(\d+)$", "", pkg) if not pkg.startswith("@") or pkg.count("@") > 1 else pkg
    g = K2.run([K2.NPMX, "root", "-g"], 20)[1].splitlines()[-1]
    for root in [Path(g)] + [d / "node_modules" for d in K2.NPMS]:
        pd = root / name
        if (pd / "package.json").exists():
            ver = json.loads((pd / "package.json").read_text(encoding="utf-8")).get("version", "?")
            for b in bins_of(pd):
                if b in YASAK: continue
                exe = shutil.which(b)
                if not exe and (root / ".bin" / (b + ".cmd")).exists(): exe = str(root / ".bin" / (b + ".cmd"))
                if not exe: continue
                for a in ("--version", "--help"):
                    c, o = K2.run([exe, a], 30)
                    if c == 0 and o: return "KANIT", "cli", f"{b} {a} exit0 (pkg {ver}): {o.splitlines()[0][:50]}"
            c, o = K2.run(["node", "-e", f"require('{pd.as_posix()}/package.json')"], 20)
            if c == 0: return "KANIT", "npm-pkg", f"{name}@{ver} paket kurulu (cli --version/--help calismadi: bin yok/hata)"
    return "KANITSIZ", "npm", "paket global/npm dizinlerinde bulunamadi"
def uv_kanit(pkg):
    c, o = K2.run([shutil.which("uv") or "uv", "tool", "list", "--show-paths"], 30)
    blok = None
    for ln in o.splitlines():
        if not ln.startswith("-") and ln.split(" ")[0].lower() == pkg.lower(): blok = ln.split(" ")[0]; continue
        if blok and ln.startswith("- "):
            exe = Path.home() / ".local/bin" / (ln[2:].strip().split(" ")[0] + ".exe")
            if exe.exists():
                for a in ("--version", "--help"):
                    cc, oo = K2.run([str(exe), a], 30)
                    if cc == 0 and oo: return "KANIT", "cli", f"{exe.stem} {a} exit0: {oo.splitlines()[0][:60]}"
        elif blok and not ln.startswith("-"): blok = None
    t = H / "AppData/Roaming/uv/tools" / pkg
    py = t / "Scripts/python.exe"
    if py.exists():
        im = pkg.replace("-", "_")
        cc, oo = K2.run([str(py), "-c", f"import {im}"], 60)
        if cc == 0: return "KANIT", "import", f"uv tool venv: import {im} ok"
    return "KANITSIZ", "uv", "uv tool ciktisinda calisan bin/import yok"
if __name__ == "__main__":
    rows = [r for r in oku_bom(R / "rapor/kurulum-omer-sonuc.tsv") if r["durum"] == "KURULDU"]
    out = []
    for r in rows:
        y, k, n = r["yontem"], r["kalem"], r["not"]
        if y == "SKILL":
            for ad in [x.strip() for x in n.split(",") if x.strip()]:
                p = skill_yol(ad); sk = K2.skill_any(str(p)) if p else None
                out.append([k + " :: " + ad, y, ad, "KANIT" if sk else "KANITSIZ", "skill", sk or "SKILL.md bulunamadi/frontmatter yok"])
        elif y == "NPM": out.append([k, y, n] + list(npm_kanit(n)))
        elif y == "UV": out.append([k, y, n] + list(uv_kanit(n)))
        else: out.append([k, y, n, "KANITSIZ", "?", "bilinmeyen yontem"])
    with open(R / "docs/video-tarama/kurulu-kanit-yeni.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["kalem", "yontem", "paket", "sonuc", "tur", "ayrinti"]); w.writerows(out)
    from collections import Counter; print(len(out), Counter(o[3] for o in out))
    for o in out:
        if o[3] != "KANIT": print(o[0], "|", o[5])
