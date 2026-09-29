# Altın set — kHtOSJRUkLs (uzun yapılandırma/prompt, 19:47) · "Paste This Into Claude Code, Never Run Out Of Tokens Again" · Sharbel A.

Özet (kalem): Araç/servis/ürün 6 · Açıklama bağlantıları 0 · Kurulum/komutlar 7 · Teknikler 10 · Kural/ipucu/iş akışı 8 · Promptlar 1 · Kareden bilgi 8 · Emin olunmayanlar 6 = 46

## Kaynaklar
- .kos/altin/kHtOSJRUkLs/kaynak.txt (yt-dlp -J açıklama (audit prompt'u tam metin) + 14 bölüm, bağlantı 0; altyazı en-orig oto, 40 satır/30 sn; `tools/video/altin_mozaik.py`, seçim motorun `dil_sec`i)
- .kos/altin/kHtOSJRUkLs/mozaik-01..05.png (39 kare, ~30 sn aralık, 3×3)
- Tekil tam çözünürlük kare (2): kare-006 (02:31 Token Audit slaytı), kare-035 (17:10 /usage paneli). Bu karelerden okunan kalem `[tekil]` işaretli.
- Motor raporu/paneli/adayları, paket.md, docs/video-tarama ve frontend kütüphanesi AÇILMADI.

Kanıt biçimi: zaman · kaynak (altyazı|kare|açıklama) · "alıntı ≤15 kelime" · önem.

## Araç/servis/ürün (6)
1. Claude Code · ajan · oturum limiti sorununun öznesi · 00:00 altyazı "Claude just told me to come back in 5 hours" · yüksek
2. MCP tool deferral (araç kılavuzlarını gerektiğinde açma; varsayılan açık) · özellik · 08:00 altyazı "your agent does not read every manual anymore" · yüksek
3. Haiku · model · alt ajan ve angarya işleri · 12:00 altyazı "set the sub-agents model to Haiku" · yüksek
4. Claude Code Docs "Explore the context window" simülasyonu · doküman · 10:30 altyazı "we have a simulation of how context windows work" + 10:36 kare "Explore the context window" · orta
5. Anthropic multi-agent research yazısı · doküman · 11:30 altyazı "Their multi-agent research post says agents use around four times more tokens" · orta
6. Connectors dizini (Gmail, Slack, Google Calendar, AWS MCP…) · Claude Code arayüzü · 09:05 kare "Directory" / "Connectors" · düşük

## Açıklama bağlantıları (0)
- yok (açıklamada bağlantı yok; bölümler + audit prompt'u var)

## Kurulum/komutlar (7)
1. /clear — iş değişince · 03:00 altyazı "When you finish a job and start with a different one, use {slash}clear" · yüksek
2. /context — araç satırı "deferred" mı bak · 09:00 altyazı "run /context, and find the tools line" · yüksek
3. /usage — limiti neyin yediğini adıyla gösterir · 16:30 altyazı "It names the specific skill, the specific tool, the specific agent." · yüksek
4. Kullanılmayan MCP/bağlayıcıyı kapat (silmeden; ~30 sn) · 08:30–09:00 altyazı "turn off anything you have not used in the last like month" · yüksek
5. /rename, sonra gerekirse /resume · 04:00 altyazı "use {slash} rename inside your session first, so you can use {slash} resume later" · orta
6. /rewind — birkaç turu geri almak için compact yerine · 15:30 altyazı "use {slash} rewind instead" · orta
7. /cost — bu oturumun maliyeti · 17:00 altyazı "The cost or slash cost." · orta

## Teknikler (10)
1. Bağlam her mesajda baştan yeniden gönderilir; erken okunan dosya her turda yeniden ödenir · 01:00 altyazı "your entire conversation gets wrapped up and sent again from the top" · yüksek
2. Model ve eforu oturum başında seç, sonra dokunma · 06:00 altyazı "Pick your model and your effort at the start of the session" · yüksek
3. Gürültülü komut çıktısını ajan görmeden kesen küçük filtre dosyası (hook), ajana yazdır · 07:00 altyazı "one small file that sits between your agent and the command" · yüksek
4. Alt ajana yalnız üç koşulda devret: yüksek hacim, ayrıntı tekrar gerekmez, oturum uzun sürecek · 11:30 altyazı "The output is high volume, you will not need the detail again" · yüksek
5. Model seçimini skill/alt ajan başına yap (angarya Haiku'da) · 12:30 altyazı "The better way to do this is per skill and per sub-agent." · yüksek
6. Zamanlanmış görev aralığını önbellek ömründen (abonelikte 1 saat) kısa tut · 13:30 altyazı "If your task can run every 45 minutes instead of every hour" · yüksek
7. PDF'i önce düz metne çevirt (~dörtte bir maliyet) · 16:00 altyazı "Ask your agent to turn it into a plain text file first" · orta
8. Metni ekran görüntüsü yerine yapıştır (görüntü ~2.700 token) · 15:30 altyazı "Paste the text instead." · orta
9. Kendi maliyet yüzdeni oturum loglarından alt ajana hesaplat · 17:30 altyazı "ask your sub agent to go read them and work out your own percentage" · orta
10. Audit'i haftada bir ya da plugin/MCP/zamanlanmış görev eklenince yeniden koş · 19:00 altyazı "I would run it once a week" + açıklama · orta

## Kural/ipucu/iş akışı (8)
1. Önbelleği bozanlar: model, efor, fast mode, MCP bağla/kopar (önden yüklüyse), MCP'li plugin, compact, güncelleyip uzun oturumu resume · 05:30 altyazı "switching models, changing effort, turning on fast mode" + 06:03 kare "BREAKS YOUR CACHE" · yüksek
2. Proxy/gateway (ANTHROPIC_BASE_URL) tool deferral'ı sessizce kapatır · açıklama "routing through a proxy silently turns deferral off and nothing warns you" · yüksek
3. Compact tasarruf değil: en pahalı mesaj + önbelleği siler · 15:00 altyazı "Compaction buys you continuity, not savings." · yüksek
4. Alt ajan token kazandırmaz, taşır · 10:00 altyazı "Everybody says sub-agents save tokens, but they do not. They move them." · yüksek
5. Güvenli değişiklikler: repo/memory dosyası düzenleme, output style, izin modu, skill/komut, rewind, alt ajan başlatma · 06:00 altyazı "Things that are safe, editing files in your repo" · orta
6. Her bağlı araç kılavuz yükler (GitHub 26k, Slack 21k token) · 08:00 altyazı "GitHub on its own, for example, costs you 26,000 tokens." · orta
7. Kısa prompt yazmak işe yaramaz (yazılan metin faturanın %0,01'i) · 14:30 altyazı "Your prompt length is a rounding error." · orta
8. Arka planda açık oturum sorun değil; zamanlanmış görevler ve canlı ajan takımları sorun · 14:00 altyazı "Your scheduled tasks are your problem, and your live agent teams" · orta

## Promptlar (1)
1. Token Audit prompt'u: "fix yok, yalnız rapor" → 7 bölüm (MEMORY, TOOLS, MODEL, HOOKS, SUBAGENTS, SCHEDULED WORK, CACHE) → tek tablo FINDING | SEVERITY | EVIDENCE | COST, maliyete göre sıralı → tek satır en yüksek kaldıraç → kurallar (ölç, tahmin etme; UNKNOWN yaz; dosya/ayar değiştirme) · açıklama tam metin + 02:31 kare [tekil] "Audit this setup for token waste. Report only." · yüksek

## Kareden bilgi (8)
1. Audit eşiği: tek CLAUDE.md >5k, toplam >10k token işaretlenir · 02:31 kare [tekil] "Flag any file over 5k, any total over 10k." · yüksek
2. /usage paneli: oturum Cost $1.16, Cache hit %84; Input 11.1k, Output 908, Cache read 5.8M, Cache write 1.1M · 17:10 kare [tekil] "Cache hit 84%" · yüksek
3. /usage "What's using your limits?": %100 8+ saat açık oturumlardan, %94 150k üstü bağlamda · 17:10 kare [tekil] "100% came from sessions active for 8+ hours" · yüksek
4. /usage ipucu: arka plan/döngü oturumları sürekli kullanım biriktirir · 17:10 kare [tekil] "These are often background or loop sessions." · orta
5. /context paneli: "System tools (deferred)" satırı; 111.6k / 1.0M (%11) · 09:35 kare "System tools (deferred)" · orta
6. Önbellek slaytı: bozan 7 madde / güvenli 3 madde iki sütun · 06:03 kare "CHANGE IT AND YOU PAY FULL PRICE AGAIN" · orta
7. Anthropic dokümanı: çoklu ajan sistemleri ~15× token · 11:37 kare "multi-agent systems use about 15× more tokens" · orta
8. Kapanış özeti slaytı: Clear between jobs · Pick model and effort once · Filter tool output · Disconnect what you never use · 18:41 kare "THE WHOLE VIDEO, IN FIVE LINES" · orta

## Emin olunmayanlar (6)
1. MCP kapatma panelini açan komut altyazıda kesik ("Type in" sonrası boş); /mcp olduğu tahmin, doğrulanmadı.
2. Filtre hook'unu yazdıran ekrandaki prompt karelere düşmedi (07:04 yüz çekimi); "Anthropic ships a working version" örneğinin adı yok.
3. Maliyet rakamları (10 sent→1 dolar, 9.800/5.700 alt ajan hesabı, görüntü 2.700 token) videodan; doğrulanmadı. Altyazıda "Opus 5", ekranda "Opus 4.8" görünüyor.
4. "Önbellek abonelikte 1 saat" iddiası; plan/API farkı anlatılmıyor.
5. "Burn rate meter" ekran köşesinde deniyor, karelerde görülmedi.
6. "Arka plan <4 sent/oturum" Anthropic dokümanına atfediliyor; kaynak gösterilmedi.
