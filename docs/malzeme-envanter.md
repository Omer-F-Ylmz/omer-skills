---
type: reference
status: aktif
tags: [malzeme, 3d, video, gorsel, envanter]
relatedTo: [tools/uret_malzeme.py, docs/kurulumlar/hunyuan3d.md]
---
# Malzeme envanteri (SITE-MALZEME-1, 28 Eki)

Kaynak: docs/arac-kart/kart.jsonl, docs/kurulumlar/hunyuan3d.md, arka/yaka-3d-*.json + yaka durum.md, `C:\AI\ComfyUI\models`, anahtar varlığı (yalnız boolean). "Doğrulandı" = bu oturumda ya da kayıtta çalıştığı görüldü.

| Araç | Ne üretir | Ücretsiz mi | Kalite | Nasıl çağrılır |
|---|---|---|---|---|
| ComfyUI + FLUX.1 schnell fp8, FLUX.2 klein 4B, Z-Image Turbo (`C:\AI\ComfyUI`) | görsel, ürün, doku, düzenleme | evet, yerel | iyi (Z-Image foto/ürün, klein metin/düzenleme) | `python tools/gorsel_uret.py ac/uret/kapat`; skill `gorsel-uret`. Doğrulandı |
| ComfyUI + Wan 2.2 TI2V 5B (model dosyası var) | görsel→video | evet, yerel | model var, **iş akışı bağlı değil** | gorsel_uret.py'de akış yok; eklenmeli |
| HF ZeroGPU `tencent/Hunyuan3D-2` | image-to-3D (şekil, dokusuz glb ~5 MB) | evet, günlük kota (HF_TOKEN var) | iyi şekil; doku yok → Blender bake (yaka-3d-3) | `uret_malzeme.py 3d --saglayici hf-zerogpu`. Doğrulandı 28 Eki (5,1 MB glb) |
| HF ZeroGPU Hunyuan3D-2.1, TRELLIS | dokulu 3D | evet, kota | kota 0 / `generation_all` bozuk (yaka-3d-4/5) | kota sıfırlanınca yeniden denenecek; doğrulanmadı |
| fal.ai (FAL_KEY var) | görsel (flux/schnell), video (ltx), 3D (trellis, tripo) | hayır, ucuz | iyi | `uret_malzeme.py --saglayici fal`. **28 Eki: bakiye bitti (403 "Exhausted balance")**, yükleme gerekir |
| Higgsfield SDK (venv `C:\Users\pc\.venvs\higgsfield`, anahtar var) / MCP | görsel (Soul), video (DoP) | ücretsiz plan ~10 kredi | yüksek (video) | `uret_malzeme.py --saglayici higgsfield` (model kimlikleri doğrulanmadı); sırada yer almaz |
| Blender + blender-oturum/blender-uretim/blender-dogrulama | modelleme, malzeme, ışık, render, GLB | evet, yerel | en yüksek kontrol | skill `blender-oturum` → `blender-uretim`; `tools/blender_*.py`, headless `-b` |
| Sketchfab | hazır 3D model indirme | çoğu CC lisanslı | değişken, lisans oku | `yaka-cicegi/indir-sketchfab` hattı (elle) |
| 3d-* / threejs-* skill'leri (3d-high-poly-models, 3d-wood-material, 3d-retina-resolution, threejs-procedural-materials/-shadow-systems/-bloom…) | gerçek zamanlı Three.js malzeme, ışık, retina | evet | yüksek | `Skill threejs-3d-paket` altından adla |
| tasteforge (`ecc:tasteforge-video`) | görsel/video/3D keşfi, tat çıkarma | evet (skill) | yön belirler, üretmez | `Skill ecc:tasteforge-video` |
| Claude Design (claude-design MCP: create_project/write_files/render_preview), hifi-design, frontend-design | arayüz tasarımı, önizleme | hesap planı | iyi | `mcp__claude-design__*` (cc-kopru); 3D/animasyon üretmez |
| nano-banana-2 MCP, banana-claude | görsel | Gemini kotası | iyi | MCP / `Skill nano-banana-2:generate-image` |
| Tripo (doğrudan) | image-to-3D PBR | TRIPO_API_KEY yok | yüksek | fal üzerinden `--model tripo` (bakiye gerekir) |

## uret_malzeme.py sağlayıcı sırası
görsel: ComfyUI → fal → (Higgsfield yalnız açıkça) · video: fal (Comfy akışı bağlanana kadar) · 3D: HF ZeroGPU → fal (trellis; `--model tripo` pahalı). Ücretsiz önce, ücretli ucuzdan pahalıya; ücretli gerçek üretim `--tavan` ister, tahmin aşarsa seçilmez.

## Bilinen boşluklar
fal bakiyesi 0 · Wan 2.2 akışı yok · HF 3D'de doku Blender bake ile · fiyatlar `uret_malzeme.py` içinde elle tahmin, doğrulanmadı.
