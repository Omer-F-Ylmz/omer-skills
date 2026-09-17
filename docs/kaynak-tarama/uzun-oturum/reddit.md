# Uzun oturum tarama — Reddit · 2026-09-17
DUR: 20 gönderilik "son 30 gün + doğrulanmış oy" listesi üretilemedi, tahminle sıralama yapılmadı.
- Erişim: reddit.com düz curl ve Jina (`old.reddit.com/.../top/?t=month`) 403 "blocked due to a network policy" (ana oturumda da doğrulandı); 5 redlib/libreddit aynası 429/410/404/timeout.
- Exa fallback: `startPublishedDate/endPublishedDate` ve `startCrawlDate/endCrawlDate` 5 sorguda uygulanmadı; dönen sonuçlar 2025-12 → 2026-06, pencerede (2026-08-18 → 09-17) doğrulanabilir gönderi 0; oy sayıları kaynak sayfa 403 olduğu için doğrulanamadı.
- Tavan: Exa 10/10 · curl+Jina 10/10 · gh 0/30.
- İlerleme yolu (kullanıcı kararı): cookie/giriş izni, başka veri kaynağı (Arctic Shift/Pushshift benzeri, resmi Reddit API anahtarı) ya da pencere/oy doğrulama ölçütünün gevşetilmesi.

Pencere dışı rastlananlar (oy doğrulanamadı, yalnız referans):
- 2026-05-30 r/ClaudeCode "compacting strategy": tmux tabanlı proaktif compaction (adı yok)
- 2026-04-09 r/ClaudeCode: `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`
- 2026-02-13 r/ClaudeAI: hook + subagent ile otomatik context yönetimi ("Controlled Lane")
- 2026-01-29 r/ClaudeAI: Claude Cortex (MCP, oturumlardan bilgi grafı)
- 2026-04-04 r/ClaudeCode: auto memory prompt önekini bozuyor iddiası (ölçülmemiş)
- 2026-06-15 r/ClaudeCode: yerel proxy "%60 token tasarrufu" (iddia, ölçülmemiş)

| araç/ayar/teknik | durum | etiket | not |
|---|---|---|---|
| SessionStart(compact) ile yeniden enjeksiyon | ZATEN VAR | — | dalga-durum hook'u |
| handoff doc + /clear | ÇİFT | ELENDİ | dalga.md kuralı aynı rol |
| /loop ile uzun oturum | ZATEN VAR | — | yerleşik skill |
| Claude Cortex (MCP hafıza) | ÇİFT | ELENDİ | graphify + auto memory; her istekte MCP tool tanımı |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | YENİ | BİLGİ | docs/en/env-vars'ta var: yalnız eşiği düşürür, ana oturum + subagent → İŞ 1 autocompact kararı |
| myc (PreCompact hook hafıza, dev.to 2026-09-15) | YENİ | ELENDİ | kaynak Reddit değil, repo/★/lisans doğrulanmadı |
| anthropics/claude-code#24147 (CLAUDE.md her turda cache-read, açık, 2026-02-08) | ZATEN VAR | — | global CLAUDE.md boyutu ölçülüyor (bugün 1248 token); Reddit değil |
