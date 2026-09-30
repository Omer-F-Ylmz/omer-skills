# Higgsfield eklentisi (MCP)
ad: Higgsfield eklentisi (MCP)
tur: MCP
video: n5eIrepe-Fg
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Servis bulutta çalışıyor ve istekler/istemler Higgsfield'e gidiyor, kullanım hesaba bağlı. Ayrıntılı telemetri politikası incelenmedi.
yildiz: bilinmiyor
alt_tur: servis
kullanim_kosullari: Kullanım koşulları incelenmedi (bilinmiyor). Hesap ve kredi tabanlı kullanım. Üretilen içeriğin ticari kullanım hakları planlara göre değişebilir, doğrulanmadı.
ucretsiz_katman: Sınırlı kredili ücretsiz katman (görsel üretimi açık). MCP bağlayınca 3 gün süreli 100 kredilik deneme. Ücretli planlar (3. taraf kaynaklara göre, 14 Eylül 2026): Starter $15/ay 200 kredi, Plus $39/ay 1.000 kredi, Ultra $99/ay 3.000 kredi. Image-to-video için en az Plus gerekiyor.
veri_gizliligi: bilinmiyor. İstemler ve yüklenen medya Higgsfield bulutuna gönderiliyor. Saklama ve model eğitimi politikası incelenmedi.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-2)
## Ne
Higgsfield'in resmi uzak MCP sunucusu/eklentisi (Nisan 2026'da duyuruldu). Claude, ChatGPT, Codex ve MCP uyumlu ajanlardan görsel, video (ve videodaki ses) üretmeyi sağlıyor. 30'dan fazla model sunuyor. Video ChatGPT/Codex içinden kurulumu gösteriyor.
## Mekanizma
Sunucu Higgsfield'in bulutunda çalışıyor (https://mcp.higgsfield.ai/mcp). İstemci bu adrese uzak MCP olarak bağlanıyor. Kullanıcı Higgsfield hesabıyla OAuth benzeri bir girişle yetkilendiriyor, API anahtarı gerekmiyor. Ajan üretim araçlarını çağırıyor, üretim Higgsfield tarafında hesabın kredisiyle yapılıyor. Claude Code/Codex için ayrıca CLI (@higgsfield/cli) ve yardımcı skill paketi var (arama sonuçlarına göre, doğrulanmadı).
## Kanıt
- Higgsfield eklentisi ChatGPT/Codex içinden görsel, video ve ses üretiyor → sınanamadı · Videoda anlatılıyor; video metni getirilemedi (getir komutu URL bekliyordu). Arama sonuçları resmi MCP ve ChatGPT eklentisi sayfalarının varlığını gösteriyor.
- Kurulum kolay, MCP'den doğrudan kullanılıyor → doğrulandı · higgsfield.ai/mcp ve yardım merkezi sayfaları, uzak URL ile eklemeyi ve API anahtarı gerekmediğini belirtiyor (arama özeti; sayfa içeriği doğrudan okunmadı).
- Ücretsiz kullanım mümkün → sınanamadı · Arama özeti: ücretsiz katman sınırlı kredi, MCP bağlayınca 3 gün/100 kredi deneme. Hesapla denenmedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- ChatGPT: Plugins Directory'de Higgsfield'i bulup 'Add' de, ya da higgsfield.ai/mcp sayfasından 'Add Higgsfield plugin' seç
- Claude (web/Desktop): Settings → Connectors → Add custom connector, ad 'Higgsfield', URL https://mcp.higgsfield.ai/mcp
- Claude Code/Codex (CLI yolu): npm i -g @higgsfield/cli ; higgsfield auth login ; npx skills add higgsfield-ai/skills
- Higgsfield hesabına giriş yapıp yetki ver
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Kod ajanından çıkmadan görsel/video/ses varlığı üretmek. Sosyal medya içeriği, ürün görseli ve prototip varlıkları için kullanışlı. Ayrı bir arayüze geçme ihtiyacını ortadan kaldırıyor.
## Maliyet/risk
Ücretli kredi tüketimi (ajan kontrolsüz üretim yapabilir, maliyet sınırı koy). İstemler ve yüklenen görseller üçüncü tarafa gidiyor. Kapalı kaynak servis, lisans/telemetri belirsiz. Fiyat ve plan bilgisi üçüncü taraf sayfalara dayanıyor, değişebilir. Image-to-video için en az Plus plan gerektiği bildirilmiş.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-2/panel.md → Ömer sütunu
## Özellikler
### Uzak MCP sunucusu: https://mcp.higgsfield.ai/mcp, API anahtarı gerekmiyor, 30+ görsel/video modeli
kaynak: https://higgsfield.ai/mcp
### ChatGPT için eklenti dizininden tek tıkla ekleme
kaynak: https://higgsfield.ai/chatgpt-plugin?tab=claude-code
### Claude Code/Codex için CLI ve skill paketi
kaynak: https://higgsfield.ai/chatgpt-plugin?tab=claude-code
### Claude veya ChatGPT'ye bağlanma rehberi
kaynak: https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent
## Destek
- n5eIrepe-Fg · 2:02 · ChatGPT/Codex içinden görsel, video ve ses üretmek için Higgsfield plugin/MCP; 'add' ile çağrılır. · kanıt: Hixfield eklentisini kuracağız... MCP'den kullanmaya başlayabiliyorsunuz direkt.
