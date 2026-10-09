# Claude Mem
ad: Claude Mem
tur: plugin
video: k0gwr-vC2Z4
repo: thedotmack/claude-mem
lisans: Apache-2.0
son_commit: bilinmiyor (README sürüm rozeti 13.29.0)
arsiv: bilinmiyor
kaynak: https://github.com/thedotmack/claude-mem
telemetri: Bilinmiyor. Arama sonuçlarında "gözlem başına maliyet" izleme çalışması geçiyor. Bunun yerel mi uzak mı olduğu doğrulanmadı. Veriler yerel SQLite'ta tutuluyor. Ancak sıkıştırma için agent-sdk üzerinden model çağrısı yapıldığından gözlem içeriği Anthropic API'ye gider.
yildiz: 65.8K civarı (augmentcode yazısına göre; GitHub'dan doğrudan doğrulanmadı)
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Claude Code için kalıcı bellek sistemi. Oturumlarda Claude'un yaptıklarını otomatik yakalar, yapay zekâyla sıkıştırır ve ilgili bağlamı sonraki oturumlara geri enjekte eder. Böylece proje her seferinde yeniden anlatılmaz.
## Mekanizma
5 yaşam döngüsü hook'u (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) araç kullanımını yakalar. Arka planda çalışan bir worker servisi (HTTP API, port 37777, web görüntüleyici) ham veriyi Claude agent-sdk ile olgu, kavram ve dosya referansı içeren gözlemlere sıkıştırır. Gözlemler yerel SQLite'ta tutulur. Arama FTS5 anahtar kelime aramasını Chroma vektör aramasıyla birleştirir. Yeni oturumda ilgili bağlam enjekte edilir. MCP üzerinden 3 katmanlı arama sunar: önce kompakt indeks, sonra yalnız süzülen ID'lerin ayrıntısı. Mekanizma bilgisi web aramasından geldi, kaynak kodu okunmadı. Repo ağacında Cursor, Codex, Grok ve Windsurf için de plugin dizinleri var.
## Kanıt
- Claude'a oturumlar arası hafıza verir; projeyi her seferinde yeniden anlatmayı bitirir. → doğrulandı · Repo tanımı 'Persistent memory compression system built for Claude Code'. Web aramasındaki özet de oturumlar arası bağlam enjeksiyonunu doğruluyor. Kurulumu çalıştırıp denemedik, yani etkinlik ölçülmedi.
- Yaklaşık 10 kat token tasarrufu sağlar. → sınanamadı · Yalnızca üçüncü taraf özetlerde geçiyor. Kendi ölçümümüz yok.
- güvenlik ön taraması: koşmadı
## Kurulum
- Claude Code içinde plugin marketplace üzerinden kurulur (repoda .claude-plugin/marketplace.json var). Kesin komutlar README'nin kesilen kısmında olduğundan doğrulanamadı; README'deki Quick Start'a bakın.
- Node >= 20 gerekir (README rozeti). Repoda bun yapılandırması (bunfig.toml) ve npx dağıtım planı (.plan/npx-distribution.md) var.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Oturumlar arası süreklilik sağlar, bağlam yeniden anlatma yükünü azaltır, geçmiş kararlar aranabilir. Birden çok ajan (Claude Code, Cursor, Codex vb.) desteklenir.
## Maliyet/risk
Ek arka plan servisi (port 37777) ve hook'lar çalışır. Araç çıktıları, yani kod ve olası sırlar, sıkıştırma için model API'ye gönderilir ve kalıcı depolanır. Ek token/API maliyeti doğar. Yanlış veya eskimiş bellek enjekte edilebilir. Bellek içeriği prompt injection yüzeyi olabilir. Proje çok hızlı değişiyor (sürüm 13.x) ve repoda çok sayıda ajan/plan dosyası var. Güvenlik denetimi yapılmadı.
## Tasarruf
Tam geçmişi bağlama yüklemek yerine sıkıştırılmış gözlemler enjekte edilir. Arama 3 katmanlıdır: önce indeks, sonra filtrelenmiş ID'lerin ayrıntısı. Üçüncü taraf yazılar bunu naif getirmeye göre yaklaşık 10 kat tasarruf diye aktarıyor. Bağımsız ölçüm yapılmadı. Sıkıştırma için ek model çağrısı yapıldığından net tasarruf bu maliyetle azalır.
## Üretilebilir
hedef_tur: hook
tarif: Hafif bir sürüm yapılabilir. (1) PostToolUse ve Stop hook'ları araç olaylarını yerel bir SQLite (FTS5) dosyasına yazar. (2) SessionEnd hook'u oturum özetini claude -p veya küçük bir modelle çıkarıp kısa gözlemler olarak kaydeder. (3) SessionStart hook'u projeye ait son N gözlemi kompakt indeks halinde additionalContext olarak enjekte eder. (4) İsteğe bağlı küçük bir MCP veya skill, indeksten ID ile ayrıntı çekmeyi (3 katmanlı arama) sağlar. Vektör arama ve sürekli çalışan worker olmadan başlanabilir. Sırları süzmek için kayıt öncesi maskeleme eklenmeli.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### 5 yaşam döngüsü hook'u ile otomatik yakalama
kaynak: https://github.com/mbrukman/thedotmack-claude-mem
### SQLite FTS5 ve Chroma vektör ile hibrit arama
kaynak: https://deepwiki.com/thedotmack/claude-mem
### 3 katmanlı MCP arama iş akışı (indeks, sonra ayrıntı)
kaynak: https://www.augmentcode.com/learn/claude-mem-v13-persistent-agent-memory
### Port 37777'de web görüntüleyici ve worker servisi
kaynak: https://github.com/thedotmack/claude-mem
### Cursor, Codex, Grok ve Windsurf için plugin dizinleri
kaynak: https://github.com/thedotmack/claude-mem
## Destek
- k0gwr-vC2Z4 · 0:35 · Claude'a oturumlar arası hafıza verir; projeyi her seferinde yeniden anlatmayı bitirir. · kanıt: Altyazı: oturumlar arası hafıza, projeyi her seferinde yeniden açıklamak yok.

## Güncellik (2026-10-04)
- kurulu adce0fd ↔ upstream 94cb08b
- yeni skill/komut/ajan: skills/agent-cost-report, skills/handoff · son commit 2026-10-03
