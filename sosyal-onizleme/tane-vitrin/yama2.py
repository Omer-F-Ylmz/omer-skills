import sys
p=sys.argv[1]
t=open(p,encoding='utf-8').read()
R=[
("key.shadow.bias=-0.0004;","key.shadow.bias=-0.0012;key.shadow.normalBias=0.03;"),
("new THREE.MeshStandardMaterial({color:0x4a2b18,roughness:.9}),AYAR.maxGround)","new THREE.MeshStandardMaterial({color:0x2a170c,roughness:.95}),AYAR.maxGround)"),
("function cizgi(g,x1,y,x2,col,w){","function aralikli(g,s,cx,y,sp){const ws=[...s].map(c=>g.measureText(c).width);const tw=ws.reduce((a,b)=>a+b,0)+sp*(ws.length-1);let x=cx-tw/2;const al=g.textAlign;g.textAlign=\"left\";[...s].forEach((c,i)=>{g.fillText(c,x,y);x+=ws[i]+sp});g.textAlign=al}\nfunction cizgi(g,x1,y,x2,col,w){"),
("g.font=\"500 132px 'Bodoni Moda', Didot, serif\";g.fillText(\"Kolombiya\",W/2,380);","g.font=\"500 104px 'Bodoni Moda', Didot, serif\";aralikli(g,\"KOLOMBİYA\",W/2,370,10);"),
("g.font=\"500 176px 'Bodoni Moda', serif\";g.fillText(\"Filtre\",W/2,380);","g.font=\"500 150px 'Bodoni Moda', serif\";aralikli(g,\"FİLTRE\",W/2,370,14);"),
]
for a,b in R:
    if a not in t: print('YOK:',a[:60]); continue
    t=t.replace(a,b)
open(p,'w',encoding='utf-8').write(t);print('tamam')
