import csv,re,json
from collections import defaultdict
from urllib.parse import urlparse
r=list(csv.reader(open('.kos/kopru/kacan-karar.tsv',encoding='utf-8',errors='replace'),delimiter='\t'))[1:]
d=defaultdict(lambda:{'v':set(),'raw':set()})
def norm(t):
    t=t.strip()
    if t.startswith('http'):
        u=urlparse(t);h=u.netloc.lower().removeprefix('www.')
        p=[x for x in u.path.split('/') if x]
        if h=='github.com' and len(p)>=2: return 'gh:'+p[0].lower()+'/'+p[1].lower()
        if h=='github.com' and len(p)==1: return 'ghuser:'+p[0].lower()
        if h in('npmjs.com',) and len(p)>=2: return 'npm:'+'/'.join(p[1:3] if p[1].startswith('@') else p[1:2])
        if h=='marketplace.visualstudio.com': return 'vsx:'+u.query
        return 'site:'+h
    return 'name:'+t.lower()
for x in r:
    if len(x)>4 and x[4]=='aday':
        k=norm(x[3]);d[k]['v'].add(x[1]);d[k]['raw'].add(x[3])
out=[{'k':k,'v':sorted(v['v']),'n':len(v['raw'])} for k,v in sorted(d.items())]
json.dump(out,open('.kos/kopru/ara/vk1_norm.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(out))
from collections import Counter
print(Counter(o['k'].split(':')[0] for o in out))
print([o['k'] for o in out if o['k'].startswith('site:')][:120])
