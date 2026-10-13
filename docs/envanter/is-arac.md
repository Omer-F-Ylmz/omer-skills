# İş → araç sırası (ENVANTER-1)

Amaç: iş başlarken kurulu aracın unutulmaması. **Departmanı olan işte sıra departman-* müdüründedir; bu dosya onu tekrar etmez, yalnız eksik kalanı ekler.** Çakışmada departman-* SKILL.md kazanır. Kaynak: `envanter.tsv` (ad, nerede, son kullanım), `bosluk.md`.
Kısaltma: CC = Claude Code, AI = Desktop/claude.ai, `*` = son 45 günde kullanıldı.

## 1. Departmanı olan işler — giriş ve eksik bağlar

| İş türü | Giriş (sıra orada) | Departman Dizin'inde olmayan, eklenecek kurulu araç |
|---|---|---|
| Arayüz, landing, bileşen, CSS | `departman-frontend`* | ajanlar `fe-*` 19 (Dizin'de yok); `infinite-canvas` MCP (tuval), `canva`/`Adobe for creativity` MCP (yalnız CC, yetki bekliyor) |
| Animasyon, scroll, 3D web sahne | `departman-frontend`* adım 4 → `animasyon-atolyesi` | `threejs-bloom`*, `web-sahne-desenleri`*, `webgpu-threejs-tsl` plugin (bağsız) |
| Test, e2e, görsel QA | `departman-test-qa`* | ajanlar `qa-*` 18; `chrome-devtools` MCP (bağsız, CC) |
| Güvenlik, sır, SAST | `departman-guvenlik`* | ajanlar `sec-*` 15; `strix-agent` CLI, `ecc-agentshield` CLI (kullanılmadı) |
| Veri, SQL, şema | `departman-veri-db`* | ajanlar `db-*` 22; `clickhouse` MCP, `drizzle-docs` MCP, `airtable` MCP (bağsız) |
| .NET, ASP.NET, backend | `departman-backend-dotnet` | ajanlar `be-*` 15; `binlog` MCP (ikisi), `mslearn`* MCP |
| Plan, PRD, görev bölme | `departman-surec-plan`* | ajanlar `pln-*` 14 |
| Kod inceleme | `departman-surec-inceleme` | ajanlar `inc-*` 12; `code-review` MCP (ikisi), `open-code-review` CLI (bağsız) |
| Git, PR, yayın, deploy | `departman-surec-git-yayin`* | `netlify` MCP, `hostinger` MCP, `vercel`* CLI (bağsız); ajanlar `git-*` 8 zaten listede |
| Belge, rapor, PDF/DOCX | `departman-belge`* | ajanlar `dok-*` 11; `markitdown`* MCP |
| Araştırma, video tarama, kütüphane | `departman-arastirma-ogrenme`* | ajanlar `ara-*` 9; `arxiv` `apify` `context7`* `hfspace` MCP; `agent-reach`* CLI |
| Skill/ajan/araç yazımı | `departman-surec-ajan-arac`* | — (ajn-* bağlı) |
| Bağlam, jeton, oturum | `departman-verimlilik`* | `context-mode`* `headroom`* `qmd` `codebase-memory-mcp` `codegraph` `serena` MCP; `claude-monitor` `claude-usage`* CLI |

## 2. Departmansız işler — araç sırası (müdür yok; ilk durak bu tablo)

| İş türü | Sıra (önce kurulu ve ölçülmüş olan) | Taraf notu |
|---|---|---|
| Video kurgu, kısa klip, altyazı | `video-cli`* (video tarama/indir) → `ffmpeg`* / `whisper-cli`* → `premiere-pro` MCP (kurgu) → `hyperframes` plugin (HTML→video) → ajanlar `vid-*` | premiere-pro, hyperframes yalnız CC |
| Blender, 3D model, render | `blender`* plugin (1.3.0 repo; CC 1.1.0) → `blender-uretim`* / `blender-oturum`* → `blender`* MCP → ajanlar `bl-*` | blender MCP ikisi; skill zip AI'de |
| Oyun, mod | `mod-atolyesi`* → `godot` / `unity` MCP → `universal-modder` plugin → ajanlar `oyn-*` | godot/unity yalnız CC |
| Görsel üretim, logo, ikon | `nano-banana-2`* MCP → `figma` → `logo-design` / `llm-icon-finder` plugin → `fal` MCP | fal, canva yalnız CC; ücretli çağrıda tavan şart |
| Otomasyon, iş akışı, kazıma | `n8n-mcp` → `airtable` → `apify` MCP → ajanlar `otm-*` → `scrapling-skill` plugin | hepsi yalnız CC |
| Hukuk, sözleşme, KVKK | `commercial-legal` / `privacy-legal`* plugin → `Ironclad` MCP → ajan `dok-sozlesme-madde` → `sec-kvkk-gdpr-kontrol` | DocuSign, iManage yetki bekliyor |
| Pazarlama, reklam, içerik | `marketing-skills` / `claude-ads` plugin → ajanlar `urn-*` → `humanizer` plugin | hepsi kullanılmadı, yalnız CC |
| Altyapı, bulut, k8s | `azure` plugin+MCP → `terraform-skill` plugin → ajanlar `ops-*` | yalnız CC |
| ML, değerlendirme, LLM eval | `promptfoo-evaluation` plugin → ajanlar `ml-*` → `ajn-skill-test` | yalnız CC |
| Mobil | `expo` plugin+MCP → `android-skills` plugin → ajanlar `mob-*` | yalnız CC |
| Dil/çatı uzmanlığı (Go, Rust, Python…) | ajanlar `dil-*` 26 (ad = dil) | yalnız CC |

## 3. Taraf kuralı (CC ↔ Desktop/claude.ai)

- AI'de alt ajan yok: tablodaki `xx-*` ajanları AI'de `departman-*/ajanlar/<ad>.md` talimatı olarak okunur (207 tanesi bu yolla var; 373 tanesi AI'de hiç yok).
- AI'de plugin yok: plugin skill'i AI'ye yalnız zip ile gider (1125'ten 213'ünün senkron kopyası var).
- Desktop MCP 18 (15'i CC ile ortak). CC'deki 46 MCP AI'de yok; AI'den CC aracına köprü `cc-kopru` (31 izinli CLI).
