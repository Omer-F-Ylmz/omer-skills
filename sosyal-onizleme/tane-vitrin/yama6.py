import sys
p=sys.argv[1];t=open(p,encoding='utf-8').read()
a="let s=seed||1;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;"
b="let s=(seed||1)*2654435761>>>0;const rnd=()=>{s=s+0x6D2B79F5|0;let q=Math.imul(s^s>>>15,1|s);q=q+Math.imul(q^q>>>7,61|q)^q;return((q^q>>>14)>>>0)/4294967296};"
assert a in t;t=t.replace(a,b)
open(p,'w',encoding='utf-8').write(t);print('tamam')
