# You're Paying Anthropic 20x MORE Than You Need To
## Künye
You're Paying Anthropic 20x MORE Than You Need To · Chase AI · süre: 18:59 · en-orig · https://youtu.be/V0XbuApxlhg
motor: parti 2026-09-30-uzun · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
## Özet
Chase AI, Claude Code token maliyetini düşürmek için beş ipucu anlatıyor. En önemlisi prompt caching: her mesajda tüm konuşma geçmişi yeniden gönderilir; cache okuması (1 $/M) cache yazmasından (20 $/M) 20 kat ucuzdur. Cache 1 saat hareketsizlikte, model/efor/MCP/plugin değişiminde, compact'ta veya sürüm yükseltmede sıfırlanır. Cache kaybında /clear, /compact veya handoff skill'i seçenekleridir. Sonra model yönlendirme (advisor modu, Codex eklentisi, GPT Luna/Terra, yerel modeller), /doctor ile config temizliği ve son olarak ponytail/caveman gibi skill'ler anlatılır.
## Bölümler
- 0:00 Giriş
- 0:28 Prompt Caching
- 9:36 Soğuk Cache (Cold Cache)
- 12:50 Model Yönlendirme
- 14:54 Config Hijyeni
- 17:33 Skill'ler
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Prompt caching | yok | teknik | yok | Konuşma geçmişini cache'te tutarak input maliyetini yaklaşık 20 kat düşürme; cache 1 saat hareketsizlikte silinir. | 4:29 | Fiyat tablosunda 1h cache write $20/MTok, cache hit $1/MTok; konuşmada 20 kat fark anlatılıyor. (karede: Fiyat tablosu: Fable 5 1h cache write $20/MTok, cache hit $1/MTok, output $50/MTok.) |
| /clear | yok | ipucu | yok | Cache kaybolunca konuşma geçmişini silip sıfırdan başlama; proje dosyaları bağlamı taşır. | 9:36 | Nuclear option: forward/clear wipes the entire conversation history. |
| /compact | yok | ipucu | yok | Konuşmayı özetleyip yeni konuşmanın mesaj geçmişine koyar; otomatik compact'ı beklemeden çalıştırmak önerilir. | 10:37 | Forward/compact will start a new conversation with that summary. |
| Handoff skill | yok | skill | yok | Özeti diskte markdown dosyası olarak saklayan devir skill'i; yeni konuşma bu dosyayı okur. Sunucunun kendi skill'i ücretsiz toplulukta. | 11:39 | It's actually just going to put it on my disk... markdown file with the summary. |
| Advisor modu | yok | iş akışı | yok | Büyük model plan yapar, küçük model (Sonnet) uygular; her ikisinin ayrı cache'i vardır. | 12:50 | Smart model like Fable or Opus advising a smaller model like Sonnet. |
| Codex plugin for Claude Code | yok | plugin | yok | Claude Code arayüzünden Codex/GPT modellerine görev devretmeyi kolaylaştırır. | 13:51 | There is a Codex plugin for Claude code. |
| Fable advisor | yok | skill | yok | Fable'ın GPT modellerini danışman olarak çağırmasını sağlayan repo (adı yalnızca söylendi, URL yok). | 13:51 | There's other repos like this Fable advisor that do exactly that. |
| /doctor | yok | CLI | yok | CLAUDE.md'yi kısaltır, kullanılmayan skill ve MCP'leri budayıp bağlam şişkinliğini azaltır. | 14:54 | Run the forward/doctor command... trim your claude.md down. |
| /context | yok | CLI | yok | Boş konuşmada bile bağlamın neyle dolduğunu gösterir (skill, sistem promptu, memory); sunucuda 40.000 token. | 15:54 | We've already used 40,000 tokens... skills, system prompt, memory files. |
| Ponytail | yok | skill | yok | Claude'un yazdığı kod miktarını azaltıp maliyeti düşüren popüler skill; Fable ile benchmark sayıları tuttu. | 17:33 | It reduces the amount of code Claude writes while maintaining its effectiveness. |
| Caveman | yok | skill | yok | Output token'larını %65 azalttığı iddia edilen skill. | 17:33 | Claiming it reduces your output tokens by 65%. |
## Açıklama bağlantıları
- https://www.skool.com/chase-ai — Chase AI Skool topluluğu · aday: hayır · Topluluk sayfası; araç/repo değil, giriş gerektiriyor olabilir. · erişilemez: giriş gerekli / topluluk (Skool)
- https://www.skool.com/chase-ai-community — Chase AI ücretsiz topluluk (handoff skill burada) · aday: hayır · Handoff skill'inin burada olduğu söyleniyor ama içerik üyelik arkasında. · erişilemez: giriş gerekli / topluluk (Skool)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /clear | Tüm konuşma geçmişini siler, yeni konuşma başlatır. | 9:36 | altyazı |
| /compact | Konuşmayı özetleyip yeni konuşmanın mesaj geçmişine koyar. | 10:37 | altyazı |
| /doctor | CLAUDE.md'yi kısaltır, kullanılmayan skill/MCP'leri budar. | 14:54 | altyazı |
| /context | Bağlam penceresinin neyle dolduğunu gösterir. | 15:54 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Cache okuması cache yazmasından yaklaşık 20 kat ucuzdur (1 $/M vs 20 $/M). | 5:30 | sayısal |
| Output token'ları input token'ın kabaca 5 katı fiyatlıdır. | 1:00 | sayısal |
| 500K token'lık konuşmada cache varken sonraki mesaj ~0,50 $, cache yokken ~10 $. | 7:34 | sayısal |
| Model, efor, fast mode, MCP, plugin, tool reddi, compact veya Claude Code yükseltmesi cache'i sıfırlar. | 7:34 | özellik |
| 600-800K token aralığında context rot sorunu var; beklemeden manuel compact önerilir. | 10:37 | öneri |
| Advisor modu daha düşük maliyetle daha iyi sonuç verdi; GPT Luna ve Terra ucuz ve Anthropic'te eşdeğeri yok. | 13:51 | karşılaştırma |
| Şişkin CLAUDE.md hem yavaşlatır hem token maliyeti yaratır; yeni modeller az talimatla yetinir. | 15:54 | öneri |
| Caveman output token'larını %65 azalttığını iddia ediyor; ancak output tek parçadır, asıl belirleyici prompt caching. | 17:33 | sayısal |
## Kareden okunanlar
- 1:59 (excalidraw): User: How are you doing today? / Fable: I'm doing great, thanks. / User: Build me an app, no mistakes. / Fable: On it, what is this app about?
- 2:59: Kutuda 5 i ve 4 o, '5X' notu; 6 i yazısı.
- 5:00: PROMPT CACHING tablosu: Fable 5 base input $10, 5m write $12.50, 1h write $20, hit $1, output $50; Opus 5: $5, $6.25, $10, $0.50, $25; 'API' notu 5m sütununda.
- 7:04: $1/M, 50¢ + ; 500K + 10 kutusu.
- 6:02: Cache belgesi ikonu ve '500K + 1' yazısı; yeşil oklarla cache şeması.
## Belirsizlikler
- Kare listesi 8 görsel için 0:14 vb. zamanlar verdi ama görsel sırası tam eşleşmiyor; kare zamanları yaklaşık.
- Fable, Luna, Terra, Opus 5 gibi model adları ve fiyatlar videodaki haliyle aktarıldı, doğrulanmadı.
- Fable advisor ve handoff skill için repo URL'si verilmedi.
- Skool bağlantılarının içeriğine erişilemedi; hangisinin ücretsiz olduğu belirsiz.
- Video sponsor kısmı: Chase AI Plus masterclass, pinned comment'te link var; açıklamada yok.
- 'Ponytail' ve 'caveman' repo adresleri verilmedi; %65 iddiası doğrulanmadı.
## Atlanan segment oranı
0/22 (paket tam okuma, motor)
ikinci göz KAPALI: --ikinci-goz yok
