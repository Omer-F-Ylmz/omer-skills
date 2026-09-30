# Google Stitch
ad: Google Stitch
tur: MCP
video: V-CIbnAAhc4
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Bulut servisi olduğu için istemler ve tasarımlar Google'a gider. Ayrıca bir telemetri incelemesi yapılmadı.
yildiz: bilinmiyor
alt_tur: servis
kullanim_kosullari: bilinmiyor. Resmî kullanım şartları okunmadı. Beta döneminde ücretsiz olduğu belirtiliyor.
ucretsiz_katman: Beta döneminde ücretsiz. Kaynaklara göre Google hesabı ve ücretsiz API anahtarı yeterli. Kota sınırları bilinmiyor.
veri_gizliligi: bilinmiyor. İstemler ve tasarımlar Google bulutuna gider. Eğitimde kullanılıp kullanılmadığı doğrulanmadı.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short)
## Ne
Google'ın yapay zekâ destekli arayüz tasarım servisi (stitch.withgoogle.com). Metin isteminden site/uygulama ekranları ve ön yüz kodu üretir. MCP ile Claude Code, Cursor, Gemini CLI gibi kodlama ajanlarına bağlanır.
## Mekanizma
Kullanıcı Stitch'te (Gemini modelleriyle) istemden ekranlar üretir. MCP sunucusu, Stitch projesine API anahtarıyla erişir. Kaynaklara göre üç araç sunuyor: build_site, get_screen_code, get_screen_image. Ajan tasarımın kodunu ve görselini çeker, kopyala-yapıştır olmadan koda çevirir. Bu araç adları yalnızca üçüncü taraf blog yazılarından geliyor. Resmî belgeyle doğrulamadım. Ayrıca topluluk yapımı sarmalayıcılar var (ör. kargatharaakash/stitch-mcp).
## Kanıt
- Ücretsiz sistem → doğrulandı · Arama sonuçlarındaki bloglar Stitch'in beta döneminde ücretsiz olduğunu ve Google hesabı ile ücretsiz API anahtarı istediğini yazıyor. Resmî sayfadan teyit edilmedi. Ücretsiz durumu beta süresine bağlı.
- MCP ile Claude Code'a bağlanır → doğrulandı · Birden çok kaynak (Felix Schmidt, SOTAAZ, MetaWhisp, Google codelab'ı) Stitch MCP'nin Claude Code, Cursor ve Gemini CLI ile çalıştığını anlatıyor.
- Site/uygulama arayüzleri tasarlar → doğrulandı · Kaynaklar metinden UI tasarımı ve ön yüz kodu üretimini tarif ediyor. Videoda karede ekranlar üretiliyor.
- Tek tıkla koda dökme (video başlığı) → sınanamadı · Bu yalnızca video başlığı. Ürettiği kodun kalitesini denemedim.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- stitch.withgoogle.com'a Google hesabıyla giriş yap
- Proje ayarlarındaki API bölümünden API anahtarı üret (anahtarı depoya yazma)
- MCP sunucusunu Claude Code'a ekle (ör. `claude mcp add ...`). Güncel komut ve paket adı için resmî Stitch belgesine veya Google codelab'ına bak
- Ajana 'şu paneli tasarla ve uygula' de; ajan Stitch araçlarını çağırır
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tasarımdan koda geçişi hızlandırır. Ajan, tasarım görselini ve kodunu doğrudan okuyabildiği için elle tarif etmek gerekmez. Beta döneminde ücretsiz.
## Maliyet/risk
Beta olduğu için fiyat, kota ve API değişebilir. Kapalı kaynak ve bulut bağımlısı. Tasarım verisi Google'a gider. Lisans ve veri kullanımı doğrulanmadı. MCP kurulum bilgisi çoğunlukla üçüncü taraf bloglardan geliyor. Topluluk sarmalayıcıları güvenilirlik açısından ayrıca denetlenmeli.
## Üretilebilir
hedef_tur: skill
tarif: Stitch'in kendisi üretilemez, çünkü tasarım modeli Google'da. Ama bir skill yazılabilir. Skill, Stitch MCP'yi çağırma sırasını tarif eder: markaya uygun istem oluştur, ekranları üret, get_screen_code ile kodu çek, projenin tasarım sistemine (renk, bileşen) uydur. Repoya sabit bir DESIGN.md şablonu ekle. Anahtarı ortam değişkeninden oku.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short/panel.md → Ömer sütunu
## Özellikler
### MCP araçları: build_site, get_screen_code, get_screen_image (üçüncü taraf kaynağa göre)
kaynak: https://metawhisp.com/blog/google-stitch-mcp/
### Claude Code, Cursor ve Gemini CLI ile kurulum rehberi
kaynak: https://sotaaz.com/post/stitch-mcp-guide-en
### Google resmî codelab'ı: Antigravity ile tasarımdan koda
kaynak: https://codelabs.developers.google.com/design-to-code-with-antigravity-stitch
### Beta döneminde ücretsiz. Google hesabı ve API anahtarı gerekir
kaynak: https://justinmckelvey.com/blog/google-stitch-mcp
### Google Stitch ücretsiz bir arayüz tasarım sistemidir (metinden site/uygulama ekranı ve ön yüz kodu üretir; MCP ile kodlama ajanlarına bağlanır).
video: V-CIbnAAhc4 · iddia: Google Stitch ücretsiz bir arayüz tasarım sistemidir.
sonuc: doğrulandı
arastirma: Bir kez WebSearch yaptım. Stitch, Google Labs deneyi olarak sunuluyor. Google hesabıyla giriş yapılıyor, abonelik, ücretli katman ya da kart istenmiyor. Kullanım günlük bir kotayla sınırlı ve bu kota parayla artırılamıyor. Kota rakamları kaynaktan kaynağa değişiyor. Eski kaynaklar Standart modda (Gemini 2.5 Flash) ayda 350, Pro/Experimental modda (Gemini 2.5 Pro) ayda 200 üretim diyor. Nisan 2026 tarihli Stitch 2.0 kaynakları günlük 400 tasarım kredisi ve 15 yeniden tasarım kredisi diyor. Kredi karmaşıklığa göre harcanıyor: tek sayfalık basit bir istem yaklaşık 3 kredi, çok ekranlı uygulamalar iki haneli kredi tutuyor. Bu yüzden özellik doğrulandı ama şartlı: "ücretsiz" doğru, ancak kotalı ve deneme (Labs/beta) statüsünde. Google kotaları birkaç kez değiştirmiş, gelecekte ücretli katman gelebilir. Bu bilgilerin hepsi üçüncü taraf inceleme ve blog yazılarından geliyor (index.dev, uxmagic, nxcode, banani vb.). Resmî Google sayfası ya da kullanım şartlarını okumadım. Video karesinde Stitch'te ekranların üretildiği görülüyor, bu da aracın arayüz tasarladığını destekliyor. Sorulan tek şey ücretsizlik iddiasıydı. MCP araç adları (build_site, get_screen_code, get_screen_image) da yalnızca üçüncü taraf kaynaklara dayanıyor, resmî belgeyle doğrulanmadı. Lisans, veri gizliliği (istemlerin eğitimde kullanılıp kullanılmadığı) ve telemetri bilinmiyor. "Ücretsiz" ifadesi güvenli gizlilik anlamına gelmez, çünkü istemler ve tasarımlar Google bulutuna gidiyor.
kaynak: https://uxmagic.ai/blog/google-stitch-pricing
## Destek
- V-CIbnAAhc4 · 0:17 · Site/uygulama arayüzleri tasarlayan ücretsiz sistem; MCP ile Claude Code'a bağlanır. · kanıt: Karede Stitch'te ekranlar üretiliyor; altyazı 'tasarım sistemiyle'. (karede: Koyu arayüzde dört 'Generating screen.' kutusu, altta 'What would you like to change or create?' giriş alanı ve '3 Flash' seçici; altta konuşmacı.) · iddia: Google Stitch ücretsiz bir arayüz tasarım sistemidir.
