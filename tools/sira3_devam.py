import csv, re, subprocess, json, time, urllib.request, sys, os
K = r"C:\Projeler\omer-skills"
os.chdir(K)
if len(sys.argv) < 2:
    subprocess.Popen([sys.executable, "-I", __file__, "calis"], cwd=K, creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(r"tmp\sira3_devam.log", "a", encoding="utf-8", buffering=1)
gir = list(csv.DictReader(open(r"tmp\sira3-girdi-0811.tsv", encoding="utf-8"), delimiter="\t"))
yapildi = set()
OUT = r"tmp\bulunan-0811.tsv"
for r in csv.reader(open(OUT, encoding="utf-8", errors="replace"), delimiter="\t"):
    if r: yapildi.add(r[0])
print(time.strftime("%H:%M:%S"), "girdi", len(gir), "yapildi", len(yapildi) - 1, file=LOG)
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "omer-skills-sira3"}), timeout=15).status
    except Exception: return 0
out = open(OUT, "a", encoding="utf-8")
hata = 0
for r in gir:
    k, s = r["kalem"], r["sinif"]
    if k in yapildi: continue
    n = norm(k); slug = re.sub(r"[^a-z0-9-]", "-", k.lower()).strip("-")
    best = ("", "", "", "")
    if len(n) >= 3:
        if get("https://pypi.org/pypi/" + slug + "/json") == 200: best = ("PYPI", slug, "tam-ad", "")
        elif get("https://registry.npmjs.org/" + slug) == 200: best = ("NPM", slug, "tam-ad", "")
        if not best[0]:
            for den in range(4):
                p = subprocess.run(["gh", "search", "repos", k, "--limit", "3", "--json", "fullName,stargazersCount"], capture_output=True, text=True, encoding="utf-8", errors="replace")
                if p.returncode == 0: break
                print(time.strftime("%H:%M:%S"), "gh hata", k, p.stderr[:150].replace("\n", " "), file=LOG)
                time.sleep(60 * (den + 1))
            time.sleep(2.2)
            try:
                for x in json.loads(p.stdout):
                    rn = norm(x["fullName"].split("/")[1])
                    if rn == n: best = ("GH", x["fullName"], "tam-ad", ""); break
                    if not best[0] and (n in rn or rn in n) and x["stargazersCount"] >= 50: best = ("GH", x["fullName"], "bulanik", f"{x['stargazersCount']}*")
            except Exception:
                hata += 1
    out.write("\t".join([k, s, best[0] or "YOK", best[1], best[2], best[3]]) + "\n"); out.flush()
print(time.strftime("%H:%M:%S"), "BITTI parse_hata", hata, file=LOG)
