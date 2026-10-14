// RT kompozit sahne geçişi: A ve B ayrı RT'ye, tam ekran dörtgen mix(A, B, gürültü eşiği); eşik kenarında sıcak çekirdek + hale + kıvılcım, UV kırılması ve kromatik ayrışma. t=0/1'de tek sahne.
import * as T from 'three';

const VERT = 'varying vec2 v; void main(){ v = uv; gl_Position = vec4(position.xy, 0., 1.); }';
const FRAG = `uniform sampler2D a, b; uniform float t, oran; uniform vec3 kor; varying vec2 v;
float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float n(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  return mix(mix(h(i), h(i + vec2(1, 0)), f.x), mix(h(i + vec2(0, 1)), h(i + 1.), f.x), f.y); }
float fbm(vec2 p){ float s = 0., k = .5; for (int i = 0; i < 5; i++){ s += k * n(p); p *= 2.; k *= .5; } return s; }
vec3 al(sampler2D s, vec2 p, vec2 d){ return vec3(texture2D(s, p + d).r, texture2D(s, p).g, texture2D(s, p - d).b); }
void main(){
  // merkezden açılan portal: en-boy düzeltmeli yarıçap + fbm yırtığı; adacık değil tek tutarlı yanan halka
  vec2 q = (v - .5) * vec2(oran, 1.);
  // d5 organik ivme: yırtık t ile kayan çarpık fbm (yalnız büyüyen sabit desen değil) + yavaş açılım, ortada atılım, sonda yerleşme
  float g = length(q) * .78 + fbm(v * vec2(6., 4.) + fbm(v * 3. + t) * .8 + vec2(0., t * 1.2)) * .38;
  float e = mix(-.12, 1.12, mix(t, t * t * (3. - 2. * t), .65));
  float m = smoothstep(g - .015, g + .015, e);
  float d = e - g;
  float cekirdek = smoothstep(.012, 0., abs(d));
  // d3: geniş/parlak hale "yanan kâğıt" okunuyordu → ince ışık, enerji kırılma + kromatik ayrışmaya
  float hale = smoothstep(.06, 0., abs(d)) * (.6 + .4 * fbm(v * 40. + t * 3.));
  float kirilma = smoothstep(.16, 0., abs(d));
  float kivilcim = step(.993, h(floor(v * vec2(420., 260.)))) * smoothstep(.12, 0., abs(d - .04));
  vec2 kay = normalize(q + 1e-4) * .045 * kirilma * sign(d);
  vec2 kr = normalize(q + 1e-4) * .018 * kirilma;
  vec3 col = mix(al(a, v + kay, kr), al(b, v - kay, kr), m) + kor * (hale * .45 + kivilcim * 2.5) + mix(kor, vec3(1.), .6) * cekirdek * 1.6;
  // d5 sis: halka çevresinde dışa sürüklenen duman bandı (A tarafında geniş), halkadan aydınlanır
  float r = length(q);
  vec2 yon = q / (r + 1e-4);
  float sis = smoothstep(mix(.1, .3, step(d, 0.)), 0., abs(d)) * smoothstep(.35, .75, fbm(q * 5. - yon * t * 2.5));
  col = mix(col, col * .5 + kor * .18, sis * .6) + kor * sis * smoothstep(.1, 0., abs(d)) * .3;
  // d5 parçacık: kutupsal hücrelerde halkadan dışa uçan köz tanecikleri; uzaklaştıkça söner
  vec2 hc = vec2(atan(q.y, q.x) * 9.55, r * 34. - t * 20.);
  vec2 hi = floor(hc);
  float tane = step(.88, h(hi));
  float nokta = smoothstep(.16, .04, length(fract(hc) - .5 - (vec2(h(hi + 7.), h(hi + 3.)) - .5) * .5));
  col += mix(kor, vec3(1., .9, .7), .4) * tane * nokta * smoothstep(.32, 0., -d) * step(d, .02) * 2.2;
  gl_FragColor = vec4(col, 1.);
  #include <tonemapping_fragment>
  #include <colorspace_fragment>
}`;

export function gecis(r, kor = 0xff8a3d) {
  const ra = new T.WebGLRenderTarget(1, 1, { type: T.HalfFloatType });
  const rb = ra.clone();
  const mat = new T.ShaderMaterial({
    uniforms: { a: { value: ra.texture }, b: { value: rb.texture }, t: { value: 0 }, oran: { value: 1 }, kor: { value: new T.Color(kor) } },
    vertexShader: VERT, fragmentShader: FRAG, depthTest: false,
  });
  const qs = new T.Scene().add(new T.Mesh(new T.PlaneGeometry(2, 2), mat));
  const qk = new T.Camera();
  const boyut = new T.Vector2();
  const bas = (s, k, rt) => { r.setRenderTarget(rt); r.render(s, k); };
  return (sA, kA, sB, kB, t) => {
    if (t <= 0 || t >= 1) return bas(t <= 0 ? sA : sB, t <= 0 ? kA : kB, null);
    r.getDrawingBufferSize(boyut);
    if (ra.width !== boyut.x || ra.height !== boyut.y) { ra.setSize(boyut.x, boyut.y); rb.setSize(boyut.x, boyut.y); }
    bas(sA, kA, ra);
    bas(sB, kB, rb);
    mat.uniforms.t.value = t;
    mat.uniforms.oran.value = boyut.x / boyut.y;
    bas(qs, qk, null);
  };
}
