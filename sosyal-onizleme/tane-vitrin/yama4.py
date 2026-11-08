import sys,re
p=sys.argv[1]
t=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global t
    if a not in t: print('YOK:',a[:70]); return
    t=t.replace(a,b,cnt)

# 1) Ortam: koyu oda + parlak kartlar (fromScene)
i=t.index("(function env(){"); j=t.index("pm.dispose()})();",i)+len("pm.dispose()})();")
t=t[:i]+'''const ENV=(function(){const s=new THREE.Scene();s.background=new THREE.Color(0x050302);
  const kart=(w,h,c,k,pos,look)=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({color:new THREE.Color(c).multiplyScalar(k),side:THREE.DoubleSide,toneMapped:false}));m.position.set(...pos);m.lookAt(...look);s.add(m)};
  kart(4,2.4,0xfff1e0,5.5,[3,4,4],[0,0,0]);
  kart(1.2,4,0xffe2c0,3.2,[-4.5,1.5,2],[0,0,0]);
  kart(5,.5,0xffb27a,2.2,[0,6,-2],[0,0,0]);
  kart(1.2,3,0xcfd8ff,1.1,[4.5,1,-3],[0,0,0]);
  kart(8,1,0x3a2416,1.0,[0,-2.5,3],[0,0,0]);
  const pm=new THREE.PMREMGenerator(R);const e=pm.fromScene(s,0.02).texture;pm.dispose();return e})();
scene.environment=ENV;'''+t[j:]

# 2) Folyo normal + pürüzlülük haritaları (fbm yükseklik → Sobel normal)
foil='''function vnoise(W,H,oct,seed){const a=new Float32Array(W*H);let s=seed||1;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;
  for(let o=0;o<oct;o++){const f=4<<o,amp=1/(1<<o);const g=[];for(let y=0;y<=f;y++){g[y]=[];for(let x=0;x<=f;x++)g[y][x]=rnd()}
    for(let y=0;y<H;y++){const fy=y/H*f,y0=fy|0,ty=fy-y0,sy=ty*ty*(3-2*ty);for(let x=0;x<W;x++){const fx=x/W*f,x0=fx|0,tx=fx-x0,sx=tx*tx*(3-2*tx);
      const v=(g[y0][x0]*(1-sx)+g[y0][x0+1]*sx)*(1-sy)+(g[y0+1][x0]*(1-sx)+g[y0+1][x0+1]*sx)*sy;a[y*W+x]+=v*amp}}}return a}
function haritalar(W,H,ridge){const h=vnoise(W,H,6,7);
  for(let y=0;y<H;y++){const v=1-y/H;for(let x=0;x<W;x++){let k=0;
    if(ridge){if(v>0.93)k+=0.35*Math.sin(y*1.9)**2; if(v<0.035)k+=0.3*Math.sin(y*2.1)**2; const u=x/W; if(u<0.035||u>0.965)k+=0.25*Math.sin(x*2.3)**2;}
    h[y*W+x]+=k}}
  const n=document.createElement("canvas");n.width=W;n.height=H;const nc=n.getContext("2d");const nd=nc.createImageData(W,H);
  const r=document.createElement("canvas");r.width=W;r.height=H;const rc=r.getContext("2d");const rd=rc.createImageData(W,H);const lo=vnoise(W,H,3,3);
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=y*W+x,xl=h[y*W+(x-1+W)%W],xr=h[y*W+(x+1)%W],yu=h[((y-1+H)%H)*W+x],yd=h[((y+1)%H)*W+x];
    let dx=(xr-xl)*2.2,dy=(yd-yu)*2.2,l=Math.hypot(dx,dy,1);const o=i*4;nd.data[o]=(-dx/l*.5+.5)*255;nd.data[o+1]=(dy/l*.5+.5)*255;nd.data[o+2]=(1/l*.5+.5)*255;nd.data[o+3]=255;
    const rv=Math.min(1,Math.max(0,.55+(lo[i]-.9)*.35+(h[i]-1)*.12));rd.data[o]=0;rd.data[o+1]=rv*255;rd.data[o+2]=0;rd.data[o+3]=255}
  nc.putImageData(nd,0,0);rc.putImageData(rd,0,0);const N=new THREE.CanvasTexture(n),Rg=new THREE.CanvasTexture(r);
  [N,Rg].forEach(x=>{x.anisotropy=R.capabilities.getMaxAnisotropy()});return {N,Rg}}
const FOIL=haritalar(512,768,true);
function mrYap(src,tex){const W=src.width,H=src.height,d=src.getContext("2d").getImageData(0,0,W,H).data;const c=tex.image,g=c.getContext("2d"),o=g.createImageData(W,H);
  for(let i=0;i<d.length;i+=4){const r=d[i],gr=d[i+1],b=d[i+2];const altin=r>120&&r-b>55&&gr>80&&gr<r;const koyu=(r+gr+b)<120;
    let rough=.82,met=0;if(altin){rough=.26+((i>>2)%7)*.012;met=1}else if(koyu){rough=.42}
    o.data[i]=0;o.data[i+1]=rough*255;o.data[i+2]=met*255;o.data[i+3]=255}
  g.putImageData(o,0,0);tex.needsUpdate=true}
function mrTex(w,h){const c=document.createElement("canvas");c.width=w;c.height=h;return new THREE.CanvasTexture(c)}
'''
rep("function makeBag(o){",foil+"function makeBag(o){")

rep("const mat=new THREE.MeshPhysicalMaterial({color:o.color,metalness:o.metal,roughness:o.rough,clearcoat:o.clear,clearcoatRoughness:.35,bumpMap:crinkle,bumpScale:.0011,envMapIntensity:.85});",
    "const mat=new THREE.MeshPhysicalMaterial({color:o.color,metalness:o.metal,roughness:1,roughnessMap:FOIL.Rg,normalMap:FOIL.N,normalScale:new THREE.Vector2(o.ns,o.ns),clearcoat:o.clear,clearcoatRoughness:.28,envMap:ENV,envMapIntensity:1});")
rep("const label=new THREE.Mesh(lg,new THREE.MeshStandardMaterial({map:tex,roughness:.6,metalness:.15,envMapIntensity:.6}));",
    "const mr=mrTex(lc.width,lc.height);const label=new THREE.Mesh(lg,new THREE.MeshPhysicalMaterial({map:tex,metalnessMap:mr,roughnessMap:mr,metalness:1,roughness:1,clearcoat:.15,clearcoatRoughness:.6,envMap:ENV}));")
rep("return {grp,mesh,label,lc,tex,o};","return {grp,mesh,label,lc,tex,o,mr};")
rep("new THREE.MeshPhysicalMaterial({color:o.color,metalness:o.metal,roughness:.5,bumpMap:crinkle,bumpScale:.004})",
    "new THREE.MeshPhysicalMaterial({color:o.color,metalness:o.metal,roughness:.45,normalMap:FOIL.N,normalScale:new THREE.Vector2(1.2,1.2),envMap:ENV})")
rep('const A=makeBag({kind:"bag",w:1.34,h:2.2,d:0.66,color:0x0d0a08,metal:.12,rough:.52,clear:.35,',
    'const A=makeBag({kind:"bag",w:1.34,h:2.2,d:0.66,color:0x0c0908,metal:.0,rough:.6,clear:.2,ns:.35,')
rep('const B=makeBag({kind:"pouch",w:1.14,h:1.58,d:0.48,color:0xa65a2a,metal:.7,rough:.36,clear:.3,',
    'const B=makeBag({kind:"pouch",w:1.14,h:1.58,d:0.48,color:0xc9875a,metal:1,rough:.3,clear:.0,ns:.55,')
rep("  A.tex.needsUpdate=true}\nfunction etiketB(){","  A.tex.needsUpdate=true;mrYap(A.lc,A.mr)}\nfunction etiketB(){")
rep("  B.tex.needsUpdate=true}\netiketA();etiketB();","  B.tex.needsUpdate=true;mrYap(B.lc,B.mr)}\netiketA();etiketB();")
rep("const m=new THREE.Mesh(lg,new THREE.MeshStandardMaterial({map:arkaT,roughness:.6,metalness:.15,side:THREE.BackSide}));",
    "const arkaMR=mrTex(1024,1290);window.__arkaMR=arkaMR;const m=new THREE.Mesh(lg,new THREE.MeshPhysicalMaterial({map:arkaT,metalnessMap:arkaMR,roughnessMap:arkaMR,metalness:1,roughness:1,envMap:ENV,side:THREE.BackSide}));")
rep("  g.restore();arkaT.needsUpdate=true}","  g.restore();arkaT.needsUpdate=true;mrYap(arkaC,window.__arkaMR)}")
rep("img.width*s,img.height*s);b.tex.needsUpdate=true};","img.width*s,img.height*s);b.tex.needsUpdate=true;mrYap(b.lc,b.mr)};")

# 3) Çekirdek dokusu
rep("const beanMat=new THREE.MeshPhysicalMaterial({color:0x3d2214,roughness:.38,metalness:0,clearcoat:.5,clearcoatRoughness:.4,sheen:0});",
'''const beanTex=(function(){const c=document.createElement("canvas");c.width=c.height=256;const g=c.getContext("2d");const gr=g.createRadialGradient(128,110,10,128,128,150);gr.addColorStop(0,"#6b3d22");gr.addColorStop(1,"#2a160c");g.fillStyle=gr;g.fillRect(0,0,256,256);
  for(let i=0;i<1800;i++){g.fillStyle=`rgba(${Math.random()<.5?"20,10,5":"120,72,40"},${Math.random()*.25})`;g.fillRect(Math.random()*256,Math.random()*256,1+Math.random()*2,1+Math.random()*2)}
  const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;return t})();
const beanMat=new THREE.MeshPhysicalMaterial({map:beanTex,color:0xffffff,roughness:.42,metalness:0,clearcoat:.55,clearcoatRoughness:.35,envMap:ENV});''')

# 4) Zemin: koyu taş, hafif yansıma + temas gölgeleri
rep("const floorMat=new THREE.MeshStandardMaterial({color:0x0b0705,roughness:.96,metalness:0});",
'''const TAS=haritalar(256,256,false);TAS.Rg.wrapS=TAS.Rg.wrapT=TAS.N.wrapS=TAS.N.wrapT=THREE.RepeatWrapping;TAS.Rg.repeat.set(10,10);TAS.N.repeat.set(10,10);
const floorMat=new THREE.MeshStandardMaterial({color:0x100b08,roughness:.85,roughnessMap:TAS.Rg,normalMap:TAS.N,normalScale:new THREE.Vector2(.25,.25),metalness:0,envMap:ENV,envMapIntensity:.35});''')
rep("scene.add(A.grp,B.grp);",'''scene.add(A.grp,B.grp);
const golgeT=(function(){const c=document.createElement("canvas");c.width=c.height=128;const g=c.getContext("2d");const gr=g.createRadialGradient(64,64,4,64,64,64);gr.addColorStop(0,"rgba(0,0,0,.85)");gr.addColorStop(.55,"rgba(0,0,0,.35)");gr.addColorStop(1,"rgba(0,0,0,0)");g.fillStyle=gr;g.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)})();
const temas=[A,B].map(b=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(b.o.w*1.5,b.o.d*2.6),new THREE.MeshBasicMaterial({map:golgeT,transparent:true,depthWrite:false}));m.rotation.x=-Math.PI/2;scene.add(m);return m});''')
rep("B.grp.position.set(S.bx,FLOOR+B.o.h/2+S.by,S.bz);B.grp.rotation.set(0,S.bry+drag*0.6-idle,S.brz);",
"B.grp.position.set(S.bx,FLOOR+B.o.h/2+S.by,S.bz);B.grp.rotation.set(0,S.bry+drag*0.6-idle,S.brz);\n  [[A,temas[0],S.ay],[B,temas[1],S.by]].forEach(([b,m,yy])=>{m.position.set(b.grp.position.x,FLOOR+0.003,b.grp.position.z);m.rotation.z=-b.grp.rotation.y;m.material.opacity=Math.max(0,1-yy*1.4)*(1-Math.min(1,Math.abs(b.grp.rotation.z)));m.scale.setScalar(1+yy*.6)});")

# 5) Işık ve ton
rep("R.toneMappingExposure=1.1;","R.toneMappingExposure=1.0;R.physicallyCorrectLights=false;")
rep("key.shadow.mapSize.set(2048,2048);","key.shadow.mapSize.set(innerWidth<720?1024:2048,innerWidth<720?1024:2048);key.shadow.radius=4;")
open(p,'w',encoding='utf-8').write(t);print('tamam')
