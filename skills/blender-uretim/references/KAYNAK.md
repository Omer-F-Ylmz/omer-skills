# Kaynak ve lisans — bpy-teknik.md, varlik-hatti.md

İki MIT lisanslı depodan bizim tarif yaklaşımına (spec JSON → tek headless koşu → özet JSON) uyarlanarak damıtıldı. Metin Türkçe yeniden yazıldı, kısa alıntı dışında kopya yok. Yerel klon incelendi, içindeki betikler çalıştırılmadı.

## A — MartinRapcan/blender-claude-skill
- URL: https://github.com/MartinRapcan/blender-claude-skill
- Commit: `964cfe73bb1d15ff5b1603c625ecf067fb8d11bc`
- Lisans: MIT, `Copyright (c) 2026 Martin Rapčan`
- Uyarlanan (dosya → bizim dosya):
  - `blender/SKILL.md` (iş akışı, headless çalıştırma, belirti→neden tablosu) → `bpy-teknik.md` "Betik iskeleti", "Render" son madde
  - `blender/references/gotchas.md` → `bpy-teknik.md` "Betik iskeleti ve tuzaklar" (sürüm kırıkları, bağlam/referans tuzakları, ölçek)
  - `blender/references/geometry.md` → `bpy-teknik.md` "Geometri" (join/boolean/parent, remove_doubles, normal, kapalılık, modifier sırası)
  - `blender/references/materials.md` → `bpy-teknik.md` "Malzeme" (soket adları, renk uzayı, UV, malzeme indeksi)
  - `blender/references/lighting.md` → `bpy-teknik.md` "Işık ve dünya" (güç birimleri, HDRI, görünüm dönüşümü)
  - `blender/references/rendering.md` → `bpy-teknik.md` "Render" (motor, örnek, kamera, çıktı, dışa aktarım adları)
  - `blender/references/animation.md` → `bpy-teknik.md` "Animasyon" (kare aralığı, fcurve, sürücü, kısıt, armatür, shape key, animasyon render)
  - `blender/references/objects_2d.md` → `bpy-teknik.md` "2B nesneler"
- Kod: `blender/scripts/boilerplate.py` kopyalanmadı; yalnız fikirleri (temiz sahne, yetim temizliği) anlatıldı.
- Alınmayan: Eevee-NEXT sabit varsayımı (tarif.py'deki motor yedeği ve 5.x notu geçerli); `action.fcurves` kodu (4.4+/5.x katmanlı action ile uyumsuz olabilir, B ile çelişkisi işaretlendi); uzun kod örnekleri (tarif.py ve diğer referanslar zaten kapsıyor); "render al ve bak" döngüsü (bizde sayısal kapı + tek görünüm sayfası, blender-oturum).

## B — elithril/blender-kiln
- URL: https://github.com/elithril/blender-kiln
- Commit: `f30581780804ff9893c2fe7e44ece5f453ccb6d8`
- Lisans: MIT, `Copyright (c) 2026 Nicolas Dolphens`
- Uyarlanan (dosya → bizim dosya):
  - `plugin/references/topology-rules.md` → `varlik-hatti.md` "Topoloji" (kural, bütçe, decimate, LOD)
  - `plugin/references/naming-conventions.md` → `varlik-hatti.md` "Adlandırma" (önekler, glTF ad eşlemesi, klasör)
  - `plugin/references/uv-materials.md` → `varlik-hatti.md` "UV ve malzeme" (dikiş, texel, doku çözünürlüğü, ORM)
  - `plugin/references/texturing-strategy.md` → `varlik-hatti.md` "Doku stratejisi" (bölge analizi, GLB'de kalan/kaybolan harita, fırınlama)
  - `plugin/references/export-targets.md` → `varlik-hatti.md` "Dışa aktarım" (eksenler, GLB/FBX/USDZ, Draco/meshopt/KTX2)
  - `plugin/references/cli-tools.md` → `varlik-hatti.md` "Dışa aktarım" (gltf-transform sırası, gltfpack LOD)
  - `plugin/references/validation-checklist.md` → `varlik-hatti.md` "Temizlik ve doğrulama kontrol listesi"
  - `plugin/references/sourcing-strategy.md` → `varlik-hatti.md` "Kaynak bulma" (Poly Haven/Sketchfab lisans, ToS)
  - `plugin/references/characters.md`, `plugin/references/animation.md` → `varlik-hatti.md` "Animasyon ve karakter özü" (T-poz, rig yoğunluğu, iskelet adları)
  - `plugin/references/reference-fidelity.md` (§1, §3, §6) → `varlik-hatti.md` "Referans sadakati"
  - `plugin/SKILL.md` (Iron Rules 10, 14-26, GN apply kuralı, FBX/USDZ ayarı, bağlam) → ilgili bölümler
- Alınmayan ve nedeni:
  - `ai-generation.md`, `setup-install.md`: ücretli/yerel GPU/ağ üretimi, tarif dışı ("Tarife sığmayan iş").
  - `batch-mode.md`: çok MCP turlu otonom döngü, tarife sığmaz.
  - `reference-fidelity.md` §2, §4-5 (piksel ölçüm betikleri, doku örnekleme, shipped-file ölçümü): bizde `kontur_profil.py` karşılığı var; uzun betikler alınmadı.
  - MCP araç tablosu, `/kiln` komutları, durum kutuları, UniMate/quadruped araçları: bizim blender-oturum ve onay akışımızla çakışır.
  - `site/`, `bench/`, `examples/`, `docs/`, `tools/`: kapsam dışı bırakıldı.
- Kod: B'den kod kopyalanmadı; API çağrı adları (ör. `export_scene.fbx` ve `wm.usd_export` bağımsız değişkenleri) olgu olarak aktarıldı.

## Lisans metni (MIT)
İki depoda metin aynıdır (yalnız telif satırı farklı); atıf şartı gereği ikisi de burada:

```
MIT License

Copyright (c) 2026 Martin Rapčan   (A: MartinRapcan/blender-claude-skill)
Copyright (c) 2026 Nicolas Dolphens (B: elithril/blender-kiln)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Notlar
- Çelişki: `tarif.py` `export_apply=True`, B kural 18 `False` önerir (Array/Mirror); tarifte Array/Mirror yok, bu yüzden korundu (varlik-hatti.md "Dışa aktarım").
- Poly Haven ToS, UniMate (CC BY-NC 4.0) ve Hunyuan3D lisans kısıtları B'den aktarıldı, ayrı kaynakta doğrulanmadı.
