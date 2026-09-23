---
iddia: Headroom settings.json env (ANTHROPIC_BASE_URL + ENABLE_TOOL_SEARCH=true) ile bağlı kalır; wrap ek kazanç getirmez, okuma görevlerinde girdi −%37.
kaynak: headroom doctor --port 6767 (v0.37.0), headroom wrap claude --help, headroom kaynağı (providers/claude/runtime.py _HEADROOM_ENV_KEYS)
guven: orta
dogrulama: docs/denemeler/headroom-ayar-sonuc.md (20b1: 4 görev × 3 kol × 2, $8.79)
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: token, headroom, proxy, olcum
---
Headroom settings.json env (ANTHROPIC_BASE_URL + ENABLE_TOOL_SEARCH=true) ile bağlı kalır; wrap ek kazanç getirmez, okuma görevlerinde girdi −%37.
- doctor uyarısı: özel ANTHROPIC_BASE_URL araç aramasını (#746) ve 1M pencereyi (#1158) kapatır. #746 global ENABLE_TOOL_SEARCH=true ile zaten kapalı değil: proxy.log'da istek başı tool_search_deferral görülüyor.
- wrap istemciye yalnız ANTHROPIC_BASE_URL + ENABLE_TOOL_SEARCH geçirir; varsayılan wrap ayrıca 8787'de ikinci vekil + MCP/Serena kaydı yapar (kalıcı yan etki). --1m = ANTHROPIC_MODEL opus[1m], yalnız opus 1M için.
- ölçüm (sonnet, sıcak $): doğrudan 375977 girdi / $0.415 · headroom-mevcut 235328 / $0.354 (başarı 1.00) · headroom-wrap (aynı env) 225586 / $0.296 (başarı 0.88). mevcut↔wrap farkı aynı ayarın gürültüsü.
- istek başı bağlam doğrudan ~107–125k, headroom ~96–100k; kalan fark tur sayısı.
- not: 20a'daki +%29 tek görevde Headroom 2. koşunun 5 tur atmasıydı (istek başı bağlam yine −%9); tek görevden genelleme yanıltıcı.
