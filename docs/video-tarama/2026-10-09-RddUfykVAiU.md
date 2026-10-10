# 05 Skin Shader | Auto Setup 1.24 | Unreal Engine 5
## Künye
05 Skin Shader | Auto Setup 1.24 | Unreal Engine 5 · Reallusion · süre: 0:34 · en-orig · https://youtu.be/RddUfykVAiU · şema 2
motor: parti 2026-10-09-short-46 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 12482 tk · claude-haiku-5-5: claude-haiku-5-5 · 30659 tk
## Özet
Reallusion Auto Setup 1.24 ile Unreal Engine 5'te cilt (skin) shader'ının kısa tanıtımı: MicroNormal ve roughness parametreleri, spekülar ayarları, SubsurfaceProfile (SSS) ayarları, dönen ışık altında cilt görünümü ve ışık geçirgenliğinin (light transmission) açılması gösterilir. Altyazı ve konuşma yok; bilgi yalnız ekran görüntülerinden ve OCR'dan gelir.
## Bölümler
- 0:00 MicroNormal parametreleri (materyal örneği)
- 0:04 Bölgesel roughness ölçekleri
- 0:09 Head Specular ayarları
- 0:12 SubsurfaceProfile / SSS ayarları
- 0:18 Dönen ışık kaynağı altında cilt
- 0:23 Işık geçirgenliğini (Transmission) açma
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Unreal Engine 5 | yok | CLI | yok | Sahnenin ve materyal düzenlemenin yapıldığı oyun motoru. | 0:00 | Editör arayüzü: Content Drawer, Outliner, Details, Perspective görünümü. (karede: Unreal editör arayüzü, Details paneli ve viewport'ta yüz modeli.) |
| Auto Setup 1.24 | yok | plugin | yok | Reallusion karakterleri için otomatik materyal kurulumu. | 0:00 | Video başlığı: Skin Shader / Auto Setup 1.24 / Unreal Engine 5 · Reallusion |
| Skin Shader | yok | teknik | yok | Cilt materyali; MicroNormal, roughness ve SSS parametreleri içerir. | 0:18 | Alt yazı: Skin Shader appearance under an orbiting light source (karede: Sol altta SKIN etiketi ve 'Skin Shader appearance under an orbiting light source' yazısı.) |
| MicroNormal | yok | teknik | yok | Cilt gözenek detayı için mikro normal haritası, güç ve tiling parametreleri. | 0:00 | MicroNormal Map, Mask Map, Strength, Tiling Value alanları. (karede: Details panelinde MicroNormal grubu: Map, Mask Map, Strength 1.021, Tiling Value, Flip Micro Normal Y.) |
| SubsurfaceProfile | yok | teknik | yok | Cilt alt-yüzey saçılımı (SSS) için profil varlığı. | 0:12 | OCR: Asset Type: SubsurfaceProfile, Mean Free path Color, Surface Albedo. (karede: kanıttan) OCR: Asset Type: SubsurfaceProfile, Mean Free path Color, Surface Albedo. |
| Light Transmission | yok | teknik | yok | Işığın cilt içinden geçişini açan ayar. | 0:23 | Alt yazı: Turning on light Transmission (karede: Koyu sahnede RectLight ve alt yazı 'Turning on light Transmission'.) |
| Rect Light | yok | teknik | yok | Sahnede cildi aydınlatan ışık türü. | 0:23 | Place Actors listesinde Rect Light; Outliner'da RectLight_key. (karede: Place Actors panelinde Directional, Point, Spot, Rect, Sky Light.) |
| MHCLightingPresets | yok | iş akışı | yok | Sahnedeki ışık ön ayarları haritası. | 0:18 | Viewport sağ üstünde MHCLightingPresets yazıyor. (karede: Outliner üstünde MHCLightingPresets sekmesi.) |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Skin shader, dönen bir ışık kaynağı altında gösterilir. | 0:18 | özellik |
| Işık geçirgenliği (transmission) açılabilir. | 0:23 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| başlık | Unreal Engine 5 | Unreal Engine 5 | Başlıkta ve editör arayüzünde |
| başlık | Reallusion Auto Setup 1.24 | Auto Setup 1.24 | Başlık |
| kare 0:00 | MicroNormal parametreleri | MicroNormal | Details paneli |
| kare 0:04 | Roughness Scale parametreleri | Skin Shader | Cheek/Chin/Nose Roughness Scale |
| kare 0:09 | Head Specular ayarları | Skin Shader | Specular Cavity Map, Specular UOffset |
| kare 0:12 | SubsurfaceProfile | SubsurfaceProfile | Asset Type: SubsurfaceProfile |
| kare 0:18 | RectLight, PointLight, SpotLight | Rect Light | Outliner listesi |
| kare 0:18 | MHCLightingPresets | MHCLightingPresets | Harita adı |
| kare 0:23 | Directional Light, Sky Light | aday değil: genel kavram | Yalnız Place Actors listesinde görünüyor |
| kare 0:23 | Light Transmission | Light Transmission | Alt yazı |
| yorum | Ayarın yerini soran yorum | aday değil: konu dışı | Yorumda öğretici isteniyor |
## Kareden okunanlar
- 0:00: Details paneli: MicroNormal Map, Mask Map, Strength, Tiling Value, Flip Micro Normal Y; Save Sibling/Save Child.
- 0:18: Outliner: RectLight, PointLight, SpotLight, RimLight_Parent, Sphere; alt yazı Skin Shader appearance under an orbiting light source.
- 0:23: Place Actors paneli ve Kevin2 skeletal mesh; alt yazı Turning on light Transmission.
## Belirsizlikler
- Ayarların Unreal'de nerede bulunduğu anlatılmıyor (yorumda istenmiş).
- Konuşma ve altyazı yok; parametre değerleri OCR'da bozuk okunmuş olabilir.
- Reallusion Auto Setup'ın ayrı bir eklenti mi olduğu yalnız başlıktan çıkarıldı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- yok
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
