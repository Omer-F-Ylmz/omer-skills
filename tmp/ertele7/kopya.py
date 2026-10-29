"""ERTELE-3 (1): yüklenen skill/ajan kaynaklarında içerik-hash birebir kopyaları ve liste maliyeti."""
import hashlib, json, re, collections
from pathlib import Path
EV, KOK = Path.home() / ".claude", Path("C:/Projeler/omer-skills")


def on(f):
    t = f.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"---\s*\n(.*?)\n---", t, re.S)
    fm = m.group(1) if m else ""
    ad = re.search(r"^name:\s*(.+)$", fm, re.M)
    ac = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", fm, re.M)
    return (ad.group(1).strip().strip("'\"") if ad else f.parent.name), (ac.group(1).strip() if ac else ""), \
        hashlib.sha256(t.replace("\r\n", "\n").encode()).hexdigest()


kayit = []  # (tur, kaynak, ad, desc_kr, hash, yol)
for kaynak, kok in (("user", EV / "skills"), ("proje", KOK / ".claude" / "skills")):
    for f in kok.glob("**/SKILL.md"):
        k = "sync" if "synced" in f.parts else kaynak
        ad, ac, h = on(f); kayit.append(("skill", k, ad, len(ad) + len(ac), h, str(f)))
for kaynak, kok in (("user", EV / "agents"), ("proje", KOK / ".claude" / "agents")):
    for f in kok.glob("*.md"):
        ad, ac, h = on(f); kayit.append(("ajan", kaynak, ad, len(ad) + len(ac), h, str(f)))
kurulu = json.loads((EV / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
etkin = json.loads((EV / "settings.json").read_text(encoding="utf-8")).get("enabledPlugins", {})
for anahtar, ks in kurulu.get("plugins", kurulu).items():
    if etkin.get(anahtar) is False:
        continue
    for k in ks:
        p = Path(k["installPath"])
        for f in p.glob("**/SKILL.md"):
            ad, ac, h = on(f); kayit.append(("skill", "plugin:" + anahtar.split("@")[0], ad, len(ad) + len(ac), h, str(f)))
        for f in p.glob("agents/**/*.md"):
            ad, ac, h = on(f); kayit.append(("ajan", "plugin:" + anahtar.split("@")[0], ad, len(ad) + len(ac), h, str(f)))
grup = collections.defaultdict(list)
for r in kayit:
    grup[(r[0], r[4])].append(r)
kop = {k: v for k, v in grup.items() if len(v) > 1}
fazla_kr = sum(sum(r[3] for r in v[1:]) for v in kop.values())
kaynak_kr = collections.Counter()
for r in kayit:
    kaynak_kr[(r[0], r[1].split(":")[0] if not r[1].startswith("plugin") else r[1])] += r[3]
cift_kaynak = collections.Counter(tuple(sorted({r[1] for r in v})) for v in kop.values())
out = {"toplam": collections.Counter(r[0] for r in kayit), "kopya_grup": len(kop),
       "fazla_kopya": sum(len(v) - 1 for v in kop.values()), "fazla_kr": fazla_kr,
       "kopya_kaynak_ciftleri": [[list(k), n] for k, n in cift_kaynak.most_common(25)],
       "kaynak_kr_ilk40": [[list(k), n] for k, n in kaynak_kr.most_common(40)],
       "ornek": [[(r[1], r[2], r[5]) for r in v] for v in list(kop.values())[:15]]}
json.dump(out, open("tmp/ertele7/kopya.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out["toplam"], "kopya grup", out["kopya_grup"], "fazla", out["fazla_kopya"], "fazla_kr", fazla_kr)
for k, n in cift_kaynak.most_common(12):
    print(n, k)
