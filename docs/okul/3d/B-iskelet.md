# DERS KİTABI İSKELETİ — 3D B: MATERYAL/IŞIK/RENDER
Kaynak: blender-agent-skills 1.1.0 (MIT, EL4CTEO) + docs/okul/kaynak/3d-b/. Başlıklar kaynaktan birebir; içerik doldurma = kuyruk işi (ücretsiz havuz dönünce `python tools/okul/hat.py 3d-b`).

## Seviye merdiveni (her seviye: ders bölümü · hata kataloğu · 1-2 ölçülü alıştırma · kalite kapısı)
- B1 PBR+HDRI
- B2 ürün/stüdyo ışığı
- B3 fotogerçekçi mekân
- B4 cilt/saç/kumaş
- B5 sinematik renk/kompozit+upscale

## Kaynak: lighting-lookdev
> "Lighting, cameras and look-dev in Blender 5.2 - studio 3-point and product lighting, HDRI environments, sun/sky exteriors, interiors, light linking, physically based light units, camera focal lengths/composition/DOF, cyclorama backdrops, looping turntables for asset presentation. Use when presenting" (lighting-lookdev.md)
- ## One call: presentation scene
- ## Lighting recipes
- ## Camera rules
- ## Look-dev procedure (material approval)
- ## Gotchas

## Kaynak: pbr-materials
> "Physically based materials in Blender 5.2 - metal/roughness rules, Principled BSDF inputs, color spaces (sRGB vs Non-Color), measured albedo/F0 values, texture-set auto-wiring, ORM channel packing, DirectX vs OpenGL normals, alpha modes, displacement, view transforms (AgX, Khronos PBR Neutral), engi" (pbr-materials.md)
- ## Fast paths
- ## The rules (violations are what make renders look "CG")
- ## Principled BSDF (5.2) quick map
- ## Engine export rules
- ## Alpha
- ## Displacement
- ## View transform (judge materials under the right one)
- ## Procedural → texture
- ## Gotchas

## Kaynak: rendering
> "Render with Blender 5.2 Cycles/EEVEE/Workbench - quality presets, GPU setup, adaptive sampling, denoising, light paths, color management (AgX, Khronos PBR Neutral, ACES), PNG/EXR/MP4 output, passes, the 5.0 compositor API, CLI and multi-camera batch rendering. Use for any still, animation or turntab" (rendering.md)
- ## One call
- ## Engine choice
- ## Cycles quality levers (ordered by impact)
- ## Color management (decide once per project)
- ## Output formats
- ## Compositor (5.0+ API)
- ## CLI rendering (render farms, CI)
- ## Gotchas

## Kaynak: texture-baking
> "Bake texture maps in Blender 5.2 Cycles - high-to-low normal maps with cage/extrusion, AO, curvature, ID, thickness, base color/roughness/metallic from procedurals, ORM packing, OpenGL vs DirectX, margins, GPU baking, fixing skewing/waviness/seams. Use when transferring sculpt or high-poly detail to" (texture-baking.md)
- ## One call
- ## Preparation checklist (most bake bugs come from this list)
- ## Rays: extrusion vs cage
- ## Map guide
- ## Fixing common artifacts
- ## Baking non-PBR data
- ## Gotchas

## Kaynak: time-of-day
> "Time of day and atmosphere in Blender 5.2 - measured sky + sun for dawn, morning, noon, golden hour, sunset, blue hour, overcast, night/moonlight with stars and city glow, exposure balance, height fog from visibility, god rays, Cycles vs EEVEE volumes, compositor grade, stylized moods (cyberpunk neo" (time-of-day.md)
- ## One call
- ## How it stays physically right
- ## Fog and volumetrics
- ## Rules
- ## Gotchas

## Hata kataloğu
KAYNAK EKSİK: alıştırma sonrası beyin dersleri + kaynak 'pitfall' bölümleri doldurulacak.

## Kalite kapısı
taban → son: yargıç puanı ≥ taban+%20 ve ≥%90; RAM %75 eşik; Blender iş bitince kapanır.