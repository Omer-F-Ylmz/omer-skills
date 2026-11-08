import os, time, csv, collections
K = r"C:\Projeler\omer-skills"
def mt(p):
    try:
        return time.strftime("%d %H:%M", time.localtime(os.path.getmtime(p)))
    except Exception:
        return "YOK"
for f in [r"rapor\kur-tur2-plan.tsv", r"rapor\kur-tur2-sonuc.tsv", r"tmp\tur2-siniflar.tsv", r"docs\video-tarama\ana-liste.tsv", r"docs\video-tarama\kurulum-coz-6.tsv"]:
    print(f, mt(os.path.join(K, f)))
def say(f, kol):
    p = os.path.join(K, f)
    if not os.path.exists(p):
        return
    with open(p, encoding="utf-8", errors="replace") as h:
        r = list(csv.DictReader(h, delimiter="\t"))
    print(f, len(r), "satir")
    if r and kol in r[0]:
        print("  ", dict(collections.Counter(x[kol] for x in r).most_common(15)))
    else:
        print("  kolonlar", list(r[0].keys()) if r else [])
say(r"rapor\kur-tur2-plan.tsv", "eylem")
say(r"rapor\kur-tur2-sonuc.tsv", "sonuc")
say(r"docs\video-tarama\ana-liste.tsv", "durum")
