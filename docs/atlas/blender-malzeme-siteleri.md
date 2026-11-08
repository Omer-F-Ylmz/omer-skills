---
type: katalog
status: active
tags: [blender, 3d, malzeme, doku, hdri, ucretsiz]
relatedTo: [site-3d, blender-uretim]
---
# Ücretsiz Blender / 3D malzeme siteleri (30 Eki, LINK-30EKI-NOTLAR satır 25)

HTTP 200 ölçüldü (30 Eki). Sayılar API'den (Poly Haven, ambientCG); diğerlerinde sayı ölçülmedi. Lisans sütunu sitenin kendi beyanıdır, indirmeden önce varlık sayfasında doğrula.

| site | ne | lisans (beyan) | not |
|---|---|---|---|
| polyhaven.com | 869 doku · 521 model · 997 HDRI | CC0 | API `api.polyhaven.com/assets?t=` ; `varlik_getir.py` zaten kullanır; Blender eklentisi var |
| ambientcg.com | 2927 PBR malzeme/HDRI/model | CC0 | API `ambientcg.com/api/v2/full_json` |
| blenderkit.com | model·malzeme·fırça·sahne | ücretsiz katman royalty-free, ücretli katman var | Blender eklentisi, hesap gerekir |
| sketchfab.com (ücretsiz model filtresi) | karışık model | varlık başına CC türü değişir | CC BY ise atıf zorunlu |
| poly.pizza | düşük poligon model | CC0 / CC-BY karışık | oyun/hafif sahne |
| quaternius.com | düşük poligon paketler | CC0 | oyun varlığı |
| kenney.nl/assets | oyun varlık paketleri | CC0 | curl 403 verdi (bot engeli), tarayıcıyla açılır |
| opengameart.org | oyun varlıkları | varlık başına değişir | karışık lisans |
| 3dtextures.me · sharetextures.com · cgbookcase.com · freepbr.com · texturecan.com | PBR doku | çoğu CC0 (site beyanı) | doku odaklı |
| blendswap.com | .blend dosyaları | CC türleri | hesap gerekebilir |
| itch.io/game-assets/free | oyun varlıkları | karışık | proje başına lisans oku |

## Kullanım sırası
1. Önce yerel `varlik_getir.py ara` (Poly Haven + ambientCG + Objaverse).
2. Yoksa BlenderKit eklentisi / Sketchfab CC0 filtresi.
3. Ticari işte CC-BY ve karışık lisanslarda atıf notu raporda; CC-NC kullanılmaz.
