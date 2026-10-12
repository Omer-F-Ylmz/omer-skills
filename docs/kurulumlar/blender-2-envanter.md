# BLENDER-2 aday envanteri (2026-10-12)

Yöntem: yalnız okuma. Yıldız/lisans/son push `gh api repos/...` ile, sürüm `pypi.org/pypi/<ad>/json` ile bugün alındı; fiyat/kota sayfaları HTTP GET ile. Hiçbir şey kurulmadı, ücretli çağrı yok. `?` = doğrulanamadı. Token etkisi ölçülmedi; "tahmin" = mekanizmadan çıkarım. Daha önce kapsanan: `docs/kurulumlar/blender-arastirma.md`, `docs/kaynak-tarama/7,9` (burada yalnız özet + yeni bulgu).
Windows sütunu: evet = PyPI win_amd64 tekerleği / saf Python / HTTP; `?` = denenmedi.

## Tablo

| ad | ne kazandırır | token etkisi | lisans | bakım (son commit) | Windows | bizde çifti | karar |
|---|---|---|---|---|---|---|---|
| [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) ★30,5k | Tek MCP: Poly Haven aramaktan indirmeye, canlı bpy API sorgusu, güvenli mod env; Sketchfab/Hyper3D/Hunyuan köprüleri (README okunmadı ?) | 36 araç şeması her oturumda yüklenir (kaynak-tarama/7 #6) | MIT | 2026-10-06 | ? | Lab MCP + blender-mcp 1.0.3 + blenderwright | RED: 4 CVE, kimliksiz soket, varsayılan telemetri, keyfi bpy+ağ (docs/kurulum-blender.md:17). İyi yanı (Poly Haven akışı) varlik_indir'e UYARLA ile alındı |
| [bpy-dev/blender-mcp](https://github.com/bpy-dev/blender-mcp) ★98 | Lab MCP'nin bağımsız dağıtımı | aynı | GPL-3.0 | 2026-09-12 | ? | Lab MCP | RED: yeni değer yok, GPL fork |
| [dcc-mcp/dcc-mcp-blender](https://github.com/dcc-mcp/dcc-mcp-blender) ★45 | Çok-DCC ailesi (model/UV/rig/render) | MCP şema yükü | MIT | 2026-10-12 | ? | blenderwright 191 araç | RED: ikinci araç seti, headless belirtilmemiş |
| [VxASI/blender-mcp-vxai](https://github.com/VxASI/blender-mcp-vxai) ★300 | ahujasid türevi | şema yükü | MIT | 2025-03-21 | ? | blender-mcp | RED: 19 aydır durgun |
| [seehiong/blender-mcp-bridge](https://github.com/seehiong/blender-mcp-bridge) ★66 · [sandraschi/blender-mcp](https://github.com/sandraschi/blender-mcp) ★57 | MCP köprüleri (içerik okunmadı ?) | şema yükü | MIT · MIT | 2026-09-13 · 2026-10-09 | ? | blender-mcp | RED: üçüncü/dördüncü MCP, okunmadan eklenmez |
| [Higgsfield Blender](https://higgsfield.ai/plugins/blender) | Zip eklenti + uzak MCP köprüsü `bridge.higgsfield.ai/mcp`; sahne/3B/video üretimi Higgsfield kredisiyle | ? (uzak sunucu araç listesi 170, video 2qM93WXeKdY) | kapalı ürün ? | ? | ? | hiçbiri (3B üretim yok) | REF: hesap+kredi ister; adaylar/higgsfield-eklentisi-mcp.md'de SOR'da bekliyor |
| [elithril/blender-kiln](https://github.com/elithril/blender-kiln) ★42 | fidelity_check + audit + Draco/WebP export kalıbı, sayısal kapı | yüksek (tahmin): görsel yerine sayı döner | MIT | 2026-10-12 | ? | blender_dogrula + glb_hat | UYARLA: kapı eşikleri/ölçüler; depo kurulmaz |
| [MartinRapcan/blender-claude-skill](https://github.com/MartinRapcan/blender-claude-skill) ★2 | boilerplate.py + gotchas.md (hata önleme listesi) | orta (tahmin): yeniden deneme turu azalır | MIT | 2026-08-11 | ? | blender-uretim tarif.py | UYARLA: yalnız gotchas, atıfla |
| [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) ★89 | ışık tablosu + çok-görünüm silüet IoU döngüsü | orta | MIT | 2026-05-01 | ? | blender_gorunum + blender_dogrula | UYARLA (7. rapor #1); 30 skill kurulmaz |
| [ra100/blender-claude-plugin](https://github.com/ra100/blender-claude-plugin) ★19 | Claude eklenti kalıbı | ? | MIT | 2026-04-29 | ? | blender eklentimiz 1.0.0 | REF |
| [nutti/fake-bpy-module](https://github.com/nutti/fake-bpy-module) ★1,8k (PyPI 20261011) | bpy tip taslağı; betik Blender açılmadan tip/API hatası verir | yüksek (tahmin): deneme-hata turu azalır | MIT | 2026-08-09 | evet (saf Python, pip) | yok | KUR (yalnız dev bağımlılığı, Blender'a yüklenmez) |
| [bpy (PyPI 5.2.2)](https://pypi.org/project/bpy/) | Blender'sız `import bpy`; CI/test ve MCP'siz tek süreç | token yok; MCP/soket yok | GPL-3.0 | 2026-09-15 | evet (cp313 win_amd64) | `blender -b` (5.2.1) | REF: sürüm 5.2.2≠5.2.1 sapması; yerel Blender zaten headless |
| [DLR-RM/BlenderProc](https://github.com/DLR-RM/BlenderProc) ★3,7k | headless render hattı, kamera örnekleme, JSON çıktı sözleşmesi | orta | GPL-3.0 | 2026-01 (önceki rapor) | ? | pisir + tarif.py | REF: yalnız çıktı sözleşmesi fikri |
| [al1brn/geonodes](https://github.com/al1brn/geonodes) ★157 | GN'yi Python sınıflarıyla kurar | yüksek (satır sayısı) | yok | 2026-09 (önceki rapor) | ? | NodeToPython | RED: lisanssız (lisans kapısı); fikir = kendi `nodes.new/links.new` sarmalayıcımız |
| [Blender-Geonodes-AI-Toolkit-](https://github.com/Roman-Software-1/Blender-Geonodes-AI-Toolkit-) ★1 | GN + AI iddiası (içerik okunmadı ?) | ? | MIT | 2026-06-16 | ? | NodeToPython | RED: ★1, okunmadan eklenmez |
| [KhronosGroup/glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO) ★1,7k | Yerleşik glTF dışa aktarıcı; `export_*` seçenek belgesi | orta: doğru seçeneği ilk seferde yazdırır | Apache-2.0 | 2026-10-10 | evet (Blender içinde) | glb_hat | REF: seçenek adları için |
| [donmccurdy/glTF-Transform](https://github.com/donmccurdy/glTF-Transform) ★2k | CLI: optimize/dedup/prune/resample/simplify/palette tek komut | düşük: tek satır komut | MIT | 2026-10-06 | ? (Node) | glb_hat (meshopt+webp) | REF: glb_hat'ta olmayan adımları (dedup/prune/instance) karşılaştır |
| [zeux/meshoptimizer](https://github.com/zeux/meshoptimizer) ★8,5k | meshopt sıkıştırma/simplify, gltfpack | — | MIT | 2026-10-09 | ? | glb_hat içinde | REF: zaten var |
| [google/draco](https://github.com/google/draco) ★7,5k | Geometri sıkıştırma | — | Apache-2.0 | 2026-10-09 | ? | meshopt | RED: ikinci codec/decoder çalışma zamanı gerekmez |
| [KTX-Software](https://github.com/KhronosGroup/KTX-Software) ★1,4k · [basis_universal](https://github.com/BinomialLLC/basis_universal) ★3,1k | KTX2/UASTC: GPU'da sıkışık doku (WebP yalnız indirme boyutunu küçültür, VRAM'i değil — genel bilgi, ölçülmedi) | — | NOASSERTION (okunmadı ?) · Apache-2.0 | 2026-10-12 · 2026-09-01 | ? | webp | UYARLA (koşullu): yalnız VRAM/mobil hedef çıkarsa; KTX lisansı okunmadan kurulmaz |
| [blender-asset-tracer](https://pypi.org/project/blender-asset-tracer/) | .blend bağımlılık izleme/paketleme (pack, dış doku yolları) | düşük | ? | PyPI 2026-10-08 | ? | yok | REF: dış doku yolu sorunu çıkarsa; GitHub'da resmi depo bulunamadı |
| [trimesh](https://github.com/mikedh/trimesh) ★3,7k · [CadQuery](https://github.com/CadQuery/cadquery) ★5,9k | Blender'sız mesh doğrulama/boolean · parametrik CAD → STEP/GLB | yüksek (tahmin): Blender başlatma yok | MIT · NOASSERTION (okunmadı ?) | 2026-10-02 · 2026-10-10 | ? | blender_dogrula | REF: Blender gerektirmeyen mekanik parçada |
| [BlenderKit / Blendkit](https://www.blenderkit.com/plans/pricing/) | 73k ücretsiz + Full Plan 152k varlık, eklenti içinden | hesap+GUI | GPL-2.0 eklenti; varlık lisansı karışık | 2026-10-08 | evet (resmi liste) | varlik_indir (CC0) | RED: karışık lisans, ücretli katman; (önceki rapor) |
| [Sketchfab Download API](https://sketchfab.com/developers/download-api) | 1M+ ücretsiz CC modeli, glTF/GLB indirme | düşük: JSON+indirme, görsel yok | CC (çoğu ticari serbest; BY/NC karışık) | canlı | evet (HTTP) | varlik_indir (polyhaven/ambientcg) | UYARLA: varlik_indir'e kaynak ekle, lisans süzgeci (yalnız CC0/CC-BY) + atıf kaydı; API token ister |
| [sketchfab/blender-plugin](https://github.com/sketchfab/blender-plugin) ★1,3k | GUI eklenti: ara/indir/yükle | GUI | Apache-2.0 | 2026-09-10 | ? | — | RED: GUI; API betikle yeter |
| [Poly Haven API](https://polyhaven.com/our-api) | Artık ticari dahil ücretsiz; CC0; toplu indirme izinli | düşük | CC0 | canlı | evet (HTTP) | varlik_indir | REF: bizde var; "canlı API'ye atıf isteği" cümlesi kesik okundu ? |
| [extensions.blender.org API](https://extensions.blender.org/api/v1/extensions/?type=add-on&page_size=1) | Eklenti keşfi JSON ile (sürüm, arşiv_hash, boyut) | düşük: HTML yerine JSON | eklentiye göre | canlı | evet (HTTP) | yok | UYARLA: oturum'da eklenti arama alt komutu; CLI kurulum yolu doğrulanmadı ? |
| [Tripo API + SDK](https://docs.tripo3d.ai/get-started/pricing.html) · [tripo-python-sdk](https://github.com/VAST-AI-Research/tripo-python-sdk) ★60 | Metin/görsel → mesh; 1 USD = 100 kredi; görsel modeli 20–50 kredi; SDK betikten | düşük: çıktı = dosya yolu | SDK MIT; ticari koşul sayfada net değil ? | 2026-07-01 | evet (PyPI tripo3d) | yok | UYARLA: tek-koşu sarmalayıcı, "en fazla N varlık" tavanı şart; ücretsiz kredi ? |
| [tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp) ★212 | Tripo MCP | şema yükü | MIT | 2025-04-14 | ? | — | RED: durgun, SDK betiği yeter |
| [Meshy API](https://www.meshy.ai/api) | Metin/görsel → 3B, auto-rig; MCP Server + CLI var (yeni) | MCP şema yükü; CLI düşük ? | ücretsiz plan CC BY 4.0 (önceki rapor); API Pro+ | canlı | ? | yok | RED-şimdilik: API ücretli plana bağlı; CLI/MCP içeriği okunmadı ? |
| [Hyper3D Rodin](https://hyper3d.ai/) · [rodin-integration](https://github.com/DeemosTech/blender-mcp-rodin-integration) ★5 | Kaliteli PBR mesh; Blender köprüsü | tarayıcı köprüsü | ticari lisans Business planda (önceki rapor) · MIT | 2026-05-21 | ? | — | RED: pahalı ticari plan, GUI'ye bağlı |
| [Hunyuan3D-2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) ★4,2k | Yerel açık ağırlıklı 3B | yerel | NOASSERTION; AB/BK/G.Kore hariç, 1M MAU sınırı (9. rapor) | 2025-10-17 | ? | — | RED: lisans bölge/ölçek kısıtlı |
| [TRELLIS.2](https://github.com/microsoft/TRELLIS.2) ★11,9k | Tek görselden PBR 3B, yerel; Claude jetonu harcamaz | süreç çağrısı | MIT (ağırlık lisansı ?) | 2026-07-10 | ? (12 GB VRAM sınırda, 9. rapor) | yok | KUR-sonra: GPU kilidi + tek ağır süreç şartı |
| [Stable Fast 3D](https://github.com/Stability-AI/stable-fast-3d) ★1,9k | Görselden doku+UV'li mesh, hızlı (makale iddiası) | yerel | Stability Community: yıllık gelir <1M USD serbest, üstü kurumsal lisans (HF kartı); HF'te onay kutusu | 2025-01-22 | ? | — | REF: TRELLIS.2 daha yeni; HF hesap+onay ister |
| CSM (csm.ai) | Görsel/metin → 3B | ? | ? | ? | ? | — | RED-şimdilik: fiyat sayfası okunamadı (`csm.ai/pricing` boş döndü), MCP ? |
| [agmmnn/awesome-blender](https://github.com/agmmnn/awesome-blender) ★7,4k | Eklenti/araç listesi | liste okuma (kaynak) | CC0-1.0 | 2026-01-22 | — | — | REF: "KONU için aday" taramasında kaynak |
| [AxiomeCG/awesome-threejs](https://github.com/AxiomeCG/awesome-threejs) ★1k | three.js kaynak listesi (glb sonrası tüketici) | — | CC0-1.0 | 2026-07-28 | — | — | REF |
| [MrNeRF/awesome-3D-gaussian-splatting](https://github.com/MrNeRF/awesome-3D-gaussian-splatting) ★8,9k · [awesome-3d-diffusion](https://github.com/cwchenwang/awesome-3d-diffusion) ★1,3k | 3B üretim/splat literatürü | — | MIT · MIT | 2026-10-04 · 2026-01-16 | — | — | REF: 3B-AI adayı çıkarken tara; tek "awesome-3d" kanonik listesi bulunamadı |
| [SunzeY/awesome-blender-script](https://github.com/SunzeY/awesome-blender-script) ★32 | bpy betik listesi | — | ? | 2024-08 | — | — | RED: 2 yıl durgun |

## Ömer hesap listesi

| site | ücretsiz kota | neden |
|---|---|---|
| sketchfab.com (API token) | token ücretsiz (kota sayısı okunmadı ?) | Download API ile varlik_indir kaynağı |
| platform.tripo3d.ai (API anahtarı) | ön ödemeli, 1 USD=100 kredi; ücretsiz kredi ? | tek-koşu 3B üretim (tavan şart) |
| huggingface.co (hesap + lisans onayı) | ücretsiz | SF3D (gated) / TRELLIS.2 ağırlıkları |
| meshy.ai | ücretsiz plan var, API Pro+ | yalnız Meshy CLI/MCP yeniden bakılırsa |
| blenderkit.com / higgsfield.ai | ücretsiz plan / kredi | önerilmiyor; karar paneli beklerse |
| polyhaven.com, ambientcg, extensions.blender.org | hesap gerekmez | — |

## İlk 5 öneri
1. **fake-bpy-module KUR** (MIT, pip, dev bağımlılığı): API hatası Blender açılmadan yakalanır.
2. **Sketchfab Download API → varlik_indir** (UYARLA): CC0/CC-BY süzgeci + atıf kaydı; token Ömer'den.
3. **blender-kiln fidelity/audit + blender-claude-skill gotchas** (UYARLA, MIT, atıfla): sayısal kapı, yeniden deneme azalır.
4. **glTF-Transform `optimize` ↔ glb_hat karşılaştırması** (REF): eksik dedup/prune/instance adımını tek ölçümle bul.
5. **TRELLIS.2 yerel** (KUR-sonra, MIT) veya **Tripo SDK sarmalayıcı** (UYARLA, N-tavanlı): 3B üretim jetonsuz.

Durum (d4 12 Eki): 1 yapıldı (dev grubunda pinli). 3 yerine kendi `beklenen` ölçü kapımız (yalin.tek, ±%15; tek ×10 10/10). 4 kapandı:
glb_hat zaten `gltf-transform optimize` koşuyor (dedup/instance/prune/weld/simplify varsayılan açık) + meshopt + webp; telve.glb 56→14.3 KB, validate 0 hata —
ek adım yok. KTX2: toktx/basisu kurulu değil; webp web için yeterli, GPU bellek sorunu görülünce `--texture-compress ktx2` (KTX-Software lisansı okunacak).
2 Ömer'in Sketchfab token'ını bekliyor; 5 GPU/ücret kararı Ömer'in.

## Notlar / doğrulanamayanlar
- blender-mcp eklentimiz port 9876 kullanıyor; bu ahujasid/blender-mcp'nin varsayılan soket portu. Eklentinin kaynağı ahujasid ise RED gerekçesi (kimliksiz soket, telemetri) eklenti için de geçerli olabilir: doğrulanmadı, ayrıca kontrol edilmeli.
- Sürüm sapması: PyPI bpy 5.2.2, yerel Blender 5.2.1.
- Okunmayanlar: ahujasid README (araç listesi), KTX-Software/CadQuery LICENSE, seehiong/sandraschi/Geonodes-AI-Toolkit içeriği, Meshy MCP/CLI, CSM, Higgsfield lisansı, tüm Windows `?` satırları.
- Video raporlarında (`docs/video-tarama`, 116 dosya) blender geçen ve burada yeni çıkan tek araç Higgsfield; BlenderKit/Tripo/Lab MCP zaten kapsanmış.
