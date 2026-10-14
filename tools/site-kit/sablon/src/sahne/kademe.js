// Kademe: ucuz sinyallerle 'dusuk' | 'orta' | 'yuksek' (detect-gpu eklenmedi). shortcut: GPU adı okunmuyor, sahada düşük fps görülürse detect-gpu.
export const DPR = { dusuk: 1, orta: 1.5, yuksek: 2 };

export function kademe() {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return 'dusuk';
  const cekirdek = navigator.hardwareConcurrency || 4;
  if (matchMedia('(pointer: coarse)').matches) return cekirdek >= 8 ? 'orta' : 'dusuk';
  return cekirdek >= 8 ? 'yuksek' : 'orta';
}
