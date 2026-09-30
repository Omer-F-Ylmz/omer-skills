# Agent view
ad: Agent view
tur: CLI
video: ZAaxx3qyT8g
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Bilinmiyor. Ayrı bir telemetri incelemesi yapılmadı. Claude Code'un genel telemetri ayarları geçerli olur.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Claude Code'un yerleşik özelliği olduğu için ayrıca yapılacak bir şey yok. Claude Code'u v2.1.139 veya üstüne güncelleyip `claude agents` çalıştırmak yeterli.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-3)
## Ne
Claude Code'un yerleşik özelliği: tüm Claude Code oturumlarını tek terminal ekranında listeleyip yöneten pano. `claude agents` komutuyla ya da bir oturumdan sol ok tuşuyla açılır. Oturumlar duruma göre gruplanır (sizi bekleyenler üstte, çalışanlar, bitenler altta); satırda oturum kimliği, bekleme durumu, son asistan yanıtı ve son etkileşim zamanı görünür; altta yeni iş göndermek için bir giriş alanı vardır.
## Mekanizma
Claude Code CLI'nin içinde çalışan bir TUI. Arka plandaki oturumların durumunu okuyup tek tabloda gösterir. Buradan oturuma girilebilir ya da yeni iş gönderilebilir. Kaynak kod açık değil. İç işleyiş ayrıntıları resmi dokümandan doğrulanmadı.
## Kanıt
- Tüm Claude Code oturumlarını tek terminal sekmesinde listeler ve durumlarını gösterir. → doğrulandı · Web araması: docs (code.claude.com/docs/en/agent-view) ve birkaç blog `claude agents` ile oturumların duruma göre gruplanıp listelendiğini anlatıyor. Kendim çalıştırıp denemedim. Video sayfasından yalnızca başlık alınabildi: 'Claude Code Just Got an Agent Dashboard'.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code'u v2.1.139 veya daha yeni bir sürüme güncelle.
- Terminalde `claude agents` komutunu çalıştır.
- Alternatif: herhangi bir oturumdayken sol ok tuşuna bas.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Birden çok paralel oturumu sekme sekme gezmeden tek ekrandan izlemeyi sağlar. Kullanıcıyı bekleyen oturumlar üstte görünür.
## Maliyet/risk
Research Preview aşamasında (11 Mayıs 2026'da çıktı), davranışı değişebilir. Kapalı kaynaklı, Claude Code sürümüne bağlı. Pro, Max, Team, Enterprise ve API kullanıcılarına açık.
## Tasarruf
Token tasarrufu sağlamaz. Amacı paralel oturumları görünür kılmak ve yönetmektir.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-3/panel.md → Ömer sütunu
## Özellikler
### `claude agents` komutu tüm oturumları tek tabloda açar. Oturumlar duruma göre gruplanır: bekleyenler, çalışanlar, bitenler.
kaynak: https://code.claude.com/docs/en/agent-view
### Satırda oturum kimliği, bekleme durumu, son yanıt ve zaman damgası görünür. Alttaki giriş alanından yeni iş gönderilir.
kaynak: https://claude.com/blog/agent-view-in-claude-code
### Video: tek sekmeden tüm oturumları görüntüleme ve yönetme.
kaynak: https://www.youtube.com/watch?v=ZAaxx3qyT8g
### Agent view: CLI'da çalışır; sol ok tuşu her oturumdan agent view'u açar.
video: ZAaxx3qyT8g · iddia: Agent view CLI'da çalışır; sol ok tuşu her oturumdan agent view'u açar.
sonuc: doğrulandı
arastirma: Resmi belge ve Anthropic blogunun arama sonuçlarına göre: "Press the left arrow from any session or run `claude agents` from the terminal to open agent view." Yani agent view CLI'da çalışır ve sol ok tuşu bir oturumdan agent view'u açar. Ek ayrıntılar: boş prompt'ta ← tuşu oturumdan ayrılıp tabloya döndürür. Kısayol, /config içindeki `leftArrowOpensAgents` ayarıyla ön plan oturumları için kapatılabilir. Aday dosyasındaki v2.1.139 ve üstü sürüm bilgisi ile Research Preview durumu bu aramada ayrıca doğrulanmadı. Kendim çalıştırıp denemedim; yalnızca arama sonucu özetlerine dayanıyor. Belge sayfasının tamamı okunmadı.
kaynak: https://code.claude.com/docs/en/agent-view
### Agent view araştırma önizlemesi (Research Preview) olarak kullanılabilir durumda.
video: -INveHwbRz4 · iddia: Agent view araştırma önizlemesi olarak kullanılabilir durumda.
sonuc: doğrulandı
arastirma: Anthropic'in resmi blogu ve Claude Code belgesi için yapılan web araması sonuçları iddiayı doğruluyor. Agent view bir Research Preview olarak sunuluyor. Pro, Max, Team, Enterprise ve Claude API planlarında kullanılabiliyor. `claude agents` komutuyla açılıyor. Tek ekrandan birçok Claude Code oturumu başlatılıp yönetilebiliyor. Oturumlar gruplanıyor: sizi bekleyenler, çalışanlar, bitenler. Satır seçilip Space'e basılınca peek paneli açılıyor. Panelde oturumun son çıktısı ya da beklediği soru görünüyor. Enter ile ekrandan çıkmadan yanıt gönderilebiliyor. Videodaki kare de (Needs input / Working / Completed başlıkları, "Agent view, now available") bununla uyuşuyor. Ben kendim çalıştırıp denemedim. Yalnızca arama sonucu özetlerine dayanıyor; belge sayfalarının tamamı okunmadı. Adayda geçen v2.1.139 ve üstü sürüm bilgisi ile 11 Mayıs 2026 çıkış tarihi bu aramada doğrulanmadı.
kaynak: https://claude.com/blog/agent-view-in-claude-code
## Destek
- ZAaxx3qyT8g · 0:44 · Tüm Claude Code oturumlarını tek terminal sekmesinde listeleyen ve yöneten görünüm; durumları gösterir. · kanıt: it lets you basically have one tab where you can not only view all of your sessions · iddia: Agent view CLI'da çalışır; sol ok tuşu her oturumdan agent view'u açar.
- -INveHwbRz4 · 0:19 · Claude Code'da birden çok ajan oturumunu durumlarına göre tek listede gösteren görünüm · kanıt: Kare oturumları Needs input, Working, Completed başlıklarıyla listeliyor; kapanışta 'Agent view, now available' yazıyor. (karede: Koyu terminal: Needs input (dark-mode, release-notes, load-test), Working (pr-review, perf-audit vb.), Completed (test-coverage); altta 'describe a task for a new session' ve 'enter to open · space to reply · ctrl+x to delete'.) · iddia: Agent view araştırma önizlemesi olarak kullanılabilir durumda.
