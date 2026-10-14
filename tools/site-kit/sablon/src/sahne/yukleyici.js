// Yükleyici % sayacı: LoadingManager ilerlemesi → yumuşatılmış, geri gitmeyen 000–100 sayaç; 100'e varınca giris() (giriş koreografisi).
import { LoadingManager } from 'three';
import gsap from 'gsap';

export function yukleyici(el, giris) {
  const m = new LoadingManager();
  const o = { p: 0 };
  const yaz = () => (el.textContent = String(Math.round(o.p)).padStart(3, '0'));
  const ilerle = (p, bitti) =>
    gsap.to(o, { p: Math.max(o.p, p), duration: bitti ? 0.5 : 0.8, ease: 'power2.out', overwrite: true, onUpdate: yaz, onComplete: bitti ? giris : undefined });
  m.onProgress = (_, n, top) => ilerle((n / top) * 99);
  m.onLoad = () => ilerle(100, true);
  return m;
}
