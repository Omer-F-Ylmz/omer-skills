# CodeBurn
ad: CodeBurn
tur: CLI
video: klDiYMzW0o0
repo: getagentseal/codeburn
lisans: bilinmiyor (repoda LICENSE dosyası var, içeriği okunamadı)
son_commit: bilinmiyor (masaüstü sürümü 0.9.25 görüldü)
arsiv: bilinmiyor
kaynak: https://github.com/getagentseal/codeburn
telemetri: Arama özetine göre ağ isteği ve telemetri yok, her şey yerel oturum dosyaları üzerinde çalışıyor, hesap gerekmiyor. README'nin okunabilen kısmı bunu açıkça doğrulamadı, tam metin kesildi. Masaüstü uygulamasının otomatik güncelleme davranışı bilinmiyor.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
Yapay zeka kodlama araçlarının (Claude Code, Codex, Cursor, Gemini vb., README'ye göre 41 entegrasyon) token ve maliyet harcamasını proje, model, git dalı ve görev türüne göre döken yerel bir panel. Terminal arayüzü, web paneli ve masaüstü uygulaması var. Videodaki benzetmeyle yapay zeka harcamaları için banka ekstresi.
## Mekanizma
Araçların diske yazdığı oturum dosyalarını (JSONL vb.) okur, her tokenı fiyatlandırır ve tablolara dönüştürür. Görev türünü (kodlama, hata ayıklama, planlama) oturumun içeriğinden çıkarır. `codeburn optimize` oturumları ve yapılandırmayı tarar. Tekrar tekrar okunan dosyaları, kullanılmayan MCP sunucularını ve şişmiş CLAUDE.md dosyalarını bulur, not verir, düzeltme önerir ve tahmini tasarrufu yazar. `--apply` ile yedek alıp değişikliği uygular, `codeburn act undo --last` ile geri alır, `codeburn act report` ile vaadi gerçekle karşılaştırır. Ayrıca `plan set` ile abonelik planı takibi, dönem karşılaştırma ve PR verimliliği (Yield) var. Arama sonucuna göre Guard özelliği bir oturumu $5'ta uyarır, $15'te durdurur; bunu README'den doğrulayamadım.
## Kanıt
- Tokenların nereye harcandığını gösterir, yapay zeka harcamaları için banka ekstresi gibi → doğrulandı · README: oturum dosyalarını okuyup araç, model, proje ve görev bazında maliyet tabloları üretir.
- Telemetri ve ağ isteği yok, her şey yerel → sınanamadı · Yalnızca arama özeti söylüyor. README'nin okunan kısmı 'hesap yok, dosyalarınıza bakar' diyor, kod incelenmedi.
- optimize komutu tasarruf tahmini verir → doğrulandı · README optimize bölümü: bulgu, not, düzeltme ve dönem başına tahmini tasarruf. Gerçek tasarruf ölçülmedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- npx codeburn
- npm install -g codeburn (Node.js 22.13+)
- brew install codeburn
- codeburn optimize
- codeburn web
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Aylık faturanın nereye gittiğini görünür kılar ve israfı bulur. Yapılandırma değişikliğinin gerçekten ucuzlatıp ucuzlatmadığı dönem karşılaştırmasıyla ölçülebilir. Birden fazla araç kullananlar için tek yerde toplanmış bir görünüm sağlar.
## Maliyet/risk
`--apply` yapılandırma dosyalarını değiştirir, yedek alınıp geri alınabildiği söyleniyor. Oturum dosyalarını okur, bunlarda gizli bilgi olabilir, yerel kalması telemetri iddiasına bağlı. Lisans doğrulanmadı. Proje hızlı değişiyor, fork'lar çok ve resmi repo AgentSeal'e ait. Masaüstü kurulum dosyaları indirilebilir ikili olduğundan imza kontrolü gerekir.
## Tasarruf
Doğrudan token azaltmaz, gözlem aracıdır. Tasarruf `optimize` ile gelir: gereksiz tekrar okumaları, kullanılmayan MCP'leri ve şişkin CLAUDE.md'yi bulur, düzeltmenin tahmini tasarrufunu token ve dolar olarak yazar. Tasarruf rakamları aracın kendi tahminidir, bağımsız doğrulanmadı.
## Üretilebilir
hedef_tur: skill
tarif: Kendi skill'imiz `codeburn` CLI'ını çağırsın. Örneğin `npx codeburn` ve `codeburn optimize` çıktısını özetlesin. Bağımsız bir sürüm için Claude Code oturum JSONL dosyalarını (~/.claude/projects) okuyan küçük bir Node veya Python betiği yazılabilir. Betik usage alanlarını toplayıp model fiyat tablosuyla çarpar, proje ve gün bazında tablo verir. Bunu bir SessionEnd hook'una da bağlayabiliriz. Optimize benzeri bulgular için CLAUDE.md boyutunu ve kullanılmayan MCP'leri kontrol eden ek kurallar eklenebilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### Proje, model, dal ve görev bazında maliyet dökümü (terminal, web ve masaüstü)
kaynak: https://github.com/getagentseal/codeburn
### optimize: israf bulma, yedekli uygulama ve geri alma (act undo/report)
kaynak: https://github.com/getagentseal/codeburn
### Dönem karşılaştırma ve plan/kota takibi
kaynak: https://github.com/getagentseal/codeburn
## Destek
- klDiYMzW0o0 · 0:19 · Tokenların nereye harcandığını gösterir; yapay zeka harcamaları için banka ekstresi gibi. · kanıt: Kare: CodeBurn logosu, altyazı 'Üçüncüsü CodeBurn.'
