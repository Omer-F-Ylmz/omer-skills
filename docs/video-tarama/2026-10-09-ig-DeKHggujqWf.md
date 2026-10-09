# Reverse engineer anything with agents, from app behavior down to native binaries
## Künye
Reverse engineer anything with agents, from app behavior down to native binaries · git.radar · süre: 1:06 · ? · https://www.instagram.com/reel/DeKHggujqWf/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-38 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 40878 tk · claude-haiku-5-5: claude-haiku-5-5 · 34423 tk
## Özet
git.radar kısa videosu, GitHub'da trend olan REA (Reverse Engineer Anything) aracını tanıtıyor. REA, ajanı MCP üzerinden ikili dosyalara, Electron/JavaScript uygulamalarına ve .NET assembly'lerine bağlıyor. Analiz yerelde çalışıyor. Kullanıcı bir uygulamadaki özelliğin nasıl çalıştığını sorup kendi projesi için benzerini yazdırabiliyor. Ekranda npx rea-agents setup, skills add, curl install.sh ve npm install komutları görünüyor.
## Bölümler
- 0:00 REA tanıtımı ve GitHub deposu
- 0:35 Hızlı başlangıç: setup ve desteklenen ajanlar
- 0:49 Skill kurulumu ve ilk analiz komutu
- 1:00 CLI kurulumu ve GitHub'a yönlendirme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| REA | yok | MCP | https://github.com/morluto/rea | Ajanı ikili dosya, uygulama ve çalışma zamanı davranışı tersine mühendisliğine bağlayan, yerel çalışan MCP. | 0:00 | README başlığı: One MCP for reverse engineering across binaries, applications, and runtime behavior. (karede: Kare 1: 'REA: Reverse Engineer Anything' başlığı, npm v4.0.1 ve MCP rozetleri, #3 Repository Of The Day.) |
| rea-agents | yok | CLI | https://github.com/morluto/rea | REA'yı ajanlara kaydeden setup ve analiz komutlarını içeren npm paketi. | 0:44 | Quick start altında npx rea-agents setup kutusu görünüyor. (karede: Kare 2: 'Run setup (recommended)' altında 'npx rea-agents setup' kutusu.) |
| reverse-engineer-anything | yok | skill | https://github.com/morluto/rea | Ajan talimatlarını kuran skill; MCP kaydı ve analiz motoru kurmaz. | 0:51 | Ekran metni: npx skills add morluto/rea --skill reverse-engineer-anything (karede: Gönderilen 3 karede yok; 0:51 OCR metninden okundu.) |
| Skills CLI | yok | CLI | yok | skills.sh üzerinden skill kuran npx skills komutu. | 0:49 | Ekran metni: npx skills add ...; skills.sh anılıyor. (karede: Gönderilen karelerde yok; 0:49-0:51 OCR metninden okundu.) |
| Claude Code | yok | CLI | yok | REA'nın desteklediği ajanlardan biri. | 0:44 | REA supports Claude Code, Claude Desktop, Codex, Cursor... (karede: Kare 2: 'REA supports Claude Code, Claude Desktop, Codex, Cursor, Gemini CLI, Windsurf, Devin, OpenCode, Antigravity, GitHub'.) |
| Claude Desktop | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: desteklenen ajan listesi satırında 'Claude Desktop'.) |
| Codex | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: listede 'Codex'.) |
| Cursor | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: listede 'Cursor'.) |
| Gemini CLI | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: 'Gemini CLI, Windsurf, Devin, OpenCode, Antigravity'.) |
| Windsurf | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: listede 'Windsurf'.) |
| Devin | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: listede 'Devin'.) |
| OpenCode | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: listede 'OpenCode'.) |
| Antigravity | yok | CLI | yok | Desteklenen ajan listesinde. | 0:44 | Desteklenen ajan listesinde yazıyor. (karede: Kare 2: listede 'Antigravity'.) |
| GitHub Copilot CLI | yok | CLI | yok | Desteklenen ajan listesinde. | 0:45 | Ekran metni: GitHub Copilot CLI, Command Code, VS Code. · kanıt: kare (karede: Kare 3: 'GitHub Copilot CLI, Command Code, and VS Code' satırı altyazının arkasında kısmen görünüyor.) |
| Command Code | yok | CLI | yok | Desteklenen ajan listesinde. | 0:45 | Ekran metni: Command Code. (karede: Kare 3: 'Command Code' satırı kısmen görünüyor.) |
| VS Code | yok | CLI | yok | Desteklenen ajan listesinde. | 0:45 | Ekran metni: and VS Code. (karede: Kare 3: 'and VS Code' kısmen görünüyor.) |
| Hopper | yok | CLI | yok | Yerel analiz motoru; onayla kurulur, demo modu var. | 0:44 | Hopper can run in demo mode; Hopper is a separate optional choice. (karede: Kare 2: 'Hopper can run in demo mode' ve 'Hopper is a separate optional choice'.) |
| Ghidra | yok | CLI | yok | Setup'ın kaydedebildiği yerel analiz motoru. | 0:44 | Setup can also record an existing Ghidra installation. (karede: Kare 2: 'Setup can also record an existing Ghidra installation.') |
| Node.js | yok | teknik | yok | REA için gerekli çalışma zamanı (22.19+). | 0:00 | Node.js 22.19+ rozeti. (karede: Kare 1: yeşil 'Node.js 22.19+' rozeti.) |
| npm | yok | CLI | yok | rea-agents paketinin kurulumu için paket yöneticisi. | 1:05 | npm install --global rea-agents (karede: Gönderilen karelerde yok; 1:05 OCR; kare 1'de npm v4.0.1 rozeti.) |
| npx | yok | CLI | yok | setup ve analiz komutlarını çalıştırır. | 0:44 | npx rea-agents setup (karede: Kare 2: 'npx rea-agents setup' kutusu.) |
| Electron | yok | teknik | yok | REA'nın incelediği uygulama türü (ASAR). | 0:09 | JavaScript and Electron apps, .NET assemblies (karede: Gönderilen karelerde yok; 0:09 OCR metni.) |
| .NET assemblies | yok | teknik | yok | REA'nın analiz edebildiği hedef türü. | 0:09 | OCR: .NET assemblies (karede: Gönderilen karelerde yok; 0:09 OCR metni.) |
| install.sh | yok | CLI | https://github.com/morluto/rea | curl ile indirilen REA yükleyici betiği. | 1:03 | curl -fsSL https://raw.githubusercontent.com/morluto/rea/main/install.sh (karede: Gönderilen karelerde yok; 1:03 OCR.) |
| Uygulama özelliğini tersine mühendislikle anlayıp kendi projeye uyarlama | yok | prompt | yok | Notes uygulamasında aramanın nasıl çalıştığını anlat, kanıtı göster ve projem için benzer bir özellik yaz. | 0:15 | kaynak: kare |
## Açıklama bağlantıları
- https://github.com/morluto/rea — REA GitHub deposu · aday: evet (REA) · Videoda anlatılan REA aracının deposu; izleyici kurup kullanabilir. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx rea-agents setup | REA'yı seçilen ajanlara MCP ve rehberli iş akışıyla kaydeder. (karede: Kare 2: 'Run setup (recommended)' altında 'npx rea-agents setup' kutusu.) | 0:44 | kare |
| npx skills add morluto/rea --skill reverse-engineer-anything | Ajan talimatları skill'ini kurar; MCP kaydı yapmaz. (karede: Gönderilen karelerde yok; 0:51 OCR metni.) | 0:51 | kare |
| npx -y rea-agents@latest analyze-javascript-application /absolute/path/ | MCP kurmadan çıkarılmış JS/Electron uygulamasını statik analiz eder. (karede: Gönderilen karelerde yok; 0:58 OCR metni.) | 0:58 | kare |
| curl -fsSL https://raw.githubusercontent.com/morluto/rea/main/install.sh | rea CLI yükleyicisini indirir; kurulumda setup başlar. (karede: Gönderilen karelerde yok; 1:03 OCR metni.) | 1:03 | kare |
| npm install --global rea-agents | rea CLI'yı npm ile global kurar. (karede: Gönderilen karelerde yok; 1:05 OCR metni.) | 1:05 | kare |
| rea update | Kurulu REA'yı günceller. (karede: Gönderilen karelerde yok; 1:04 OCR metni.) | 1:04 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| REA 7.565 yıldıza ulaştı. | 0:00 | sayısal |
| Analiz yerel makinede çalışır, uygulama barındırılan servise yüklenmez. | 0:31 | özellik |
| REA özgün kaynak kodu kurtarmayı ya da otomatik klonlamayı iddia etmez. | 0:23 | özellik |
| Kullanıcının profesyonel programcı olması gerekmez. | 0:38 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | morluto/rea GitHub deposu | REA | Kare 1 depo başlığı |
| kare 0:00 | GitHub Trending rozeti | aday değil: konu dışı | #3 Repository Of The Day |
| kare 0:00 | npm rozeti | npm | npm v4.0.1 |
| kare 0:00 | Node.js 22.19+ | Node.js | rozet |
| kare 0:00 | Discord rozeti | aday değil: konu dışı | Discord 78 online |
| kare 0:44 | Claude Code, Claude Desktop, Codex, Cursor | Claude Code | ajan listesi |
| kare 0:44 | Gemini CLI, Windsurf, Devin, OpenCode, Antigravity | Gemini CLI | ajan listesi |
| kare 0:45 | GitHub Copilot CLI, Command Code, VS Code | GitHub Copilot CLI | ajan listesi |
| kare 0:44 | Hopper | Hopper | demo modu |
| kare 0:44 | Ghidra | Ghidra | Ghidra kurulumu |
| ekran 0:51 | skills.sh / skills add | Skills CLI | komut |
| ekran 0:51 | reverse-engineer-anything skill | reverse-engineer-anything | komut |
| ekran 0:09 | Electron ve .NET assemblies | Electron | OCR |
| ekran 0:58 | analyze-javascript-application | rea-agents | komut |
| ekran 1:03 | install.sh | install.sh | curl komutu |
| açıklama | TypeScript etiketi | aday değil: genel kavram | 🔵 TypeScript |
| açıklama | Hashtag'ler | aday değil: genel kavram | #opensource #coding |
| konuşma 0:00 | Dijital asistan | aday değil: genel kavram | your computer's digital assistant |
| açıklama | github.com/morluto/rea | REA | açıklama bağlantısı |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamıyor |
## Kareden okunanlar
- 0:00: morluto/rea, 66 issue, 1 PR, 5af1699 commit, README: REA: Reverse Engineer Anything, npm v4.0.1, CI passing, MIT, Discord 78 online, #3 Repository Of The Day, npx rea-agents setup.
- 0:44: Quick start; 'npx rea-agents setup'; setup ajan seçimi, Hopper demo modu, Ghidra; desteklenen ajan listesi.
- 0:46: 0:44 karesine benzer sayfa; ajan listesi altyazı arkasında kısmen kapalı.
## Belirsizlikler
- Sunucunun içinde çalıştığı ana yapay zekâ modeli videoda belirtilmiyor.
- Ses ve açıklamada ad 'Ria' diye geçiyor; ekranda REA yazıyor, REA alındı.
- curl komutunun sonu (/ sh) OCR'de net değil.
- OCR'deki bazı satırlar altyazıyla karışmış; komutlar elle düzeltildi.
- Yorumlar girişsiz alınamadı.
- Discord ve Roadmap/Tool catalog bağlantıları yalnız anıldı.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/morluto/rea | açıklama | açıklama | evet |
| https://www.instagram.com/reel/DeKHggujqWf/ | açıklama | açıklama | hayır |
| skills.sh | 0:51 | ekran | evet |
| https://raw.githubusercontent.com/morluto/rea/main/install.sh | 1:03 | ekran | evet |
## İş akışı
- 1. adım — Gerekli Node.js 22.19+ sürümünü ve npm'i hazırlama — araçlar: Node.js, npm
- 2. adım — REA setup'ı çalıştırıp ajanları seçme — araçlar: npx, rea-agents
- 3. adım — Değişiklikleri onaylayıp MCP erişimini kaydetme — araçlar: REA, Claude Code, Cursor
- 4. adım — İsteğe bağlı Hopper veya Ghidra motorunu bağlama — araçlar: Hopper, Ghidra
- 5. adım — Ajanı yeniden başlatıp uygulama veya özellik tarif etme — araçlar: Claude Code, Codex, REA
- 6. adım — Ajanın kanıtla analizi ve kendi sürümü yazması — araçlar: REA, Hopper
- 7. adım — Alternatif: skill kurma — araçlar: Skills CLI, reverse-engineer-anything
- 8. adım — Terminalden JS uygulaması analizi — araçlar: rea-agents, npx
- 9. adım — CLI'yı curl veya npm ile kurma — araçlar: install.sh, npm
- 10. adım — rea update ile güncelleme — araçlar: rea-agents
## Promptlar
- Uygulama özelliğini tersine mühendislikle anlayıp kendi projeye uyarlama — Notes uygulamasında aramanın nasıl çalıştığını anlat, kanıtı göster ve projem için benzer bir özellik yaz.
