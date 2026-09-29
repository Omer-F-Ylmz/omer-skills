# Headroom
ad: Headroom
tur: CLI
video: klDiYMzW0o0
repo: headroomlabs-ai/headroom
lisans: Apache-2.0
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/headroomlabs-ai/headroom
telemetri: README: sıkıştırma makinede çalışır, sıkıştırmak için hiçbir istem/dosya içeriği bir yere gönderilmez. Anonim kullanım telemetrisi olup olmadığı okunan kısımda doğrulanmadı: bilinmiyor. Not: Kompress-v2-base modeli HuggingFace'ten indirilir (ilk kurulumda ağ erişimi). Yönlendirilen istekler zaten LLM sağlayıcısına gider.
yildiz: ~73.9k (SkillsLLM arama sonucundan; GitHub'dan doğrudan doğrulanmadı)
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
Yapay zeka ajanının okuduğu her şeyi (araç çıktıları, loglar, RAG parçaları, dosyalar, konuşma geçmişi) LLM'e ulaşmadan önce yerelde sıkıştıran bağlam sıkıştırma katmanı. Kütüphane (Python/TS), proxy, ajan sarmalayıcı (`headroom wrap claude` vb.) ve MCP sunucusu olarak kullanılır.
## Mekanizma
Ajan ile sağlayıcı (Anthropic/OpenAI/Bedrock…) arasına yerel proxy olarak girer (ANTHROPIC_BASE_URL yönlendirmesi). ContentRouter içerik türünü saptar ve sıkıştırıcı seçer: SmartCrusher (JSON), CodeCompressor (AST tabanlı kod), Kompress-v2-base (HuggingFace metin modeli). CacheAligner, sağlayıcı KV-cache önekini bozacak değişken içeriği işaretler ama istemi yeniden yazmaz. CCR (geri alınabilir sıkıştırma): orijinaller yerelde saklanır, model gerekirse `headroom_retrieve` aracıyla tam metni çeker. Ek olarak çapraz ajan hafızası, `headroom learn` (başarısız oturumlardan CLAUDE.local.md'ye düzeltme yazar) ve çıktı token azaltma var. Ağaçta Rust proxy'ye geçiş (REALIGNMENT belgeleri) görülüyor.
## Kanıt
- Kullanıcı ile model arasına girip gereksiz içeriği Claude'a ulaşmadan sıkıştırır (video 0:06). → doğrulandı · README: 'compresses everything your AI agent reads … before it reaches the LLM'; proxy modu ve `headroom wrap claude` mevcut.
- %20 (kod ajanları) ile %60-95 (JSON) token tasarrufu. → sınanamadı · Yalnız README/arama özetindeki üretici iddiası; kendi çalıştırmamla ölçülmedi.
- Sıkıştırma yerelde çalışır, içerik dışarı gönderilmez. → sınanamadı · README beyanı; kod/ağ trafiği incelenmedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- uv tool install --python 3.13 "headroom-ai[all]" (veya pip install "headroom-ai[all]")
- headroom wrap claude (Claude Code'u sarar; geri almak için headroom unwrap claude)
- alternatif: headroom proxy --port 8787 ve ANTHROPIC_BASE_URL'i proxy'ye yönlendir; ya da headroom init claude
- headroom doctor ile sağlık kontrolü; headroom perf / headroom dashboard ile tasarruf izleme
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude Code'da uzun araç çıktılarının ve loglarının bağlamı şişirmesini azaltır; maliyet ve bağlam dolma sorununu hafifletir. Tek komutla sarma/geri alma kolaylığı, birçok ajanı destekleme ve yerel çalışma güçlü yanları.
## Maliyet/risk
Tüm trafik yerel proxy'den geçer (API anahtarı/istem içeriği proxy'de görünür); kayıplı sıkıştırma modelin önemli ayrıntıyı kaçırmasına yol açabilir (CCR ile hafifletilir). Issue #1158: `headroom wrap claude` özel ANTHROPIC_BASE_URL nedeniyle 1M bağlam penceresini düşürüyor. Ağır bağımlılık (`[all]`, ML modeli), çok büyük/hızlı gelişen kod tabanı, Python→Rust geçişi kararsızlık getirebilir. Prompt cache ile etkileşim riski. Wrap Claude ayarlarını değiştirir.
## Tasarruf
Sıkıştırma + geri alınabilir önbellek: koda yönelik ajanlarda ~%20, JSON'da %60-95 daha az token iddiası (README). Örnek: 10.144 → 1.260 token log dökümü, FATAL satırı korunarak. Orijinal CCR ile gerektiğinde geri alınabilir; ayrıca model çıktısını da kısaltma özelliği var.
## Üretilebilir
hedef_tur: hook
tarif: Tam proxy yerine hafif bir Claude Code PostToolUse hook'u: Bash/Read çıktısı eşiği (örn. >8k token) aşarsa (1) JSON'u alan/dizi örnekleyerek özetle, (2) log'ları tekrarlayan satırları grupla ama ERROR/FATAL/stack trace satırlarını aynen koru, (3) tam çıktıyı yerel bir dosyaya (.cache/ccr/<hash>.txt) yaz ve özetin sonuna 'tam çıktı: <yol>' referansı ekle; modele bu dosyayı Read ile geri çağırma imkanı ver. İstenirse ek olarak `retrieve`/`stats` için küçük bir MCP sunucusu. Kompress benzeri ML modeli gerektirmez; kural tabanlı başla, ölçüm için önce/sonra token sayısını logla.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### Yerel proxy (headroom proxy --port 8787), sıfır kod değişikliği
kaynak: https://github.com/headroomlabs-ai/headroom
### headroom wrap/unwrap ile ajanları (claude, codex, cursor, aider…) tek komutla sarma
kaynak: https://github.com/headroomlabs-ai/headroom
### ContentRouter + SmartCrusher/CodeCompressor/Kompress-v2-base içerik türüne göre sıkıştırma
kaynak: https://github.com/headroomlabs-ai/headroom
### CCR: orijinali yerelde saklayıp headroom_retrieve ile geri alma
kaynak: https://github.com/headroomlabs-ai/headroom
### MCP sunucusu: headroom_compress, headroom_retrieve, headroom_stats
kaynak: https://github.com/headroomlabs-ai/headroom
### headroom learn: başarısız oturumlardan CLAUDE.local.md düzeltmeleri üretir
kaynak: https://github.com/headroomlabs-ai/headroom
### CacheAligner: prompt-cache önekini bozan değişken içeriği işaretler
kaynak: https://github.com/headroomlabs-ai/headroom
## Destek
- klDiYMzW0o0 · 0:06 · Kullanıcı ile model arasında durup gereksiz içeriği Claude'a ulaşmadan sıkıştırır. · kanıt: Seninle yapay zeka modeli arasına giriyor ve gereksiz içeriği sıkıştırıyor.
- g89FJiNAlEs · 5:47 · İstekler ile model arasına giren proxy. Konuşma geçmişindeki tekrarları sıkıştırır. /compact gibi özetlemez, tekrarlı bilgiyi çıkarır. 'headroom wrap claude' ile ajan sarılır, 'headroom dashboard' ile tasarruf izlenir. · kanıt: Anlatıcı wrap ile Claude oturumunu sarıyor ve dashboard'da önce/sonra token kullanımını gösteriyor.
