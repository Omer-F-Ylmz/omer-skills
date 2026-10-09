# Claude can now read your scripts out loud in a voice you picked yourself. The Fi
## Künye
Claude can now read your scripts out loud in a voice you picked yourself. The Fi · claudetipsandtricks · süre: 0:00 · ? · https://www.instagram.com/p/DbaXC_zDEe1/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-22 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 26277 tk · claude-haiku-5-5: claude-haiku-5-5 · 35818 tk
## Özet
Instagram kaydırmalı gönderi (8 görsel): Fish Audio'nun barındırdığı MCP sunucusunu Claude Code'a tek satırla bağlamayı, Claude.ai'de özel bağlayıcı olarak eklemeyi, ses seçip metni seslendirmeyi, köşeli parantezli ses etiketlerini, kayıt transkripsiyonunu ve kredi kullanımını anlatır. Altyazı yok; kanıt kare ve açıklamadan.
## Bölümler
- 0:00 Giriş: Claude istediği sesle konuşur
- 0:00 1. Tek satırda bağla (Claude Code)
- 0:00 2. Terminalsiz bağlama (Claude.ai)
- 0:00 3. İstediğin sesi iste
- 0:00 4. Etiketlerle seslendirmeyi yönet
- 0:00 5. Dinler de: transkripsiyon
- 0:00 6. Krediler planından düşer
- 0:00 Kapanış: takip çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Fish Audio MCP | yok | MCP | yok | Fish Audio'nun barındırdığı MCP sunucusu; ses arama, konuşma üretme ve transkripsiyon sağlar | 0:00 | Fish Audio ships an MCP server. Connecting it takes one line. (karede: kanıttan) Fish Audio ships an MCP server. Connecting it takes one line. |
| Fish Audio | yok | CLI | yok | Metinden konuşma ve transkripsiyon servisi; ses kütüphanesi ve web uygulaması var | 0:00 | Credits: same package credits as the Fish Audio web app (karede: kanıttan) Credits: same package credits as the Fish Audio web app |
| Claude Code | yok | CLI | yok | MCP sunucusunun claude mcp add ile eklendiği ana araç | 0:00 | Run this in Claude Code, then sign in through the browser (karede: kanıttan) Run this in Claude Code, then sign in through the browser |
| Claude.ai | yok | iş akışı | yok | Settings > Connectors > Add custom connector ile terminalsiz bağlama | 0:00 | On Claude.ai open Settings, then Connectors, then Add custom connector (karede: kanıttan) On Claude.ai open Settings, then Connectors, then Add custom connector |
| Claude | yok | prompt | yok | Sohbette araçları kendi seçen ana yapay zekâ | 0:00 | Claude picks the tools itself (karede: kanıttan) Claude picks the tools itself |
| Ses etiketleri | yok | teknik | yok | Köşeli parantezli etiketlerle ([whispering], [excited]) seslendirme tonunu yönetme | 0:00 | [whispering] keep this between us / [excited] the build finally passed · kanıt: kare (karede: [whispering] keep this between us / [excited] the build finally passed) |
| Ses transkripsiyonu | yok | teknik | yok | Kaydı yükleyip metne çevirme; yüklemeler 7 gün sonra silinir | 0:00 | Transcribe meeting.mp3 and pull out every decision we made. · kanıt: kare (karede: Transcribe meeting.mp3 and pull out every decision we made.) |
| Ses kütüphanesinde arama ve metni seslendirme | yok | prompt | yok | Sakin bir İngilizce anlatım sesi bul, intro.md dosyasını sesli oku ve ses bağlantısını ver. | 0:00 | kaynak: kare |
| Toplantı kaydı transkripsiyonu ve karar çıkarma | yok | prompt | yok | meeting.mp3 dosyasını yazıya dök ve alınan tüm kararları çıkar. | 0:00 | kaynak: kare |
| Kredi bakiyesi sorgulama | yok | prompt | yok | Kaç Fish Audio kredim kaldığını sor. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude mcp add --transport http fish-audio https://api.fish.audio/mcp | Fish Audio MCP sunucusunu Claude Code'a HTTP taşımasıyla ekler; tarayıcıdan oturum açılır (karede: 2. karede 'claude mcp add --transport http fish-audio https://api.fish.audio/mcp') | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Sunucu Fish Audio tarafından barındırılır; API anahtarı yapıştırmak gerekmez. | 0:00 | özellik |
| MCP kullanımı web uygulamasıyla aynı paket kredilerinden düşer; Developer API kredilerine dokunmaz, başarısız üretimler iade edilir. | 0:00 | özellik |
| Yüklenen dosyalar 7 gün sonra temizlenir. | 0:00 | sayısal |
| Claude ses kütüphanesinde arar, konuşma üretir ve kalıcı ses bağlantısı verir. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | Fish Audio MCP sunucusu | Fish Audio MCP | Fish Audio ships an MCP server |
| kare 0:00 | Fish Audio | Fish Audio | Fish Audio web app, credits |
| kare 0:00 | Claude Code | Claude Code | Run this in Claude Code |
| kare 0:00 | Claude.ai bağlayıcılar | Claude.ai | Settings, then Connectors, then Add custom connector |
| açıklama | Claude | Claude | Claude can now read your scripts out loud |
| açıklama | Anthropic | aday değil: genel kavram | #Anthropic hashtag |
| açıklama | MCP / Model Context Protocol | Fish Audio MCP | Fish Audio MCP server is hosted |
| kare 0:00 | Ses etiketleri | Ses etiketleri | [whispering] [excited] |
| kare 0:00 | Transkripsiyon | Ses transkripsiyonu | Transcribe meeting.mp3 |
| kare 0:00 | intro.md / meeting.mp3 | aday değil: genel kavram | örnek dosya adları |
| kare 0:00 | @claudetipsandtricks | aday değil: konu dışı | hesap takip çağrısı |
| açıklama | TextToSpeech, AIVoice, AITools hashtagleri | aday değil: genel kavram | hashtag listesi |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamıyor |
## Kareden okunanlar
- 1 (0:00): CLAUDE SPEAKS in any voice; Fish Audio ships an MCP server, one line
- 2 (0:00): claude mcp add --transport http fish-audio https://api.fish.audio/mcp
- 3 (0:00): Add custom connector, https://api.fish.audio/mcp
- 4 (0:00): ASK: Find a calm English narration voice and read intro.md aloud
- 5 (0:00): TAGS: [whispering] ve [excited] örnekleri
- 6 (0:00): ASK: Transcribe meeting.mp3; yüklemeler 7 gün sonra silinir
- 7 (0:00): ASK: How many Fish Audio credits do I have left?
- 8 (0:00): One Claude tip, every day. Follow @claudetipsandtricks
## Belirsizlikler
- Gönderi görsel olduğundan süre 0:00; tüm zamanlar 0:00 olarak verildi.
- Yorumlar girişsiz alınamadı.
- Açıklamadaki 5. slayt etiket sözdizimi, karelerde 5. sayfa olarak görünüyor (sayfa 5/8).
- Karedeki başka etiket adları (ör. diğer duygu etiketleri) gösterilmedi.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/DbaXC_zDEe1/ | açıklama | açıklama | hayır |
| https://api.fish.audio/mcp | 0:00 | ekran | evet |
## İş akışı
- yok
## Promptlar
- Ses kütüphanesinde arama ve metni seslendirme — Sakin bir İngilizce anlatım sesi bul, intro.md dosyasını sesli oku ve ses bağlantısını ver.
- Toplantı kaydı transkripsiyonu ve karar çıkarma — meeting.mp3 dosyasını yazıya dök ve alınan tüm kararları çıkar.
- Kredi bakiyesi sorgulama — Kaç Fish Audio kredim kaldığını sor.
