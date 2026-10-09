# REA lets your AI agent take any app apart and explain how its features really wo
## Künye
REA lets your AI agent take any app apart and explain how its features really wo · gittrend.io · süre: 0:25 · ? · https://www.instagram.com/reel/DeGeaxYjeCq/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-8 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 35395 tk · claude-haiku-5-5: claude-haiku-5-5 · 74123 tk
## Özet
25 saniyelik reel, REA (Reverse Engineer Anything) adlı açık kaynak aracı tanıtıyor. Ajan, orijinal kaynak kodu olmadan bir uygulamayı inceleyip özelliğin nasıl çalıştığını kanıtlarıyla açıklıyor; istenirse o özelliğin kendi projeye uyarlanmış sürümü üretiliyor. Her şey yerel makinede çalışıyor, uygulama sunucuya yüklenmiyor. Ekranda GitHub README sayfası, npx kurulum komutları ve desteklenen ajanlar görünüyor.
## Bölümler
- 0:00 REA tanıtımı: ajanı uygulamaya yönlendir
- 0:09 Just ask your agent ve örnek prompt
- 0:13 Decompile, Understand, Recreate modeli
- 0:17 Yerel çalışma ve hızlı kurulum
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| REA | yok | CLI | https://github.com/morluto/rea | Ajanlara uygulamaları tersine mühendislikle inceletip özelliklerin nasıl çalıştığını kanıtla açıklatan araç; CLI ve MCP sunar. | 0:00 | REA: Reverse Engineer Anything (karede: GitHub README sayfası, başlık 'REA: Reverse Engineer Anything', npm v3.2.1 rozeti, 'POINT YOUR AGENT' altyazısı) |
| rea-agents | yok | CLI | yok | REA'nın npm paketi; npx ile setup çalıştırılır. | 0:09 | npx rea-agents setup (karede: 'Just ask your agent' bölümünde npx rea-agents setup kod bloğu) |
| MCP | yok | MCP | yok | REA ajan entegrasyonunda hizalı MCP kaydı kurar. | 0:09 | Agent integration installs an aligned MCP registration (karede: README metni 'aligned MCP registration and the bundled routing skill'; MCP rozeti) |
| Routing skill | yok | skill | yok | REA ile gelen, ajanı yönlendiren paketli skill. | 0:09 | bundled routing skill together (karede: README metni 'bundled routing skill together:') |
| Hopper | yok | CLI | yok | Derin yerel analiz sağlayıcısı; gerektiğinde kurulur. | 0:21 | and—when needed—the Hopper provider (karede: Quick start metni: 'the Hopper provider. Nothing is preselected.') |
| Ghidra | yok | CLI | yok | Linux ve macOS'ta derin yerel analiz için kullanılan araç; Windows x64 için deneysel. | 0:13 | bring-your-own Ghidra on Linux and macOS (karede: README paragrafı 'bring-your-own Ghidra on Linux and macOS, plus an experimental Windows x64 Ghidra P0') |
| Claude Code | yok | CLI | yok | REA'nın kayıt yaptığı desteklenen ajan. | 0:24 | REA detects Claude Code, Claude Desktop, Codex, Cursor (karede: Quick start: 'REA detects Claude Code, Claude Desktop, Codex, Cursor, Gemini CLI, Windsurf, and Devin') |
| Claude Desktop | yok | CLI | yok | REA'nın kayıt yaptığı desteklenen ajan. | 0:24 | REA detects Claude Code, Claude Desktop (karede: Aynı Quick start paragrafı) |
| Codex | yok | CLI | yok | Desteklenen ajan. | 0:24 | Claude Desktop, Codex, Cursor (karede: Aynı Quick start paragrafı) |
| Cursor | yok | CLI | yok | Desteklenen ajan. | 0:24 | Codex, Cursor, Gemini CLI (karede: Aynı Quick start paragrafı) |
| Gemini CLI | yok | CLI | yok | Desteklenen ajan. | 0:24 | Cursor, Gemini CLI, Windsurf (karede: Aynı Quick start paragrafı) |
| Windsurf | yok | CLI | yok | Desteklenen ajan. | 0:24 | Gemini CLI, Windsurf, and Devin (karede: Aynı Quick start paragrafı) |
| Devin | yok | CLI | yok | Algılanır ama yerel MCP yapılandırma sınırı olmadığından değiştirilmez. | 0:24 | Devin is reported but left unchanged (karede: Quick start paragrafı: Devin is reported but left unchanged) |
| npx | yok | CLI | yok | REA setup'ını çalıştırmak için paket çalıştırıcı. | 0:19 | npx --yes rea-agents@latest setup (karede: Run setup — recommended altında npx komutu) |
| Node.js | yok | teknik | yok | REA için gereken çalışma ortamı (22.19+). | 0:00 | Node.js 22.19+ (karede: README rozeti 'Node.js 22.19+') |
| Electron | yok | teknik | yok | Electron sayfası ve Node/Electron V8 Inspector gözlemi REA yetenekleri arasında. | 0:13 | Node/Electron V8 Inspector observation (karede: README paragrafı 'Electron page, and Node/Electron V8 Inspector observation') |
| gittrend.io | yok | iş akışı | yok | Reel'i yayınlayan trend repo takip sitesi. | 0:00 | gittrend.io (karede: Sağ altta gittrend.io rozeti) |
| npm | yok | CLI | yok | REA paketini global olarak kurmak için kullanılan paket yöneticisi. | 0:00 | npm install --global rea-agents && rea setup (karede: README'de kurulum kod bloğu; npm komutu gösteriliyor.) |
| V8 Inspector | yok | teknik | yok | Node ve Electron uygulamalarının çalışma zamanı gözlemi için kullanılan V8 hata ayıklayıcısı. | 0:00 | Node/Electron V8 Inspector observation (karede: README'de REA yetenek listesi; 'V8 Inspector observation' ifadesi görünüyor.) |
| Bir uygulamanın özelliğini tersine mühendislikle anlatıp uyarlamak | yok | prompt | yok | Notes uygulamasında aramanın nasıl çalıştığını anlat, kanıtı göster ve projem için benzer bir özellik oluştur. | 0:13 | kaynak: kare |
## Açıklama bağlantıları
- gittrend.io — Reel yayıncısının 'daha fazlası' sitesi · aday: evet (gittrend.io) · Videoda gösterilen trend repo takip sitesi; izleyicinin kullanabileceği servis. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm install --global rea-agents && rea setup | REA'yı global kurar ve setup sihirbazını başlatır. (karede: README başlığı altında kod satırı) | 0:00 | kare |
| npx rea-agents setup | Ajan entegrasyonu için MCP kaydı ve routing skill kurar. (karede: Just ask your agent bölümünde kod bloğu) | 0:09 | kare |
| npx --yes rea-agents@latest setup | En son REA sürümünü indirip setup sihirbazını çalıştırır. (karede: Run setup — recommended altında kod bloğu) | 0:19 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ajan, orijinal kaynak kodu olmadan yazılımı parçalarına ayırabilir. | 0:00 | özellik |
| Her şey kullanıcının kendi bilgisayarında çalışır, hiçbir şey yüklenmez. | 0:00 | özellik |
| REA bulguları kanıtlarıyla açıklar ve özelliğin kendi projeye uyarlanmış sürümünü üretebilir. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | REA: Reverse Engineer Anything | REA | README başlığı |
| kare 0:09 | npx rea-agents setup | rea-agents | Just ask your agent bölümü |
| kare 0:09 | MCP kaydı | MCP | aligned MCP registration |
| kare 0:09 | bundled routing skill | Routing skill | README metni |
| kare 0:21 | Hopper provider | Hopper | Quick start metni |
| kare 0:13 | Ghidra | Ghidra | README paragrafı |
| kare 0:24 | Claude Code | Claude Code | ajan listesi |
| kare 0:24 | Claude Desktop | Claude Desktop | ajan listesi |
| kare 0:24 | Codex | Codex | ajan listesi |
| kare 0:24 | Cursor | Cursor | ajan listesi |
| kare 0:24 | Gemini CLI | Gemini CLI | ajan listesi |
| kare 0:24 | Windsurf | Windsurf | ajan listesi |
| kare 0:24 | Devin | Devin | ajan listesi |
| kare 0:19 | npx --yes rea-agents@latest setup | npx | Quick start |
| kare 0:00 | Node.js 22.19+ | Node.js | rozet |
| kare 0:13 | Electron / V8 Inspector | Electron | README paragrafı |
| kare 0:00 | gittrend.io | gittrend.io | rozet ve açıklama |
| kare 0:00 | GitHub | aday değil: genel kavram | README'nin barındığı platform |
| kare 0:00 | npm | aday değil: başka adayın parçası (rea-agents) | paket kaydı rozeti |
| açıklama | #github #opensource #aiagents #reversengineering #devtools | aday değil: genel kavram | hashtag listesi |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamadı |
## Kareden okunanlar
- 0:00: GitHub morluto/rea README; 'REA: Reverse Engineer Anything'; npm v3.2.1, CI passing, MCP tool catalog, Node.js 22.19+, MIT; 'npm install --global rea-agents && rea setup'; altyazı 'POINT YOUR AGENT'
- 0:13: 'Just ask your agent' bölümü; 'npx rea-agents setup'; örnek Notes arama prompt'u; Decompile/Understand/Recreate tablosu
- 0:24: Quick start: 'npx --yes rea-agents@latest setup'; CLI and MCP, Local by design, Keeps context; desteklenen ajan listesi
## Belirsizlikler
- Konuşmada 'Ria' denmesi, ekranda 'REA' yazıyor; ad aynı araç sayılarak REA yazıldı.
- Yorumlar girişsiz alınamadı.
- Sözlükteki Next.js, React, Inter eşleşmeleri karelerde doğrulanamadı; aday yapılmadı.
- Altyazıda 'Comment Ria, and I'll send you the repo link' geçiyor; ayrı bir bağlantı verilmiyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/morluto/rea#readme | 0:00 | ekran | evet |
| gittrend.io | 0:00 | ekran | evet |
## İş akışı
- 1. adım — REA paketini global olarak kurma (npm install --global rea-agents) — araçlar: npm, Node.js
- 2. adım — REA kurulum sihirbazını çalıştırma (rea setup) — araçlar: REA, npm
- 3. adım — Ajan entegrasyonunu kurma: MCP kaydı ve yönlendirme skill'i (npx rea-agents setup) — araçlar: REA, MCP
- 4. adım — Algılanan ajanlar arasında yapılandırma seçimi ve son onay — araçlar: REA, Claude Code, Codex, Cursor
- 5. adım — Ajana uygulamadaki bir özelliği sorma (örnek prompt) — araçlar: Claude Code, REA
- 6. adım — Uygulamanın native ikili dosyasını ya da kodunu okuma ve ayrıştırma — araçlar: Ghidra, Hopper, REA
- 7. adım — Kod izini takip ederek özelliğin nasıl çalıştığını çıkarma — araçlar: REA, Claude Code
- 8. adım — Bulunan her adımı kanıtıyla birlikte raporlama — araçlar: REA
- 9. adım — Özelliğin kendi projen için benzer sürümünü üretme — araçlar: REA, Claude Code
## Promptlar
- Bir uygulamanın özelliğini tersine mühendislikle anlatıp uyarlamak — Notes uygulamasında aramanın nasıl çalıştığını anlat, kanıtı göster ve projem için benzer bir özellik oluştur.
ikinci göz KAPALI: --ikinci-goz yok
