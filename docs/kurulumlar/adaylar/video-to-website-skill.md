# video-to-website skill
ad: video-to-website skill
tur: skill
video: BdLrWHzdYt4
repo: thanhthuduc99/video-to-website
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/thanhthuduc99/video-to-website
telemetri: Yok: skill salt markdown talimatı, kendi kodu/ağ çağrısı içermiyor. Üretilen site GSAP ve Lenis'i CDN'den çekiyorsa üçüncü taraf istekleri olabilir (bilinmiyor). Claude Code'un kendi telemetrisi ayrı konu.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-3)
## Ne
Claude Code için markdown skill: verilen bir video dosyasını kare dizisine bölüp tam ekran canvas'a çizen, kaydırma (scroll) ile video karelerini senkronlayan, yazı animasyonlu bir web sitesi üretir. Not: videodaki skill'in birebir kaynağı doğrulanamadı; bulunan repo Vietnamca bir uyarlama, aslı remamare13'ün claude-framework paketindeki İngilizce video-to-website skill'i (README'ye göre). Videoda bu ikisinin aynısı olup olmadığı sınanamadı.
## Mekanizma
SKILL.md, Claude'a adım adım talimat verir: (1) ffprobe ile çözünürlük/süre/kare sayısı analizi, (2) ffmpeg ile 150-300 WebP kare çıkarma, (3) index.html, css/style.css, js/app.js iskeleti, (4) HTML'de loader, header, hero, canvas ve data-enter/data-leave/data-animation nitelikli bölümler, (5) CSS'de metnin yanlarda %40 içinde durması, mobilde ortalanması, (6) JS'te Lenis yumuşak kaydırma, ilk 10 kareyi önce yükleyip kalanı sonra yükleme, canvas çizimi, GSAP ScrollTrigger ile kare–scroll bağlama, 7 metin animasyon türü, sayaç ve marquee, (7) Playwright ile tüm sayfayı kaydırıp ekran görüntüsüyle test. 14 maddelik kontrol listesi ve sık hata listesi içerir. Kullanım: /video-to-website video.mp4.
## Kanıt
- Video, videoyu karelere bölüp scroll ile senkronlayan siteyi Claude Code'a kurduran markdown skill dosyasının var olduğunu söylüyor. → doğrulandı · thanhthuduc99/video-to-website README'si: ffmpeg ile 150-300 WebP kare, canvas, GSAP ScrollTrigger + Lenis ile scroll'a bağlı kare oynatma; repo SKILL.md içeriyor. Videodaki dosyanın aynısı olduğu ise sınanamadı.
- İki skill dosyası gerekli (frontend-design ve video-to-website). → sınanamadı · Bulunan repo README'sinde frontend-design bağımlılığı geçmiyor; video karesinde iki klasör görünüyor. `video getir` komutu URL yerine video ID verildiği için hata verdi, video içeriği tekrar çekilmedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- ffmpeg'i PATH'e kur (ffprobe ile birlikte gelir)
- git clone https://github.com/thanhthuduc99/video-to-website ~/.claude/skills/video-to-website
- Claude Code'da: /video-to-website path/to/video.mp4 (renk tercihi çağrı sırasında söylenebilir; varsayılan marka Contentta Orbital, koyu zemin/kırmızı vurgu)
- Videoda ayrıca frontend-design/SKILL.md skill'inin de gerekli olduğu söyleniyor; bu ayrı skill kurulmalı
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Videodan scroll-senkronlu tanıtım sayfasını tek komutla, tutarlı yapı ve test adımıyla kurdurur; tekrar eden tasarım/kurulum işini standartlaştırır.
## Maliyet/risk
Repoda LICENSE dosyası görünmüyor (ağaçta yok): lisans belirsiz, kopyalama/dağıtım hakkı net değil; kaynak çeviri türevi. 150-300 WebP kare büyük sayfa boyutu ve mobil performans sorunu doğurabilir. ffmpeg ve Playwright bağımlılığı. Yıldız/commit verisi alınamadı, bakım durumu bilinmiyor. Videodaki skill ile birebir aynı olduğu doğrulanmadı. Skill talimatları ajana dosya yazdırıp komut çalıştırtır; kullanmadan önce SKILL.md okunmalı.
## Tasarruf
Token aracı değil; tasarruf iddiası yok.
## Üretilebilir
hedef_tur: skill
tarif: Kendi SKILL.md'mizi yaz: frontmatter (name, description, argüman = video yolu). Adımlar: ffprobe ile analiz; ffmpeg -i video -vf fps=N,scale=1920:-1 -c:v libwebp kare_%04d.webp ile 150-300 kare (mobil için ikinci küçük set); şablon index.html/style.css/app.js (Lenis + GSAP ScrollTrigger, canvas çizimi, ilk kareleri önce yükleme, data-enter/leave/animation nitelikleri, prefers-reduced-motion yedeği); Playwright ile kaydırma+ekran görüntüsü doğrulaması; kontrol listesi. Kendi marka/renk parametremizi ve kare sayısı/boyut bütçesini ekle. Lisans belirsiz olduğu için metni kopyalama, yalnız yaklaşımı yeniden yaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-3/panel.md → Ömer sütunu
## Özellikler
### Videoyu ffmpeg ile 150-300 WebP kareye böler; ilk 10 kareyi önce yükler, kalanı sonra
kaynak: https://github.com/thanhthuduc99/video-to-website
### Tam ekran canvas, kareler GSAP ScrollTrigger + Lenis ile scroll'a bağlı
kaynak: https://github.com/thanhthuduc99/video-to-website
### 7 metin animasyon türü, ardışık bölümlerde tekrar yok; sayaç, marquee, sabit CTA
kaynak: https://github.com/thanhthuduc99/video-to-website
### Playwright ile test, 14 maddelik kontrol listesi ve sık hata listesi
kaynak: https://github.com/thanhthuduc99/video-to-website
## Destek
- BdLrWHzdYt4 · 1:02 · Videoyu karelere bölüp scroll ile senkronlayan siteyi Claude Code'a kurduran markdown skill dosyası. · kanıt: Video iki skill dosyasının gerekli olduğunu söylüyor. (karede: Explorer'da skills altında frontend-design/SKILL.md ve video-to-website/SKILL.md klasörleri görünüyor.)
