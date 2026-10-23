"""VIDEO-SONRASI-1 adım 3-4: derin json'lardan araç adları + CC modları → arac-tam.tsv, modlar.tsv; sonra arac-indir-1 bulunamadı + yeni → gh eşle → indir (kurma yok).
Model yok: regex (github linki, kurulum komutu) + atlas adı sözlüğü + OCR yazım birleştirme; eşleme gh (video bağlamı = aynı videolardaki github linkleri). Kullanım: arac_cikar.py [--indir]"""
import collections
import csv
import difflib
import glob
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RAPOR = os.path.join(KOK, ".kos", "kopru", "rapor")
sys.path.insert(0, os.path.join(KOK, "tools"))


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


GH = re.compile(r"github\.com/([A-Za-z0-9][\w.-]{0,38})/([A-Za-z0-9][\w.-]{1,60})", re.I)
INS = re.compile(r"(?:npx(?:\s+-y)?|npm\s+(?:i|install)(?:\s+-g)?|pnpm\s+(?:add|dlx)|pip3?\s+install(?:\s+-U)?|uv\s+(?:tool\s+install|pip\s+install)|uvx|brew\s+install|winget\s+install|claude\s+plugin\s+install|/plugin\s+install)\s+([@\w./:-]{3,60})", re.I)
GENEL = {"install", "skills", "skill", "claude", "claude-code", "code", "awesome", "agents", "mcp", "plugins", "tools", "cli", "app", "docs", "main", "readme", "repo", "project", "example", "demo", "latest", "github", "issues", "topics", "features", "sponsors", "settings", "orgs", "marketplace", "blob", "tree", "pull", "actions", "releases", "wiki"}
SLASH = "plan model fast loop schedule compact clear init memory agents mcp plugin hooks permissions config context cost usage resume rewind review security-review output-style vim btw ultrareview ultraplan goal skills doctor export ide terminal-setup statusline add-dir teleport sandbox todos voice chrome remote-control batch simplify".split()
MOD_RE = re.compile(r"\b((?:[A-Za-z]+[ -])?[A-Za-z]+) mode\b")
MOD_DUR = {"the", "a", "in", "this", "that", "your", "my", "to", "of", "and", "or", "is", "on", "for", "it", "with", "when", "one", "another", "other", "same", "different", "default", "normal", "ve", "bir", "bu"}

atlas = set()
for s in open(os.path.join(KOK, "docs/atlas/kart.jsonl"), encoding="utf-8"):
    try:
        a = json.loads(s)["ad"]
    except (ValueError, KeyError):
        continue
    if len(norm(a)) >= 6 and (("-" in a) or len(a) >= 8):
        atlas.add(norm(a))

cand = collections.defaultdict(lambda: {"vid": set(), "ham": collections.Counter(), "ek": set(), "ko": set(), "link": set(), "tur": set()})
mod = collections.defaultdict(lambda: {"vid": set(), "ek": set(), "ko": set()})
dosya = sorted(glob.glob(os.path.join(KOK, "docs/video-tarama/derin/*.json")))
vid_gh = {}  # video → github owner/repo listesi (video bağlamı)
for f in dosya:
    d = json.load(open(f, encoding="utf-8"))
    kod = d.get("kod") or os.path.basename(f)[:-5]
    ek = "\n".join([str(e.get("t", "")) for e in d.get("ekran") or [] if isinstance(e, dict)] + [str(d.get("kare_aciklama") or "")] + [str(x) for x in d.get("linkler") or []] + [str(x) for x in d.get("komutlar") or []])
    ko = " ".join(str(s.get("t", "")) for s in d.get("transkript") or [] if isinstance(s, dict))
    gh = []
    for yer, txt in (("ek", ek), ("ko", ko)):
        for o, r in GH.findall(txt):
            r = re.sub(r"(\.git)?[.,;:)]*$", "", r)
            if o.lower() in GENEL or r.lower() in GENEL:
                continue
            k = norm(r)
            c = cand[k]
            c["vid"].add(kod); c["ham"][r] += 1; c[yer].add(kod); c["link"].add(f"https://github.com/{o}/{r}"); c["tur"].add("repo")
            gh.append(f"{o}/{r}")
        for m in INS.findall(txt):
            m = re.sub(r"(--\S*|@latest|@lat)$", "", m.strip(".,;:)\"'"))
            if m.endswith((".txt", ".json", ".py", ".md")) or m.startswith("http") or len(norm(m)) < 4:
                continue
            ad = m.split("/")[-1] if m.count("/") == 1 and not m.startswith("@") else m
            if ad.lower() in GENEL:
                continue
            k = norm(ad)
            c = cand[k]
            c["vid"].add(kod); c["ham"][ad] += 1; c[yer].add(kod); c["tur"].add("komut")
    vid_gh[kod] = gh
    for yer, txt in (("ek", ek), ("ko", ko)):  # atlas adı sözlüğü: ekranda/konuşmada geçen bilinen ad
        tok = [norm(t) for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9._-]*", txt)]
        for ngram in set(tok) | {a + b for a, b in zip(tok, tok[1:])}:
            if ngram in atlas:
                c = cand[ngram]
                c["vid"].add(kod); c["ham"][ngram] += 1; c[yer].add(kod); c["tur"].add("atlas")
    tum = ek + "\n" + ko
    if re.search(r"claude|anthropic", tum, re.I):
        for yer, txt in (("ek", ek), ("ko", ko)):
            for m in MOD_RE.findall(txt):
                m = m.lower().replace("-", " ")
                if m.split()[-1] in MOD_DUR or len(m) < 4:
                    continue
                x = mod["mod: " + m]
                x["vid"].add(kod); x[yer].add(kod)
            for m in re.findall(r"(?<![\w/.])/([a-z][a-z-]{2,20})\b", txt):
                if m in SLASH:
                    x = mod["slash: /" + m]
                    x["vid"].add(kod); x[yer].add(kod)

# OCR yazım kopyalarını birleştir: aynı ilk 3 harf, uzunluk farkı ≤1, benzerlik ≥0.9 → en çok videoda geçen yazım kalır
sirali = sorted(cand, key=lambda k: -len(cand[k]["vid"]))
kume = {}
kovalar = collections.defaultdict(list)
for k in sirali:
    hedef = next((h for h in kovalar[k[:3]] if abs(len(h) - len(k)) <= 1 and difflib.SequenceMatcher(None, h, k).ratio() >= 0.9), None)
    if hedef:
        kume[k] = hedef
        h, c = cand[hedef], cand[k]
        h["vid"] |= c["vid"]; h["ham"] += c["ham"]; h["ek"] |= c["ek"]; h["ko"] |= c["ko"]; h["link"] |= c["link"]; h["tur"] |= c["tur"]
    else:
        kovalar[k[:3]].append(k)
ana = [k for k in sirali if k not in kume]

envanter = ""
for f in glob.glob(os.path.join(RAPOR, "_inv_*.txt")):
    envanter += open(f, encoding="utf-8", errors="replace").read().lower() + "\n"
for t in (os.path.expanduser("~/.claude/skills"), os.path.expanduser("~/.claude/agents")):
    if os.path.isdir(t):
        envanter += "\n".join(os.listdir(t)).lower()
envn = re.sub(r"[^a-z0-9\n]", "", envanter)
satir = []
for k in ana:
    c = cand[k]
    ad = c["ham"].most_common(1)[0][0]
    yer = "+".join(y for y, n in (("ekranda", c["ek"]), ("konuşmada", c["ko"])) if n)
    kurulu = "evet" if len(k) >= 4 and k in envn else "hayır"
    v = sorted(c["vid"])
    satir.append([ad, f"{len(v)}:" + ",".join(v[:8]), yer, " ".join(sorted(c["link"]))[:200], kurulu, "+".join(sorted(c["tur"])), k])
satir.sort(key=lambda r: -int(r[1].split(":")[0]))
with open(os.path.join(RAPOR, "arac-tam.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["ad", "video_say:kodlar", "yer", "link", "kurulu", "tur", "norm"])
    w.writerows(satir)
mrows = sorted(([m, len(x["vid"]), "+".join(y for y, n in (("ekranda", x["ek"]), ("konuşmada", x["ko"])) if n), ",".join(sorted(x["vid"])[:5])] for m, x in mod.items() if len(x["vid"]) >= 3 or m.startswith("slash")), key=lambda r: -r[1])
with open(os.path.join(RAPOR, "modlar.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["mod", "video_say", "yer", "ornek_video"])
    w.writerows(mrows)
print("tekil araç", len(satir), "kurulu", sum(r[4] == "evet" for r in satir), "mod satırı", len(mrows), "birleşen yazım", len(kume), flush=True)

if "--indir" not in sys.argv:
    sys.exit()

# ---- adım 4: arac-indir-1 ile karşılaştır; yeni + bulunamadı → video bağlamıyla gh eşle → indir
import arac_indir_1 as ai  # noqa: E402

eski = {}
with open(os.path.join(RAPOR, "arac-indir-1.tsv"), encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        eski[norm(r["ad"])] = r
bul = [r for r in eski.values() if r["durum"] == "bulunamadi"]
indirilmis = {norm(r["ad"].split("/")[-1]) for r in eski.values() if r["durum"] in ("indirildi", "buyuk-ertelendi")}
yeni = [r for r in satir if r[6] not in eski and r[4] == "hayır" and "atlas" not in r[5] and r[6] not in indirilmis and ("repo" in r[5] or "komut" in r[5])]
is_listesi = []
for r in bul:
    vids = [v for v in r["video"].split(",") if v]
    ham = {g for v in vids for g in vid_gh.get(v, []) if difflib.SequenceMatcher(None, norm(g.split("/")[1]), norm(r["ad"])).ratio() >= 0.6}
    is_listesi.append({"ad": r["ad"], "ham": "|".join(sorted(ham)), "ornek_video": "[" + ",".join(vids) + "]", "tip": "bulunamadi-yeniden"})
for r in yeni:
    ham = "|".join(sorted({u.split("github.com/")[1] for u in r[3].split() if "github.com/" in u}))
    is_listesi.append({"ad": r[0], "ham": ham, "ornek_video": "[" + r[1].split(":")[1] + "]", "tip": "yeni"})
print("adım4 iş:", collections.Counter(s["tip"] for s in is_listesi), flush=True)
with ThreadPoolExecutor(8) as ex:
    sonuc = list(ex.map(ai.coz, is_listesi))
tekil, cikti = {}, []
for s, (d, kaynak) in zip(is_listesi, sonuc):
    v = s["ornek_video"].strip("[]")
    if d is None:
        cikti.append([s["ad"], "-", "bulunamadi", "-", "-", v])
        continue
    k = d["nameWithOwner"].lower()
    if k in tekil:
        tekil[k]["video"] += "," + v
    elif not os.path.isdir(os.path.join(ai.HEDEF, d["nameWithOwner"].replace("/", "__"))):
        tekil[k] = {"d": d, "kaynak": kaynak + "/" + s["tip"], "video": v}
    else:
        cikti.append([d["nameWithOwner"], "-", "zaten-indirilmis", "-", "-", v])
print("eşlenen tekil yeni repo", len(tekil), "bulunamayan", sum(c[2] == "bulunamadi" for c in cikti), flush=True)
liste = list(tekil.values())[:200]  # tavan: en çok 200 klon
with ThreadPoolExecutor(4) as ex:
    for sat in ex.map(ai.isle, liste):
        cikti.append(sat)
        print(sat[0], sat[2], sat[4], flush=True)
with open(os.path.join(RAPOR, "arac-indir-2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["ad", "kaynak", "durum", "boyut", "tarama", "video"])
    w.writerows(cikti)
print("BITTI", collections.Counter(c[2] for c in cikti), flush=True)
