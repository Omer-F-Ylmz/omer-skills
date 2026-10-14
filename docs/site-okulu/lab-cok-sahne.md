# lab · tek renderer çok sahne + talep üzerine render
Modül `tools/site-kit/sablon/src/sahne/cok-sahne.js`, lab `labs/cok-sahne/` (shopify raf ızgarası etkisi: 2 raf, 9 kart, her kart kendi cezve/fincan sahnesi + ışık rengi).
- Mekanizma: sabit tam ekran tuval (pointer-events: none), her karede tüm tuval temizlenir, sonra görünür her DOM kutusu için `setViewport`+`setScissor` (y = tuval yüksekliği − rect.bottom) ve kendi kamerası (aspect = kutu oranı) ile `render`. Ekran dışı kutu atlanır.
- Talep üzerine: `dongu.js` — kaydırma (Lenis scroll), boyut ve üzerine gelme dışında kare yok; üzerindeki kartın nesnesi döndükçe döngü sürer, bırakınca durur.
- Neden: tek WebGL bağlamı (tarayıcı ~16 bağlam sınırı), shader/doku tek kez derlenir/yüklenir.
- Tuzak: tek kutuyu yenilemek (kısmi çizim) `preserveDrawingBuffer` olmadan güvenli değil — tampon bileşimden sonra silinebilir; bu yüzden her kare tüm görünür kutular. Kısmi çizim gerekirse preserveDrawingBuffer: true + ölç.
- Bütçe: kutu başı 1 render çağrısı; kart başı PMREM ortamı lab kolaylığı — gerçek sitede tek ortam dokusu paylaşılmalı.
- Kabul (`lab.olc()`, headless): 1 tuval ✓, boşta 0 kare/sn ✓, üzerindeyken 14 kare/sn (yazılım GPU, 9 sahne) ✓, bırakınca 0 ✓, üstte 9 kutu çizilir, sayfa sonunda 0 ✓. Görsel yargı (`kare.py cok-sahne`, ref shopify) 10:00 sonrası.
- Mobil: kart sayısı aynı, `kur(cv, dpr=1.5)` yeter; çok kartta görünür olmayanlar zaten atlanıyor.
