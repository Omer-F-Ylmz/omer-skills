# frontend-design skill (özelleştirilmiş)
ad: frontend-design skill (özelleştirilmiş)
tur: skill
video: BdLrWHzdYt4
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Skill salt markdown talimatıdır, kendi başına ağ çağrısı veya telemetri yapmaz. Yazarın değiştirilmiş dosyasını görmediğim için içinde betik veya harici bağlantı olup olmadığı doğrulanmadı.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Orijinal anthropics/skills frontend-design skill'i zaten kurulabilir. Yazarın değişikliklerine erişim yok; aynı işi kendi türev skill'imizle yapabiliriz.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-3)
## Ne
Anthropic'in resmi frontend-design skill'inin (anthropics/skills deposunda skills/frontend-design) video yazarı tarafından kendi ihtiyacına göre biraz değiştirilmiş hâli. Videonun sayfa başlığı: 'Claude Code + Nano Banana Pro + Kling AI Kullanarak 3D Websiteleri Oluştur'. Değiştirilmiş dosya yazarın ücretsiz topluluğunda paylaşılıyor; herkese açık bir repo yok.
## Mekanizma
Skill, YAML frontmatter (name, description) ve markdown talimatlarından oluşan bir SKILL.md dosyasıdır. Claude, frontend/arayüz işi istendiğinde bu talimatları yükler ve sıradan, jenerik görünümlü çıktı yerine belirgin bir estetik yön seçen, tasarım odaklı kod üretir. Yazarın hangi kısımları değiştirdiği doğrulanamadı: değiştirilmiş dosya erişilebilir değil, video özeti de bunu vermiyor. Orijinal skill'in içeriğini de bu oturumda okumadım; yalnızca deponun dizin ağacında varlığını gördüm.
## Kanıt
- Video, orijinal frontend design skill'inin yazar tarafından değiştirilmiş hâlini paylaşıyor. → sınanamadı · Video sayfası çekildi ama yalnızca başlık ve YouTube alt bilgisi geldi; açıklama ve altyazı yoktu. İddia yalnızca verilen video bulgusuna dayanıyor.
- Orijinal skill anthropics/skills deposunda mevcut. → doğrulandı · `video repo anthropics/skills` çıktısının ağacında skills/frontend-design klasörü var.
- Değiştirilmiş dosya ücretsiz toplulukta paylaşılıyor. → sınanamadı · Topluluk bağlantısı ve dosya erişilebilir değil.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Orijinal: Claude Code içinde `/plugin marketplace add anthropics/skills`, ardından `/plugin install example-skills@anthropic-agent-skills` (depo README'sinden).
- Özelleştirilmiş sürüm: yazarın ücretsiz topluluğuna üye olup dosyayı indirmek ve ~/.claude/skills/frontend-design/SKILL.md yoluna koymak gerekir (topluluk erişimi doğrulanmadı).
- Alternatif: orijinal skills/frontend-design/SKILL.md dosyasını kopyalayıp kendi tercihlerimize göre düzenlemek.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Jenerik 'yapay zekâ' görünümlü arayüzler yerine daha özgün ve iddialı frontend tasarım çıktısı verir. Yazarın kişisel ayarlarını da taşır, ama bu ayarların ne olduğu bilinmiyor.
## Maliyet/risk
Değiştirilmiş dosya kapalı bir toplulukta duruyor: kaynağı, sürümü ve lisansı doğrulanamıyor. Orijinal depo README'sine göre skills deposundaki birçok skill Apache 2.0, ama frontend-design'ın lisansını tek tek doğrulamadım; türev dosyanın yeniden dağıtım hakkı belirsiz. Topluluk dosyası harici komut veya betik içerebilir, kullanmadan önce incelenmeli. Video ayrıca ücretli üçüncü taraf araçlara (Nano Banana Pro, Kling AI) dayanıyor.
## Üretilebilir
hedef_tur: skill
tarif: Orijinal anthropics/skills içindeki frontend-design/SKILL.md dosyasını (lisansını kontrol ederek) temel al. Kendi skill'imizi omer-skills altında frontend-design-ozel adıyla oluştur. Ekle: (1) tercih ettiğimiz estetik yönler ve yasak jenerik kalıplar, (2) tipografi, renk ve hareket kuralları, (3) 3D/animasyonlu landing page için isteğe bağlı bölüm. Yazarın kapalı dosyasını kopyalama; onun yerine kendi değişikliklerimizi yaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-3/panel.md → Ömer sütunu
## Özellikler
### Orijinal frontend-design skill'i resmî anthropics/skills deposunda bulunuyor ve Claude Code plugin marketplace üzerinden kurulabiliyor.
kaynak: https://github.com/anthropics/skills
### Video: Claude Code ile 3D web sitesi üretimi iş akışı; frontend design skill'inin değiştirilmiş hâli bu akışta kullanılıyor.
kaynak: https://www.youtube.com/watch?v=BdLrWHzdYt4
## Destek
- BdLrWHzdYt4 · 1:02 · Orijinalinden yazarın değiştirdiği frontend tasarım skill'i; ücretsiz toplulukta paylaşılıyor. · kanıt: Orijinal dosyayı alıp kendim için biraz değiştirdiğim frontend design skilli.
