# Blender Product Lighting Tutorial | Light a Beverage Can Scene in 6 Minutes
## Künye
Blender Product Lighting Tutorial | Light a Beverage Can Scene in 6 Minutes · Nicholas Ashcroft · süre: 6:07 · en · https://youtu.be/wySOWP-MevI
## Özet
Blender 5.0'da bir içecek kutusu sahnesi sıfırdan aydınlatılıyor. Dünya (world) gücü sıfıra çekilip arka ışıkla başlanıyor.
Sonra etiketi hedefleyen ana (key) ışık ekleniyor. Dolgu için ışık yerine bir plane duvarı (basit ortam) kuruluyor ve ışıklar ondan sekiyor.
Arka plan (backdrop) plane'i düz görünüyor; gobo dokuları (alan ışığına bağlı) ile renkli desenli ışık eklenip çeşitlendiriliyor.
Son olarak compositing'de lens distortion, vignette ve sensor noise düğümleriyle cilalanıyor. Sahne Patreon'da, gobo paketi Gumroad'da.
## Bölümler
- 0:00 Giriş ve kurulum — sahne tanıtımı, gobo'lar
- 0:35 Arka ışık — rendered view, world gücü 0, area light, güç 3000
- 1:28 Ana ışık — ikinci area light, etikete yönlendirme, loş atmosfer
- 2:09 Dolgu ortamı — plane duvar, extrude, bevel, bounce
- 3:21 Backdrop ve gobo'lar — arka plan plane'i, gobo area light, renk, pozlama
- 5:25 Son cila — compositing, vignette
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Arka ışıkla başlama (world gücü 0) | yok | iş akışı | yok | Dünya ışığını sıfırlayıp önce arka ışıkla başlayarak ışığı katman katman kurmak | 0:35 | Anlatıcı world strength'i sıfıra indirip önce backlight ekliyor; sonra artırılabilir diyor. |
| Area light (ürüne göre genişlik, güç ~3000) | yok | teknik | yok | Arka ışık üründen geniş ama aşırı geniş olmayan area light; güç 3000 | 0:35 | “I'm going to increase it all the way to 3,000.” |
| Key light etiketi hedefleme | yok | teknik | yok | Ana ışığı logoya doğru açılı yerleştirip gölgeleri koruyarak loş görünüm | 1:28 | Key light etikete/logoya yönlendiriliyor, moody gölgeler korunuyor. |
| Plane duvar ile ışıksız dolgu (bounce ortamı) | yok | teknik | yok | Ürün arkasına extrude+bevel plane koyup ışıkların sekmesiyle dolgu elde etmek | 2:09 | Dolgu için ışık yerine duvar; ışıklar duvardan sekiyor, en basit ortam. |
| Duvar base color kısma | yok | ipucu | yok | Fazla parlak dolguyu duvar malzemesinin base color'ını düşürerek azaltmak | 2:09 | Duvarın base color'ını biraz düşürüyor. |
| Işık exposure ayarı | yok | ipucu | yok | Işığı sürüklemek yerine exposure değeriyle (örn. 1) güç ayarlamak | 3:09 | Anlatıcı gücü sürüklemek yerine exposure'ı sürüklemeyi tercih ettiğini söylüyor. |
| Backdrop plane | yok | teknik | yok | Çerçevede, çok uzak olmayan arka plan plane'i; iki ışığı da kontrol edilebilir tutar | 3:21 | Backdrop çerçevede ve ışıklara yakın olmalı. |
| Gobo ışıkları (Wendelin Jacobers gobo paketi) | yok | teknik | https://wendelinjacober.gumroad.com/l/blender-gobos?layout=profile | Doku (soyut desen) ile ışık gölge deseni; spotlight yerine area light, ölçeklenip yumuşatılıyor | 3:21 | Gobo'lar “Wendi's gobo lighting”ten, abstract gobo seçiliyor, area light'a çevriliyor. |
| Renkli gobo (sarı, mor) + pozlama | yok | teknik | yok | Gobo ışığına sahneye uyan renk verip pozlamayı patlatmak, kenara yerleştirmek, kopyalayıp ikinci renk eklemek | 4:21 | Açık sarı, sonra kopya açık mor, köşeden. |
| Compositing: Lens Distortion + Vignette + Sensor Noise | yok | teknik | yok | Son cila düğümleri; vignette azaltılıyor | 5:46 | Kare 5:46'da bu üç düğüm Render Layers'a bağlı. |
| Rendered view'da kontrol | yok | ipucu | yok | Işık ayarlarını sürekli rendered view'da izlemek | 0:35 | Rendered view'a geçerek başlıyor. |
| Patreon sahne indirme | yok | iş akışı | https://www.patreon.com/c/nicholasashcroft | Videodaki sahne dosyası Patreon'da | 0:00 | Açıklamada Patreon bağlantısı. |

## İddialar
| iddia | zaman | tür |
|---|---|---|
| Arka ışık gücü yaklaşık 3000 | 0:35 | sayısal |
| Backlight en havalı görünen ışık (kişisel görüş) | 0:00 | öneri |
| Key light en önemli ışık | 1:28 | öneri |
| Backlight ürün kenarlarını kesmesin diye üründen geniş olmalı ama difüz olmayacak kadar dar | 0:35 | öneri |
| Plane duvar ışık eklemeden dolgu etkisi yaratır | 2:09 | özellik |
| Düz backdrop sahneyi sıkıcı yapar, gobo çeşitlilik katar | 3:21 | karşılaştırma |
| Gobo'lar ücretsiz indirilebilir | 0:00 | özellik |
| Gobo spotlight yerine area light yapılmalı | 3:21 | öneri |
| Backdrop çok uzak olmamalı, ışıklarda kaybolmasın | 3:21 | öneri |

## Site/UI teknikleri
(Frontend/site içeriği değil; atlandı.)

## Kareden okunanlar
- 1:01 Blender 5.0.0 arayüzü, World sekmesi Strength ≈ 0.0
- 2:39 Plane (U şekilli duvar), outliner: Area, Area.001, Camera, Plane; kutu "MYDRATE / PULSE"
- 3:51 Plane.001 backdrop, malzeme yok
- 4:51 gobo görüntü tarayıcı (abstract, abstract2, abstract3, ... seçenekleri), Plane malzeme Principled BSDF
- 5:46 Compositing: Render Layers → Lens Distortion (Distortion 0.010, Dispersion 0.020) → Vignette (Fade ~0.84, Feather 0.400) → Sensor Noise (Luminance 0.100, Chroma 0.050) → Group Output/Viewer; Render Engine Cycles, GPU Compute

## Belirsizlikler
- “Wendi's gobo lighting” ASR; Gumroad bağlantısı Wendelin Jacober.
- Gobo'ların ücretsiz mi (Gumroad) olduğu net değil.
- Vignette/Lens Distortion değerleri kareden tahmin okuma.

## Atlanan segment oranı
0/9 (paket tam okuma)
