# DERS KİTABI İSKELETİ — 3D D: EFEKT/VFX
Kaynak: blender-agent-skills 1.1.0 (MIT, EL4CTEO) + docs/okul/kaynak/3d-d/. Başlıklar kaynaktan birebir; içerik doldurma = kuyruk işi (ücretsiz havuz dönünce `python tools/okul/hat.py 3d-d`).

## Seviye merdiveni (her seviye: ders bölümü · hata kataloğu · 1-2 ölçülü alıştırma · kalite kapısı)
- D1 parçacık+duman
- D2 sıvı/kumaş/rigid
- D3 OYUN VFX
- D4 geometry nodes efekt
- D5 kompozit+video

## Kaynak: asset-qa
> "Mandatory review gate for any mesh or asset created or edited in Blender. Detects z-fighting (coplanar overlaps), floating/detached parts, inverted or inconsistent normals, non-manifold/open geometry, degenerate faces, duplicate verts, n-gons, unapplied scale, UV problems, bad skin weights, and rend" (asset-qa.md)
- ## Procedure
- ## What each finding means → fix
- ## Manual checks the script can't fully judge
- ## Tuning

## Kaynak: game-optimization
> "Optimize Blender assets for real-time engines - triangle/material/texture/bone budgets per platform (mobile, Roblox, web, VR, console, PC), LOD chains, decimation modes, mesh cleanup, draw-call reduction (material merging, atlases, trim sheets), instancing, vertex-split costs, collision proxies, tex" (game-optimization.md)
- ## Procedure
- ## Budgets (guidance per asset, 2026)
- ## Decimate modes
- ## The hidden cost: vertex splits
- ## LOD rules
- ## Draw calls and batching
- ## Collision
- ## Rig and animation cost
- ## Gotchas

## Kaynak: geometry-nodes
> "Geometry Nodes in Blender 5.2 - fields, domains, attributes, instancing, zones (simulation/repeat/for-each), closures/bundles, lists, SDF grids, node tools, baking, plus a JSON-to-node-tree builder and socket inspector. Use for scattering, procedural assets/environments, parametric tools and modifie" (geometry-nodes.md)
- ## Core concepts (get these right or nothing works)
- ## Zones and advanced types
- ## Procedure
- ## Rules
- ## Gotchas

## Kaynak: simulation
> "Physics in Blender 5.2 - rigid bodies (density mass, shapes, bake to keys), classic cloth presets and pinning, new node-based Cloth/Hair Dynamics (XPBD, Collider, effectors), Mantaflow fluids, hair curves, GN simulation zones, headless baking. Use for destruction, drapes, flags, falling objects, liq" (simulation.md)
- ## One call
- ## Choose the solver
- ## Rigid bodies
- ## Classic cloth
- ## Node-based dynamics (5.2, experimental)
- ## Fluids (Mantaflow) quick setup
- ## Rules
- ## Gotchas

## Kaynak: weather-fx
> "Weather effects in Blender 5.2 - looping Geometry Nodes rain, snow, dust, ash and embers with ground hits and splashes, wet surfaces, puddles with animated ripples, wall streaks, snow cover (shader + real snow geometry), storm lightning with multi-stroke flashes and bolts, engine-ready weather masks" (weather-fx.md)
- ## One call each
- ## precipitation.py (rain, snow, dust, ash, embers)
- ## surface_weather.py (wet, puddles, ripples, streaks, snow)
- ## lightning.py
- ## Rules
- ## Games and real-time
- ## Gotchas

## Hata kataloğu
KAYNAK EKSİK: alıştırma sonrası beyin dersleri + kaynak 'pitfall' bölümleri doldurulacak.

## Kalite kapısı
taban → son: yargıç puanı ≥ taban+%20 ve ≥%90; RAM %75 eşik; Blender iş bitince kapanır.