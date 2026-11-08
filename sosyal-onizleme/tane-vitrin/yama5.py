import sys
p=sys.argv[1];t=open(p,encoding='utf-8').read()
R=[
("const floorMat=new THREE.MeshStandardMaterial({color:0x100b08,roughness:.85,roughnessMap:TAS.Rg,normalMap:TAS.N,normalScale:new THREE.Vector2(.25,.25),metalness:0,envMap:ENV,envMapIntensity:.35});",
 "const floorMat=new THREE.MeshStandardMaterial({color:0x0e0a08,roughness:.92,metalness:0,envMap:ENV,envMapIntensity:.06});"),
("normalScale:new THREE.Vector2(o.ns,o.ns),clearcoat:o.clear,clearcoatRoughness:.28,envMap:ENV,envMapIntensity:1});",
 "normalScale:new THREE.Vector2(o.ns,o.ns),clearcoat:o.clear,clearcoatRoughness:.4,envMap:ENV,envMapIntensity:o.ei});"),
("metal:.0,rough:.6,clear:.2,ns:.35,","metal:.0,rough:.6,clear:.08,ns:.12,ei:.28,"),
("metal:1,rough:.3,clear:.0,ns:.55,","metal:1,rough:.3,clear:.0,ns:.3,ei:.9,"),
("metalness:1,roughness:1,clearcoat:.15,clearcoatRoughness:.6,envMap:ENV}));label.position.y",
 "metalness:1,roughness:1,clearcoat:.1,clearcoatRoughness:.6,envMap:ENV,envMapIntensity:.7}));label.position.y"),
("new THREE.MeshStandardMaterial({color:0x2b2b2b,roughness:.4,metalness:.2})","new THREE.MeshStandardMaterial({color:0x1a1512,roughness:.5,metalness:.1,envMapIntensity:.3})"),
("let dx=(xr-xl)*2.2,dy=(yd-yu)*2.2","let dx=(xr-xl)*1.1,dy=(yd-yu)*1.1"),
]
for a,b in R:
    if a not in t: print('YOK:',a[:60]); continue
    t=t.replace(a,b)
open(p,'w',encoding='utf-8').write(t);print('tamam')
