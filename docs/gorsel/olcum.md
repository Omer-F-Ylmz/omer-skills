# K6 ölçümü — 2026-10-01 · RTX 4070 Ti 12 GB · 31.7 GB RAM

Yapılandırma (ölçülen = kullanılan): zimage `z_image_turbo_fp8_e4m3fn` (türetilmiş, weight_dtype default) · klein `flux-2-klein-4b` · iki model de `qwen_3_4b_fp8_mixed` kodlayıcı · ComfyUI v0.38 `--cache-ram` · 1024², tohum 42.
Tepe RAM = ComfyUI süreç ağacı çalışma kümesi (psutil, 1 sn örnekleme); acil fren 0,5 sn, 2 GB — tetiklenmedi.

| # | iş | zimage sn · VRAM MiB · RAM GB | klein sn · VRAM MiB · RAM GB |
|---|----|---|---|
| 1 | urun | 12.3 · 11382 · 2.4 | 8.3 · 11467 · 2.2 |
| 2 | foto (makro) | 15.2 · 11501 · 2.4 | 6.2 · 11545 · 2.2 |
| 3 | foto (barista) | 10.2 · 11374 · 2.4 | 5.2 · 11526 · 2.2 |
| 4 | metinli | 10.2 · 11469 · 2.4 | 8.2 · 11468 · 2.4 |
| 5 | doku | 10.2 · 11701 · 2.4 | 5.2 · 11437 · 2.4 |
| – | duzenle (referans) | – | 9.2 · 11592 · 2.5 |
| – | arkaplan (rembg, ComfyUI dışı) | 18.5 sn | |
| – | buyut x2 (1024² → 2048², Real-ESRGAN) | 7.2 · 5899 · 1.5 | |

**Model başına tepe RAM:** zimage 2.4 GB → `ram_gb` 4.4 · klein 2.5 GB → `ram_gb` 4.5 · buyut 1.5 GB → `BUYUT_RAM_GB` 3.5.

- Görseller: bozuk yok. Metin: zimage "TËLVE" (fazladan nokta), klein "TELVE · Türk Kahvesi" doğru.
- klein fp8 kodlayıcıyla hatasız; bf16 kodlayıcıya dönüş gerekmedi.
- buyut ayrı koşuyla ölçüldü (ilk koşuda bekçi varsayılanı 16 GB, boş 8.3 GB → exit 2); acil fren tetiklenmedi.
- Koşu sırasında bulunan hata: `kapat` portu bırakmadan dönüyordu → ardından gelen `ac` 8188'i yabancı sandı; `kapat` artık ≤15 sn port boşalmasını bekler (test).
