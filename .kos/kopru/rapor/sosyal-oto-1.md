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
