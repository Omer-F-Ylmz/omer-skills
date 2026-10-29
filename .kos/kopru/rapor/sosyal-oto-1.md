---
type: summary
status: active
tags: [sosyal-oto, shorts, faceless, ara-kayit]
relatedTo: [SOSYAL-OTO-1]
---
# SOSYAL-OTO-1 — ara kayıt (tur 1, çağrı tavanı 45/45)

## Durum
- (a) Araştırma TAMAM: rapor/sosyal-oto-1/arastirma.md (alt ajan, ~25 web çağrısı, kaynaklı). Önemli: YT "inauthentic" (2025-07-15) okuma-tipi içeriği dışlar → B kendi anlatımımız; TikTok Creator Rewards >60 sn ister → TikTok kesimi 61 sn+; IG 2026-04-30'dan beri özgün olmayanı önermiyor; YT Shorts geliri 1000 abone + 10M görüntüleme/90 gün (2027-02-01'den yeni başvuru 20M).
- (b) Plan + Roast Room TAMAM: sosyal-oto/PLAN.md, .roast-room/2026-10-30-sosyal-oto-1.md. 4 persona S1 (yerel ffmpeg) seçti; 7 zorunlu düzeltme kayıtlı.
- (c) Prototip YARIM: sosyal-oto/hat.py (+kokoro_tts.py, kelime.py) yazıldı.
  - B koşusu: Wikimedia küçük resim 429 → düzeltildi (standart 1280 genişlik, UA, geri çekilme); yeniden koşulmadı.
  - A koşusu: ucretsiz_havuz tüm halkalar 429/soğuma (01:45) → OmniRoute nemotron :free yedeği eklendi; upscayl.org koşusu arka planda başladı, sonucu ölçülmedi.
  - Hakem puanı: henüz yok (video üretilmedi).
- (d) TAMAM: sosyal-oto/OMER-ADIMLAR.md.

## Devam (yeni oturum)
1. log-a.txt kontrol; out/a/<kimlik>/meta.json puanı.
2. `python -I hat.py b --n 2`, `python -I hat.py a https://jan.ai`.
3. Her grup 2 video, hakem ≥70 değilse en iyi + neden raporla; kare ızgarası hakem-izgara.jpg.
4. TikTok 61 sn+ varyantı (kelime sınırı 150–175) ayrı bayrak.

## Ek (A koşusu sonucu)
- upscayl: nemotron yedeği metni yazdı, Kokoro sesi üretildi (ses-kokoro.wav 1.9M); whisper GPU cublas64_12.dll yok diye düştü → kelime.py CPU yedeği eklendi, yeniden koşulmadı.

## Tur 2 (30 Eki 02:20, çağrı tavanı yine doldu)
- GPU kelime zamanı ÇÖZÜLDÜ: nvidia-cublas/cudnn pip paketleri zaten kuruluydu, DLL dizini PATH'te değildi; kelime.py başına os.add_dll_directory(site-packages/nvidia/*/bin) eklendi. Ölçüm: upscayl ses-kokoro.wav → 112 kelime, gpu, 53 sn (model yükleme dahil). CPU yedeği duruyor.
- Metin adımı ÇÖZÜLDÜ: nemotron-nano düşünme jetonuyla max_tokens'u yiyip içerik boş dönüyordu → "reasoning": {"enabled": False} (260 jeton, geçerli JSON). Ret olunca 3 geri bildirimli deneme eklendi; nano 73–84 kelime yazıyor → alt sınır 95→75 (~30 sn). Metinde gerçek-dışı ayrıntı riski (War of the Worlds testinde "çiftçi" uydurdu): hakem/olgu kontrolü şart.
- Video HÂLÂ YOK: montaj aşaması ffmpeg'de düşüyor. A: "Error reinitializing filters" (-22, libx264 açılmadı); B: montaj_b ffmpeg rc 3221225477 (0xC0000005) stderr boş. Hakem puanı yok, mp4 yok.
- Sonraki oturum: (1) hat.py montaj_a/montaj_b filtre dizgisini `ffmpeg -v error` ile tek tek yokla (görsel boyutu tek sayı? zoompan/boxblur girdisi? Wikimedia dosyası bozuk mu?); (2) sonra `hat.py a https://upscayl.org https://jan.ai`, `hat.py b --n 2`; (3) hakem. Not: arka.py+kos2.py yoluyla koşuda hat.py rc 1 veriyordu; doğrudan `python -I hat.py ...` çalışıyor (run_in_background).
