"""VIDEO-IZLE-KUR-1 adim 1: video-764 adaylari (kurulum-v1-plan.tsv) + kurulu isaretleme -> envanter.tsv.
Kurulu kaniti: ~/.claude/skills dizin adi, installed_plugins.json, 00-kurulu.txt, C:/AI/indirilen klonu,
kaynak-kutuphane envanteri, KURULUM-V1 karari. Kullanim: python -I -X utf8 video_izle_kur_1_envanter.py
"""
import csv, json, os, re
from pathlib import Path

K = Path(r"C:/Projeler/omer-skills")
H = Path.home() / ".claude"
OUT = K / ".kos/kopru/ogren/video-izle-kur-1/envanter.tsv"


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


skills = {norm(p.name): "skill:" + p.name for p in (H / "skills").iterdir()}
plug = {}
for k in json.load(open(H / "plugins/installed_plugins.json", encoding="utf-8")).get("plugins", {}):
    plug[norm(k.split("@")[0])] = "plugin:" + k
klon = {norm(p.name): "klon:" + p.name for p in Path(r"C:/AI/indirilen").iterdir()}
for p in Path(r"C:/AI/indirilen").iterdir():
    if "__" in p.name:
        klon[norm(p.name.split("__", 1)[1])] = "klon:" + p.name
kurulu_txt = norm((K / "docs/video-tarama/00-kurulu.txt").read_text(encoding="utf-8", errors="ignore"))
ek = norm((K / ".kos/kopru/ogren/video-izle-kur-1/kurulu-ek.txt").read_text(encoding="utf-8", errors="ignore"))
for sk in (H / "skills").glob("*/*/SKILL.md"):
    skills.setdefault(norm(sk.parent.name), "skill:" + sk.parent.parent.name + "/" + sk.parent.name)
kk = norm((K / "docs/kaynak-kutuphane/envanter.tsv").read_text(encoding="utf-8", errors="ignore"))


def kanit(ad, repo, karar):
    if karar.startswith(("KURULDU", "UYARLANDI")):
        return "KURULU", karar[:80]
    if karar.startswith("ELE"):
        return "ELE-V1", karar[:80]
    adlar = [norm(ad)]
    if repo and "/" in repo:
        adlar += [norm(repo.split("/")[-1]), norm(repo.replace("/", ""))]
    for a in [x for x in adlar if len(x) >= 4]:
        for d in (skills, plug):
            if a in d:
                return "KURULU", d[a]
        if a in klon:
            return "KLONLU", klon[a]
        if len(a) >= 6 and a in kurulu_txt:
            return "KURULU", "00-kurulu.txt"
        if len(a) >= 5 and a in ek:
            return "KURULU", "npm/uv/pip/mcp/tools"
        if len(a) >= 6 and a in kk:
            return "KURULU", "kaynak-kutuphane"
    return "KURULACAK", ""


rows = list(csv.DictReader(open(K / ".kos/kopru/ogren/kurulum-v1-plan.tsv", encoding="utf-8"), delimiter="\t"))
seen, out = set(), []
for r in rows:
    key = norm(r["repo"] or r["ad"])
    if key in seen:
        continue
    seen.add(key)
    durum, kn = kanit(r["ad"], r["repo"].strip(), r["karar"])
    out.append({"ad": r["ad"], "tür": r["tür"], "grup": r["grup"], "repo": r["repo"], "lisans": r["lisans"],
                "puan": r["ölçüt_puanı(0-8)"], "durum": durum, "kanıt": kn})
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
    w.writeheader()
    w.writerows(out)
from collections import Counter
print(len(rows), len(out), Counter(o["durum"] for o in out))
