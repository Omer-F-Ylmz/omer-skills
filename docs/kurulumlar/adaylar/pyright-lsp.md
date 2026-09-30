# Pyright LSP
ad: Pyright LSP
tur: plugin
video: uuUo7gWuH9w
repo: anthropics/claude-plugins-official
lisans: bilinmiyor (eklenti için doğrulanamadı; altındaki Microsoft Pyright dil sunucusu MIT lisanslı olarak biliniyor, ama bu depodan doğrulamadım)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pyright-lsp
telemetri: Eklentinin kendisinde telemetri olduğuna dair bir bulgu yok, ama eklenti kodunu incelemedim. Pyright dil sunucusu yerelde çalışır ve kod göndermez. Kesin yanıt için eklenti dosyalarına bakılmalı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Claude Code için Python dil sunucusu (LSP) eklentisi. Microsoft Pyright'ı Claude Code'a bağlar. Tip çıkarımı, statik tip denetimi ve kod zekâsı sağlar. Claude'un yazdığı Python kodundaki tip hatalarını yakalamasına yardım eder.
## Mekanizma
Eklenti anthropics/claude-plugins-official pazar yerinde plugins/pyright-lsp altında duruyor. Claude Code'a hangi LSP sunucusunun Python dosyalarına bağlanacağını söyleyen bir yapılandırma içeriyor. Claude .py dosyası düzenleyince Pyright dil sunucusu tanılamaları (tip hataları, tanımsız adlar) geri verir. Tanıma gitme ve başvuru bulma gibi kod gezinme işlemleri de aynı sunucudan gelir. Claude hataları görüp düzeltir. Ayrıntıları eklentinin kendi dosyalarından okumadım. Bu anlatım videodaki tanıma ve LSP eklentilerinin genel yapısına dayanıyor. Pyright sunucusunun ayrıca kurulu olması gerekebilir (çoğu LSP eklentisi ikili dosyayı kendisi getirmez), bunu doğrulamadım.
## Kanıt
- Eklenti Python için tip çıkarımı, statik tip denetimi ve tamamlama sağlar. → sınanamadı · Sadece video bulgusuna dayanıyor. Eklenti dizini ağaçta var (plugins/pyright-lsp), ama içeriğini okuyamadım.
- Kurulum satırı /plugin install pyright-lsp@claude-plugins-official. → doğrulandı · Pazar yeri README'sindeki kurulum biçimi (/plugin install {plugin-name}@claude-plugins-official) ve plugins/pyright-lsp dizininin varlığı bununla uyuşuyor.
- Claude üretilen kodu bununla doğrular. → sınanamadı · Canlı denemedim. Bu davranışı eklenti kodundan ya da belgeden doğrulayamadım.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- /plugin install pyright-lsp@claude-plugins-official
- Alternatif: /plugin > Discover menüsünden bul
- Gerekirse Pyright'ı ayrıca kur: npm i -g pyright veya pip install pyright (eklentinin bunu gerektirip gerektirmediği doğrulanmadı)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Python projelerinde Claude'un ürettiği kodu statik tip denetimiyle doğrular. Çalıştırmadan önce tip hatalarını yakalar. Tek komutla kurulur. Anthropic'in resmi pazar yerinde yer alır.
## Maliyet/risk
Pazar yeri README'si, eklentilere güvenmeden kurmamayı ve eklentilerin içeriğini Anthropic'in denetlemediğini uyarıyor. Pyright'ın ayrıca kurulması gerekebilir. Büyük projelerde bellek ve CPU kullanabilir. Eklenti lisansı ve son commit bilgisi doğrulanamadı.
## Tasarruf
Token aracı değil. Dolaylı etkisi var: tip hataları çalıştırmadan önce yakalanınca test-hata-düzelt döngüsü kısalabilir. Bunu ölçmedim.
## Üretilebilir
hedef_tur: plugin
tarif: Kendi Python LSP eklentimizi yapmak mümkün. .claude-plugin/plugin.json yaz ve Pyright için LSP sunucu yapılandırmasını ekle (komut: pyright-langserver --stdio, dosya uzantısı .py). Alternatif olarak PostToolUse hook'u kur: Python dosyası düzenlenince `pyright --outputjson <dosya>` çalıştırıp hataları Claude'a geri versin. Bunu yapmadan önce resmi eklentinin yapılandırma biçimini okuyup referans al. Zaten resmi eklenti varsa yeniden üretmeye gerek yok.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### Resmi pazar yerinde bulunur, /plugin install ile tek komutta kurulur.
kaynak: https://github.com/anthropics/claude-plugins-official
### Pyright: yüksek performanslı, standartlara uygun Python statik tip denetleyicisi (komut satırı aracı ve dil sunucusu).
kaynak: https://github.com/microsoft/pyright
### Aynı pazar yerinde başka diller için LSP eklentileri var (clangd, gopls, rust-analyzer, typescript, jdtls, kotlin, php, ruby, swift, lua, csharp).
kaynak: https://github.com/anthropics/claude-plugins-official/tree/main/plugins
## Destek
- uuUo7gWuH9w · 3:21 · Python için tip çıkarımı, statik tip denetimi ve tamamlama sağlayan dil sunucusu plugini; Claude üretilen kodu bununla doğrular. · kanıt: Pyright LSP sayfası ve kurulum satırı karede görülüyor. (karede: Pyright LSP sayfası: 'Static type checking' vurgulu; Installation altında /plugin install pyright-lsp@claude-plugins-official)
