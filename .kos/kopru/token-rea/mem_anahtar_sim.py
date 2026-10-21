"""d19 yol (a) benzetimi: gözlem yazılırken başlığa 'TR anahtarlar · EN anahtarlar' satırı eklense paraphrase isabeti ne olurdu.
Gerçek korpusta ölçülemez (yalnız yeni gözlemlere uygulanır) -> kontrollü alt küme: N kayıt (yarı TR yarı EN), hepsine havuzla anahtar satırı, bellek içi FTS5;
B = anahtarsız · K = anahtar sütunlu; iki kol AYNI alt kümede, aynı sorular. Mutlak sayı küçük korpus yüzünden şişkin, yalnız fark okunur.
Kullanım: python -I mem_anahtar_sim.py <tohum> [N=600] [soru=30]   (havuz çağrısı ≈ N/25 + 2*soru/10; yanıtlar mem_sim_onbellek.json'da)"""
import json
import os
import random
import re
import sqlite3
import sys

AD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AD, "..", "..", "..", "tools"))
import ucretsiz_havuz as H  # noqa: E402

DB = os.path.expanduser("~/.claude-mem/claude-mem.db")
OB = os.path.join(AD, "mem_sim_onbellek.json")
tohum = int(sys.argv[1])
N = int(sys.argv[2]) if len(sys.argv) > 2 else 600
SQ = int(sys.argv[3]) if len(sys.argv) > 3 else 30
rnd = random.Random(tohum)
TRK = re.compile(r"[çğıöşüÇĞİÖŞÜ]")
try:
    ob = json.load(open(OB, encoding="utf-8"))
except (OSError, ValueError):
    ob = {}


def kes(w):
    return w[:5]


def sozcukler(s):
    return [w for w in re.findall(r"[^\W\d_]+", (s or "").lower()) if len(w) > 3]


def cagir(anahtar, ist, adet):
    if anahtar in ob:
        return ob[anahtar]
    y, _, _ = H.cagir("ozet", ist, max_tokens=3000, haiku_tavan=0, etiket="mem-sim",
                      dogrula=lambda m: None if len([x for x in m.strip().splitlines() if x.strip()]) == adet else "satır sayısı")
    ob[anahtar] = [x.strip() for x in y.strip().splitlines() if x.strip()] if y else None
    json.dump(ob, open(OB, "w", encoding="utf-8"), ensure_ascii=False)
    return ob[anahtar]


c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
satir = c.execute("SELECT id,title,subtitle,narrative,facts,concepts FROM observations WHERE project='omer-skills' AND length(narrative)>300 AND id<(SELECT max(id) FROM observations)-5").fetchall()
tr = [r for r in satir if TRK.search(" ".join(x or "" for x in r[1:3]))]
en = [r for r in satir if r not in tr]
alt = rnd.sample(tr, N // 2) + rnd.sample(en, N // 2)
kw = {}
for k in range(0, len(alt), 25):
    p = alt[k:k + 25]
    ist = ("Aşağıdaki numaralı satırlar birer iş günlüğü kaydı. Her kayıt için aranırken kullanılacak anahtar sözcükleri yaz: önce 6 Türkçe, sonra 6 İngilizce, "
           "kaydın konusunu ve eylemini anlatan, birbirinin karşılığı olacak biçimde. Biçim (tek satır, numarasız, aynı sırayla): `TR: s1 s2 s3 s4 s5 s6 | EN: s1 s2 s3 s4 s5 s6`.\n"
           + "\n".join(f"{j + 1}. {(r[1] or '')[:90]} — {(r[3] or '')[:200]}".replace("\n", " ") for j, r in enumerate(p)))
    y = cagir("kw:%d:%d:%d" % (tohum, N, k), ist, len(p))
    for r, l in zip(p, y or []):
        kw[r[0]] = " ".join(kes(w) for w in sozcukler(l))

y = sqlite3.connect(":memory:")
y.execute("CREATE VIRTUAL TABLE a USING fts5(title,subtitle,narrative,facts,concepts,kw)")
for r in alt:
    y.execute("INSERT INTO a(rowid,title,subtitle,narrative,facts,concepts,kw) VALUES(?,?,?,?,?,?,?)", (*r, kw.get(r[0], "")))


def ara(soru, anahtarli):
    w = list(dict.fromkeys(x for x in re.findall(r"\w+", soru.lower()) if len(x) > 2))
    q = "{title subtitle narrative facts concepts} : (%s)" % " OR ".join('"%s"' % x for x in w)
    if anahtarli:
        q += " OR {kw} : (%s)" % " OR ".join('"%s"' % kes(x) for x in w if len(x) > 3)
    return [x[0] for x in y.execute("SELECT rowid FROM a WHERE a MATCH ? ORDER BY bm25(a,5,2,5,3,3,3) LIMIT 5", (q,))]


R = {"tohum": tohum, "N": N, "kw_kapsam": round(len(kw) / len(alt), 2)}
for ad, grup, hedef in (("TR->EN", [r for r in alt if r in en], "Türkçe"), ("EN->TR", [r for r in alt if r in tr], "İngilizce")):
    sec = rnd.sample(grup, SQ)
    B = K = n = 0
    for k in range(0, len(sec), 10):
        p = sec[k:k + 10]
        ist = ("Aşağıdaki numaralı satırlar birer iş günlüğü kaydı. Her biri için, geliştiricinin o kaydı geri bulmak için yazacağı KISA %s soruyu yaz "
               "(en çok 12 sözcük): kayıt başlığındaki sözcükleri birebir kopyalama, eş anlamlı/dolaylı anlat, dosya adı uydurma. "
               "Çıktı yalnız sorular, aynı sırayla, numarasız.\n" % hedef
               + "\n".join(f"{j + 1}. {(r[1] or '')[:90]} — {(r[3] or '')[:260]}".replace("\n", " ") for j, r in enumerate(p)))
        sor = cagir("q:%d:%s:%d" % (tohum, ad, k), ist, len(p))
        for r, q in zip(p, sor or []):
            n += 1
            B += r[0] in ara(q, False)
            K += r[0] in ara(q, True)
    R[ad] = {"n": n, "B": round(B / max(1, n), 3), "K": round(K / max(1, n), 3)}
print(json.dumps(R, indent=1))
json.dump(R, open(os.path.join(AD, "mem_anahtar_sim_%d.json" % tohum), "w", encoding="utf-8"), indent=1)
