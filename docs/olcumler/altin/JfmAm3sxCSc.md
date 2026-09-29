# Altın set — JfmAm3sxCSc (site 3D, 10:52) · "Claude'a Ödüllü Siteler Gibi 3D Website Yaptırdım" · Yıldız Dikme

Özet (kalem): Araç/servis/ürün 9 · Açıklama bağlantıları 5 · Kurulum/komutlar 3 · Teknikler 11 · Kural/ipucu/iş akışı 6 · Promptlar 2 · Kareden bilgi 8 · Emin olunmayanlar 6 = 50

## Kaynaklar
- .kos/altin/JfmAm3sxCSc/kaynak.txt (yt-dlp -J açıklama + 5 bağlantı, bölüm yok; altyazı tr-orig oto, 22 satır/30 sn; `tools/video/altin_mozaik.py`, seçim motorun `dil_sec`i)
- .kos/altin/JfmAm3sxCSc/mozaik-02..05.png (22 kare, 30 sn aralık, 2×2)
- Tekil tam çözünürlük kare (3): kare-006 (02:31 ilk prompt gövdesi), kare-008 (03:31 prompt adımları + model), kare-013 (06:01 CONFIG kaldıraçları + düzeltme promptu). Bu karelerden okunan kalem `[tekil]` işaretli.
- Motor raporu/paneli/adayları, paket.md, docs/video-tarama ve frontend kütüphanesi AÇILMADI. Eski (altyazısız) sürüm git geçmişinde.

Kanıt biçimi: zaman · kaynak (altyazı|kare|açıklama) · "alıntı ≤15 kelime" · önem.

## Araç/servis/ürün (9)
1. Claude Code (masaüstü uygulaması, Code sekmesi) · ajan · 00:00 altyazı "Bu gördüğünüz web siteyi Cloud yaptı" + 03:31 kare [tekil] "Chat Cowork Code" · yüksek
2. Opus 4.7 (1M bağlam, Extra high efor) · model · 04:00 altyazı "Opus 4.7 kullandım dediğim gibi" · yüksek
3. Three.js · kütüphane · 3D spiral galeri · 01:00 altyazı "boyutlu 3GS ile yapılmış bir görsel galeri var" · yüksek
4. Lenis · kütüphane · yumuşak kaydırma + kaydırma hızı · 02:31 kare [tekil] "Lenis should detect scroll velocity" · yüksek
5. GSAP · kütüphane · animasyon · 00:00 altyazı "3GS, GSP gibi animasyonlu web sitelerde birçok farklı projem var" + açıklama "#GSAP" · orta
6. Studio Dialect · ilham sitesi (ödüllü) · 00:00 altyazı "ilhamı ödül alan bir web siteden aldım" + açıklama · orta
7. motionsites.ai · hazır prompt'lu site galerisi (ücretsiz + Premium) · 09:00 altyazı "copy prompt dediği zaman ... prompu'u bize hazır şekilde veriyor" · orta
8. Awwwards · ödül/ilham galerisi · 04:31 kare sekme "Awwwards Nominees" · düşük
9. Hostinger · barındırma (sponsor) · açıklama "web sitesini yayına almak istersen Hostinger'i buradan inceleyebilirsin" · düşük

## Açıklama bağlantıları (5)
1. https://github.com/YildizDikme/3D-threejs-spiral-gallery · proje kaynağı · açıklama "Github Link" · yüksek
2. https://drive.google.com/drive/folders/1o04wleIp1qUDPjiFk-FHt4t-Eby3jxi8 · prompt dosyaları · açıklama "Prompt Link" · yüksek
3. https://stately-naiad-8f0d7f.netlify.app/ · canlı site · açıklama "Site linki" · orta
4. https://studiodialect.com/ · ilham sitesi · açıklama "İlham Aldığım Web Site" · orta
5. https://hostinger.com/YILDIZDIKME10 · sponsor · açıklama · düşük

## Kurulum/komutlar (3)
1. Boş klasör ("new-video") aç, Claude Code'da çalışma alanına güven · 02:30 altyazı "masaüstümde new video diye bir dosya yolu belirttim" + 04:01 kare "Trust this workspace?" · orta
2. Görselleri public/images/img1..img10.jpg olarak koy · 06:01 kare [tekil] "Drop replacements into lumen-practice/public/images/img1.jpg … img10.jpg" · orta
3. Dev sunucu 5174 portunda; durdurmak için preview_stop ya da Ctrl+C · 06:31 kare "Dev server is still running on port 5174" · düşük

## Teknikler (11)
1. Prompt'u Türkçe yaz, bir AI'a İngilizceye çevirt · 02:00 altyazı "İlk Türkçe yazabilirsiniz. Sonrasında herhangi bir yapay zekaya bunu İngilizceye çevir" · yüksek
2. Ödüllü siteyi kopyalama, atmosferinden ilham al · 00:30 altyazı "Buradan ilham alarak yeniden bir web site oluşturmaktı" · yüksek
3. Teknolojileri ve dosya yapısını prompt'ta tek tek yaz · 02:30 altyazı "kullanacağı teknolojilerden bahsettim. JavaScript, 3Gs, CSS dosyalarından" · yüksek
4. Galeri parametrelerini tek CONFIG nesnesinde topla (görsel sayısı, hız, boşluk) · 03:00 altyazı "toplam kaç tane görsel olması gerektiğini, hızını, aralarındaki görsellerin boşluğunu" · yüksek
5. Spiral geometri: kare sayısı tilesPerRevolution × revolutions, açı adımı 2π/tilesPerRevolution, eğri BufferGeometry · 03:31 kare [tekil] "Build each image tile as a curved BufferGeometry, not a simple flat plane." · yüksek
6. Kaydırma hızı dönüşü geçici hızlandırır, sonra sönümlenir · 02:31 kare [tekil] "The spin velocity should decay smoothly over time." · yüksek
7. Masaüstünde fare parallax; mobilde kapat, kamerayı geri çek · 02:31 kare [tekil] "On mobile, disable mouse parallax and move the camera slightly farther back." · orta
8. Özel shader: ayrı shaders.js (vertexShader/fragmentShader), ShaderMaterial · 02:31 kare [tekil] "Create a simple shaders.js file that exports vertexShader and fragmentShader" · orta
9. Kod sonrası açıklama iste (geometri, kaydırma→kamera, Lenis→dönüş, CONFIG değerleri) · 02:31 kare [tekil] "After generating the code, please explain" · orta
10. İkinci turda yalnız hedef düzeltme, gerisini "bozma" diye kilitle · 06:00 altyazı "Diğer yaptıklarını kesinlikle bozmasını istemiyorum" · yüksek
11. Metinlere kaydırmayla tetiklenen yavaş giriş animasyonu · 06:00 altyazı "scroll'la beraber tetiklenen bir yavaşça yüklenmesini istiyorum" · orta

## Kural/ipucu/iş akışı (6)
1. Aynı prompt farklı sonuç verir; çıktı kararlı değil · 07:30 altyazı "Aynı prompa farklı sonuçlar verdiği çok oldu" · yüksek
2. Ajanlar İngilizce prompt'u daha iyi anlar · 02:00 altyazı "İngilizceyi AI agentlar çok daha iyi anlıyor" · orta
3. Prompt ne kadar ayrıntılıysa çıktı o kadar iyi · 03:00 altyazı "promptu ne kadar iyi verirseniz çıktıyı o kadar çok iyi verir" · orta
4. Boyut düzeltmesini sayıyla ver · 06:30 altyazı "direkt siz matematiksel olarak da söyleyebilirsiniz" · orta
5. JS'i HTML'e gömme, dosyalara ayır · 02:31 kare [tekil] "Do not put JavaScript code inside the HTML." · orta
6. Sıfırdan proje üretimi ~5 dk sürer · 04:00 altyazı "Ortalama bir 5 dakika kadar bekledim ben" · düşük

## Promptlar (2)
1. Ana prompt anatomisi: amaç (özgün ajans sitesi, 3D spiral galeri) → teknoloji/dosyalar → CONFIG nesnesi → 14 adım Three.js talimatı → görsel stil listesi → shader dosyası → "açıkla" soruları · 02:31–04:01 kare [tekil] "The layout should feel like a modern digital studio, not a template" · yüksek
2. Düzeltme prompt'u: "Important" altında bozma yasakları + numaralı iyileştirmeler (hero yazı küçültme…) · 06:01 kare [tekil] "Please update the project carefully without breaking the existing Three.js spiral/gallery structure." · yüksek

## Kareden bilgi (8)
1. CONFIG kaldıraçları: revolutions/tilesPerRevolution (75 kare), startRadius/endRadius, spiralGap, tileHeightRatio, cameraZ, cameraYMultiplier, scrollRotationMultiplier, rotationDecay, baseRotationSpeed, parallaxStrength, cameraSmoothing · 06:01 kare [tekil] "rotationDecay → how long the scroll-induced spin lingers." · yüksek
2. Dönüş sönümü rotationDecay 0.9; spinVelocity her karede çarpılır · 06:01 kare [tekil] "spinVelocity *= rotationDecay (0.9)" · orta
3. Kaydırma→kamera: targetCameraY = -scrollProgress·cameraYMultiplier·10; lookAt ile hafif aşağı eğim · 06:01 kare [tekil] "camera.lookAt(0, currentCameraY · 0.4, 0)" · orta
4. Doku yükleyicide koyu yedek; eksik görsel spirali bozmaz · 06:01 kare [tekil] "missing files won't break the spiral" · orta
5. Shader girdileri uMap, uCameraPosition; THREE.DoubleSide; tile.rotation.y = i * angleStep · 02:31 kare [tekil] "tile.rotation.y = i * angleStep" · orta
6. Görsel stil maddeleri: koyu arka plan, editoryal tipografi, CSS grain/noise, minimal bölümler · 02:31 kare [tekil] "Subtle grain/noise if possible with CSS" · orta
7. Oturum ayarı: "Opus 4.7 1M · Extra high", "Accept edits" · 03:31 kare [tekil] "Opus 4.7 1M · Extra high" · düşük
8. Sonuç: "Lumen Practice" sitesi, serif editoryal hero, localhost:5174 · 04:31 kare "A studio of long shadows & warm light" · düşük

## Emin olunmayanlar (6)
1. "3GS"/"GSP" oto altyazı Three.js/GSAP diye okundu; GSAP'ın bu projede kullanıldığı karede görülmedi (yalnız açıklama etiketi).
2. İlk prompt karelerden kısmi okundu (baş kısım ve CONFIG gövdesi görünmüyor); tam metin Drive bağlantısında, açılmadı.
3. "75 kare" Claude'un yanıtındaki değer; ilk prompttaki CONFIG değerleriyle aynı mı bilinmiyor.
4. Dev sunucu aracı (Vite?) videoda adıyla geçmiyor.
5. motionsites.ai Premium içerik denenmedi (anlatıcı giriş yapamadı); kalitesi doğrulanmadı.
6. Hover'da görselin geri kayması modelin kendi eklemesi deniyor (08:00); promptta olmadığı doğrulanamadı (prompt kısmi).
