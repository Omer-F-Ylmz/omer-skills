# Blender üretim araçları (BLENDER-ARAC-2 · 1 Eki 2026)

Kaynak: docs/kaynak-tarama/7-blender.md Q2–Q5 + Faz 1 (1 NodeToPython · 2 Poly Haven · 5 headless pişirme · 7 kontur→profil).
KARAR: görüşten bağımsız olan (diffuse, AO) pişer, görüşe bağlı olan (yansıma) HDRI'de kalır. Dönen ürünlerde yalnız AO
pişer. Varlıklar yalnız CC0 kaynaktan ve kaynak kaydıyla gelir. GPU'yu kullanan iki iş aynı anda koşmaz.

araç kanıt alanı: Desktop\blender-kum (kalıcı; .blend'ler Desktop\blender-kum\blender\, varlıklar \varlik\)

## Araçlar
| araç | ne | neden |
|---|---|---|
| `tools/gpu_kilit.py` | %TEMP%\gpu-kilit.json {pid, is, baslangic}; ölü PID kilidi düşer | ComfyUI + Cycles aynı anda VRAM'i boğar |
| `tools/varlik_indir.py` | Poly Haven (hdri/doku/model) + ambientCG (doku) ara/indir | CC0, kaynak kaydı, özet doğrulaması |
| `tools/blender_pisir.py` | Apply Scale → UV2 LightMap → Cycles bake → denoise → PNG/EXR | web'de ışık/AO ücretsiz (Q3) |
| `tools/kontur_profil.py` | silüet → profil zinciri → Screw modeli + IoU öz-doğrulama | dönel ürün tek görselden (Q4) |
| NodeToPython 4.2.0 | malzeme ağacı → .py tarif | UI'da kurulan malzeme tekrar üretilebilir (Q5) |

## Dört ölçüt (araç değerlendirme)
- **gpu_kilit** — bakım: stdlib, ~90 satır · CC'de çift mi: hayır (9876 kontrolü yalnız Blender oturumunu görür) · izin: %TEMP% tek dosya · context: 1 satır mesaj · mekanizma: dosya kilidi + OpenProcess/GetExitCodeProcess (`os.kill` Windows'ta süreci öldürür).
- **varlik_indir** — bakım: stdlib urllib · çift: hayır (MCP yok) · izin: ağ okuma + yalnız `Desktop\<Proje>\` yazma (`proje_ici`) · context: tek JSON satırı · mekanizma: api.polyhaven.com `/info` + `/files` (md5 + boyut) · ambientCG `/api/v2/full_json?include=downloadData` (özet yok → boyut).
- **blender_pisir** — bakım: blender_cli sözleşmesi · çift: hayır · izin: kaynak .blend salt-okunur, çıktı aynı klasöre · context: SONUC JSON · mekanizma: `bpy.ops.object.bake` + geçici sahnede compositor Denoise (render katmanı yok, kamera gerekmez).
- **kontur_profil** — bakım: PEP 723 `uv run` betiği (opencv-python-headless Apache-2.0, numpy) · çift: hayır · izin: .blend `yol_gecerli` · context: JSON (zincir) · mekanizma: kontur + bant-medyan eksen + Screw/Subsurf/Solidify + blender_gorunum IoU.
- **NodeToPython** — bakım: extensions.blender.org güncellemesi · çift: hayır · izin: Blender eklentisi (dosya yazma izni bildirir) · context: tarif dosyada kalır · mekanizma: `scene.ntp_material_slots` + `bpy.ops.ntp.export()` SCRIPT → clipboard.

## Ayrıntılar
- **Pişirme**: UV1 render kanalı korunur, UV2 "LightMap" tek atlas (smart_project ada payı 8/boyut + bake taşması 4 px). isik = DIFFUSE direct+indirect (renk yok), ao = AO. PNG'de p99.9 → 0.9'a ölçeklenir; JSON'daki `lightMapIntensity` three.js'te geri çarpar. `--hdr` EXR (ölçek 1). Cihaz OPTIX→CUDA→HIP→ONEAPI→CPU. Kanıt: zemin + küp + area, 1024², OPTIX, 2.7 sn, lightMapIntensity 7.48 → `Desktop\blender-kum\blender\pisir-kanit-isik.png`.
- **Kontur**: `--kulp sag|sol|yok`; eksen = üst/alt %15 bantlarındaki satır orta noktalarının medyanı (kulp bandı dışı); profil kulpsuz yarıdan; IoU referansı kulpsuz gövde maskesi (aynalanmış), gorunum'un ön ortho çerçevesine (bbox merkezi, 2r·1.05, 512²) oturtulur. Kanıt: kulplu fincan → eksen 299.5 px (hata 0), yükseklik 79.84/80 mm, yarıçap 23.92/24 mm, IoU 0.9897.
- **Varlık**: dosyalar orijinal biçimde (dönüşüm yok; web sıkıştırması glb_hat'ın işi). Poly Haven dokusu `/info.type` ile ayrılır (dokuda da `gltf` anahtarı var). User-Agent repo URL'si taşır, e-posta göndermez. Powered by Poly Haven (polyhaven.com) — her PH .json'ında `not`.
- **NodeToPython**: kurulum belgeden — `blender --online-mode --command extension install -s -e node_to_python` (docs.blender.org/manual/en/latest/advanced/command_line/extension_arguments.html). Lisans GPL-3.0-or-later; README notu: üretilen kod Blender Python API'sine (GPL) dayanır, uyumlu kullanım kullanıcının sorumluluğu → tarifler repo'ya girmez, proje klasöründe kalır. Headless (`-b`) `ntp.export` clipboard'a boş yazar (ölçüldü) → dışa aktarım canlı oturumda `execute_blender_code`; tarifin yeniden kurulumu headless (`blender_cli`, boş sahne): 4 düğüm / 3 bağlantı = 4 / 3. Bekçi `exec` ve değişkenli `open()` yolunu reddeder (koruma çalıştı) → tarif MCP'de değil, headless koşturulur.
- **Desktop salt-okur (K6)**: Desktop config'e CC ile aynı giriş (`C:\blender_mcp\mcp\.venv\Scripts\blender-mcp.exe`, doğrudan başlatma, env yok). Eşzamanlılık: Blender açık + CC bağlıyken ikinci istemciden 2× `get_objects_summary` yanıt aldı, CC'nin sonraki `execute_blender_code` çağrıları bozulmadı; `mcp_kurutest --config desktop blender` OK (26 araç). Salt-okurluk sunucuda değil: araçlar readOnly ipucu taşır, Desktop yazan araçlarda onay sorar. Desktop'u yeniden başlatınca görünür. Yedek: `claude_desktop_config.json.bak-blender-arac-2`.
