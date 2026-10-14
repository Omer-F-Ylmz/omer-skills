// TELVE-TOKEN-1 M4: sıvı malzemesinin onBeforeCompile parçaları (fincan.js enjekte eder); GLSL değişikliği yalnız burada.
export const SIVI_ORTAK = /* glsl */`
uniform vec3 uC, uL, uW; uniform float uPen, uH, uR, uF, uT, uPar, uKar, uRimY, uRimR, uTep; uniform vec4 uKat;
uniform sampler2D uYuk, uGec, uSan; uniform vec3 uRenk[4];
#ifdef KESIT
uniform vec4 uKes4; // kesit düzlemi (normal, sabit)
#endif
varying vec3 vWp;
vec3 lin(vec3 c) { return pow(c, vec3(2.2)); }
vec2 h22(vec2 p) { p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3))); return fract(sin(p) * 43758.5453); }
float worley(vec2 p) { vec2 i = floor(p), f = fract(p); float d = 1.;
  for (int y = -1; y <= 1; y++) for (int x = -1; x <= 1; x++) { vec2 o = vec2(x, y); vec2 r = o + h22(i + o) - f; d = min(d, dot(r, r)); }
  return sqrt(d); }
float g31(vec3 p) { return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453); }
float gur(vec3 p) { vec3 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  return mix(mix(mix(g31(i), g31(i + vec3(1, 0, 0)), f.x), mix(g31(i + vec3(0, 1, 0)), g31(i + vec3(1, 1, 0)), f.x), f.y),
             mix(mix(g31(i + vec3(0, 0, 1)), g31(i + vec3(1, 0, 1)), f.x), mix(g31(i + vec3(0, 1, 1)), g31(i + 1.), f.x), f.y), f.z); }
float fbm(vec3 p) { return .5 * gur(p) + .25 * gur(p * 2.03) + .125 * gur(p * 4.1) + .125 * gur(p * 8.3); }
float fbm2(vec3 p) { return (2. * gur(p) + gur(p * 2.03)) / 3.; } // 2 oktav: sınır yumuşak dalga, yırtık kâğıt değil (E8)
vec2 akisK(vec2 xz) { float c = cos(uF), s = sin(uF); return vec2(c * xz.x - s * xz.y, s * xz.x + c * xz.y) / uR; } // dünya → sıvı çerçevesi
vec2 dunyaY(vec2 g) { float c = cos(uF), s = sin(uF); return vec2(c * g.x + s * g.y, -s * g.x + c * g.y); }
vec2 kuv(vec2 p) { float l = length(p); return (l > .985 ? p * (.985 / l) : p) * .5 + .5; }
#ifdef BARDAK
float kopuk(vec2 xz) { vec2 p = akisK(xz); return clamp((uH - uKat.z) / .08, 0., 1.) * (.02 * (1. - dot(p, p)) + .014 * fbm(vec3(p * 3.2, 1.7))); } // köpük kubbesi + düzensiz tepe
#else
float kopuk(vec2 xz) { return 0.; }
// kalbin işaretli uzaklığı (hp birimi): iki daire lob (merkez (±.48, .63), r .55) ∪ uçtan (0, −1.15) loba teğet 65° V,
// V üstten lob merkezinden geçen dikmeyle ve yarık yüksekliğiyle kırpılır (yarığı doldurmaz). Eski iq kalbi 90° uçlu
// 45° kareydi; V'yi dışa büken x/(1+.2 sin) V dalını lob dairesinin dışına taşırıp yanlarda dikey basamak (tost dilimi)
// bırakıyor, ucu körleştiriyordu (F2)
float kalpSd(vec2 p) {
  p.x = abs(p.x);
  vec2 c = vec2(.48, .63), u = vec2(.5365, .8439); // u: V kenarı yönü (uçtan teğet noktasına)
  float t = clamp(dot(p - vec2(0., -1.15), u) / 1.76, 0., 1.); // V kenarında uç → teğet noktası; süt kalbi gibi hafif dışa bombe, uç sivri kalır
  float dv = max(max(dot(p - vec2(0., -1.15), vec2(u.y, -u.x)) - .04 * sin(3.1416 * t), dot(p - c, u)), p.y - .8985);
  return min(length(p - c) - .55, dv);
}
#endif
// tepe ağın üst diskinin (uTep) 4 mm altında yumuşak doyar (yumuşak min, k .016): duvardaki dalga tepesi diski aşınca
// yüzey disk düzleminde düz kirişle kesilip kama çiziyordu (F1); doyunca duvar kesişimi her zaman menisküslü arka yüz kesiği
float yuks(vec2 xz) { float h = texture(uYuk, kuv(akisK(xz))).r + uPar * (dot(xz, xz) - .5 * uR * uR) + kopuk(xz), c = uTep - uH - .004;
  return min(h, c) - pow(max(.016 - abs(h - c), 0.), 2.) / .064; }
// hacim: koyu (emici) katman kenarda amber geçirir, süt/köpük saçıcı → neredeyse opak
vec3 sigma(vec3 c) { return mix(vec3(16., 25., 42.), vec3(70.), smoothstep(.02, .5, dot(c, vec3(.2126, .7152, .0722)))); }
// katmanlar: ara yüz yüzeyin gecikmeli kopyasıyla dalgalanır, sınırda fbm bulutu (döküm sırasında mermerleşir)
float katG = 1.; // kesit kapağında 0: sınır gürültüsü yok, geçiş geniş (R2d C3c)
vec3 katRenk(float h, vec2 xz, out vec3 sg) {
  vec2 p = akisK(xz);
  vec4 lg = texture(uGec, kuv(p));
  // gürültü dünya biriminde izotrop ve h'ye göre eğimi < 1: eski p·2.2 / h·34 oranında sınır aynı yükseklikte
  // birkaç kez kesişip yatay sürtme çizgileri çiziyordu (T6)
  // karışımda eski genlik·h-frekansı (.1·(10+5)) eğimi 1'i aşıyordu → sınır kendini birkaç kez kesip yırtık kâğıt çiziyordu (E8)
  float n = fbm2(vec3(p * uR * 10. + h * uKar * 2.5, h * 5. - uT * (.05 + .6 * uKar))) - .5, w = fwidth(h) + .02 * (1. - katG);
  n *= katG; lg *= katG;
  float b1 = uKat.x + lg.r * 3. + n * (.04 + .04 * uKar), b2 = uKat.y + lg.g * 2.2 + n * .03, b3 = uKat.z + lg.g * 1.2 + n * .012;
  vec3 c = mix(uRenk[0], uRenk[1], smoothstep(b1 - .028 - w, b1 + .028 + w, h));
  c = mix(c, mix(uRenk[0], uRenk[1], .5), .3 * exp(-(h - b1) * (h - b1) / .0012) * fbm2(vec3(p * uR * 14., h * 14. + 3.))); // ince karışım bulutu
  c = mix(c, uRenk[2], smoothstep(b2 - .012 - w, b2 + .008 + w, h));
  c = mix(c, uRenk[3], smoothstep(b3 - .005 - w, b3 + .005 + w, h));
  sg = sigma(c);
  return c;
}
`;
export const SIVI_KES = /* glsl */`
vec3 rel = vWp - uC;
float ust = rel.y - uH - yuks(rel.xz), da = 0., dikey = fwidth(rel.y); // kapak (yatay disk) üzerinde y sabit → 0
#ifdef DANTEL
// yüzeyin üstü: yalnız duvardaki köpük izi, ayrı saydam geçişte (alfa karışımı) — ince, yumuşak kavisli halkalar + seyrek damla izi.
// Eski: opak + discard, değer gürültüsü step/dar smoothstep ile eşiklenince kafes hücresine yapışıp kısa yatay/dikey çizgi
// parçaları (tuğla deseni) ve gölgesiz beyaz kenar bırakıyordu (E1, E7)
if (ust <= 0.) discard;
vec2 pk = akisK(rel.xz);
float lp = length(pk), iz = texture(uGec, kuv(pk / max(lp, 1e-3) * .97)).b - (rel.y - uH);
// kapakta (ağın üst diski, lp < .97) iz yok: eski worley(atan·22, y) orada merkezden kenara ışın + ±π dikişi çiziyordu (T1)
if (lp > .97 && dikey > 1e-6 && iz > 0.) {
  vec3 dk = vec3(pk / lp, 0.);                                     // açı birim çemberde 3B gürültüyle → dikişsiz
  float x = (rel.y + uT * .004) * 28. + 1.5 * gur(dk * 2.5 + 3.1); // halka: düşük frekanslı açısal kayma → yumuşak kavis, yavaşça süzülür
  float hal = exp(-pow((fract(x) - .5) / max(.07, fwidth(x)), 2.)) * smoothstep(.3, .8, gur(dk * 4. + vec3(0., 0., floor(x))));
  float s = atan(dk.y, dk.x) * 7.6394, hc = g31(vec3(floor(s), 1.7, 0.)), d0 = .006 + .03 * fract(hc * 7.); // 48 sütun: sınır ±π'de, dikiş yok
  float dam = step(hc, .22) * exp(-pow((fract(s) - .3 - .4 * fract(hc * 13.)) / (.06 * (.4 + .6 * clamp(iz / d0, 0., 1.))), 2.)) * smoothstep(d0 + .002, d0 - .001, iz);
  da = max(hal * .32, dam * .4) * smoothstep(0., .004, iz) * (1. - smoothstep(.4, 1., ust / (ust + iz)));
}
if (da < .004) discard;
#else
float kapA = clamp(.5 - ust / max(fwidth(ust), 1e-6), 0., 1.); // kesik kenar: alfa→kapsama (MSAA) ile yumuşak, merdiven yok
if (kapA <= 0.) discard;
#endif
bool dantel = da > 0.;
// arka yüz = yüzey kapağı: ışını eğri yüzeyle kesip oradan boya. Ağın üst diski (ön yüz, dolum + 6 mm) da kapak: çalkalanmada
// duvardaki tepe diski aşınca disk yan rengiyle (amber) eğik düzlemin düz kirişinde kesilen bir kama çiziyordu (F1)
#ifdef BARDAK
bool kapak = !dantel && (!gl_FrontFacing || abs(normalize(cross(dFdx(vWp), dFdy(vWp))).y) > .5);
#else
bool kapak = !dantel; // porselen fincanda sıvının yanı hiç görünmez: görünen her parça (üst disk, ağız boşluğu) yüzeydir
#endif
vec3 yon = normalize(vWp - cameraPosition);
bool kes = false;
#ifdef KESIT
// R2c F3: kesik sıvının arka yüzü düzlemin ardından görünür → ışını kesit düzlemiyle kes; yüzeyin altındaysa kesit kapağı
vec3 kp = cameraPosition + yon * (-(dot(uKes4.xyz, cameraPosition) + uKes4.w) / dot(uKes4.xyz, yon));
if (!gl_FrontFacing && !dantel && kp.y - uC.y < uH + yuks(kp.xz - uC.xz)) { kes = true; kapak = false; }
#endif
vec3 isa = cameraPosition + yon * ((uC.y + uH - cameraPosition.y) / yon.y);
for (int i = 0; i < 2; i++) isa = cameraPosition + yon * ((uC.y + uH + yuks(isa.xz - uC.xz) - cameraPosition.y) / yon.y);
vec3 yer = isa - uC;
float rn = length(yer.xz) / uR;
vec2 yp = akisK(yer.xz);
float golge = smoothstep(uRimR * .9, uRimR * 1.1, length(yer.xz + uL.xz * ((uRimY - yer.y) / max(uL.y, .05))));
vec3 gec = vec3(0.);
`;
export const SIVI_RENK = /* glsl */`
#ifdef BARDAK
  vec3 sg, sg2;
  vec2 yh = normalize(yon.xz);
  float rw = length(rel.xz), dx = rel.x * yh.y - rel.z * yh.x, dd = abs(dx), e = clamp(dd / max(rw, 1e-4), 0., 1.), kb = smoothstep(.8, .97, e);
  // kenar bandı: silindir mercek yatayda kırar → siluete yakın desen sıkışır (açı arkaya kayar) + ince parlak iç yansıma çizgisi
  float ka = kb * .5 * sign(dx);
  vec3 yan = katRenk(rel.y, mat2(cos(ka), sin(ka), -sin(ka), cos(ka)) * rel.xz, sg);
  // Beer-Lambert: görüş ışınının sıvı silindirindeki yolu → kenarda ince (açık, fon geçer), ortada kalın (koyu)
  vec3 T = exp(-sg * 2. * sqrt(max(rw * rw - dd * dd, 0.)) / max(length(yon.xz), .3));
  gec = lin(vec3(.89, .86, .82)) * T * .9 + lin(vec3(.95, .93, .9)) * smoothstep(.9, .99, e) * .3;
  yan *= (1. - T) * (1. - .25 * kb * (1. - smoothstep(.93, .99, e)));
  vec3 yuz = katRenk(uH - .004, yer.xz, sg2) * (1. - .07 * smoothstep(.3, .08, worley(yp * 38.)) - .05 * smoothstep(.25, .05, worley(yp * 90.)));
  // yalnız espresso varken üst crema: altın-fındık, merkez açık → kenar koyu + ince, düşük kontrastlı kaplan çizgisi (E4: eski
  // fbm·13 dar eşikle iri koyu benek = leopar)
  float krema = step(uH, uKat.x);
  // F4: merkez daha az doygun, degrade geniş (eski dar smoothstep(.05) merkezde turuncu 'glow' topluyordu); benek ince ve ~⅓ kontrast
  vec3 kr = mix(lin(vec3(.69, .51, .32)), lin(vec3(.42, .26, .13)), smoothstep(-.2, 1.1, rn));
  kr *= 1. - .018 * smoothstep(.4, .75, fbm2(vec3(yp.x * 70., yp.y * 22., uT * .06)));
  yuz = mix(yuz, kr * (1. + .015 * smoothstep(.22, .04, worley(yp * 110.))), krema);
  vec3 dr = yuz; // köpük izi rengi: üst katman
  float kalp = 0.;
  golge *= .35; // cam duvar ışığı az keser
#else
  vec4 am = texture(uSan, kuv(yp)); // advekte harita: desen ve crema benekleri akışla gerilir
  vec2 m = am.rg;
  vec2 hp = vec2(m.x, -m.y) * 3.3 + vec2(0., .26); // uç kameraya (dinlenme açısında)
  hp += .025 * vec2(sin(m.y * 7. + 1.3), cos(m.x * 6.));
  // tam uzaklık (×2: hp birimi) → tekil nokta yok; uçtaki koyu "bıyık" eski "uçtan çekilen çizgi" çarpanıydı, kaldırıldı (E3).
  // Kenar: piksel genişliği + hafif dağılma (T3)
  float sd = kalpSd(hp);
  float kw = max(.008 + am.b * .012, min(fwidth(sd), .02));
  float kalp = 1. - smoothstep(-kw, kw, sd);
#ifdef TURK
  kalp = 0.; // Türk kahvesi: desen yok, yalnız köpük halesi
#endif
  float hale = 1. - smoothstep(-.01, .06 + am.b * .06, sd), mr = length(m);
  vec3 yuz = mix(lin(vec3(.30, .17, .08)), lin(vec3(.58, .41, .27)), hale * .4);
  yuz = mix(yuz, lin(vec3(.95, .92, .86)), kalp);
  yuz = mix(yuz, lin(vec3(.19, .10, .04)), smoothstep(.70, 1., mr) * (1. - kalp));
  float b = worley(m * 42.), b2 = worley(m * 13. + 7.);
  yuz *= 1. - .10 * smoothstep(.30, .10, b) - .25 * smoothstep(.22, .06, b2) * smoothstep(.5, .95, mr);
#ifdef TURK
  // R2e C1b: ince fındık köpük, merkezden kenara tek yumuşak geçiş (hale + kenar halkası iki tonlu bant çiziyordu)
  yuz = mix(lin(vec3(.60, .44, .30)), lin(vec3(.36, .22, .12)), smoothstep(-.2, 1.3, mr)) * (1. - .08 * smoothstep(.3, .1, b));
#endif
  vec3 yan = lin(vec3(.30, .16, .07)), dr = lin(vec3(.74, .63, .49));
#endif
// köpük izi yarı saydam film (alfa = da, duvarın üstüne karışır), ağız gölgesi analitik (sıvı ağı gölge almaz)
#ifdef KESIT
if (kes) { vec3 sk; katG = 0.; yan = katRenk(kp.y - uC.y, kp.xz - uC.xz, sk); gec = vec3(0.); } // kesit: katmanlar opak, kırılmasız
#endif
diffuseColor.rgb = dantel ? dr * mix(1., .6, smoothstep(uRimR * .9, uRimR * 1.1, length(rel.xz + uL.xz * ((uRimY - rel.y) / max(uL.y, .05)))))
    : kapak ? yuz * mix(1., .62, golge) * mix(1., .9, smoothstep(.96, 1.02, rn)) : yan;
#ifdef DANTEL
diffuseColor.a = da;
#else
diffuseColor.a = kapA;
#endif
if (kapak || dantel) gec = vec3(0.);
`;
