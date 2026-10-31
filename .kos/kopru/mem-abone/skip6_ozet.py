import json,io
R=[json.loads(l) for l in io.open('.kos/kopru/mem-abone/deney6.jsonl',encoding='utf-8')]
sk=lambda s:s.lstrip().startswith('<skip_summary')
ac=lambda s:s.upper().startswith('ACCEPT')
dur=[r['sj'].upper().startswith('DURABLE') for r in R]
print('kor hakem: DURABLE',sum(dur),'NOISE',len(R)-sum(dur))
for k in ('A','B','C','live'):
    S=[sk(r[k]) for r in R]
    dogru=sum(s==(not d) for s,d in zip(S,dur))            # skip<->NOISE uyumu
    yanlis_skip=sum(s and d for s,d in zip(S,dur)); kacan_gur=sum((not s) and (not d) for s,d in zip(S,dur))
    print(k,'skip',sum(S),'| skip karari dogru',dogru,'/24 | yanlis skip(DURABLE atlandi)',yanlis_skip,'| gereksiz obs(NOISE yazildi)',kacan_gur)
N=[r for r in R if not sk(r['C'])]
print('C obs',len(N),'hakem ACCEPT',sum(ac(r['j1C']) for r in N))
