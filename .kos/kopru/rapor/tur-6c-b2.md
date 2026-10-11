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

## B2-devam (2026-10-11 08:10) — ölç → aile paketi onarımı; canlıya YAZILMADI

| kol | görev | ilk istem bağlamı | kalite | isabet | USD | süre |
|---|---|---|---|---|---|---|
| tam (taban, t7c 11 Eki ×2) | G01 | 85.3k | 8 / 10 | 1 / 1 | 0.70 / 0.59 | 45 / 38 sn |
| tam (taban, t7b ×2) | G06 | 85.4k (cc) | 10 / 10 | 0 / 0 | 0.72 / 0.72 | 46 / 44 sn |
| b2sonra (1008 gevşek + 824 plugin, name-only) | G01 ×1 | **127.3k (+42k)** | 10 | 1 | 1.04 | 74 sn |
| b2aile (96 aile, açıklamalı) | G01 ×2 + G06 ×1 | ölçüm sürüyor → `docs/kutuphane/olcum/2026-10-11-b2d*-b2aile.tsv` | | | | |

- Onarım: onay betiği artık 1832 adı değil, claude.ai ile aynı 96 aile paketini (`dist/yukle-13/_paket`, 1892 alt skill, B1-devam denetimli) `~/.claude/skills/<aile>`'ye açar; açıklama = konu + alt skill adları (≤90 kr, tetikleme anahtar kelimesi), kaba tahmin ≈2.2k jeton. cybersecurity-skills (818) plugin olarak değil mukul975-* aile paketleri olarak gelir (kapatma yok, kurulmamıştı); hermoso + agent-browser plugin (6 ad, name-only). Self-check güncel: OK.
- Bütçe: b2sonra G01 ×1 (×2 değil) — +42k ilk koşuda kesin; $4 tavanı onarım ölçümüne ayrıldı. Harcanan ≈$1.04 + b2aile ≈$2.2.
- Hook maliyeti (enable edilmedi, geçici cwd, soğuk/sıcak): tdd-guard `npx tdd-guard@latest` her istemde 14.1 / 3.5 sn, her Write/Edit'te 25.5 / 13.1 sn (npm kayıt sorgusu) → öneri: yalnız test projesinde proje-scope enable + `@latest` yerine pinli yerel kurulum. gsd-core 12 hook node, her biri 0.06–0.16 sn (Write başına 4 hook ≈0.35 sn), çıktı 0 → düşük maliyet, matcher olduğu gibi kabul edilebilir. superpowers-zh SessionStart 0.25 sn ama her oturuma ≈0.8k jeton enjekte → öneri: enable etme (skill'leri aile paketiyle zaten geliyor). Karar Ömer'de.
- Onay (b2aile ölçümü ≤ taban + 3k ve kalite ≥ taban çıkarsa): `python C:\Projeler\omer-skills\.kos\kopru\onay\tur_6c_b_kur.py` — önce `--kuru` (sha256 + mcp_var_mi önce=sonra).
- Kalanlar: b2aile sonuçları tabloya; bağlam aşarsa AILE_ACIK düşür (90→60) ya da küçük aileleri birleştir; `--kuru` 3. koşu (aile kipi) sha256 kanıtı.
