import sys,json,random
sys.path.insert(0,'tools')
import usta_kart as u
U=list(u.oku_usta().values())
yeni=U[300:]
cand=[c for c in yeni if 'paket' not in c['ad']]
print(len(yeni),len(cand))
random.seed(12)
o=random.sample(cand,min(40,len(cand)))
K={k['ad']:k for k in u.kartlar()}
out=[]
for i,c in enumerate(o):
    out.append(f"[{i}] {c['ad']}\nKAYNAK: {u.kaynak(K[c['ad']],lim=6000)}\nKART: {json.dumps({x:c[x] for x in u.ALANLAR},ensure_ascii=False)}\n")
open('.kos/kopru/usta-haiku/hakem12.txt','w',encoding='utf-8').write("\n".join(out))
