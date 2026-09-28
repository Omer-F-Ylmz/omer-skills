# blz-sinematik-portfoy-promptu
ad: blz-sinematik-portfoy-promptu
tur: prompt
video: b-LZ_Y9wor8
repo: yok
lisans: yok
son_commit: yok
arsiv: yok
kaynak: yok
telemetri: yok
arastirma: tam
## Ne
Yıldız Dikme, Awwwards SOTD jeskojets.com sitesini bölüm bölüm inceleyip sinematik anlatıyı (uçak penceresinden giriş, 3D jet, kağıt fizikli slider, globe footer) kendi portföyüne uyarlayan uzun/detaylı prompt gönderiyor Claude'a (Opus); Next.js+GSAP+WebGL+Lenis, dosya yapısı promptta dikte ediliyor. Prompt metni Google Drive linkinde, videoda okunmuyor; kopyalanmadı.
## Kanıt
jeskojets.com bağımsız kaynakla doğrulandı: Awwwards Site of the Day + Developer Award (Ocak 2026), ajans The First The Last, site Webflow ile yapılmış (video onu Next.js+GSAP+WebGL+Lenis ile yeniden üretiyor, kopyalamıyor). Aynı videonun 5 tekniği zaten docs/kurulumlar/bekleyen/teknik-*.md içinde UYARLA olarak onaysız kayıtlı (3d jet, pencere-scroll geçişi, kağıt fizik slider, globe footer, loading screen); bu aday aynı bulguyu tekrarlamaz.
## Prompt anatomisi
bolumler: tasarım analiz bağlamı (jeskojets.com bölüm bölüm) + teknoloji seçimi + davranış/etkileşim detayı + dosya yapısı dikte + loading screen kısıtı
hareket: pencereden içeri giren scroll geçişi · kağıt gibi savrulan (drag+inertia) proje slider · dönen 3D jet modeli · sırayla beliren iki kelimelik tipografi · noktalı 3D globe
teknoloji: Next.js + GSAP + WebGL + Lenis (sürüm promptta/videoda geçmiyor)
dosya: dosya yapısı promptun içinde ajana bırakılmadan belirtiliyor (7:42 "I spell out file structure... I don't want that")
config: görünmedi (ekranda config detayı okunmuyor)
asset: 3D jet modeli muhtemelen Sketchfab kaynaklı (tarayıcı sekmesinden çıkarım, doğrulanmadı)
kabul: yazılı ölçüt yok; yazarın kendi dumanı: localhost:3000 canlı test, "no stuttering" + küçük konumlama/tipografi kusuru not edildi
### Kalıplar
- Ödüllü siteyi bölüm bölüm inceleyip ilham alma · 0:51 · teknik: tasarım analizi iş akışı · şablon: yok
- Dosya yapısını promptta zorunlu kılma (modele bırakmama) · 7:42 · teknik: redundant talimat · şablon: dosya
- Uzun/detaylı prompt ile %90-100 birebir sonuç hedefleme · 6:41 · teknik: ayrıntı seviyesi arttırma · şablon: kabul
- Her şey hazır olana kadar loading screen ekletme · 9:08 · teknik: yükleme durumu koruması · şablon: hareket
- Kaydırmaya bağlı kağıt fiziği slider tarifi · 3:47 · teknik: drag+inertia fizik · şablon: hareket
## Özellikler
### uzun-detayli-prompt-ile-dosya-yapisini-dikte-etme
ne: tasarımı adım adım anlatan uzun prompt + dosya yapısını promptta zorunlu kılma
kurulum: yok (prompt tekniği, kütüphane değil)
lisans: yok
etiket: teknik
karar: ZATEN VAR
gerekce: zaten var: docs/video-tarama/kayit.jsonl (b-LZ_Y9wor8, 2026-09-24 toplu) — aynı kalıp "ZATEN VAR" karara bağlanmış
### pencereden-iceri-giren-sinematik-scroll-girisi
ne: scroll'a bağlı sahne geçişi; uçak penceresinden içeri girip plan/metin belirmesi
kurulum: yok (GSAP ScrollTrigger tahmini, prompt fikri)
lisans: yok
etiket: teknik
karar: ZATEN VAR
gerekce: zaten var: docs/kurulumlar/bekleyen/teknik-kaydirmaya-bagli-sahne-gecisi-pencereden-iceri-girme-plan-metin-belirme.md (aynı video, onaysız bekliyor)
## Mekanizma
### uzun-detayli-prompt-ile-dosya-yapisini-dikte-etme
nasıl: her tasarım bölümü tek tek anlatılıp dosya ağacı doğrudan prompt içine yazılıyor; model kendi mimarisini seçmiyor
neden: modelin varsayılan/şablon çözüme kaymasını önler, %90-100 birebir sonuç hedefine yaklaştırır
koşul: kısa/az detaylı taleplerde ekstra token maliyeti getirir, fayda yalnız kompleks tasarımda görülür
bizde: departman-frontend prompt şablonuna not; kod yazılmaz
### pencereden-iceri-giren-sinematik-scroll-girisi
nasıl: scroll pozisyonu tek bir progress değişkenine bağlanıp pencere/plan objesi buna göre ölçek+opaklıkla açılır, metin katmanları sırayla belirir
neden: DOM/CSS+GSAP transform ile film girişi hissi verir, WebGL sahne kurmadan da uygulanabilir
koşul: mobil/düşük FPS cihazda scroll-jack rahatsız edebilir; kısa/tek ekranlı sitede fayda azdır
bizde: uygulanmadı; bekleyen/teknik-*.md onaya bağlı
## Bağımsız kanıt
- https://www.awwwards.com/sites/jesko-jets — Jesko Jets, Awwwards Site of the Day + Developer Award, Ocak 2026, ajans The First The Last, Webflow ile yapılmış.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| jeskojets.com Awwwards ödüllü site | awwwards.com/sites/jesko-jets | doğru | SOTD + Developer Award, Ocak 2026 | - |
| ~25 dakikada tüm proje üretildi | yok | doğrulanamadı | yazarın kendi zaman iddiası, kaynak yok | - |
| Uzun/detaylı prompt ile %90-100 birebir sonuç alınıyor | yok | doğrulanamadı | ölçülmemiş kişisel iddia | - |
| Kanalın izleyicileri 50'den fazla ülkeden geliyor | yok | doğrulanamadı | doğrulanamayan kişisel iddia | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): anthropic-skills:creative-coding 0.94
