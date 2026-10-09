# Sonnet does the work. Opus checks the work. You pay mostly Sonnet prices.
## Künye
Sonnet does the work. Opus checks the work. You pay mostly Sonnet prices. · claudetipsandtricks · süre: 0:00 · ? · https://www.instagram.com/p/DYlzNOlDBbZ/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-37 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (7)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 52347 tk · claude-haiku-5-5: claude-haiku-5-5 · 33896 tk
## Özet
Instagram karusel gönderisi (7 slayt): Claude Platform'da beta olan Advisor Tool, Sonnet 4.6'yı yürütücü, Opus 4.6'yı danışman olarak tek API çağrısında eşleştirir. SWE-bench Multilingual'da Sonnet tek başına %70,3, Sonnet+Advisor %77,1, Opus tek başına %78,2. Kurulum: beta header ve tools dizisine advisor aracı eklemek, model olarak claude-sonnet-4-6 seçmek. Ne zaman kullanılıp ne zaman atlanacağı da anlatılıyor.
## Bölümler
- 0:00 Kapak: Opus seviyesi sonuç, Sonnet fiyatı
- 0:00 İki model, tek çağrı: nasıl çalışır
- 0:00 Benchmark sonuçları
- 0:00 Ne zaman kullanılır, ne zaman atlanır
- 0:00 API çağrılarına Advisor ekleme
- 0:00 Özet slaytı
- 0:00 Kapanış: günlük Claude ipucu
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Advisor Tool | yok | teknik | yok | Sonnet yürütücü ile Opus danışmanı tek API çağrısında eşleştiren beta araç | 0:00 | Kapak ve slayt 2'de Advisor Tool tanımlanıyor (karede: Kapakta 'The Advisor Tool.' başlığı; slayt 2'de 'Two models. One call.' ve HOW IT WORKS listesi) |
| Sonnet 4.6 | yok | teknik | yok | Görevi yapan hızlı ve ucuz yürütücü model | 0:00 | EXECUTOR: Sonnet 4.6; model adı claude-sonnet-4-6 (karede: Slayt 2'de EXECUTOR kutusu 'Sonnet 4.6'; slayt 5'te 'claude-sonnet-4-6') |
| Opus 4.6 | yok | teknik | yok | İşi gözden geçirip yön veren danışman model | 0:00 | ADVISOR: Opus 4.6, talep üzerine çağrılır (karede: Slayt 2'de ADVISOR kutusu 'Opus 4.6'; slayt 6'da 'Opus 4.6. Reviews and guides.') |
| SWE-bench Multilingual | yok | teknik | yok | Kodlama başarımını ölçen benchmark | 0:00 | 70,3% / 77,1% / 78,2% skorları (karede: Slayt 3'te iki kart: 70.3% ve 77.1% 'SWE-bench Multilingual') |
| BrowseComp | yok | teknik | yok | Web araştırma benchmark'ı | 0:00 | Sonnet solo 28,2%, Sonnet + Advisor 31,6% (karede: Slayt 3'te 'BROWSECOMP (WEB RESEARCH)' kutusu) |
| Claude Code | yok | CLI | yok | Advisor ile çalıştığı belirtilen kodlama aracı | 0:00 | Works with Claude Code and Managed Agents too (karede: Slayt 5 altındaki kutuda 'Works with Claude Code and Managed Agents too.') |
| Managed Agents | yok | teknik | yok | Advisor ile çalıştığı belirtilen yönetilen ajan servisi | 0:00 | Claude Code ile birlikte anılıyor (karede: Slayt 5 altındaki kutuda 'Managed Agents') |
| Claude Platform | yok | teknik | yok | Advisor Tool'un beta olarak sunulduğu platform | 0:00 | Beta. Available now on the Claude Platform. (karede: Slayt 6'da STATUS satırı) |
| DM Sans | yok | teknik | yok | Slaytlarda kullanılan sans-serif yazı tipi (benzer görünüm; kesin değil) | 0:00 | Geometrik sans-serif başlık ve gövde yazısı · kanıt: kare (karede: Tüm slaytlarda geometrik sans-serif başlık ve metin) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| anthropic-beta: advisor-tool-2026-03-01 | Advisor Tool beta başlığını API isteğine ekler (karede: Slayt 5 kod kutusu 1: 'anthropic-beta: advisor-tool-2026-03-01') | 0:00 | kare |
| {"type": "advisor_20260301", "name": "advisor"} | Advisor aracını tools dizisine ekler (karede: Slayt 5 kod kutusu 2: '{"type": "advisor_20260301", "name": "advisor"}') | 0:00 | kare |
| model: claude-sonnet-4-6 | Yürütücü modeli seçer; Opus otomatik danışman olur (karede: Slayt 5 madde 3: 'Set model to claude-sonnet-4-6 as executor.') | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Sonnet tek başına SWE-bench Multilingual'da %70,3 alır | 0:00 | sayısal |
| Sonnet + Advisor %77,1, Opus tek başına %78,2; Opus kalitesinin %99'u | 0:00 | sayısal |
| BrowseComp'ta Sonnet 28,2%, Sonnet + Advisor 31,6% | 0:00 | sayısal |
| Sonnet fiyatı 3$/15$ per M token | 0:00 | sayısal |
| Çok adımlı ajan görevleri ve yüksek riskli işlerde Advisor kullan, basit tek turlu işlerde atla | 0:00 | öneri |
| Anthropic eval önerisi: Sonnet solo, Sonnet+Advisor, Opus solo karşılaştır; dolar başına kalite | 0:00 | öneri |
| Sonnet Opus'a ne zaman danışacağına otomatik karar verir | 0:00 | özellik |
| Her çağrıda Opus ödüyorsanız API faturası yarıya inebilir (kanıtsız iddia) | 0:00 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | Advisor Tool | Advisor Tool | Kapak başlığı |
| kare 0:00 | Sonnet 4.6 | Sonnet 4.6 | EXECUTOR kutusu |
| kare 0:00 | Opus 4.6 | Opus 4.6 | ADVISOR kutusu |
| kare 0:00 | SWE-bench Multilingual | SWE-bench Multilingual | Slayt 3 kartları |
| kare 0:00 | BrowseComp | BrowseComp | Slayt 3 alt kutu |
| kare 0:00 | Claude Code | Claude Code | Slayt 5 alt kutu |
| kare 0:00 | Managed Agents | Managed Agents | Slayt 5 alt kutu |
| kare 0:00 | Claude Platform | Claude Platform | Slayt 6 STATUS |
| kare 0:00 | anthropic-beta başlığı | Advisor Tool | Slayt 5 kod kutusu |
| kare 0:00 | advisor_20260301 araç tipi | Advisor Tool | Slayt 5 kod kutusu |
| kare 0:00 | claude-sonnet-4-6 | Sonnet 4.6 | Slayt 5 madde 3 |
| kare 0:00 | Anthropic | aday değil: genel kavram | Slayt 4 'Anthropic's recommended eval approach'; slayt 5 anthropic-beta |
| kare 0:00 | @claudetipsandtricks | aday değil: konu dışı | Hesap adı, her slaytın alt köşesi |
| kare 0:00 | DM Sans (tahmini yazı tipi) | DM Sans | Slayt başlık ve gövde yazısı |
| açıklama | Claude platform/Claude AI etiketleri (#claude #claudeai #anthropic #api) | aday değil: genel kavram | Açıklama hashtag satırı |
## Kareden okunanlar
- 1 (0:00): NEW IN BETA; Opus-level results at Sonnet prices. The Advisor Tool.; @claudetipsandtricks
- 2 (0:00): Nasıl çalışır 4 adım; EXECUTOR Sonnet 4.6, ADVISOR Opus 4.6
- 3 (0:00): 70.3% vs 77.1% SWE-bench Multilingual; Opus solo 78.2%; BrowseComp 28.2% vs 31.6%
- 4 (0:00): Ne zaman kullan/atla; Anthropic'in eval yaklaşımı
- 5 (0:00): Beta header, advisor_20260301 aracı, claude-sonnet-4-6; Claude Code ve Managed Agents ile çalışır
- 6 (0:00): Advisor Tool özet tablosu: executor, advisor, quality, best for, setup, status
- 7 (0:00): Kapanış: One Claude tip, every day; Follow @claudetipsandtricks
## Belirsizlikler
- Video değil görsel gönderi; süre 0:00, tüm zamanlar 0:00 yaklaşık kare sırasıdır.
- Yorumlar girişsiz alınamadı.
- Yazı tipi DM Sans görünüm tahminidir, ekranda adı yazmıyor.
- Gönderideki benchmark ve fiyat iddiaları bağımsız doğrulanmadı.
- Açıklamada bağlantı yok.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Beta başlığını (anthropic-beta: advisor-tool-2026-03-01) API isteğine ekle — araçlar: Advisor Tool, Claude Platform
- 2. adım — Advisor aracını tools dizisine ekle — araçlar: Advisor Tool
- 3. adım — Modeli claude-sonnet-4-6 yürütücü olarak ayarla; Opus otomatik danışman olur — araçlar: Sonnet 4.6, Opus 4.6
- 4. adım — Sonnet görevi yürütür, gerektiğinde Opus'a danışır, rehberi uygular — araçlar: Sonnet 4.6, Opus 4.6
- 5. adım — Sonnet solo, Sonnet+Advisor ve Opus solo için eval çalıştırıp dolar başına kaliteyi karşılaştır — araçlar: SWE-bench Multilingual, BrowseComp
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
