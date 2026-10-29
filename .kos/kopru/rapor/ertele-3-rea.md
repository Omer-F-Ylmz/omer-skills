---
type: rapor
status: ara-kayit
tags: [ertele-3, rea, skill-listing, agent-listing, mcp-instructions]
relatedTo: [ertele-2-rea, ertele-3]
---
# ERTELE-3 TUR 3 — claude.exe 2.1.311 kod kanıtı (tmp/ertele8/sl.txt, xyn.txt, mcp.txt, lnn.txt; bayt regex, yama yok)
1. Ekler tek yerde toplanır (@257923770): `ou("agent_listing_delta",()=>bwe(n,L))`, `ou("mcp_instructions_delta",()=>q9e(...))`, `ou("skill_listing",()=>xYn(ve,L))`.
2. Skill listesi `jwr` (@257973633): `if(L_())return[]` (L_ = launchOptions.disableSlashCommands) ve `if(!e.options.tools.some(we=>xt(we,vo)))return[]` → araç listesinde Skill aracı yoksa liste HİÇ gönderilmez. Ayar düzeyi karşılık: `permissions.deny:["Skill"]` (araç listeden düşer). Başka belgelenmemiş anahtar yok; `disableModelInvocation` olanlar listeden süzülür (dosya frontmatter'ı, plugin cache'te ezilir).
3. Kesme `Pnn` (@256944803): bütçe `skillListingBudgetFraction`/`SLASH_COMMAND_TOOL_CHAR_BUDGET`; aşınca açıklama → yalnız ad (bundled sabit), adlar hiç düşmez (`tengu_skill_descriptions_truncated`). Delta: ad+digest önceki eklerde varsa yeniden gönderilmez.
4. Ajan listesi `bwe` (@257947931): yalnız Agent aracı varsa; `activeAgents` ∩ izinli; deny edilen tip listeden düşer (TUR 2 kanıtı). Özel ajan için ad-yalnız/bütçe yok.
5. MCP talimatı `q9e`→`Jbe`/`Lnn` (@257949289): bağlı sunucuların `instructions` alanı delta olarak; bütçe/kesme/ayar yok. ENABLE_TOOL_SEARCH yalnız araç ŞEMASINI erteler, talimatı değil → ertelemenin tek yolu sunucuyu açılışta bağlamamak (kural: kapatma sayılır, uygulanmadı).
