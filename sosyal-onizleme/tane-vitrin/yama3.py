import sys
p=sys.argv[1]
t=open(p,encoding='utf-8').read()
R=[
("const z=new THREE.Mesh(new THREE.BoxGeometry(o.w*0.94,0.03,0.025)","const z=new THREE.Mesh(new THREE.BoxGeometry(o.w*0.78,0.022,0.012)"),
("const mesh=new THREE.Mesh(g,mat);mesh.castShadow=true;mesh.receiveShadow=true;","const mesh=new THREE.Mesh(g,mat);mesh.castShadow=true;mesh.receiveShadow=false;"),
("label.position.y=o.ly;label.receiveShadow=true;","label.position.y=o.ly;label.receiveShadow=false;"),
(".hesap input,.hesap select{",".hesap input,.hesap select{box-sizing:border-box;"),
("cx:1.8,cy:m?2.2:1.8,cz:m?9.6:7.8,lx:m?0.4:1.8,ly:m?0.4:-0.4,orbit:.5,pour:0}","cx:1.8,cy:m?2.2:1.8,cz:m?9.6:7.8,lx:m?0.4:1.8,ly:m?0.4:-0.4,orbit:0,pour:0}"),
]
for a,b in R:
    if a not in t: print('YOK:',a[:60]); continue
    t=t.replace(a,b)
open(p,'w',encoding='utf-8').write(t);print('tamam')
