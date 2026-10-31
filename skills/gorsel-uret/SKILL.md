---
name: gorsel-uret
description: "Görsel üretme, düzenleme, büyütme, arka plan silme işinde önce yükle: yerel ComfyUI oturumunu CC yönetir; tools/gorsel_uret.py ac/uret/buyut/arkaplan/kapat. Yalnız Claude Code'da."
---

# gorsel-uret — yerel, ücretsiz görsel üretimi

Araç: `python C:\Projeler\omer-skills\tools\gorsel_uret.py <komut>` (mutlak yolla).
ComfyUI yolu: çalışan kurulum `C:\AI\ComfyUI` (kod sabiti; tek kurulum, `Desktop\araclar\ComfyUI` yok).
VIDEO HATTI KURALI (Ömer 21 Eki): üretim (görüntü/video/ses/kurgu) tamamen yerel ve ücretsiz (ComfyUI+FLUX/Wan, Chatterbox/edge-tts, Remotion, ffmpeg); Claude yalnız senaryo + sahne listesi yazar; hedef reklam filmi başına Claude maliyeti ≤$0.10.

## Akış (sıra değişmez)
1. `ac` — ComfyUI 127.0.0.1:8188'de açılır (Blender açıksa 9876 dolu → 2; ikisi birlikte koşmaz).
2. `uret --is <iş> --prompt "..." --cikti C:\Users\pc\Desktop\<Proje>\... [--adet ≤4] [--tohum N] [--referans a.png ...]`
   `buyut <png> --kat 2|4` · `arkaplan <png>` (ComfyUI gerekmez).
   Alternatif büyütme (yalnız CC): `python tools/upscale.py <girdi> <çıktı> [digital-art-4x|high-fidelity-4x]` (Upscayl, 1352x455→5408x1820 5,4 sn; kenar keskinliği bicubic 149,5 → high-fidelity 194,4 · digital-art 854,2; afiş/illüstrasyon digital-art, foto high-fidelity).
3. `kapat` — yalnız durum dosyasındaki PID ile kapatır, port boşalana dek (≤15 sn) bekler.

İş yarıda kalsa da 3 çalıştırılır; sunucu açık bırakılmaz.

## Yönlendirme (K6 ölçümüyle)
| iş | model | neden |
|----|-------|-------|
| urun · foto · doku | zimage (Z-Image Turbo fp8) | fotogerçekçilik |
| metinli · duzenle | klein (FLUX.2 klein 4B) | metin doğru ("TELVE"), referansla düzenleme |
| düşük RAM · hızlı foto/logo | turbo (Z-Image-Turbo GGUF Q4_K_M, Apache-2.0) | ölçüm: 1024² ~20 sn, tepe RAM %82–84 · VRAM %50 (boş RAM ≥13 GB iken); boş RAM ~8 GB ise soğuk yüklemede acil fren riski |
`--model` ile elle seçilebilir; `GORSEL_PORT` ile port değişir (8188'de PID 0 hayalet dinleyici kalırsa); `COMFY_EK` ile `ac`'a deney bayrağı eklenir; `--referans` yalnız `duzenle` işinde.
Prompt her zaman İngilizce yazılır (Türkçe prompt Z-Image'da konudan sapar: "beyaz fonda seramik fincan" → ahşap masada kavanoz); görselin İÇİNE yazılacak metin (ör. "Türk Kahvesi") tırnak içinde aynen kalır.

## İstem kalıpları (VIDEO-IHZ-2)
- Sohbet tarzı istem: JSON'a çevirtme yok; sahneyi arkadaşına anlatır gibi yaz, kamera/ışık/malzemeyi düz cümleyle ver. Metin modeli (klein) için metin tırnak içinde.
- Dondur + yeşil ekran (animasyon kalıbı): "freeze the subject in place, same position, make the background greenscreen" — kare ilk üretilir, sonra arka plan `arkaplan` ile ayrılır (ücretsiz yerel).
- Site arka plan döngü videosu tarifi: kısa (4–8 sn), döngülü (başı = sonu), ≤1,5 MB, 16:9 ve mobil kırpma, poster = ilk kare (JPG/WebP), `prefers-reduced-motion` için video yerine poster.
- Karşılıklar: Flow/Nano Banana → zimage/klein; Veo/Omni video → yerel Wan + ffmpeg (döngü kırpma).

## Bellek
- Model değişiminde bellek araçla boşaltılır (`/free`); elle müdahale gerekmez.
- Bekçi, iş öncesi boş RAM'e bakar (ram_gb = K6 tepe + 2): zimage 4.4 · klein 4.5 · buyut 3.5 GB; `ac` en küçüğünü ister.
  Yetmezse exit 2 ve tek satır; listedeki altyapı (node, claude, python, uv, dotnet, MsMpEng…) kapatma önerisi değildir.
- Acil fren: kuyrukta boş RAM 2 GB altına inerse ComfyUI PID ile kapatılır, exit 1.

## Kurallar
- Çıktı yalnız `C:\Users\pc\Desktop\<Proje>\` altına; dışı → 2. Her PNG'nin yanına meta .json (model · lisans · prompt · tohum · süre).
- Yalnız 127.0.0.1; dinleme 127 dışındaysa süreç PID ile kapatılır → 1. Ad ile öldürme yasak.
- Model kurulu değilse DUR (exit 2); modeller ve lisanslar: `docs/gorsel/modeller.md`, ölçüm: `docs/gorsel/olcum.md`.

| exit | anlam |
|------|-------|
| 0 | tamam |
| 1 | ComfyUI hatası/zaman aşımı · acil fren · 127 dışı dinleme |
| 2 | geçersiz girdi/yol · 8188 ya da 9876 dolu · model kurulu değil · ComfyUI kapalı · RAM yetmez |
