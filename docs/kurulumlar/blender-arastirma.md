# BLENDER-1 Faz 2 araştırması (2026-10-11)

Yöntem: yalnız okuma (gh api, WebFetch/WebSearch); hiçbir şey kurulmadı/indirilmedi/çalıştırılmadı; paralı API çağrısı yok. Yıldız/push/lisans `gh api repos/...` ile 2026-10-11'de alındı. `kaynak-tarama/7` ve `9` bulguları tekrarlanmadı (orada olan: RobLe3, ra100, blendops, ahujasid, Lab MCP, blend-ai, harveyxiacn, PatrykIti, ozanzeng, NodeToPython-fikri, Pixal3D/TRELLIS.2, Hunyuan3D RED, UniRig/Puppeteer DENE).

## Özet (5 satır)
1. En değerli yeni bulgu: `MartinRapcan/blender-claude-skill` (MIT) tam bizim mimari (headless `--background --factory-startup --python`, tek koşu) ve `elithril/blender-kiln` (MIT, Claude Code eklentisi) ölçülü maliyet verisi veriyor (varlık başına ~$3.8-7.8 API eşdeğeri; GLB 32.9 MB → 0.96 MB).
2. MCP araç şemaları pahalı: blenderwright 191 araç ≈ 48k jeton/istek (kendi README'si); çözüm headless betik + `auto`/`core` araç seti; biz MCP'yi hiç yüklemeyip betik kitaplığına gidiyoruz.
3. Jeton kazancı bpy tarafında: geonodes için `al1brn/geonodes` (lisanssız → RED/fikir), `fake-bpy-module` (MIT) yalnız tip ipucu için; NodeToPython (GPL-3) ile üretilen tarifler, "harici araç" olarak.
4. AI 3D: ücretsiz katman ticari kullanıma uygun değil (Tripo ücretsiz = ticari değil; Meshy ücretsiz = CC BY 4.0 atıflı; Rodin ücretsiz = sınırlı). Yerel TRELLIS.2 (MIT) tek temiz yol; API'ler yalnız ön ödemeli ve tavanlı.
5. Animasyon: Rigify (yerleşik, GPL add-on) + UniRig (MIT) + glTF-Blender-IO (Apache); mocap için lisanslar kısıtlı (GVHMR lisansı belirsiz, FreeMoCap AGPL, BlendArMocap GPL) → harici süreç olarak.

Not: Blender add-on'larının GPL olması doğaldır (bpy GPL'dir). GPL kod projeye kopyalanmaz; "UYARLA" = fikir/mekanizma yeniden yazılır, "HARİCİ" = kurulu araç olarak çağrılır, kopyalanmaz.

## 1. Blender MCP / skill / eklenti / CLI / ajan depoları

Jeton etkisi sütunu: MCP aracı sayısı ve görüntü dönüşü = her istekte şema yükü; headless = çıktı yalnız metin.

| aday | ne kazandırır | jeton etkisi | lisans | karar | kaynak |
|---|---|---|---|---|---|
| MartinRapcan/blender-claude-skill (★2, 2026-08) | Claude'a sağlam headless bpy betiği yazdırır: boilerplate.py, geometri/malzeme/ışık/animasyon/render/gotchas referansları; `--background --factory-startup --python scene.py` | En düşük: yalnız md skill, MCP yok, ekran görüntüsü yok; referanslar ihtiyaçta okunur | MIT | UYARLA: `references/gotchas.md` + `scripts/boilerplate.py` kalıbı bizim kütüphanenin başlığı olur (MIT, atıfla kopyalanabilir); olgunlaşmamış (★2) → doğrudan kurma | https://github.com/MartinRapcan/blender-claude-skill |
| elithril/blender-kiln (★42, 2026-10-09) | Claude Code eklentisi: metin/foto → üretim hattı (A/B fazları), fidelity_check.py (render ↔ foto IoU), audit, Draco+WebP sıkıştırma; MCP ve headless betik geçişi bayt-bayt aynı çıktı | Ölçümlü: 5 varlık $5.82-7.81, tek varlık $3.80-6.13 (API eşdeğeri); GLB 3.9 MB → 0.75 MB; eskisi için sıfırdan sahnelenmiyor | MIT | UYARLA (fikir): fidelity_check + audit + export sıkıştırma kalıbı; eklentinin kendisi MCP+Hunyuan3D istiyor → kurma | https://github.com/elithril/blender-kiln |
| sandraschi/blender-mcp (★56, 2026-10-09) | Headless FastMCP: araçların çoğu `blender --background` alt süreci; ihtiyaç halinde canlı köprü; VSE/geonodes/export | 41 "portmanteau" araç (150+ işlem) → şema orta-büyük; çıktı headless | MIT | ÖĞREN: "araç başına headless/oturum ezme" ve hands-in/hands-out tablosu; kurma (MCP turu yerine betik kararımızla çelişir) | https://github.com/sandraschi/blender-mcp |
| HoldMyBeer-gg/blenderwright (★168, 2026-10-08; blend-ai'nin yeni adı olabilir, 9. raporda "blend-ai 175 araç") | 191 araç, 28 modül, `auto_critique_workflow` (ne zaman ekran görüntüsü, jeton bütçesi); araç seti seçimi `BLENDERWRIGHT_TOOLSETS=auto/core` | Tüm araç ≈ 48k jeton/istek (README); `auto` ile azalır; görüntü base64 döner | MIT | ÖĞREN: toolset/lazy-enable mekanizması ve görüntü-bütçesi kuralı; kurma | https://github.com/HoldMyBeer-gg/blenderwright |
| bpy-dev/blender-mcp (★98, 2026-09-12) | Lab MCP'nin bağımsız dağıtımı: bağımsız bpy, çalışma zamanı API belgesi | Lab MCP ile aynı; yeni değer yok | GPL-3.0 | RED (zaten Lab MCP var; GPL fork) | https://github.com/bpy-dev/blender-mcp |
| dcc-mcp/dcc-mcp-blender (★45, 2026-10-10) | Model/UV/rig/malzeme/render; çok-DCC ailesi | MCP şema yükü; headless belirtilmemiş | MIT | RED (Lab MCP + betik yeterli, yeni mekanizma yok) | https://github.com/dcc-mcp/dcc-mcp-blender |
| djeada/blender-mcp-server (★30, 2026-09-23) | Claude Desktop için basit MCP | MCP şema yükü | MIT | RED | https://github.com/djeada/blender-mcp-server |
| pranav-deshmukh/blender-mcp (★98, son push 2025-08) | ahujasid türevi | durgun | MIT | RED (bakımsız) | https://github.com/pranav-deshmukh/blender-mcp |
| pflerman/blender-mcp-headless (★1, 2026-07) | Flatpak headless sarmalayıcı | ihmal edilebilir | lisans yok | RED (lisanssız; lisans kuralı) | https://github.com/pflerman/blender-mcp-headless |
| ProfRino/Blender-MCP-Assembly-Skill (★76, 2026-05) | "Güvenilir model" montaj skill'i | md skill | lisans yok | RED (lisanssız); fikir 9. rapordaki ozanzeng ile örtüşür | https://github.com/ProfRino/Blender-MCP-Assembly-Skill |
| HKUDS/CLI-Anything blender/ (★51890, 2026-09-22) | "Her yazılımı ajana CLI yap": `blender/agent-harness` altında bpy tabanlı CLI + SKILL.md | CLI = sıkıştırılmış metin çıktısı; ama genel çerçeve büyük (yüzlerce klasör) | Apache-2.0 | ÖĞREN: yalnız `blender/agent-harness` yapısını oku (komut yüzeyi nasıl daraltılmış); çerçeveyi kurma | https://github.com/HKUDS/CLI-Anything/tree/main/blender |
| Evolink-AI/Awesome-Blender-Seedance-Workflow-Usecases (★342) | Seedance (video) tarif listesi; Blender betiği değil | yok | lisans yok | RED (konu dışı, lisanssız) | https://github.com/Evolink-AI/Awesome-Blender-Seedance-Workflow-Usecases |
| ahujasid/mcp-for-blender (★30456, 2026-10-06) | (7. raporda var) yalnızca teyit: yıldız/push güncel | zaten kayıtlı | MIT | değişmedi (7. rapor: UYARLA mekanizma) | https://github.com/ahujasid/blender-mcp |

## 2. Profesyonel iş akışları: bpy kitaplığı, geometry nodes, headless render/bake, add-on

| aday | ne kazandırır | jeton etkisi | lisans | karar | kaynak |
|---|---|---|---|---|---|
| nutti/fake-bpy-module (★1817, 2026-08) | bpy tip taslakları (kod tamamlama); bizim betik doğrulamasında `py_compile` + tip kontrolü için çevrimdışı API şeması | Orta-yüksek: yanlış API çağrısını Blender açmadan yakalar; her deneme-hata turu (~3-8k jeton) azalır | MIT | KUR (yalnız geliştirme bağımlılığı, pip; Blender'a yüklenmez) | https://github.com/nutti/fake-bpy-module |
| al1brn/geonodes (★157, 2026-09) | Geometry nodes'u Python sınıflarıyla kurar; düğüm bağlantı kodu çok kısalır | Yüksek (GN betik satırı sayısı düşer), ama API ek öğrenme | lisans yok | RED (lisanssız); fikir: kendi ince `gn.py` yardımcımız (`nodes.new` + `links.new` sarmalayıcı) | https://github.com/al1brn/geonodes |
| BrendanParmer/NodeToPython (★364, 2026-08) | Elle kurulan düğüm ağacı → bpy betik (malzeme/GN/compositor); tarif kütüphanesi üretimi | Yüksek: tarif bir kez kurulur, sonra parametreli betik; model yazmaz | GPL-3.0 | HARİCİ (bir kez UI'dan çalıştırılıp çıktı betiği sürüm başlıklı tarif olarak saklanır; üreten add-on projeye kopyalanmaz); 7. raporla uyumlu | https://github.com/BrendanParmer/NodeToPython |
| DLR-RM/BlenderProc (★3739, 2026-01) | Headless prosedürel render hattı (eğitim verisi); `blenderproc run script.py` kalıbı, kamera örnekleme, JSON/HDF5 çıktısı | Orta: headless sözleşme fikri; ana işimiz değil | GPL-3.0 | UYARLA (fikir): kamera örnekleme + çıktı sözleşmesi; kodu kopyalama | https://github.com/DLR-RM/BlenderProc |
| KhronosGroup/glTF-Blender-IO (★1664, 2026-10) | Blender'ın yerleşik glTF dışa/içe aktarıcı kaynağı; `export_*` seçeneklerinin belgesi | Orta: Draco/NLA/animasyon seçeneklerini doğru betiğe yazmak | Apache-2.0 (Blender'a gömülü) | KUR gerekmez (yerleşik); belgesini betik başlığında referans al | https://github.com/KhronosGroup/glTF-Blender-IO |
| Headless bake/render kalıbı (Cycles, `blender -b file.blend -P`, `bpy.ops.object.bake`) | Tek koşuda bake + render; çıktı yalnız dosya + JSON | En yüksek: sıfır görüntü jetonu; kontrol sayısal (IoU/bbox) | GPL (Blender) | UYARLA: 7. rapor madde 5-6 zaten tarif; bizim kütüphanede `bake.py` + `render.py` | https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html |
| Yerleşik add-on'lar: Node Wrangler, Bool Tool, LoopTools, Rigify, Extra Objects | Ek kurulum olmadan modelleme/rig; LoopTools ve Bool Tool operatörleri betikten çağrılır | Düşük-orta | GPL (Blender ile gelir) | KULLAN (yerleşik; kopyalama yok; betikte `bpy.ops` çağrısı) | https://extensions.blender.org/ |
| BlenderKit (kataloğu) | Varlık kütüphanesi; ücretsiz/ücretli karışık | Ağ/hesap gerekir | GPL add-on; varlık lisansları ayrı | RED (varlık lisansı karışık; Poly Haven CC0 zaten 7. raporda) | https://github.com/BlenderKit/BlenderKit |

## 3. AI 3D üretim

Fiyat/kredi verisi üçüncü taraf özetlerinden; resmi fiyat sayfası Tripo için 403 verdi, "doğrulanmadı" olarak işaretlendi. Hiçbir API çağrılmadı.

| aday | ne kazandırır | jeton etkisi | lisans | karar | kaynak |
|---|---|---|---|---|---|
| TRELLIS.2 (microsoft, ★11819, 2026-07) yerel | Tek görselden dokulu PBR 3D; 12 GB VRAM'de sınırda (9. rapor) | Betik dışı: üretim Claude jetonu harcamaz, yalnız süreç çağrısı | MIT (kod; ağırlık lisansı depodan teyit) | KUR-sonra (9. rapordaki ComfyUI yolu; GPU kilidi + RAM bekçisi şartı) | https://github.com/microsoft/TRELLIS.2 |
| TRELLIS (v1, microsoft, ★13890, 2026-06) | Önceki sürüm, daha az bellek | aynı | MIT | ÖĞREN/yedek (TRELLIS.2 12 GB'a sığmazsa) | https://github.com/microsoft/TRELLIS |
| Tripo API + tripo-python-sdk (★60, 2026-07) / tripo-mcp (★212, 2025-04) | Metin/görsel → mesh; quad remesh; resmi Python SDK (betikten çağrılır, MCP gerekmez) | Betikle: çıktı yalnız indirme yolu; MCP gerekmez (tripo-mcp'yi kurma) | SDK MIT; API ön ödemeli, ~$1/100 kredi, ~20 kredi/varlık (yaklaşık $0.20), API çıktısı ticari kullanıma açık (Tripo blog); ücretsiz Studio katmanı ticari değil (kaynaklar çelişiyor); yeni hesap için 2000 kredi hibesi tek kaynakta, DOĞRULANMADI | UYARLA: gerektiğinde SDK'yı betikle çağıran tek-koşu sarmalayıcı, "en fazla N varlık" tavanı şartı; şimdilik kurma (anahtar/ödeme kullanıcıda) | https://github.com/VAST-AI-Research/tripo-python-sdk · https://docs.tripo3d.ai/get-started/pricing.html |
| Meshy | Metin/görsel → mesh; ücretsiz 100 kredi/ay; API Pro ve üstü (ücretsizde belirsiz) | API'siz zayıf | Ücretsiz: CC BY 4.0 (ticari, atıf şartı); ücretli: çıktı sahibi sizsiniz | RED-şimdilik (API ücretli plana bağlı, atıf yükü); ihtiyaç olursa yeniden bak | https://www.meshy.ai/pricing |
| Hyper3D Rodin (Deemos) | Kaliteli mesh/PBR; Gen-2.5 API ~0.5 kredi/üretim; Blender'a RodinBridge add-on (Gumroad $0+, Chrome gerekir) | Add-on tarayıcı köprüsü: otomasyona uygun değil; API = betik çağrısı | Ücretsiz plan sınırlı; ticari lisans net olarak Business (~$120/ay) planında; Shutterstock lisanslı eğitim verisi | RED (ticari lisans pahalı plan; add-on GUI'ye bağlı) | https://hyper3d.ai/ · https://github.com/DeemosTech/blender-mcp-rodin-integration |
| Hunyuan3D 2 / 2.1 (Tencent, ★15068/★4162) | Açık ağırlıklı yerel 3D üretim | yerel | NOASSERTION; 9. rapora göre AB/BK/G.Kore hariç + 1M MAU sınırı | RED (9. raporla aynı) | https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 |
| TripoSG (★1827) | Yalnız şekil, yerel | yerel | MIT | DENE sonra (9. raporda zaten) | https://github.com/VAST-AI-Research/TripoSG |
| Step1X-3D (StepFun, ★897, 2025-09) | Dokulu 3D, açık ağırlık | yerel | Apache-2.0 | DENE sonra (TRELLIS.2 başarısız olursa; 12 GB uyumu doğrulanmadı) | https://github.com/stepfun-ai/Step1X-3D |
| MrForExample/ComfyUI-3D-Pack (★3882, 2025-12) | Çok modelli 3D düğüm paketi (ComfyUI) | yerel | MIT | ÖĞREN (bakım 2025-12'de durgun, TRELLIS.2 yerel Comfy çekirdekte var) | https://github.com/MrForExample/ComfyUI-3D-Pack |
| facebookresearch/sam-3d-objects (★7504, 2026-06) | Görselden nesne 3D | yerel | NOASSERTION (özel lisans) | RED şimdilik (lisans okunmadı → 9. rapor kuralı: lisans belirsiz kurulmaz) | https://github.com/facebookresearch/sam-3d-objects |

## 4. Animasyon: rig, mocap, NLA

| aday | ne kazandırır | jeton etkisi | lisans | karar | kaynak |
|---|---|---|---|---|---|
| Rigify (Blender yerleşik) | metarig → generate; `bpy.ops.pose.rigify_generate()` betikle | Düşük: tek betik, görsel yok | GPL (Blender ile gelir) | KULLAN (betikten; kopyalama yok) | https://docs.blender.org/manual/en/latest/addons/rigging/rigify/index.html |
| UniRig (VAST, ★1820, 2026-06) | Otomatik iskelet + skin ağırlığı; çıktı FBX/GLB, Blender'a aktarılır | Yerel süreç, jeton yok; ≥8 GB VRAM | MIT | KUR-sonra (animasyon fazı; Windows doğrulanmadı — 9. rapor) | https://github.com/VAST-AI-Research/UniRig |
| Puppeteer (Seed3D, ★429, 2025-09) | Rig + animasyon, UniRig'e alternatif | yerel | Apache-2.0 | DENE (UniRig başarısız olursa) | https://github.com/Seed3D/Puppeteer |
| BlendArMocap (cgtinker, ★1087, 2025-12) | MediaPipe ile webcam/video → Rigify iskeletine mocap | Betik içi değil, Blender add-on'u; GUI | GPL-3.0 | HARİCİ (add-on olarak çalıştırılır, kopyalanmaz); video mocap için en doğrudan yol, Rigify gerektirir | https://github.com/cgtinker/BlendArMocap |
| GVHMR (zju3dv, ★2102, 2026-09) | Videodan dünya-hizalı insan hareketi (SMPL); Blender'a aktarım topluluk betikleriyle | GPU süreç, jeton yok | NOASSERTION (LICENSE dosyası 768 bayt; okunmadı, araştırma lisansı olması olası) | RED şimdilik (lisans okunmadan ticari kullanıma sokulmaz; okunursa yeniden değerlendir) | https://github.com/zju3dv/GVHMR |
| FreeMoCap (★10420, 2026-10) | Çok kameralı markersız mocap; Blender çıktısı var | donanım/çoklu kamera gerekir | AGPL-3.0 | RED (AGPL + çoklu kamera donanımı) | https://github.com/freemocap/freemocap |
| NLA betikle (bpy.data.actions + `anim_data.nla_tracks.new()` + `strips.new`) | Hareket kütüphanesi: eylemleri NLA şeritlerine yerleştirip glTF'e `export_nla_strips` ile verir | Düşük: saf betik, 9. rapor vladmdgolam tarifiyle birleşir | GPL (Blender API) | UYARLA: kütüphanede `nla.py` (fikir; kendi kodumuz) | https://docs.blender.org/api/current/bpy.types.NlaTrack.html |
| Mixamo alternatifleri: Cascadeur (ücretsiz katman), Rokoko Studio | Hazır hareket/hareket yakalama | GUI; ajana girmez | Ticari ürün/ücretsiz katman koşulları doğrulanmadı | RED (9. raporda Mixamo/AccuRIG GUI nedeniyle RED; aynı gerekçe) | https://cascadeur.com/ |

## Kur önerileri (en çok 5, en yüksek kazanç önce)

1. **MartinRapcan/blender-claude-skill kalıbı + gotchas.md** (MIT): kütüphanenin başlığı (`boilerplate.py`) ve hata önleme listesi; her koşunun başında MCP yerine tek komut. Atıfla uyarla, depoyu kurma.
2. **nutti/fake-bpy-module** (MIT, pip, yalnız geliştirme): betikler Blender açılmadan tip/API hatası verir; yeniden deneme turu azalır.
3. **elithril/blender-kiln'den fidelity_check + audit + Draco/WebP sıkıştırma kalıbı** (MIT, fikir/uyarla): sayısal kapı + export boyutu ölçüleri; ölçülü maliyet taban çizgisi ($4-6/varlık API eşdeğeri) hedefi için referans.
4. **NodeToPython** (GPL-3, harici araç): malzeme/GN tarif kütüphanesi bir kez UI'dan üretilir; çıktı betikleri sürüm başlıklı parametreli tarif olarak saklanır.
5. **TRELLIS.2 yerel (MIT) + UniRig (MIT)**: AI 3D üretim ve otomatik rig için tek temiz yerel yol; yalnız GPU kilidi + RAM bekçisi ve tek ağır süreç kuralıyla (9. rapor).

Karar özeti: Tripo SDK betikle isteğe bağlı (tavan "en fazla N varlık"); Meshy/Rodin/Hunyuan/GVHMR/FreeMoCap RED; yeni MCP sunucularının hiçbiri kurulmaz (mimari karar).

## Profesyonel iş akışı (Blender 5.2; M = docs.blender.org/manual/en/latest/, A = docs.blender.org/api/current/, CY = intern/cycles/blender/addon/properties.py)
- **Render örnek + denoise (Cycles):** kod varsayılanı samples 4096, adaptive açık, eşik 0.01 (kılavuz aralığı 0.1–0.001), min 0 = otomatik; denoise açık, girdi RGB_ALBEDO_NORMAL, prefilter ACCURATE, kalite HIGH (CY; M render/cycles/render_settings/sampling.html — "en az Albedo"). Kılavuz: Automatic denoiser OIDN'i OptiX'e tercih eder. **Tarife yansıyan:** GPU seçimi (önceden CPU'da kalıyordu; kalite aynı, süre kısa) + adaptive/albedo-normal açıkça (eski .blend ayarı sızmasın); tarif örneği 64 + denoise kalır. Test: test_cycles_gpu_adaptif_denoise.
- **Gürültü:** Filter Glossy (bpy `blur_glossy`) 1.0 başlangıç; caustics "yaygın gürültü kaynağı", yalnız firefly varsa kapat (cam görünümü değişir → tarif varsayılanı değişmedi); Clamp Indirect parlak yerleri kısar (M light_paths.html).
- **EEVEE:** taa_render_samples 64 varsayılan (tarif aynı); raytracing kapalı varsayılan (A SceneEEVEE).
- **Renk:** AgX 4.0'dan beri varsayılan, Filmic kullanımdan kalktı; exposure 0, gamma 1 (release_notes/4.0/color_management, M displays_views.html). Tarif AgX'i zaten sabitliyor.
- **HDRI/varlık:** Environment Texture (equirectangular) ile dünya ışığı (M environment.html); Poly Haven CC0, atıf gerekmez (polyhaven.com/license) → tarif `hdri`. Asset Browser: `ID.asset_mark()` (A bpy.types.ID).
- **Geometry nodes:** modifier + node group; Instance on Points hızlı (veri çoğaltmaz), Realize Instances tek tek düzenleme için (M modeling/geometry_nodes). Tarife alınmadı (tarife sığmayan iş; bpy-teknik.md).
- **Prosedürel malzeme:** Noise (fraktal Perlin), Voronoi (Worley), Wave; Principled girişleri Base Color/Roughness/Metallic/IOR/Coat/Sheen/Transmission/Emission/Subsurface "Weight" alt başlıklı (M principled.html). Mevcut malzemeler.py yeterli; değişmedi.
- **Kamera/kompozisyon:** Composition Guides thirds/golden; F-stop düşük = güçlü alan derinliği, Focus Object mesafeyi geçersiz kılar (M render/cameras.html; A Camera, CameraDOFSettings: fstop 2.8, use_dof kapalı). Tarif `oto` kamera 50 mm + 3/4 açı kalır; DOF ürün netliğini düşürebileceği için varsayılan kapalı.
- **3 nokta ışık:** kılavuzda yok (bulunamadı); ışık birimi W, Area `spread` varsayılan π (A AreaLight). Tarifin isik_kur "urun" profili kaynağı mevcut referansta.

## Doğrulanamayanlar
Tripo resmi fiyat sayfası (403, üçüncü taraf özet); Tripo 2000 kredi hibesi (tek kaynak); GVHMR ve sam-3d-objects LICENSE içeriği (okunmadı); TRELLIS.2 ağırlık lisansı; kiln ve blenderwright'ın Windows'ta çalışması; blenderwright ile blend-ai'nin aynı proje olup olmadığı (depo adı değişmiş olabilir; blend-ai adı gh api'de 404).
