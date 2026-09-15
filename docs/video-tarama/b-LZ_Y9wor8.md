# Claude'a Awwwards Ödüllü Siteden 3D Sinematik Web Site Yaptırdım
kanal: Yıldız Dikme · süre: 13 dk · altyazı: otomatik tr
ana iddia: Tasarımı anlatan ve stack/sürüm/dosya yapısı/kod düzeyine inen uzun bir promptla Claude Opus 5, Awwwards ödüllü Jesko Jets'ten uyarlanan 3D sinematik scroll portfolyosunu doğru kurar; promptu alanın "%90, %100'e yakın" benzerini çıkaracağı iddiası ölçümsüz.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| greensock/GSAP + darkroomengineering/lenis | YENİ | ELENDİ | promptta sürümleriyle istenen animasyon/smooth scroll stack'i; Claude ortamına kurulan araç değil, proje bağımlılığı (kural hedefi aşağıda) |
| diğer: vercel/next.js, Vue (vuejs/core), Angular (angular/angular), mrdoob/three.js? | YENİ | ELENDİ | proje framework'ü: Next.js kullanıldı, Vue/Angular sözlü alternatif; three.js yalnız açıklama hashtag'inde (sözlü "WebGL"); kurulacak araç değil |
| anlatı konsepti: ürün yerine hikâye/metafor, her öğe fikre hizmet eder | YENİ | BİLGİ | pencere=yolculuk, footer dünyası=global; Bölüm 10 yalnız ritim/kontrast/boşluk çıkarıyor, Bölüm 11 "ayırt edici hamle" konsept istemiyor |
| ağır 3D/görsel varlıkta yükleme ekranı (site hazır olunca aç) | YENİ | BİLGİ | videoda "performans için çok önemli" iddiası, ölçüm gösterilmedi; Bölüm 4 perf'te 3D/varlık yükleme kuralı yok |
| hareketi sıfatla değil teknik tarifle iste (kütüphane+sürüm, kod düzeyi) | YENİ | BİLGİ | sözlü: "sinematik yap derseniz büyük ihtimal yapamaz"; DESIGN.md Hareket yalnız süre+easing |
| diğer: Awwwards referansını kopyalamadan uyarlama, dosya yapısını dikte, sade tek mesaj, localhost 3000, görselleri proje klasörüne koy, responsive, sonucu gözle düzeltme (~10px kayma) | ZATEN VAR | ELENDİ | Bölüm 10 · Bölüm 5 (çıktı yapısı, TEK mesaj, brand_assets) · Bölüm 1 · Bölüm 2 (3 genişlik, tolerans) |
## ölçütler (YENİ)
- greensock/GSAP + darkroomengineering/lenis: bakım=GSAP pushed 2026-04-13, 28.4k yıldız, arşiv değil; lenis pushed 2026-09-09, 15.8k yıldız, arşiv değil · çift=örtüşme yok (ui-ux-pro-max'ta yalnız GSAP preset verisi) · izin=proje başına npm bağımlılığı, anahtar/login yok · context=0 (Claude'a yüklenmez) · kurulum: —
- diğer (next.js, Vue, Angular, three.js?): bakım=next.js 2026-09-15 142k · vuejs/core 2026-09-15 54k · angular 2026-09-13 101k · three.js 2026-09-15 116k yıldız, hiçbiri arşiv değil · çift=örtüşme yok · izin=proje başına npm bağımlılığı · context=0 · kurulum: —
- teknikler (anlatı konsepti, yükleme ekranı, hareket tarifi): bakım=— · çift=örtüşme yok · izin=yok · context=SKILL.md'ye birer satır, yalnız skill yüklenince · kurulum: —
## hedefler (BİLGİ)
- anlatı konsepti + öğe-amaç eşlemesi (ürün yerine hikâye; her sahne/öğe fikre bağlı) → frontend-craft Bölüm 11 (künye: ayırt edici hamle)
- ağır 3D/görsel varlıkta yükleme ekranı, site hazır olunca aç → frontend-craft Bölüm 4 (perf)
- hareket/scroll sahnesini sıfatla değil teknik tarifle yaz (kütüphane+sürüm, ör. GSAP/Lenis) → DESIGN.md şablonu (Hareket)
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda; açıklama promptları ve görselleri bir Google Drive klasörüne yönlendiriyor
GSAP ve WebGL kullanan bir creative developer portfolyosu olduğunu en başta belirt (sözlü özet, birebir değil)
teknoloji: Next.js (Vue/Angular da olur); sinematik yapı; tüm cihazlara uyumlu, responsive (sözlü özet, birebir değil)
GSAP ve Lenis sürümlerini yaz; dosya yapısını tarif et, kafasına göre proje kurmasın (sözlü özet, birebir değil)
geri kalanı tamamen teknik/kod kısmı; smooth sinematik akış için promptta kod düzeyinde tarif (sözlü özet, birebir değil)
son olarak projeyi 3000 portunda ayağa kaldır; görseller prompttan ayrı, doğrudan public klasörüne konuyor (sözlü özet, birebir değil)
referans siteler: https://jeskojets.com/ (Jesko Jets, Awwwards ödüllü ilham sitesi), Awwwards (ödül bağlamı, URL verilmiyor)
stiller: sinematik scroll, 3D, oyunlaştırılmış web sitesi, basit/sade tasarım (kanonik stil adı geçmiyor)
premium kararlar:
1) ürünü tanıtmak yerine yolculuk/özgürlük hissi veren tek fikir: uçak penceresinden girilip scroll ile sahneden sahneye geçilen hikâye; sözlü: "Bir fikir var, farklılık var. Bu yüzden bu websler ödül alıyor."
2) footer'da dünya modeli: global marka mesajı; portfolyoda "globalde çalışıyorum, hizmet verebilirim" imajı
3) scroll'da iki kelimenin (sözlü: "creative ve teknoloji") yavaşça belirip netleşmesi; sadelikle akılda kalma (Apple kutuları örneği)
4) gökyüzü sahnesindeki proje slider'ı sürüklenince "A4 kağıdı rüzgarda sallanıyormuş gibi" hareket eder; efekt sahne temasına bağlı
5) jet görsel değil 3D obje, scroll ile süzülerek gelir
