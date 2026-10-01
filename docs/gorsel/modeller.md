# Görsel modelleri (KURULUM-GÖRSEL, 2026-10-01)

Konum `C:\AI\ComfyUI\models\<alt>\`. sha256 HF LFS değeriyle indirme sonrası yerelde doğrulandı. Hepsi kapısız (HF `gated: false`).

| Dosya | Alt | Boyut (bayt) | sha256 | Lisans | Kaynak |
|---|---|---|---|---|---|
| z_image_turbo_bf16.safetensors | diffusion_models | 12309866400 | 2407613050b809ffdff18a4ac99af83ea6b95443ecebdf80e064a79c825574a6 | Apache-2.0 | https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors |
| z_image_turbo_fp8_e4m3fn.safetensors | diffusion_models | 6155996016 | 6a089a94935944d827fd5e454005d0353ee7ebbeec8de45d80325df68d0c1b25 | Apache-2.0 | türetilmiş: kaynak z_image_turbo_bf16 (sha256 2407613050b8…74a6) + tools/gorsel/fp8_cevir.py; 210/453 tensör fp8, çevirme tepe RAM 7.8 GB |
| qwen_3_4b.safetensors | text_encoders | 8044982048 | 6c671498573ac2f7a5501502ccce8d2b08ea6ca2f661c458e708f36b36edfc5a | Apache-2.0 | https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/text_encoders/qwen_3_4b.safetensors |
| qwen_3_4b_fp8_mixed.safetensors | text_encoders | 5631994051 | 72450b19758172c5a7273cf7de729d1c17e7f434a104a00167624cba94f68f15 | Apache-2.0 | https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/text_encoders/qwen_3_4b_fp8_mixed.safetensors |
| ae.safetensors | vae | 335304388 | afc8e28272cd15db3919bacdb6918ce9c1ed22e96cb12c4d5ed0fba823529e38 | Apache-2.0 | https://huggingface.co/Comfy-Org/z_image_turbo/blob/main/split_files/vae/ae.safetensors |
| flux-2-klein-4b.safetensors | diffusion_models | 7751105712 | ec3d4e733a771f61c052fb4856c48b336c55eaf2c65487c2a1faeb9bbda7a343 | Apache-2.0 | https://huggingface.co/Comfy-Org/flux2-klein-4B/blob/main/split_files/diffusion_models/flux-2-klein-4b.safetensors |
| flux2-vae.safetensors | vae | 336211292 | 868fe7b343cc8f3a19dbcfcafbc3d5f888802be3f89bd81b65b3621a066ce8f3 | Apache-2.0 | https://huggingface.co/Comfy-Org/flux2-klein-4B/blob/main/split_files/vae/flux2-vae.safetensors |
| RealESRGAN_x4plus.safetensors | upscale_models | 66857836 | 37f9a931c215f040aa6d50f711f2cb115f713c46df1d0d6469a8bd7bfe9a60bb | BSD-3-Clause | https://huggingface.co/Comfy-Org/Real-ESRGAN_repackaged/blob/main/RealESRGAN_x4plus.safetensors |
| birefnet-general.onnx (rembg) | `~\.u2net\` | 972666916 | 58f621f00f5d756097615970a88a791584600dcf7c45b18a0a6267535a1ebd3c | MIT | https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-general-epoch_244.onnx |

- `qwen_3_4b.safetensors` Comfy-Org/flux2-klein-4B'de de aynı sha256 → bir kez indirildi, iki model ortak kullanır.
- klein: yalnız 4B distilled. 9B ve [dev] BFL sözleşmesi ister → indirilmedi.
- Real-ESRGAN: resmi safetensors yeniden paketlemesi; .pth kullanılmadı.

## Kurulmayan
- **Qwen-Image (K2b):** kurulmadı. Koşul RAM ≥32 GB ve boş disk ≥80 GB; ölçülen RAM 31.7 GB (disk 299 GB yeterliydi). `metinli` iş türü K6 ölçümündeki 4. prompt kazananına yönlendi.
- **rembg varsayılanı bria-rmbg:** ticari lisans ister → indirilmedi; araç her zaman `-m birefnet-general`.
