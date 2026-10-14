// Tek sayfa iskeleti (TELVE R2a'dan): Lenis + ScrollTrigger senkronu, alt ilerleme dilimleri, bölüm sahnesi yükleyici.
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';

gsap.registerPlugin(ScrollTrigger);
const AZ = matchMedia('(prefers-reduced-motion: reduce)').matches;

// reduced-motion'da Lenis yok: yerel scroll, bağlantılar anında atlar
if (!AZ) {
  const lenis = new Lenis({ autoRaf: false, anchors: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}

// ilerleme: dilim bölümün ilerlemesiyle dolar; etkin bölüm aria-current
for (const a of document.querySelectorAll<HTMLAnchorElement>('[data-dilim]')) {
  ScrollTrigger.create({
    trigger: `#${a.dataset.dilim}`,
    start: 'top center',
    end: 'bottom center',
    onUpdate: (s) => a.style.setProperty('--p', s.progress.toFixed(3)),
    onToggle: (s) => (s.isActive ? a.setAttribute('aria-current', 'step') : a.removeAttribute('aria-current')),
  });
}

// sahne yükleyici: bolum/<id>.ts bir ekran kala ayrı dinamik parça olarak yüklenir; yüklenemezse (WebGL yok) poster kalır
type Sahne = { ilerle: (p: number) => void; calis: (acik: boolean) => void };
const moduller = import.meta.glob<{ kur: (cv: HTMLCanvasElement) => Promise<Sahne> }>('./bolum/*.ts');
for (const cv of document.querySelectorAll<HTMLCanvasElement>('[data-sahne]')) {
  const id = `#${cv.dataset.sahne}`;
  const yukle = moduller[`./bolum/${cv.dataset.sahne}.ts`];
  if (!yukle) continue;
  ScrollTrigger.create({
    trigger: id,
    start: 'top bottom+=100%',
    once: true,
    onEnter: () =>
      void yukle()
        .then((m) => m.kur(cv))
        .then((s) => {
          cv.classList.add('hazir');
          const o = { p: 0 };
          // scrub 1.2 karşılığı; reduced-motion'da bölüm pozuna 0.3 s
          const git = (p: number) =>
            gsap.to(o, { p, duration: AZ ? 0.3 : 1.2, ease: 'power3.out', overwrite: true, onUpdate: () => s.ilerle(o.p) });
          ScrollTrigger.create({ trigger: id, start: 'top top', end: 'bottom bottom', onUpdate: (t) => git(AZ ? Math.round(t.progress) : t.progress) });
          const gor = ScrollTrigger.create({ trigger: id, start: 'top bottom', end: 'bottom top', onToggle: (t) => s.calis(t.isActive) });
          s.calis(gor.isActive);
        })
        .catch((e) => console.error(e)),
  });
}
