"""INDIRME-HATA 'checkout failed' repolarını core.longpaths ile yeniden açar; sonucu .kos/kopru/checkout-onar.log'a yazar."""
import json, os, subprocess, time
K = r"C:\Projeler\omer-skills"
LOG = K + r"\.kos\kopru\checkout-onar.log"
def yaz(m):
    open(LOG, "a", encoding="utf-8").write(time.strftime("%H:%M:%S ") + m + "\n")
son = {}
for l in open(K + r"\.kos\kopru\kurulum-toplu.jsonl", encoding="utf-8", errors="replace"):
    try: o = json.loads(l); son[o.get("repo_istenen")] = o
    except: pass
for r, o in son.items():
    if o.get("durum") != "INDIRME-HATA" or "checkout failed" not in (o.get("hata") or ""):
        continue
    owner, repo = r.split("/")[:2]
    d = os.path.join(r"C:\Projeler\_araclar\v", f"{owner}__{repo}")
    if not os.path.isdir(os.path.join(d, ".git")):
        yaz(f"{r} klasor yok"); continue
    subprocess.run(["git", "-C", d, "config", "core.longpaths", "true"], capture_output=True)
    p = subprocess.run(["git", "-C", d, "restore", "--source=HEAD", ":/"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    if p.returncode == 0:
        durum = "INDIRILDI"
        not_ = "longpaths ile onarildi"
    else:
        sp = subprocess.run(["git", "-C", d, "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        eksik = len([x for x in sp.stdout.splitlines() if x.startswith(" D") or x.startswith("D")])
        durum = "KISMEN" if eksik else "INDIRILDI"
        not_ = f"Windows'a acilamayan {eksik} dosya; hata: {(p.stderr or '')[-160:]}"
    yaz(f"{r} -> {durum} | {not_}")
    with open(K + r"\.kos\kopru\kurulum-toplu.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"repo": r, "repo_istenen": r, "durum": durum, "yol": d, "not": not_, "kalemler": o.get("kalemler"), "zaman": time.strftime("%H:%M:%S")}, ensure_ascii=False) + "\n")
yaz("BITTI")
