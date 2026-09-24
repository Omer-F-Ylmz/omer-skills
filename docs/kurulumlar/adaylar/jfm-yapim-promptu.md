# jfm-yapim-promptu
ad: jfm-yapim-promptu
tur: prompt
video: JfmAm3sxCSc
## Ne
Videonun kendi site yapım promptları: ilk prompt (2:01–3:01) ve düzeltme promptu (5:06–6:07). Prompt metni açıklamadaki Drive linkinde; açılmadı, kopyalanmaz. Kaynak: altyazı segmentleri (paket.md) + docs/video-tarama/2026-09-24-JfmAm3sxCSc.md + repo ağacı (YildizDikme/3D-threejs-spiral-gallery).
## Prompt anatomisi
bolumler: hero (büyük başlık) · 3D helezon görsel galeri · sayfanın geri kalanı metin bölümleri (kısa açıklamayla ajana bırakıldı)
hareket: mouse'a tepkili galeri döndürme · yavaş/yumuşak scroll · 2. promptta scroll-tetikli yavaş yazı belirmesi (reveal)
teknoloji: JavaScript, Three.js, GSAP, CSS; repo ağacında Vite + Lenis — sürüm promptta görünmedi
dosya: ayrı dosyalar istendi (2:01); repo: index.html · src/script.js · shaders.js · styles.css · vite.config.js
config: config dosyasında genel ayarlar — görsel sayısı, hız, görseller arası boşluk (3:01)
asset: galeri görselleri (sayısı config'te); kaynak/oran promptta görünmedi
kabul: ölçülebilir ölçüt yok; 2. prompt koruma kısıtı taşır — mevcut galeriyi bozma, yalnız başlığı küçült (6:07)
### Kalıplar
- referans siteyi kopyalama, atmosferinden ilham alan özgün tasarım iste · 2:01 · teknik: - · şablon: yok
- kullanılacak teknolojileri tek tek say · 2:01 · teknik: 3D helezon galeri · şablon: teknoloji
- dosya yapısını ayrı JS ve CSS dosyaları olarak belirt · 2:01 · teknik: 3D helezon galeri · şablon: dosya
- galeri ayarlarını config dosyasında topla: görsel sayısı, hız, boşluk · 3:01 · teknik: 3D helezon galeri · şablon: config
- ana sahneyi ayrıntılı, ikincil bölümleri kısa tarif edip ajana bırak · 3:01 · teknik: - · şablon: yok
- düzeltme promptunda mevcut olanı bozma kısıtını açıkça yaz · 6:07 · teknik: - · şablon: yok
- scroll ile tetiklenen yavaş yazı belirmesi iste · 6:07 · teknik: scroll reveal · şablon: hareket
