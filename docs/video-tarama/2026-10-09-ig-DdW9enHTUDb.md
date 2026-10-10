# Rehber Bağlantısı: https://guides.yasinarsal.com/10-adet-claude-hacki
## Künye
Rehber Bağlantısı: https://guides.yasinarsal.com/10-adet-claude-hacki · yasin.arsal · süre: 0:50 · ? · https://www.instagram.com/reel/DdW9enHTUDb/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-30 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 74953 tk · claude-haiku-5-5: claude-haiku-5-5 · 87006 tk
## Özet
Claude Code'u yaratan Boris Cherny'nin 10 ipucundan ilk dördü anlatılıyor: Plan Mode (Shift-Tab), git worktree ile paralel Claude oturumları, hata sonrası CLAUDE.md güncelletme ve iş akışını otomatikleştiren alt ajanlar. Kalan 6 ipucu için yorumlara 'rehber' yazılırsa bağlantı paylaşılıyor.
## Bölümler
- 0:00 Giriş: Boris Cherny'nin ipuçları
- 0:04 1. Plan Mode kullan
- 0:15 2. Paralel Claude agent'ları
- 0:27 3. CLAUDE.md
- 0:35 4. Alt ajanlar
- 0:45 Kalan 6 ipucu için rehber
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Anthropic'in terminal tabanlı kodlama ajanı; videonun ana aracı. | 0:00 | Claude Code'u yaratan adam Boris Cherny'nin kullandığı 10 ipucu |
| Plan Mode | yok | ipucu | yok | Koda dokunmadan önce plan çıkarır; Shift-Tab ile açılır. | 0:11 | Ekranda 'Plan = Less Errors' ve ExitPlanMode izin penceresi var. (karede: Üstte 'Plan = Less Errors' başlığı, ortada 'Allow Claude to ExitPlanMode ?' penceresi, altyazı 'plan=daha az hata'.) |
| Git Worktree | yok | teknik | yok | Paralel Claude oturumlarını ayrı çalışma dizinlerinde yürütmek için. | 0:21 | git work tree veya agent teams kullanarak |
| Agent Teams | yok | teknik | yok | Paralel çalışma için anılan ajan ekibi özelliği. | 0:21 | Git Worktree veya Agent Teams kullanarak 3 ila 5 kat daha hızlı |
| CLAUDE.md | yok | ipucu | yok | Hataları kalıcı belleğe çeviren talimat dosyası; ajan hata yapınca güncellenir. | 0:31 | Editörde CLAUDE.md açık, kurallar yazılı. (karede: CLAUDE.md sekmesi, '# Remotion Project — Claude Instructions', 'B-Roll Versioning Rule', altyazı 'kendi claude md dosyasını güncellemesini söyleyin'.) |
| Alt ajanlar | yok | teknik | yok | Kod yazan, inceleyen ve yayına alan ayrı ajanlar. | 0:38 | mesela bi agent kod yazsın, diğer agent kodu incelesin |
| Remotion | yok | teknik | yok | CLAUDE.md örneğindeki React tabanlı video projesi. | 0:31 | CLAUDE.md başlığında Remotion Project yazıyor. (karede: '# Remotion Project — Claude Instructions' ve 'using Remotion (React-based video)'.) |
| GitHub CLI (gh) | yok | CLI | yok | GitHub issue'larını terminalden görüntülemek için kullanılan komut | 0:15 | Sağ terminal panelinde 'Bash(gh issue view 6)' satırı; OCR 'gh' okumasını bozuk veriyor · kanıt: kare (karede: Sağ terminal panelinde 'Bash(gh issue view 6)' satırı; OCR 'gh' okumasını bozuk veriyor) |
| code-reviewer subagent | yok | teknik | yok | Performans sorunlarını bulmak için çağrılan alt-agent | 0:38 | 'First use the @code-reviewer subage' ekran metni · kanıt: kare (karede: 'First use the @code-reviewer subage' ekran metni) |
| debugger agent | yok | teknik | yok | Bulunan performans sorunlarını düzeltmek için çağrılan alt-agent | 0:40 | 'Next: Use debugger agent to fix identified performance issues' (karede: kanıttan) 'Next: Use debugger agent to fix identified performance issues' |
| Claude Opus 4.5 | yok | teknik | yok | Claude Code oturumunda kullanılan ana yapay zekâ modeli | 0:34 | Oturum ekranında 'Opus 4.5' model satırı · kanıt: kare (karede: Oturum ekranında 'Opus 4.5' model satırı) |
| VS Code | yok | teknik | yok | CLAUDE.md dosyasının açık olduğu kod editörü (arayüz benzeri, emin değil) | 0:31 | Sekmede 'CLAUDE.md' ve üstte dosya yolu gezgini görünümü · kanıt: kare (karede: Sekmede 'CLAUDE.md' ve üstte dosya yolu gezgini görünümü) |
| MCP | yok | teknik | yok | Model Context Protocol; Claude Code'a dış servis sunucularını bağlar | 0:08 | 'MCP servers. They'll work here, too!' (karede: kanıttan) 'MCP servers. They'll work here, too!' |
| AskUserQuestion | yok | teknik | yok | Claude'un gereksinim netleştirmek için kullanıcıya soru sormasını sağlayan araç | 0:09 | Ekran metninde '• AskUserQuestion' satırı (karede: kanıttan) Ekran metninde '• AskUserQuestion' satırı |
| Yemek siparişi uygulaması MVP'si | yok | prompt | yok | Yemek siparişi uygulaması için MVP geliştirilmesini ister. | 0:00 | kaynak: kare |
| Plan Mode ile özellik planlama | yok | prompt | yok | Haftalık yemek planı ve alışveriş listesi özelliği eklenmesini ister; tek index.html, localStorage. | 0:09 | kaynak: kare |
## Açıklama bağlantıları
- https://guides.yasinarsal.com/10-adet-claude-hacki — Yazarın 10 Claude hack'i rehber sayfası · aday: hayır · Yazarın kendi rehberi; izleyicinin kullanacağı araç değil, içerik sayfası. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| Shift-Tab | Claude Code'da Plan Mode'u etkinleştirir. | 0:04 | altyazı |
| /init | CLAUDE.md dosyası oluşturur. (karede: Claude Code karşılama ekranında 'Run /init to create a CLAUDE.md file' ipucu.) | 0:34 | kare |
| claude | Terminalde Claude Code oturumunu başlatır (proje klasöründe) (karede: (karede OCR) ClaudeCode claude-agent-sdk-demos % claude Claude Code v2.8.68 started Tips for getting Welcome back Claude! Run /init to create a CLAUDE Recent activity No recent activity Opus 4.5 . Claude Max -/Pro) | 0:34 | kare |
| gh issue view 6 | GitHub issue 6'nın ayrıntılarını terminalde gösterir (karede: Sağ terminal panelinde 'Bash(gh issue view 6)' satırı) | 0:15 | kare |
| git worktree | Aynı repo için ayrı çalışma dizinleri açar; paralel agent oturumları için kullanılır (yalnızca adı söylenir, komut gösterilmez) | 0:00 | altyazı |
| ctrl-g | Claude Code'da prompt'u Vim içinde düzenler (karede: (karede OCR) ClaudeCode claude-agent-sdk-demos % claude Claude Code v2.0.60 Tips for getting started Run /init to create a CLAUDE.md file with Welcome back Claude! Recent activity No recent activity Opus 4.5 - Cla) | 0:35 | kare |
| Ctrl+Esc | VS Code'da Claude paneline odağı verir ya da çıkarır (karede: (karede OCR) * Claude Code × ... Untitled + Claude Code Use Claude Code in the terminal to configure Th~/ll...lh. AACD ktrl esc to focus or unfocus Claude </> Edit automatically index.html + │ koda dokunmadan önce) | 0:06 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Plan modu ileride çıkabilecek birçok hatayı önler. | 0:09 | özellik |
| Git Worktree veya Agent Teams ile proje 3-5 kat daha hızlı biter. | 0:21 | sayısal |
| Plan Mode Shift-Tab tuşlarıyla etkinleşir. | 0:04 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Boris Cherny | aday değil: konu dışı | Ekranda @bcherny ve Boris Cherny yazıyor. |
| konuşma 0:00 | Claude Code | Claude Code | Claude Code'u yaratan adam |
| konuşma 0:04 | Plan Mode | Plan Mode | Her zaman plan modunu kullanın |
| konuşma 0:21 | Git Worktree | Git Worktree | git work tree veya agent teams |
| konuşma 0:21 | Agent Teams | Agent Teams | git work tree veya agent teams |
| kare 0:31 | CLAUDE.md | CLAUDE.md | CLAUDE.md editör sekmesi |
| kare 0:31 | Remotion | Remotion | Remotion Project başlığı |
| konuşma 0:38 | Alt ajanlar | Alt ajanlar | alt ajanlar kullanın |
| açıklama | guides.yasinarsal.com rehberi | aday değil: konu dışı | Açıklamadaki rehber bağlantısı |
| ekran 0:41 | Playwright | aday değil: konu dışı | OCR'de '# Playwright traces' satırı |
## Kareden okunanlar
- 0:11: 'Plan = Less Errors'; 'Allow Claude to ExitPlanMode ?' penceresi; Allow once/Deny; altyazı 'plan=daha az hata'.
- 0:15: 'Run Parallel Claude Agents'; iki terminal bölmesi, worktree yolları; altyazı '2 paralel claude agent'ları çalıştırın'.
- 0:31: CLAUDE.md editörü: Remotion Project, Purpose, B-Roll Versioning Rule; altyazı 'kendi claude md dosyasını güncellemesini söyleyin'.
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Sözlükteki Codex, Cursor, Inter, Supabase vb. eşleşmeleri videoda kullanılmıyor; aday yapılmadı.
- Altyazıdaki 'Cloud' sesi Claude demektir; 'Boris Churn' Boris Cherny olarak yazıldı.
- Ekranda geçen Playwright, Next.js, Hermes Agent, TypeScript yalnızca ekran görüntüsünde belirip anlatılmıyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://guides.yasinarsal.com/10-adet-claude-hacki | açıklama | açıklama | hayır |
| https://www.instagram.com/reel/DdW9enHTUDb/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Plan Mode'a Shift-Tab ile geçilir. — araçlar: Claude Code, Plan Mode
- 2. adım — Ajan plan çıkarır, ExitPlanMode onayı verilir. — araçlar: Claude Code
- 3. adım — Paralel Claude oturumları ayrı worktree'lerde çalıştırılır. — araçlar: Git Worktree, Agent Teams
- 4. adım — Hata sonrası ajana CLAUDE.md güncellettirilir. — araçlar: CLAUDE.md
- 5. adım — Alt ajanlar kod yazma, inceleme ve yayına alma için kullanılır. — araçlar: Alt ajanlar
## Promptlar
- Yemek siparişi uygulaması MVP'si — Yemek siparişi uygulaması için MVP geliştirilmesini ister.
- Plan Mode ile özellik planlama — Haftalık yemek planı ve alışveriş listesi özelliği eklenmesini ister; tek index.html, localStorage.
