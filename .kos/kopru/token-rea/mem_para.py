"""claude-mem anlamsal (paraphrase) A/B: worker /api/search (A) vs mem2 (B) vs mem2→worker yedek (C).
Soru metnini havuz yeniden ifade eder (gözlem başlığındaki sözcükleri kopyalamadan); anahtar = gözlem id (ilk 5).
Kullanım: python -I mem_para.py <tohum> [n=60]  — Claude çağrısı yok (yalnız ücretsiz havuz). Soru içeriği stdout'a basılmaz."""
import json
import os
import random
import re
import sqlite3
import sys

AD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AD)
sys.path.insert(0, os.path.join(AD, "..", "..", "..", "tools"))
import mem2  # noqa: E402
import ucretsiz_havuz as H  # noqa: E402
import urllib.parse, urllib.request, time  # noqa: E401,E402

tohum, n = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 60
rnd = random.Random(tohum)
c = sqlite3.connect("file:" + mem2.DB + "?mode=ro", uri=True)
son = [r[0] for r in c.execute("SELECT id FROM observations WHERE project='omer-skills' ORDER BY id DESC LIMIT 15")]
pencere = son[7:15]  # 8.–15. en yeni: 15→7 geçişinde bağlamdan düşen gözlemler
genel = c.execute("SELECT id,title,narrative FROM observations WHERE project='omer-skills' AND length(narrative)>300 AND id<?", (min(son),)).fetchall()
secim = [(i, b, a, "genel") for i, b, a in rnd.sample(genel, n)]
for i in pencere:
    r = c.execute("SELECT id,title,narrative FROM observations WHERE id=?", (i,)).fetchone()
    if len(r[2] or "") > 100:
        secim.append((*r, "pencere"))


def yeniden(parca):
    ist = ("Aşağıdaki numaralı satırlar birer iş günlüğü kaydı. Her biri için, geliştiricinin o kaydı geri bulmak için yazacağı KISA Türkçe soruyu yaz "
           "(en çok 12 sözcük): kayıt başlığındaki sözcükleri birebir kopyalama, eş anlamlı/dolaylı anlat, dosya adı uydurma. "
           "Çıktı yalnız sorular, aynı sırayla, numarasız.\n" + "\n".join(f"{k + 1}. {(b or '')[:90]} — {(a or '')[:260]}".replace("\n", " ") for k, (_, b, a, _) in enumerate(parca)))
    y, kaynak, _ = H.cagir("ozet", ist, max_tokens=1200, haiku_tavan=0, etiket="mem-para",
                           dogrula=lambda m: None if len([l for l in m.strip().splitlines() if l.strip()]) == len(parca) else "satır sayısı")
    return ([l.strip().lstrip("0123456789.) ") for l in y.strip().splitlines() if l.strip()], kaynak) if y else (None, None)


def worker(q):
    t = time.time()
    try:
        r = json.loads(urllib.request.urlopen("http://127.0.0.1:37777/api/search?" + urllib.parse.urlencode({"query": q, "limit": 5}), timeout=20).read().decode())
        m = r["content"][0]["text"]
    except Exception:  # noqa: BLE001
        m = ""
    return [int(x) for x in re.findall(r"#(\d+) ", m)][:5], len(m) // 4, time.time() - t


S, kaynaklar, atlanan = [], set(), 0
for k in range(0, len(secim), 10):
    parca = secim[k:k + 10]
    sor, kay = yeniden(parca)
    if not sor:
        atlanan += len(parca)
        continue
    kaynaklar.add(kay)
    ekler = mem2.genislet(sor)
    for (i, _, _, grup), q, ek in zip(parca, sor, ekler):
        t = time.time()
        b = [r[0] for r in mem2.ara(q, 5)]
        sb = time.time() - t
        g = [r[0] for r in mem2.ara2(q, 5, ek=ek)]
        a, ta, sa = worker(q)
        if os.environ.get("MEM_PARA_DEBUG"):  # tanı: soru + worker/mem2 kimlikleri (soru metni yalnız dosyaya)
            open(os.path.join(AD, "_para_debug.jsonl"), "a", encoding="utf-8").write(json.dumps({"i": i, "q": q, "a": a, "b": b}, ensure_ascii=False) + "\n")
        S.append({"grup": grup, "A": int(i in a), "B": int(i in b), "C": int(i in (b if b else a)), "G": int(i in g), "U": int(i in a or i in b),
                  "tokA": ta, "tokB": len(mem2.bicim(mem2.ara(q, 5))) // 4, "sA": sa, "sB": sb, "bos_B": int(not b)})


def ozet(L):
    m = max(1, len(L))
    return {"n": len(L), **{x: round(sum(s[x] for s in L) / m, 3) for x in ("A", "B", "G", "C", "U", "bos_B")},
            "tokA": round(sum(s["tokA"] for s in L) / m), "tokB": round(sum(s["tokB"] for s in L) / m),
            "sA": round(sum(s["sA"] for s in L) / m, 3), "sB": round(sum(s["sB"] for s in L) / m, 3)}


R = {"tohum": tohum, "kaynak": sorted(kaynaklar), "atlanan": atlanan, "hepsi": ozet(S),
     "genel": ozet([s for s in S if s["grup"] == "genel"]), "pencere_8_15": ozet([s for s in S if s["grup"] == "pencere"])}
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open(os.path.join(AD, "mem_para_%d.json" % tohum), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
