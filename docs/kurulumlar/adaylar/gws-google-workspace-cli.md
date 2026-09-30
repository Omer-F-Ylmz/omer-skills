# GWS (Google Workspace CLI)
ad: GWS (Google Workspace CLI)
tur: CLI
video: V2RIVnGCy74
repo: googleworkspace/cli
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/googleworkspace/cli
telemetri: bilinmiyor. Sağlanan README bölümünde telemetri açıklaması yok. Ağ çağrıları Google API'lerine ve Discovery Service'e gidiyor. Kaynak kodu denetlenmedi.
yildiz: bilinmiyor
alt_tur: araç
skillspector: SkillSpector --no-llm: 278 HIGH/CRITICAL bulgu (ön tarama). Bulgular incelenmedi, yanlış pozitif olasılığı var.
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Drive, Gmail, Calendar, Sheets, Chat gibi tüm Google Workspace API'leri için tek bir komut satırı aracı (gws). İnsanlar ve yapay zekâ ajanları için yazılmış. Çıktı yapılandırılmış JSON. 40'tan fazla ajan skill'i (haftalık özet, toplantı hazırlığı, e-postadan göreve) içeriyor. Resmî Google ürünü değil.
## Mekanizma
Sabit bir komut listesi yok. gws çalışma anında Google'ın Discovery Service'ini okuyup komut yüzeyini dinamik üretiyor. Google yeni bir API uç noktası eklediğinde gws bunu otomatik alıyor. Komutlar `gws <servis> <kaynak> <yöntem> --params '{...}' --json '{...}'` biçiminde. Her kaynakta --help var. --dry-run isteği göndermeden önizliyor. --page-all sayfalamayı otomatik yapıp NDJSON akıtıyor. `gws schema drive.files.list` bir yöntemin istek/yanıt şemasını gösteriyor. Kimlik doğrulama OAuth (`gws auth setup/login`), hazır erişim token'ı, kimlik bilgisi dosyası ya da servis hesabıyla yapılıyor. Kod Rust (crates/google-workspace-cli), npm paketi yalnızca GitHub Releases'tan ikili dosyayı indiriyor. skills/ klasöründeki SKILL.md dosyaları ajana gws komutlarını nasıl kullanacağını anlatıyor.
## Kanıt
- 40'tan fazla hazır skill içeriyor → doğrulandı · README 'AI Agent Skills' bölümünü ve '40+ agent skills included' ifadesini içeriyor. Ağaçta skills/ altında gws-admin-reports, gws-calendar-agenda, gws-calendar-insert, gws-chat-send gibi klasörler var (90 satır kesildi). Tam sayı sayılmadı.
- Kurulum biraz daha karmaşık olabilir → doğrulandı · README'ye göre Google Cloud projesi, OAuth kimlik bilgileri ve gws auth setup/login adımları gerekiyor.
- Google bağlayıcısında olmayan işlevler (e-posta gönderme) sunuyor → sınanamadı · README Gmail'i kapsadığını söylüyor. Bağlayıcıyla karşılaştırma yapılmadı ve komut çalıştırılmadı.
- Gayriresmî bir araç → doğrulandı · README: 'This is not an officially supported Google product.'
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 278
## Kurulum
- Önerilen: GitHub Releases sayfasından işletim sisteminize uygun ikili dosyayı indirip PATH'e koyun
- npm install -g @googleworkspace/cli (Node.js 18+ gerekir)
- brew install googleworkspace-cli (macOS/Linux)
- cargo install --git https://github.com/googleworkspace/cli --locked
- nix run github:googleworkspace/cli
- gws auth setup (Google Cloud projesi yapılandırması), ardından gws auth login
- Deneme: gws drive files list --params '{"pageSize": 5}'
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Google'ın kendi bağlayıcısında olmayan işlevleri (e-posta gönderme dahil, videoya göre) ajana açıyor. Tüm Workspace API'lerini tek araçla kapsıyor. Hazır skill'ler haftalık özet, toplantı hazırlığı ve e-postadan göreve dönüştürme gibi iş akışlarını kolaylaştırıyor.
## Maliyet/risk
Resmî olarak desteklenmiyor. README, v1.0'a kadar kırıcı değişiklikler olabileceğini söylüyor. Kurulum karmaşık: Google Cloud projesi ve OAuth gerekiyor. Ajan Gmail, Drive ve Takvim'e yazma yetkisi alıyor, bu yüzden yanlış gönderim ya da silme riski var. Kapsamları dar tutmak ve önce --dry-run kullanmak gerekir. Ön güvenlik taraması (SkillSpector --no-llm) 278 HIGH/CRITICAL bulgu verdi. Bulguların gerçek mi yanlış pozitif mi olduğu incelenmedi. Skill sayısı ve Rust kodunun büyüklüğü sayıyı şişirmiş olabilir. Lisans dosyası var ama türü okunmadı.
## Tasarruf
Token aracı değil. Dolaylı fayda: yapılandırılmış JSON çıktı ve hazır skill'ler, ajanın özel entegrasyon kodu yazma ve REST dokümanı okuma maliyetini azaltabilir. Bu ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: gws'yi kopyalamaya gerek yok, olduğu gibi kullanılır. Kendi skill'imizi yazmak için: gws'yi kurup kimlik doğrulamasını yapın. Sonra SKILL.md dosyası yazın. Dosya gws gmail/calendar/drive komutlarını çağırsın, --dry-run ile önizlesin, çıktıyı JSON olarak işlesin ve göndermeden önce kullanıcıdan onay istesin. Örnek akışlar: haftalık özet, toplantı hazırlığı, e-postadan göreve. Yazma yetkisi gerektiren komutları açık onaya bağlayın. Repodaki skills/ klasörü şablon olarak kullanılabilir ama önce güvenlik bulguları incelenmeli.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### Discovery Service'ten çalışma anında dinamik komut üretimi, yeni API'ler otomatik gelir
kaynak: https://github.com/googleworkspace/cli
### Yapılandırılmış JSON çıktı, --dry-run, --page-all (NDJSON), gws schema ile şema sorgulama
kaynak: https://github.com/googleworkspace/cli
### 40'tan fazla ajan skill'i (skills/ klasörü, docs/skills.md)
kaynak: https://github.com/googleworkspace/cli/tree/main/skills
### Çoklu kimlik doğrulama: OAuth, hazır token, kimlik dosyası, servis hesabı
kaynak: https://github.com/googleworkspace/cli
### Çok kanallı dağıtım: Releases ikilisi, npm, Homebrew, cargo, Nix, Gemini uzantısı
kaynak: https://github.com/googleworkspace/cli
## Destek
- V2RIVnGCy74 · 9:04 · Google Workspace için gayriresmî CLI; e-posta gönderme dahil Google bağlayıcısında olmayan işlevler ve 40+ hazır skill (haftalık özet, toplantı hazırlığı, e-postadan göreve). · kanıt: 40'tan fazla skill içeriyor; kurulumu biraz daha karmaşık olabilir. (karede: İlgili kare yok; altyazıdan.)
