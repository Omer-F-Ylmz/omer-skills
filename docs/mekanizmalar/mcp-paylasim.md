# Paylaşımlı MCP (mcp-proxy)

- **Sorun:** CC her oturumda (etkileşimli ya da `claude -p`) her stdio MCP'yi yeniden başlatır; `cmd /c npx -y pkg` zinciri sunucu başına ≈5 süreç / ≈250 MB. Tam profilli bir oturum ≈180 süreç / ≈5.3 GB.
- **Mekanizma:** `mcp-proxy` (sparfenyuk, MIT, uv tool) durumsuz stdio sunucularını bir kez başlatır ve her birini `http://127.0.0.1:47800/servers/<ad>/mcp` (streamable HTTP) adresinde yayınlar. `~/.claude.json` içindeki girdi `{"type":"http","url":...}` olur; oturum başına süreç açılmaz.
- **Kapsam:** `tools/mcp_paylasim.py` içindeki `PAYLASIM` (21 ad). Oturum başına kalanlar: tarayıcılar (playwright, puppeteer), roots/cwd'ye bağlı olanlar (mcp-filesystem, mcp-git), editör köprüleri (blender, unity, godot), codebase-memory-mcp ve eklenti MCP'leri (plugin `.mcp.json`; kullanıcı yapılandırmasından değiştirilemez).
- **npx → node:** oturum başına kalanlardan godot ve unity `C:\AI\mcp\<ad>` yerel kopyasıyla doğrudan node'dan koşar (aynı sürüm).
- **Güvence:** her ad için stdio `tools/list` ile http `tools/list` karşılaştırılır; eşit değilse o ad çevrilmez. Ad kümesi önce ve sonra aynı kalır.
- **Açılış:** Startup klasöründeki `omer-mcp-paylasim.vbs` gizli pencerede başlatır. Proxy kapalıyken açılan oturumda bu 21 MCP "failed" görünür; proxy açılınca yeni oturumda düzelir.
- **Risk:** paylaşılan sunucuların belleği tek bir proxy sürecinde toplanır (≈4 GB). Proxy düşerse 21 MCP birlikte düşer. Ortam değişkenleri `~/.claude/mcp-paylasim/sunucular.json` dosyasında durur (repo dışında, ~/.claude.json ile aynı ACL).
