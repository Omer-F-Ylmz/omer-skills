---
name: parsel-video
description: Drone olmadan arsa/parsel tanıtım videosu üretir — il/ilçe/mahalle + ada/parsel (ya da koordinat/GeoJSON) verilince TKGM'den parsel sınırını alır, Esri uydu görüntüsü üstünde parseli işaretler, yaklaşıp dönen kamerayla MP4 çıkarır. Emlak/arsa ilanı, "havadan arsa videosu", "parsel videosu" isteklerinde kullan.
---

# parsel-video

Kaynak: YT Shorts qs-DetJr2nQ (Dolunay Özeren) yöntemi; uç noktalar okansafak/qgistkgmplugin'den doğrulandı.

## Kullanım
```
python scripts/parsel_video.py --il Muğla --ilce Bodrum --mahalle Bitez --ada 204 --parsel 3 --dikey --cikti bitez-204-3.mp4
python scripts/parsel_video.py --latlng 37.03,27.39 --cikti nokta.mp4
python scripts/parsel_video.py --geojson parsel.geojson --sure 12 --aci 180
```
Bayraklar: `--dikey` (1080x1920, Reels/Shorts) · `--sure` sn (8) · `--fps` (30) · `--aci` toplam dönüş derecesi (90) · `--zoom` karo seviyesi (18; büyük arazide 17) · `--baslik` metin · `--mahalle-kodu` biliniyorsa ad aramasını atlar.

## Akış
1. TKGM CBS API: `ilListe.json` → `idariYapi/ilceListe/{il}` → `idariYapi/mahalleListe/{ilce}` → `parsel/{mahalle}/{ada}/{parsel}` (GeoJSON Feature; alan, nitelik). Koordinatla: `parsel/{lat}/{lng}/`.
2. Esri World Imagery karoları (z=18) parselin ~3 katı alanda birleştirilir.
3. Parsel sarı dolgu + kontur, etrafında kesikli halka.
4. Kareler bellekten ffmpeg'e borulanır (diske kare yazılmaz): uzaktan yakına yumuşak zoom + dönüş, alt bantta başlık/alan, "© Esri, TKGM" atfı.
5. Yanına `<cikti>.geojson` kaydedilir.

## Gereksinim
Python 3 + Pillow, ffmpeg PATH'te. Ağ: cbsapi.tkgm.gov.tr, parselsorgu.tkgm.gov.tr, server.arcgisonline.com.

## Notlar
- TKGM günlük sorgu sınırı uygular; aynı parseli tekrar çekmek yerine `--geojson` ile kayıtlı dosyayı kullan.
- Esri görüntüsü atıfla kullanılır; ticari yayın öncesi Esri kullanım şartlarına bak.
- Geliştirme: Remotion/hyperframes ile logo + müzik bindirme, Blender'da DEM ile 3D arazi (blender-uretim).
