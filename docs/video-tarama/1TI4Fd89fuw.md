# Claude Fable + GPT-5.6 Sol ile Web Sitelerinizi 10 Kat Daha Premium Yapın!
kanal: Yıldız Dikme · süre: 20 dk · altyazı: otomatik tr
ana iddia: Premium site uzun prompttan değil; ödüllü bir tasarımı (ekran kaydıyla) analiz edip yazılım kurallarına ve teknoloji seçimine çevirmekten ve işe göre model seçmekten gelir (GPT-5.6 Sol kurulum/video analizi/performans, Claude Fable 5 tasarım/animasyon iyileştirme; "10 kat premium" ve model kıyası ölçümsüz iddia).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| greensock/GSAP | YENİ | ELENDİ | dağınık kart → sıra → 3D galeri ve dönerek açılma GSAP ile yapıldı; proje başına JS bağımlılığı, ortama kurulacak araç değil |
| model iş bölümü: GPT-5.6 Sol (iskelet, video analizi, performans) + Claude Fable 5 (tasarım, animasyon, mobil iyileştirme) | YENİ | ELENDİ | ikinci ücretli platform; "1,5 haftalık yoğun kullanım" anekdotu, kıyas ölçümü gösterilmedi |
| hareketli referansı ekran kaydıyla analiz ettir: davranış saniye saniye metne, teknoloji önerisi (Blender gerekmez, Three.js/GSAP) | YENİ | BİLGİ | REF girdisi yalnız png/jpg/pdf, hareket kaybolur; Claude Code video okumaz, kare dizisi gerekir; "Fable video anlamada zayıf" iddiası |
| animasyon akıcılığı kabul kriteri: kasma yok, mobil dahil | YENİ | BİLGİ | GPT çıktısı "bazı yerlerde kasıyor", Fable pass'i performans+mobil odakla düzeltti (görsel gözlem, ölçüm yok); screenshot döngüsü kasmayı yakalamaz |
| Mobbin (mobbin.com) | YENİ | ELENDİ | web+mobil uygulama/panel ekranı referansı; free kısıtlı, pro üyelik ücretli (sözlü); login'li kaynak agent'ın okuyacağı Bölüm 10'a uymaz |
| Awwwards, Godly / recent.design · analiz→kural→teknoloji · kopyalamadan uyarlama · analizi dokümanla sonraki modele devretme · iyileştirme ayrı pass · yüksek düşünme seviyesi | ZATEN VAR | ELENDİ | Bölüm 10 (awwwards.com, recent.design; dil çıkar, kopyalama) · Bölüm 7 (DESIGN.md kalıcı hafıza) · Bölüm 8/9 (iki-pass, tur sırası) · Claude Code effort ayarı |
| diğer: vercel/next.js, mrdoob/three.js, Blender, Netlify, Google Drive, LinkedIn geri bildirimi | YENİ | ELENDİ | proje stack'i (frontend-craft static/aspnet sabit; Three.js/Blender yalnız AI analizinde anıldı) ya da barındırma/paylaşım |
## ölçütler (YENİ)
- greensock/GSAP · vercel/next.js · mrdoob/three.js: bakım=GSAP pushed 2026-04-13, 28.4k yıldız; next.js pushed 2026-09-15, 142.3k yıldız; three.js pushed 2026-09-15, 115.6k yıldız; hiçbiri arşivli değil · çift=örtüşme yok (ui-ux-pro-max'ta yalnız GSAP preset verisi) · izin=projeye npm/CDN bağımlılığı · context=0 (ortama yüklenmez) · kurulum: —
- Mobbin · GPT-5.6 Sol / Claude Fable 5 · Blender, Netlify, Google Drive, LinkedIn: bakım=bilinmiyor · çift=Mobbin kısmen Bölüm 10 kaynaklarıyla (awwwards, lapa.ninja, dribbble); diğerleri örtüşme yok · izin=Mobbin üyelik (pro ücretli), GPT-5.6 Sol OpenAI hesabı, diğerleri hesap/login · context=0 · kurulum: —
- teknikler (ekran kaydı analizi, akıcılık kriteri): bakım=— (teknik) · çift=örtüşme yok (Bölüm 0 REF statik görsel, Bölüm 4 perf yalnız font/CLS) · izin=kare çıkarma için ek araç gerekebilir (videoda ChatGPT'ye doğrudan video atıldı) · context=yalnız kural satırı · kurulum: —
## hedefler (BİLGİ)
- hareketli referans: ekran kaydından kare dizisi + davranış dökümü (giriş, geçiş, hover, mobil) → frontend-craft Bölüm 0 (REF girdisi)
- animasyon akıcılığı (kasma yok, mobil dahil) ayrı kabul satırı → frontend-craft Bölüm 4 (perf)
---
## ek: tasarım
prompt:
- ilk prompt (ChatGPT'ye ekran kaydıyla): Bu videoyu detaylı bir şekilde izlemeni istiyorum. Bu web siteyi ben çok beğendim ve wipe coding yaparak ilk olarak tasarımı analiz edeceğiz. Sonrasında bunu Fable ve GBT 5.6 ile kodlayacağız. Beni yönlendireceksin. Bu proje nasıl yapılmış olabilir? Bana hepsini detaylı anlat (sözlü)
- proje prompt'u (GPT-5.6 Sol): metin altyazı/açıklamada yok — yalnız ekranda (tam metin açıklamadaki Google Drive dosyasında)
- Next projesi olsun; GSAP ile yapılsın; galeri circle/daire şeklinde olsun; hazırlanan ekran kaydı videosu da prompta eklendi (sözlü özet, birebir değil)
- ikinci prompt (Claude Fable 5): metin altyazı/açıklamada yok — yalnız ekranda
- 5.6'dan alınan teknik yapı verilir; performans, görsel kalite, animasyon iyileştirme ve özellikle mobil tarafa odaklan (sözlü özet, birebir değil)
referans siteler: inkwell.tech (ilham), awwwards.com, recent.design/?ref=godly (Godly), mobbin.com/discover/apps/web/latest, gsap-impression-gallery.netlify.app (videoda üretilen proje)
stiller: üç boyutlu (3D) galeri; portfolyo (Awwwards kategorisi); editorial, illustration/3D (Godly kategorileri)
premium kararlar:
1) Giriş koreografisi: yenilemede dağınık kartlar → düzen/sıra → üç boyutlu galeri; tıklanan görsel dönerek açılır, mouse'a tepki veren görseller ön-arka yüz döner, galeri mouse ile döner (GSAP); mobilde görseller hafif büyüyerek gelir
2) Scroll davranışı: "Awwwards ödüllülerin en önemli ortak noktası" iddiası; animasyon yalnız çalışmamalı, tüm cihazlarda performanslı çalışmalı (kanıt/ölçüm gösterilmedi)
3) İşe göre model: iskelet + video analizi + performans GPT-5.6 Sol, tasarım/animasyon/mobil iyileştirme Claude Fable 5 ("premium sitelerde Fable çok daha iyi" iddiası, kıyas ölçümü yok)
