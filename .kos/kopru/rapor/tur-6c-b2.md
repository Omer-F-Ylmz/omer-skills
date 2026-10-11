# TUR-6c-B2 rapor (2026-10-11) — onay betiği hazır, canlıya YAZILMADI (Ömer koşar)

- Betik: `.kos/kopru/onay/tur_6c_b_kur.py` (uygula / --kuru / --geri); yedek `.kos/kopru/onay/yedek-6c-b/<dosya>.<damga>`.
- Skill: 17 depodan 1008 yeni SKILL.md (var olan ada dokunmaz) → ~/.claude/skills, skillOverrides name-only (ilk istemde yalnız ad).
- Plugin: 3 marketplace+install (hermoso, cybersecurity-skills 818, agent-browser; hook/MCP yok), 824 skill name-only. claude-ads + azure ×6 zaten etkin.
- Hook'lu plugin'ler (tdd-guard `npx` her istemde, gsd-core, superpowers-zh SessionStart) enable EDİLMEDİ — ilk istem + RAM şişirir; skill'leri gevşek kopya name-only geliyor. Ömer isterse PLUGINLER'e eklenir.
- MCP paylaşımlı (47800 proxy, sunucular.json + ~/.claude.json http): qmd 2.8.3 (tek kullanıcı indeksi, durumsuz sayıldı).
- MCP stdio (deferred, ENABLE_TOOL_SEARCH açık): premiere-pro 1.2.8 (MIT), infinite-canvas/canvas-agent 0.6.0 (repo MIT; npm paketi lisans alanı boş) — yerel node, C:\AI\mcp\<ad>, `--ignore-scripts`.
- CLI: B1'de kurulu 7 (cloudflared, gws, inspector, qmd, bun, ollama, agentshield) — yeni CLI yok.
- --kuru 1. koşu: proxy 47899 açılmadı — kök neden qmd yolu (npm -g kökü APPDATA değil node dizini); düzeltildi, `qmd mcp` initialize OK. 2. koşu: MCP duman 3/3 (premiere-pro 5 araç, infinite-canvas 34, qmd stdio 4 = http 4), skill 1008 kopya OK, canlı AYNI, 47899 kapandı.
- Canlı kanıt: settings/mcpServers/skills sha256 önce=sonra (06df589e… / 2288e524… / 0e275e17…), mcp_var_mi 36 ad aynı; canlı proxy 18136 dokunulmadı; geçici bekçi durduruldu.
- claude.ai: dist/yukle-13/_paket 98 zip — skill_denetim 0 hata, duman_claudeai 0 sorunlu (Desktop yükler).
- Hesap: docs/kurulumlar/hesap-gereken.md 59 öncelikli + 29 yeni servis (plan 184 "hesap bekliyor"); değer yazılmadı.
- Ölçüm: profiller.json `b2sonra` (tam + --add-dir/--mcp-config/--plugin-dir, ağaç `B2_OLCUM=1 --kuru` ile .claude/b2-olcum) — koşulmadı (tur bütçesi); ilk istem/RAM kanıtı KALİTE-1 başında `kosucu.py --profil tam,b2sonra --gorev G01,G06`.
- Test: test_tur_6c_b_kur.py self-check OK (sahte dizin, canlı sha256 aynı). Silinen/kapatılan yok; güvenlik ayarlarına dokunulmadı.
