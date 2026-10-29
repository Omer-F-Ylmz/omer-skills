import glob,re,os,json,collections,csv
H=os.path.expanduser('~')
def n(s): return re.sub(r'[^a-z0-9]','',s.lower())
# rows
rows=[];S=set()
for f in sorted(glob.glob('.kos/kopru/ogren/yeni1-cikti/env*.tsv')):
    for l in open(f,encoding='utf-8'):
        p=l.rstrip('\n').split('\t')
        if len(p)<3: continue
        p+=['']*(5-len(p)); key=(p[1].lower().replace(' (?)','').strip(),p[2])
        if key in S: continue
        S.add(key); rows.append(p[:5])
N=len(rows)
# installed names: name -> evidence
inst={}
def add(name,ev):
    k=n(name)
    if len(k)>=3: inst.setdefault(k,ev)
for d,ev in [(H+'/.claude/skills','~/.claude/skills/'),(H+'/.claude/agents','~/.claude/agents/'),('araclar','araclar/'),('C:/AI/indirilen','C:/AI/indirilen/')]:
    if os.path.isdir(d):
        for x in os.listdir(d): add(x.replace('.md',''),ev+x)
for p in glob.glob(H+'/.claude/plugins/cache/*/*'):
    add(os.path.basename(p),p.replace(H,'~'))
    for q in glob.glob(p+'/*'): add(os.path.basename(q),q.replace(H,'~'))
for p in glob.glob(H+'/.claude/plugins/marketplaces/*'): add(os.path.basename(p),p.replace(H,'~'))
for f in glob.glob('.kos/kopru/rapor/_inv_*.txt'):
    for l in open(f,encoding='utf-8',errors='ignore'):
        w=l.split()
        if w and not w[0].startswith('-'): add(w[0],os.path.basename(f))
for l in open('docs/envanter/envanter.tsv',encoding='utf-8',errors='ignore'):
    p=l.split('\t')
    if len(p)>3 and p[2] in('CC','ikisi','claude.ai'): add(p[0],'envanter.tsv:'+p[2]+':'+p[1])
try:
    j=json.load(open(H+'/.claude.json',encoding='utf-8'))
    for k in j.get('mcpServers',{}): add(k,'~/.claude.json mcp')
    for pr in j.get('projects',{}).values():
        for k in pr.get('mcpServers',{}): add(k,'~/.claude.json mcp(proje)')
except Exception as e: print('mcp',e)
# url corpus
urls=''
def rd(f):
    try: return open(f,encoding='utf-8',errors='ignore').read().lower()
    except: return ''
for f in [H+'/.claude/plugins/installed_plugins.json',H+'/.claude/plugins/known_marketplaces.json']: urls+=rd(f)
for pat in ['araclar/*/.git/config','araclar/*/*/.git/config','C:/AI/indirilen/*/.git/config',H+'/.claude/plugins/marketplaces/*/.git/config',H+'/.claude/skills/*/.git/config']:
    for f in glob.glob(pat): urls+=rd(f)
for l in open('docs/kurulumlar/kayit.jsonl',encoding='utf-8',errors='ignore'):
    if '"KUR"' in l: urls+=l.lower()
cat=set(n(l.split('\t')[0]) for l in open('docs/katalog/yetenek.tsv',encoding='utf-8',errors='ignore'))
print('inst',len(inst),'urlbyte',len(urls),'cat',len(cat))
# dedupe
def slug(u):
    m=re.search(r'github\.com/([\w.-]+/[\w.-]+)',u.lower().replace(' (?)',''))
    return m.group(1).removesuffix('.git') if m else None
G={}
for r in rows:
    k=slug(r[3]) or n(r[1])
    G.setdefault(k,[]).append(r)
out=[];cnt=collections.Counter()
for k,rs in G.items():
    r=rs[0]; sl=slug(r[3]); nm=n(r[1]); last=n(sl.split('/')[1]) if sl else ''
    sh=None
    if sl and sl in urls: sh='repo-url:'+sl
    if not sh:
        for c in (nm,last):
            if len(c)>=4 and c in inst: sh='ad=%s'%inst[c];break
    if sh: cl='KURULU-KANIT'; ev=sh
    else:
        wk=None
        for c in (nm,last):
            if len(c)>=7:
                hit=[v for kk,v in inst.items() if min(len(c),len(kk))>=7 and (c in kk or kk in c) and min(len(c),len(kk))/max(len(c),len(kk))>=0.6]
                if hit: wk='benzer:'+hit[0];break
                if c in cat: wk='yalniz-katalog';break
        if wk: cl='BELİRSİZ'; ev=wk
        else: cl='KURULACAK'; ev=''
    cnt[cl]+=1
    out.append([cl,r[1],r[2],r[3],ev,str(len(rs)),r[0],r[4]])
print(N,'tekil',len(G),dict(cnt))
os.makedirs('.kos/kopru/rapor',exist_ok=True)
with open('.kos/kopru/rapor/video-yeni-1-kurulacaklar-tekil.tsv','w',encoding='utf-8',newline='') as f:
    f.write('sinif\tad\ttur\turl/komut\tkanit\tkopya\tkod\tne isi yarar\n')
    for o in sorted(out,key=lambda x:x[0]): f.write('\t'.join(c.replace('\t',' ') for c in o)+'\n')
