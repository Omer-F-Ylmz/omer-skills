# Tastemaker
ad: Tastemaker
tur: skill
video: Ysr7oNDajJI
repo: codeswithroh/tastemaker
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/codeswithroh/tastemaker
telemetri: README'ye göre her şey yerelde çalışır: barındırılan backend, hesap ve API anahtarı yoktur. Skill için telemetri iddiası görünmüyor. Repoda `worker/` (Cloudflare wrangler) ve `web/` klasörleri var. Bunlar büyük olasılıkla demo/site içindir ama skill'e bağlı olup olmadıkları doğrulanmadı. Betik kaynak kodu okunmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: SkillSpector --no-llm çıktısı boş geldi, sonuç yok. Güvenlik durumu bilinmiyor.
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Kodlama ajanlarına tasarım zevki kazandıran bir skill. Amacı, yapay zekânın ürettiği arayüzün "AI yapmış" gibi görünmemesi. Ajan arayüz kurarken ya da stillerken devreye girer. İndigo-mor gradyan, gölgeli kart ve jenerik hero gibi varsayılanlar yerine gerçek bir tasarım sistemi kullanır.
## Mekanizma
Düz Markdown (SKILL.md, references/) ve küçük Python betiklerinden oluşur (README'ye göre). 1) Palet üretimi: Her proje için taze bir ton ve armoni üretilir. Hazır renk listesi yoktur. `check_contrast.py --matrix` WCAG hesabıyla her renk çiftini denetler ve çiftin metin taşıyıp taşıyamayacağını, kenarlık taşıyıp taşıyamayacağını ya da hiçbirini taşıyamayacağını belirtir. 2) Piksel temelli referans okuma: `extract_palette.py` (Python 3 + Pillow) gerçek görselin piksellerinden renk ve kontrastı çıkarır. Pillow yoksa görüntü tabanlı okumaya (vision) düşer. 3) Hafıza: Proje kararları `.tastemaker/style-lock.md` ve `decisions.log` dosyalarına yazılır. Kalıcı tercihler `~/.tastemaker/profile.md` dosyasına terfi eder. 4) Kapsam: Önce spec okunur ve hangi ekranların tasarıma ihtiyaç duyduğu belirlenir. Ayrıca tip çifti seçimi, gerçek ikon ve varlık çekme, hareket (motion), anti-slop kontrol listesi ve yardımcı bir ideagram illüstrasyon alt-skill'i var. README'nin kendi ayrımı: yalnızca kontrast hesabı doğrulanmıştır. Referans çıkarma, mood-palet eşleştirme ve profil yargı düzeyindedir, kanıtlanmış değildir.
## Kanıt
- Referans görselin gerçek piksellerinden script ile renk/kontrast çıkarır → sınanamadı · README `extract_palette.py` (Python 3 + Pillow) betiğini ve Pillow yoksa vision'a düşmeyi anlatıyor. Betik kodu okunmadı, çalıştırılmadı. Video özeti de aynısını söylüyor.
- Palet, çalışan bir kontrast matrisine (check_contrast.py --matrix) karşı üretilir → sınanamadı · README'de anlatılıyor, betik incelenmedi.
- Hosted backend, hesap ve API anahtarı yok, her şey yerelde → sınanamadı · README bunu iddia ediyor. Repoda worker/ (wrangler.jsonc, schema.sql) klasörü var ve amacı doğrulanmadı.
- Lisans MIT → doğrulandı · README'deki rozet 'MIT License' diyor ve kökte LICENSE dosyası var. Dosya içeriği okunmadı.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 11
## Kurulum
- /plugin marketplace add codeswithroh/tastemaker
- /plugin install tastemaker@codeswithroh
- Elle kurulum: git clone https://github.com/codeswithroh/tastemaker /tmp/tastemaker && cp -r /tmp/tastemaker/skills/tastemaker ~/.claude/skills/tastemaker
- Gemini CLI: gemini skills install https://github.com/codeswithroh/tastemaker --path skills/tastemaker
- Piksel çıkarma için: pip install Pillow (isteğe bağlı)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanın ürettiği arayüzlerde jenerik görünümü azaltır. Kontrast hesabı çalışan bir kontrol olduğu için erişilebilirlik hatalarını yakalar. Stil kararları oturumlar ve ekranlar arasında kalıcı olur. Referans görselden gerçek renk çıkarılır.
## Maliyet/risk
Estetik kalite kanıtlanmış değil. README bunu kendisi de kabul ediyor: yalnızca kontrast doğrulanmış, gerisi yargı. Cursor'da alt klasörler kaybolduğu için mekanizmanın büyük kısmı çalışmaz. Repo `.tastemaker/` çalışma dosyalarını ve site/web/worker gibi alakasız klasörleri de içeriyor. Güvenlik ön taraması "SkillSpector --no-llm" şeklinde geldi ve içinde sonuç yok. Betikler ve SKILL.md'nin kendisi incelenmedi. Yıldız sayısı ve son commit bilgisi alınamadı. Video bulgusunu doğrulayan tek kanıt README ve video özeti.
## Tasarruf
Token aracı değil. Ek bir tasarruf mekanizması yok. Kilitli stil dosyası, aynı kararların her ekranda yeniden türetilmesini önleyerek dolaylı olarak biraz token harcamasını azaltabilir, ama bu ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: Kendi skill'imizi yazabiliriz. Yapı: (1) SKILL.md, arayüz işlerinde tetiklenir ve önce spec okunup tasarım gereken ekranlar çıkarılır. (2) scripts/extract_palette.py: Pillow ile görseli küçültüp k-means veya median-cut ile baskın renkleri, sRGB'den luminans ve kontrast oranlarını çıkarır. (3) scripts/check_contrast.py --matrix: paletteki her çift için WCAG oranını hesaplar. 4.5 ve üzeri metin, 3 ve üzeri kenarlık/UI, altı ise yasak olarak etiketlenir. (4) Stil kararlarını .style-lock.md dosyasına yazıp sonraki ekranlarda okuma kuralı. (5) references/ altında anti-slop kontrol listesi: indigo-mor gradyan, emoji ikon, harf kutulu logo gibi kalıpları yasakla. Kodu doğrudan kopyalamak yerine bu tarife göre sıfırdan yazmak daha güvenli. Önce upstream betikleri okunmalı.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### Proje başına taze palet üretimi ve WCAG kontrast matrisi (hangi çift metin/kenarlık taşıyabilir)
kaynak: https://github.com/codeswithroh/tastemaker
### Gerçek görsel piksellerinden palet çıkarma (extract_palette.py, Pillow, vision yedeği)
kaynak: https://github.com/codeswithroh/tastemaker
### Kalıcı stil kilidi (.tastemaker/style-lock.md, decisions.log) ve kullanıcı profili (~/.tastemaker/profile.md)
kaynak: https://github.com/codeswithroh/tastemaker
### Spec okuyup tasarım gereken ekranları belirleme, tip çifti, gerçek ikon ve varlık, hareket, anti-slop kontrol listesi
kaynak: https://github.com/codeswithroh/tastemaker
### Tastemaker, referansın piksellerinden script (extract_palette.py) ile renk/kontrast çıkarır; metne çevirip bilgi kaybetmez.
video: Ysr7oNDajJI · iddia: Tastemaker referansın piksellerinden script ile detay çıkarır, metne çevirerek bilgi kaybetmez.
sonuc: doğrulandı
arastirma: README bu özelliği açıkça belgeliyor. İlke 2 "Ground in real pixels, not words": Ekran görüntüsü ya da referans verilince ajan görselin gerçek renk ve kontrastını bir script ile okur. Havada bir "vibe" özeti yazıp ondan yeniden kurmaz. README'ye göre metin özetleri referansı özel kılan şeylerin çoğunu kaybeder. SSS bölümü de şunu söylüyor: "Match this reference" konuşma yoluyla yapılırsa görselin metin tarifine, sonra bu tariften yeniden inşaya dönüşür. `extract_palette.py` ise gerçek piksel değerlerini okur. Çalışma şekli: Python 3 ve Pillow gerekir (`pip install Pillow`). Pillow yoksa hata vermek yerine vision tabanlı okumaya düşer. Bu durumda o yedek yol piksel okuması değildir, metin/görüntü yorumudur. Kısıtlar ve dürüst çekince: README'nin "verified vs judgment" bölümü yalnızca kontrast hesabını (check_contrast.py) doğrulanmış sayıyor. Referans çıkarma, mood-palet eşleştirme, profil ve anti-slop listesi "judgment" olarak etiketli, yani kanıtlanmış değil. Yani "script ile piksel okur" iddiası belgede var, ama çıkarımın kalitesi ya da "bilgi kaybetmez" ifadesi kanıtlanmış değil. Bilgi kaybı yalnızca renk/kontrast boyutunda azalır. Düzen, tipografi ve his gibi diğer boyutlar bu script ile taşınmaz. Betik kaynağı (skills/tastemaker/scripts/) okunmadı, çalıştırılmadı. Cursor'da alt klasörler kaybolduğu için bu betik orada çalışmaz. Son commit, yıldız sayısı ve güvenlik taraması: bilinmiyor.
kaynak: https://github.com/codeswithroh/tastemaker
## Destek
- Ysr7oNDajJI · 10:14 · Referans görselin piksellerinden script ile tasarım detaylarını yapılandırılmış biçimde çıkarır, jenerik varsayılanlardan kaçınır. · kanıt: works from the actual pixels of a real reference · iddia: Tastemaker referansın piksellerinden script ile detay çıkarır, metne çevirerek bilgi kaybetmez.
