# bl — 16 benzersiz kayıt

**Amaç:** Blender 3B iş akışı ajanları: modelleme planı, UV, malzeme, ışık/kamera, render ayarı, doku pişirme, rig, animasyon, headless bpy betiği ve web için GLB dışa aktarım.

**İç yapı:** Tümü [ajan], bl-<konu>; boru hattı sırası: plan/modelleme → uv/malzeme/pişirme → ışık/kamera/render → rig/animasyon → kontrol/temizlik → dışa aktarım.

## En güçlü parçalar
- `bl-python-betik` — Toplu içe aktarma, düzenleme, render ve dışa aktarma için headless bpy betikleri.
- `bl-glb-disa-aktar` — Modeli three.js ve web için küçük GLB olarak hazırlar.
- `bl-gorsel-ani-kontrol` — Ters normal, non-manifold kenar ve eksik dokuları yakalar.
- `bl-render-ayari` — Gürültülü/yavaş render'da Cycles/Eevee, sample ve denoise seçimi.
- `bl-uv-acma` — Dikiş, eşit texel yoğunluğu ve çakışmasız UV; gerilmiş/bozuk pişirmede.
- `bl-dokuya-pisirme` — Yüksekten alçak poligona normal, AO ve renk haritası pişirir.
- `bl-urun-turntable` — Ürün turntable kareleri render edip web döngüsü kurar.
- `bl-malzeme-kurucu` — Roughness, metallic, doku girişli Principled BSDF malzemeler.

## Birlikte kullanım
- bl-modelleme-plani → bl-uv-acma → bl-dokuya-pisirme → bl-glb-disa-aktar.
- bl-isik-kurulumu + bl-kamera-kompozisyon + bl-render-ayari: ürün çekimi.
- bl-glb-disa-aktar çıktısı 3d ailesi ve threejs ailesindeki web sahnelerine girer.
- cli ailesinden blender-dogrulama ile çıktıyı sayısal kapıdan geçirmek.

## Tuzaklar
- bl-mod-modeli-blender ölçek, kemik, vertex group dönüşümü ister; oyun formatları universal-modder ile örtüşür.
- Blender kurulumu ve render süresi/donanım katalog metninde belirtilmemiş.
- bl-animasyon-anahtar ile bl-urun-turntable turntable konusunda çakışır.

## Üyeler
- ajan (16): bl-animasyon-anahtar, bl-dokuya-pisirme, bl-geometri-dugumleri, bl-glb-disa-aktar, bl-gorsel-ani-kontrol, bl-isik-kurulumu, bl-kamera-kompozisyon, bl-malzeme-kurucu, bl-mod-modeli-blender, bl-modelleme-plani, bl-python-betik, bl-render-ayari, bl-rig-iskelet, bl-sahne-temizlik, bl-urun-turntable, bl-uv-acma
