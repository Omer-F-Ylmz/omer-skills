# DaWTq7aKSKq · kayvon.ai · reel · https://www.instagram.com/reel/DaWTq7aKSKq/

## Özet
Claude'a "sonsuz hafıza": NotebookLM defteri + notebooklm MCP/CLI bağlantısı, oturum sonu wrap-up skill'i deftere yazar, CLAUDE.md kuralı önce deftere sordurur.

## Kalemler
| ad | tür | link | karar | ölçütler (bakım · çift · izin · context) | gerekçe |
|---|---|---|---|---|---|
| NotebookLM (Gemini Notebook) | site/servis | https://notebooklm.google.com | KUR | site canlı · önceki-karar:sirali.tsv:teknik (118) · hesap token'ı (Google) · - | Hesap isteyen servis; notebooklm-py'nin arka ucu. |
| notebooklm-mcp | MCP | https://github.com/PleasePrompto/notebooklm-mcp | RED | ★3436 push:2026-09-10 arşiv:e · yok · tarayıcı, hesap · araçlar her oturum | Arşivlenmiş; yerine notebooklm-py. |
| notebooklm-skill | skill | https://github.com/PleasePrompto/notebooklm-skill | RED | ★7777 push:2026-09-10 arşiv:e · kurulu:phoenix-docs-research/notebooklm (aynı tarayıcı otomasyonu) · tarayıcı, shell, hesap · çağrılınca | Arşiv + bizde eşdeğeri kurulu. |
| notebooklm-py | CLI/Python API + skill | https://github.com/teng-lin/notebooklm-py | KUR | ★19708 push:2026-10-13 arşiv:h · kısmen:phoenix-docs-research/notebooklm · ağ, shell, hesap token'ı · SKILL.md ~2100 kelime, çağrılınca | MIT, aktif; bizdeki tarayıcı otomasyonu yalnız sorguluyor, bu API ile defter/kaynak da yazıyor (wrap-up akışı için şart). |
| wrap-up skill + CLAUDE.md yönlendirme | teknik | - | ÖĞREN | - · kısmen:claude-mem@thedotmack + MEMORY.md · dosya yazma, ağ · - | Ders: oturum geçmişini aranabilir harici depoya yaz, CLAUDE.md'de "önce depoya sor" kuralı koy; bizde claude-mem yerelde yapıyor. |
