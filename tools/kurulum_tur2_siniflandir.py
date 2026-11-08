"""KUR-TUR2: HATA/YOLU-YOK kalemlerin klon dizinine bakip kok nedeni ve cozum grubunu belirler -> tmp/tur2-siniflar.tsv (kanit: dizin ogeleri)."""
import csv, json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
S = R / "docs/video-tarama/kurulum-d2-sonuc.tsv"
son = {}
for r in csv.DictReader(open(S, encoding="utf-8"), delimiter="\t"): son[r["kalem"]] = r
def bak(d):
    d = Path(d)
    if not d.is_dir(): return "YOK-DIZIN", ""
    ad = {p.name for p in d.iterdir()}
    k = []
    if (d / ".claude-plugin").exists() or "plugin.json" in ad: k.append("plugin")
    if "skills" in ad or ".claude" in ad: k.append("skills-alt")
    if "pyproject.toml" in ad or "setup.py" in ad: k.append("py")
    if "package.json" in ad:
        try: pj = json.loads((d / "package.json").read_text(encoding="utf-8"))
        except Exception: pj = {}
        k.append("npm-bin" if pj.get("bin") else "npm-lib" + ("-ws" if pj.get("workspaces") else ""))
    if "Cargo.toml" in ad: k.append("cargo")
    if "go.mod" in ad: k.append("go")
    if "CMakeLists.txt" in ad: k.append("cmake")
    if "Makefile" in ad: k.append("make")
    if any(n.endswith((".sln", ".csproj")) for n in ad): k.append("dotnet")
    if "Dockerfile" in ad or "docker-compose.yml" in ad: k.append("docker")
    if "README.md" in ad and len(k) == 0: k.append("yalniz-readme")
    return "+".join(k) or "bos", ",".join(sorted(ad)[:12])
o = csv.writer(open(R / "tmp/tur2-siniflar.tsv", "w", encoding="utf-8", newline=""), delimiter="\t")
o.writerow(["kalem", "durum", "sinif", "kaynak", "neden", "dizin_turu", "dizin_ogeleri", "not"])
for k, r in son.items():
    if r["durum"] not in ("HATA", "KURULUM-YOLU-YOK", "KURULDU-DOGRULANMADI"): continue
    n = r["not"]
    for pat, g in (("SKILL.md bulunamad", "skill-yok"), ("package.json 'bin'", "bin-yok"), ("çok büyük", "buyuk"), ("repo (", "buyuk"),
                   ("EBUSY", "npm-ebusy"), ("npm", "npm-diger"), ("uv tool", "pip-uv"), ("pip:", "pip-uv"), ("0 skill", "npm-0skill"),
                   ("klon:", "klon"), ("release", "release"), ("win-x64 release asset yok", "yolu-yok"), ("LLM", "llm")):
        if pat in n: neden = g; break
    else: neden = "diger"
    if r["durum"] == "KURULUM-YOLU-YOK": neden = "yolu-yok"
    if r["durum"] == "KURULDU-DOGRULANMADI": neden = "dogrulanmadi"
    dt, oge = bak(r["yol"]) if r["yol"] else ("yolsuz", "")
    o.writerow([k, r["durum"], r["sinif"], r["kaynak"], neden, dt, oge, n[:140]])
