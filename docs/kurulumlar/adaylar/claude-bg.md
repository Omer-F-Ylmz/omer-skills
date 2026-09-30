# claude --bg
ad: claude --bg
tur: CLI
video: ZAaxx3qyT8g
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Bilinmiyor. Claude Code'un kendi telemetri ayarları geçerlidir; bu bayrağa özgü ek telemetri doğrulanmadı.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Claude Code'un yerleşik özelliği olduğu için ayrıca kurulum gerekmez; sürüm güncel olmalı. Kısmi benzeri: `claude -p "görev"` ile arka plan kabuk işi başlatmak (agent view olmadan).
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-3)
## Ne
Claude Code'un komut satırı bayrağı: görevi tırnak içinde verilen yeni bir oturumu arka planda başlatır ve doğrudan agent view (ajan panosu) içine yerleştirir.
## Mekanizma
Video bulgusuna göre `claude --bg "görev"` şeklinde çağrılır; görev metni tırnak içinde verilmelidir. Oturum ön planda tutulmadan agent view'da izlenir. Farklı dizinlerde çalışırken kullanışlıdır (her dizinden oturum başlatıp tek panoda görmek). İç işleyiş (süreç yönetimi, kalıcılık) doğrulanmadı; resmi dokümana bakılmadı.
## Kanıt
- Görev tırnak içinde verilmeli ve oturum doğrudan agent view'da başlar; farklı dizinlerde çalışmak için kullanışlı. → sınanamadı · Yalnızca video bulgusu (ZAaxx3qyT8g, 4:20, 'you have to wrap it in quotes'). Sayfa getirme yalnızca YouTube alt bilgisi döndürdü, döküm alınamadı; komut yerelde çalıştırılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code'un agent view içeren güncel sürümü gerekir (sürüm numarası bilinmiyor)
- Kullanım: claude --bg "görev metni"
- Bayrağın varlığı için `claude --help` ile kontrol edin
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Birden çok görevi/dizini paralel ve arka planda yürütüp tek panodan izlemeyi sağlar; terminali bloklamaz.
## Maliyet/risk
Kapalı kaynak, Claude Code'un parçası; sürüme bağımlı ve deneysel olabilir. Arka planda çalışan oturumlar izin/onay ve kullanım (token) maliyeti açısından dikkatsizce çoğaltılabilir. Yalnızca tek bir video kaynağına dayanıyor; resmi doküman doğrulanmadı.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-3/panel.md → Ömer sütunu
## Özellikler
### Tırnak içinde verilen görevle yeni oturumu doğrudan agent view'da başlatma
kaynak: https://www.youtube.com/watch?v=ZAaxx3qyT8g
## Destek
- ZAaxx3qyT8g · 4:20 · Görevi tırnak içinde verilen yeni bir oturumu doğrudan agent view'a başlatır; farklı dizinlerde çalışmak için kullanışlı. · kanıt: you have to wrap it in quotes
