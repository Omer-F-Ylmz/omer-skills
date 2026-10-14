// GPGPU parçacık (buhar/telve tozu): konum dokusu GPUComputationRenderer'da girdaplı yükselen alanla ilerler, ömür bitince kaynağa döner.
// Çizim: Points, boyut 1/derinlik, ömür boyu sin solması, derinlik sisi; additive.
import * as T from 'three';
import { GPUComputationRenderer } from 'three/addons/misc/GPUComputationRenderer.js';

const ORTAK = `float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
float omur(vec2 p){ return 3. + 2. * h(p); }`;
const AKIS = `uniform float t, dt; uniform vec3 kaynak; ${ORTAK}
void main(){
  vec2 uv = gl_FragCoord.xy / resolution.xy;
  vec4 p = texture2D(konum, uv);
  vec3 q = p.xyz - kaynak;
  vec3 v = vec3(sin(q.y * 2.1 + t) + .6 * cos(q.z * 3.3 - t), 1.1 + .4 * sin(q.x * 2.7 + t * .7), cos(q.y * 1.7 - t * 1.3) + .6 * sin(q.x * 3.1));
  p.xyz += v * vec3(.18 * (.3 + q.y), .55, .18 * (.3 + q.y)) * dt;
  p.w += dt;
  if (p.w > omur(uv)) p = vec4(kaynak + vec3(h(uv + t) - .5, 0., h(uv - t) - .5) * .45, 0.);
  gl_FragColor = p;
}`;
const VERT = `uniform sampler2D konum; uniform float boy; attribute vec2 ref; varying float a; ${ORTAK}
void main(){
  vec4 p = texture2D(konum, ref);
  vec4 mv = modelViewMatrix * vec4(p.xyz, 1.);
  gl_Position = projectionMatrix * mv;
  a = sin(3.1416 * clamp(p.w / omur(ref), 0., 1.)) * exp(-(-mv.z) * .06);
  gl_PointSize = boy / -mv.z;
}`;
const FRAG = `uniform vec3 renk; varying float a;
void main(){ float r = length(gl_PointCoord - .5); if (r > .5) discard; gl_FragColor = vec4(renk, a * (1. - 2. * r) * .5); }`;

export function parcacik(r, { n = 256, kaynak = [0, 1, 0], renk = 0xfff1e0, boy = 30 } = {}) {
  const g = new GPUComputationRenderer(n, n, r);
  const d0 = g.createTexture();
  const d = d0.image.data;
  for (let i = 0; i < d.length; i += 4) {
    d[i] = kaynak[0] + (Math.random() - 0.5) * 0.6;
    d[i + 1] = kaynak[1] + Math.random() * 2.5;
    d[i + 2] = kaynak[2] + (Math.random() - 0.5) * 0.6;
    d[i + 3] = Math.random() * 3;
  }
  const v = g.addVariable('konum', AKIS, d0);
  g.setVariableDependencies(v, [v]);
  Object.assign(v.material.uniforms, { t: { value: 0 }, dt: { value: 0 }, kaynak: { value: new T.Vector3(...kaynak) } });
  const hata = g.init();
  if (hata) throw new Error(hata);
  const ref = new Float32Array(n * n * 2);
  for (let i = 0; i < n * n; i++) ref.set([((i % n) + 0.5) / n, (Math.floor(i / n) + 0.5) / n], i * 2);
  const geo = new T.BufferGeometry();
  geo.setAttribute('position', new T.BufferAttribute(new Float32Array(n * n * 3), 3));
  geo.setAttribute('ref', new T.BufferAttribute(ref, 2));
  const mat = new T.ShaderMaterial({
    uniforms: { konum: { value: null }, boy: { value: boy * r.getPixelRatio() }, renk: { value: new T.Color(renk) } },
    vertexShader: VERT, fragmentShader: FRAG, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
  });
  const nesne = new T.Points(geo, mat);
  nesne.frustumCulled = false;
  return {
    nesne,
    adim(t, dt) {
      v.material.uniforms.t.value = t;
      v.material.uniforms.dt.value = Math.min(dt, 0.05);
      g.compute();
      mat.uniforms.konum.value = g.getCurrentRenderTarget(v).texture;
    },
  };
}
