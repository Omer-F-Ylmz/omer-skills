# Uzun oturum tarama — Anthropic (changelog + docs + engineering blog) · 2026-09-17
Kapsam: changelog 2.1.235 (18 Ağu) → 2.1.274 (17 Eyl), 39 sürüm, uzun oturum/token merceğiyle (5.md genel taramasının yeniden süzümü); 8 docs sayfası (context-window, hooks, hooks-guide, model-config, memory, skills, sub-agents, costs); engineering blog 20 yazı listelendi, pencerede 1. Tavan: curl/Jina 12/30 · gh 0/30 · Exa 0/5.
| kalem (sürüm/yazı) | durum | etiket | not |
|---|---|---|---|
| 2.1.273 (15 Eyl) advisor-tool turn'leri context meter + auto-compact'ta ~2× sayılıyordu, compact yarı pencerede tetikleniyordu | ZATEN VAR | — | kurulu 2.1.274 düzeltmeyi içeriyor |
| 2.1.260 (3 Eyl) "Opus and Fable sessions now compact shortly before the 1M-token limit, and recovery compaction on very large contexts no longer times out at 10 minutes" | ZATEN VAR | — | opus[1m] otomatik; İŞ 1 967K bilgisiyle aynı |
| 2.1.266–2.1.267 (8–9 Eyl) subagent resume prompt-cache yeniden kullanım düzeltmeleri | ZATEN VAR | — | kurulu sürümde, aksiyon yok |
| 2.1.251 (28 Ağu) `CLAUDE_CODE_SUBAGENT_MODEL` varsayılan, agent `model:` ve çağrı başı model öncelikli | ZATEN VAR | — | kaynak-tarama 99-sentez.md Bölüm 4'te işlendi |
| 2.1.251 + 2.1.260 `/cost` prompt-cache satırı · 2.1.247 967K varsayılanı · 2.1.243 `promptCacheTtl`/`subagentPromptCacheTtl` | ZATEN VAR | — | 99-sentez.md / İŞ 1 |
| 2.1.257 (1 Eyl) `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` | YENİ | ELENDİ | agent tanımı ve çağrı başı `model:` değerini de ezer; kurulu varsayılan yeterli |
| 2.1.269 (11 Eyl) attribution reminder CLAUDE.md/memory kuralını ezmiyor | YENİ | ELENDİ | uzun oturum/token konusu değil |
| docs 8 sayfa | taranan | — | pencerede yeni "As of v2.1.235+" notu yok; "What survives compaction" tablosu İŞ 1'de uygulanan bilgilerle aynı |
| blog "How we contain Claude across products" (anthropic.com/engineering/how-we-contain-claude) | YENİ | BİLGİ | persistent memory poisoning; aşağıda |
## YENİ ölçütler
- CLAUDE_CODE_SUBAGENT_MODEL_FORCE: bakım=2.1.257, stabil · çift=kurulu `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` · izin=settings.json env · context=yok · uzun oturum=yok; agent tanımında `model:` olan ajanları (ör. opus tanımlı) sessizce sonnet'e çevirir → ELENDİ
- Blog, persistent memory poisoning: bakım=resmi mühendislik yazısı, ürün ayarı değil · çift=yok; dalga-durum hook'u ve auto memory tam bu kalıcılık sınıfında · izin=yok · context=yok · uzun oturum=alıntı (ana oturumda doğrulandı): "The share of agent context that persists across sessions keeps growing—this includes product memory, CLAUDE.md files, mounted workspaces, and the state directories of scheduled and long-running agents. An injection that lands in any of these is reloaded each time the agent starts." context-window.md'ye göre auto memory ve kök CLAUDE.md compaction'da diskten yeniden enjekte ediliyor, dalga.md de hook'la geri basılıyor; bu dosyalara giren enjekte metin her compaction'da geri gelir → BİLGİ, hedef ~/.claude/CLAUDE.md dalga.md satırı (web/subagent çıktısı dalga.md ve MEMORY.md'ye aynen kopyalanmaz; dalga kapanınca silme kuralı zaten kalıcılığı sınırlıyor)
