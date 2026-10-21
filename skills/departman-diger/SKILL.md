---
name: departman-diger
description: "Departmansız işler müdürü: video kurgu, Blender/3D, oyun/mod, görsel üretim, otomasyon/kazıma, hukuk, pazarlama, bulut/k8s, ML/eval, mobil, dil uzmanlığı. Bu işlere başlarken önce oku."
---

# Departman: diğer — iş → araç sırası
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

Kaynak: `docs/envanter/is-arac.md` §2. Satırda soldan sağa: önce kurulu ve ölçülmüş olan. `ajan:` = alt ajan; claude.ai'de alt ajan yok → bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula.

## Sıra
| İş türü | Sıra | Taraf notu |
|---|---|---|
| Video kurgu, kısa klip, altyazı | `video-cli` (tarama/indir) → `ffmpeg` / `whisper-cli` → `premiere-pro` MCP → `hyperframes` plugin (HTML→video) → ajan `vid-*` | premiere-pro, hyperframes yalnız CC |
| Video linki → bilgi (uzun/kısa) | `video ozet <url>` (önbellekte 1 sn, ≤6 satır) → `video paket <id>` (~79 sn, yerel) → `video kare <id> --t …` → altyazı yoksa/Gemini kotası bittiyse `ffmpeg -ss … -t 30 -ar 16000 -ac 1` + `whisper-cli -m ggml-large-v3-turbo.bin --prompt "<sözlük>"` (CUDA; sözlük garanti değil, özel adı ekran metniyle karşılaştır). Kare metni: RapidOCR (CPU ~30 sn/kare, ikon gürültüsü var) → boşsa VLM `qwen3.5:4b` (RAM <%80 ise). Dikey klip hazırlığı: `ffmpeg -vf "crop=ih*9/16:ih,scale=540:960"`. Desktop: köprü `komut` ile `video ozet`, ayrıntı için köprü `ajan` → `video-tarayici`; Desktop'a yalnız rapor yolu + ≤5 satır döner. Ayrıntı ve ölçüler: `docs/ogren/g3.md` | Desktop kendi indirmez; Remotion/hyperframes render ve VLM kolu bu turda denenmedi |
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

Slash katalog (iş türü → /komut·skill): `yetenek-getir/reference/slash-katalog.md` — Read; oturuma yüklenmez.

Kombo adayları (A/B ölçümü geçmedi; önerme, yalnız ipucu): vm-video-izle, vm-blender-dekupaj, vm-tam-sayfa-yakalama.
