# DERS KİTABI İSKELETİ — 3D C: ANİMASYON
Kaynak: blender-agent-skills 1.1.0 (MIT, EL4CTEO) + docs/okul/kaynak/3d-c/. Başlıklar kaynaktan birebir; içerik doldurma = kuyruk işi (ücretsiz havuz dönünce `python tools/okul/hat.py 3d-c`).

## Seviye merdiveni (her seviye: ders bölümü · hata kataloğu · 1-2 ölçülü alıştırma · kalite kapısı)
- C1 12 prensip+graph editor
- C2 rig+yürüyüş
- C3 OYUN ANİMASYONLARI
- C4 mocap+yüz/lipsync
- C5 sinematik/kamera

## Kaynak: animation
> "Animation in Blender 5.2 - slotted/layered actions and the channelbag API, Python keyframing, F-curves, game loops, NLA clips, pose library, mocap/BVH retargeting via constraints, baking control rigs to export skeletons, root motion, per-clip export. Use for any keyframe, action, NLA, mocap, or anim" (animation.md)
- ## 5.x data model (what changed)
- ## Workflow (keyframe animation, studio style)
- ## Game animation rules
- ## Bake control rig → export skeleton
- ## Mocap and retargeting
- ## NLA and pose library
- ## Shape keys and other properties
- ## Gotchas

## Kaynak: character-rigging
> "Character rigging in Blender 5.2 - Rigify metarig fit/generate, bone naming/roll/collections, DEF/MCH/control layers, IK/FK, robust skinning (heat + proxy fallback), weight-painting rules, correctives, engine game skeletons (Unity, Unreal, Roblox R15), rig validation and deformation stress tests. Us" (character-rigging.md)
- ## Pipeline (scripts chain; each returns JSON)
- ## Bone rules
- ## Weight painting rules (what pros check)
- ## Correctives (beyond weights)
- ## Engine skeleton specifics
- ## Gotchas

## Kaynak: export-pipelines
> "Export from Blender 5.2 with verified presets - Roblox (FBX/glTF, cages, R15, SurfaceAppearance), Unity (FBX, Humanoid), Unreal (FBX skeletal, Nanite, UCX), Godot/web (GLB, meshopt/Draco, WebP), USD. Scale/axes, smoothing, tangents, leaf bones, clips, batch export, post-export verification. Use when" (export-pipelines.md)
- ## One call
- ## Engine reference (load only the one you need)
- ## Universal pre-export checklist
- ## Format choice
- ## Verify after export (required)
- ## Collection exporters (re-export in one click, 4.2+)
- ## Gotchas

## Kaynak: facial-shapekeys
> "Facial rigs and shape keys in Blender 5.2 - ARKit 52 blendshapes, visemes for lip-sync, sculpting expressions, splitting symmetric shapes into Left/Right, mirroring, corrective and combination shapes, drivers and control rigs, bone+blendshape hybrids, export to engines (Unity, Unreal, Roblox dynamic" (facial-shapekeys.md)
- ## Choose the approach
- ## Procedure (blendshapes)
- ## Shape key rules
- ## Correctives and combination shapes
- ## Engine notes
- ## Gotchas

## Kaynak: workflow-recipes
> "End-to-end Blender 5.2 playbooks chaining the blender-* skills with QA gates - game props (mid-poly, high-to-low), game characters (sculpt/AI mesh to rigged, animated export), Roblox props/accessories/avatars, AI or downloaded asset cleanup, procedural environments, web/AR assets, product turntables" (workflow-recipes.md)
- ## 1. Game prop, mid-poly (fast, no bake)
- ## 2. Game prop, high → low baked (hero quality)
- ## 3. Game character (sculpt or AI mesh → animated export)
- ## 4. Roblox
- ## 5. Cleaning AI-generated / downloaded assets
- ## 6. Procedural environment
- ## 7. Web / AR asset
- ## 8. Product shot / turntable
- ## 9. Mood / weather shot (rainy night, snowy morning, foggy dawn)

## Hata kataloğu
KAYNAK EKSİK: alıştırma sonrası beyin dersleri + kaynak 'pitfall' bölümleri doldurulacak.

## Kalite kapısı
taban → son: yargıç puanı ≥ taban+%20 ve ≥%90; RAM %75 eşik; Blender iş bitince kapanır.