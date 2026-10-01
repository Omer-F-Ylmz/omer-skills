# ComfyUI yerel görsel hattı (KURULUM-GÖRSEL, 2026-10-01)

Ücretsiz, yerel görsel üretimi: `C:\AI\ComfyUI` (v0.38.0, torch cu130, uv venv) + `C:\AI\rembg` (ayrı uv venv). Sürüş `tools/gorsel_uret.py`, skill `gorsel-uret`. Model dosyaları, sha256 ve lisanslar: `docs/gorsel/modeller.md`; seçim: `docs/gorsel/olcum.md`.

## Lisanslar
- ComfyUI GPL-3.0: yalnız yerel araç olarak çalışır, dağıtılmaz; çıktı görseller GPL kapsamında değil.
- Z-Image Turbo, FLUX.2 [klein] 4B: Apache-2.0, kapısız (Comfy-Org yeniden paketlemesi). klein 9B/[dev] BFL sözleşmesi ister → yasak.
- Real-ESRGAN x4plus: BSD-3-Clause (safetensors; .pth gerekmedi).
- rembg MIT + BiRefNet MIT. rembg varsayılanı `bria-rmbg` ticari lisans ister → araç modeli her zaman `-m birefnet-general` verir.
- Qwen-Image kurulmadı: RAM 31.7 GB < 32 GB eşiği.

## Güvenlik
- Dinleme yalnız 127.0.0.1:8188; başka adres → exit 1 + PID ile kapatma. Kapatma yalnız durum dosyasındaki PID ile (`taskkill /PID /T`), ad ile öldürme yok.
- Yalnız .safetensors (ComfyUI .pth'yi zaten `weights_only=True` ile yükler; kullanılmadı). sha256 HF LFS değeriyle doğrulandı.
- ComfyUI-Manager, topluluk node'u, GGUF yok; 12 GB'ye sığdırma çekirdek `UNETLoader weight_dtype=fp8_e4m3fn` + çekirdek RAM offload'u.
- Uzak API çağrısı yok; ağ yalnız kurulumdaki HF indirmesi.
- Blender (9876) açıkken ac/uret/buyut exit 2: GPU ortak.

## Dört ölçüt
- Bakım: ComfyUI haftalık sürüm, Comfy-Org resmi; modeller sabit dosya, güncelleme elle (git pull + sha256 yeniden).
- CC'de çift mi: nano-banana-2 MCP (Gemini, ücretli) ile aynı işi yapar; ücretsiz yol bu, nano-banana yalnız Ömer açıkça isterse.
- İzin kapsamı: repo dışı `C:\AI\`; çıktı yalnız `Desktop\<Proje>\`; sistem ayarı/servis yok.
- Context maliyeti: skill ≤3 KB; araç çıktısı yol + tek satır; görseller yalnız kontrol için Read ile açılır.
