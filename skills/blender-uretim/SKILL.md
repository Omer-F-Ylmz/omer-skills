---
name: blender-uretim
description: "Blender'da 3D ürün üretimi: fincan/cezve modelle, ışıkla, malzeme kur, render al, GLB'yi web'e hazırla; blender-oturum ile yükle. 3DMigoto, three.js kodu, 2D görsel değil."
---

# blender-uretim — Blender'da ürün üretimi rehberi

Rehber: zorunlu akış yok; ölçü, ad, teslim tanımı ve referanslar yeter. Oturum (aç · kaydet · kapat) ve araç
komutları **blender-oturum**'dadır; önce onu yükle, oradaki kurallar burada tekrarlanmaz.

Referanslar — v1 tesliminden önce yalnız `olculer.md` okunur; ışık `isik_kur.kur("urun")`, malzeme `malzemeler.kur(ad)` ile kurulur (md okunmaz). Teslimden sonra gerektiğinde: `C:\Projeler\omer-skills\skills\blender-uretim\references\`
- `olculer.md` — kahve nesneleri gerçek boyut tablosu (mm)
- `isik-profilleri.md` + `isik_kur.py` — ışık profilleri; `isik_kur.kur(profil, boyut_m)`
- `malzemeler.md` + `malzemeler.py` — malzeme tarifleri; `malzemeler.kur(ad)`
- `donel-model.md` — silüetten Screw, kulp/ağız/sap
- `web-aktarim.md` — export, pişirme kararı, AgX eşleme, three.js tarafı

`#no` = docs/kaynak-tarama/7-blender.md kaynağı · `öneri` = kaynaksız varsayılanımız; öneriyi kaynak gibi sunma.

## Ölçü ve ad

- Gerçek boyut `references/olculer.md`'den. Tablo dışı nesnede ölçüyü brief'ten ya da bulunan kaynaktan al, **uydurma**; kaynak yoksa sor. Birim metre (Blender), tabloda mm.
- Veri bloğu öneki (öneri): GEO- mesh · MAT- malzeme · LGT- ışık/ışıyan düzlem · CAM- kamera · TEX- görüntü/doku · WLD- world · SCN- sahne/compositing.

## Sahne = kod

- Betik `C:\Users\pc\Desktop\<Proje>\blender\sahneler\<ad>.py`; göndermeden önce `tools/bpy_kontrol.py <betik.py>` temiz geçer. Turda düzenlenir, sıfırdan yazılmaz (#12).
- Canlı oturum: betiğin **içeriği** `execute_blender_code`'a; exec/eval/importlib ile dosya çalıştırma yok (bekçi reddeder). Headless: `tools/blender_cli.py` (SONUC JSON).
- Diskte kopya yalnız `bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)`. `bpy.data.libraries.write` ile Scene yazma: Blender 5.2.1'de çöküyor, bekçi reddeder.

## Teslim

Teslim = kahraman render (brief çözünürlüğü, Cycles + denoise) + GLB + `tools/blender_dogrula.py <blend> --glb <glb>` exit 0.
- Sıra: render → GLB dışa aktarımı (transform_apply → glTF +Y) → `blender_dogrula --glb`. İlk teslim bu üçü olmadan bitmez; üçü bitmeden ikinci render yok.
- Kapı geçmezse en fazla 2 düzeltme; sonra DUR raporu (ne denendi · çıktı · açık madde).
- Teslimde bir kez: `tools/blender_gorunum.py <blend> [--referans on.png]` görünüm sayfası, tek Read.
- **Durma kuralı:** v1 teslim + kapı geçtiyse en fazla 1 iyileştirme turu (teslimi yeniden üretir), sonra dur ve raporla: teslim yolları · dogrula çıktısı · açık maddeler.
- Eleştiri turları (≤3; madde listesi + evet/hayır teyidi; referansta silüet IoU ≥ 0.90 öneri) yalnız kullanıcı isterse.

## Görüntü disiplini

- Kendi kontrol render'ın ≤512 px (Workbench/Eevee); kontrol görüntülerine en fazla 3 Read.
- Tam çözünürlük yalnız teslim render'ında.
- Workbench görüntüsü ölçeği/pivotu/topolojiyi kanıtlamaz; önce sayısal kapı (#8).

## API disiplini

- Düğüm girişi/özniteliği yazmadan önce **canlı sorgu**: `[i.name for i in node.inputs]`, `obj.bl_rna.properties` ya da `get_python_api_docs`. Soket adları sürümle değişir ("Specular" → "Specular IOR Level", #12). `isik_kur.soket()` tutmayan adda mevcut adları listeleyerek durur.
- Hata mesajı gelince `search_api_docs` ile **hata metniyle yeniden sorgula**; tahminle ikinci deneme yapma (#2 #6 #12).
- Canlı oturum yokken .blend denetimi: Lab MCP `*_for_cli` araçları (ör. `get_blendfile_summary_missing_files_for_cli` → mutlak/eksik yol) (#7).
- API kataloğu gerekiyorsa (ör. ~373 Geometry Nodes, ~95 shader düğümü listesi) ra100 skill'leri; kurulu değilse `search_api_docs` (#2).

## Kurallar

- `get_objects_summary` yalnız ≤10 nesneli sahnede; üstünde hedefli bpy sorgusu (ad · boyut · malzeme).
- Araç argümanı için kod aranmaz; blender-oturum'daki komut kartına bakılır.
- Varlık yalnız CC0 ve kaynak kaydıyla: `tools/varlik_indir.py` (Poly Haven / ambientCG) (#6).
- GPU'yu kullanan iki iş aynı anda koşmaz (gpu_kilit; blender_pisir ve gorsel_uret alır).
- Işık profili belirsizse `urun` + HDRI dolgu 0.3 (#1).
- Yansıma pişmez, HDRI'de kalır; dönen üründe yalnız AO pişer (web-aktarim.md).
