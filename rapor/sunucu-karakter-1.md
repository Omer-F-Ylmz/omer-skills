# SUNUCU-KARAKTER-1 tur 3 — TUR BITTI (görsel üretim yolu kapalı)

Çıktı değişmedi: `Desktop\Claude ile yapılanlar\sosyal-oto\sunucu\{free-ai-drop,curiosity-well}\` + `etiket-plani.md` (tur 2 kod-çizim set). Yayın/yükleme yok. Yoklama betiği: `tools/sunucu_bulut_dene.py`.

## Ücretsiz görsel yol yoklaması (30 Eki ~11:40, tek istek/yol)
- Gemini görsel (2.5-flash-image, 3-pro-image, 3.1-flash-image): 429, free tier `limit: 0` → kota yenilenmesi değil, ücretsiz katmanda görsel modeli kapalı. Beklemek işe yaramaz.
- Cloudflare flux-1-schnell: 429 günlük 10.000 neuron tükendi (hesap kimliği var, sıfırlanma 03:00 TR).
- fal.ai: 403 "User is locked, TOP_UP" (kredi bitti; ücretli yok).
- HF router FLUX.1-schnell: 410 model sağlayıcıda kaldırıldı.
- NVIDIA build flux.1-schnell: 2 denemede zaman aşımı (120 sn, 100 sn).
- Higgsfield CLI: çalışma alanı seçili değil, `auth login` OAuth tarayıcı penceresi açar → ekran kuralı gereği çalıştırılmadı.
- Yerel Z-Image-Turbo: boş RAM 7,6-8,3 GB < 12 GB eşiği → ComfyUI açılmadı (VRAM 2/12 GB uygundu).

## Sonuç
Kabul kapısı (her parça ≥7) bu turda ölçülemedi: kod-çizim set son hakemde 5-7 aralığında (tur 2), gerçek üretim yolu yok; sahte ilerleme için yeniden çizim yapılmadı.

## Ömer'in kararı gerekenler / sonraki tur koşulu
1. Boş RAM ≥12 GB olunca (başka uygulamalar kapanınca) yerel Z-Image-Turbo ile karakter referansı + 10 poz üret → hakem.
2. Ya da Cloudflare kotası 03:00 TR sonrası (bir sonraki gece koşusu) flux-1-schnell ile.
3. NVIDIA yolunu daha uzun zaman aşımıyla (300 sn) ayrıca denemek mümkün; denenmedi.
4. Ses insan kulağıyla ölçülmedi; Ömer dinlemeli.

## Tur 4 (31 Eki ~12:00) — TUR BITTI, kök neden bulundu
- Yerel turbo yolu (GGUF Q4_K_M + `--disable-mmap` + `GORSEL_PORT`) 3 kez açıldı; her seferinde "Requested to load ZImageTEModel_" satırında sunucu öldü. RAM tepesi %71 (sorun RAM değil).
- Kök neden (`.kos/kopru/vram-siper.log` 11:58-11:59): `tools/vram_siper.py` ComfyUI'yi "tek-gpu-isi vram 71-76%" ile kapattı. Başka bir oturumun `tools/video_derin.py` (PID 616, OCR) ~6,3 GB VRAM tutuyor (taban %51); ComfyUI ikinci GPU işi sayılıp VRAM %70'i geçince en yeni olarak öldürülüyor. Önceki turdaki "takılma / bağlantı koptu" da aynı olabilir (doğrulanmadı).
- Siper kapatılmadı (NİHAİ 35), video_derin'e dokunulmadı (başka oturumun işi).
- Bulut yeniden yoklandı: nvidia zaman aşımı, hf 410, fal 403 TOP_UP, cf 429 günlük pay dolu. Hepsi kapalı.
- Karakter görseli bu turda üretilmedi; kapı ölçülemedi.
- Sonraki tur koşulu: `video_derin.py` (PID 616) bitince (GPU'da tek iş) `GORSEL_PORT=<yeni> COMFY_EK=--disable-mmap` ile turbo yolu; ya da 03:00 TR sonrası CF flux-1-schnell (seed yok → prompt kalıbı).

## Tur 5 (31 Eki ~14:30) — TUR BITTI, yerel yol çalışıyor ama RAM'i yetim ComfyUI tutuyor
- video_derin bitti, VRAM boş (2,3/12 GB); `GORSEL_PORT=8231 COMFY_EK=--disable-mmap gorsel_uret.py uret --is foto --model turbo` 1 görseli üretti (89 sn): free-ai-drop `uretim/t1/` — stilize 3D robot-tilki, palet markaya uygun, kök neden (VRAM siper) doğrulandı.
- Sonraki üretimler VAE aşamasında `RAM 2 GB altına indi` freniyle ölüyor. Sebep: önceki `ac` çağrılarımdan kalan yetim ComfyUI (PID 57156, port 8231 komutu, ~5-7,7 GB RAM) bellekte duruyor, yeni örnek üstüne biniyor. `gorsel_uret.py kapat` onu görmüyor ("oturum yok"); `taskkill /PID 57156` auto-mode sınıflandırıcısınca reddedildi.
- Hazır: `tools/sunucu_karakter_batch.py` (3 dönüş · 6 ifade · 10 poz, iki marka, sabit tohum + sabit karakter cümlesi = tutarlılık reçetesi).
- Ömer'in tek adımı: PID 57156'yı kapat (Görev Yöneticisi ya da `taskkill /PID 57156 /T /F`) → sonra `GORSEL_PORT=8231 COMFY_EK=--disable-mmap python tools/gorsel_uret.py ac` + `python tools/sunucu_karakter_batch.py`.
- Kapı ölçülemedi; ses/klip/hakem adımları üretilen görsellere bağlı.
