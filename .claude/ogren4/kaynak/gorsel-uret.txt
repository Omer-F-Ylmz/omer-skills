---
name: gorsel-uret
description: "Görsel üretme, düzenleme, büyütme, arka plan silme işinde önce yükle: yerel ComfyUI oturumunu CC yönetir; tools/gorsel_uret.py ac/uret/buyut/arkaplan/kapat. Yalnız Claude Code'da."
---

# gorsel-uret — yerel, ücretsiz görsel üretimi

Araç: `python C:\Projeler\omer-skills\tools\gorsel_uret.py <komut>` (mutlak yolla).

## Akış (sıra değişmez)
1. `ac` — ComfyUI 127.0.0.1:8188'de açılır (Blender açıksa 9876 dolu → 2; ikisi birlikte koşmaz).
2. `uret --is <iş> --prompt "..." --cikti C:\Users\pc\Desktop\<Proje>\... [--adet ≤4] [--tohum N] [--referans a.png ...]`
   `buyut <png> --kat 2|4` · `arkaplan <png>` (ComfyUI gerekmez).
3. `kapat` — yalnız durum dosyasındaki PID ile kapatır, port boşalana dek (≤15 sn) bekler.

İş yarıda kalsa da 3 çalıştırılır; sunucu açık bırakılmaz.

## Yönlendirme (K6 ölçümüyle)
| iş | model | neden |
|----|-------|-------|
| urun · foto · doku | zimage (Z-Image Turbo fp8) | fotogerçekçilik |
| metinli · duzenle | klein (FLUX.2 klein 4B) | metin doğru ("TELVE"), referansla düzenleme |
`--model` ile elle seçilebilir; `--referans` yalnız `duzenle` işinde.
Prompt her zaman İngilizce yazılır (Türkçe prompt Z-Image'da konudan sapar: "beyaz fonda seramik fincan" → ahşap masada kavanoz); görselin İÇİNE yazılacak metin (ör. "Türk Kahvesi") tırnak içinde aynen kalır.

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
