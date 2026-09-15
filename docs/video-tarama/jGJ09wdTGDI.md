# Claude Design ile Web Sitesi Yapmak Bu Kadar Kolay mı? | Yazılımcı Gözüyle Test
kanal: Yıldız Dikme · süre: 15 dk · altyazı: otomatik tr
ana iddia: Claude Design yalnız promptla premium görünen bir site tasarımı çıkarıyor ama performansı zayıf (iddia: perf %71, araç adı geçmiyor), bu yüzden tasarım orada yapılıp proje indirilerek Claude'da optimize edilmeli.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Claude Design (claude-design MCP) | ZATEN VAR | ELENDİ | claude-design MCP kurulu; videoda prompt→site, UI kit (renk paleti, buton, form input, tag, logo dark/light), asset/component klasörü, share ile indirme |
| Adobe Firefly | YENİ | ELENDİ | arka plan saat videosu ve görseller için; ilk+son kare verip 8 sn video; ücretli abonelik (sözlü), UI/kod iş akışına katkısı yok |
| Lighthouse? | ÇİFT | ELENDİ | adı geçmiyor; performans/erişilebilirlik/best practice/SEO skorları okunuyor, perf %71 (iddia, yalnız ekranda); frontend-craft audit.mjs aynı işi yapıyor |
| Claude Design çıktısını Claude'a taşıyıp optimize etme | YENİ | BİLGİ | videonun ana önerisi: çıktı doğrudan kullanılmaz; arka plan videosu geç yükleniyor, loading ve görsel optimizasyonu yok, açılış animasyonu yok |
| Metin seçim rengi (::selection) | YENİ | BİLGİ | kopyalamak için seçilen metnin yeşil görünmesi "ince detay" olarak övülüyor |
| diğer: Google Veo, Kling AI?, Hostinger, İngilizce prompt | YENİ | ELENDİ | Veo (ASR "VO") ve Kling AI? (ASR "Clint", "Clank Aa") video modeli/prompt galerisi, UI işine katkı yok; Hostinger açıklamadaki sponsor linki; İngilizce prompt kanıtsız görüş |
| diğer: cihaz önizlemesiyle responsive kontrol, kendi görsellerini prompta verme | ZATEN VAR | ELENDİ | frontend-craft Bölüm 2 (390/768/1440 screenshot), Bölüm 5 (brand_assets/) |
## ölçütler (YENİ)
- Adobe Firefly, Google Veo, Kling AI?, Hostinger: bakım=bilinmiyor (repo yok, web servisi) · çift=örtüşme yok · izin=hesap+login; Firefly ücretli abonelik (sözlü), Veo Firefly içinden kullanılıyor · context=yok (Claude Code'a yüklenmez) · kurulum: —
- Claude Design çıktısını optimize etme, ::selection rengi, İngilizce prompt: bakım=— (teknik) · çift=örtüşme yok (Bölüm 4 perf görsel/video yüklemesini kapsamıyor) · izin=yok · context=yalnız kural satırı · kurulum: —
## hedefler (BİLGİ)
- Claude Design gibi dış tasarım aracından indirilen proje olduğu gibi teslim edilmez: görsel optimizasyonu ve arka plan videosu için yükleme durumu eklenip audit'ten geçirilir → frontend-craft Bölüm 4 (perf)
- Metin seçim rengi (::selection) marka renginden verilir → frontend-craft Bölüm 3 (Renk)
---
## ek: tasarım
prompt:
Web sitenin ortasındaki cloudy yazısını kaldır. Çünkü zaten logoda yazıyor. Buraya ekstra yazmaya gerek yok. Geri kalan kısımları yani buton ve yazıları web sitenin sağ alt köşesine al. (sözlü)
Ayrıca şu anda web site tüm cihazlara uyumlu değil. Bu web siteyi responsive yap. (sözlü)
önerilen, gönderimi görünmüyor: Yani tablet ve telefon boyutunda bu ikonları e menüye dahil edebilirsin (sözlü)
Ana site promptu (İngilizce): metin altyazı/açıklamada yok — yalnız ekranda. İçerik: e-ticaret sitesi, verilen video arka plana tam ekran ve sürekli oynar, verilen saat görselleri kullanılır, premium ve dark temalı, "shop now" gibi harekete geçiren butonlar (sözlü özet, birebir değil)
Firefly video promptu (İngilizce, başkasının promptundan uyarlanmış): metin altyazı/açıklamada yok — yalnız ekranda. İçerik: ilk ve son kare yüklenip 8 sn video; parlaklığın fazla verilmesi istenebilir (sözlü özet, birebir değil)
İlk düzeltmedeki "sağ alt köşe" sonradan "sola al" diye yeniden istendi (sözlü özet, birebir değil)
referans siteler: Rolex resmi web sitesi (karşılaştırma), Kling AI? (prompt galerisi, video promptu için), hostinger.com/YILDIZDIKME10 (açıklama, sponsor)
stiller: dark tema, premium
premium kararlar:
1) Tam ekran, sürekli oynayan arka plan videosu (AI ile üretilmiş saat videosu); Rolex resmi sitesinin de arka planda video kullandığı gösteriliyor
2) Promptta açıkça "premium" ve "dark temalı" site istenmesi ve AI ile üretilmiş kendi saat görsellerinin verilmesi
3) İnce detaylar: metin seçiminde yeşil vurgu, renk geçişi, Roma rakamları, footer (ASR "Futur"); ölçüm/kanıt yok, yalnız beğeni
