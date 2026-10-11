# AI Agents Can Now Control the iOS Simulator
## Künye
AI Agents Can Now Control the iOS Simulator · Antoine van der Lee · süre: 5:36 · en-orig · https://youtu.be/mD6vpokRpsU · şema 2
motor: parti 2026-10-11-uzun-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 43950 tk · claude-haiku-5-5: claude-haiku-5-5 · 174731 tk
## Özet
Antoine van der Lee, RocketSim'in yeni CLI'sını ve paketlenmiş Agent Skill'ini tanıtıyor. Yapay zekâ ajanları iOS Simulator'ı kontrol edebiliyor. CLI, arka planda çalışan RocketSim Mac uygulamasıyla konuşuyor, rs/1 protokolüyle kompakt çıktı veriyor. Dahili kıyaslamada yaklaşık %19 daha hızlı, yanlış dokunma yok, yaklaşık %63 daha az tahmini token iddia ediliyor. Kurulum Ayarlar > CLI & Agent sayfasından yapılıyor. Erişilebilirlik ağacı IDB üzerine kurulu, sandbox ve kurumsal kullanıma uygun.
## Bölümler
- 0:00 Yapay zekâ ajanları iOS Simulator'ı kullanabiliyor
- 0:15 Token verimli Simulator kontrolü neden önemli
- 0:40 RocketSim CLI ve Agent Skill nasıl çalışıyor
- 1:12 CLI ve Agent Skill kurulumu
- 1:45 RocketSim ajanlar için neden daha hızlı
- 2:30 Kıyaslama sonuçları ve token tasarrufu
- 3:10 Erişilebilirlik ağacı iyileştirmeleri
- 3:50 Sandbox ve kurumsal kullanıma hazır
- 4:20 Örnek promptlar ve başlangıç
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| RocketSim | yok | CLI | yok | iOS Simulator için Mac uygulaması; ajanlara CLI ve Agent Skill sunuyor | 0:40 | we communicate with RocketSim CLI, which communicates with the RocketSim Mac app |
| RocketSim CLI | yok | CLI | yok | rocketsim komutu; çalışan Mac uygulamasıyla konuşan ajan odaklı CLI | 1:04 | Install Command Line Tool... düğmesi ve /opt/homebrew/bin/rocketsim symlink'i (karede: kanıttan) Install Command Line Tool... düğmesi ve /opt/homebrew/bin/rocketsim symlink'i |
| RocketSim Agent Skill | yok | skill | yok | Ajana RocketSim CLI'ın kullanımını öğreten paketlenmiş skill | 1:12 | we bundle the CLI and the agent skill in the Mac app itself |
| rs/1 protokolü | yok | teknik | yok | Ajanlar için kompakt çıktı veren özel protokol | 1:45 | we created what we like to call the RS1 protocol · kanıt: yok |
| Facebook IDB | yok | CLI | yok | Simulator erişilebilirlik öğelerini çeken açık kaynak proje | 3:10 | Many of the available tools rely on Facebook's IDB open-source project |
| Cursor | yok | CLI | yok | Skill kurulum hedefi ve ajan aracı | 1:08 | Cursor: Symlink the bundled RocketSim Agent Skill in ~/.cursor/skills (karede: kanıttan) Cursor: Symlink the bundled RocketSim Agent Skill in ~/.cursor/skills |
| Claude | yok | CLI | yok | Skill kurulum hedefi (~/.claude/skills) | 1:08 | Claude: Symlink the bundled RocketSim Agent Skill in ~/.claude/skills (karede: kanıttan) Claude: Symlink the bundled RocketSim Agent Skill in ~/.claude/skills |
| Codex | yok | CLI | yok | Skill kurulum hedefi (~/.codex/skills); demo ajanı Codex arayüzü olabilir | 1:08 | Codex: Symlink the bundled RocketSim Agent Skill in ~/.codex/skills (karede: kanıttan) Codex: Symlink the bundled RocketSim Agent Skill in ~/.codex/skills |
| GPT-5.5 | yok | teknik | yok | Demoda ajanın modeli (GPT-5.5 Medium) ve beta test alıntısı | 0:00 | Prompt kutusunda GPT-5.5 Medium seçimi (karede: kanıttan) Prompt kutusunda GPT-5.5 Medium seçimi |
| VoiceOver Overlay | yok | teknik | yok | RocketSim'in VoiceOver Navigator erişilebilirlik özelliği | 3:24 | our VoiceOver Overlay; there's nothing like that available elsewhere (karede: kanıttan) our VoiceOver Overlay; there's nothing like that available elsewhere |
| WKWebView | yok | teknik | yok | Kıyaslamada web giriş akışı senaryosu | 2:32 | a web login inside a WKWebView (karede: kanıttan) a web login inside a WKWebView |
| Mac App Store | yok | teknik | yok | RocketSim'in sandbox'lı dağıtım kanalı | 4:20 | We're sandboxed in the Mac App Store |
| Agent Skills | yok | skill | yok | Yeniden kullanılabilir ajan bilgisi; makale önerisi | 1:42 | Agent Skills explained: Replacing AGENTS.md with reusable AI knowledge (karede: kanıttan) Agent Skills explained: Replacing AGENTS.md with reusable AI knowledge |
| Claude Code | yok | CLI | yok | Açıklamada anılan ajan aracı | açıklama | using AI agents in Cursor, Claude Code, or other coding tools |
| iOS Simulator | yok | teknik | yok | Apple'ın iPhone simülatörü; ajanın kontrol ettiği hedef | 0:00 | Your AI agent can now use the iOS simulator |
| Demo: Team Docs erişilebilirlik doğrulaması | yok | prompt | yok | Team Docs sayfasına git ve erişilebilirlik desteğini rocketsim ile doğrula. | 0:00 | kaynak: kare |
| Örnek prompt: Ayarlar'da gezinme | yok | prompt | yok | /rocketsim ile Ayarlar'ı aç ve General'a git. | 4:46 | kaynak: kare |
| Örnek prompt: giriş akışı testi | yok | prompt | yok | /rocketsim ile giriş akışını user@example.com ile test et ve ana ekranın göründüğünü doğrula. | 4:47 | kaynak: kare |
## Açıklama bağlantıları
- https://www.avanderlee.com/ai-development/ai-powered-xcode-simulator-automation-token-efficient/ — Makale: AI-Powered Xcode Simulator Automation · aday: hayır · Videoda gösterilen makale; araç değil, bilgi sayfası · sınıf: diğer
- https://www.rocketsim.app — RocketSim ana sayfa / Mac App Store · aday: evet (RocketSim) · Alan adı videoda kullanılan RocketSim aracını adlandırıyor · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| rocketsim --help | CLI'ı doğrudan terminalden başlatır, yardım gösterir (karede: Makalede 'rocketsim --help to get started') | 1:38 | kare |
| /rocketsim | Sohbette paketlenmiş Agent Skill'i çağırır (karede: Use /rocketsim to open Settings and navigate to General.) | 4:46 | kare |
| --agent | CLI'da kompakt ajan çıktısı ister (karede: when to request compact --agent output) | 1:43 | kare |
| Install Command Line Tool... (RocketSim Ayarlar > CLI & Agent düğmesi) | rocketsim komutunu PATH üzerindeki bir klasöre (ör. /opt/homebrew/bin) symlink olarak kurar | 0:40 | altyazı |
| General Agents / Cursor / Claude / Codex 'Install' düğmeleri | Bundled Agent Skill'i ~/.agents/skills ve ajan skill klasörlerine symlink olarak kurar | 1:12 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| RocketSim aynı ajan iş akışlarını popüler bir alternatiften yaklaşık %19 daha hızlı tamamladı. | 2:30 | karşılaştırma |
| Yaklaşık %63 daha az tahmini token kullanıldı ve yanlış dokunma olmadı. | 2:30 | sayısal |
| CLI ve Agent Skill şu an ücretsiz. | 4:20 | özellik |
| RocketSim önbellekleme yapabilir ve ekran farklarını (diff) döndürebilir. | 0:40 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| 0:00 ekran | RocketSim | RocketSim | Yan pencere ve ajan demosu |
| 0:40 konuşma | RocketSim CLI | RocketSim CLI | we communicate with RocketSim CLI |
| 1:12 konuşma | Agent Skill | RocketSim Agent Skill | we bundle the CLI and the agent skill |
| 1:45 konuşma | RS1 protokolü | rs/1 protokolü | dedicated protocol specifically designed for agents |
| 3:10 konuşma | Facebook IDB | Facebook IDB | we use it, too |
| 1:08 kare | Cursor | Cursor | Cursor skills yolu |
| 1:08 kare | Claude | Claude | ~/.claude/skills |
| 1:05 kare | Codex | Codex | ~/.codex/skills |
| 0:00 kare | GPT-5.5 | GPT-5.5 | GPT-5.5 Medium |
| 3:24 kare | VoiceOver Overlay | VoiceOver Overlay | our VoiceOver Overlay |
| 2:32 kare | WKWebView | WKWebView | a web login inside a WKWebView |
| 4:20 konuşma | Mac App Store | Mac App Store | sandboxed in the Mac App Store |
| 4:27 kare | Guardsquare | aday değil: sponsor/reklam | Makalede SPONSOR kutusu |
| 1:10 kare | brew | aday değil: konu dışı | Klasör seçicide bin dosya listesi |
| 1:15 kare | seo-audit, popup-cro vb. skill klasörleri | aday değil: konu dışı | Skill klasör seçicisinde görünen diğer klasörler |
| açıklama | Claude Code | Claude Code | AI agents in Cursor, Claude Code |
| açıklama | aifundamentals.dev | aday değil: sponsor/reklam | Makalede Join the Waitlist banner |
| 1:42 kare | Agent Skills explained makalesi | Agent Skills | Agent Skills explained: Replacing AGENTS.md |
| yorum/sayfa | github.com/kean/Pulse | aday değil: konu dışı | Yalnız rocketsim.app sayfasında link |
## Kareden okunanlar
- 0:00: iPhone 17 Simulator'da Files ekranı; sağda ajan penceresi, GPT-5.5 Medium
- 1:04: CLI & Agent ayarları: Install Command Line Tool, General Agents, Cursor, Claude, Codex, skills-test
- 1:12: CLI kuruldu: /opt/homebrew/bin/rocketsim symlink
- 3:02: Senaryolar S1-S5 ve A1-A5 listesi
- 4:27: Makalede Guardsquare SPONSOR kutusu
## Belirsizlikler
- Demo ajan arayüzünün Codex mi Cursor mu olduğu net değil; yalnız GPT-5.5 Medium görülüyor.
- Karşılaştırılan 'popüler açık kaynak alternatif' adı verilmiyor.
- Kıyaslama rakamları dahili araştırma; bağımsız doğrulama yok.
- Sözlük eşleşmeleri (Next.js, Three.js, Astro, React vb.) videoda kullanılmıyor, sahte eşleşme.
- Altyazıda geçen 'Pulse' vb. bağlantılı sayfa içerikleri videoda anlatılmıyor.
## Atlanan segment oranı
0/10 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.avanderlee.com/ai-development/ai-powered-xcode-simulator-automation-token-efficient/ | açıklama | açıklama | hayır |
| https://www.rocketsim.app | açıklama | açıklama | evet |
| RocketSim.app | 1:12 | ekran | evet |
| example.com | 2:29 | ekran | hayır |
| https://github.com/AvdLee/RocketSimApp/issues | açıklama | açıklama | hayır |
| https://www.rocketsim.app/docs/features/agentic-development/rocketsim-cli | açıklama | açıklama | evet |
| https://www.avanderlee.com | açıklama | açıklama | hayır |
| https://www.youtube.com/@avanderlee?sub_confirmation=1 | açıklama | açıklama | hayır |
| https://www.aifundamentals.dev?utm_source=swiftlee&utm_medium=article&utm_campaign=inline-banner&source=swiftlee&ref=swiftlee-inline-banner | açıklama | açıklama | hayır |
| https://www.rocketsim.app/docs/features/accessibility/voiceover-navigator | açıklama | açıklama | evet |
| https://www.rocketsim.app/docs/features/agentic-development | açıklama | açıklama | evet |
| https://www.rocketsim.app/docs/features/agentic-development/agent-skill | açıklama | açıklama | evet |
| https://www.youtube.com/watch?v=ihVwU9usxgQ | açıklama | açıklama | hayır |
| https://github.com/kean/Pulse | açıklama | açıklama | hayır |
| https://github.com/kean | açıklama | açıklama | hayır |
| https://www.rocketsim.app/docs/features/physical-devices | açıklama | açıklama | evet |
| https://www.youtube.com/watch?v=xK3iI5TzuA4 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=zTbQck3ofcc | açıklama | açıklama | hayır |
| https://www.rocketsim.app/docs/features/app-actions/location-simulation | açıklama | açıklama | evet |
| https://www.youtube.com/watch?v=zukRdke1cP8 | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=RQ7tXHyY5Ic | açıklama | açıklama | hayır |
| https://github.com/AvdLee/RocketSimApp | açıklama | açıklama | evet |
| https://RocketSim.app/docs/features/physical-devices | açıklama | açıklama | evet |
| https://RocketSim.app/docs/features/app-actions/location-simulation | açıklama | açıklama | evet |
## İş akışı
- 1. adım — Simulator'da uygulamayı açık tutup sohbet ajanına Team Docs erişilebilirlik doğrulama görevini ver — araçlar: iOS Simulator, GPT-5.5 Medium (sohbet ajanı)
- 2. adım — Ajan ekranın anlık görüntüsünü ve gezinilebilir öğeleri alır — araçlar: RocketSim CLI, RocketSim Agent Skill
- 3. adım — Ajan Team Docs öğesine dokunur — araçlar: RocketSim CLI
- 4. adım — Ajan ayrıntılı hata ayıklama (debug) ağaç görüntüsünü alır — araçlar: RocketSim CLI
- 5. adım — Ajan etiketli (annotated) ekran görüntüsünü kaydeder — araçlar: RocketSim CLI
- 6. adım — Ajan erişilebilirlik etiketlerini ve rolleri doğrular, metadata'yı kontrol eder — araçlar: RocketSim CLI, rs-screen.json
- 7. adım — RocketSim Ayarlar > CLI & Agent sayfasında komut satırı aracını kurar — araçlar: RocketSim, macOS dosya seçici (/opt/homebrew/bin)
- 8. adım — Agent Skill'i General Agents yolu ve Cursor, Claude, Codex hedeflerine kurar — araçlar: RocketSim, RocketSim Agent Skill
- 9. adım — Kurulum sonrası kontrolü yapar: CLI symlink ve skill klasörleri doğrulanır — araçlar: RocketSim, RocketSim CLI
- 10. adım — Makaledeki örnek promptları (/rocketsim) sohbete yazar ve sonuçlara bakar — araçlar: RocketSim Agent Skill, sohbet ajanı
- 11. adım — Benchmark senaryolarını (gezinme, dokunma, kurtarma) açıklar ve sonuçları karşılaştırır — araçlar: RocketSim CLI, açık kaynak alternatif (adı verilmiyor)
- 12. adım — Erişilebilirlik ağacı farkını (IDB ile karşılaştırma) gösterir — araçlar: Facebook IDB, RocketSim
- 13. adım — Sandbox'lı yapı ve Mac App Store dağıtımını anlatır, uygulamayı ücretsiz indirme yönlendirmesi yapar — araçlar: Mac App Store, RocketSim
## Promptlar
- Demo: Team Docs erişilebilirlik doğrulaması — Team Docs sayfasına git ve erişilebilirlik desteğini rocketsim ile doğrula.
- Örnek prompt: Ayarlar'da gezinme — /rocketsim ile Ayarlar'ı aç ve General'a git.
- Örnek prompt: giriş akışı testi — /rocketsim ile giriş akışını user@example.com ile test et ve ana ekranın göründüğünü doğrula.
ikinci göz KAPALI: --ikinci-goz yok
