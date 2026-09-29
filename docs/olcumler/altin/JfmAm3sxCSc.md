# Altın set — JfmAm3sxCSc (site 3D, 10:52) · "Claude'a Ödüllü Siteler Gibi 3D Website Yaptırdım" · Yıldız Dikme

## Kaynaklar
- .kos/altin/JfmAm3sxCSc/kaynak.txt (yt-dlp -J açıklama + bağlantılar; altyazı YOK: en.*/tr.* bulunamadı)
- .kos/altin/JfmAm3sxCSc/mozaik-01..06.png (22 kare, 30 sn aralık, 2×2; `tools/video/altin_mozaik.py`)
- Tekil tam çözünürlük kare: okunmadı (dalga çağrı tavanı). Kod/ayar değerleri 2×2 mozaikten okundu.
- Motor raporu/paneli/adayları, docs/video-tarama ve frontend kütüphanesi AÇILMADI.

Kanıt biçimi: zaman · kaynak (altyazı|kare|açıklama) · "alıntı ≤15 kelime" · önem.

## Araç/servis/ürün adayları (9)
1. Claude Code (Desktop, Code sekmesi) · ajan/IDE · siteyi promptla üretir · 02:00 kare "Opus 4.7 1M · Extra high" · yüksek
2. Three.js · kütüphane · WebGL 3D spiral galeri · açıklama "3D Three.js spiral galeri tasarımını Claude'a yaptırdım" · yüksek
3. Lenis · kütüphane · pürüzsüz scroll + scroll hızı · 02:31 kare "Lenis should detect scroll velocity" · yüksek
4. GSAP · kütüphane · scroll animasyonu · açıklama "Three.js, GSAP, scroll animasyonları ve premium bir hero" · orta
5. Awwwards · referans sitesi · SOTD ilham kaynağı · 00:30 kare "awwwards.com/sites/studio-dialect" · orta
6. motionsites.ai (Design Rocket) · prompt kütüphanesi · hazır landing promptları · 10:02 kare "ready-to-use prompt library. Just copy, paste, and launch." · orta
7. Netlify · barındırma · demo yayını · açıklama "stately-naiad-8f0d7f.netlify.app" · düşük
8. Hostinger · barındırma (sponsor) · yayına alma · açıklama "yayına almak istersen Hostinger'i buradan inceleyebilirsin" · düşük
9. Claude Code önizleme sunucusu · araç özelliği · dev server'ı yönetir · 06:31 kare "otherwise call preview_stop" · orta

## Açıklama bağlantıları (5)
1. github.com/YildizDikme/3D-threejs-spiral-gallery · sitenin kaynak kodu · karar: EVET (referans repo; lisans kontrolü) · yüksek
2. drive.google.com/…/1o04wleIp1qUDPjiFk-FHt4t-Eby3jxi8 · prompt klasörü · karar: EVET (tam prompt metni burada) · yüksek
3. studiodialect.com · ilham sitesi (Awwwards SOTD) · karar: hayır (yalnız referans) · düşük
4. stately-naiad-8f0d7f.netlify.app · canlı demo · karar: hayır · düşük
5. hostinger.com/YILDIZDIKME10 · sponsor · karar: hayır · düşük

## Teknikler (12)
1. Silindirik spiral yerleşim · tile'lar sin/cos ile silindir yüzeyinde · 03:31 kare "follow a cylindrical curve using sin/cos positions" · Three.js · yüksek
2. Kavisli tile geometrisi · düz plane değil, eğri BufferGeometry · 03:31 kare "curved BufferGeometry, not a simple flat plane" · Three.js · yüksek
3. Özel shader'lı tile · ShaderMaterial, uMap doku uniform'u, DoubleSide · 02:31 kare "ShaderMaterial with custom vertex and fragment shaders" · Three.js · yüksek
4. Scroll hızı → dönüş · Lenis velocity spin'e eklenir, 0.9 ile söner · 06:01 kare "spinVelocity *= rotationDecay (0.9)" · Lenis+Three.js · yüksek
5. Scroll → kamera inişi · scrollProgress ile hedef Y, lerp yumuşatma · 06:01 kare "targetCameraY = -scrollProgress · cameraYMultiplier" · Three.js · yüksek
6. Masaüstü-yalnız fare paralaksı · mobilde kapalı, kamera geri çekilir · 02:31 kare "On mobile, disable mouse parallax and move the camera" · Three.js · orta
7. Resize yönetimi · aspect, projection matrix, renderer boyutu güncellenir · 02:31 kare "update camera aspect / update projection matrix" · Three.js · orta
8. Canvas hero metninin arkasında · metin WebGL üstünde okunur kalır · 02:31 kare "The canvas should sit behind the hero text" · CSS · yüksek
9. CONFIG kolları · revolutions, tilesPerRevolution, radius, gap, parallax, decay tek nesnede · 06:31 kare "revolutions / tilesPerRevolution → density and length of the helix" · — · yüksek
10. Dokuda koyu yedek · eksik görsel spirali bozmaz · 06:01 kare "texture loader has a dark fallback so missing files won't break" · Three.js · orta
11. 3D galeri CSS · perspective 1400px, preserve-3d, kenarlarda gradient maske · 02:00 kare "linear-gradient(to right, var(--bg), transparent)" · CSS · orta
12. Editoryal serif + italik renkli vurgu · büyük serif başlık, italik kelime altın tonda · 04:31 kare "A studio of long shadows & warm light" · CSS · orta

## Kural/ipucu/iş akışı (6)
1. Revizyonda koruma listesi · değişmeyecekleri önce yaz, sonra tek iyileştirme · 06:01 kare "Only make the specific improvements below." · yüksek
2. Koddan sonra açıklama iste · geometri, scroll, Lenis, paralaks, CONFIG · 04:01 kare "After generating the code, please explain" · orta
3. JS'yi HTML'e gömme, dosyalara ayır · 02:31 kare "Do not put JavaScript code inside the HTML." · orta
4. Görseller için sabit placeholder yolları · 03:01 kare "public/images/img1.jpg to img10.jpg as expected placeholder paths" · orta
5. Awwwards SOTD sitesini ilham olarak açıp promptla yeniden yorumlatma · 00:30 kare "Site of the Day - Feb 18, 2026" · orta
6. "Şablon gibi değil" hedefi prompta açık yazılır · 02:31 kare "should feel like a modern digital studio, not a template" · yüksek

## Promptlar — anatomi (2)
1. Ana site promptu (02:31–04:01 kare, kısmi): (a) rol/hedef: premium stüdyo landing + spiral galeri; (b) dosya yapısı: src/styles.css, shaders.js, public/images; (c) HTML bölümleri: hero, editoryal başlık, about, services/works/process/contact CTA; (d) numaralı teknik gereksinim (renderer→geometri→shader→scroll→kamera→paralaks→resize); (e) görsel stil maddeleri: "Dark background · Editorial typography · Subtle grain/noise"; (f) CONFIG nesnesi; (g) çıktı sonrası 6 açıklama sorusu · yüksek
2. Revizyon promptu (06:01 kare): koruma listesi ("Do not redesign the page.") + numaralı tek düzeltme ("Hero typography adjustment") · yüksek

## Kareden okunan somut bilgiler (7)
1. Model/efor: 02:00 kare "Opus 4.7 1M · Extra high" · orta
2. Claude Code istatistik ekranı: 03:01 kare "19 sessions · 5,820 messages · 6.1M tokens" · düşük
3. Workspace güven diyaloğu: 04:01 kare "Trust this workspace? … /Users/yildizdikme/Desktop/new-video" · düşük
4. İki sürüm: 00:00 kare "localhost:5173 Helix Studio", 04:31 kare "localhost:5174 Lumen Practice" · orta
5. Tile sayısı: 06:01 kare "density and length of the helix (currently 75 tiles)" · orta
6. Açı adımı formülü: 03:31 kare "angle step using Math.PI * 2 / tilesPerRevolution" · yüksek
7. Renderer: 03:31 kare "Create a WebGLRenderer with antialias enabled and alpha enabled" · orta

## Emin olunmayanlar (5)
1. Altyazı yok: sesli anlatım (değerlendirme, "yazılımcı gözüyle" yorumlar) altın sete girmedi.
2. Dev server'ın Vite olduğu yalnız 5173/5174 portundan çıkarım.
3. GSAP'in kodda kullanıldığı karede görülmedi; yalnız açıklamada geçiyor.
4. Kod/değerler 2×2 mozaikten okundu; clamp/px değerleri yanlış okunmuş olabilir (tekil kare okunmadı).
5. Tam prompt Drive klasöründe; kareler yalnız kesitleri gösteriyor.

Kalem sayısı: araç 9 · bağlantı 5 · teknik 12 · kural 6 · prompt 2 · kare bilgisi 7 = 41 · emin olunmayan 5
