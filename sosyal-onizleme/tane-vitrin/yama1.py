import sys
p=sys.argv[1]
t=open(p,encoding='utf-8').read()
R=[
("const AYAR={orbitBean:110,maxGround:900,camFov:28,pour:{rate:10}};","const AYAR={orbitBean:64,maxGround:700,camFov:28,pour:{rate:5}};"),
("const floorMat=new THREE.MeshStandardMaterial({color:0x1b120d,roughness:.85,metalness:0});","const floorMat=new THREE.MeshStandardMaterial({color:0x0b0705,roughness:.96,metalness:0});"),
("scene.add(new THREE.HemisphereLight(0xffe2c4,0x120c09,0.35));","scene.add(new THREE.HemisphereLight(0xffe2c4,0x120c09,0.22));"),
("const key=new THREE.SpotLight(0xffe9d2,2.4,30,0.55,0.6,1.2);","const key=new THREE.SpotLight(0xffe9d2,2.1,30,0.42,0.75,1.4);"),
('g.strokeStyle=Math.random()<.5?"rgba(255,255,255,.18)":"rgba(0,0,0,.18)";g.lineWidth=.6+Math.random()*1.8;','g.strokeStyle=Math.random()<.5?"rgba(255,255,255,.07)":"rgba(0,0,0,.07)";g.lineWidth=.4+Math.random()*1.2;'),
("for(let i=0;i<900;i++){const x=Math.random()*s,y=Math.random()*s,l=10+Math.random()*60","for(let i=0;i<1400;i++){const x=Math.random()*s,y=Math.random()*s,l=6+Math.random()*28"),
("  f*=1-ss(0.8,0.94,yn)*0.94;","  f*=1-ss(0.74,0.96,yn)*0.97;"),
("nz+=Math.sign(z)*wr(x,y)*(1-ss(.8,.94,yn))","nz+=Math.sign(z)*wr(x,y)*(1-ss(.74,.96,yn))"),
("bumpMap:crinkle,bumpScale:.0025,envMapIntensity:1});","bumpMap:crinkle,bumpScale:.0011,envMapIntensity:.85});"),
("const seal=new THREE.Mesh(new THREE.BoxGeometry(o.w,o.h*0.055,o.d*0.06)","const seal=new THREE.Mesh(new THREE.BoxGeometry(o.w*0.995,o.h*0.04,o.d*0.025)"),
("seal.position.y=o.h*0.475;","seal.position.y=o.h*0.48;"),
('const A=makeBag({kind:"bag",w:1.34,h:2.2,d:0.66,color:0x16110e,metal:.35,rough:.42,clear:.6,','const A=makeBag({kind:"bag",w:1.34,h:2.2,d:0.66,color:0x0d0a08,metal:.12,rough:.52,clear:.35,'),
("const B=makeBag({kind:\"pouch\",w:1.14,h:1.58,d:0.48,color:0xb5652f,metal:.82,rough:.3,clear:.4,","const B=makeBag({kind:\"pouch\",w:1.14,h:1.58,d:0.48,color:0xa65a2a,metal:.7,rough:.36,clear:.3,"),
("g.font=\"italic 400 150px 'Bodoni Moda', Didot, serif\";g.fillText(\"Kolombiya\",W/2,380);","g.font=\"500 132px 'Bodoni Moda', Didot, serif\";g.fillText(\"Kolombiya\",W/2,380);"),
("g.font=\"italic 400 190px 'Bodoni Moda', serif\";g.fillText(\"Filtre\",W/2,380);","g.font=\"500 176px 'Bodoni Moda', serif\";g.fillText(\"Filtre\",W/2,380);"),
("const ob=[];for(let i=0;i<AYAR.orbitBean;i++){ob.push({r:1.3+Math.random()*1.9,a:Math.random()*Math.PI*2,y:-1+Math.random()*2.6,","const ob=[];for(let i=0;i<AYAR.orbitBean;i++){ob.push({r:0.95+Math.random()*0.75,a:Math.random()*Math.PI*2,y:-0.9+Math.random()*2.4,"),
("{ax:m?-2.6:-3.4,ay:0,az:-1.6,ary:0.4,arz:0,bx:m?0.2:-1.2,by:m?1.2:0.75,bz:0.2,bry:0.2,brz:m?-1.6:-1.9,cx:-0.6,cy:m?1:0.4,cz:m?9:6.6,lx:m?0:-0.9,ly:m?0.2:-0.3,orbit:.15,pour:1},",
 "{ax:m?-2.6:-4.2,ay:0,az:-1.8,ary:0.4,arz:0,bx:m?-0.3:-2.1,by:m?1.2:0.75,bz:0.2,bry:0.2,brz:m?-1.6:-1.9,cx:-1.1,cy:m?1:0.4,cz:m?9:6.6,lx:m?-0.2:-1.3,ly:m?0.2:-0.3,orbit:0,pour:1},"),
("{ax:m?-2.6:-3.2,ay:0,az:-1.4,ary:0.4,arz:0,bx:m?0:1.5,","{ax:m?-2.6:-3.2,ay:0,az:-1.4,ary:0.4,arz:0,bx:m?0:1.6,"),
("const k=S.orbit;dum.position.set(S.ax+Math.cos(b.a)*b.r,","const k=S.orbit;dum.position.set(S.ax+Math.cos(b.a)*b.r*1.15,"),
("#urunler{flex-direction:column;justify-content:center}","#urunler{flex-direction:column;justify-content:center;padding-top:128px}"),
]
for a,b in R:
    if a not in t: print('YOK:',a[:60]); continue
    t=t.replace(a,b)
anchor="etiketA();etiketB();\n"
arka='''const arkaC=document.createElement("canvas");arkaC.width=1024;arkaC.height=1290;const arkaT=new THREE.CanvasTexture(arkaC);arkaT.encoding=THREE.sRGBEncoding;
(function(){const lg=A.label.geometry.clone();const lp=lg.attributes.position;for(let i=0;i<lp.count;i++)lp.setZ(i,-lp.getZ(i));lg.computeVertexNormals();
  const m=new THREE.Mesh(lg,new THREE.MeshStandardMaterial({map:arkaT,roughness:.6,metalness:.15,side:THREE.BackSide}));m.position.y=A.o.ly;A.grp.add(m)})();
function etiketArka(){const g=arkaC.getContext("2d"),W=arkaC.width,H=arkaC.height;g.save();g.translate(W,0);g.scale(-1,1);
  g.fillStyle="#0f0b09";g.fillRect(0,0,W,H);g.strokeStyle="rgba(217,178,90,.6)";g.lineWidth=2;g.strokeRect(40,40,W-80,H-80);
  g.fillStyle="#d9b25a";g.textAlign="left";g.font="500 30px Manrope, sans-serif";g.fillText("HİKÂYE",100,150);
  g.font="500 64px 'Bodoni Moda', serif";g.fillStyle="#efe6da";["Andların gölge","ağaçları altında","yetişen arabika."].forEach((s,i)=>g.fillText(s,100,250+i*76));
  g.font="400 30px Manrope, sans-serif";g.fillStyle="#b8aa99";["Elle toplanır, yıkanarak işlenir,","orta derecede kavrulur.","Gövdesi dolgun, asiditesi yumuşak."].forEach((s,i)=>g.fillText(s,100,560+i*48));
  g.strokeStyle="rgba(217,178,90,.4)";g.lineWidth=1;g.beginPath();g.moveTo(100,760);g.lineTo(W-100,760);g.stroke();
  g.font="500 26px Manrope, sans-serif";g.fillStyle="#d9b25a";[["RAKIM","1.600–1.900 m"],["İŞLEM","Yıkanmış"],["KAVRUM","Orta"],["NET","1 kg"]].forEach((r,i)=>{g.fillStyle="#b8aa99";g.fillText(r[0],100,840+i*62);g.fillStyle="#efe6da";g.fillText(r[1],420,840+i*62)});
  g.font="italic 400 40px 'Bodoni Moda', serif";g.fillStyle="#d9b25a";g.fillText("Açtıktan sonra serin ve kuru yerde, 4 hafta içinde.",100,1150);
  g.restore();arkaT.needsUpdate=true}
etiketArka();
'''
if anchor in t: t=t.replace(anchor,anchor+arka,1)
else: print('YOK anchor')
t=t.replace("ready.then(()=>{etiketA();etiketB()});","ready.then(()=>{etiketA();etiketB();etiketArka()});")
open(p,'w',encoding='utf-8').write(t);print('tamam')
