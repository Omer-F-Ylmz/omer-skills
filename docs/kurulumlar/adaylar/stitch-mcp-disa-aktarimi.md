# Stitch MCP dışa aktarımı
ad: Stitch MCP dışa aktarımı
tur: MCP
video: V-CIbnAAhc4
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor; Google hizmeti olduğundan tasarım istekleri Google'a gider, ayrıca telemetri politikası incelenmedi.
yildiz: bilinmiyor
alt_tur: servis
kullanim_kosullari: bilinmiyor; Google hesabı ve Stitch API anahtarı gerekir, resmi şartlar incelenmedi.
ucretsiz_katman: Aylık ~350 ücretsiz üretim, kredi kartı gerekmez (üçüncü taraf bloglara göre, doğrulanmadı).
veri_gizliligi: bilinmiyor; tasarım istemleri ve ekranlar Google sunucularında işlenir.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short)
## Ne
Google Stitch (yapay zekâ ile UI tasarımı üreten servis) tasarımlarını MCP üzerinden Claude Code gibi kodlama ajanlarına aktarır. Kopyala-yapıştır veya ekran görüntüsü olmadan ajan tasarımı doğrudan okur.
## Mekanizma
Stitch'te dışa aktarımda "MCP" ve ardından "Claude Code" seçilir; verilen bağlantı/yapılandırma Claude'a yapıştırılır (video). Claude Code, Stitch MCP sunucusuna bağlanır (.mcp.json, API anahtarı ile) ve blog kaynaklarına göre build_site, get_screen_code, get_screen_image gibi araçlarla ekran kodunu ve görselini çeker; Claude bunu React vb. koda çevirir. Ayrıntılar üçüncü taraf blog yazılarına dayanır, resmi dokümandan doğrulanmadı.
## Kanıt
- Dışa aktarımda MCP ve Claude Code seçilip bağlantı Claude'a yapıştırılır → doğrulandı · Video 0:22 ifadesi ve arama sonuçlarındaki blog yazıları (Stitch MCP + Claude Code kurulum rehberleri) aynı akışı anlatıyor.
- Ayda 350 ücretsiz üretim hakkı var → sınanamadı · Yalnızca arama özeti belirtiyor; resmi sayfadan doğrulanmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Stitch'te tasarımı oluştur, dışa aktarımdan MCP > Claude Code seç
- Verilen bağlantıyı/yapılandırmayı Claude Code'a yapıştır ya da proje kökündeki .mcp.json'a Stitch MCP sunucusunu ekle (API anahtarı ile; değer yazılmaz)
- Claude Code'u yeniden başlat ve Stitch araçlarının göründüğünü doğrula
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tasarımdan koda geçişte manuel dışa aktarma ve ekran görüntüsü yapıştırma adımını kaldırır; ajan tasarım kodunu/görselini doğrudan alır.
## Maliyet/risk
Kapalı Google servisi; API anahtarı yönetimi gerekir (.mcp.json'a sızdırma riski, repoya işlenmemeli). Servis/kota koşulları değişebilir. Bilgi çoğunlukla üçüncü taraf bloglardan; resmi doğrulama yapılmadı.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short/panel.md → Ömer sütunu
## Özellikler
### Claude Code, Cursor, Gemini CLI gibi 6+ ajanla çalışan Stitch MCP sunucusu
kaynak: https://sotaaz.com/post/stitch-mcp-guide-en
### build_site, get_screen_code, get_screen_image araçları; .mcp.json ile kurulum
kaynak: https://felixschmidt.software/en/blog/google-stitch-mcp-claude-code
### Gmail hesabıyla ayda 350 ücretsiz üretim (doğrulanmadı)
kaynak: https://justinmckelvey.com/blog/google-stitch-mcp
## Destek
- V-CIbnAAhc4 · 0:22 · Dışa aktarımda MCP ve Claude Code seçilir; bağlantı Claude'a yapıştırılır. · kanıt: MCP'yi seçiyoruz ve orada da cloud kodu seçiyoruz.
