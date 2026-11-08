"""KURULUM-COZ-1: SKILL/CLI/PAKET/MODEL kalemlerinin kaynağını doğrular.
Sıra: klon/kurulu skill dizini eşleşmesi → model önerisi doğrulama (gh/pypi/npm/hf) → gh arama (ad benzerliği ≥0.8).
Çıktı docs/video-tarama/kurulum-coz.tsv; yeniden koşunca biten kalemler atlanır."""
import csv, json, re, subprocess, sys, io, time, urllib.request, urllib.parse
from difflib import SequenceMatcher
from pathlib import Path
KOK = Path(__file__).resolve().parents[1] / "docs/video-tarama"
CIK = KOK / "kurulum-coz.tsv"
NW = 0x08000000
DIZIN = [Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar"), Path.home() / ".claude/skills", Path.home() / ".claude/plugins"]


def norm(s):
    s = re.sub(r"\b(skill|skills|plugin|mcp|server|cli|agent|ajan|becerisi)\b", " ", s.lower())
    return re.sub(r"[^a-z0-9]+", "", s)


def skill_dizini():
    idx = {}
    for d in DIZIN:
        if not d.exists():
            continue
        for f in d.rglob("SKILL.md"):
            try:
                m = re.search(r"^name:\s*['\"]?([^'\"\n]+)", f.read_text(encoding="utf-8", errors="ignore")[:800], re.M)
            except OSError:
                continue
            ad = m.group(1).strip() if m else f.parent.name
            for k in {norm(ad), norm(f.parent.name)}:
                if k:
                    idx.setdefault(k, str(f.parent))
    return idx


def http_var(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "omer-skills"}), timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


def gh(a):
    r = subprocess.run(["gh"] + a, capture_output=True, text=True, encoding="utf-8", errors="ignore", creationflags=NW)
    return r.returncode, r.stdout


def dogrula(k):
    t, _, v = k.partition(":")
    v = v.strip().strip("/")
    if t == "gh" and re.fullmatch(r"[\w.-]+/[\w.-]+", v):
        c, o = gh(["api", "repos/" + v, "--jq", ".full_name"])
        return ("gh:" + o.strip()) if c == 0 else ""
    if t == "pip" and v:
        return "pip:" + v if http_var(f"https://pypi.org/pypi/{urllib.parse.quote(v)}/json") else ""
    if t == "npm" and v:
        return "npm:" + v if http_var(f"https://registry.npmjs.org/{urllib.parse.quote(v, safe='@')}") else ""
    if t == "hf" and re.fullmatch(r"[\w.-]+/[\w.-]+", v):
        return "hf:" + v if http_var(f"https://huggingface.co/api/models/{v}") else ""
    if t == "url" and "github.com/" in v:
        m = re.search(r"github\.com/([\w.-]+/[\w.-]+)", v)
        return dogrula("gh:" + m.group(1)) if m else ""
    return ""


def gh_ara(ad):
    q = re.sub(r"[^\w\s.-]", " ", ad).strip()
    if len(q) < 3:
        return "", 0
    c, o = gh(["search", "repos", q, "--limit", "5", "--sort", "stars", "--json", "fullName,stargazersCount"])
    time.sleep(2.2)
    if c:
        return "", 0
    en, puan = "", 0
    for x in json.loads(o or "[]"):
        p = SequenceMatcher(None, norm(ad), norm(x["fullName"].split("/")[1])).ratio()
        if p > puan:
            en, puan = x["fullName"], p
    return en, round(puan, 2)


def main():
    idx = skill_dizini()
    print("skill dizini", len(idx), flush=True)
    R = [r for r in csv.DictReader(open(KOK / "kurulum-ad.tsv", encoding="utf-8"), delimiter="\t") if r["sinif"] in ("SKILL", "CLI", "PAKET", "MODEL")]
    bitmis = set()
    if CIK.exists():
        bitmis = {r["kalem"] for r in csv.DictReader(open(CIK, encoding="utf-8"), delimiter="\t")}
    yeni = not CIK.exists()
    f = open(CIK, "a", encoding="utf-8", newline="")
    w = csv.writer(f, delimiter="\t")
    if yeni:
        w.writerow(["kalem", "sinif", "sonuc", "kaynak", "puan", "yol"])
    n = 0
    for r in R:
        if r["kalem"] in bitmis:
            continue
        k = norm(r["ad"] or r["kalem"])
        if k and k in idx:
            w.writerow([r["kalem"], r["sinif"], "BIZDE-SKILL", "", 1, idx[k]])
        else:
            v = dogrula(r["kaynak"]) if r["kaynak"] else ""
            if v:
                w.writerow([r["kalem"], r["sinif"], "DOGRULANDI", v, 1, ""])
            elif r["sinif"] == "MODEL":
                w.writerow([r["kalem"], r["sinif"], "MODEL-TURU", r["kaynak"], 0, ""])
            else:
                en, p = gh_ara(r["ad"] or r["kalem"])
                w.writerow([r["kalem"], r["sinif"], "ADAY" if p >= 0.8 else "BULUNAMADI", "gh:" + en if en else "", p, ""])
        f.flush()
        n += 1
        if n % 20 == 0:
            (KOK / "kurulum-coz.ilerleme").write_text(f"{n}/{len(R)}")
    (KOK / "kurulum-coz.ilerleme").write_text(f"BITTI {n}")
    print("BITTI", n, flush=True)
    print("BITIS", flush=True)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
