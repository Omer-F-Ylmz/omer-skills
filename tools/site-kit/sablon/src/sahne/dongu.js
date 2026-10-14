// Talep üzerine render: kare yalnız tuval görünür + sekme açıkken ve iste() çağrılınca; kare() true dönerse sürer, false → setAnimationLoop(null).
export function dongu(r, el, kare) {
  let gor = false;
  let acik = false;
  const dur = () => {
    r.setAnimationLoop(null);
    acik = false;
  };
  const iste = () => {
    if (acik || !gor || document.hidden) return;
    acik = true;
    r.setAnimationLoop((z) => {
      if (!kare(z)) dur();
    });
  };
  new IntersectionObserver(([e]) => ((gor = e.isIntersecting) ? iste() : dur())).observe(el);
  document.addEventListener('visibilitychange', () => (document.hidden ? dur() : iste()));
  return iste;
}
