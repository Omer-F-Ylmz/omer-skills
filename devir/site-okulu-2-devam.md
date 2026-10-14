# SİTE-OKULU-2 devam (14 Eki, ara kayıt — çağrı tavanı 45)

## Yapılan
- K7 modülleri (`tools/site-kit/sablon/src/sahne/`, .js — sivi-glsl.js emsali): kamera-yolu · dongu (talep üzerine render) · kademe · post · gecis · metin · yukleyici · parcacik. K7 package.json'a `postprocessing` (Zlib) eklendi.
- Lab'lar `labs/<teknik>/index.html` (ortak.js: tornalanmış cezve/fincan, köz, sis — kendi varlığımız; importmap → labs/node_modules). Koşucu `python labs/kare.py [teknik...]` (headless d3d11 RTX 4070 Ti, Gemini 1 çağrı/teknik, TAVAN 8).
- Kıyas kareleri `dist/site-okulu/<teknik>-kiyas.jpg` (üst = referans, alt = biz); ölçüm + Gemini notu `labs/<teknik>/olcum.json`.

## Eşleşme puanı (Gemini, 0-10, ilk tur)
kamera-yolu 8 (igloo) · post 9 (lusion) · gecis 7 (activetheory) · metin 9 (lando) · yukleyici ~7 · parcacik ~8 (çıktı sıkıştı; kesin değer olcum.json'da).
Ölçüm: talep üzerine render sayfalarında boşta 0 kare/sn (kamera, gecis, metin); sürekli döngüde 60 fps (post yüksek + düşük, parcacik 256² ve 96²). Sayfa hatası 0.

## Kalan (sıra)
1. Kıyas karelerine bak (teknik başı ≤1 görüntü okuma), olcum.json `oneriler` ile tur 2 (≤4 tur), en zayıf önce: gecis (7).
2. `docs/site-okulu/lab-<teknik>.md` ×6 (≤20 satır: işe yarayan, tuzak, mobil düşüş, maliyet). Tuzaklar şimdiden: Windows http.server .js→text/plain (kare.py düzeltir); DoF + kromatik tek EffectPass'te birleşmez; postprocessing RT'de ton eşleme yok → ToneMappingEffect; kisa.anahtar için tools/jev sys.path'te olmalı.
3. Yapılmayan teknikler: makro sıvı/köpük malzemesi, ses tasarımı (Tone/howler), tek renderer çok sahne.
4. web-sahne-desenleri skill'ine modül atıfları + dist zip (zip_denetle temiz) + CC onay betiği; Desktop kıyas karelerini Ömer'e gösterir.
5. pixeljury/kör puan yapılmadı (Gemini tek yargıç); metin lab'ında impeccable low-contrast uyarısı (mix-blend difference metni) açık.
