---
type: rapor
status: ara-kayit
tags: [ertele-2, rea, toolsearch, skill-listing, agent-listing]
relatedTo: [ertele-2, ertele-1]
---
# ERTELE-2 TUR 4 — claude.exe tersine okuma (kanıt tmp/ertele5/kod2-9.txt, idler.txt, bin20.txt)
Yöntem: REA MCP bağlıydı ama 298 MB Bun tek-dosya JS gömülü; doğrudan bayt regex (rx.py/kod.py) daha ucuz ve yeterli. Binary yamalanmadı.

1. ToolSearch erteleme yalnız ARAÇ şeması içindir: `isDeferredToolByEngine`, `isToolSearchEnabled`, `ENABLE_TOOL_SEARCH=auto:N` (`auto_above_threshold`), `DeferredToolPlaceholder`. Skill ve ajan listesi araç değil, sistem-reminder EKİ (attachment) — bu motora girmiyor; skill/ajan için `ENABLE_TOOL_SEARCH` benzeri ayar/env binary'de YOK (`agentListing*` dizgesi 0, `skillListing*` yalnız BudgetFraction/MaxDescChars).
2. Skill listesi `jwr` (xYn): `skill_listing` eki; `disableModelInvocation` olanlar listeden düşer; bütçe aşılınca `Pnn` açıklamaları kırpar, adlar kalır. Ekler delta: yalnız yeni/değişen skill sonraki turda gönderilir (digest).
3. Skill aracı doğrulaması `oGe`: `PTe(e)==="user-invocable-only" && !userTypedThisTurn` → RED (errorCode 7). Yani ERTELE-2 F/F2/G/H adaylarındaki 3151 `user-invocable-only` skill Skill aracından ÇAĞRILAMAZ — kural ihlali; bu adaylar geçersiz.
4. ToolSearch'ün skill karşılığı zaten var: `name-only` (listede yalnız ad, gövde Skill çağrısında yüklenir, Skill aracı + /ad çalışır). Plugin skill'i (`source==="plugin"`) override'ı yalnız synced eşlemeden alır; ama bütçe aşımında açıklamaları zaten kırpılıyor → ~30k plugin skill ADI tabanı kaldırmasız düşmez.
5. Ajan listesi `bwe` → `agent_listing_delta` eki, satır `$Fr`: `- tip: (lean? whenToUseLean : whenToUse) (Tools: …)`. `whenToUseLean` yalnız yerleşik ajanlarda (Explore vb.); özel/plugin ajan için ad-yalnız modu ya da bütçe YOK. Ölçüm: plugin cache'te 765 ajan dosyası, description 237k kr + tools 25k kr; ~/.claude/agents boş, proje 12 ajan 1,9k kr.
6. Sonuç: skill/ajan için resmi "erteleme" anahtarı yok. Kaldırmasız en yakın yol: (a) user+sync skill'lerinde `user-invocable-only` yerine `name-only` (çağrılabilir kalır); (b) ajan açıklamasını kaynakta tek satıra indirip uzun metni ajan gövdesine taşımak — plugin ajanlarında cache güncellemede ezilir, kalıcı değil.
