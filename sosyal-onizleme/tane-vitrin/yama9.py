import sys
p=sys.argv[1];t=open(p,encoding='utf-8').read()
KR='''const KRAFT=(function(){const c=document.createElement("canvas");c.width=512;c.height=768;const g=c.getContext("2d");g.fillStyle="#b08a5f";g.fillRect(0,0,512,768);
  for(let i=0;i<5200;i++){const x=Math.random()*512,y=Math.random()*768,l=3+Math.random()*14,a=(Math.random()-.5)*.8;g.strokeStyle=Math.random()<.5?`rgba(222,190,146,${.05+Math.random()*.14})`:`rgba(92,62,36,${.05+Math.random()*.14})`;g.lineWidth=.5+Math.random();g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.cos(a)*l,y+Math.sin(a)*l);g.stroke()}
  for(let i=0;i<900;i++){g.fillStyle=`rgba(60,38,20,${Math.random()*.35})`;g.fillRect(Math.random()*512,Math.random()*768,1+Math.random()*1.5,1+Math.random()*1.5)}
  const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;t.anisotropy=R.capabilities.getMaxAnisotropy();return t})();
function makeBag(o){'''
WIN='''z.position.set(0,zy,(o.d/2)*puff(0,zy/(o.h/2),"pouch")+0.008);grp.add(z);
    const pc=document.createElement("canvas");pc.width=320;pc.height=128;const pg=pc.getContext("2d");
    pg.beginPath();pg.moveTo(26,6);pg.arcTo(314,6,314,122,20);pg.arcTo(314,122,6,122,20);pg.arcTo(6,122,6,6,20);pg.arcTo(6,6,314,6,20);pg.closePath();pg.clip();
    pg.fillStyle="#24130a";pg.fillRect(0,0,320,128);for(let i=0;i<3000;i++){pg.fillStyle=["#4a2a14","#1a0d05","#6b3f1f","#331a0b","#59331a"][i%5];pg.beginPath();pg.arc(Math.random()*320,Math.random()*128,.6+Math.random()*1.7,0,7);pg.fill()}
    const gl=pg.createLinearGradient(0,0,320,128);gl.addColorStop(0,"rgba(255,255,255,.2)");gl.addColorStop(.3,"rgba(255,255,255,0)");pg.fillStyle=gl;pg.fillRect(0,0,320,128);
    const wt=new THREE.CanvasTexture(pc);wt.encoding=THREE.sRGBEncoding;const wg=new THREE.PlaneGeometry(.64,.256,20,8);const wp=wg.attributes.position;const wy=o.h*0.25;
    for(let i=0;i<wp.count;i++){const x=wp.getX(i),y=wp.getY(i)+wy;wp.setZ(i,(o.d/2)*puff(x/(o.w/2),y/(o.h/2),"pouch")+wr(x,y)+0.007)}wg.computeVertexNormals();
    const win=new THREE.Mesh(wg,new THREE.MeshPhysicalMaterial({map:wt,transparent:true,alphaTest:.5,roughness:.1,clearcoat:1,clearcoatRoughness:.04,envMap:ENV,envMapIntensity:1.1}));win.position.y=wy;grp.add(win)}'''
R=[
('function puff(xn,yn,kind){let f=','function puff(xn,yn,kind){if(kind==="kraft")return Math.max(.035,(1-ss(.3,.64,yn)*.95)*(.93+.07*(1-xn*xn)));let f='),
('function makeBag(o){',KR),
('let nz=z*puff(xn,yn,o.kind);','if(o.kind==="kraft"&&Math.abs(Math.abs(x)-o.w/2)<1e-4)p.setX(i,x-Math.sign(x)*0.11*(1-Math.abs(z)/(o.d/2))*(0.4+0.6*ss(-0.2,0.6,yn)));let nz=z*puff(xn,yn,o.kind);'),
('const mat=new THREE.MeshPhysicalMaterial({color:o.color,metalness:o.metal,roughness:1,roughnessMap:FOIL.Rg,normalMap:FOIL.N,normalScale:new THREE.Vector2(o.ns,o.ns),clearcoat:o.clear,clearcoatRoughness:.4,envMap:ENV,envMapIntensity:o.ei});',
 'const mat=new THREE.MeshPhysicalMaterial(Object.assign({color:o.color,metalness:o.metal,roughness:1,roughnessMap:FOIL.Rg,normalMap:FOIL.N,normalScale:new THREE.Vector2(o.ns,o.ns),clearcoat:o.clear,clearcoatRoughness:.4,envMap:ENV,envMapIntensity:o.ei},o.kind==="kraft"?{map:KRAFT,roughnessMap:null,roughness:.93}:{}));'),
('seal.position.y=o.h*0.48;seal.castShadow=true;grp.add(seal);','''seal.position.y=o.h*0.48;seal.castShadow=true;
  if(o.kind!=="kraft")grp.add(seal);else{const rk=new THREE.MeshPhysicalMaterial({map:KRAFT,roughness:.9,normalMap:FOIL.N,normalScale:new THREE.Vector2(.4,.4),envMap:ENV,envMapIntensity:.25});
    const rl=new THREE.Mesh(new THREE.CylinderGeometry(.07,.07,o.w*.97,28),rk);rl.rotation.z=Math.PI/2;rl.position.y=o.h/2-.035;rl.castShadow=true;grp.add(rl);
    const fl=new THREE.Mesh(new THREE.BoxGeometry(o.w*.97,.16,.022),rk);fl.position.set(0,o.h/2-.11,.04);fl.rotation.x=-.18;fl.castShadow=true;grp.add(fl);
    const tm=new THREE.MeshPhysicalMaterial({color:0xc9a24e,metalness:1,roughness:.32,envMap:ENV,envMapIntensity:1});
    const tie=new THREE.Mesh(new THREE.BoxGeometry(o.w*1.16,.032,.014),tm);tie.position.set(0,o.h/2-.035,.074);tie.castShadow=true;grp.add(tie);
    [-1,1].forEach(s=>{const e=new THREE.Mesh(new THREE.BoxGeometry(.1,.032,.014),tm);e.position.set(s*(o.w*.58+.03),o.h/2-.06,.05);e.rotation.z=s*-.9;grp.add(e)})}'''),
('const vy=o.h*0.3;','const vy=o.h*(o.kind==="kraft"?0.22:0.3);'),
('z.position.set(0,zy,(o.d/2)*puff(0,zy/(o.h/2),"pouch")+0.008);grp.add(z)}',WIN),
('makeBag({kind:"bag",w:1.34,h:2.2,d:0.66,color:0x0c0908,metal:.0,rough:.6,clear:.08,ns:.12,ei:.28,lw:0.98,lh:1.24,ly:-0.16,valve:true});',
 'makeBag({kind:"kraft",w:1.3,h:2.2,d:0.72,color:0xffffff,metal:0,rough:.9,clear:0,ns:.3,ei:.25,lw:0.98,lh:1.24,ly:-0.24,valve:true});'),
]
for a,b in R:
    if a not in t: print('YOK:',a[:70]); sys.exit(1)
    t=t.replace(a,b,1)
open(p,'w',encoding='utf-8').write(t);print('tamam')
