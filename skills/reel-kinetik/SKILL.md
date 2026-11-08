---
name: reel-kinetik
description: "Kinetik altyazılı + sesli kısa dikey reel (1080x1920 mp4) üretir: metin → TTS ses → kelime zamanları → Remotion render. Reel/short/kinetik altyazı isteğinde kullan."
---
# reel-kinetik — metinden kinetik altyazılı reel

Şablon: `sablon/` (Remotion 4 + React; kendi yazımımız, OpenMontage kodu kopyalanmadı — OpenMontage AGPL-3.0, koda dokunulacaksa kaynak açma yükümlülüğü doğar).
Kurulum (bir kez, CC'de): şablonu bir çalışma klasörüne kopyala (ör. `araclar\reel-kinetik`), `npm install`. Chrome headless ilk render'da iner.
Akış:
1. `python hazirla.py "<metin>"` → `public/ses.wav` (Windows SAPI sesi; Türkçe ses kuruluysa Türkçe, değilse İngilizce) + `reel.json` (kelime zamanları kelime uzunluğuna orantılı; gerçek hizalama için whisper kullan).
2. `npx remotion render src/index.tsx Reel out/reel.mp4 --props=reel.json`
3. Kareyi doğrula: `npx remotion still src/index.tsx Reel out/kare.png --props=reel.json --frame=45`.
Gerçek koşu (27 Eki): "Free tools can build a real reel in one minute" → 3,7 sn, 1080x1920 h264 + aac, 378 KB; altyazı 3'lü kayan pencere, aktif kelime büyür/renklenir.
Sınır: yalnız CC (Node + Chrome + SAPI); claude.ai sandbox'ında render yok, orada yalnız `Reel.tsx`/`hazirla.py` metni verilir. Daha zengin sahne/müzik için `reel-plan`, `reel-taste`, `reel-export`, `remotion-*` skill'leri.
