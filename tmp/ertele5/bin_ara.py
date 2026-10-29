import sys,re,os
sys.stdout.reconfigure(encoding="utf-8")
p=sys.argv[1]; pats=sys.argv[2:]
b=open(p,'rb').read()
for pat in pats:
    seen=set()
    for m in re.finditer(pat.encode(),b):
        s=b[max(0,m.start()-250):m.end()+350]
        t=s.decode('utf-8','replace').replace('\n',' ')
        k=t[200:320]
        if k in seen: continue
        seen.add(k); print('==',pat,'@',m.start()); print(t[:600])
        if len(seen)>=4: break
