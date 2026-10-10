# 03 Teeth Shader | Auto Setup 1.24 | Unreal Engine 5
## Künye
03 Teeth Shader | Auto Setup 1.24 | Unreal Engine 5 · Reallusion · süre: 0:13 · en-orig · https://youtu.be/Qjh7uXXsOvE · şema 2
motor: parti 2026-10-09-short-46 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 22517 tk · claude-haiku-5-5: claude-haiku-5-5 · 17919 tk
## Özet
13 saniyelik kısa video: Unreal Engine 5'te Reallusion Auto Setup'ın 1.23 sürümünden 1.24 sürümüne geçişiyle gelen diş (Teeth) shader'ı gösteriliyor. Karakterin ağız yakın çekiminde Normal (Bump Strength) ve Roughness (TeethGum Front Roughness / Specular) parametreleri değiştirilerek dişlerin görünümündeki fark sergileniyor. Konuşma ve altyazı yok; bilgi yalnız karelerden ve ekran metninden geliyor.
## Bölümler
- 0:00 Auto Setup 1.23 – Teeth başlangıç görünümü
- 0:03 Normal: Bump Strength 1.0 ayarı
- 0:08 Roughness: TeethGum Front Roughness 0.208, Specular 0.042
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Unreal Engine 5 | yok | teknik | yok | Videonun içinde çalıştığı oyun motoru; editörde diş materyali düzenleniyor. | 0:00 | Başlıkta Unreal Engine 5; editörde Content Drawer, Output Log, Select Mode görünüyor. (karede: Unreal Editor penceresi, File/Edit/Window menüsü, sahnede ağız yakın çekimi.) |
| Reallusion Auto Setup | yok | plugin | yok | Karakter materyallerini Unreal'e otomatik kuran Reallusion aracı; sürüm 1.23'ten 1.24'e geçiyor. | 0:00 | Ekranda 'Auto Setup Version 1.23' yazıyor; OCR 0:01'de 1.24. · kanıt: kare (karede: Sol üstte 'Auto Setup Version 1.23' yazısı.) |
| MHCLightingPresets | yok | teknik | yok | Sahnede kullanılan aydınlatma ön ayarı haritası. | 0:00 | Pencere başlığında MHCLightingPresets, sekmede CustomLight_01_Kevin. (karede: Sağ üstte 'MHCLightingPresets', sol sekmede 'CustomLight_01_Kevin'.) |
| Teeth shader | yok | teknik | yok | 1.24 ile gelen diş materyal katmanı; normal, roughness, scatter ve gum AO/specular parametreleri içerir. | 0:03 | Material Instance'ta Teeth bölümü: Teeth Mask Map, Teeth Scatter, TeethGum Back AO. (karede: Sağ panelde Teeth bölümü parametre listesi, solda 'TEETH / Normal' etiketi.) |
| Material Instance Editor | yok | teknik | yok | Diş materyali parametrelerini (Layer Parameters) düzenlemek için kullanılan düzenleme penceresi. | 0:03 | Edit Asset Window, Layer Parameters sekmesi, Save Child / Save Sibling düğmeleri. · kanıt: kare (karede: Sağ panelde Details ve Layer Parameters sekmeleri, altta Save Sibling ve Save Child.) |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Auto Setup 1.24 sürümü yeni bir Teeth (diş) shader'ı getiriyor; normal ve roughness ayarlarıyla diş görünümü değişiyor. | 0:08 | özellik |
| Bump Strength 1.0 değeri normal harita etkisini gösteriyor. | 0:03 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | Unreal Engine 5 | Unreal Engine 5 | Başlık ve editör arayüzü |
| kare 0:00 | Reallusion Auto Setup 1.23/1.24 | Reallusion Auto Setup | Auto Setup Version yazısı |
| kare 0:00 | MHCLightingPresets | MHCLightingPresets | Pencere başlığı |
| kare 0:03 | Teeth parametre paneli | Teeth shader | Teeth Mask Map, Teeth Scatter, TeethGum alanları |
| kare 0:03 | Edit Asset penceresi, Save Child/Sibling | Material Instance Editor | Details, Layer Parameters, Save düğmeleri |
| kare 0:08 | Roughness/Specular değerleri | Teeth shader | TeethGum Front Roughness 0.208, Specular 0.042 |
| kare 0:00 | Content Drawer, Output Log, Derived Data, Source Control | aday değil: genel kavram | Editör alt çubuğu |
| kare 0:00 | Kevin karakteri (CustomLight_01_Kevin) | aday değil: konu dışı | Sekme adı |
## Kareden okunanlar
- 0:00: Auto Setup Version 1.23; TEETH etiketi; Unreal editör, MHCLightingPresets, CustomLight_01_Kevin.
- 0:03: Bump Strength: 1.0; TEETH / Normal; sağda Teeth parametreleri (Teeth Mask Map, Teeth Edge Color, Teeth Scatter, TeethGum Back/Front AO, Roughness, Specular).
- 0:08: TeethGum Front Roughness: 0.208; TeethGum Front Specular: 0.042; TEETH / Roughness etiketi.
## Belirsizlikler
- Başlıkta 1.24, ilk karede 1.23 yazıyor; OCR 0:01'de 1.24 görüyor, geçiş karelerde doğrulanamadı.
- Konuşma ve açıklama yok; amaç yalnız görüntüden çıkarıldı.
- Sağ paneldeki varlık adı (UpperTeeth_before_...) tam okunamadı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Auto Setup 1.23 ile kurulan karakterin diş görünümü Unreal editöründe gösterilir. — araçlar: Unreal Engine 5, Reallusion Auto Setup
- 2. adım — Auto Setup 1.24 sürümüne geçilir. — araçlar: Reallusion Auto Setup
- 3. adım — Diş materyalinin Layer Parameters paneli açılır. — araçlar: Material Instance Editor
- 4. adım — Normal bölümünde Bump Strength 1.0 gösterilir. — araçlar: Teeth shader
- 5. adım — Roughness ve Specular değerleri (0.208 / 0.042) ayarlanır. — araçlar: Teeth shader, Material Instance Editor
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
