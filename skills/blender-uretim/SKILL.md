---
name: blender-uretim
description: "Blender'da 3D ürün üretimi: fincan/cezve modelle, ışıkla, malzeme kur, render al, GLB'yi web'e hazırla; blender-oturum ile yükle. 3DMigoto, three.js kodu, 2D görsel değil."
---

# blender-uretim — Blender'da güzel ve kanıtlı üretim

Orkestra: akışı, sırayı ve kalite kapısını bu skill yönetir. Oturum (aç · kaydet · kapat) ve araç komutları
**blender-oturum**'dadır; önce onu yükle, oradaki kurallar burada tekrarlanmaz.

Referanslar (gerektiğinde oku): `C:\Projeler\omer-skills\skills\blender-uretim\references\`
- `olculer.md` — kahve nesneleri gerçek boyut tablosu (mm)
- `isik-profilleri.md` + `isik_kur.py` — ışık profilleri ve kurulum fonksiyonları
- `malzemeler.md` + `malzemeler.py` — malzeme tarifleri
- `donel-model.md` — silüetten Screw, kulp/ağız/sap
- `web-aktarim.md` — export, pişirme kararı, AgX eşleme, three.js tarafı

Tablolarda **kaynak** sütunu: `#no` = docs/kaynak-tarama/7-blender.md kaynağı · video id = docs/video-tarama/2026-10-01-toplu.md · `öneri` = kaynaksız, bizim varsayılanımız. İkisi karıştırılmaz; öneriyi kaynak gibi sunma.

## Akış (sıra değişmez)

1. **Brief** — nesne, kullanım (render · web · ikisi), referans görsel, malzeme, ışık profili, teslim biçimi. Eksik madde varsa sor; varsayma.
2. **Ölçü** — gerçek boyutu `references/olculer.md`'den al. Tablo dışı nesnede ölçüyü brief'ten ya da bulunan kaynaktan al, **uydurma**; kaynak yoksa sor. Birim metre (Blender), tabloda mm.
3. **Adlandırma** — her veri bloğu öneki taşır:

| önek | ne | kaynak |
|---|---|---|
| GEO- | mesh nesne/veri | öneri |
| MAT- | malzeme | öneri |
| LGT- | ışık ve ışıyan düzlem | öneri |
| CAM- | kamera | öneri |
| TEX- | görüntü/doku | öneri |
| WLD- | world | öneri |
| SCN- | sahne, compositing grubu | öneri |

4. **Sahne = kod** — sahne betiği `C:\Users\pc\Desktop\<Proje>\blender\sahneler\<ad>.py`'ye yazılır, göndermeden önce `tools/bpy_kontrol.py <betik.py>` temiz geçer.
   - Canlı oturum: betiğin **içeriği** `execute_blender_code`'a doğrudan gönderilir. exec/eval/importlib ile dosya çalıştırma yok — bekçi reddeder.
   - Headless: `tools/blender_cli.py` ile koşturulur (SONUC JSON sözleşmesi).
   - Tur içinde betik **düzenlenir**, sıfırdan yazılmaz (#12).
5. **Aşamalar** — her aşama sonunda `tools/blender_dogrula.py <blend>` exit 0; değilse sonraki aşamaya geçme.

| # | aşama | ne yapılır | referans | kaynak |
|---|---|---|---|---|
| 1 | blokaj | gerçek ölçülü kaba hacimler, pivot tabanda, ölçek uygulanmış | olculer.md | #8 #11 |
| 2 | kamera | CAM-Ana; ön/3-4 kadraj, kamera uzaklığı bbox'tan | — | #12 |
| 3 | ışık | profil seç → `isik_kur.kur(profil, boyut_m)` | isik-profilleri.md | #1 |
| 4 | form | dönel gövde Screw, kulp/sap/ağız ayrı | donel-model.md | Q4 |
| 5 | malzeme | `malzemeler.kur(ad)`; dış malzeme NodeToPython ile okunur | malzemeler.md | #19 |
| 6 | detay | bevel (modifier + shader), DOF, ölçülü compositing | isik-profilleri.md | ZYk3OOf-gBk, 4Uy2SzB-Kuk, wySOWP-MevI |
| 7 | render | turlarda Workbench; son tur Eevee kahraman; teslim Cycles + denoise | — | #10 #1 · 4Uy2SzB-Kuk |
| 8 | dışa aktarım | transform_apply → glTF +Y → `--glb` geri okuma → glb_hat | web-aktarim.md | #4 #8 |

6. **Eleştiri döngüsü** (biçim → görünüş; sayısal kapı her turun önünde)
   - Biçim turları: `tools/blender_gorunum.py <blend> [--referans on.png]` → 4 Workbench görünüm sayfası tek Read (#10 #11). Son tur: Eevee kahraman görünüm.
   - Her tur: eleştiri **madde listesi** yaz (1 madde = 1 somut kusur + düzeltme). Düzeltmeden sonra her madde için tek tek `evet/hayır uygulandı` teyidi (#12). Teyitsiz madde açık sayılır.
   - Referans varsa silüet IoU (araç çıktısı); öneri eşik ≥ 0.90 + bbox oranı ±%3 (#1 eşik vermiyor → öneri).
   - **En fazla 3 tur.** İki tur üst üste IoU artışı < 0.02 ya da açık madde sayısı azalmıyorsa dur → DUR raporu (ne denendi · ölçümler · açık maddeler) (#12 tavan vermiyor → öneri).
7. **Kanıt paketi olmadan bitti yok** — `blender_dogrula` exit 0 çıktısı · görünüm sayfası (son tur) · kahraman render · eleştiri listesi evet/hayır tablosu · web işinde `--glb` geri okuma + glb_hat çıktısı. Biri eksikse "bitti" deme.

## API disiplini

- Düğüm girişi/özniteliği yazmadan önce **canlı sorgu**: `[i.name for i in node.inputs]`, `obj.bl_rna.properties` ya da `get_python_api_docs`. Soket adları sürümle değişir ("Specular" → "Specular IOR Level", #12). `isik_kur.soket()` tutmayan adda mevcut adları listeleyerek durur.
- Hata mesajı gelince `search_api_docs` ile **hata metniyle yeniden sorgula**; tahminle ikinci deneme yapma (#2 #6 #12).
- Canlı oturum yokken .blend denetimi: Lab MCP `*_for_cli` araçları (ör. `get_blendfile_summary_missing_files_for_cli` → mutlak/eksik yol) (#7).
- API kataloğu gerekiyorsa (ör. ~373 Geometry Nodes, ~95 shader düğümü listesi) ra100 skill'leri; kurulu değilse `search_api_docs` (#2).

## Kurallar

- Varlık yalnız CC0 ve kaynak kaydıyla: `tools/varlik_indir.py` (Poly Haven / ambientCG) (#6).
- GPU'yu kullanan iki iş aynı anda koşmaz (gpu_kilit; blender_pisir ve gorsel_uret alır).
- Işık profili belirsizse `urun` + HDRI dolgu 0.3 (#1).
- Yansıma pişmez, HDRI'de kalır; dönen üründe yalnız AO pişer (web-aktarim.md).
- Workbench görüntüsü ölçeği/pivotu/topolojiyi kanıtlamaz; önce sayısal kapı (#8).
