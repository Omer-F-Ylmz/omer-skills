import json,re
c=json.load(open('.kos/kopru/ara/vk1_norm.json',encoding='utf-8'))
# alt alan adlarini kayıtlı alan adina birlestir
inv=[l.strip() for l in open('.kos/kopru/ara/vk1_env.txt',encoding='utf-8') if l.strip()]
bare={}
for e in inv:
    b=e.split(':',1)[-1] if re.match(r'^(npm|pip|uv|app|mcp|bin|gh-ext):',e) else e
    bare.setdefault(re.sub(r'[^a-z0-9]','',b.split('@')[0].split('/')[-1]),[]).append(e)
def dom(h):
    p=h.split('.');return '.'.join(p[-2:]) if len(p)>2 else h
m={}
for o in c:
    k=o['k'];t,v=k.split(':',1)
    if t=='site': v=dom(v); k='site:'+v
    m.setdefault(k,{'k':k,'v':set(),'n':0});m[k]['v']|=set(o['v']);m[k]['n']+=o['n']
rows=[]
for k,o in m.items():
    t,v=k.split(':',1)
    tok=v.split('/')[-1] if t!='site' else v.split('.')[0]
    if t=='vsx': tok=v.split('.')[-1]
    s=re.sub(r'[^a-z0-9]','',tok.lower())
    hit=[]
    if len(s)>=4:
        for b,es in bare.items():
            if b==s or (len(s)>=6 and (s in b or b in s and len(b)>=6)): hit+=es
    rows.append({'k':k,'v':sorted(o['v']),'nv':len(o['v']),'hit':hit[:4]})
rows.sort(key=lambda r:-r['nv'])
json.dump(rows,open('.kos/kopru/ara/vk1_rows.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(rows),sum(1 for r in rows if r['hit']))
for r in rows[:12]: print(r['k'],r['nv'],r['hit'])
