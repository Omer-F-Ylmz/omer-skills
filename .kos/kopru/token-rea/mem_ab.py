"""claude-mem arama A/B: worker /api/search (A) vs mem2 (B). Held-out: tohumla betikle örneklenen gözlemler,
anahtar = gözlem id'si (ilk 5'te mi). Kullanım: python -I -S mem_ab.py <tohum> [n]  — Claude çağrısı yok."""
import json
import os
import random
import re
import sqlite3
import subprocess
import sys
import time
import urllib.parse
import urllib.request

AD = os.path.dirname(os.path.abspath(__file__))
DB = os.path.expanduser("~/.claude-mem/claude-mem.db")
tohum, n = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 40
rnd = random.Random(tohum)
c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
satir = c.execute("SELECT id,title,narrative FROM observations WHERE project='omer-skills' AND length(narrative)>300 AND id<(SELECT max(id) FROM observations)-5").fetchall()
SEC = [("baslik", 3), ("anlati", 4)]


def sozcuk(s):
    return list(dict.fromkeys(w for w in re.findall(r"[^\W\d_]{5,}", (s or "").lower())))


sorular = []
for i, b, a in rnd.sample(satir, n):
    wb, wa = sozcuk(b), [w for w in sozcuk(a) if w not in sozcuk(b)]
    if len(wb) >= 3:
        sorular.append((i, "baslik", " ".join(rnd.sample(wb, 3))))
    if len(wa) >= 4:
        sorular.append((i, "anlati", " ".join(rnd.sample(wa, 4))))


def worker(q):
    t = time.time()
    try:
        r = json.loads(urllib.request.urlopen("http://127.0.0.1:37777/api/search?" + urllib.parse.urlencode({"query": q, "limit": 5}), timeout=20).read().decode())
        m, h = r["content"][0]["text"], 0
    except Exception as ex:  # noqa: BLE001
        m, h = "", 1
    return [int(x) for x in re.findall(r"#(\d+) ", m)], len(m), time.time() - t, h


def b_kol(q):
    t = time.time()
    p = subprocess.run([sys.executable, "-I", "-S", os.path.join(AD, "mem2.py"), q], capture_output=True, text=True, encoding="utf-8", creationflags=0x08000000)
    return [int(x) for x in re.findall(r"^#(\d+) ", p.stdout, re.M)], len(p.stdout), time.time() - t, int(p.returncode != 0)


sys.path.insert(0, AD)
import mem2  # noqa: E402

EK = {}
for k in range(0, len(sorular), 10):
    ps = sorular[k:k + 10]
    EK.update(zip([q for _, _, q in ps], mem2.genislet([q for _, _, q in ps])))


def g_kol(q):
    t = time.time()
    ids = [r[0] for r in mem2.ara(q, 5, ek=EK.get(q, ()))]
    return ids, len(mem2.bicim(mem2.ara(q, 5, ek=EK.get(q, ())))), time.time() - t, 0


S = {"A": [], "B": [], "G": []}
for i, tur, q in sorular:
    for kol, f in (("A", worker), ("B", b_kol), ("G", g_kol)):
        ids, ch, s, h = f(q)
        S[kol].append({"tur": tur, "isabet": int(i in ids[:5]), "tok": ch // 4, "s": s, "hata": h})


def ozet(L):
    o = {"n": len(L), "isabet": round(sum(x["isabet"] for x in L) / len(L), 3), "tok": round(sum(x["tok"] for x in L) / len(L)),
         "s_ort": round(sum(x["s"] for x in L) / len(L), 3), "s_max": round(max(x["s"] for x in L), 3), "hata": sum(x["hata"] for x in L)}
    for t in ("baslik", "anlati"):
        K = [x for x in L if x["tur"] == t]
        o["isabet_" + t] = round(sum(x["isabet"] for x in K) / max(1, len(K)), 3)
    return o


R = {"tohum": tohum, "A_worker": ozet(S["A"]), "B_mem2": ozet(S["B"]), "G_mem2_genis": ozet(S["G"])}
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open(os.path.join(AD, "mem_ab_%d.json" % tohum), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
