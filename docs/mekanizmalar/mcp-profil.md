# Departman → MCP profili (TOKEN-7e d, tasarım — uygulanmadı)

- **Sorun:** her oturum 37 user-scope MCP'yi (+ eklenti MCP'leri) görür. Tool search açıkken tanımlar ertelenir (sonnet, 9 stdio sunucu: +4.6k jeton ilk istem), ama ertelenmiş araç adları listesi ve seçim gürültüsü kalır; G06 (web araştırma) tam profilde de Bash'e kayıyor (0/2).
- **Amaç:** iş türüne göre yalnız ilgili MCP'ler bağlamda → seçim isabeti ↑, ilk istem ↓, oturum başı stdio süreç ↓. Kalite kuralı: hiçbir departmanda isabet/kalite düşmez.

## Profil tablosu (kaynak: departman-* SKILL.md araç sırası + envanter)

Ortak (her profilde): context-mode, claude-mem (eklenti), mcp-time.

| departman | MCP |
|---|---|
| arastirma-ogrenme | brave-search, context7, mcp-fetch, mslearn, arxiv, markitdown |
| backend-dotnet | mslearn, context7, dotnet-msbuild:binlog, mcp-git, github |
| frontend | 21st, figma, claude-design, stitch, playwright, context7 |
| test-qa | playwright, puppeteer, chrome-devtools |
| veri-db | clickhouse, drizzle-docs, supabase, airtable |
| surec-inceleme | code-review, github, mcp-git |
| surec-git-yayin | github, mcp-git, netlify, hostinger |
| surec-ajan-arac | jev, context7 |
| surec-plan | mcp-sequential-thinking |
| verimlilik | headroom, jev |
| belge | markitdown |
| guvenlik | github, mcp-git |
| 3D/oyun (departman yok) | blender, godot, unity |

Hiçbir profilde olmayanlar (yalnız tam): auth0, apify, n8n-mcp, gsc, canva, hfspace, mcp-memory, mcp-filesystem, codebase-memory-mcp, design:* eklenti bağlayıcıları.

## Uygulama yolları

1. **`claude -p` (koşucu, video, köprü ajanları):** `--strict-mcp-config --mcp-config <profil.json>` — tam küme kontrolü, kanıtlı (kur.py hafif profil, t7c G01). Profil JSON'u `~/.claude.json` + `~/.claude/mcp-paylasim/sunucular.json`'dan üretilir (env değeri repo'ya yazılmaz; geçici dosya).
2. **Etkileşimli oturum:** başlatıcı (`cc <departman>` → aynı bayraklar). Proje `.mcp.json` yalnız EKLER (user ∪ project), çıkaramaz → profil için uygun değil; yalnız projeye özgü sunucu eklemek için.
3. **Alt ajan:** `.claude/agents/<ad>.md` frontmatter `mcpServers` — ajan başına küme. Oturum ortasında yeni tanım yüklenmez (yeni oturum gerekir).
4. **Yapılmayacak:** user-scope'tan sunucu silmek/kapatmak (kural: kurulu hiçbir şey kaldırılmaz) — tam profil her zaman varsayılan kalır.

## Ölçüm planı (KALİTE-1 isabet ölçüsü)

- Düzenek: `tools/olcum/kosucu.py`; isabet = beklenen araç önekinden biri kullanıldı mı (kosucu.py `isabet`), kalite = rubrik (≤10), bağlam = ilk istem jetonu.
- Görev → departman: G01/G02 backend-dotnet · G03 frontend · G04/G08 surec-git-yayin · G05 belge · G06 arastirma-ogrenme · G07/G15 3D · G09 guvenlik · G10/G11 frontend · G12 surec-plan · G13 backend · G14 surec-plan.
- Kol: tam vs profil (görevin departman profili, 47899 geçici proxy), görev başı ×2, model sonnet. Karar: her departmanda isabet(profil) ≥ isabet(tam) ve kalite farkı ≥ −0.5; bağlam ve stdio süreç sayısı raporlanır. Tetikleme isabeti ek sütun: araçlarda `Skill:departman-*` var mı.
- Tavan: 15 görev × 2 kol × 2 = 60 `claude -p`, ≈$12 → ayrı onaylı dalga.

## Deneme (G06 ×1, 11 Eki)

`.claude/t7e_profil.py` (47899 geçici bekçi, yalnız brave-search/context7/mcp-fetch + mslearn http; strict), tam kol 2026-10-11-t7b-g06-tam:

| kol | mcp | cache_creation | bağlam | tur | USD | kalite | isabet | araç |
|---|---|---|---|---|---|---|---|---|
| tam (×2 ort.) | 56 | 85.4k | 192.6k | 2 | 0.724 | 10 | 0/2 | Bash |
| profil arastirma (×1) | 4 | 62.1k | 227.2k | 3 | 0.551 | 10 | 0/1 | Bash |

Sonuç (n=1): ilk istem −23k (−27%), USD −24%, kalite eşit; isabet değişmedi — G06'da Bash'e kayış MCP kalabalığından değil (web aracı görünür olduğunda da Bash/curl seçiliyor). İsabet için profil tek başına yetmez; araştırma yönlendirmesi (departman skill tetiklemesi) ayrı ölçülmeli. Not: ajan frontmatter `mcpServers` bu kurulumda denenmedi.
