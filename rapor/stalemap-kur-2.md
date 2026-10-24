# STALEMAP-KUR-2
- gitleaks 5 bulgu: hepsi bench/heldout-v3|v4/tasks/*/hidden/*.test.ts (test fixture sahte sır) → temiz. npm: integrity sha512-bFqie0R1wmidOc4FOE6tKGoIR8ZyEclZyxmpTiXaFA8gt8SGpKxXyD8S8hjKN+dRNE81eV+WVkkdsVmhDKbfqw==, maintainer umairjz <umairejaz.ch@gmail.com>.
- Plugin hook'ları --strict-mcp-config altında yükleniyor: stream-json'da SessionStart:startup hook_response stalemap bloğu döndü (omer-site, 5 sn).
- mcp_profil.py: JS/TS desenine `stalemap` eklendi + tanım (npx -y stalemap@0.4.1 mcp). tools/test_mcp_profil_stalemap.py: kırmızı (1F+1E) → yeşil 3/3.
- `claude -p "echo ok"` 60 sn İÇİNDE DÖNMÜYOR (90 sn timeout): enabledPlugins kullanıcı ayarında açıkken asılıyor, --strict-mcp-config tek başına yetmiyor; --setting-sources project ile 4,7 sn. Stalemap'i --settings ile kapatmak da düzeltmedi (80 sn) → neden stalemap değil, başka eklenti/ayar; kök neden ÇÖZÜLMEDİ (BASE-KUR-1 ile aynı bulgu).
- Önizleme omer-site (sync yok): 8 dosya, lenis 1.3.23→1.3.27, three 0.184→0.186.1; 2,0 sn. post-edit hook (Python projesi, omer-skills): ~2,0-2,5 sn/çağrı (npx ek yükü), exit 0, çıktı yok.
- Katalog: .kos/kopru/skill-mode/yetenek-tam.jsonl'a stalemap eklendi.
- Desktop MCP JSON (config'e dokunulmadı): {"stalemap":{"command":"C:\Program Files\nodejs\npx.cmd","args":["-y","stalemap@0.4.1","mcp"]}}
- Sapma: post-edit 2 sn/Edit pahalı; npx yerine sabit node yolu denenmedi.
