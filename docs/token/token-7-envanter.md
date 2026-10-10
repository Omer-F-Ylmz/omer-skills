# TOKEN-7 envanter (10 Eki 2026, TOKEN-7a)

Son durum yalnız üç değerden biri: **çalışıyor** = kurulu-çalışıyor · **7b** = 7b ölçümü bekliyor · **onarım** = onarım bekliyor (sebep + sonraki adım). RED satırları yalnız listelenir.

| ad | tür | son durum | mekanizma | kötü yan | iyileştirme / sonraki adım | ölçüm |
|---|---|---|---|---|---|---|
| RTK (Bash+PowerShell hook) | CLI+hook | çalışıyor | `rtk hook claude` komutu `rtk <cmd>` biçimine çevirir, çıktı süzülür | dotnet test, npm test, `dotnet --info` yazılmıyor; `rtk dotnet --info` tasarrufsuz (2275→2275 kr) | 7a: proje filtresi onarıldı (trust + verify 1/1) | git status 5253→4980 kr |
| rtk-onisle (tools/rtk_onisle.py) | hook | onarım | rtk'nın yazmadığı aileleri (git/dotnet/npm/pytest/node --test; Bash'te grep/ls/wc) çevirir, rtk yazıyorsa susar | — | settings.json yazımı oto-mod tarafından engellendi; uygulama komutu raporda | 7b: kazanç/oturum |
| Headroom Desktop vekili | uygulama+ayar | çalışıyor | ANTHROPIC_BASE_URL üstünden istek sıkıştırma | alt süreçte araçları gizleyebilir | guard kancası izliyor | token-6b'de yapıldı |
| Headroom CLI | CLI | çalışıyor | uv tool; proxy/wrap | python3 shim'e bağlı | — | gerekmez |
| Headroom MCP | MCP | 7b | headroom_compress/retrieve | şema bağlam yükü | deferred kalır | araç şeması token |
| Headroom output_shaper | ayar | RED | — | — | token-6d: tasarruf gürültü bandında | — |
| graphify | CLI+skill | 7b | AST bilgi grafı query/path/explain | graf eskir (update gerekir) | codebase-memory-mcp ile kıyas | sorgu isabeti/token |
| claude-mem | plugin+MCP | çalışıyor | gözlem enjeksiyonu + arama | observer önbellek yaması sürümde silinir | her güncellemede cmem_yama.py | gözlem id durgunluğu |
| context-mode | plugin+MCP+hook | 7b | ctx_* sandbox, ham çıktı bağlama girmez | ipucu tekrarı + MCP talimatı ~5k | CONTEXT_MODE_* ile ipucu kısma | A/B bağlam |
| caveman proxy | CLI (BSL-1.1) | çalışıyor | 127.0.0.1:8787 vekil | Headroom portuyla çakışır | 7a: yetim PID 41352 zaten yok, 8787 LISTEN yok; bayat run json `.kos/caveman-yedek-7a/` | — |
| caveman compress/shrink/convert | CLI | 7b | skill gövdesini sıkıştırır | okunabilirlik düşer | önce kopyada | önce/sonra token+kalite |
| cavecrew | skill (MIT) | 7b | terse alt ajan skill'leri | kalite riski | name-only kurulum, A/B ile | A/B |
| caveman otobaşlat | hook | 7b | oturumda caveman kipi | çıktı üslubu kısalır | kalite A/B | rubrik |
| ponytail | plugin | çalışıyor | kod yazımı merdiveni | kapatınca %4,8 | dokunma (token-6e) | yapıldı |
| markitdown | CLI+MCP | çalışıyor | belge→Markdown | büyük belgede büyük çıktı | sayfa aralığı | gerekmez |
| strategic-compact | skill (ecc) | çalışıyor | mantıksal noktada /compact önerir | — | ecc:strategic-compact kurulu | gerekmez |
| Task Observer | skill (Desktop) | çalışıyor | oturum gözlemi | claude-mem ile örtüşür | anthropic-skills:task-observer kurulu | gerekmez |
| codebase-memory-mcp v0.11.0 | MCP (MIT) | onarım | tree-sitter kod grafı, tek exe | graphify ile örtüşür | indirildi `C:\AI\mcp\codebase-memory-mcp\bin`, sha256 OK, Defender temiz; exe çalıştırma + `claude mcp add` oto-mod engeli → Ömer onayı | 7b: graphify kıyası |
| claude-usage 1.5.5 | CLI | çalışıyor | yerel jsonl'den kullanım özeti | scan gerektirir | 7a: köprü allowlist (today/week/stats/--version) | olcum-araclari.md |
| codeburn | CLI | 7b | proje/model bazlı maliyet dökümü | telemetri doğrulanmadı | claude-usage yetmezse | — |
| OmniRoute / model yönlendirme | vekil+ayar | 7b | sağlayıcı/model yönlendirme | Headroom vekiliyle zincir | 7c'de | USD/kalite |
| MAX_THINKING_TOKENS | ayar | 7b | düşünme bütçesi tavanı | zor işte kalite | A/B | rubrik+USD |
| skill listesi bütçesi | ayar | çalışıyor | skillListingBudgetFraction 0.02 + name-only override | açıklaması düşen skill tetiklenmeyebilir | 40000 A/B (KALİTE-1) | bağlam+tetik isabeti |
| SLASH_COMMAND_TOOL_CHAR_BUDGET | ayar | 7b | 75000 kr | eski ad | yeni anahtarla çakışma ölçümü | bağlam |
| ajan gizleme | ayar | çalışıyor | 141 Agent(...) deny | gizli ajan çağrılamaz | KÜTÜPHANE-5 | yapıldı (−33%) |
| ENABLE_TOOL_SEARCH | ayar | çalışıyor | araç şemaları deferred | ek ToolSearch turu | — | gerekmez |
| promptCacheTtl 1h | ayar | çalışıyor | 1 saat önbellek | yazma ×2 | token-6b | yapıldı |
| SUBAGENT_MODEL + FORCE | ayar | 7b | alt ajan modelini zorlar | tanımdaki model ezilir | 7b ölçer | USD/kalite |
| ajan model satırları (sonnet→claude-sonnet-5-5) | ayar | onarım | 4 repo ajanında model satırı | `.claude/agents` yazımı oto-mod engeli | komut raporda | — |
| output style Concise | ayar | çalışıyor | kısa yanıt | ayrıntı azalabilir | — | gerekmez |
| autocompact pct override | ayar | 7b | erken compact | bağlam kaybı | A/B | rubrik |
| CLAUDE.md boyutu | ayar | çalışıyor | global 3276 B + repo 1203 B | her tura girer | 1.3k tavanı korunur | gerekmez |
| MCP node girişi (5 npx sunucusu) | ayar | çalışıyor | `cmd /c npx` yerine `node giriş.js` | Desktop'ta brave/stitch anahtarı `cmd` ortamından alıyor | CC 5/5 node; Desktop 3/5 node (brave/stitch npx kaldı: node girişte anahtar yok → env bloğuna anahtar adı, onarım) | kurutest |
| proje profilleri | ayar | 7b | proje düzeyi plugin kapatma | blender kalite −2 | iş türüne göre | rubrik |
| kredi-token takibi · balance API · yüksek context model · security-guidance/superpowers/ECC claude-mem yinelemesi | kural/plugin | RED | — | — | — | — |

## Bekleyen token kuralları (3d kararı)
| kural | karar |
|---|---|
| kural-15-20-mesajda-yeni-sohbete-gec | CLAUDE.md'de var ("/clear mandatory at dalga start") — ek yok |
| kural-compact-clear-karar-kurali | CLAUDE.md'de var ("/compact recommended within") — ek yok |
| kural-max-thinking-tokens-ayari | 7b listesine (A/B: rubrik + USD) |
| kural-en-fazla-10-skill | 7b listesine (skill bütçesi A/B ile birlikte) |
| kural-skill-context-degisikligini-tek-skaler-s | CLAUDE.md'de kısmi ("Verification proportional"); 7b yöntemi zaten tek skaler (bağlam/USD) — ek yok |
| kural-kredi-token-ayrimini-takip-etme · kural-token-kullanim-takibi-balance-api-usage · kural-yuksek-context-limitli-model-secme | RED (28 Eyl) — dokunulmadı |
