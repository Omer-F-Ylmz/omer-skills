import re
t = open(r"C:\Projeler\omer-skills\tools\kurulum_tur2.py", encoding="utf-8", errors="ignore").read().splitlines()
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\tur2_haric_bak.log", "w", encoding="utf-8")
for i, l in enumerate(t, 1):
    if re.search(r"aircrack|afl|wifite|haric|HARIC|def |--uygula|kur-tur2-plan|args\.uygula|args\.plan", l):
        print(i, l[:160], file=out)
for l in open(r"C:\Projeler\omer-skills\rapor\kur-tur2-plan.tsv", encoding="utf-8", errors="ignore"):
    if re.search(r"aircrack|afl|wifite", l, re.I): print("PLAN:", l.strip()[:200], file=out)
print("BITTI", file=out)
