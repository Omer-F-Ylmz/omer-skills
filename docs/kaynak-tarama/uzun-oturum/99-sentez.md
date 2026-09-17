# Kaynak tarama 2 — uzun oturum + token · sentez · 2026-09-17
5 kaynak, her biri ayrı sonnet subagent + Agent Reach; kurulum ve ayar değişikliği yok. Sonnet çıktıları ana oturumda örneklemle doğrulandı; subagent ADAY'larının üçü de hook/plugin dosyası okununca düştü (§4).
| kaynak | taranan | ZATEN VAR | BİLGİ | ELENDİ | not |
|---|---|---|---|---|---|
| a GitHub | 157 repo, 28 konu eşleşen | 1 | 0 | 15 | 4 repo 60g ★ artışı ölçülemedi |
| b YouTube | 95 video, 30 günde 11 | 2 | 0 | 7 | 5 yeni altyazı işlendi · 3 önceki tarama · 3 YouTube 429 |
| c Reddit | DUR | 3 | 1 | 3 | reddit.com curl+Jina 403, Exa tarih filtresi işlemiyor → pencerede 0 gönderi; kalemler pencere dışı referans |
| d X/Twitter | 0 | 0 | 0 | 0 | Jina x.com anonim 403, Exa tweet döndürmedi |
| e Anthropic | changelog 2.1.235→2.1.274 · 8 docs sayfası · 1 blog yazısı | 7 | 1 | 2 | docs'ta pencerede yeni "As of" notu yok |

## 1. ADAY (0)
Beş ölçütü geçen kalem yok, kurulum komutu yok. Önerilen üç aday tur başı/compaction maliyeti ve kurulu kurallarla çiftlik yüzünden ELENDİ (§4).

## 2. BİLGİ → hedef
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` → İŞ 1 autocompact kararı (settings.json `env`). docs/en/env-vars: "Set the percentage (1-100) of the auto-compact window at which auto-compaction triggers. Use lower values like `50` to compact earlier; the variable can't raise the threshold … Applies to both main conversations and subagents". `/autocompact`, `--autocompact` ve `CLAUDE_CODE_AUTO_COMPACT_WINDOW` yanında dördüncü yol; yalnız eşiği düşürür. İŞ 1 doküman subagent'inin "böyle bir env var yok" demesi yanlıştı. (c + ana oturum)
- Plugin kurulum ölçütü → README "Yeni plugin kurmadan önce" (skillspector adımından sonra). `hooks.json` event + matcher ve enjekte edilen metnin boyutu okunur. SessionStart matcher'ında `clear|compact` varsa enjeksiyon her /clear ve compaction'da yeniden ödenir; SubagentStart her subagent'te ödenir; PreToolUse/PostToolUse `*` her araç çağrısında süreç açar. Kanıt: ponytail ≤1.7k token × (startup|resume|clear|compact + her subagent) · stop-that-shit araç çağrısı başına 2 node süreci · superpowers ~880 token/clear (kaynak-tarama 1). (a + b)
- Kalıcı hafıza zehirlenmesi → ~/.claude/CLAUDE.md dalga.md satırı: web ya da subagent çıktısı dalga.md ve MEMORY.md'ye aynen kopyalanmaz. anthropic.com/engineering/how-we-contain-claude: "An injection that lands in any of these is reloaded each time the agent starts." dalga-durum hook'u dalga.md'yi her compaction'da geri basar; auto memory ve kök CLAUDE.md compaction'da diskten yeniden enjekte edilir (context-window.md). (e)
- Tarama erişimi → sonraki KAYNAK-TARAMA tarifleri:
  - GitHub yıldız zaman damgası kapalı (REST `stargazers` star+json 404, GraphQL `STARRED_AT` boş).
  - Wayback CDX Jina'da 403, available API doğrudan 429.
  - reddit.com ve x.com cookie'siz 403; Exa `web_search_exa` tarih/domain filtresi almıyor.
  - Tarif ölçütü "60 günde ≥N★" yerine "açılış ≥ tarih + ★" olur; Reddit/X için cookie izni ya da kaynak değişikliği tarifte önceden kararlaştırılır. (a, c, d)

## 3. Elenen
ELENDİ 27 (a 15 · b 7 · c 3 · e 2). En sık sebep: kurulu araç ya da CLAUDE.md kuralıyla çift, 16 kalem (graphify, RTK, auto memory, /cost + /usage, dalga.md, "En basit çözüm" ve "Cerrahi değişiklik" satırları). Sonra konu dışı/yanlış pozitif 7, kaynak doğrulanamadı 2, ölçümde kötü 1, Claude Code yerine ayrı yığın 1.

## 4. Sorgulamada düşürülen / değişen
- tigerless-labs/agent-memory ADAY→ELENDİ. README'de "Deterministic `MEMORY.md` injection at session start" (auto memory ile aynı mekanizma), "SessionStart injects, Stop and SessionEnd distil" ve "judgement is borrowed from the host agent's own CLI" geçiyor; yani tur sonunda `claude -p` kotası harcanabilir (sıklık doğrulanamadı). Python 3.12+ + uv gerekiyor, native Windows yok. Rapordaki açılış 2026-08 → 2026-09-01, açık issue 21 → 5.
- lennney/stop-that-shit ADAY→ELENDİ. `hooks/hooks.json` SessionStart(*), UserPromptSubmit, PreToolUse(*), PostToolUse(*) ve SessionEnd tanımlıyor; araç çağrısı başına 2 node süreci açılır. Açıklama "面向 Codex/GPT 场景" (Codex/GPT odaklı), kural "Cerrahi değişiklik" ile çift.
- DietrichGebert/ponytail ADAY→ELENDİ. "UserPromptSubmit her turda kural setini enjekte eder" iddiası Claude Code için yanlış; bu yalnız Qoder'da oluyor (`ponytail-mode-tracker.js`). Gerçek maliyet: SessionStart `startup|resume|clear|compact` ve SubagentStart'ta ≤6637 baytlık SKILL.md (≈≤1.7k token). Kural "En basit çözüm" satırıyla aynı. Açık issue 274 → 95 (PR'lar dahil sayılmıştı).
- YouTube BİLGİ ×2 → ELENDİ. Theo altyazısında denetim kalıbı yok, "for coding, I don't want a memory" görüşü var; MEMORY.md 62 token. Sharbel'in token denetimi /context + /skill-doctor + skill-kapatma.md ölçümüyle çift.
- Anthropic BİLGİ ×4 → ZATEN VAR / ELENDİ. 2.1.273, 2.1.260 ve 2.1.266–267 kurulu 2.1.274'te var; 2.1.251 kaynak-tarama 99-sentez §4'te işlenmişti; 2.1.269 (attribution) konu dışı.
- Reddit: rapor 29 → 24 satır. myc için "ADAY*" ve "ADAY DEĞİL" çelişkisi → ELENDİ. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` "doğrulanmadı" → env-vars.md ile doğrulandı. anthropics/claude-code#24147 BİLGİ → ZATEN VAR (açık issue doğrulandı; CLAUDE.md bugün 1248 token ölçüldü).
- X: 403 bloğu ana oturumda doğrulandı, tablo ayırıcısı düzeltildi.
- GitHub'da ölçülemeyen 4 repo: thedotmack/claude-mem 94.1k · gastownhall/beads 27.2k · OthmanAdi/planning-with-files 26.9k · DeusData/codebase-memory-mcp 43.6k. Wayback devam turunda tavan doldu (20/20) → etiket yok. Sonraki turda önce beads denenir (Mart 2026'dan snapshot var).
