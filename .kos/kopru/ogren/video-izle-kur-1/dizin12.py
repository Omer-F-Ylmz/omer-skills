# TUR 12: NİHAİ 36(J) — kurulan her kalem envanter.tsv + kayit.jsonl'de mi; eksikleri ekler (--yaz)
import csv, json, sys, re
from pathlib import Path
K = Path(r"C:\Projeler\omer-skills")
D = K / ".kos/kopru/ogren/video-izle-kur-1"
son = {}
for f in sorted(D.glob("kur-tur*.tsv"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0)):
    for r in csv.reader(open(f, encoding="utf-8", errors="replace"), delimiter="\t"):
        if len(r) >= 2 and r[0] and r[0] != "ad":
            if "/" in r[1] and len(r) > 2:  # tur6/7 biçimi: ad, repo, durum, kanit, yer
                son[r[0]] = (r[2], r[4] if len(r) > 4 else "", f.name)
            else:
                son[r[0]] = (r[1], r[3] if len(r) > 3 else "", f.name)
for r in csv.reader(open(D / "skill-kur.tsv", encoding="utf-8", errors="replace"), delimiter="\t"):
    if len(r) >= 4 and r[0] != "ad" and "kuruldu" in r[3]:
        son.setdefault(r[2] or r[0], ("skill-kuruldu", "~/.claude/skills", "skill-kur.tsv"))
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
env = (K / "docs/envanter/envanter.tsv").read_text(encoding="utf-8")
kay = (K / "docs/kurulumlar/kayit.jsonl").read_text(encoding="utf-8")
envn = {norm(l.split("	")[0]) for l in env.splitlines()}
kayn = {norm(l.split('"ad": "')[1].split('"')[0]) for l in kay.splitlines() if '"ad": "' in l}
tek = {norm(a): (a, v) for a, v in son.items()}  # "HTML Anything" / "HTML_Anything" tek kalem, son tur kazanır
eksik = []
for ad, (dur, yer, kaynak) in tek.values():
    if not re.search(r"calisiyor|çalışıyor|kuruldu", dur):
        continue
    e, k = norm(ad) in envn, norm(ad) in kayn
    print(f"{ad}\t{dur}\tenv={int(e)}\tkayit={int(k)}")
    if not (e and k):
        eksik.append((ad, dur, yer, kaynak, e, k))
print("EKSIK", len(eksik))
if "--yaz" in sys.argv:
    with open(K / "docs/envanter/envanter.tsv", "ab") as fe, open(K / "docs/kurulumlar/kayit.jsonl", "ab") as fk:
        for ad, dur, yer, kaynak, e, k in eksik:
            tur = "skill" if dur.startswith("skill") else "arac"
            if not e:
                fe.write(("\t".join([ad.lower().replace("_", "-"), tur, "CC", "1", f"VIDEO-IZLE-KUR-1 {dur}; {yer}"[:200], "", "", "kurulum:2026-10-30", "CC", f".kos/kopru/ogren/video-izle-kur-1/{kaynak}"]) + "\n").encode("utf-8"))
            if not k:
                fk.write((json.dumps({"ad": ad.lower().replace("_", "-"), "karar": f"KURULDU {dur}", "tarih": "2026-10-30", "parti": "video-izle-kur-1"}, ensure_ascii=False) + "\n").encode("utf-8"))
    print("YAZILDI")
