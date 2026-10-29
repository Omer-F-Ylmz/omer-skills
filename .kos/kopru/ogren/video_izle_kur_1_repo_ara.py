"""VIDEO-IZLE-KUR-1: kurulacaklar.tsv'de repo/URL'i olmayan kalemler için gh search repos ile ilk 3 aday -> repo-aday.tsv.
Aday doğrulanmış değildir; kurulum turunda videodaki kanıtla eşlenir. Kullanim: python -I video_izle_kur_1_repo_ara.py
"""
import csv, json, os, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = Path(r"C:/Projeler/omer-skills/.kos/kopru/ogren/video-izle-kur-1")
rows = list(csv.DictReader(open(D / "kurulacaklar.tsv", encoding="utf-8"), delimiter="\t"))
eski = {}
if (D / "repo-aday.tsv").exists():  # önceki koşudan bulunanlar yeniden aranmaz
    eski = {r["kalem"]: r for r in csv.DictReader(open(D / "repo-aday.tsv", encoding="utf-8"), delimiter="\t") if r["aday"] != "aday yok"}
out, bos = [], 0
for r in rows:
    if not r["kurulum_yolu"].startswith("repo/URL"):
        continue
    if r["kalem"] in eski:
        out.append(eski[r["kalem"]])
        continue
    time.sleep(2.2)  # gh search sınırı 30/dk
    p = subprocess.run(["gh", "search", "repos", r["kalem"], "--limit", "3", "--sort", "stars",
                        "--json", "fullName,stargazersCount,description"], capture_output=True, text=True, encoding="utf-8",
                       env=os.environ.copy(), timeout=60)
    try:
        ad = json.loads(p.stdout or "[]")
    except json.JSONDecodeError:
        ad = []
    bos += not ad
    out.append({"kalem": r["kalem"], "tür": r["tür"],
                "aday": " | ".join(f"{a['fullName']} ★{a['stargazersCount']} — {(a['description'] or '')[:70]}" for a in ad) or "aday yok"})
with open(D / "repo-aday.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["kalem", "tür", "aday"], delimiter="\t")
    w.writeheader()
    w.writerows(out)
print("aranan", len(out), "aday yok", bos)
