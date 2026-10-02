# 8b — Animasyon araştırması tur 3 (Desktop Advanced Research, 2026-10-01)

8a'nın devamı; 8a'da olan tekrar edilmez. Kod yok; mekanizma + lisans + kaynak. Belirsizler "doğrulanmadı" diye işaretli.

## 1. Lisans duvarı (en önemli karar)
- AMASS lisansı: ticari kullanım, ticari ürüne dahil etme ve verinin ticari amaçla model eğitiminde kullanımı yasak. SMPL aynı (ticari lisans Meshcapade/MPI). → HumanML3D/AMASS/SMPL ile eğitilmiş metinden-hareket çıktıları müşteri işine GİRMEZ; yalnız fikir/blocking.
- Veri setleri:
| Veri | Lisans | Ticari |
|---|---|---|
| Quaternius UAL | CC0 | evet |
| CMU mocap (mocap.cs.cmu.edu) | ürüne gömülebilir, verinin kendisi (dönüştürülmüş bile) satılamaz; parmak yok, el/ayak parmağı gürültülü | evet (ürün içinde) |
| 100STYLE (ianxmason.github.io/100style) | CC BY 4.0, 100 stil, 60 fps, 4M+ kare; atıf "The 100STYLE Dataset - Ian Mason"; Geno mesh + local-phases kodu ticari değil | evet, atıflı |
| AIST++ anotasyon | CC BY 4.0 (video/müzik ayrı, SMPL bağımlı) | anotasyon evet |
| Bandai-Namco Research | CC BY-NC(-ND) | hayır |
| LAFAN1 / lafan1-resolved / ZeroEGGS | CC BY-NC-ND 4.0 | hayır |
| Motorica Dance | yazılı izinsiz ticari yok | hayır |
| AMASS / HumanML3D / SMPL(-X) | MPI ticari olmayan | hayır (SMPL-X sayfası doğrulanmadı) |

## 2. Motion matching (oyunlar, özellikle zombi-survival)
- Referans açık uygulamalar: JLPM22/MotionMatching (Unity 6, BVH veritabanı) · MxM topluluk çatalı (MIT) · GuilhermeGSousa/godot-motion-matching (Godot 4 C++, Mart 2026) · theroeberry/Motion-Matching-For-Godot (MIT; katmanlı AABB arama + inertialization) · V-Sekai/motion_matching. Olgun JS/WebGPU kütüphanesi yok → kendi `mm-lite` modülümüz.
- Mekanizma: özellik vektörü = 20/40/60 kare sonraki kök konum+yön, iki ayak konum+hız, kalça hızı; her boyut normalize; arama ~0,1 s'de bir; geçiş crossfade değil inertialization (yarı ömür ~0,1 s). Küçük veritabanında (birkaç bin kare) kaba-kuvvet tarayıcıda yeterli (mühendislik çıkarımı).
- Klipler root motion'lı olmalı; oyun karakteri kapsülle gider → kök XZ/yaw deltası ayrı kanala çıkarılır, görsel kök sıfırlanır.
- Katman: alt gövde = lokomosyon (MM/durum makinesi), üst gövde = kemik maskeli saldırı, üstüne additive vuruş tepkisi/nefes.
- Roblox da motion matching'i "Late 2026" yol haritasına koydu (duyuru, çıkmadı).

## 3. glTF animasyon sıkıştırma sırası
- gltf-transform resample (kayıpsız kare azaltma) → quantize → meshopt. meshopt keyframe ve morph target'ı da sıkıştırır, Draco sıkıştırmaz. gltfpack -cc üçünü birden yapar. Three.js'te MeshoptDecoder. Önce/sonra boyut + kare sayısı loglanır.
- motion/three: Object3D, malzeme, ShaderMaterial ve TSL uniform() değerlerini DOM ile aynı timeline'da yay fiziğiyle sürer (TELVE buhar shader'ı için GSAP'e alternatif).

## 4. 2025-2026 hareket modelleri (kısa; hepsinde ağırlık/veri lisansı ayrıca kontrol)
- SATA (ICML 2026): topolojiden bağımsız latent, metinden hareket + türler arası sıfır-atış retarget, BVH çıkışı → insan dışı rig (dört ayaklı zombi köpek) için ilk aday.
- MoMADiff (anahtar kare güdümlü) · MotionGPT3 · FloodDiffusion (akışlı) · AutoKeyframe + Two-Stage Transformer in-betweening (LAFAN1 → NC) · EDGE (müzik→dans, kod MIT) · SoulDance (veri EULA) · PantoMatrix/EMAGE (ses→yüz+vücut, İngilizce) · AniMo (hayvan, 114 tür) · OpenT2M (2800+ saat açık veri; HumanML3D/Motion-X'te eğitim/test sızıntısı tespit etti).
- ProtoMotions3 (NVIDIA, kod Apache-2.0; SMPL varlıkları ayrı lisans; MuJoCo arka ucu CPU): üretici değil DÜZELTİCİ olarak kullan — kinematik klibi fizik takipçisinden geçirip ayak kayması/gömülmeyi düzelt. Windows'ta yerel çalışma doğrulanmadı (WSL yok).

## 5. Ajanla üretim + doğrulama (skill tasarımını destekleyen çalışmalar)
- 3DHarnessBench (2026): 1 üretim + 3 render-düzelt turu, turda en fazla 3 hata geri bildirimi; Blender 5.1.2 başsız; 512×512 render geri beslenir; Agent Skill + Blender MCP. → bizim tavan: 3 tur.
- 3DCodeBench (Blender 5.0 Python, 212 kategori, 81.605 betik + 2.767 ajan transkripti açık).
- Cutscene Agent (2026): üretimden sonra AYRI doğrulama alt-ajanı zaman çizelgesini tarar, anahtar karede çarpışma testi yapar; ders: araç çağrıları eksiksiz olsa da zamansal tutarlılık garanti değil.
- CodeGen-3D: güçlü model + ucuz öz-düzeltme döngüsü tek seferlik üretimden iyi.

## 6. Sayısal kapılar (8a §8'e ek)
1. Jitter: kanal başına ivme/jerk; medyanın k katını aşan kare oranı eşik üstü → Smooth (Gaussian) F-curve.
2. Gömülme: ayak/el dünya Z'si zemin − tolerans altına inmez.
3. Döngü dikişi: ilk/son kare poz açısal farkı + hız farkı eşik altı.
4. Eklem limiti: dirsek/diz tek eksen + aralık, rig başına JSON.
5. Kök tutarlılığı: in-place klipte kök XZ ≈ 0; root-motion klipte ayak temas fazlarıyla uyumlu.
6. Çarpışma: seyrek karelerde mesh-mesh kesişimi (BVHTree overlap).
7. Roblox ön-kapısı: standart R15 · CurveAnimation (KeyframeSequence değil) · ≤10 s · Jump hariç döngülü · kök başlangıçtan fazla uzaklaşmaz · kare-arası hız sınırı · parça 1,5 stud'dan fazla taşınmaz (animation-packs sayfası; paket 8-9 klip, 80 Robux, günde 1).

## 7. 2D çalışma zamanları
- Spine: runtime'ı yazılıma gömmek için ücretli editör lisansı şart (deneme lisansı runtime hakkı vermez; 500.000 $ gelir eşiği) → KULLANILMAZ.
- DragonBonesJS: MIT (Pixi/Phaser/Three portları); editör ölü; COA Tools (Blender) DragonBones'a aktarır.
- Rive web runtime MIT; editör tescilli.
- Öneri (kendi runtime): Blender kesme rig'inden kemik başına 2D afin dönüşüm dizisini JSON'a pişir → canvas setTransform ile parça sprite çiz. Lisans/bakım riski sıfır.

## 8. Web teknik seçimi
| İhtiyaç | Seçim |
|---|---|
| reveal, ilerleme, hafif paralaks | CSS scroll-driven + @supports (animation-timeline: view()) |
| MPA sayfa geçişi | cross-document View Transitions |
| pin/scrub/3D kamera senkronu | GSAP ScrollTrigger |
| yay fiziği, DOM+Three ortak timeline | Motion (motion/three) |
| tasarımcı vektör animasyonu | Lottie |
| durum makineli etkileşimli ikon/karakter | Rive |
| buhar/sıvı/distorsiyon | Three.js TSL/WebGPU shader |
- Firefox: scroll-driven ve cross-document geçiş desteği kaynaklarda çelişkili → DESTEKLENMİYOR varsay; son hal CSS varsayılanı olsun.
- prefers-reduced-motion: scroll-scrub kamera yerine statik kare/kısa geçiş; paralaks ve otomatik oynatma kapalı.

## 9. Roblox
- Studio Animation Capture: .mp4/.mov videodan R15 gövde anahtar kareleri + yüz yakalama (ücretsiz, hazır).
- Yol haritası (Late 2026, duyuru): prompt-to-animation, animasyon grafiklerinde motion matching, FBX/GLTF yeniden içe aktarma, Open Cloud API'lerinin MCP istemcilerinden (Claude Code dahil) çağrılabilmesi, sprite/flipbook.
- Hat: Blender R15 rig → klip → §6.7 kapısı → FBX → Studio import → Roblox Studio MCP ile doğrulama.
- NoCapMocap / UGCraft: kapalı ücretli servis, yalnız referans.

## 10. Yeni skill/araç adayları (ANİM-1 lisans kapısından geçecek)
- ra100/blender-claude-plugin (8 skill; animation-rigging, 5.1 Gaussian smooth, ~45 constraint, IK/FK, NLA; resmi Blender MCP entegrasyonu) · kevinbadi/blender-skills (ürün turntable, logoya zoom kamera iş akışı) · sambena/autorig-workbench (başsız auto-rig, GPL-3.0) · 4onstudios/AutoTPose (GLB/FBX → rig + T-poz) · Mesh2Motion (tarayıcıda insan/dört ayaklı/kuş rig → GLB) · freshtechbro/claudedesignskills · 199-biotechnologies/motion-dev-animations-skill (MIT) · corevider/meshy-threejs-skill (Meshy ücretli → RED).

## 11. Yüz
- NVIDIA Audio2Face-3D: SDK açık (Samples Apache-2), ağırlıklar NVIDIA Open Model License; çıktı ARKit ağırlıkları; göz bakışı, dil ve kafa kanalları HEP 0 → göz kırpma/bakış/kafa prosedürel katman şart; girdi mono 16 kHz PCM. Türkçe kalite doğrulanmadı. QtMeshEditor'da entegrasyon açık iş (#1019).
- MediaPipe Face Landmarker: 478 nokta + 52 blendshape + kafa matrisi, Apache-2.0, ~4 MB, CPU/tarayıcı. VIPER Blender eklentisi Rigify yüz rig'ine gerçek zamanlı aktarır.

## 12. VRAM'e göre yol (HY-Motion dışındaki değerler tahmini, ölçülecek)
| VRAM | Yol |
|---|---|
| 8 GB | kütüphane + motion matching + prosedürel · MediaPipe yüz · Mesh2Motion · ağır modeller Colab/Kaggle'da → BVH |
| 12 GB | + MoMask/MDM sınıfı, EMAGE, Audio2Face-3D yerel, ProtoMotions MuJoCo (CPU) |
| 16 GB | + SATA, MoMADiff, EDGE, Kimodo (öneri 16 GB+) |
| 24 GB | + HY-Motion 1.0 (24-26 GB, sınırda) |

## 13. ANİM hattı — ilk 20 mekanizma
Faz 1 araç: (1) anim-export: glTF → resample → meshopt + log · (2) mm-lite (Three.js MM + inertialization) · (3) kök hareket çıkarıcı · (4) üst/alt gövde maske + additive üretici · (5) lisans etiketli klip kütüphanesi · (6) BVH içe aktarma + retarget + T-poz normalleştirme · (7) Audio2Face-3D → shape key yazıcı · (8) MediaPipe webcam yüz → 52 kanal → Blender · (9) Colab/Kaggle şablonu → BVH · (10) 2D afin JSON pişirici + canvas oynatıcı.
Faz 2 skill: (11) anim-gate-numeric · (12) anim-gate-visual (kontak sayfası + 3 tur) · (13) anim-validator-subagent · (14) anim-procedural-blender (sürücü, Noise/Cycles, Follow Path, GN simülasyon) · (15) anim-scroll-camera (+ reduced-motion dalı) · (16) anim-web-decide (§8) · (17) anim-roblox (§6.7) · (18) anim-license-guard (§1) · (19) anim-face (A2F + prosedürel göz/kafa) · (20) anim-physics-fix (deneysel, ProtoMotions).

## Güvenli / riskli (ticari müşteri işi)
- Güvenli: Quaternius CC0 · CMU (ürün içinde) · 100STYLE (atıflı) · AIST++ anotasyon · kendi çekimimiz · prosedürel/elle · gltf-transform, MediaPipe, ProtoMotions kodu · DragonBonesJS, Rive runtime · Audio2Face-3D SDK (ağırlık lisansı okunacak).
- Riskli: AMASS/HumanML3D/SMPL(-X) ve bunlarla eğitilmiş ağırlıkların çıktısı · LAFAN1 türevleri · ZeroEGGS · Bandai-Namco · Motorica · SoulDance verisi · Spine runtime · kapalı ücretli servisler (NoCapMocap, UGCraft, Meshy).
