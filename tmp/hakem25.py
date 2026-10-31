import json, sys, random
sys.path.insert(0, 'tools')
import usta_kart as u
K = {k["ad"]: k for k in u.kartlar()}
U = u.oku_usta()
eski = set()
for d in ('hakem21','hakem22','hakem23','hakem24'):
    try:
        j=json.load(open(f'tmp/{d}/adlar.json',encoding='utf-8')); eski |= set(j.get('eski',[])+j.get('ret',[]))|set(j.get('yeni',[]))
    except Exception as e: print(d, e)
ret = ['ub-mode','n8n-workflow-patterns']
yetersiz = [a for a in U if a in K and len(u.kaynak(K[a],60000))<400]
print('kaynak-yetersiz', len(yetersiz), yetersiz[:10])
rest = sorted(a for a in U if a in K and a not in eski and a not in ret and a not in yetersiz)
random.seed(25)
yeni = random.sample(rest, 40)
json.dump({"ret":ret,"yeni":yeni,"yetersiz":yetersiz}, open('tmp/hakem25/adlar.json','w',encoding='utf-8'), ensure_ascii=False)
bas = "Hakemsin. Her kart icin: kaynak metne gore DOGRU (kaynakta olmayan iddia, uydurma sayi/olcu, dusurulmus kosul yok) ve YARARLI mi? YALNIZ JSON dizisi: [{\"i\":0,\"dogru\":true,\"yararli\":true,\"neden\":\"<=10 kelime\"}]\n\n"
tum = ret + yeni
for g in range(3):
    p = bas
    for j, a in enumerate(tum[g*14:(g+1)*14]):
        c = U[a]
        p += f"=== [{j}] {a}\nKAYNAK(TAM): {u.kaynak(K[a], 60000)}\nKART: {json.dumps({x: c[x] for x in u.ALANLAR}, ensure_ascii=False)}\n\n"
    open(f'tmp/hakem25/f{g}.txt','w',encoding='utf-8').write(p); print(g,len(p))
