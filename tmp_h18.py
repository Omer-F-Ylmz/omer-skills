import sys,json,random
sys.path.insert(0,'tools'); sys.argv=['x','say']
import usta_kart as u
U=u.oku_usta(); K={k['ad']:k for k in u.kartlar()}
ret=["supabase-postgres-best-practices","sentry-instrument-logging","setup-gbrain","ship","n8n-expression-syntax","spec","mukul975-zero-trust-paket","davila7-productivity-paket"]
rest=[a for a in U if a not in ret and a in K]
random.seed(18); ad=ret+random.sample(rest,32)
out=u.KOK/'.kos/kopru/usta-haiku/ileri/h18'
G=[]
for i in range(4):
    s=[]
    for a in ad[i::4]:
        tam=u.kaynak(K[a],10**6); par=[tam[x:x+6000] for x in range(0,len(tam),6000)] or ['']
        s.append(f"=== KART {a}\n"+json.dumps({x:U[a][x] for x in u.ALANLAR},ensure_ascii=False)+"\n--- KAYNAK (tam)\n"+"\n".join(par))
    p=out/f'g{i}.txt'; p.write_text("\n\n".join(s),encoding='utf-8'); G.append((str(p),len(ad[i::4]),sum(len(x) for x in s)))
json.dump(ad,open(out/'adlar.json','w'))
print(G)
