# 9 — Blender "profesyonel modelleyici" araştırması (Desktop Claude, Advanced Research, 2 Eki 2026)

Kaynak: Claude Desktop derin araştırma raporu (özet; kararlar + bağlantılar). Doğrulanmayanlar "doğrulanmadı" diye işaretli — kurmadan önce depo sayfasından teyit et.

## Özet karar
Yeni büyük Blender MCP'si yok. Resmi Blender Lab MCP + bizim kapı/bekçi/kanıt araçlarımız temel. Eksik: geometrinin kaynağı (CAD çekirdeği, üretken model) ve ağ temizliği (retopo, UV).

## KUR
| aday | bağlantı | ne | lisans | not |
|---|---|---|---|---|
| build123d-mcp | https://github.com/pzfreo/build123d-mcp | build123d (OCCT B-rep) üstünde execute/validate/measure/compare/export; skill (b123d-modeling) | lisans dosyası doğrulanmadı | CADGenBench Haz 2026: aynı model 0.360 → 0.457 (+%27), geçerlilik %88 → %100; sürüm 0.3.90; sandbox katmanları |
| STEP Importer | https://extensions.blender.org/add-ons/step-importer/ | STEP/STP/IGES → (Cascadio) glTF → Blender içe aktarma | Blender Extensions (GPL uyumlu) | v1.2.1, Blender 5.1+; Windows desteği doğrulanmadı |
| QRemeshify | https://github.com/ksami/QRemeshify | QuadWild + Bi-MDF quad retopo; simetri; dikiş/keskin/malzeme sınırı rehberi; harici program yok (ikili gömülü) | GPL-3 | Blender 4.2+; spiral/iç içe organik şekillerde zayıf |
| sivik Retopology Extension | https://github.com/sivik/Retopology-Blender-Extension | 6 remesh modu · LOD · eğrilik haritası · topoloji kalite metrikleri; QRemeshify'ı algılar | Apache-2.0 | Blender 5.0+ |
| Pixal3D + TRELLIS.2 (ComfyUI çekirdeğinde) | https://blog.comfy.org/p/trellis2-and-pixal3d-are-now-native · https://huggingface.co/Comfy-Org/Pixal3D | tek görselden dokulu PBR GLB; çekirdek UV açma + normal/AO pişirme | kod + ağırlık MIT (20 May 2026'dan beri); Comfy sürümünde nvdiffrast kaldırıldı | UYARI: HF'de extra_gated_eu_disallowed bayrağı · DINOv3 bileşeninin kendi lisansı · ticari kullanım issue #33 yanıtsız (TencentARC/Pixal3D) → müşteri tesliminde hukuki kontrol |

12 GB / Windows kanıtı (kullanıcı raporları): int8 checkpoint 5.58 GB; RTX 4070 12 GB/Win11'de DecimateMesh target_face_count < 700k ile uçtan uca GLB (ComfyUI issue #16056); Remesh 31.4M yüzde 18 GiB isteyip çöktü (issue #15996, 12 GB + 32 GB RAM). Topluluk: 8-12 GB kart için 32 GB+ RAM, taslak ~6.8 GB VRAM. → bizde sınırda; tek ağır süreç, GPU kilidi, RAM bekçisi zorunlu.

## DENE (sonra — animasyon fazı)
- UniRig https://github.com/VAST-AI-Research/UniRig (MIT, ≥8 GB VRAM, Windows doğrulanmadı) · Puppeteer https://github.com/Seed3D/Puppeteer (Apache-2.0) · TripoSG (MIT, yalnız şekil) · agentcad https://agentcad.dev (CLI, build123d-mcp yetmezse).

## ÖĞREN — mekanizma al, kurma
| kaynak | bağlantı | alınacak mekanizma |
|---|---|---|
| ozanzeng/blender-LPM-skill (+ blender-modelling-skills) | https://github.com/ozanzeng/blender-LPM-skill | compare_silhouette: render'ı referansın üstüne bindir → IoU + en-boy hatası + ağırlık merkezi hatası + bindirme görüntüsü (kalkan örneği IoU 0.78 → 0.95, en-boy hatası %23 → %0.9); 4-5 görünüm sayfası; headless çalışma |
| 3DHarnessBench (Apache-2.0) | https://arxiv.org/html/2609.06535v1 | ajana ölçü sorgusu (bbox, boyut, parça istatistiği) vermek her modelde işe yarar; serbest kamera yalnız güçlü modelde → sabit kanıt görünümleri kalsın, serbest kamera opsiyonel |
| 3DCodeBench | https://arxiv.org/pdf/2606.01057 | headless Blender betiği + örnek başına süre bütçesi (600-900 sn) ile kendini düzeltme |
| vladmdgolam agent-skills blender-mcp skill | https://claudemarketplaces.com/skills/vladmdgolam/agent-skills/blender-mcp | prosedürel düğümler glTF'e taşınmaz → export öncesi normal/renk haritasına pişir · export'u MCP'den değil headless'tan (MCP'de zaman aşımı) · glTF'de export_animations + export_nla_strips, Draco kapalı → sıkıştırma gltf-transform |
| blend-ai (175 araç, 12 MCP prompt) | https://github.com/HoldMyBeer-gg/blend-ai | uzman MCP prompt'ları + iş akışları + ağ kalite analizi (oku, kurma) |
| harveyxiacn/blender-mcp (359 araç) | https://github.com/harveyxiacn/blender-mcp | araç profilleri (minimal 29 / skill 32 / full 356) → token fazında MCP profili fikri |
| PatrykIti/blender-ai-mcp | https://github.com/PatrykIti/blender-ai-mcp | hedef-öncelikli yönlendirici + search_tools/call_tool ile küçük araç yüzeyi + deterministik doğrulama |
| scenario-labs/skills | https://github.com/scenario-labs/skills | Blender 5.2 uzman dokümanları (retopo · UV/bake · rig); headless 5.2.1 testleri — referans olarak oku (ana ürün ücretli MCP) |
| Blender 5.1 SLIM UV | https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html | bpy.ops.uv.unwrap(method='MINIMUM_STRETCH'); Pack UV Islands özel bölge |
| Rigify | Blender yerleşik | metarig → generate tarifi (animasyon fazında) |

Texel yoğunluğu için olgun ücretsiz ajan aracı yok → kendi metriğimiz: UV alanı / 3D yüzey alanı oranı (nesneler arası tutarlılık).

## RED
Hunyuan3D 2.1 (AB/BK/Güney Kore hariç bölge lisansı, 1M MAU sınırı) · Stable Fast 3D / SPAR3D (yıllık gelir ≥1M USD kurumsal lisans) · Ubisoft CHORD (yalnız araştırma lisansı) · RFingAdam/mcp-blender (ağır) · arjun988/blender-skills (94 skill, token) · ahujasid → mcp-for-blender (yalnız ad değişti; önceki CVE/telemetri endişeleri) · 6xvl/blender-mcp (iwr | iex kurulum) · AccuRIG, Mixamo (GUI, ajana girmez) · TripoSR (Pixal3D varken gereksiz) · ücretli: Blender MCP Pro, StraySpark, StepIO, Quad Remesher, Auto-Rig Pro, Tripo/Meshy/Rodin.

## Token / RAM notları
- CLI > MCP; uzun işler (export) headless. Tool search açık; yerel MCP'leri stdio tut (HTTP MCP'lerin ertelenmediği hata raporu #40314).
- Aynı anda tek ağır süreç: ComfyUI üretken 3D YA DA Cycles render YA DA rig modeli.
- Pixal3D "dynamic VRAM" VRAM'i sistem RAM'ine taşır → 32 GB'ı hızla tüketir.

## Doğrulanamayanlar
benchlm CADGenBench anlık görüntüsü · StraySpark tarihleri · triposr.org karşılaştırmaları · Hunyuan VRAM · build123d-mcp ve STEP Importer'ın Windows'ta çalışması ve lisans dosyaları · UniRig/Puppeteer Windows · Casys-AI/fingerskier · autoremesher/Instant Meshes güncelliği · LL3M/BlenderAlchemy/SceneCraft ayrıntıları.
