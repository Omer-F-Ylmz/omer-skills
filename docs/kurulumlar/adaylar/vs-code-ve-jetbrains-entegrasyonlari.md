# VS Code ve JetBrains entegrasyonları
ad: VS Code ve JetBrains entegrasyonları
tur: plugin
video: gv0WHhKelSE
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor — bu eklentiler için ayrı telemetri politikası doğrulanamadı; Claude Code'un genel telemetri ayarları geçerli varsayılır.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Claude Code'un kendisi zaten resmi eklentiyi sağlıyor; ek üretim gerekmez. Kurulum, ilgili IDE'ye eklentiyi yüklemekten ibaret. Bizde ayrı bir karşılık yok, resmi eklenti doğrudan kullanılır.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-3)
## Ne
Anthropic'in Claude Code için sunduğu resmi IDE eklentileri. VS Code (ve Cursor gibi türevleri) için yerel uzantı, JetBrains IDE'leri (IntelliJ, PyCharm, WebStorm, PhpStorm, GoLand, Android Studio) için marketplace eklentisi. Claude'a hangi dosyada, hangi seçimde olduğunuzu bildirir.
## Mekanizma
Eklenti IDE ile Claude Code CLI arasında köprü kurar. Aktif dosya yolu, imleç konumu ve seçili metin isteme eklenir; JetBrains'te CLI'yi saran bir katmandır ve Claude, yerleşik 'ide' MCP sunucusu üzerinden IDE'nin denetim (inspection) tanılarını isteyebilir. VS Code uzantısı ayrıca grafik sohbet paneli, checkpoint tabanlı geri alma, @-ile dosya anma ve paralel konuşma sunar. (Kaynak: arama sonuçlarındaki özetler; video sayfasından transkript alınamadı, yalnızca video başlığı doğrulandı.)
## Kanıt
- IDE entegrasyonu Claude'un hangi dosyada olduğunuzu bilmesini sağlar. → doğrulandı · Arama sonuçları: JetBrains eklentisi aktif seçimi ve dosya yolunu istemle birlikte iletir; entegrasyon açık dosyaları ve imleç konumunu görür (code.claude.com/docs/en/jetbrains).
- VS Code 1.94 veya üstü gerekir. → doğrulandı · Arama sonucu özetleri bunu belirtiyor; resmi sayfa doğrudan açılmadı, ikincil kaynak.
- Video (gv0WHhKelSE) bu özellikleri anlatıyor. → sınanamadı · Video getirme yalnızca sayfa başlığını (Claude Code best practices / Code w/ Claude) döndürdü, transkript yok.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- VS Code: Uzantılar sekmesinden Claude Code uzantısını kur (VS Code 1.94+ gerekir).
- JetBrains: Marketplace'ten 'Claude Code [Beta]' eklentisini kur ve IDE'yi yeniden başlat.
- Claude Code CLI'yi kur ve Anthropic aboneliği/Console hesabı veya desteklenen üçüncü taraf sağlayıcıyla oturum aç.
- IDE'nin entegre terminalinde claude çalıştır; bağlantı otomatik kurulur.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude'un bağlamı (açık dosya, seçim, terminal çıktısı, IDE tanıları) otomatik alması; diff'lerin IDE'de görülmesi; VS Code'da geri alma noktaları ve paralel sohbetler.
## Maliyet/risk
Kapalı kaynak/lisansı doğrulanamadı; Claude Code CLI'ye bağımlı; JetBrains eklentisi Beta etiketli. IDE içeriği (açık dosya/seçim) modele gönderilir. Video kanıtı yalnızca başlık düzeyinde; transkript alınamadı.
## Tasarruf
Token aracı değil. Dolaylı olarak dosya yolunu/seçimi otomatik vererek elle yapıştırmayı azaltabilir; ölçülmedi.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-3/panel.md → Ömer sütunu
## Özellikler
### JetBrains: aktif seçim ve dosya yolu isteme eklenir; yerleşik 'ide' MCP sunucusuyla IDE tanıları istenebilir
kaynak: https://code.claude.com/docs/en/jetbrains
### VS Code: grafik sohbet paneli, checkpoint tabanlı geri alma, @-mention dosya referansı, paralel konuşmalar; Cursor ve uyumlu forklarda çalışır
kaynak: https://docs.anthropic.com/en/docs/claude-code/ide-integrations
### JetBrains eklentisi CLI'yi saran katmandır; IntelliJ, PyCharm, WebStorm, PhpStorm, GoLand, Android Studio desteklenir
kaynak: https://plugins.jetbrains.com/plugin/27310-claude-code-beta-
## Destek
- gv0WHhKelSE · 20:30 · IDE entegrasyonu Claude'un hangi dosyada olduğunuzu bilmesini sağlar. · kanıt: new great integrations with VS Code and Jet Brains
