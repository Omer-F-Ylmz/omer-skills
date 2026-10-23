# DERS KİTABI İSKELETİ — 3D A: MODELLEME
Kaynak: blender-agent-skills 1.1.0 (MIT, EL4CTEO) + docs/okul/kaynak/3d-a/. Başlıklar kaynaktan birebir; içerik doldurma = kuyruk işi (ücretsiz havuz dönünce `python tools/okul/hat.py 3d-a`).

## Seviye merdiveni (her seviye: ders bölümü · hata kataloğu · 1-2 ölçülü alıştırma · kalite kapısı)
- A1 basit prop
- A2 karmaşık hard-surface
- A3 organik+sculpt
- A4 KARAKTER (sculpt→retopo→UV→bake)
- A5 çevre/prosedürel

## Kaynak: blender-uretim
> "Blender'da 3D ürün üretimi, bpy (Blender Python) betiği: fincan/cezve modelle, ışıkla, malzeme kur, render al, GLB'yi web'e hazırla; blender-oturum ile yükle. 3DMigoto, three.js, 2D görsel değil." (blender-uretim.md)
- ## Ölçü ve ad
- ## Sahne = kod
- ## Teslim
- ## Görüntü disiplini
- ## API disiplini
- ## Kurallar

## Kaynak: geometry-nodes
> "Geometry Nodes in Blender 5.2 - fields, domains, attributes, instancing, zones (simulation/repeat/for-each), closures/bundles, lists, SDF grids, node tools, baking, plus a JSON-to-node-tree builder and socket inspector. Use for scattering, procedural assets/environments, parametric tools and modifie" (geometry-nodes.md)
- ## Core concepts (get these right or nothing works)
- ## Zones and advanced types
- ## Procedure
- ## Rules
- ## Gotchas

## Kaynak: hardsurface-modeling
> "Hard-surface and prop modeling in Blender 5.2 - blockout-to-detail flow, non-destructive modifier stacks (Mirror, Boolean Exact/Manifold, Bevel, Weighted Normal, Smooth by Angle), mid-poly vs subdivision vs high-to-low workflows, shading/custom normals, cylinder segment budgets, edge attributes from" (hardsurface-modeling.md)
- ## Pick the workflow first
- ## Procedure
- ## Stack rules
- ## Topology rules
- ## Edge/face attributes from Python (4.0+ names)
- ## Gotchas

## Kaynak: retopology-uv
> "Retopology and UVs in Blender 5.2 - auto retopo (Quadriflow, Decimate, planar), deformation edge flow, seams, unwrap (Angle Based, Minimum Stretch, Smart), pixel-margin packing, texel density measure/set, lightmap UV2, UDIMs, mirrored UVs. Use to turn sculpts/scans/AI meshes into game meshes or prep" (retopology-uv.md)
- ## Retopology
- ### Edge flow rules for deforming meshes
- ## UVs
- ### Texel density targets (px/m; studio baselines, not laws)
- ## Special cases
- ## Gotchas

## Kaynak: scene-setup
> "Set up and audit Blender scenes the way studios do - units and real-world scale, collection layout, naming conventions (SM_/SK_/T_/M_), origins, linking vs appending, library overrides, asset libraries and catalogs, collection exporters, orphan/path cleanup. Use when starting a project, organizing a" (scene-setup.md)
- ## Procedure
- ## Collection layout (one asset per .blend, or one collection per asset)
- ## Naming conventions (Unreal-style, accepted by all engines)
- ## Real-world scale reference (meters)
- ## Linking, appending, overrides
- ## Asset libraries
- ## Hygiene rules

## Kaynak: sculpting
> "Sculpting in Blender 5.2 - base-to-detail workflow, voxel remesh, dyntopo, multires, 5.x brush types, masks/face sets, symmetry, plus headless-safe procedural ops for agents (remesh, symmetrize, multires, inflate, noise detail, smooth) and the sculpt-to-game handoff. Use for organic models, characte" (sculpting.md)
- ## Agents: what you can and can't do
- ## Professional workflow
- ## Brushes (5.x: brushes are assets in the Essentials library)
- ## Rules of thumb
- ## Gotchas

## Hata kataloğu
KAYNAK EKSİK: alıştırma sonrası beyin dersleri + kaynak 'pitfall' bölümleri doldurulacak.

## Kalite kapısı
taban → son: yargıç puanı ≥ taban+%20 ve ≥%90; RAM %75 eşik; Blender iş bitince kapanır.