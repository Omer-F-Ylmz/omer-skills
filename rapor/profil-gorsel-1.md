# PROFIL-GORSEL-1 tur4 — TUR BITTI (hakem ≥8 sağlanmadı)
Çıktı: Desktop\Claude ile yapılanlar\sosyal-oto\marka\{free-ai-drop,curiosity-well}\v3\ (isaret-1600, profil, afiş, shorts şablon+boş, _kucuk-boyut, aday/ 8'er bulut adayı); v1/v2 duruyor. Çakışma testi: marka\cakisma-testi-v3.json (tüm kesişim listeleri boş).
Bulut sırası: Cloudflare flux-1-schnell ÇALIŞTI (8+8 aday, ücretsiz; seed parametresi reddediliyor, prompt'a varyasyon eki); NVIDIA zaman aşımı; HF 410 Gone; fal 403 'User is locked: TOP_UP'; Higgsfield denenmedi.
Seçim: FAD aday 03 (damla + yıldız ışık kaynağı, arka plan alfa ile kesildi, parlama eklendi); CW aday 06 (aşağıdan yukarı kuyu, altın çekirdek, daire kırpma + halka). vtracer ile vektörleme YAPILMADI (raster kesim kullanıldı).
Hakem (bağımsız okuyucu ajan, Ömer ölçeği, düzeltme ÖNCESİ): FAD profil 6,5 · afiş 6 · shorts 5,5 · genel 6; CW 6 · 5 · 5,5 · genel 5,5. Düzeltme sonrası yeniden puanlanmadı.
Hakem sonrası düzeltilen: afişte işaret güvenli alana çekildi/küçültüldü, CW daire-metin çakışması kalktı, bulanık levha yumuşatıldı, shorts'ta b-roll alanında yinelenen logo kaldırıldı, CW profilde işaret büyütüldü.
Kalan kusurlar: FAD sembolü klişe (damla+kıvılcım), 48px'te iç yıldız kayboluyor; CW kuyu görseli AI-slop (ışık mantığı, çamurlu tuğla), 48px'te göz/lens gibi; shorts kart sağ/sol marj asimetrisi (60/150); 8 aday + tek sağlayıcı yeterli çeşitlilik vermedi.
Sonraki tur: ComfyUI/RAM boşken ya da NVIDIA/HF yeniden dene; CW'yi radyal ışıklı vektör/gravür stilinde yeniden üret; FAD'e özgün form + kalın kontur; shorts'u ortala; yeniden puanlat.
Araçlar: tools/profil_bulut.py, tools/profil_gorsel_v3.py. Test/CI yok.
