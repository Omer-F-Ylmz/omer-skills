---
name: departman-diger
description: "Departmansız işler müdürü: video kurgu, Blender/3D, oyun/mod, görsel üretim, otomasyon/kazıma, hukuk, pazarlama, bulut/k8s, ML/eval, mobil, dil uzmanlığı. Bu işlere başlarken önce oku."
---

# Departman: diğer — iş → araç sırası
Katalogda bulunmayan, alan dışı ya da emin olunmayan iş: Skill `yetenek-getir` (3.3k araç, işle ilgili her şey, gruplu).

Kaynak: `docs/envanter/is-arac.md` §2. Satırda soldan sağa: önce kurulu ve ölçülmüş olan. `ajan:` = alt ajan; claude.ai'de alt ajan yok → bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula.

## Sıra
| İş türü | Sıra | Taraf notu |
|---|---|---|
| Video kurgu, kısa klip, altyazı | `video-cli` (tarama/indir) → `ffmpeg` / `whisper-cli` → `premiere-pro` MCP → `hyperframes` plugin (HTML→video) → ajan `vid-*` | premiere-pro, hyperframes yalnız CC |
| Blender, 3D model, render | `blender` plugin → `blender-uretim` / `blender-oturum` → `blender` MCP → ajan `bl-*` | blender MCP ikisi |
| Oyun, mod | `mod-atolyesi` → `godot` / `unity` MCP → `universal-modder` plugin → ajan `oyn-*` | godot/unity yalnız CC |
| Görsel üretim, logo, ikon | `nano-banana-2` MCP → `figma` → `logo-design` / `llm-icon-finder` → `fal` MCP | fal yalnız CC; ücretli çağrıda tavan şart |
| Otomasyon, iş akışı, kazıma | `n8n-mcp` → `airtable` → `apify` MCP → ajan `otm-*` → `scrapling-skill` | yalnız CC |
| Hukuk, sözleşme, KVKK | `commercial-legal` / `privacy-legal` → `Ironclad` MCP → ajan `dok-sozlesme-madde` → `sec-kvkk-gdpr-kontrol` | DocuSign, iManage yetki bekliyor |
| Pazarlama, reklam, içerik | `marketing-skills` / `claude-ads` → ajan `urn-*` → `humanizer` | yalnız CC |
| Altyapı, bulut, k8s | `azure` plugin+MCP → `terraform-skill` → ajan `ops-*` | yalnız CC |
| ML, değerlendirme, LLM eval | `promptfoo-evaluation` → ajan `ml-*` → `ajn-skill-test` | yalnız CC |
| Mobil | `expo` plugin+MCP → `android-skills` → ajan `mob-*` | yalnız CC |
| Dil/çatı uzmanlığı (Go, Rust, Python…) | ajan `dil-*` (ad = dil) | ajan dosyası ikisi |

## Kapılar
- İş türü bir departman-* müdürüne uyuyorsa (arayüz, test, güvenlik, veri, .NET, belge, araştırma, plan, inceleme, git) o müdür kazanır; burası yalnız onların dışı.
- Araç bu tarafta yoksa (taraf notu) sıradaki araca geç; atlamayı raporda tek satırla yaz.
- Ücretli API/üretim çağrısında sayısal tavan ("en fazla N") olmadan başlama.
