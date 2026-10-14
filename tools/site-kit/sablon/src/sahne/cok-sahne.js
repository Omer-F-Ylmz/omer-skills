// Tek renderer çok sahne: sabit tam ekran tuval, her DOM kutusuna (el) scissor/viewport ile kendi sahne+kamerası çizilir; ekran dışı kutu atlanır.
// Tek WebGL bağlamı = tarayıcının ~16 bağlam sınırı ve kopya doku/shader derlemesi yok. Dönen çiz() çizilen kutu sayısını verir.
// Her kare tüm görünür kutular çizilir: preserveDrawingBuffer olmadan tampon bileşimden sonra silinebilir, tek kutuyu yenilemek güvenli değil.
export function cokSahne(r, gorunumler) {
  return () => {
    const tv = r.domElement;
    const g = tv.clientWidth;
    const y = tv.clientHeight;
    r.setScissorTest(false);
    r.clear();
    r.setScissorTest(true);
    let n = 0;
    for (const { el, s, kam } of gorunumler) {
      const b = el.getBoundingClientRect();
      if (b.bottom < 0 || b.top > y || b.right < 0 || b.left > g) continue;
      r.setViewport(b.left, y - b.bottom, b.width, b.height);
      r.setScissor(b.left, y - b.bottom, b.width, b.height);
      kam.aspect = b.width / b.height;
      kam.updateProjectionMatrix();
      r.render(s, kam);
      n++;
    }
    return n;
  };
}
