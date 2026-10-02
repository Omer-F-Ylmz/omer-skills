# 8a — Animasyon bilgi tabanı (Desktop araştırması, 2026-10-01)

İki tur web araştırması (~40 arama). Kod yok; mekanizma + sayı + kaynak. KAYNAK-TARAMA-ANİM bunu taban alır: burada olanı yeniden araştırmaz, yalnız lisans/README/sürüm doğrular ve "öneri" işaretli eşikleri sınar. Sayılar kaynaktan; kaynakta olmayanlar "öneri" diye işaretli.

## 1. Zanaat: ilkeler, zamanlama, iş akışı
- 12 ilke (Thomas & Johnston): zamanlama/aralık · ezme-uzatma · hazırlık · sahneleme · düz-ileri / pozdan-poza · devam eden ve örtüşen hareket · yavaş giriş-çıkış · ark · ikincil hareket · abartı · sağlam çizim · çekicilik. 3D'de: ezme-uzatma rig deformasyonuyla, ark Graph Editor + motion path ile, örtüşme parça anahtarlarını kaydırarak.
- Bloklama: varsayılan enterpolasyon Constant (pozdan-poza; eğri ara kareleri yanıltmasın). Sert temas karelerinde tutamaçlar sıfıra (keskin dönüş), temiz ark için Auto Clamped. Kaynak: CG Cookie "Make It Move in Blender 5.2".
- Aralık: hızlanma/yavaşlama = uç karelerde sık, ortada seyrek kare. Hızlı hareketin arkı daha düz. Motion path: geçmiş kırmızı, gelecek yeşil.
- Yürüme döngüsü (24 fps): adım başına 12 kare, tam döngü 24 kare (iki adım). Dört poz eşit aralıkla: temas · aşağı (kalça en alçak) · geçiş · yukarı (kalça en yüksek). Temas kareleri 1-13-25; 25 = 1 olduğundan render/dışa aktarımda son kare tekrar edilmez.
- Döngü uzunluğu tablosu (24 fps, tam döngü): 8 çok hızlı koşu · 12 koşu/çok hızlı yürüyüş · 16 yavaş koşu/çizgi film yürüyüşü · 24 doğal · 32 gezinti · 40 yaşlı/yorgun · 48 çok yavaş. 30 fps'de doğal yürüyüş 30-40 kare.
- Hata teşhisi: "havada süzülüyor" → aşağı pozu sığ; "fazla ağır" → geri tepme-geçiş arası kısalt. Döngü: Graph Editor Cycles modifier (Cycle with Offset, öncesi/sonrası).
- Kaynak: animschool blog walk-cycle · bluehawk.monmouth.edu (Williams yöntemi tablosu) · anim.works/walk-cycle · mocaponline walk-cycle.

## 2. Blender 5.x teknik tuzaklar (kod bekçisi + skill)
- Slotted action 4.4'te geldi; 5.0'da eski API silindi: action.fcurves, action.groups, action.id_root YOK. Yol: bpy_extras.anim_utils.action_ensure_channelbag_for_slot(action, slot) → channelbag.fcurves.new/ensure(data_path, index, group_name). Okuma: action_get_channelbag_for_slot. Eski dosyalar tek "Legacy Slot" ile yükseltilir. (developer.blender.org 5.0 Python API)
- Katmanlı animasyon arayüzde hâlâ yok; toplamalı katman NLA'da ya da motorda.
- glTF: 4.4'ten beri NLA track'ler adla değil kullandıkları action'la birleşir; slotted action doğrudan dışa aktarılır, NLA ad hilesi gereksiz; sahne animasyonu hep bake edilir. 5.2: glTF'e EXT/KHR_meshopt_compression. 5.0: C++ FBX içe aktarıcı varsayılan, Collada kaldırıldı, Python 3.13 (eklentiler yeniden derlenmeli). (cinevva "Blender 5 for game artists", 4.4 Pipeline & I/O notları)
- Grease Pencil v3 (4.3+): çizgiler frame.drawing.strokes üstünden; eski gpencil API'li örnekler kırılır.
- 5.2 animasyon: döngü/sektirme oynatma modu · Object Mode'da in-between · Dope Sheet'te türe göre seçim · Ctrl+L "Copy Constraints" · kemik "Duplicate and Rename" · GN XPBD kumaş/saç · Sample Sound Frequencies (sese tepkili animasyon). 5.3 (geliştirme): anim.rotation_mode_convert.
- Her MCP kod çağrısı yeni namespace: nesnelere kalıcı adla eriş (öneri önekler: ARM- · ACT- · CAM- · CTL-). (RobLe3/cc-blender-skill mekanizması)
- Kamera: anahtarları kameraya değil üst Empty'ye koy; web'de kameraya ek sallama/fare paralaksı eklenebilir. (three.js forum)

## 3. Hareket kaynakları
| Yol | Araç | Gereksinim / not |
|---|---|---|
| Kütüphane | Quaternius UAL 1+2 | 250+ klip, CC0, evrensel insan rig'i, Mixamo uyumlu; UAL2: kombo saldırı, parkur, zombi yürüyüşü |
| Kütüphane | Mixamo | Adobe ID ile ücretsiz, telifsiz ticari; tek başına yeniden dağıtılamaz; bakım modunda, yalnız T-poz insan |
| Kütüphane | QtMeshEditor eğitim külliyatı | CC0/CC-BY klipler (HF: fernandotonon/QtMeshEditor-motion-corpus) |
| Metin→hareket | NVIDIA Kimodo (+ MMCP) | Blender 5 eklentileri (Xingxun7777 · atticus-lv · lewdineer · animatica proscenium); RTX, 16 GB+ VRAM önerisi, ~50 GB disk, HF girişi (LLaMA-3-8B kodlayıcı); 77 eklem SOMA → FBX SDK ile dosya seviyesinde retarget (Blender rest-pose kalça titremesini önlemek için) |
| Metin→hareket | Tencent HY-Motion 1.0 | 1B / Lite 0.46B; en az 26 / 24 GB VRAM; ücretsiz Kaggle P100 defteri; zysilm/hy-motion-fbx-exporter tek komutla Mixamo FBX; lisans bölge kısıtlı (AB/İngiltere/G.Kore hariç) |
| Metin→hareket | QtMeshEditor t2m | yalnız izinli veriyle (CMU + Quaternius) sıfırdan eğitim, ONNX, şablon klip + ayak temas IK sabitleme |
| Video→hareket | FreeMoCap (AGPL, çok kamera) · Mocapy (video/webcam → BVH + yüz morph dosyası) · GVHMR (tek kamera) · QtMeshEditor webcam/video + ARKit yüz · QuickMagic / Rokoko Vision (web, ücretsiz katman) | GVHMR zor videoda ayak kayması ~%29 → temizlik şart |
| Görüntü→video (2D klip) | Wan 2.2 TI2V-5B (Apache-2.0, ComfyUI offload ile ~8 GB) · LTX-2.3 (ses+video, 16 GB+) | 3D değil; site arka planı, sosyal klip; gorsel-uret hattına eklenir |
- Ders (QtMeshEditor araştırması): AMASS/HumanML3D ticari değil → izinli önceden eğitilmiş ağırlık yok denecek kadar az; kaliteyi veri + retarget matematiği belirliyor.

## 4. Rig ve retarget
- Rig: Rigify (yerleşik, 5.2'de var) · AccuRIG 2.0 (Windows, ücretsiz) · Mixamo autorig · UniRig / SkinTokens-TokenRig (HF Space) · QtMeshEditor (UniRig ONNX CLI/MCP + tek tık ARKit 52 yüz rig'i).
- Retarget: "Retarget" eklentisi (Expy Kit + AnimAide çatalı, yalnız Blender 5+, Mixamo/Unreal/VRoid/MMD/Daz/ARP hazır ayarları, kök hareket aktarımı, GPL) · Mixaify (Mixamo→Rigify, Blender 5, FK; IK'ye Rigify FK→IK) · Kimodo FBX SDK retarget.

## 5. İkincil hareket ve simülasyon
- Yay kemik: Wiggle Bones (Wiggle 2 refaktörü, 5.0 düzeltmeli, GPL) · Jiggle Physics (verlet; render'da kendini kapatır → bake şart) · EXea Jiggle (katman sistemi, 5.x). Hepsi "bake to keyframes" ile motora gider.
- Simülasyonu web/oyuna taşıma = VAT: OpenVAT · "VAT" eklentisi (extensions.blender.org/add-ons/vat; WebGPU için VAB) · manthrax/three-vat çalışma zamanı · QtMeshEditor `qtmesh vat`. Kurallar: önce Bake All Dynamics · Z-up→Y-up · doku RGB16 · sert kenarları ayır · köşe sayısı sabit kalmalı.

## 6. Yüz ve dudak senkronu
- Rhubarb Lip Sync CLI: 9 ağız şekli, TSV/JSON çıktı; İngilizce için PocketSphinx, diğer dillerde phonetic tanıyıcı (Türkçe → phonetic). Eklentiler: Rhubarb Lip Sync NG (4.2+, shape key + pose) · LipKit (2D GP + 3D) · "Lip Sync" eklentisi (Charley3D, 25+ dil, GPL — Türkçe desteği doğrulanacak).
- ARKit 52 blendshape: QtMeshEditor yüz rig'i + yüz yakalama.

## 7. Teslim adaptörleri
- three.js: nesne başına bir AnimationMixer, mixer.update(delta) · geçiş crossFadeTo · toplamalı: AnimationUtils.makeClipAdditive · kaydırmayla oynatma: action duraklat + mixer.setTime(), GSAP ScrollTrigger proxy'si; birden çok nesne ayrı ayrı sürülecekse ayrı mixer · çalışma zamanı IK: CCDIKSolver · prosedürel: kurulu threejs-procedural-animation (ZATEN VAR).
- Sinematik web sekansı: Theatre.js (@theatre/core Apache-2.0 pakete girer; @theatre/studio AGPL yalnız geliştirmede).
- Web UI hareketi: GSAP resmi 8 skill · Motion AI Kit (`npx motion-ai`, mcp.motion.dev ücretsiz, hesapsız) · Remotion skill'leri (video).
- Lottie: LottieFiles Creator MCP (hesap) · diffusionstudio text-to-lottie · Blender "Lottie Export" (GP → Lottie/dotLottie/TGS, 5.1+) · glaxnimate Python (başsız SVG→Lottie, GIF render) · python-lottie.
- Rive: resmi MCP (Rive Early Access editörü açık olmalı, 127.0.0.1:9791) · virodeveloper/rive-mcp (editörsüz).
- Sprite (Efsun/Bakkalım): Sprite Sheet Maker eklentisi (5.1+, isteğe bağlı pikselleme) · 8 yön render.
- Roblox: Studio MCP animation aracı (read/preview/build) · ThatGuyTHD/animation-mcp · Cautioned/Blender-Animations-Plugin (Blender↔Roblox rig/animasyon, 4.2-5.x) · FBX'te Bake Animation.

## 8. Kalite kapıları (sayısal)
- Ayak kayması oranı: ayak temas hâlindeyken (yükseklik < 5 cm) karede > 2,5 cm kayan kare yüzdesi (bazı çalışmalar 2 cm). Referans: işaretli mocap ~%6, GVHMR zor videoda ~%29, temizlik sonrası ~%5.
- Ayak çakışması: iki ayak arası < 5 cm. Yüzme/batma: en alçak eklem ile zemin arası. Titreme: ivme istatistiği.
- Döngü dikişi: son kare = ilk kare (öneri eşik: kemik başına < 0,5° ve kök < 1 mm).
- Görsel: kontak sayfası (RobLe3 animation-quality-gate) + oyun kamerasından render + döngü dikişi ve olay zamanı kontrolü (majidmanzarpour/blender-game-skills).
- Öneri kapı (insan yürüme/koşu): ayak kayması ≤ %8 · titreme başlangıç klibinden kötü değil · döngü dikişi geçer · kontak sayfasında ark kırığı yok.

## 9. Lisans haritası (ticari müşteri işi)
- Serbest: kendi keyframe/prosedürel · Quaternius CC0 · Mixamo (proje içinde) · kendi mocap çekimimiz (araç lisansı ≠ çıktı; FreeMoCap AGPL — tarama doğrulasın) · Wan 2.2 Apache-2.0 · Theatre core Apache · GSAP/Motion/Remotion skill'leri (Remotion şirket lisansını kurulumda kontrol et).
- Dikkat: HY-Motion (Tencent topluluk lisansı) · Kimodo ağırlıkları (NVIDIA Open Model License — metin okunacak) · AMASS/HumanML3D/SMPL tabanlı modeller (çoğu ticari değil) · Cascadeur ücretsiz (ticari değil, FBX yok) · spine-animation-ai (PolyForm NC).
- GPL eklentiler (Wiggle, Retarget, Lip Sync, Sprite Sheet Maker vb.): iç kullanım serbest; kodları ürüne gömülmez.
- Manifest alanları (öneri): kaynak · lisans · ağırlık lisansı · fps · döngü · kök hareketi · rig · etiket · kontrol sonuçları.

## 10. Öğrenme kaynakları (VİDEO-TARAMA adayı)
- CG Cookie "Make It Move in Blender 5.2" · Pierrick Picaut (oyun animasyonu/rig) · CGDive (rig, oyuna aktarım; addons.cgdive.com eklenti dizini) · Grant Abbitt · Dikko · CrossMind Studio (hareketli grafik) · Blender Studio "Humane Rigging" (eski sürüm). Kitaplar (ad, içerik değil): The Illusion of Life · The Animator's Survival Kit.

## 11. ANİM hattına alınacaklar
Faz 1 (araç): GPU ölçümüne göre hareket kaynağı yönlendirici · tek ortak rig + Retarget eklentisi · anim_kontrol (ayak kayması, çakışma, titreme, döngü dikişi) · kontak sayfası (Workbench, oyun kamerası) · anim-kutuphane + manifest · glTF çok klip + meshopt · VAT · sprite · Lottie export · Rhubarb · yay kemik bake · QtMeshEditor CLI/MCP denemesi (telemetri kapalı).
Faz 2 (skill `animasyon`): ilke kontrol listesi · zamanlama tabloları · Blender 5.x kalıpları + yasak kalıplar · teslim adaptörü seçimi · lisans kuralı · kanıt kapısı.
Kanıt koşusu: zombi yürüyüşü + TELVE kamera/fincan hareketi + Lottie ikon, skill'siz/skill'li.
