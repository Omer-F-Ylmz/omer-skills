# Claude can build your n8n automations for you. The unofficial n8n-mcp server han
## Künye
Claude can build your n8n automations for you. The unofficial n8n-mcp server han · claudetipsandtricks · süre: 0:00 · ? · https://www.instagram.com/p/DZ29oQwDBlV/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-26 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (5)
kareler: girdi ≤40000 jeton için 8→5
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 33985 tk · claude-haiku-5-5: claude-haiku-5-5 · 46596 tk
## Özet
Instagram karusel gönderisi (8 sayfa; 5 kare gönderildi): resmi olmayan n8n-mcp sunucusu Claude'a n8n düğümlerinin şemalarını verir. Kullanıcı otomasyonu düz İngilizce tarif eder, Claude akışı kurar ve doğrular. Kurulum için npx n8n-mcp ve claude mcp add anılır; üretim akışını önce kopyalayıp farkı kontrol etme uyarısı verilir.
## Bölümler
- 0:00 Kapak: Claude n8n akışlarını kurar
- 0:00 1. n8n'e köprü (npx n8n-mcp)
- 0:00 2. Canvas'ı atla (claude mcp add)
- 0:00 3. 1.845 düğüm (search_nodes)
- 0:00 4. Tek cümle (Stripe, Notion, Slack örneği)
- 0:00 5-8. Kurulum, önce kopyala uyarısı, takip çağrısı (yalnız OCR'da)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| n8n-mcp | yok | MCP | yok | Claude'u n8n düğüm belgeleri ve şemalarına bağlayan resmi olmayan MCP sunucusu | 0:00 | n8n-mcp connects Claude to n8n, the workflow tool that wires 500+ apps together. (karede: 2. karede başlık 'The bridge to n8n', kartta 'npx n8n-mcp' ve açıklama metni) |
| n8n | yok | iş akışı | yok | 500+ uygulamayı birbirine bağlayan iş akışı otomasyon aracı | 0:00 | n8n, the workflow tool that wires 500+ apps together (karede: Kapakta 'n8n flows', 2. karede turuncu vurgulu 'n8n') |
| Claude | yok | CLI | yok | Akışı tarif edilen cümleden tasarlayan ana yapay zekâ asistanı | 0:00 | Claude designs the whole workflow from your goal, then validates every node (karede: Kapakta 'CLAUDE' etiketi ve Claude logosu; 5. karede metin) |
| Claude Desktop | yok | CLI | yok | n8n-mcp'nin bağlandığı masaüstü istemci | 0:00 | Wires n8n into Claude Desktop. (karede: 3. karede 'claude mcp add' altında 'Wires n8n into Claude Desktop.') |
| claude mcp add | yok | CLI | yok | MCP sunucusunu Claude'a ekleyen komut | 0:00 | claude mcp add — Wires n8n into Claude Desktop. (karede: 3. karede komut kartı 'claude mcp add') |
| npx | yok | CLI | yok | n8n-mcp paketini çalıştıran Node paket çalıştırıcısı | 0:00 | npx n8n-mcp — Installs and starts the local server. (karede: 2. karede komut kartı 'npx n8n-mcp') |
| search_nodes | yok | MCP | yok | Doğru n8n düğümünü bulan MCP aracı | 0:00 | search_nodes ("stripe") Claude finds the right node for you. (karede: 4. karede kart: search_nodes ("stripe")) |
| Stripe | yok | iş akışı | yok | Örnek akışın tetikleyicisi olan ödeme servisi | 0:00 | When a Stripe payment succeeds, add the customer to Notion (karede: 5. karede örnek istem, 'Stripe' turuncu vurgulu) |
| Notion | yok | iş akışı | yok | Örnek akışta müşterinin eklendiği servis | 0:00 | add the customer to Notion and ping Slack. (karede: 5. karede örnek istemde 'Notion') |
| Slack | yok | iş akışı | yok | Örnek akışta bildirim gönderilen servis | 0:00 | add the customer to Notion and ping Slack. (karede: 5. karede örnek istemde 'Slack') |
| Claude Code | yok | CLI | yok | Araç setinin çalıştığı istemcilerden biri | açıklama | #claudecode; OCR 6. görsel: live in Desktop, Code, Cursor, and Windsurf. |
| Cursor | yok | CLI | yok | n8n-mcp'nin çalıştığı istemcilerden biri | açıklama | OCR 6. görsel: the toolkit is live in Desktop, Code, Cursor, and Windsurf. |
| Windsurf | yok | CLI | yok | n8n-mcp'nin çalıştığı istemcilerden biri | açıklama | OCR 6. görsel: the toolkit is live in Desktop, Code, Cursor, and Windsurf. |
| Duplicate first | yok | ipucu | yok | Üretim akışını yapay zekâ dokunmadan önce kopyalayıp farkı kontrol etme | açıklama | duplicate any production workflow before you let AI touch it, then check the diff. |
| n8n akışını tek cümleyle Claude'a kurdurma | yok | prompt | yok | Bir Stripe ödemesi başarılı olduğunda müşteriyi Notion'a ekle ve Slack'e bildirim gönder. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx n8n-mcp | Yerel n8n-mcp sunucusunu kurar ve başlatır (karede: 2. karede 'npx n8n-mcp · Installs and starts the local server.') | 0:00 | kare |
| claude mcp add | n8n'i Claude'a MCP olarak bağlar (tam argümanlar gösterilmedi) (karede: 3. karede 'claude mcp add · Wires n8n into Claude Desktop.') | 0:00 | kare |
| search_nodes("stripe") | Stripe için doğru n8n düğümünü arar (MCP aracı çağrısı) (karede: 4. karede 'search_nodes ("stripe")') | 0:00 | kare |
| npx n8n-mcp (görsel 6, yalnız OCR) | En güncel node kütüphanesini çeker. (karede: Görsel 6 gönderilmedi; yalnız OCR: 'npx n8n-mcp' - 'Pulls the latest node library.') | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude 1.845 düğümün şemasını okur: 816 çekirdek ve 1.029 topluluk düğümü. | 0:00 | sayısal |
| 2.300+ hazır şablon başlangıç noktası olarak sunulur. | 0:00 | sayısal |
| Claude akışı çalıştırmadan önce her düğümü doğrular. | 0:00 | özellik |
| Kurulum yaklaşık 2 dakika sürer; MCP yapılandırmasına bir satır eklenir (OCR 6. görsel). | açıklama | sayısal |
| Üretim akışı yapay zekâya verilmeden önce kopyalanmalı, sonuç diff ile kontrol edilmeli. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 · 0:00 | Claude | Claude | CLAUDE BUILDS your n8n flows |
| kare 1-2 · 0:00 | n8n | n8n | n8n flows |
| kare 2 · 0:00 | n8n-mcp | n8n-mcp | n8n-mcp connects Claude to n8n |
| kare 2 · 0:00 | npx | npx | npx n8n-mcp |
| kare 3 · 0:00 | claude mcp add | claude mcp add | claude mcp add |
| kare 3 · 0:00 | Claude Desktop | Claude Desktop | Wires n8n into Claude Desktop. |
| kare 4 · 0:00 | search_nodes | search_nodes | search_nodes ("stripe") |
| kare 5 · 0:00 | Stripe | Stripe | When a Stripe payment succeeds |
| kare 5 · 0:00 | Notion | Notion | add the customer to Notion |
| kare 5 · 0:00 | Slack | Slack | ping Slack |
| OCR 6 · açıklama | Cursor | Cursor | live in Desktop, Code, Cursor, and Windsurf |
| OCR 6 · açıklama | Windsurf | Windsurf | live in Desktop, Code, Cursor, and Windsurf |
| açıklama | Claude Code | Claude Code | #claudecode |
| OCR 7 · açıklama | Önce kopyala uyarısı | Duplicate first | Duplicate any production workflow before letting Claude touch it |
| açıklama | MCP | aday değil: başka adayın parçası (n8n-mcp) | #MCP |
| açıklama | Anthropic | aday değil: konu dışı | #Anthropic |
| açıklama | @claudetipsandtricks | aday değil: konu dışı | Follow @claudetipsandtricks |
| açıklama | Canva | aday değil: konu dışı | Sözlük eşleşmesi; gönderide kanıt yok |
| açıklama | Instagram gönderi bağlantısı | aday değil: konu dışı | https://www.instagram.com/p/DZ29oQwDBlV/ |
## Kareden okunanlar
- 1: Kapak: 'CLAUDE BUILDS your n8n flows', Claude logosu, @claudetipsandtricks, 8 noktalı sayfa göstergesi
- 2: 1. The bridge to n8n; n8n-mcp, 500+ uygulama; 'npx n8n-mcp'; Page 2/8
- 3: 2. Skip the canvas; 'claude mcp add' — Wires n8n into Claude Desktop; Page 3/8
- 4: 3. 1,845 nodes; 816 core + 1,029 community, 2,300+ şablon; search_nodes("stripe"); Page 4/8
- 5: 4. One sentence; validates every node; Stripe/Notion/Slack istemi; Page 5/8
## Belirsizlikler
- Yalnızca 5 kare gönderildi; 6-8. sayfalar yalnızca OCR metninden okundu.
- Altyazı/ses yok; zamanlar 0:00 (görsel gönderi).
- claude mcp add komutunun tam argümanları gösterilmedi.
- Yorumlar girişsiz alınamadı.
- Sayılar (1.845 düğüm, 2.300+ şablon) doğrulanmadı, gönderi iddiası.
- Gönderi n8n-mcp'nin resmi olmadığını açıklamada belirtiyor.
- Sözlükte Canva eşleşmesi var ama gönderide kullanıldığına dair kanıt yok.
- Tasarım yazı tipleri belirlenemedi.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/DZ29oQwDBlV/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — n8n-mcp sunucusunu npx ile kurup başlatma — araçlar: npx, n8n-mcp
- 2. adım — Sunucuyu Claude'a MCP olarak ekleme — araçlar: claude mcp add, Claude Desktop
- 3. adım — Claude'un düğüm şemalarını ve şablonlarını araştırması — araçlar: search_nodes, n8n-mcp
- 4. adım — Otomasyonu tek cümleyle tarif etme — araçlar: Claude, Stripe, Notion, Slack
- 5. adım — Claude'un akışı tasarlaması ve düğümleri doğrulaması — araçlar: Claude, n8n-mcp
- 6. adım — Üretim akışını kopyalama — araçlar: n8n
- 7. adım — Claude'a kopyayı düzenletip farkı kontrol etme — araçlar: Claude, n8n
## Promptlar
- n8n akışını tek cümleyle Claude'a kurdurma — Bir Stripe ödemesi başarılı olduğunda müşteriyi Notion'a ekle ve Slack'e bildirim gönder.
ikinci göz KAPALI: --ikinci-goz yok
