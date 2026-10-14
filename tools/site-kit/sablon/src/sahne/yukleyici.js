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
  const yaz = () => (el.textContent = String(Math.round(o.p)).padStart(3, '0'));
  const ilerle = (p, sure) =>
    gsap.to(o, { p: Math.max(o.p, p), duration: sure ?? 0.8, ease: sure ? 'power1.inOut' : 'power2.out', overwrite: true, onUpdate: yaz, onComplete: sure ? ac : undefined });
  m.onProgress = (_, n, top) => ilerle((n / top) * 99);
  m.onLoad = () => ilerle(100, Math.max(0.5, enAz - (performance.now() - t0) / 1000));
  return m;
}
