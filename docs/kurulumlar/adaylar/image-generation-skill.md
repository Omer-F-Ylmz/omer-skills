# Image generation skill
ad: Image generation skill
tur: skill
video: -_S3KD0ZIfI
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kaynak kod incelenemedi). Görsel üretimi büyük olasılıkla harici bir model API'sine istek gönderir; bu durumda istem metni üçüncü tarafa gider, ancak doğrulanmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short-2)
## Ne
Videoda kısaca geçen, Claude'a "Use your image generation skill" denilerek çağrılan ve hero bölümü için birden çok (altı) mock-up görseli ürettiği söylenen bir skill. Belirli bir repo, paket veya yazar tespit edilemedi. Aday, tek bir tanımlı araçtan çok genel bir skill adı olarak görünüyor.
## Mekanizma
bilinmiyor. Video kanıtı yalnızca skill'in doğal dilde çağrıldığını gösteriyor. Arka uçta hangi görsel modelinin/API'nin kullanıldığı ve skill'in nasıl yapılandırıldığı doğrulanamadı.
## Kanıt
- Skill hero bölümü için altı mock-up üretir → sınanamadı · Yalnızca video konuşması ve karedeki 'Use your' metni var; repo/çalıştırılabilir kaynak bulunmadığı için üretim sınanamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Kurulum bilgisi yok: repo veya paket adı belirlenemedi.
- Kaynak bulunursa yeniden değerlendirilmeli; şu an kurulum önerilmez.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tasarım/arayüz akışında hero bölümü için hızlıca birden fazla görsel mock-up üretmek. Doğrulanmış bir fayda değil, videodaki tek cümlelik kullanıma dayanıyor.
## Maliyet/risk
Kaynağı, lisansı ve kodu belirsiz; içeriği incelenemeyen bir skill'i kurmak güvenlik riski taşır (istem/veri sızması, harici API anahtarı gereksinimi olasılığı). Görsel API maliyeti bilinmiyor. Yanlış tanımlama riski: aday belirli bir araç olmayabilir.
## Üretilebilir
hedef_tur: skill
tarif: SKILL.md yaz: (1) tetikleyici: 'mock-up/hero görseli üret'; (2) girdi: sayfa amacı, marka/renk, stil, adet N; (3) her varyasyon için farklı istem üretip kullanıcının seçtiği görsel API'sini (anahtar ortam değişkeninden okunur, dosyaya yazılmaz) çağıran küçük bir script (scripts/generate.py); (4) çıktıları mockups/hero-01..N.png olarak kaydet ve index.md ile istemleri listele; (5) maliyet uyarısı ve adet üst sınırı ekle.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short-2/panel.md → Ömer sütunu
## Özellikler
### Doğal dille 'image generation skill' çağrılarak hero bölümü için mock-up görselleri üretme (video iddiası, doğrulanmadı)
kaynak: https://www.youtube.com/watch?v=-_S3KD0ZIfI
## Destek
- -_S3KD0ZIfI · 0:09 · Hero bölümü için altı mock-up üretir · kanıt: Konuşmada 'Use your image generation skill' komutu geçiyor; karede 'Use your' yazısı başlıyor. (karede: Sağ üstte 'Use your' yazan küçük bir metin balonu ve sağda kısmen görünen panel.)
