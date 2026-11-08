import sys
p=sys.argv[1];t=open(p,encoding='utf-8').read()
J='https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/'
pp=''.join(f'\n<script src="{J}{f}"></script>' for f in ['shaders/CopyShader.js','shaders/LuminosityHighPassShader.js','shaders/GammaCorrectionShader.js','shaders/BokehShader.js','postprocessing/EffectComposer.js','postprocessing/RenderPass.js','postprocessing/ShaderPass.js','postprocessing/UnrealBloomPass.js','postprocessing/BokehPass.js'])
R=[
('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>','<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>'+pp),
('const AYAR={orbitBean:64,','const AYAR={orbitBean:40,'),
('const floor=new THREE.Mesh(new THREE.PlaneGeometry(40,40),floorMat);','''function siklorama(){const g=new THREE.PlaneGeometry(40,40,1,90);const p=g.attributes.position;const r=4.5;
  for(let i=0;i<p.count;i++){const y=p.getY(i),d=y-3;if(d<=0)continue;let ny,nz;if(d<Math.PI*r/2){ny=3+r*Math.sin(d/r);nz=r*(1-Math.cos(d/r))}else{ny=3+r;nz=r+(d-Math.PI*r/2)}p.setY(i,ny);p.setZ(i,nz)}
  g.computeVertexNormals();return g}
const floor=new THREE.Mesh(siklorama(),floorMat);'''),
('const g=new THREE.SphereGeometry(1,20,14);','const g=new THREE.SphereGeometry(1,32,22);'),
('const gp=[];const dum=new THREE.Object3D();','''const gp=[];const dum=new THREE.Object3D();
const pileN=240;const pile=new THREE.InstancedMesh(orbit.geometry,beanMat,pileN+40);pile.castShadow=true;pile.receiveShadow=true;
(function(){const d=new THREE.Object3D();let s=11;const r=()=>{s=(s*9301+49297)%233280;return s/233280};
  for(let i=0;i<pileN+40;i++){let x,z,y;const sc=.05+r()*.016;
    if(i<pileN){const a=r()*Math.PI*2,rr=.62*Math.sqrt(r());x=2.75+Math.cos(a)*rr*1.2;z=1.05+Math.sin(a)*rr*.75;const h=.22*Math.max(0,1-rr/.62);y=FLOOR+sc*.52+r()*h}
    else{x=-1+r()*5.5;z=.6+r()*1.6;y=FLOOR+sc*.52}
    d.position.set(x,y,z);d.rotation.set(Math.PI/2*(r()<.5?1:-1)+(r()-.5)*.5,(r()-.5)*.4,r()*Math.PI*2);d.scale.setScalar(sc);d.updateMatrix();pile.setMatrixAt(i,d.matrix)}})();
scene.add(pile);
const yumusakT=(()=>{const c=document.createElement("canvas");c.width=c.height=64;const g=c.getContext("2d");const gr=g.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,"rgba(255,248,240,1)");gr.addColorStop(.4,"rgba(255,248,240,.35)");gr.addColorStop(1,"rgba(255,248,240,0)");g.fillStyle=gr;g.fillRect(0,0,64,64);return new THREE.CanvasTexture(c)})();
const kupa=new THREE.Group();
const seramik=new THREE.MeshPhysicalMaterial({color:0xefe8df,roughness:.22,clearcoat:1,clearcoatRoughness:.08,envMap:ENV,envMapIntensity:.8});
const V2=a=>a.map(q=>new THREE.Vector2(q[0],q[1]));
const fincan=new THREE.Mesh(new THREE.LatheGeometry(V2([[0,0],[.2,0],[.235,.012],[.24,.03],[.255,.2],[.29,.36],[.3,.38],[.285,.385],[.27,.36],[.24,.2],[.225,.05],[0,.05]]),64),seramik);fincan.castShadow=true;fincan.position.y=.05;kupa.add(fincan);
const tabak=new THREE.Mesh(new THREE.LatheGeometry(V2([[0,0],[.42,0],[.5,.035],[.52,.05],[.49,.05],[.4,.025],[.2,.02],[0,.02]]),64),seramik);tabak.castShadow=true;tabak.receiveShadow=true;kupa.add(tabak);
const kulp=new THREE.Mesh(new THREE.TorusGeometry(.09,.022,16,32,Math.PI*1.2),seramik);kulp.position.set(.3,.25,0);kulp.rotation.z=-Math.PI*.6;kupa.add(kulp);
const kremaT=(()=>{const c=document.createElement("canvas");c.width=c.height=256;const g=c.getContext("2d");const gr=g.createRadialGradient(118,122,4,128,128,128);
  gr.addColorStop(0,"#9a6432");gr.addColorStop(.5,"#7a4520");gr.addColorStop(.8,"#c8925a");gr.addColorStop(.9,"#5a3017");gr.addColorStop(1,"#2e170a");g.fillStyle=gr;g.fillRect(0,0,256,256);
  for(let i=0;i<900;i++){g.fillStyle=`rgba(${Math.random()<.5?"230,190,140":"60,30,12"},${Math.random()*.18})`;g.beginPath();g.arc(Math.random()*256,Math.random()*256,Math.random()*2.2,0,7);g.fill()}
  const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;return t})();
const kahveY=new THREE.Mesh(new THREE.CircleGeometry(.258,48),new THREE.MeshPhysicalMaterial({map:kremaT,roughness:.25,clearcoat:.6,clearcoatRoughness:.15,envMap:ENV}));kahveY.rotation.x=-Math.PI/2;kahveY.position.y=.35;kupa.add(kahveY);
const buhar=[];for(let i=0;i<16;i++){const m=new THREE.Sprite(new THREE.SpriteMaterial({map:yumusakT,transparent:true,depthWrite:false,opacity:0}));kupa.add(m);buhar.push({m,t:i/16,x:(Math.random()-.5)*.1,ph:Math.random()*6})}
scene.add(kupa);
const tozN=260;const tozG=new THREE.BufferGeometry();const tp=new Float32Array(tozN*3);for(let i=0;i<tozN;i++){tp[i*3]=-3+Math.random()*7;tp[i*3+1]=FLOOR+Math.random()*4.5;tp[i*3+2]=-2+Math.random()*4.5}
tozG.setAttribute("position",new THREE.BufferAttribute(tp,3));
const toz=new THREE.Points(tozG,new THREE.PointsMaterial({color:0xffd9a8,size:.022,map:yumusakT,transparent:true,opacity:.6,depthWrite:false,blending:THREE.AdditiveBlending}));scene.add(toz);'''),
('addEventListener("resize",resize);resize();','''addEventListener("resize",resize);resize();
let comp=null,bokeh=null,bloom=null;
if(THREE.EffectComposer&&THREE.UnrealBloomPass&&THREE.GammaCorrectionShader){try{comp=new THREE.EffectComposer(R);comp.addPass(new THREE.RenderPass(scene,cam));
  if(THREE.BokehPass&&!mobil()){bokeh=new THREE.BokehPass(scene,cam,{focus:7,aperture:.0025,maxblur:.006,width:innerWidth,height:innerHeight});comp.addPass(bokeh)}
  bloom=new THREE.UnrealBloomPass(new THREE.Vector2(innerWidth,innerHeight),.32,.55,.85);comp.addPass(bloom);comp.addPass(new THREE.ShaderPass(THREE.GammaCorrectionShader));
  addEventListener("resize",()=>{comp.setSize(innerWidth,innerHeight)})}catch(e){comp=null}}'''),
('  R.render(scene,cam);\n','''  const sp=scrollY/Math.max(1,document.documentElement.scrollHeight-innerHeight);const cupK=1-ss(.03,.11,sp);kupa.visible=cupK>.01;
  if(mobil())kupa.position.set(-.8,FLOOR,1.4);else kupa.position.set(.3,FLOOR,1.6);kupa.scale.setScalar(.9);
  for(const b of buhar){if(!reduce)b.t+=dt*.16;if(b.t>1)b.t-=1;b.m.position.set(b.x+Math.sin(t*1.3+b.ph+b.t*4)*.09*b.t,.42+b.t*1.15,Math.cos(t+b.ph)*.04);b.m.scale.setScalar(.1+b.t*.5);b.m.material.opacity=.22*Math.sin(Math.PI*b.t)*cupK}
  if(!reduce){toz.rotation.y=t*.012;toz.position.y=Math.sin(t*.25)*.06}
  if(comp){if(bokeh)bokeh.uniforms.focus.value=cam.position.distanceTo(A.grp.position.x<-2.5?B.grp.position:A.grp.position);comp.render()}else R.render(scene,cam);
'''),
]
for a,b in R:
    if a not in t: print('YOK:',a[:70]); sys.exit(1)
    t=t.replace(a,b,1)
open(p,'w',encoding='utf-8').write(t);print('tamam')
