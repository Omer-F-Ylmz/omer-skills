"""KURULUM-D2C adim 4: kurulu tekil kalemler icin calistirma kaniti (skill: SKILL.md+frontmatter; CLI: --version/--help exit 0; paket: import/resolve).
Cikti docs/video-tarama/kurulu-kanit.tsv (kalem,sinif,durum,sonuc KANIT|KANITSIZ,tur,ayrinti). Kurulum yapmaz."""
import csv, re, shutil, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R = Path(__file__).resolve().parents[1]; K = R / "docs/video-tarama"
NW = 0x08000000
VENVK = Path.home() / ".venvs/ana-liste312"; VENV = Path.home() / ".venvs/ana-liste"; NPM = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste-npm")
KUR = {"KURULDU", "KURULDU-SARMALAYICI", "KURULDU-KAYNAK", "KURULDU-KUTUPHANE", "ZATEN"}
def oku(p): return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
def run(a, t=8, cwd=None):
    t = min(t, 8)  # D2C: kalem basina en fazla 8 sn
    try:
        r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=t, stdin=subprocess.DEVNULL, creationflags=NW, cwd=cwd)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e: return -1, type(e).__name__
def skill_kanit(yol):
    p = Path(yol)
    if not yol or not p.exists(): return None
    f = p if p.is_file() else (p / "SKILL.md" if (p / "SKILL.md").exists() else next(iter(sorted(p.rglob("SKILL.md"))[:1]), None))
    if not f: return None
    t = f.read_text(encoding="utf-8", errors="ignore")[:1500]
    if t.startswith("---") and re.search(r"^name:\s*\S", t, re.M): return f"SKILL.md frontmatter name ok ({f.name})"
    return None
def cli_adaylari(r):
    ad = r["kaynak"].split(":", 1)[-1].split("/")[-1]
    m = re.findall(r"([\w.-]+)\.(?:cmd|exe)", r["not"])
    return list(dict.fromkeys([x.lower() for x in m] + [r["kalem"].lower().replace(" ", "-"), r["kalem"].lower().replace(" ", ""), ad.lower()]))
def isle(r):
    k, s, d, y = r["kalem"], r["sinif"], r["durum"], r["yol"]
    sk = skill_kanit(y) if s in ("SKILL", "CLI", "MODEL", "PAKET") else None
    if s == "SKILL":
        return (k, s, d, "KANIT", "skill", sk) if sk else (k, s, d, "KANITSIZ", "skill", "SKILL.md/frontmatter yok: " + y[-60:])
    if s == "CLI":
        for n in cli_adaylari(r):
            p = shutil.which(n) or shutil.which(n + ".cmd")
            if not p: continue
            for a in ("--version", "--help"):
                c, o = run([p, a])
                if c == 0 and o: return (k, s, d, "KANIT", "cli", f"{n} {a} exit0: {o.splitlines()[0][:60]}")
        if sk: return (k, s, d, "KANIT", "skill-sarmalayici", sk)
        return (k, s, d, "KANITSIZ", "cli", "PATH'te --version/--help calisan exe yok; kaynak yolu: " + (y[-60:] or "-"))
    if s == "PAKET":
        if sk: return (k, s, d, "KANIT", "skill", sk)
        m = re.search(r"import (\w[\w.]*) ok", r["not"]); pv = re.search(r"py(3\.\d+)", r["not"])
        if m:
            for v in ([pv.group(1)] if pv else ["3.12", "3.13"]):
                for vd in list(VENVK.glob(f"*-{v}")):
                    c, o = run([str(vd / "Scripts/python.exe"), "-c", f"import {m.group(1)}"], 60)
                    if c == 0: return (k, s, d, "KANIT", "import", f"{vd.name}: import {m.group(1)} ok")
        pn = re.sub(r"[^\w@/.-]", "", k)
        if (NPM / "node_modules" / k / "package.json").exists():
            c, o = run(["node", "--input-type=module", "-e", f"console.log(import.meta.resolve('{k}'))"], 40, cwd=str(NPM))
            if c == 0: return (k, s, d, "KANIT", "npm-resolve", "import.meta.resolve ok")
        if y and Path(y).exists(): return (k, s, d, "KANITSIZ", "paket", "kaynak/klon var, calisma kaniti yok: " + y[-50:])
        return (k, s, d, "KANITSIZ", "paket", "import/resolve dogrulanamadi; kurulum notu: " + r["not"][:60])
    if s == "MODEL":
        if sk: return (k, s, d, "KANIT", "skill", sk)
        p = Path(y)
        if y and p.exists() and any(p.rglob("*.safetensors")) or (y and p.exists() and any(p.rglob("*.bin"))): return (k, s, d, "KANIT", "model-dosya", "agirlik dosyasi var")
        return (k, s, d, "KANITSIZ", "model", "agirlik dosyasi/skill yok")
    return (k, s, d, "KANITSIZ", "?", "bilinmeyen sinif")
if __name__ == "__main__":
    # parti parti, .ilerleme ile devam: tekrar kosulunca biten kalemler atlanir
    import os
    son = {r["kalem"]: r for r in oku(K / "kurulum-d2-sonuc.tsv")}
    todo = [r for r in son.values() if r["durum"] in KUR]
    cikti = K / "kurulu-kanit.tsv"; yeni = not cikti.exists()
    biten = {r["kalem"] for r in oku(cikti)} if not yeni else set()
    todo = [r for r in todo if r["kalem"] not in biten]
    PARTI = int(os.environ.get("PARTI", "60"))
    with open(cikti, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="	")
        if yeni: w.writerow(["kalem", "sinif", "durum", "sonuc", "tur", "ayrinti"])
        for i in range(0, len(todo), PARTI):
            with ThreadPoolExecutor(6) as ex: out = list(ex.map(isle, todo[i:i + PARTI]))
            w.writerows(out); f.flush()
            (K / "kurulu-kanit.ilerleme").write_text(str(len(biten) + i + len(out)), encoding="utf-8")
            print(i + len(out), "/", len(todo), flush=True)
    from collections import Counter
    print(Counter((r["sinif"], r["sonuc"]) for r in oku(cikti)))
