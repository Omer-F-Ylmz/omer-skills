import sys
p=sys.argv[1];t=open(p,encoding='utf-8').read()
R=[('color:0xc9a24e,metalness:1,roughness:.32,envMap:ENV,envMapIntensity:1','color:0x8f6a2c,metalness:1,roughness:.48,envMap:ENV,envMapIntensity:.45'),
('v.position.set(0,vy,(o.d/2)*puff(0,vy/(o.h/2),o.kind)+0.01)','v.position.set(0,vy,(o.d/2)*puff(0,vy/(o.h/2),o.kind)+0.03);v.rotation.x=Math.PI/2-(o.kind==="kraft"?0.5:0)')]
for a,b in R:
    assert a in t,a;t=t.replace(a,b,1)
open(p,'w',encoding='utf-8').write(t);print('tamam')
