"""VAR-YENIDEN (5 Kas): kurulum-toplu.jsonl'daki 'VAR' kayitlarinin cogu yalniz klasor ADI eslesmesi
(or. remotion-dev/skills, mattpocock/skills, anthropics/skills hepsi ~/.claude/skills/skills -> baska skill).
Her supheli kayit: yolun git remote'u repo ile eslesiyorsa GERCEK-VAR; degilse repo dogrulanir ve
C:\\Projeler\\_araclar\\v\\owner__repo'ya indirilir (>300MB -> BUYUK-SOR, yok -> REPO-YOK).
python tools/var_yeniden.py  -> .kos/kopru/var-yeniden.log + kurulum-toplu.jsonl (kaynak=var_yeniden)
"""
import json, os, re, subprocess, sys, time, shutil
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "tools"))
import kurulum_coz2 as K  # noqa: E402
LOG = os.path.join(KOK, ".kos", "kopru", "var-yeniden.log")


def yaz(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(s, flush=True)
    open(LOG, "a", encoding="utf-8").write(s + "\n")


def kayit(d):
    d["kaynak"] = "var_yeniden"; d["zaman"] = time.strftime("%H:%M:%S")
    open(K.TOPLU, "a", encoding="utf-8").write(json.dumps(d, ensure_ascii=False) + "\n")


def remote(y):
    try:
        r = subprocess.run(["git", "-C", y, "config", "--get", "remote.origin.url"], capture_output=True, text=True, timeout=20)
        return r.stdout.strip().lower()
    except Exception:
        return ""


t = [json.loads(l) for l in open(K.TOPLU, encoding="utf-8", errors="replace") if l.strip()]
son = {}
for x in t:
    son[x.get("repo_istenen")] = x
isler, gorulen = [], set()
for ist, x in son.items():
    if x.get("durum") != "VAR" or x.get("kaynak") == "var_yeniden":
        continue
    rp = x.get("repo") or ""
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", rp):
        continue
    owner, repo = rp.split("/")
    y = x.get("yol") or ""
    if os.path.basename(y.rstrip("\\/")).lower() == f"{owner}__{repo}".lower():
        continue
    if rp.lower() in gorulen:
        continue
    gorulen.add(rp.lower())
    isler.append((ist, rp, y))
yaz("supheli", len(isler))
say = {}
for i, (ist, rp, y) in enumerate(isler, 1):
    owner, repo = rp.split("/")
    rm = remote(y) if os.path.isdir(y) else ""
    if rm and f"{owner}/{repo}".lower() in rm.replace(".git", ""):
        d = {"repo": rp, "durum": "GERCEK-VAR", "yol": y}
    else:
        hedef = os.path.join(K.HEDEF, f"{owner}__{repo}")
        if os.path.isdir(hedef):
            d = {"repo": rp, "durum": "VAR", "yol": hedef}
        else:
            rc, o, e = K.k(["gh", "api", f"repos/{owner}/{repo}", "--jq", "[.full_name,.size,.license.spdx_id,.stargazers_count]|@tsv"], 60)
            if rc != 0:
                d = {"repo": rp, "durum": "REPO-YOK", "eski_yol": y, "hata": (e or "")[:120]}
            else:
                p = o.strip().split("\t")
                gercek = p[0] if p and "/" in p[0] else rp
                mb = int(p[1]) / 1024 if len(p) > 1 and p[1].isdigit() else 0
                hedef = os.path.join(K.HEDEF, gercek.replace("/", "__"))
                if os.path.isdir(hedef):
                    d = {"repo": gercek, "durum": "VAR", "yol": hedef}
                elif mb > 300:
                    d = {"repo": gercek, "durum": "BUYUK-SOR", "mb": round(mb), "eski_yol": y}
                elif shutil.disk_usage("C:\\").free / 2**30 < 45:
                    d = {"repo": gercek, "durum": "DISK-BEKLE"}
                else:
                    rc, o, e = K.k(["git", "clone", "--depth", "1", "--single-branch", "--no-tags", f"https://github.com/{gercek}.git", hedef], 900)
                    d = {"repo": gercek, "durum": "INDIRILDI" if rc == 0 else "INDIRME-HATA", "yol": hedef, "mb": round(mb), "eski_yol": y}
                    if rc != 0:
                        d["hata"] = (e or "")[-150:]
    d["repo_istenen"] = ist
    kayit(d)
    say[d["durum"]] = say.get(d["durum"], 0) + 1
    if i % 10 == 0:
        yaz(i, "/", len(isler), say)
yaz("BITTI", say)
