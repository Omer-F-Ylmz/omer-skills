# MCP sunucularını doğrudan başlatma (RAM-1)

**Neden:** `npx -y` / `uvx` / `uv run` / `dotnet dnx` / `cmd /c` zincirleri her oturumda sunucu başına 2-4 aracı süreç
tutuyordu; `npx -y` ve `@latest` açılışta sürüm de çözümlüyordu. Ölçüm (docs/ram/olcum.md, yeni boşta CC oturumu):
83 → 59 süreç · çalışma kümesi 2,94 → 2,19 GB · özel 4,03 → 3,16 GB · `claude mcp list` 14,9 → 10,8 sn.
Sunucu, sürüm ve araç seti aynı: docs/ram/envanter-once.json = envanter-sonra.json (31 sunucu, CC + Desktop).

**Nasıl:** config `command` = node.exe ya da araç exe'sinin mutlak yolu, `args` = giriş dosyası + eski argümanlar.

| Kurulum | Yer | Sunucular |
|---|---|---|
| npm (package-lock, `--ignore-scripts`) | `C:\AI\mcp\<ad>\` | mcp-sequential-thinking 0.6.2 · mcp-memory · mcp-filesystem 2026.8.31 · stitch 0.9.0 · brave-search 2.1.4 · playwright (Desktop) 0.0.83 |
| `uv tool install` | `~\.local\bin\<exe>` | mcp-fetch · mcp-git · mcp-time 2026.8.18 · code-review 2.0.0 |
| `dotnet tool --tool-path` | `C:\AI\mcp\binlog\binlog-mcp.exe` | binlog (Desktop) 3.0.3 |
| mevcut .venv | `C:\blender_mcp\mcp\.venv\Scripts\blender-mcp.exe` | blender (yollar `__file__`'a göreli, cwd bağımsız) |

- mcp-memory grafı: `MEMORY_FILE_PATH=C:\AI\mcp\mcp-memory\memory.jsonl` (CC ve Desktop aynı yol; paket güncellemesi
  silmez). Eski varsayılan yol (`_npx\...\dist\memory.jsonl`) diskte yoktu; read_graph 0/0 → 0/0.
- API anahtarları: CC'de `${VAR}` düzeni aynen. Desktop env'i beyaz listeyle verir (`mcp_kurutest.DESKTOP_ENV`) ve
  `${VAR}` genişletmez → anahtarlı Desktop sunucuları .cmd ile registry'den okumaya devam eder.

**cmd /c kalanlar (zorunlu):** puppeteer (paket cwd'ye göreli günlük yazar → `cd %TEMP%`) · Desktop brave-search, stitch
(anahtar, yukarıda) · Desktop mcp-filesystem, mcp-git (gecit.mjs kanca geçidi) · Desktop obsidian, cc-kopru,
claude-design (cwd). Bu .cmd'lerin iç satırı da artık npx/uvx/global shim yerine node.exe + `C:\AI\mcp` girişi.
Plugin'lerin kendi .mcp.json'ları (nano-banana, playwright, dotnet binlog) değiştirilmedi.

**Kalan, config'le kalkmayan:** her stdio sunucusuna ayrı conhost (CC başlatma biçimi) · uv tool exe'sinde trampolin +
venv python · node.exe yolu WinGet Node sürümüne bağlı (`node-v24.19.0`); Node yükselince
`python tools/mcp_guncelle.py node-yolu` (WinGet Links'te node.exe yok; en yeni `node-v*` klasörünü bulur, CC + Desktop +
.cmd yollarını çevirir, envanteri karşılaştırır).

**Güncelleme:** `python tools/mcp_guncelle.py <ad> <sürüm>` — sabit sürüm ister (latest/^/~ red, exit 2), kurar, kurulu
sürümü doğrular, araç setini önce/sonra karşılaştırır (fark → exit 1). Config yolu sürümden bağımsız, değişmez.
Envanter: `python tools/mcp_envanter.py al <çıktı.json>` · `karsilastir A B` · `graf` · `olc <etiket>`.

**Geri alma (tek komut):** `python tools/mcp_guncelle.py geri-al` — `~\.claude.json.bak-ram1` sunucularını
`claude mcp remove/add-json` ile, Desktop config'i `<config>.bak-ram1`'den, .cmd'leri `C:\AI\mcp\mcp-launch.bak-ram1\`
yedeğinden geri yazar. Sonra CC oturumunu ve Desktop'u yeniden başlat.
