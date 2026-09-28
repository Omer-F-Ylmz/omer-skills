# Parti D brief — fCc97Rv-60w · v-vRYtvWDYs · 39IlNR-P3-Q (2026-09-28)
kaynak: `video brief docs/kurulumlar/2026-09-28-uygula.md` (Koşu 7: Özellik kararları · Olası tekrarlar) + `video brief <tarama raporu>` ×3 (Site/UI · Prompt anatomisi video başına; uygula brief'i birikimli raporda ilk 6 satırı Parti C'den aldığı için)
## Özellik kararları
- frontend-design/kurulu → ZATEN VAR — kurulu: frontend-design
- frontend-design/dörtlü-skill-yığını → ÖĞREN — kurulu; yeni olan kullanım biçimi, kurulum yok
- taste-skill/kurulu → ZATEN VAR — kurulu: taste-skill
- taste-skill/animasyon-düzeyi-kararı → ÖĞREN — kurulu; yeni olan kullanım biçimi, kurulum yok
- scroll-craft/kurulu → ZATEN VAR — kurulu: nateherk-design:scroll-craft
- scroll-craft/referans-videodan-scroll-geçişleri → ÖĞREN — kurulu; yeni olan kullanım biçimi, kurulum yok
- design-dna/kurulu → ZATEN VAR — kurulu: anthropic-skills:design-dna
- design-dna/referans-video-analizi → ÖĞREN — kurulu; yeni olan kullanım biçimi, kurulum yok
- everything-claude-code/kurulu → ZATEN VAR — kurulu: everything-claude-code
- context-mode/sandbox-context-saving → DENE — hipotez: RTK+headroom üstüne ek kazanç var mı · metrik: token · bütçe: 1 aday görev · geri_alma: mcp kaldır · eşik: %20 üstü ek tasarruf yoksa RED
## Site/UI teknikleri
### fCc97Rv-60w
- Kaydırınca eski haline dönen portal/kapı geçişi (glow çerçeveli telefon siluetinde manzara) · tahmin: GSAP ScrollTrigger · bizde: yok
- Kaydırmaya bağlı 3D kredi kartı (yansıma, çip, eğim) · tahmin: CSS 3D transform / Three.js · bizde: yok
- Kaydırmaya bağlı para birimi kaydırıcısı (slider kaydırınca hareket ediyor) · tahmin: GSAP ScrollTrigger · bizde: yok
- Kaydırmaya bağlı ülke/isim listesi değişimi · tahmin: GSAP ScrollTrigger · bizde: yok
- Bölüm bazlı snap kaydırma (Fable 5 versiyonu) · tahmin: CSS scroll-snap · bizde: yok
- Çapraz (diagonal) tipografi, görsel yerine yazıyla anlatım · tahmin: CSS transform rotate · bizde: yok
### v-vRYtvWDYs
- yok (raporda site/UI tekniği yok)
### 39IlNR-P3-Q
- kaydırmaya bağlı video scrub + sahne geçişi · tahmin: scroll-craft (ekranda "scrollcraft.css" adı geçiyor, k00686) · bizde: bilgi/scroll-a-bağlı-video-scrub.md
- kaydırmaya bağlı kademeli metin belirme/kaybolma · tahmin: scroll-craft · bizde: bilgi/scroll-a-bagli-kademeli-metin-belirme-reveal-fade-translatey.md
- sayfa içi konum göstergesi (scroll navigasyonu) · tahmin: scroll-craft/custom · bizde: web-sahne-desenleri
- tutarlı tema/yoğunluk kararı (klasik vs. animasyonlu) · taste-skill · bizde: yok
- footer'da mouse hover ışık efekti · tahmin: custom CSS/JS · bizde: yok
- mobil görünüm devtools ile responsive test · tahmin: Chrome DevTools · bizde: bilgi/responsive-mobil-sahne-testi.md
## Prompt anatomisi
### fCc97Rv-60w
- fontlara, görsellere, boşluklara çok dikkat et · 2:01 · şablon: yok
- intro bölümünü bozma, sonrasını tamamla · 2:01 · şablon: yok
- Awwwards seviyesinde yap, oradaki tasarım kurallarını uygula · 2:01 · şablon: yok
- önceki 4 skill'i kullan · 3:03 · şablon: yok
### v-vRYtvWDYs
- yok (bu videonun prompt adayı yok)
### 39IlNR-P3-Q
- bu 4 skill'i kullan · 8:47 · şablon: yok
- bu videoyu referans al, kopyalama, ilham al · 8:47 · şablon: yok
- tüm cihazlarda çalışsın · 10:56 · şablon: yok
## Olası tekrarlar
- klasik-prompt-şablonu: fontlara, görsellere, boşluklara çok dikkat et · DESIGN.md (frontend-craft:15): DESIGN.md tam olarak 6 başlık, fazlası yok: · 1. Stil adı · 2. Token'lar — 3-6 a · p=0.45
- klasik-prompt-şablonu: intro bölümünü bozma, sonrasını tamamla · kalıp:12: düzeltme promptunda mevcut olanı bozma kısıtını açıkça yaz (teknik: -) · p=0.50
- scroll-site-promptu: tüm cihazlarda çalışsın · kalıp:27: Bu web siteyi responsive yap tek cümle (teknik: doğal dil revizyon) · p=0.57
- karar Desktop'ta (0.4–0.6 bandı kendiliğinden karara bağlanmaz)
