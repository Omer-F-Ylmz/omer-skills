// SplitText maskeli satır girişi (GSAP standart ücretsiz lisans): harfler satır maskesinin altından yükselir, tetik görününce bir kez. autoSplit → font/boyut değişince yeniden böler.
import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(SplitText, ScrollTrigger);

export function metinGir(el, tetik = el) {
  return SplitText.create(el, {
    type: 'lines,chars',
    mask: 'lines',
    autoSplit: true,
    onSplit: (s) =>
      gsap.from(s.chars, {
        yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.012,
        scrollTrigger: { trigger: tetik, start: 'top 85%' },
      }),
  });
}
