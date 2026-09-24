# Claude'a Ödüllü Siteler Gibi 3D Website Yaptırdım
## Künye
Claude'a Ödüllü Siteler Gibi 3D Website Yaptırdım | Yazılımcı Gözüyle · Yıldız Dikme · süre 10:52 · dil tr-orig · https://youtu.be/JfmAm3sxCSc

## Özet
Yazılımcı Yıldız Dikme, Awwwards'ta günün sitesi seçilen bir ajans sitesinden ilham alıp Claude'a (Claude Code) sıfırdan 3D sarmal (spiral) görsel galerili bir "stüdyo" landing page yaptırıyor. İlk promptu Türkçe yazıp yapay zekaya İngilizceye çevirtiyor; teknolojileri (JavaScript, GSAP, CSS, ayrı dosyalar) ve bir config dosyasıyla genel ayarları (görsel sayısı vb.) detaylı anlatıyor. Claude ilk seferde galeri ve tipografiyi büyük ölçüde doğru üretiyor. İkinci promptta "var olanı bozma" kısıtıyla başlık boyutunu küçültmesini ve sayfanın geri kalanına scroll'a bağlı yumuşak beliren (reveal) yazı animasyonu eklenmesini istiyor; Claude ayrıca kendiliğinden galeri görsellerine hover'da yavaş geri kayma efekti ekliyor. Ekranda Claude'un kod arayüzünde script.js/shaders.js dosyaları, Three.js sahne kurulumu, Lenis tabanlı scroll döngüsü ve GSAP context/cleanup mantığı görünüyor; ayrıca canlı doğrulama çıktısı (ölçülen piksel/opaklık değerleri) paylaşılıyor. Video, hazır prompt kütüphanesi sunan motionsites.ai sitesine değinerek kapanıyor.

## Bölümler
- 0:00 Giriş ve ilham — Awwwards'ta ödül alan/günün sitesi seçilen bir siteden ilham; kopya değil yeniden yorumlama hedefi
- 1:00 Geçiş (3GS/GSAP referansı)
- 2:01 AI ile prompt yazımı — Türkçe yaz, AI'a İngilizceye çevirt; kullanılacak teknolojileri ve dosya yapısını detaylandırma
- 3:01 Prompt detay seviyesi — ne kadar detaylı prompt o kadar iyi çıktı (tüm AI araçları için geçerli)
- 4:02 Config dosyası — galeri görsel sayısı gibi genel ayarlar
- 5:06 İlk sonuç — büyük görsellerle tek galeri tasarımı, renk uyumu, yavaş scroll davranışı
- 6:07 İkinci prompt — mevcut galeriyi bozmadan başlığı küçültme + scroll'la tetiklenen yavaş yazı yüklemesi isteği
- 7:07 Sonuç doğrulama — yazılar scroll ile yumuşak beliriyor
- 8:09 Hover detayı — galeri görselinde hover'da yavaş geri kayma (Claude'un kendi eklediği ince detay)
- 8:09 motionsites.ai tanıtımı — hazır prompt kütüphanesi olan siteler
- 9:12 Kapanış — gelecek proje planı, veda

## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude (Claude Code arayüzü) | yok | CLI | yok | Promptla sıfırdan 3D web sitesi kodu üretme/düzenleme | 6:37 | Ekranda "new-video / Create premium studio landing page with spiral gallery" dosya sekmesi ve "Opus 4.7 1M Extra high" model etiketi |
| Three.js | mrdoob/three.js (ele, 1.00) | teknik | yok | 3D sarmal görsel galerinin sahne/kamera/renderer ve eğri geometrisi | 6:37 | "The entire Three.js section in script.js (CONFIG, scene/camera/renderer setup, createCurvedTileGeometry, buildSpiral)... untouched" |
| GSAP | greensock/GSAP (ele, 1.00) | teknik | yok | Scroll'a bağlı reveal animasyonu ve context/cleanup yönetimi | 6:37 | "gsap.context() + ctx.revert() cleanup... wired ctx.revert() to Vite's import.meta.hot dispose hook" |
| Lenis | greensock/GSAP + darkroomengineering/lenis (ele, 1.00) | teknik | yok | Yumuşak (inertial) scroll döngüsü | 6:37 | "shaders.js ... callback driving spinVelocity, the existing lenisRaf loop" |
| Vite | yok | CLI | yok | Geliştirme sunucusu ve HMR (import.meta.hot) | 6:37 | "Dev server still running on http://localhost:5174/" ve "import.meta.hot dispose hook" |
| Detaylı prompt yazıp gerekirse AI'a çevirtme | yok | ipucu | yok | Türkçe düşünüp önce Türkçe yaz, sonra AI'a İngilizceye çevirt, sonucu kopyala | 2:01 | "Türkçe yazabilirsiniz... herhangi bir yapay zekaya bunu İngilizceye çevir derseniz rahatlıkla çevirir" |
| Prompt'ta kullanılacak teknolojileri ve dosya yapısını açıkça belirtme | yok | ipucu | yok | Çıktının istenen mimaride (JS/CSS dosya ayrımı) gelmesini sağlar | 2:01 | "Burada kullanacağı teknolojilerden bahsettim. JavaScript, 3Gs, CSS dosyalarından, diğer JavaScript dosyalarından" |
| Merkezi config dosyasıyla genel ayar tutma | yok | ipucu | yok | Görsel sayısı gibi parametreleri tek yerden değiştirilebilir kılar | 4:02 | "Burada config dosyamızda... genel ayarları söyledim... toplam kaç tane görsel olması gerektiğini" |
| İkinci promptta "mevcut olanı bozma" kısıtı koyma | yok | ipucu | yok | Var olan çalışan kısımların yeniden yazılıp bozulmasını önler | 6:07 | "Diğer yaptıklarını kesinlikle bozmasını istemiyorum. Bunu belirttim direkt." |
| Scroll'a bağlı kademeli metin belirme (reveal) animasyonu | yok | teknik | yok | Sayfa kaydırıldıkça yazıların yumuşak/kademeli görünür olması | 7:07 | "sayfanın geri kalanındaki yazılar için de scroll'la beraber tetiklenen bir yavaşça yüklenmesini" |
| Galeri görselinde hover'da parallax/geri kayma efekti | yok | teknik | yok | Mouse üstüne gelince görselin yavaşça geriye kaymasıyla derinlik hissi | 8:09 | "üstüne hover yaptığımızda... yavaşça böyle geriye gidiyor görsel" |
| motionsites.ai | Motion Sites? (ele, 0.92) | iş akışı | https://motionsites.ai (görselde) | Hazır AI prompt kütüphanesinden landing page promptu kopyalayıp kullanma | 8:09 | Ekranda "Unlock your AI design superpowers... copy paste and launch", "copy prompt" |
| Netlify (deploy) | yok | iş akışı | https://stately-naiad-8f0d7f.netlify.app/ (açıklamadan) | Üretilen siteyi canlıya alma/paylaşma | 5:06 | Açıklama linki netlify.app uzantılı canlı demo |
| GitHub'da proje reposu paylaşma | yok | iş akışı | https://github.com/YildizDikme/3D-threejs-spiral-gallery (açıklamadan) | Üretilen kodun izlenebilir/tekrar kullanılabilir olması | 0:00 | Açıklamadaki repo linki |
| Awwwards | yok | iş akışı | yok | İlham/kıyaslama kaynağı olarak ödüllü site listesi kullanma | 0:00 | "ilhamı ödül alan bir web siteden aldım... günün web sitesi seçildi"; sekmede "Awwwards Nominees" |

## İddialar
| iddia | zaman | tür |
|---|---|---|
| Video, ilham alınan siteyi birebir kopyalamak değil yeniden yorumlamak amacıyla yapıldı | 0:00 | öneri |
| Prompt ne kadar detaylı yazılırsa çıktı o kadar iyi olur; bu sadece Claude değil tüm yapay zeka araçları için geçerli | 2:01-3:01 | öneri |
| İkinci sürümde tek büyük görselli galeri, iki ayrı scroll-bazlı galeriden daha iyi bulundu | 5:06 | karşılaştırma |
| Scroll ne kadar hızlı yapılırsa yapılsın galeri çok yavaş bir hızla aşağı iniyor | 5:06 | özellik |
| Claude Code doğrulama çıktısı: Hero başlık 1440px görünümde 138.24px hesaplandı (önceki 187.2px) | 6:37 | sayısal |
| Claude Code doğrulama çıktısı: sayfada 23 adet .reveal-text elemanı tespit edildi | 6:37 | sayısal |
| Claude Code doğrulama çıktısı: scroll ortasında örnek elemanda opacity 0.07, transform translateY(44.66px) ölçüldü (animasyon devam ederken) | 6:37 | sayısal |
| Claude Code doğrulama çıktısı: canvas 1440x900 boyutunda ve is-ready işaretli, konsolda hata yok | 6:37 | sayısal |
| Hover'da görselin yavaşça geri kayma efektini Claude kendiliğinden ekledi, prompt'ta istenmedi | 8:09 | özellik |

## Site/UI teknikleri
| teknik | kanıt | kütüphane/araç | bizde |
|---|---|---|---|
| Scroll'a bağlı kademeli metin belirme (reveal, fade+translateY) | 6:37 k00397_0.jpg + "yazılar biraz daha yumuşak bir şekilde yükleniyor" (7:07) | GSAP | omer-kutuphaneler/web-sahne-desenleri kontrol edilmedi |
| Yumuşak (inertial) kaydırma | 6:37 k00397_0.jpg "existing lenisRaf loop" | tahmin: Lenis | omer-kutuphaneler/scroll-craft kontrol edilmedi |
| 3D sarmal görsel galeri sahnesi | 6:37 k00397_0.jpg "Three.js section... createCurvedTileGeometry, buildSpiral" | Three.js | omer-kutuphaneler/web-sahne-desenleri kontrol edilmedi |
| Hover'da görsele parallax/geri kayma | 8:09 sözlü anlatım (görsel kare yok) | tahmin: CSS/JS transform + mousemove veya GSAP | yok |
| Büyük serif italik başlık tipografisi + kontrast renk paneli | 1:31 k00091_0.jpg, 5:36 k00336_0.jpg, 7:38 k00458_0.jpg | tahmin: özel/serif display font (ad ekranda görünmüyor) | yok |
| Kademeli (staggered) satır/blok belirmesi (scroll top 80% eşiği) | 6:37 k00397_0.jpg "Practice rows revealed in staggered fashion as they each crossed top 80%" | tahmin: GSAP ScrollTrigger | yok |

## Kareden okunanlar
- 6:37 Dosya sekmesi: "new-video / Create premium studio landing page with spiral gallery"
- 6:37 script.js: CONFIG, scene/camera/renderer setup, createCurvedTileGeometry, buildSpiral
- 6:37 shaders.js: spinVelocity callback, "existing lenisRaf loop"
- 6:37 "gsap.context() + ctx.revert() cleanup... wired ctx.revert() to Vite's import.meta.hot dispose hook"
- 6:37 Doğrulama metrikleri: Hero title 138.24px (was 187.2px); 23 .reveal-text elements; mid-scroll opacity 0.07 / translateY(44.66px); canvas 1440x900, is-ready; "No console errors"; "Dev server still running on http://localhost:5174/"
- 6:37 Sağ altta model etiketi: "Opus 4.7 1M Extra high"
- 9:42 motionsites.ai anasayfası: "Unlock your AI design superpowers", "copy prompt" özelliği, "Powered by DESIGN ROCKET"

## Belirsizlikler
- Segment metninde "3GS" / "3Gs" geçiyor (1:00, 2:01) — muhtemelen ASR hatası, gerçek terim "GSAP" olabilir; kesin doğrulanamadı.
- "Opus 4.7 1M Extra high" model adı ekranda öyle yazıyor ama bu tarihte (2026-09-24) gerçek bir sürüm adı olup olmadığı doğrulanamadı; video/demo arayüzü kurgusal olabilir.
- Hover parallax efekti sadece sözlü anlatılıyor, ilgili kare pakette yok; teknik ayrıntı (CSS/JS) tahmine dayalı.
- Hostinger sponsor linki (https://hostinger.com/YILDIZDIKME10) açıklamada var ama videoda somut bir kullanım/demo gösterilmiyor; bu nedenle aday listesine alınmadı.
- studiodialect.com açıklamada link olarak var, videoda ilham alınan siteyle aynı mı yoksa ayrı bir referans mı net değil.

## Atlanan segment oranı
0/11 (paket tam okuma)
