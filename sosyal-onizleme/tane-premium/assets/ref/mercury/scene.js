import * as THREE from './vendor/three.module.js';
const TAU=Math.PI*2, stage=document.querySelector('#stage');
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setSize(innerWidth,innerHeight);
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;stage.appendChild(renderer.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color('#bfc3c4');scene.fog=new THREE.FogExp2('#cbd0d1',.022);
const camera=new THREE.PerspectiveCamera(44,innerWidth/innerHeight,.1,120);
const chrome=new THREE.MeshPhysicalMaterial({color:0xaab4b6,metalness:1,roughness:.085,clearcoat:1,envMapIntensity:1.1});
const metal=new THREE.MeshStandardMaterial({color:0x9ba4a2,metalness:.92,roughness:.25});
// Fine circumferential brushing on the structural metal.
const brushCanvas=document.createElement('canvas');brushCanvas.width=512;brushCanvas.height=512;const bc=brushCanvas.getContext('2d');bc.fillStyle='#999999';bc.fillRect(0,0,512,512);for(let i=0;i<1600;i++){const v=90+Math.floor((Math.sin(i*73.71)*.5+.5)*100);bc.strokeStyle=`rgba(${v},${v},${v},.22)`;const y=(i*37.71)%512;bc.beginPath();bc.moveTo(0,y);bc.lineTo(512,y+.3);bc.stroke();}const brushing=new THREE.CanvasTexture(brushCanvas);brushing.wrapS=brushing.wrapT=THREE.RepeatWrapping;brushing.repeat.set(4,2);metal.bumpMap=brushing;metal.bumpScale=.006;metal.roughness=.31;
const wall=new THREE.MeshStandardMaterial({color:0xbfc5c2,metalness:.65,roughness:.34,side:THREE.BackSide});
const dark=new THREE.MeshStandardMaterial({color:0x46514f,metalness:.85,roughness:.3});
// High-contrast studio reflections, augmented below with the actual chamber.
const ec=document.createElement('canvas');ec.width=2048;ec.height=1024;const ctx=ec.getContext('2d');
let bg=ctx.createLinearGradient(0,0,0,1024);bg.addColorStop(0,'#f9faf6');bg.addColorStop(.42,'#9aaba9');bg.addColorStop(.55,'#172120');bg.addColorStop(1,'#b9c2bf');ctx.fillStyle=bg;ctx.fillRect(0,0,2048,1024);
for(const [x,w] of [[60,250],[450,35],[650,370],[1280,80],[1560,240]]){ctx.fillStyle='#f5f7f2';ctx.fillRect(x,60,w,600);ctx.fillStyle='#394541';ctx.fillRect(x+w,60,22,730);}
const et=new THREE.CanvasTexture(ec);et.mapping=THREE.EquirectangularReflectionMapping;et.colorSpace=THREE.SRGBColorSpace;
const pmrem=new THREE.PMREMGenerator(renderer);const studio=pmrem.fromEquirectangular(et);scene.environment=studio.texture;et.dispose();
scene.add(new THREE.HemisphereLight(0xf6f8fa,0x465054,1.3));
for(const [x,y,z,intensity] of [[-6,9,4,190],[6,7,-5,200],[0,12,0,240]]){let light=new THREE.PointLight(0xf8faff,intensity,45,2);light.position.set(x,y,z);scene.add(light);}
function mesh(g,m,parent=scene){const o=new THREE.Mesh(g,m);parent.add(o);return o;}
function rod(a,b,r,parent=scene,mat=metal){const p=new THREE.Vector3(...a),q=new THREE.Vector3(...b);const o=mesh(new THREE.CylinderGeometry(r,r,p.distanceTo(q),8),mat,parent);o.position.copy(p).add(q).multiplyScalar(.5);o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),q.sub(p).normalize());return o;}
function ring(r,t,parent,mat=metal){return mesh(new THREE.TorusGeometry(r,t,20,160),mat,parent);}
// Large opaque wall panels replace the previous wire cage.
const shell=mesh(new THREE.CylinderGeometry(24,24,36,128,1,true),wall);shell.position.y=7;
const ceiling=mesh(new THREE.CircleGeometry(24,100),wall);ceiling.rotation.x=Math.PI/2;ceiling.position.y=19;
const ground=mesh(new THREE.CircleGeometry(24,100),metal);ground.rotation.x=-Math.PI/2;ground.position.y=-6;
for(let j=0;j<4;j++){const rib=ring(23.8,.28,scene);rib.rotation.x=Math.PI/2;rib.position.y=-4+j*7;}
// Offset, tilted annular structure: broad metal sweeps around the view.
const architecture=new THREE.Group();scene.add(architecture);architecture.position.set(.5,3,-3.4);architecture.rotation.set(.43,-.17,-.14);
// Wide rolled-steel annuli with rounded lips, rather than circular pipes.
function band(radius,width,depth,parent){const pts=[[radius,0],[radius+.035,.08],[radius+.08,depth],[radius+width-.06,depth+.04],[radius+width,depth],[radius+width,-.05],[radius+.06,-.08],[radius,0]];const g=new THREE.LatheGeometry(pts.map(p=>new THREE.Vector2(...p)),192);const o=mesh(g,metal,parent);o.rotation.x=Math.PI/2;return o;}
for(const [r,z,w,d] of [[6.2,0,.7,.45],[7.55,-1.6,.85,.6],[9.3,-3.8,1.1,.7]]){const o=band(r,w,d,architecture);o.position.z=z;const lip=ring(r,.045,architecture);lip.position.z=z;}
for(let i=0;i<44;i++){const a=i/44*TAU;rod([6.85*Math.cos(a),6.85*Math.sin(a),-.4],[8.3*Math.cos(a),8.3*Math.sin(a),-2.1],.085,architecture);}
const outer=new THREE.Group();scene.add(outer);outer.position.set(-.5,5.35,2.4);outer.rotation.set(.62,.18,-.27);
const sweep=band(7.3,1.15,.7,outer);const inset=ring(7.3,.055,outer);inset.position.z=.03;
// Structural ceiling rails, visible through the diagonal woven beam.
for(let x=-12;x<=12;x+=2.4){rod([x,11,-16],[x,11,7],.12);rod([x+.2,11.35,-16],[x+.2,11.35,7],.045);}
for(let z=-15;z<8;z+=3.3)rod([-13,11,z],[13,11,z],.12);
const beam=new THREE.Group();scene.add(beam);beam.position.set(0,7.4,0);beam.rotation.set(.08,.12,-.49);beam.scale.set(1,.82,.82);
// Instanced wire sections keep the dense diamond weave inexpensive.
const wireSegments=[];
function wire(a,b,r=.013){wireSegments.push({a:new THREE.Vector3(...a),b:new THREE.Vector3(...b),r});}
for(let y of [-.54,.54])for(let z of [-.48,.48])wire([-12,y,z],[12,y,z],.045);
for(let z of [-.48,.48]){for(let x=-13;x<12;x+=.24){wire([x,-.54,z],[x+1.08,.54,z]);wire([x,.54,z],[x+1.08,-.54,z]);}for(let y=-.54;y<=.55;y+=.18)wire([-12,y,z],[12,y,z],.009);}
for(let x=-12;x<12;x+=.3){wire([x,.54,-.48],[x+.96,.54,.48]);wire([x,-.54,-.48],[x+.96,-.54,.48]);}
const wires=new THREE.InstancedMesh(new THREE.CylinderGeometry(1,1,1,5),metal,wireSegments.length),wd=new THREE.Object3D();
for(let i=0;i<wireSegments.length;i++){let {a,b,r}=wireSegments[i];wd.position.copy(a).add(b).multiplyScalar(.5);wd.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),b.clone().sub(a).normalize());wd.scale.set(r,a.distanceTo(b),r);wd.updateMatrix();wires.setMatrixAt(i,wd.matrix);}beam.add(wires);
// Softbox panels illuminate the space and are visible in the captured reflections.
const lightPanels=[];
const luminous=new THREE.MeshBasicMaterial({color:new THREE.Color(3,3,2.9),side:THREE.DoubleSide});
for(let x of [-7,7]){const panel=mesh(new THREE.PlaneGeometry(4,12),luminous);panel.position.set(x,7,-8);panel.rotation.y=x>0?-.45:.45;lightPanels.push(panel);}
const top=mesh(new THREE.PlaneGeometry(11,9),luminous);top.position.set(0,14,-1);top.rotation.x=Math.PI/2;
// Bake the chamber into the liquid's reflection map once; no remote HDR needed.
const capture=new THREE.WebGLCubeRenderTarget(512,{type:THREE.HalfFloatType,generateMipmaps:true,minFilter:THREE.LinearMipmapLinearFilter});
const cube=new THREE.CubeCamera(.1,100,capture);cube.position.set(0,3,0);cube.update(renderer,scene);
const chamberEnvironment=pmrem.fromCubemap(capture.texture);chrome.envMap=chamberEnvironment.texture;pmrem.dispose();capture.dispose();
for(const panel of lightPanels)panel.visible=false;top.visible=false;
let seed=518;function random(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
const liquid=new THREE.Group();scene.add(liquid);liquid.position.y=1.2;liquid.scale.setScalar(.77);
// Smooth elliptical liquid cross sections, tapering to droplets at both ends.
// Irregular width, changing thickness and twisting frames avoid flat ribbon shapes.
const fluidParts=[];
function fluid(points,width,depth,phase=0,parent=liquid){const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));const n=160,k=20,frames=curve.computeFrenetFrames(n,false);const verts=[],indices=[];
for(let i=0;i<=n;i++){let u=i/n,c=curve.getPointAt(u),taper=.04+.96*Math.pow(Math.sin(Math.PI*u),.5),wave=1+.2*Math.sin(u*12+phase)+.09*Math.sin(u*25+phase);let twist=.65*Math.sin(u*11+phase)+u*3;
for(let j=0;j<=k;j++){let a=j/k*TAU,xx=Math.cos(a)*width*taper*wave,yy=Math.sin(a)*depth*taper*(1+.16*Math.sin(u*13));let nx=xx*Math.cos(twist)-yy*Math.sin(twist),ny=xx*Math.sin(twist)+yy*Math.cos(twist);const p=c.clone().addScaledVector(frames.normals[i],nx).addScaledVector(frames.binormals[i],ny);verts.push(p.x,p.y,p.z);if(i<n&&j<k){let q=i*(k+1)+j;indices.push(q,q+1,q+k+1,q+1,q+k+2,q+k+1);}}}
let g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));g.setIndex(indices);g.computeVertexNormals();const o=mesh(g,chrome,parent);fluidParts.push({mesh:o,phase});return o;}
// Separate impact splashes: unequal arcs, broad liquid lobes and tapered tips.
// No common axis, constant pitch, or repeated helical strands.
const splashPaths=[
[[-2.5,.6,.3],[-1.9,.15,.6],[-.8,.4,.85],[.1,1.1,.3],[.8,1.45,-.25]],
[[-1.9,2.1,-.3],[-1.4,2.9,.15],[-.2,3.2,.55],[.9,2.7,.8],[1.8,2.9,.2],[2.25,3.65,-.1]],
[[.1,4.4,-.7],[.95,4.85,-.3],[1.9,4.4,.25],[2.35,3.6,.55]],
[[-2.25,4.6,.3],[-1.85,4.1,.8],[-1.15,4.3,1.1],[-.85,5.2,.55]],
[[.8,.1,-.6],[1.7,.7,-.1],[2.15,1.5,.2],[1.9,2.1,.6]],
[[-.6,1.5,-1.1],[.1,1.9,-1.7],[.9,2.8,-1.4],[.4,3.55,-.8]],
[[-2.5,2,-.7],[-2.8,2.7,-.2],[-2.6,3.3,.1]]];
const splashCurves=splashPaths.map(path=>new THREE.CatmullRomCurve3(path.map(p=>new THREE.Vector3(...p))));
splashPaths.forEach((path,i)=>{fluid(path,[.38,.48,.34,.23,.3,.27,.13][i],[.11,.1,.09,.065,.12,.07,.045][i],i*.73);});
// Fingers peel away from the sheets; a few looped edges suggest torn liquid skins.
for(let i=0;i<12;i++){const curve=splashCurves[i%splashCurves.length],u=.2+random()*.6,p=curve.getPoint(u),dir=i%2?1:-1;fluid([[p.x,p.y,p.z],[p.x+dir*.28,p.y+.22,p.z+.12],[p.x+dir*.52,p.y+.65,p.z+.25],[p.x+dir*.42,p.y+1,p.z+.18]],.045+random()*.03,.025,i);}
fluid([[-1.55,2.9,.2],[-1.8,3.4,.4],[-1.4,3.75,.7],[-.85,3.5,.75],[-.7,3.12,.5]],.085,.03,2);
// Framing splash, inspired by the close molten sweep at the reference's lower edge.
const foreground=new THREE.Group();scene.add(foreground);
fluid([[-6,-1.8,3],[-4.6,-2.1,4],[-2.1,-2.5,4.3],[.5,-2.35,4],[3,-1.5,3.5],[5,-.2,2.8]],.36,.1,2,foreground);
// Mirror-polished silver, shaped by surface tension like suspended water.
const dropletMaterial=chrome.clone();dropletMaterial.roughness=.065;
dropletMaterial.color.setHex(0xd3dce0);dropletMaterial.envMap=studio.texture;dropletMaterial.envMapIntensity=1.1;
const dropletGeometry=new THREE.SphereGeometry(1,24,16);
// Surface tension keeps suspended drops nearly round, with a softly tapered shoulder.
const dropVertices=dropletGeometry.attributes.position;
for(let i=0;i<dropVertices.count;i++){const y=dropVertices.getY(i),shoulder=1-.075*y;dropVertices.setXYZ(i,dropVertices.getX(i)*shoulder,y,dropVertices.getZ(i)*shoulder);}
dropletGeometry.computeVertexNormals();
const count=520,drops=new THREE.InstancedMesh(dropletGeometry,dropletMaterial,count);scene.add(drops);const data=[];
// Uneven spray clusters around splash tips and surfaces, plus sparse free droplets.
for(let i=0;i<count;i++){const curve=splashCurves[Math.floor(random()*splashCurves.length)],u=random(),p=curve.getPoint(u),spread=i%5===0?1.1:.20+random()*.35;p.x+=(random()-.5)*spread*2;p.y+=(random()-.5)*spread*2;p.z+=(random()-.5)*spread*2;data.push({x:p.x,y:p.y,z:p.z,s:.022+Math.pow(random(),2)*.095,p:random()*TAU,stretch:.92+random()*.36});}
drops.position.y=1.2;drops.scale.setScalar(.77);
// A continuous surface changes from an open helix into an asymmetric chrome loop.
const formingMaterial=chrome.clone();formingMaterial.envMap=studio.texture;formingMaterial.color.setHex(0xe0e4e7);formingMaterial.roughness=.13;
const morphSegments=224,morphSides=64,morphPositions=new Float32Array((morphSegments+1)*(morphSides+1)*3),morphIndices=[];
for(let i=0;i<morphSegments;i++)for(let j=0;j<morphSides;j++){let a=i*(morphSides+1)+j,b=a+morphSides+1;morphIndices.push(a,a+1,b,a+1,b+1,b);}
const morphGeometry=new THREE.BufferGeometry();morphGeometry.setAttribute('position',new THREE.BufferAttribute(morphPositions,3).setUsage(THREE.DynamicDrawUsage));morphGeometry.setIndex(morphIndices);
const formedLoop=mesh(morphGeometry,formingMaterial,liquid);formedLoop.frustumCulled=false;
const fadingMaterial=chrome.clone();fadingMaterial.transparent=true;fadingMaterial.depthWrite=false;
for(const part of fluidParts)if(part.mesh.parent===liquid)part.mesh.material=fadingMaterial;
function loopPoint(u,v){const a=u*TAU;
// Asymmetric rounded triangular loop: heavy lower lobe, narrow left waist,
// sloping crown and softly folded inner rim, matching the supplied sculpture.
const thickness=.54+.19*(1-Math.cos(a))+.075*Math.sin(a-.6);
const x=1.11*Math.sin(a)-.30*Math.cos(a)+.16*Math.cos(a*2)-.13*Math.sin(a*2),y=2.7+1.7*Math.cos(a),z=.14*Math.sin(a*2);
const inner=Math.pow(Math.max(0,-Math.cos(v)),3),fold=inner*(.055*Math.sin(a*5+.4)+.025*Math.sin(a*9));
return new THREE.Vector3(x+Math.sin(a)*Math.cos(v)*(thickness+fold),y+Math.cos(a)*Math.cos(v)*(thickness+fold),z+Math.sin(v)*thickness*.98+fold);}
// Matching vertex layouts let one continuous silver surface become several sculptures.
const loopShape=new Float32Array(morphPositions.length),orbShape=new Float32Array(morphPositions.length);
const knotGeometry=new THREE.TorusKnotGeometry(1.16,.38,morphSegments,morphSides,2,3);
const knotShape=knotGeometry.attributes.position.array.slice();
for(let i=0;i<=morphSegments;i++)for(let j=0;j<=morphSides;j++){
 const u=i/morphSegments,v=j/morphSides*TAU,k=(i*(morphSides+1)+j)*3,p=loopPoint(u,v);
 loopShape.set([p.x,p.y,p.z],k);knotShape[k+1]+=2.7;
 // A near-closed toroidal skin preserves topology while reading as a molten orb.
 const a=u*TAU,r=1.4+.08*Math.sin(a*3+Math.sin(v)*2),radial=.23+r*(1+Math.cos(v));
 orbShape.set([Math.sin(a)*radial*.75,2.7+Math.sin(v)*1.7,Math.cos(a)*radial*.75],k);
}
knotGeometry.dispose();
const shapes=[loopShape,knotShape,orbShape];let lastShape=-1;
function updateFormation(value){
 if(Math.abs(value-lastShape)<.0003)return;lastShape=value;
 const n=Math.min(1,Math.floor(value)),f=THREE.MathUtils.smootherstep(value-n,0,1),a=shapes[n],b=shapes[n+1];
 for(let k=0;k<morphPositions.length;k++)morphPositions[k]=a[k]+(b[k]-a[k])*f;
 morphGeometry.attributes.position.needsUpdate=true;morphGeometry.computeVertexNormals();
 const normals=morphGeometry.attributes.normal,norm=new THREE.Vector3(),other=new THREE.Vector3();
 function weld(a,b){norm.fromBufferAttribute(normals,a).add(other.fromBufferAttribute(normals,b)).normalize();normals.setXYZ(a,norm.x,norm.y,norm.z);normals.setXYZ(b,norm.x,norm.y,norm.z);}
 for(let i=0;i<=morphSegments;i++)weld(i*(morphSides+1),i*(morphSides+1)+morphSides);
 for(let j=0;j<=morphSides;j++)weld(j,morphSegments*(morphSides+1)+j);
 normals.needsUpdate=true;
}
updateFormation(0);drops.visible=true;formedLoop.visible=false;
formingMaterial.transparent=true;formingMaterial.opacity=0;
const particleTargets=data.map((d,i)=>loopPoint(i/count,d.p));
drops.rotation.copy(liquid.rotation);
for(const part of fluidParts)if(part.mesh.parent===liquid)part.mesh.visible=true;
liquid.rotation.set(0,-.14,-.025);
// Only the chamber rotates; the central model and camera remain independent.
const environmentGroup=new THREE.Group();environmentGroup.position.set(0,3,0);
const environmentObjects=scene.children.filter(o=>o!==liquid&&o!==drops);scene.add(environmentGroup);for(const o of environmentObjects)environmentGroup.attach(o);
// Second world: a sculptural silver spinal column and a spatial gallery.
const axisWorld=new THREE.Group();scene.add(axisWorld);axisWorld.visible=false;
const spine=new THREE.Group();axisWorld.add(spine);spine.position.y=3;spine.scale.setScalar(.74);
const boneMaterial=chrome.clone();boneMaterial.envMap=studio.texture;boneMaterial.color.setHex(0xe1e7eb);boneMaterial.roughness=.29;boneMaterial.envMapIntensity=1.2;boneMaterial.clearcoat=.32;
// Fine machining grain and sparse hairline scratches; reflections remain silver.
const metalCanvas=document.createElement('canvas');metalCanvas.width=metalCanvas.height=1024;
const mg=metalCanvas.getContext('2d'),grain=mg.createImageData(1024,1024);
let metalSeed=92741;function metalRandom(){metalSeed=(metalSeed*1664525+1013904223)>>>0;return metalSeed/4294967296;}
for(let y=0;y<1024;y++){const line=metalRandom()*24;for(let x=0;x<1024;x++){const k=(y*1024+x)*4,v=166+line+metalRandom()*20;grain.data[k]=grain.data[k+1]=grain.data[k+2]=v;grain.data[k+3]=255;}}
mg.putImageData(grain,0,0);
for(let i=0;i<950;i++){const x=metalRandom()*1024,y=metalRandom()*1024;mg.strokeStyle=`rgba(65,65,65,${.08+metalRandom()*.2})`;mg.lineWidth=.35+metalRandom()*.6;mg.beginPath();mg.moveTo(x,y);mg.lineTo(x+12+metalRandom()*170,y+metalRandom()*2);mg.stroke();}
const spineFinish=new THREE.CanvasTexture(metalCanvas);spineFinish.wrapS=spineFinish.wrapT=THREE.RepeatWrapping;spineFinish.repeat.set(2,3);spineFinish.anisotropy=renderer.capabilities.getMaxAnisotropy();
boneMaterial.bumpMap=spineFinish;boneMaterial.bumpScale=.018;boneMaterial.roughnessMap=spineFinish;

// Swept, flattened chrome blades: broad roots flow into hooked needle tips.
function spineBlade(points,width,depth,parent){
 const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p))),n=48,k=12,frames=curve.computeFrenetFrames(n,false),positions=[],indices=[],uvs=[];
 for(let i=0;i<=n;i++){const t=i/n,c=curve.getPointAt(t),taper=Math.pow(1-t,.85)*(.56+.8*Math.sin(Math.PI*t));
  for(let j=0;j<=k;j++){const v=j/k*TAU,p=c.clone().addScaledVector(frames.normals[i],Math.cos(v)*width*taper).addScaledVector(frames.binormals[i],Math.sin(v)*depth*taper);positions.push(p.x,p.y,p.z);uvs.push(j/k,t);if(i<n&&j<k){const q=i*(k+1)+j;indices.push(q,q+1,q+k+1,q+1,q+k+2,q+k+1);}}
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uvs,2));g.setIndex(indices);g.computeVertexNormals();return mesh(g,boneMaterial,parent);
}
const spinePath=new THREE.CatmullRomCurve3([new THREE.Vector3(-.7,-5.1,0),new THREE.Vector3(-.9,-3,.1),new THREE.Vector3(.35,-.5,0),new THREE.Vector3(.9,2,.1),new THREE.Vector3(.05,4.2,0),new THREE.Vector3(-1.2,5.1,-.1)].map(p=>new THREE.Vector3(p.x,p.y*3.4,p.z)));
mesh(new THREE.TubeGeometry(spinePath,160,.115,12,false),boneMaterial,spine);
const vertebraGeo=new THREE.SphereGeometry(1,32,20);
// Pinched waist and scalloped shoulders give each vertebra an armored silhouette.
const vp=vertebraGeo.attributes.position;
for(let i=0;i<vp.count;i++){const y=vp.getY(i),angle=Math.atan2(vp.getZ(i),vp.getX(i)),flare=.76+.3*Math.abs(y)+.09*Math.cos(angle*4);vp.setXYZ(i,vp.getX(i)*flare,y,vp.getZ(i)*flare);}
vertebraGeo.computeVertexNormals();
for(let i=0;i<72;i++){
 const t=(i+.3)/73,center=spinePath.getPointAt(t),tangent=spinePath.getTangentAt(t),width=.72-.3*t+.10*Math.sin(t*Math.PI);
 const vertebra=new THREE.Group();spine.add(vertebra);vertebra.position.copy(center);vertebra.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),tangent);
 const body=mesh(vertebraGeo,boneMaterial,vertebra);body.scale.set(width*.67,.29,width*.54);body.rotation.y=i*.19;
 for(const side of [-1,1]){
  const length=(1.25-.55*t)*(1+.12*Math.sin(i*.8));
  spineBlade([[side*.16,.10,0],[side*.48,.17,-.04],[side*length,-.12,-.08],[side*(length+.14),-.72,.03],[side*(length+.05),-1.04,.12]],.34*(1-.4*t),.085,vertebra);
  spineBlade([[side*.13,.09,.19],[side*.38,.29,.37],[side*.62,.56,.38],[side*.79,.65,.26]],.19,.065,vertebra);
 }
 spineBlade([[0,.04,-.12],[0,.18,-.48],[.05,.04,-.93],[.12,-.54,-1.12]],.26*(1-.35*t),.08,vertebra);
}
// Open upper tip: no oversized crescent hook.
spineBlade([[-.8,-4.7,0],[-1.2,-5.25,.02],[-1.05,-5.75,.1],[-.55,-6,.12]],.30,.09,spine).position.y=-12.24;
axisWorld.add(new THREE.HemisphereLight(0xd8eaff,0x101923,2));
for(const [x,y,z] of [[-5,7,4],[5,3,-4],[0,-3,5]]){const light=new THREE.PointLight(0xe1f1ff,100,30,2);light.position.set(x,y,z);axisWorld.add(light);}
// Original procedural editorial artwork on actual 3D panels.
const cardGlass=new THREE.MeshPhysicalMaterial({color:0xdceaf1,metalness:.08,roughness:.09,transmission:.94,thickness:.22,ior:1.46,clearcoat:1,clearcoatRoughness:.04,envMap:studio.texture,envMapIntensity:1.25,attenuationColor:0xb7d1de,attenuationDistance:3});
const cardChrome=chrome.clone();cardChrome.envMap=studio.texture;cardChrome.roughness=.065;cardChrome.color.setHex(0xe0e8ee);
const cards=[],cardTitles=['LIQUID MEMORY','SILVER STUDY','AFTER IMAGE','FORM / FIELD','SOFT MATTER','IN ORBIT'];
for(let i=0;i<6;i++){
 const c=document.createElement('canvas');c.width=1024;c.height=640;const g=c.getContext('2d');
 g.clearRect(0,0,1024,640);
 g.save();g.translate(600,290);g.rotate(i*.45-.4);
 for(let j=18;j>0;j--){g.beginPath();g.ellipse(Math.sin(j*.3)*40,0,55+j*17,40+j*10,j*.045,0,TAU);g.strokeStyle=`rgba(225,243,252,${.07+j*.014})`;g.lineWidth=2+j*.35;g.stroke();}g.restore();
 g.fillStyle='#eff7fa';g.font='16px monospace';g.fillText('M / '+String(i+1).padStart(2,'0')+'     MATERIAL EXPLORATIONS',48,55);g.font='52px Times New Roman';g.fillText(cardTitles[i],48,548);g.font='15px monospace';g.fillText('MERCURY     —     STUDIES IN MOTION',48,593);
 const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;texture.anisotropy=renderer.capabilities.getMaxAnisotropy();
 const group=new THREE.Group();axisWorld.add(group);
 const shape=new THREE.Shape(),w=3.5,h=2.19,r=.16;shape.moveTo(-w/2+r,-h/2);shape.lineTo(w/2-r,-h/2);shape.quadraticCurveTo(w/2,-h/2,w/2,-h/2+r);shape.lineTo(w/2,h/2-r);shape.quadraticCurveTo(w/2,h/2,w/2-r,h/2);shape.lineTo(-w/2+r,h/2);shape.quadraticCurveTo(-w/2,h/2,-w/2,h/2-r);shape.lineTo(-w/2,-h/2+r);shape.quadraticCurveTo(-w/2,-h/2,-w/2+r,-h/2);
 const plate=mesh(new THREE.ExtrudeGeometry(shape,{depth:.065,bevelEnabled:true,bevelSize:.025,bevelThickness:.025,bevelSegments:5,steps:1}),cardGlass,group);
 const faceGeo=new THREE.ShapeGeometry(shape),uv=faceGeo.attributes.uv,pp=faceGeo.attributes.position;for(let j=0;j<uv.count;j++)uv.setXY(j,(pp.getX(j)+w/2)/w,(pp.getY(j)+h/2)/h);
 const face=mesh(faceGeo,new THREE.MeshBasicMaterial({map:texture,side:THREE.DoubleSide,transparent:true,depthWrite:false,opacity:.8}),group);face.position.z=.094;
 const back=mesh(faceGeo,face.material,group);back.position.z=-.03;back.rotation.y=Math.PI;
 const rimPoints=shape.getPoints(80).map(p=>new THREE.Vector3(p.x,p.y,.04));
 const rimCurve=new THREE.CatmullRomCurve3(rimPoints,true);
 mesh(new THREE.TubeGeometry(rimCurve,160,.027,8,true),cardChrome,group);
 // Molten silver skims the glass at the upper and lower corners.
 for(const side of [-1,1]){
 const glaze=spineBlade([[side*1.69,-side*.76,.09],[side*1.60,-side*.93,.12],[side*.9,-side*1.04,.13],[side*.25,-side*.99,.10],[-side*.22,-side*1.05,.08]],.055,.018,group);glaze.material=cardChrome;
 }
 cards.push({group,phase:i/6*TAU,y:15-i*4.8});
}
// Emissive silver spray runs well beyond both ends of the camera journey.
const dustCount=innerWidth<768?28000:80000,dustPositions=new Float32Array(dustCount*3),dustSizes=new Float32Array(dustCount),dustSeeds=new Float32Array(dustCount);
for(let i=0;i<dustCount;i++){
 const y=-24+random()*54,stream=i%3,fringe=i%9===0;
 // Narrow luminous currents with feathered spray, rather than an even cloud.
 const scatter=(random()+random()+random()-1.5);
 const angle=y*.68+stream*TAU/3+.32*Math.sin(y*.34+stream)+scatter*(fringe?.9:.16);
 const radius=2.15+.60*Math.sin(y*.38+stream*.9)+scatter*(fringe?2.8:.46);
 dustPositions.set([Math.cos(angle)*radius,y,Math.sin(angle)*radius],i*3);
 dustSizes[i]=.028+Math.pow(random(),4)*.09;dustSeeds[i]=random()*TAU;
}
const axisDustGeo=new THREE.BufferGeometry();axisDustGeo.setAttribute('position',new THREE.BufferAttribute(dustPositions,3));axisDustGeo.setAttribute('aSize',new THREE.BufferAttribute(dustSizes,1));axisDustGeo.setAttribute('aSeed',new THREE.BufferAttribute(dustSeeds,1));
const dustMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,uniforms:{uTime:{value:0},uDpr:{value:renderer.getPixelRatio()}},vertexShader:`
attribute float aSize;attribute float aSeed;uniform float uTime;uniform float uDpr;varying float vLight;
void main(){vec3 p=position;float a=uTime*.16+.11*sin(p.y*.5+uTime*.3);mat2 rot=mat2(cos(a),-sin(a),sin(a),cos(a));p.xz=rot*p.xz;p.y+=.45*sin(uTime*.24+p.y*.18);p.x+=.13*sin(p.y*.7+uTime*.2);vec4 mv=modelViewMatrix*vec4(p,1.);gl_Position=projectionMatrix*mv;gl_PointSize=clamp(aSize*180.*uDpr/max(1.,-mv.z),.65,3.2*uDpr);vLight=.65+.35*sin(aSeed+uTime*.8);}`,fragmentShader:`
varying float vLight;void main(){float r=length(gl_PointCoord-.5)*2.;if(r>1.)discard;float core=exp(-r*r*8.),halo=exp(-r*r*4.)*.12;float alpha=(core+halo)*vLight;gl_FragColor=vec4(vec3(2.5,2.65,2.8),alpha*.75);}`});
const axisDust=new THREE.Points(axisDustGeo,dustMaterial);axisDust.frustumCulled=false;axisWorld.add(axisDust);
const chamberColor=new THREE.Color('#bfc3c4'),axisColor=new THREE.Color('#080f17'),lookTarget=new THREE.Vector3();
// Full-width editorial film replaces the procedural portrait.
const portraitWorld=new THREE.Group();scene.add(portraitWorld);portraitWorld.visible=false;
const beautyVideo=document.createElement('video');beautyVideo.src='./assets/beauty-scroll.mp4';beautyVideo.preload='auto';beautyVideo.muted=true;beautyVideo.playsInline=true;beautyVideo.setAttribute('playsinline','');beautyVideo.style.display='none';beautyVideo.setAttribute('aria-hidden','true');document.body.appendChild(beautyVideo);
// Hold the last decoded frame during seeks: a video element can temporarily
// lose HAVE_CURRENT_DATA, which must never flash the poster back on screen.
const beautyFrame=document.createElement('canvas');beautyFrame.width=1928;beautyFrame.height=1076;
const beautyContext=beautyFrame.getContext('2d',{alpha:false});
let beautyHasFrame=false,beautyDisplayedTime=0,beautyTargetTime=0;
const beautyTexture=new THREE.CanvasTexture(beautyFrame);beautyTexture.generateMipmaps=false;
function captureBeautyFrame(){
 if(beautyVideo.readyState<2||beautyVideo.seeking)return;
 beautyContext.drawImage(beautyVideo,0,0,beautyFrame.width,beautyFrame.height);
 beautyTexture.needsUpdate=true;beautyDisplayedTime=beautyVideo.currentTime;beautyHasFrame=true;
}
beautyVideo.addEventListener('loadeddata',captureBeautyFrame);
beautyVideo.addEventListener('seeked',captureBeautyFrame);
function seekBeautyFrame(time){
 // Coalesce input to one outstanding decode and quantize to source frames.
 beautyTargetTime=Math.round(time*24)/24;
 if(beautyVideo.readyState>=2&&!beautyVideo.seeking&&Math.abs(beautyVideo.currentTime-beautyTargetTime)>1/48){
  beautyVideo.currentTime=beautyTargetTime;
 }
}
beautyTexture.colorSpace=THREE.NoColorSpace;beautyTexture.minFilter=THREE.LinearFilter;beautyTexture.magFilter=THREE.LinearFilter;
const loader=new THREE.TextureLoader(),beautyPoster=loader.load('./assets/beauty-poster.jpg'),beautyDepth=loader.load('./assets/beauty-depth-atlas.png');beautyPoster.colorSpace=THREE.NoColorSpace;beautyDepth.colorSpace=THREE.NoColorSpace;beautyDepth.minFilter=THREE.LinearFilter;beautyDepth.generateMipmaps=false;
const beautyScene=new THREE.Scene(),beautyCamera=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
const beautyMaterial=new THREE.ShaderMaterial({transparent:true,depthTest:false,depthWrite:false,toneMapped:false,uniforms:{tFilm:{value:beautyTexture},tPoster:{value:beautyPoster},tDepth:{value:beautyDepth},uMix:{value:0},uReady:{value:0},uFrame:{value:0},uAspect:{value:innerWidth/innerHeight},uPointer:{value:new THREE.Vector2()}},vertexShader:`varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}`,fragmentShader:`
uniform sampler2D tFilm,tPoster,tDepth;uniform float uMix,uReady,uFrame,uAspect;uniform vec2 uPointer;varying vec2 vUv;
float depthAt(vec2 uv,float frame){float tile=floor(frame);vec2 cell=vec2(mod(tile,5.),4.-floor(tile/5.));vec2 inset=vec2(.5/512.,.5/288.);return texture2D(tDepth,(cell+clamp(uv,inset,1.-inset))/5.).r;}
void main(){float filmAspect=1928./1076.;vec2 uv;
if(uAspect<.8){uv=vec2(vUv.x,(vUv.y-.60)*filmAspect/uAspect+.5);}else{uv=(vUv-.5)*vec2(min(1.,uAspect/filmAspect),min(1.,filmAspect/uAspect))+.5;}
float inside=step(0.,uv.y)*step(uv.y,1.);uv=(uv-.5)*.975+.5;
float d=mix(depthAt(uv,floor(uFrame)),depthAt(uv,min(24.,floor(uFrame)+1.)),fract(uFrame));
vec2 offset=uPointer*(d-.28)*.008;uv=clamp(uv+offset,vec2(.001),vec2(.999));vec3 color=mix(texture2D(tPoster,uv).rgb,texture2D(tFilm,uv).rgb,uReady);
// A restrained bottom gradient keeps the unboxed editorial text readable.
color*=1.-.32*(1.-smoothstep(0.,.36,vUv.y));color=mix(vec3(.015,.021,.028),color,inside);
gl_FragColor=vec4(color,uMix);}`});
beautyScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),beautyMaterial));
beautyVideo.addEventListener('error',()=>{const box=document.querySelector('#error');box.hidden=false;box.textContent='The portrait film could not load. Please reload the page.';});
beautyVideo.load();
// Translucent pigment washes overlap into a continuous, feathered brushstroke.
const trailCount=640,trailLife=16,trailData=Array.from({length:trailCount},()=>({position:new THREE.Vector3(),born:-100,size:0,seed:0}));let trailCursor=0,lastTrailX=null,lastTrailY=null;
const washData=new Float32Array(trailCount*2),washGeometry=new THREE.PlaneGeometry(1,1);
washGeometry.setAttribute('aWash',new THREE.InstancedBufferAttribute(washData,2).setUsage(THREE.DynamicDrawUsage));
const trailMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,depthTest:false,uniforms:{uTime:{value:0}},vertexShader:`
attribute vec2 aWash;varying vec2 vUv;varying vec2 vWash;
void main(){vUv=uv;vWash=aWash;gl_Position=projectionMatrix*modelViewMatrix*instanceMatrix*vec4(position,1.);}`,fragmentShader:`
uniform float uTime;varying vec2 vUv;varying vec2 vWash;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+1.),f.x),f.y);}
void main(){
 float age=uTime-vWash.y;if(age<0.||age>16.)discard;
 vec2 p=(vUv-.5)*2.;float n=noise(p*4.+vWash.x*13.);
 float fine=noise(p*23.+vWash.x),r=length(p*vec2(1.,1.13));
 float edge=.72+(n-.5)*.26;float wet=1.-smoothstep(edge-.28,edge+.06,r);
 float rim=exp(-pow((r-edge+.10)*16.,2.))*.22;
 float fade=(1.-smoothstep(6.,16.,age))*smoothstep(0.,.12,age);
 float pigment=(wet*(.055+.07*n)+rim*.09)*(.72+.28*fine);
 vec3 color=mix(vec3(.31,.37,.40),vec3(.77,.82,.83),n*.65+fine*.15);
 gl_FragColor=vec4(color,pigment*fade);
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
}`});
const mouseTrail=new THREE.InstancedMesh(washGeometry,trailMaterial,trailCount);mouseTrail.instanceMatrix.setUsage(THREE.DynamicDrawUsage);mouseTrail.frustumCulled=false;mouseTrail.renderOrder=20;scene.add(mouseTrail);const trailDummy=new THREE.Object3D();
for(let i=0;i<trailCount;i++){trailDummy.scale.setScalar(0);trailDummy.updateMatrix();mouseTrail.setMatrixAt(i,trailDummy.matrix);}
addEventListener('pointermove',e=>{
 if(scrollSpin<3.8||portraitWorld.visible||reducedMotion.matches){lastTrailX=null;return;}
 const x=e.clientX,y=e.clientY;if(lastTrailX===null){lastTrailX=x;lastTrailY=y;}
 const distance=Math.hypot(x-lastTrailX,y-lastTrailY),steps=Math.min(48,Math.max(1,Math.ceil(distance/10))),birth=performance.now()/1000;
 camera.updateMatrixWorld();
 for(let n=0;n<steps;n++)for(let j=0;j<1;j++){
 const t=(n+1)/steps,nx=(lastTrailX+(x-lastTrailX)*t+(random()-.5)*13)/innerWidth*2-1,ny=1-(lastTrailY+(y-lastTrailY)*t+(random()-.5)*13)/innerHeight*2;
 const direction=new THREE.Vector3(nx,ny,.5).unproject(camera).sub(camera.position).normalize(),d=trailData[trailCursor];
 d.position.copy(camera.position).addScaledVector(direction,3.7+random()*.35);d.born=birth;d.size=.19+random()*.12;d.seed=random()*TAU;washData[trailCursor*2]=d.seed;washData[trailCursor*2+1]=birth;washGeometry.attributes.aWash.needsUpdate=true;trailCursor=(trailCursor+1)%trailCount;
 }lastTrailX=x;lastTrailY=y;
},{passive:true});
addEventListener('pointerleave',()=>lastTrailX=null);addEventListener('scroll',()=>lastTrailX=null,{passive:true});
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
let scrollTarget=0,scrollSpin=0,orbitScroll=0,scrollEnergy=0;const pointer=new THREE.Vector2(),pointerSmooth=new THREE.Vector2();
const chapters=[...document.querySelectorAll('.chapter')],chapterLinks=[...document.querySelectorAll('.chapters a')];
function readScroll(){const y=scrollY;let index=0;while(index<chapters.length-1&&y>=chapters[index+1].offsetTop)index++;const next=chapters[index+1];
if(index<4)scrollTarget=index+THREE.MathUtils.clamp((y-chapters[index].offsetTop)/((next?.offsetTop||y+innerHeight)-chapters[index].offsetTop),0,1);
else scrollTarget=4+(y-chapters[4].offsetTop)/innerHeight;
document.body.style.setProperty('--progress',y/Math.max(1,document.documentElement.scrollHeight-innerHeight));chapterLinks.forEach((a,i)=>a.setAttribute('aria-current',String(i===index)));}
addEventListener('scroll',readScroll,{passive:true});addEventListener('resize',readScroll);readScroll();
addEventListener('pointermove',e=>{pointer.set(e.clientX/innerWidth*2-1,e.clientY/innerHeight*2-1);},{passive:true});

const dummy=new THREE.Object3D();let elapsed=0,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,yaw=0,pitch=0,zoom=1,dragging=false,lastX=0,lastY=0;
document.querySelector('#clean').onclick=()=>document.body.classList.add('hidden-ui');
document.addEventListener('keydown',e=>{if(e.key.toLowerCase()==='h')document.body.classList.toggle('hidden-ui');if(e.code==='Space'&&e.target===document.body){e.preventDefault();paused=!paused;}if(e.key==='Escape')document.body.classList.remove('hidden-ui');});
renderer.domElement.addEventListener('dblclick',()=>document.body.classList.toggle('hidden-ui'));
renderer.domElement.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;lastY=e.clientY;renderer.domElement.setPointerCapture(e.pointerId);});renderer.domElement.addEventListener('pointermove',e=>{if(!dragging)return;yaw-=(e.clientX-lastX)*.006;pitch=THREE.MathUtils.clamp(pitch+(e.clientY-lastY)*.004,-.45,.65);lastX=e.clientX;lastY=e.clientY;});for(const event of ['pointerup','pointercancel'])renderer.domElement.addEventListener(event,()=>dragging=false);
function resize(){renderer.setSize(innerWidth,innerHeight);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();}addEventListener('resize',resize);
// Filmic finishing pass: restrained depth blur, highlight bloom, neutral silver grade.
const renderScale=renderer.getPixelRatio();
const renderTarget=new THREE.WebGLRenderTarget(innerWidth*renderScale,innerHeight*renderScale,{type:THREE.HalfFloatType});renderTarget.depthTexture=new THREE.DepthTexture(innerWidth*renderScale,innerHeight*renderScale);
const postScene=new THREE.Scene(),postCamera=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
const postMaterial=new THREE.ShaderMaterial({uniforms:{tColor:{value:renderTarget.texture},tDepth:{value:renderTarget.depthTexture},uFocus:{value:15},uBlurAmount:{value:1},uResolution:{value:new THREE.Vector2(innerWidth*renderScale,innerHeight*renderScale)}},vertexShader:`varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position,1.);}`,fragmentShader:`
uniform float uFocus,uBlurAmount;uniform sampler2D tColor;uniform sampler2D tDepth;uniform vec2 uResolution;varying vec2 vUv;
float distanceAt(vec2 p){float d=texture2D(tDepth,p).r;return .1*120.0/(120.0-d*119.9);}
void main(){vec3 base=texture2D(tColor,vUv).rgb;float distance=distanceAt(vUv);float blur=clamp(abs(distance-uFocus)*.09,0.,1.6);vec3 soft=vec3(0.);vec3 glow=vec3(0.);for(int i=0;i<12;i++){float a=float(i)*6.2831853/12.;vec2 dir=vec2(cos(a),sin(a))/uResolution;vec3 sampleColor=texture2D(tColor,vUv+dir*blur*1.6).rgb;soft+=sampleColor;glow+=max(texture2D(tColor,vUv+dir*5.).rgb-vec3(1.0),0.);}vec3 color=mix(base,soft/12.,.65*uBlurAmount)+glow/12.*.13;float lum=dot(color,vec3(.2126,.7152,.0722));color=mix(vec3(lum),color,.23);vec2 q=(vUv-.5)*vec2(1.,1.);float vignette=1.-.65*smoothstep(.2,.69,length(q));color*=vignette;float grain=fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5;color+=grain*.006;gl_FragColor=vec4(color,1.);
#include <tonemapping_fragment>
#include <colorspace_fragment>
}`});postScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),postMaterial));
addEventListener('resize',()=>{renderTarget.setSize(innerWidth*renderScale,innerHeight*renderScale);postMaterial.uniforms.uResolution.value.set(innerWidth*renderScale,innerHeight*renderScale);});
// Refract the completed composition, including the portrait, during chapter crossings.
const waterTarget=new THREE.WebGLRenderTarget(innerWidth*renderScale,innerHeight*renderScale);
waterTarget.texture.colorSpace=THREE.SRGBColorSpace;
const waterScene=new THREE.Scene();
const waterMaterial=new THREE.ShaderMaterial({depthTest:false,depthWrite:false,toneMapped:false,uniforms:{tScene:{value:waterTarget.texture},uProgress:{value:0},uStrength:{value:0},uAspect:{value:camera.aspect}},vertexShader:`varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}`,fragmentShader:`
uniform sampler2D tScene;uniform float uProgress,uStrength,uAspect;varying vec2 vUv;
void main(){
 vec2 p=(vUv-vec2(.5,.48))*vec2(uAspect,1.);float r=length(p);
 vec2 direction=p/max(r,.001);float front=uProgress*1.65;
 float ring=exp(-pow((r-front)*4.,2.));
 float wave=sin(r*30.-uProgress*24.)*ring;
 float swell=sin(r*12.-uProgress*12.)*.28;
 vec2 displacement=direction/vec2(uAspect,1.)*(wave+swell)*.024*uStrength;
 vec2 uv=clamp(vUv+displacement,vec2(.002),vec2(.998));
 vec3 color=texture2D(tScene,uv).rgb;
 float caustic=cos(r*30.-uProgress*24.)*ring*.045*uStrength;
 color+=caustic*vec3(.86,.94,1.);
 gl_FragColor=vec4(color,1.);
#include <colorspace_fragment>
}`});
waterScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),waterMaterial));
addEventListener('resize',()=>{waterTarget.setSize(innerWidth*renderScale,innerHeight*renderScale);waterMaterial.uniforms.uAspect.value=camera.aspect;});
let last=performance.now();function animate(now){requestAnimationFrame(animate);let dt=Math.min((now-last)/1000,.05);last=now;scrollSpin+=(scrollTarget-scrollSpin)*(1-Math.exp(-9*dt));if(!paused)elapsed+=dt;const phase=(elapsed%40)/40*TAU;
// A slower follow gives the surrounding rings a short, smooth coast after scrolling.
const motionAmount=reducedMotion.matches?.15:1;
orbitScroll+=(scrollSpin-orbitScroll)*(1-Math.exp(-3.2*dt));
const scrollImpulse=THREE.MathUtils.clamp((scrollTarget-scrollSpin)*3,-1,1);
scrollEnergy+=(scrollImpulse-scrollEnergy)*(1-Math.exp(-4*dt));
environmentGroup.rotation.z=elapsed*.045+orbitScroll*.95*motionAmount;
environmentGroup.rotation.y=.07*Math.sin(elapsed*.11)+Math.sin(orbitScroll*1.8)*.13*motionAmount;
environmentGroup.rotation.x=scrollEnergy*.045*motionAmount;
const gathering=THREE.MathUtils.smoothstep(scrollSpin,0,.85);
updateFormation(THREE.MathUtils.clamp(scrollSpin-1,0,2));
pointerSmooth.lerp(pointer,1-Math.exp(-3*dt));
liquid.rotation.y=-.14+elapsed*.095+scrollSpin*.75+pointerSmooth.x*.12+scrollEnergy*.14*motionAmount;
liquid.rotation.z=-.06+Math.sin(elapsed*.4)*.08+scrollEnergy*.09*motionAmount;
liquid.position.y=1.2+Math.sin(elapsed*.75)*.095;drops.position.copy(liquid.position);

const solid=THREE.MathUtils.smoothstep(gathering,.64,.98);
formedLoop.visible=solid>.001;formingMaterial.opacity=solid;formingMaterial.depthWrite=solid>.99;
const splashFade=1-THREE.MathUtils.smoothstep(gathering,.28,.88);fadingMaterial.opacity=splashFade;
for(const part of fluidParts){if(part.mesh.parent!==liquid)continue;part.mesh.visible=splashFade>.001;const scale=1-.28*gathering;part.mesh.scale.set(scale*(1+.012*Math.sin(elapsed*.6+part.phase)),scale,scale);part.mesh.position.y=2.7*(1-scale)+.035*Math.sin(elapsed*.45+part.phase)*(1-gathering);}
drops.visible=gathering<.999;drops.rotation.copy(liquid.rotation);
for(let i=0;i<count;i++){const d=data[i],target=particleTargets[i],drift=.13*Math.sin(elapsed*.65+d.p)*(1-gathering);
dummy.position.set(THREE.MathUtils.lerp(d.x+drift,target.x,gathering),THREE.MathUtils.lerp(d.y+drift*.6,target.y,gathering),THREE.MathUtils.lerp(d.z+drift*.4,target.z,gathering));
const size=d.s*(1-THREE.MathUtils.smoothstep(gathering,.87,1));const wobble=.035*Math.sin(elapsed*1.8+d.p);dummy.scale.set(size*(1-wobble*.5),size*(d.stretch+wobble),size*(1-wobble*.5));dummy.rotation.set(d.p,d.p*.7,Math.sin(d.p));dummy.updateMatrix();drops.setMatrixAt(i,dummy.matrix);}drops.instanceMatrix.needsUpdate=true;
const mobile=camera.aspect<.8,approach=THREE.MathUtils.smoothstep(scrollSpin,0,3),angle=yaw+pointerSmooth.x*.07;
const distance=(mobile?14.3:10.8)-approach*1.2;
const targetY=mobile?1.65:3.1,lookX=mobile?0:2.25;
camera.position.set(Math.sin(angle)*distance+lookX,-.2+approach*1.65+pitch*6-pointerSmooth.y*.24,Math.cos(angle)*distance);
camera.lookAt(lookX,targetY,0);camera.rotateZ(-.055+Math.sin(scrollSpin*2)*.025);
const entry=THREE.MathUtils.smootherstep(scrollSpin,3.2,4),orbit=THREE.MathUtils.clamp(scrollSpin-4,0,8.4);
axisWorld.visible=entry>.001;axisWorld.scale.setScalar(.01+.99*entry);
environmentGroup.visible=entry<.999;environmentGroup.scale.setScalar(1+entry*2.5);
liquid.visible=entry<.999;liquid.scale.setScalar(.77*(1-entry));drops.visible=drops.visible&&entry<.01;
scene.background.copy(chamberColor).lerp(axisColor,entry);scene.fog.color.copy(scene.background);scene.fog.density=THREE.MathUtils.lerp(.022,.035,entry);
document.body.classList.toggle('axis-mode',entry>.5);
const orbitAngle=orbit*2.1*motionAmount+elapsed*.045+pointerSmooth.x*.12;
const descent=.14+.72*THREE.MathUtils.smootherstep(orbit,0,8.4);

const pathFollow=spinePath.getPointAt(1-descent).multiplyScalar(.74).applyAxisAngle(new THREE.Vector3(0,1,0),elapsed*.09);
const followY=3+pathFollow.y;
const orbitRadius=mobile?11.8:7.1;
const axisCamera=new THREE.Vector3(pathFollow.x+Math.sin(orbitAngle)*orbitRadius,followY+.25-pointerSmooth.y*.25,pathFollow.z+Math.cos(orbitAngle)*orbitRadius);
camera.position.lerp(axisCamera,entry);lookTarget.set(lookX,targetY,0).lerp(new THREE.Vector3(pathFollow.x,followY,pathFollow.z),entry);camera.lookAt(lookTarget);camera.rotateZ((-.055+Math.sin(scrollSpin*2)*.025)*(1-entry));
spine.rotation.y=elapsed*.09;axisDust.rotation.y=-elapsed*.025;dustMaterial.uniforms.uTime.value=elapsed;
for(const card of cards){const a=card.phase-elapsed*.075-orbit*.4*motionAmount;card.group.position.set(Math.sin(a)*3.2,card.y+Math.sin(elapsed*.5+card.phase)*.16,Math.cos(a)*3.2);card.group.rotation.set(0,a,Math.sin(elapsed*.3+card.phase)*.035);}
const portraitStart=4+(chapters[5].offsetTop-chapters[4].offsetTop)/innerHeight;
const portraitEntry=THREE.MathUtils.smootherstep(scrollSpin,portraitStart-.9,portraitStart);
portraitWorld.visible=portraitEntry>.001;portraitWorld.scale.setScalar(.3+.7*portraitEntry);
axisWorld.visible=axisWorld.visible&&portraitEntry<.999;axisWorld.scale.multiplyScalar(1-portraitEntry*.98);axisWorld.position.y=-portraitEntry*6;
document.body.classList.toggle('portrait-mode',portraitEntry>.5);
const filmProgress=THREE.MathUtils.clamp((scrollSpin-portraitStart)/4,0,1);
const filmDuration=Number.isFinite(beautyVideo.duration)?beautyVideo.duration:8.041667;
const desiredTime=filmProgress*Math.max(0,filmDuration-1/24);
seekBeautyFrame(desiredTime);
beautyMaterial.uniforms.uMix.value=portraitEntry;beautyMaterial.uniforms.uReady.value=beautyHasFrame?1:0;
beautyMaterial.uniforms.uFrame.value=THREE.MathUtils.clamp(beautyDisplayedTime/Math.max(.1,filmDuration-1/24)*24,0,24);
beautyMaterial.uniforms.uAspect.value=camera.aspect;beautyMaterial.uniforms.uPointer.value.set(reducedMotion.matches?0:pointerSmooth.x,reducedMotion.matches?0:-pointerSmooth.y);
renderer.domElement.dataset.filmTime=beautyDisplayedTime.toFixed(2);
renderer.domElement.dataset.filmReady=String(beautyHasFrame);
mouseTrail.visible=entry>.8&&portraitEntry<.1;
if(mouseTrail.visible){const trailTime=now/1000;trailMaterial.uniforms.uTime.value=trailTime;
for(let i=0;i<trailCount;i++){const d=trailData[i],age=trailTime-d.born;
trailDummy.position.copy(d.position);trailDummy.quaternion.copy(camera.quaternion);trailDummy.rotateZ(d.seed);
const bloom=1+.22*THREE.MathUtils.smoothstep(age,0,5);
trailDummy.scale.setScalar(age>=0&&age<trailLife?d.size*bloom:0);trailDummy.updateMatrix();mouseTrail.setMatrixAt(i,trailDummy.matrix);}
mouseTrail.instanceMatrix.needsUpdate=true;}

postMaterial.uniforms.uFocus.value=camera.position.distanceTo(lookTarget);
postMaterial.uniforms.uBlurAmount.value=1-entry;
renderer.setRenderTarget(renderTarget);renderer.render(scene,camera);renderer.setRenderTarget(waterTarget);renderer.render(postScene,postCamera);if(portraitEntry>.001){renderer.autoClear=false;renderer.render(beautyScene,beautyCamera);renderer.autoClear=true;}
let rippleStrength=0,rippleProgress=0;
for(const boundary of [1,2,3,4,portraitStart]){
 const progress=THREE.MathUtils.clamp((scrollSpin-boundary+.85),0,1);
 const strength=Math.pow(Math.sin(progress*Math.PI),2);
 if(strength>rippleStrength){rippleStrength=strength;rippleProgress=progress;}
}
waterMaterial.uniforms.uProgress.value=rippleProgress;
waterMaterial.uniforms.uStrength.value=reducedMotion.matches?0:rippleStrength;
renderer.setRenderTarget(null);renderer.render(waterScene,postCamera);}

requestAnimationFrame(animate);
window.addEventListener('error',e=>{const box=document.querySelector('#error');box.hidden=false;box.textContent='Unable to render the scene: '+e.message;});
