# 4ce9-yat-sitesi-promptu
ad: 4ce9-yat-sitesi-promptu
tur: prompt
video: 4cE9t4rE0-0
repo: yok
lisans: yok
son_commit: yok
arsiv: yok
kaynak: yok
telemetri: yok
arastirma: tam
## Ne
Kurulabilir bir araç değil: Abacus.AI ChatLLM Teams agent'ına verilen bir "site build prompt" tekniği. Kling AI v3 ile üretilen bir yat tanıtım videosu agent bağlamına ("agent section") bırakılıyor, agent bunu hero referansı sayıp scroll-scrub video hero'lu bir site üretiyor. Anlatıcı aynı akışın kahve/uçak gibi başka ürünlerle de tekrarlanabileceğini söylüyor.
## Kanıt
Repo yok (SaaS). Okunan kare (k00442_0.jpg) site-build promptunu değil, önceki adım olan Kling AI video-üretim promptunu gösteriyor; site promptunun renk/font/teknoloji detayları ekranda görünmüyor.
## Kurulum
- yok (Abacus.AI ChatLLM Teams ücretli SaaS abonelik gerektirir, ~$10/ay; yerelde kurulabilir paket yok)
## İzinler
Abacus.AI hesabı + kredi (Basic: konuşma başına 2500 kredi, video üretimi kredi tüketir); yerel dosya sistemi/araç erişimi yok.
## Duman testi
- yok (SaaS, yerel CLI/paket yok)
## Geri alma
- yok
## Köprü izni
- yok
## Önerilen katman
RED (ücretli kapalı SaaS, kurulabilir araç değil; teknik fikir UYARLA olarak alınabilir)
## Telemetri kapatma
- yok
## Özellikler
### scroll-scrub-hero-video
ne: AI ile üretilmiş kısa tanıtım videosunu site hero'sunda scroll pozisyonuna bağlı oynatma (video otomatik oynamaz, scroll ileri/geri sardırır)
kurulum: CSS `view-timeline`/`scroll-timeline` veya GSAP ScrollTrigger + `video.currentTime` senkronizasyonu; kurulabilir paket değil, kod deseni
lisans: yok
etiket: teknik
karar: UYARLA
gerekce: zaten var: yok (kataloğumuzda scroll-scrub hero şablonu yok); aracı kurmadan fikir: mevcut site-build pipeline'ına GSAP ScrollTrigger tabanlı hero-video şablonu eklenebilir
## Mekanizma
### scroll-scrub-hero-video
nasıl: Kısa hero videosu yüklenir; scroll ilerlemesi 0-100% aralığına eşlenir (view-timeline/animation-range veya GSAP ScrollTrigger), bu yüzde `video.currentTime`'a ya da CSS animation-range'e bağlanır; kullanıcı scroll ettikçe video zaman ekseni sürücü kontrolüyle ileri/geri oynatılır, dokunulmayan kısım videonun kendisi ve orijinal kare hızıdır.
neden: Otomatik oynamayan, kullanıcı kontrollü video "premium" algısı yaratıyor (Apple tarzı ürün sitelerinde kanıtlı desen); token kazancı değil, algılanan kalite/etkileşim kazancı.
koşul: Safari (2026 ortası) CSS scroll-driven animasyonları desteklemiyor; mobilde video decode performansı tutarsız; düşük bant genişliğinde video yüklenmeden scrub boş kalır — bu durumlarda JS/GSAP fallback ya da IntersectionObserver tetiklemeli versiyon gerekir.
bizde: kendi site-build şablonlarımızda hero bileşenine opsiyonel "scroll-scrub video" varyantı eklenebilir; ölçülebilir token etkisi yok, UYARLA kalır.
## Bağımsız kanıt
- https://developer.chrome.com/docs/css-ui/scroll-driven-animations — scroll-driven animasyonlar Chrome'da native destekleniyor, Safari desteklemiyor.
- https://medium.com/@maskanati/cinematic-scroll-driven-video-experiences-in-react-fe33f7749b26 — video scrubbing gerçekte JS ile `video.currentTime` ayarlanarak yapılıyor, CSS-only yaklaşım video için güvenilir değil.
- https://www.kdnuggets.com/2026/08/abacus/honest-abacus-ai-review — ChatLLM Teams kredi sistemine tabi (Basic: konuşma/kredi limiti), ağır kullanım için dikkat gerekiyor.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Aynı akışla sınırsız/kolayca kahve, uçak vb. başka site üretilebilir | https://www.kdnuggets.com/2026/08/abacus/honest-abacus-ai-review | abartılı | "unlimited" değil, kredi/konuşma limiti var (Basic tier) | - |
| Scroll ile video sürüklenince site "çok premium" görünüyor | https://developer.chrome.com/docs/css-ui/scroll-driven-animations | doğru | yaygın kanıtlı desen ama Safari desteklemiyor, JS fallback gerek | scroll-scrub-hero-video |
## Prompt anatomisi
bolumler: doğrulanamadı (okunan karede yalnız video-üretim promptu görünüyor, site bölümleri ekranda değil)
hareket: scroll-scrub (video zaman ekseni scroll'a bağlı), drone pull-back (hero videosunun kendi hareketi)
teknoloji: doğrulanamadı (ekranda görünmüyor)
dosya: doğrulanamadı
config: doğrulanamadı
asset: Kling AI v3 ile üretilen yat tanıtım videosu, hero asset olarak agent bağlamına bırakılıyor
kabul: doğrulanamadı
### Kalıplar
- AI üretimi kısa videoyu hero'ya scroll-scrub olarak yerleştir · 7:22 · teknik: scroll-timeline/GSAP ScrollTrigger · şablon: hareket
- Aynı prompt akışını ürün türü değiştirerek tekrar kullan (yat/kahve/uçak) · 7:22 · teknik: parametrik prompt şablonu · şablon: yok
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
