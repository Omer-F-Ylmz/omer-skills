import os, csv, collections, subprocess, glob
K = r"C:\Projeler\omer-skills"
with open(os.path.join(K, r"rapor\kur-tur2-sonuc.tsv"), encoding="utf-8", errors="replace") as h:
    r = list(csv.DictReader(h, delimiter="\t"))
print("tur2 sonuc durum", dict(collections.Counter(x["durum"] for x in r)))
print("tur2 sonuc eylem x durum", dict(collections.Counter((x["eylem"], x["durum"]) for x in r).most_common(12)))
def g(*a):
    return subprocess.run(["git", *a], cwd=K, capture_output=True, text=True, errors="ignore").stdout.strip()
print("hooksPath:", repr(g("config", "--get", "core.hooksPath")))
st = g("status", "--porcelain").splitlines()
print("git degisen dosya", len(st))
print("son commit", g("log", "-1", "--format=%ci %s"))
print("onde commit", g("rev-list", "--count", "@{u}..HEAD"))
logs = sorted(glob.glob(os.path.join(K, r"tmp\le_haiku*.log")), key=os.path.getmtime)
if logs:
    print("son haiku log", os.path.basename(logs[-1]), open(logs[-1], encoding="utf-8", errors="replace").read()[-300:])
sk = os.path.expanduser(r"~\.claude\skills")
print("skills klasor", len(os.listdir(sk)) if os.path.isdir(sk) else "yok")
