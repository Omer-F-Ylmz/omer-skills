# FREEFIELD-H3 raporu (7 Kas)

- Modeller: `C:\AI\ComfyUI\models` altında (indirme betiği `.kos/kopru/tmp/h3_dl.py`, ilerleme `h3_ilerleme.txt`).
- Hazır (boyut): fl2va int8 diffusion 20.97 GB · Qwen3VL-32B H3 nvfp4_awq text encoder 15.69 GB · video VAE fp16 5.21 GB · sol_h3_vae fp16 3.60 GB · audio VAE fp32 0.61 GB · latent upscaler 3d-conv 0.69 GB · turbo 4-step LoRA 1.96 GB · regenerate r128 LoRA 1.96 GB · open_h3_regenerate_2k LoRA 8.80 GB · face_yolov8m / person_yolov8m-seg (FaceRefine/Extender yardımcıları).
- `.incoming_h3` içinde 6.09 GB artık (eski yarım dosya `.incomplete`) duruyor; silme yok, dokunulmadı. `rmtree` pack indiricisinin kendi işi; bu betikte yok.
- Not: packs/video-h3.json yalnız int8 text encoder + int8 video VAE listeliyor; ikisi yerelde yok. Test için workflow kopyasında nvfp4 text encoder + fp16 VAE kullanıldı (app dosyası değişmedi).
- Test: h3-video workflow (kopya, `.kos/kopru/tmp/h3_test.py`) + turbo 4-step LoRA, 4 adım, 608x352, istek 4 sn → 107 kare / 4.46 sn / 24 fps, h264+aac. Süre 225 sn. Çıktı `C:\AI\ComfyUI\output\freefield\h3-test4s_00001_.mp4`.
- Kareler: ffmpeg ile 0/35/70/105 çıkarıldı (`.kos/kopru/tmp/h3_kareler/serit.png`); tilki karelerde tutarlı, kamera ileri, bozulma yok.
- VRAM: 10.6/12.3 GiB sonda (~%86; tepe ölçülmedi, başta 8.7 GiB başka süreçlerden). Hedef ≤%80 aşılmış olabilir: ölçülemedi + neden: örnekleme tepe değeri kaydedilmedi.
- Disk: C: 107 GB boş (eşik 80).
- Test edilmeyenler: extend-video, h3-photo, reshoot (reshoot ref2va diffusion + MoGe + CrossViewWarp indirilmedi).
- Kullanılan: ComfyUI :8188 API, ffmpeg, hf_hub, Read. Kullanılmayan kurulu araç gerekçesi: tek betikli indirme/test işi.
