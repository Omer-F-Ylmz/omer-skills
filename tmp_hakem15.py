import sys, json, random
sys.path.insert(0, "tools")
import usta_kart as u
C = [json.loads(l) for l in open(".kos/kopru/usta-haiku/ileri/tur15.jsonl", encoding="utf-8") if l.strip()]
random.seed(15)
o = random.sample(C, 40)
K = {k["ad"]: k for k in u.kartlar()}
par = "\n".join(f"[{i}] {c['ad']} | kaynak: {u.kaynak(K[c['ad']], 4000)}\n kart: {json.dumps({x: c[x] for x in u.ALANLAR}, ensure_ascii=False)}" for i, c in enumerate(o))
ist = ("Hakemsin. Her kart için: kaynak metne göre DOĞRU (uydurma/yanlış yok) ve YARARLI (somut, genel geçer değil) mi? "
       'YALNIZ JSON dizisi: [{"i":0,"dogru":true,"yararli":true,"neden":"≤10 kelime"}...]\n\n' + par)
d = ".kos/kopru/usta-haiku/ileri/"
open(d + "hakem15-istem.txt", "w", encoding="utf-8").write(ist)
json.dump([c["ad"] for c in o], open(d + "hakem15-adlar.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(ist))
