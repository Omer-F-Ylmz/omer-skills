# Uzun oturum tarama — YouTube · 2026-09-17
8 sorgu (EN context window/token usage/memory/compaction · TR context/token tasarrufu/uzun oturum/hafıza) · bulunan 95 tekil · 30-gün-içi (≥20260818) 11 · işlenen 11/15 (havuzda daha fazla yok) · tavan: yt-dlp arama 9/10 · altyazı indirme 8 video/15 (3'ü 429 sonrası "altyazı yok") · Exa 0/5 · gh+curl doğrulama ~9/30
IKfUxgO0apE · 20260914 · EN · AI Dive "5 Rules To Stop AI Specs From Rotting" · Superpowers(bilinen)/spec-kit/Kiro
iCyGIF5uIzo · 20260906 · TR · Emrullah Yaprak "Fable 5.1 Profesyonel Web Sitesi" · altyazı yok (429)
yFvl2x8_9gI · 20260906 · EN · Jordan Urbs "Why I Cancelled My Claude Code Subscription" · Venice AI/OpenCode
F8UYuyma3lc · 20260903 · TR · Algoritim Bilişim "Kendi Claude Code'umu Yazabilir Miyim?" · altyazı yok (429)
hAYPvExWmCw · 20260901 · TR · Selma Kocabıyık "Hafızayı Sıfırdan Anlattım" · ÖNCEKİ TARAMA (hAYPvExWmCw.md)
Jf54k7tFeEc · 20260825 · EN · Theo/t3.gg "Turn off Claude Code's Memory" · auto-memory denetimi
sRCTOxc4658 · 20260825 · TR · Avenox "130 Gündür Kendi Hafızasını Yazıyor" · altyazı yok (429)
XemheY_aM1g · 20260821 · TR · Burhan Kocabıyık "MiniMax'i Claude Code'a Bağlayıp" · ÖNCEKİ TARAMA (XemheY_aM1g.md)
Gg35_iQWx7g · 20260820 · TR · Burhan Kocabıyık "Yapay Zekayı Verimli Kullanmak" · ÖNCEKİ TARAMA (Gg35_iQWx7g.md)
kHtOSJRUkLs · 20260819 · EN · Sharbel A. "Never Run Out Of Tokens Again" · token-audit prompt
YAsxyoTWFDA · 20260818 · EN · The Coding Sloth "1000+ Hours With Claude Code" · ponytail/rtk-ai/caveman/skills.sh
## tablo
| araç/ayar | durum | etiket | not |
|---|---|---|---|
| DietrichGebert/ponytail | YENİ | ELENDİ | CLAUDE.md "En basit çözüm" satırıyla çift; kural setini her SessionStart (compact dahil) + SubagentStart'ta yeniden basar (ana oturum doğrulaması, aşağıda) |
| rtk-ai/rtk | ZATEN VAR | — | tanım kurulu RTK 0.49 ile birebir aynı (token sıkıştırma CLI) |
| skills.sh (vercel-labs/skills CLI) | ZATEN VAR | — | önceki taramada (99-sentez) değerlendirildi, `npx skills add` |
| JuliusBrussee/caveman | YENİ | ELENDİ | ponytail'in kendi ölçümünde token/maliyet/süreyi baseline'a göre artırıyor; lisans MIT değil ("Other") |
| github/spec-kit · Amazon Kiro | ÇİFT | ELENDİ | IDE/spec-workflow alternatifi; Superpowers zaten KAPAT (99-sentez §3) |
| Theo: auto memory'yi kapat (görüş) | YENİ | ELENDİ | altyazıda denetim kalıbı yok, "for coding, I don't want a memory" görüşü; kurulu MEMORY.md 62 token (/context), kapatma kazancı ihmal edilebilir |
| Sharbel: token-audit prompt (CLAUDE.md boyutu, tool deferral, memory, proxy env, subagent model) | ÇİFT | ELENDİ | /context + /skill-doctor + skill-kapatma.md `claude -p --output-format json` ölçümü aynı işi yapıyor |
## YENİ ölçütler (ana oturumda düzeltildi; caveman: ponytail A/B ölçümünde baseline'dan kötü, lisans "Other" okunmadı → ELENDİ)
- DietrichGebert/ponytail: bakım=push 2026-09-14 · 140.8k★ · MIT · 95 açık issue (GraphQL; 274 PR dahil sayımdı) · açılış 2026-06-12 · çift=~/.claude/CLAUDE.md "En basit çözüm: istenmeyen özellik/soyutlama… yok" ile aynı kural ("YAGNI, stdlib first, no unrequested abstractions") · izin=plugin, node PATH, hook kodunda ağ çağrısı yok · context=kural seti `skills/ponytail/SKILL.md` mod süzgeçli ≤6637 bayt ≈ ≤1.7k token · uzun oturum=`hooks/claude-codex-hooks.json`: SessionStart `startup|resume|clear|compact` → her /clear ve compact'ta ≤1.7k yeniden; SubagentStart → her subagent'e ≤1.7k (bu taramada 5 subagent ≈ 8.5k); UserPromptSubmit her prompt'ta node süreci, çıktı yalnız /ponytail komutunda (her tur enjeksiyonu yalnız Qoder'da, `ponytail-mode-tracker.js`) → ELENDİ
