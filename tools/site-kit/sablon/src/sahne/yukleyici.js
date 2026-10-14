// Yükleyici % sayacı: LoadingManager ilerlemesi → yumuşatılmış, geri gitmeyen 000–100 sayaç; 100'e varınca giris() (giriş koreografisi).
import { LoadingManager } from 'three';
import gsap from 'gsap';

// enAz (sn): önbellekte yükleme anında biter → sayaç görünmeden perde açılırdı; sayaç en az bu sürede 100'e varır.
export function yukleyici(el, giris, { enAz = 2 } = {}) {
  const m = new LoadingManager();
  const o = { p: 0 };
  const t0 = performance.now();
  let acildi = false; // sonradan aynı yöneticiye eklenen varlık onLoad'u yeniden tetikler; giriş bir kez
  const ac = () => { if (!acildi) { acildi = true; giris(); } };
  // sayaç rakamları kilometre sayacı gibi dikey kayar: her basamak 0–9+0 şeridi, üst basamak alt basamak 9→0 geçerken birlikte döner
  const serit = '<span style="display:inline-block;height:1em;overflow:hidden;vertical-align:top"><span style="display:block;line-height:1">' + [...'01234567890'].join('<br>') + '</span></span>';
  el.innerHTML = serit.repeat(3); // sabit işaretleme, dış girdi yok
  const seritler = [...el.children].map((s) => s.firstChild);
  const yaz = () => seritler.forEach((s, i) => {
    const b = 10 ** (2 - i); // basamak ağırlığı 100/10/1; birler sürekli, üstler alt basamak b-1'i aşınca birlikte kayar
    s.style.transform = `translateY(${-((Math.floor(o.p / b) % 10) + Math.max(0, (o.p % b) - (b - 1))) * (100 / 11)}%)`;
  });
  yaz();
  const ilerle = (p, sure) =>
    gsap.to(o, { p: Math.max(o.p, p), duration: sure ?? 0.8, ease: sure ? 'power1.inOut' : 'power2.out', overwrite: true, onUpdate: yaz, onComplete: sure ? ac : undefined });
  m.onProgress = (_, n, top) => ilerle((n / top) * 99);
  m.onLoad = () => ilerle(100, Math.max(0.5, enAz - (performance.now() - t0) / 1000));
  return m;
}
