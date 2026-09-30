# Open Design
ad: Open Design
tur: skill
video: L2JKgj7WzU4
repo: nexu-io/open-design
lisans: Apache-2.0
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/nexu-io/open-design
telemetri: bilinmiyor. Depoda PRIVACY.md var ama içeriği okunmadı; telemetri durumu doğrulanmadı. Kurmadan önce PRIVACY.md okunmalı.
yildiz: bilinmiyor
alt_tur: bilinmiyor
skillspector: atlandı (repo 3427 MB)
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Açık kaynaklı, "Claude Design alternatifi" olarak konumlanan, ortak çalışmaya dayalı bir tasarım ajanı çalışma alanı (OpenDesign). Brief'ten başlayıp mevcut kodlama ajanınızla (veya OpenDesign Cloud ile) tasarım sistemine uyan prototip, slayt, görsel ve HyperFrames hareketli grafik (MP4) üretir. Skill, tasarım şablonu, tasarım sistemi ve eklentiler (plugin) sunar.
## Mekanizma
README'ye göre iki yolla ajanlara bağlanır: (1) OD'yi tüketen ajanlar için skill/CLI/MCP (`od mcp install <ajan>`: claude, codex, cursor, opencode, copilot, cline, kiro, hermes vb.), (2) OD'nin doğrudan başlattığı yerel runtime adaptörleri (örn. DeepSeek Harness `dsh`; yapılandırılmış akış, model keşfi, iptal, oturum devam ettirme). Depoda apps/daemon, apps/web, apps/desktop var; yani yerel bir daemon + web arayüzü + masaüstü paketi mimarisi görünüyor. craft/ klasöründe tasarım kalite kılavuzları (anti-ai-slop, renk, tipografi, erişilebilirlik, durum kapsamı, UX yasaları) bulunuyor. Tarayıcı uzantısı (clipper) marka yakalama için var. Ayrıntılı iç işleyiş kaynak kodundan doğrulanmadı; yukarıdakiler README ve dosya ağacından çıkarıldı.
## Kanıt
- Lisans Apache 2.0 → doğrulandı · README rozeti ve 'licensed under Apache 2.0' metni. LICENSE dosyası ağaçta var ama içeriği okunmadı.
- 13 kodlama ajanı CLI'ı otomatik algılanıyor (video) → sınanamadı · README'deki uyumluluk tablosunda 19 ajan/platform listeli ve 'od mcp install' ile kurulum var. 'Otomatik algılama' ifadesi README'de görülmedi.
- 31 tasarım skill'i ve 72 marka sınıfı tasarım sistemi (video) → sınanamadı · Kesilmiş README ve ağaçta sayılar görülmedi. Video transkripti de alınamadı (sayfa yalnızca başlık verdi).
- güvenlik ön taraması: atlandı (repo 3427 MB)
## Kurulum
- README'de hızlı başlangıç 3 komut denmiş (QUICKSTART.md); komutlar görülmedi, bilinmiyor
- Ajan bağlama: `od mcp install claude` (önizleme için `--print`, kaldırmak için `--uninstall`, liste: `od mcp install --help`)
- DeepSeek Harness için: önce resmi `dsh` CLI, sonra `od agent setup deepseek-harness`
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Kendi kodlama ajanınızla (Claude Code, Codex, Cursor vb.) marka/tasarım sistemine uygun prototip, slayt ve görsel üretmek için hazır skill, tasarım sistemi ve kalite kılavuzu seti sağlar. Ayrı bir tasarım aracı aboneliğine gerek bırakmayabilir.
## Maliyet/risk
Büyük ve hızlı değişen bir monorepo (3427 MB). Güvenlik taraması atlandı. Telemetri ve veri akışı doğrulanmadı. Ticari katman (OpenDesign Go, $8'dan başlayan plan, Cloud) var; bazı özellikler ücretli bulut olabilir. README'de geçen bazı model adları ve sürümler (GPT-6.1 Sol vb.) doğrulanmadı. Kendi makinede daemon çalıştırır ve MCP ile ajanlara yazma/okuma erişimi verir; kurulumdan önce `--print` ile önizleme yapılmalı.
## Üretilebilir
hedef_tur: skill
tarif: Kendi skill'imiz için craft/ klasöründeki fikirler (anti-ai-slop, durum kapsamı, erişilebilirlik kontrol listesi, tipografi hiyerarşisi) Apache-2.0 lisansı ve atıf şartıyla uyarlanabilir. SKILL.md içinde 'tasarım çıktısı vermeden önce kontrol listesi' olarak yazılır. Tasarım sistemi için DESIGN.md şablonu (renk, tipografi, boşluk, bileşen kuralları) hazırlanır ve skill her üretimde onu okutur. Tam çalışma alanı (daemon, canlı önizleme, HyperFrames) yeniden yazmaya değmez; doğrudan kurulum daha mantıklı.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### Brief'ten tasarım sistemine uyan prototip üretimi, canlı önizleme ve ajanla yineleme
kaynak: https://github.com/nexu-io/open-design
### Slayt oluşturma, konuşmacı notları ve dışa aktarma
kaynak: https://github.com/nexu-io/open-design
### HyperFrames: ajanla hareketli grafik üretip MP4 dışa aktarma
kaynak: https://github.com/nexu-io/open-design
### Görsel üretimi ve medya sağlayıcı desteği
kaynak: https://github.com/nexu-io/open-design
### Tasarım sistemleri sayfası (örn. Stripe marka kimliği) ve ajanla rafine etme
kaynak: https://github.com/nexu-io/open-design
### `od mcp install <ajan>` ile 19 ajan/platforma MCP entegrasyonu; DeepSeek Harness için yerel runtime
kaynak: https://github.com/nexu-io/open-design
### craft/ tasarım kalite kılavuzları (anti-ai-slop, erişilebilirlik, tipografi, renk, durum kapsamı, RTL)
kaynak: https://github.com/nexu-io/open-design/tree/main/craft
### clipper tarayıcı uzantısı ile marka yakalama
kaynak: https://github.com/nexu-io/open-design/tree/main/clipper
## Destek
- L2JKgj7WzU4 · 11:35 · Claude Design'a açık kaynak alternatif: 31 tasarım skill'i, 72 marka sınıfı tasarım sistemi, 13 kodlama ajanı CLI'ı otomatik algılama. · kanıt: 13 coding agents CLIs auto detecting, 31 design skills, 72 brand grade design systems
