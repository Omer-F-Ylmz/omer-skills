# Blender
ad: Blender
tur: CLI
video: eKnpRVgqXR8
repo: blender/blender
lisans: GPL-3.0-or-later
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/blender/blender
telemetri: Bilinmiyor. README'de belirtilmemiş ve bu oturumda doğrulamadım.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short-2)
## Ne
Ücretsiz ve açık kaynak 3B üretim paketi. Modelleme, rigging, animasyon, simülasyon, render, compositing, hareket takibi ve video düzenlemeyi kapsıyor. Videolarda küp, 3B metin, eğri, Array ve Simple Deform ile modelleme yapılıyor. Shader node'larıyla bulut üretiliyor.
## Mekanizma
Masaüstü uygulaması olarak çalışır. Sahne nesnelerden, modifier'lardan (Array, Simple Deform gibi) ve node tabanlı materyallerden oluşur. Render motorları sahneyi görüntüye çevirir. `blender -b dosya.blend -P betik.py` ile arayüzsüz çalıştırılabilir ve Python API'si (bpy) sahneyi programla kontrol eder. Bu bilgi genel bilgime ve repo README'sine dayanıyor. CLI bayraklarını bu oturumda çalıştırıp sınamadım.
## Kanıt
- Blender ücretsiz ve açık kaynaktır → doğrulandı · Repo README: 'free and open source 3D creation suite', GPL v3.
- Videolardaki araç Blender'dır → doğrulandı · Video bulgularında Blender logosu ve Material.004 node editörü var. Videoyu kendim izlemedim.
- Blender arayüzsüz CLI ile betiklenebilir → sınanamadı · Genel bilgiye dayanıyor. Bu oturumda çalıştırılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- blender.org/download adresinden işletim sistemine uygun sürümü indir
- Kaynaktan derlemek için developer.blender.org/docs/handbook/building_blender/ adresine bak. GitHub yansısını klonlarken GIT_LFS_SKIP_SMUDGE=1 kullan
- Arayüzsüz kullanım: blender -b dosya.blend -P betik.py
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
3B içerik üretimi için tam donanımlı, ücretsiz bir araç. Betiklenebilir olduğu için bir ajan ya da otomasyon hattına (toplu render, prosedürel model) bağlanabilir.
## Maliyet/risk
GPL-3.0 türev kodda copyleft getirir. Blender'ı çağırmak ya da betik yazmak bunu doğrudan tetiklemez ama bpy'yi gömmek tetikleyebilir. Öğrenme eğrisi diktir. Ağır render'lar GPU ve zaman ister. GitHub yansısında LFS sorunu çıkabilir. Videolar yalnızca ~30 sn'lik kesitler ve derin bir kanıt sunmuyor.
## Tasarruf
Token aracı değil, uygulanamaz.
## Üretilebilir
hedef_tur: skill
tarif: 'blender-headless' adında bir skill yaz. Kullanıcı isteğinden bpy betiği üretsin (küp, Array modifier, Simple Deform, metin nesnesi). Sonra `blender -b -P betik.py -- --render-output ... -f 1` ile çalıştırıp çıktı görüntüsünü döndürsün. Blender yolunu ve sürümünü ortam değişkeninden okusun. Bu tarif denenmedi.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short-2/panel.md → Ömer sütunu
## Özellikler
### Modelleme, rigging, animasyon, simülasyon, render, compositing, hareket takibi ve video düzenleme
kaynak: https://github.com/blender/blender
### GPL v3 lisansı, açık kaynak geliştirme
kaynak: https://www.blender.org/about/license
### Python API ile betikleme
kaynak: https://docs.blender.org/manual/en/latest/index.html
### İş akışı aşamalıdır: Figma sonrası Blender'da ikinci aşama tamamlanıyor.
video: 9opJeH9j9qs · iddia: İş akışı aşamalıdır: Figma sonrası Blender'da ikinci aşama tamamlanıyor.
sonuc: sınanamadı
arastirma: Bu iddia Blender'ın bir özelliği değil, videodaki kullanıcının iş akışını anlatıyor. Blender belgesinde "Figma sonrası ikinci aşama" diye bir özellik ya da yerleşik iş akışı yok. Aday dosyasındaki kareye göre üstte solda Figma, sağda Blender logosu görünüyor. 9opJeH9j9qs karesinde küre nesnesi, kare 87 zaman çizelgesi ve Material.004 node editörü var. Altyazı "make clouds and combine shapes". Bunlar iki aracın birlikte kullanıldığını düşündürüyor. Ama "aşamalı" ve "ikinci aşama tamamlanıyor" ifadesini gösteren bir kanıt yok. Videoyu bu oturumda izlemedim ve web araması yapmadım. Blender'ın Figma ile yerleşik bir entegrasyonu olduğuna dair belge bilgim de yok (bilinmiyor). Blender tarafında kanıtlanan tek şey, modelleme ve shader node'larıyla bulut üretimi gibi genel yeteneklerdir. Bunların kaynağı repo README'si ve Blender kılavuzudur. Figma→Blender sıralaması ise yalnızca videonun anlatımına dayanır. Bu yüzden iddia belgeden doğrulanamıyor ya da çürütülemiyor.
kaynak: https://docs.blender.org/manual/en/latest/index.html
## Destek
- eKnpRVgqXR8 · 0:30 · 3B modelleme ve render aracı; küp, 3B metin, eğriler, Array ve Simple Deform kullanılıyor. · kanıt: Karede Blender logosu ve 'extrude and place it in the desired position' altyazısı var. (karede: Üstte solda Figma, sağda Blender logosu; bulanık Blender arayüzü; altyazı: 'extrude and place it in the desired position'.)
- 9opJeH9j9qs · 0:28 · Shader node'larıyla bulut üretme ve şekilleri birleştirme. · kanıt: Altyazı 'make clouds and combine shapes', Material.004 node editörü. (karede: Blender 3B görünüm penceresinde küre nesnesi, altta zaman çizelgesi (kare 87) ve Material.004 node editörü; altyazı 'make clouds and combine shapes'.) · iddia: İş akışı aşamalıdır: Figma sonrası Blender'da ikinci aşama tamamlanıyor.
