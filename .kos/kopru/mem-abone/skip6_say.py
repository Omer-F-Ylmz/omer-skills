import json,io
R=[json.loads(l) for l in io.open('.kos/kopru/mem-abone/deney5.jsonl',encoding='utf-8')]
sk=lambda s:s.lstrip().startswith('<skip_summary')
ac=lambda s:s.upper().startswith('ACCEPT')
for k in 'AB':
    n=len(R);S=[r for r in R if sk(r[k])];N=[r for r in R if not sk(r[k])]
    print(k,'skip',len(S),'obs',len(N),'| hakem ACCEPT skip',sum(ac(r['j1'+k]) for r in S),'obs',sum(ac(r['j1'+k]) for r in N))
print('A/B skip uyumu',sum(sk(r['A'])==sk(r['B']) for r in R),'canli skip',sum(sk(r['live']) for r in R))
