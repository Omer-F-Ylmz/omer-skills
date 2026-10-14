# SİTE-OKULU-2 devam (14 Eki 21:15, d3 ara kayıt — çağrı tavanı 45)
graphify update omer-skills'te 3.5 GB RAM yedi — bu işte graphify update KOŞMA.

## Yapılan (d1 e85cabf1 + d2 65b0c9b6 + d3)
- K7 modülleri `tools/site-kit/sablon/src/sahne/`: kamera-yolu · dongu · post · gecis · metin · yukleyici · parcacik. Lab'lar `labs/<teknik>/`, koşucu `python labs/kare.py <teknik>...`.
- d3 yargı (`labs/kare.py`): Gemini temp 0 × KOSU=3 → medyan (`<alan>_kosular` olcum.json'da) + ikinci bağımsız yargıç OmniRoute `openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` (yedek gemma-4 :free; A/B 4'lü ızgara, 2 görsel). Rubrik: `mekanizma` (kapı ≥9) + `icerik` (yalnız not). TAVAN 12 Gemini çağrısı/koşu (= 4 teknik).
- d3 gecis.js: çapraz cephe → merkezden açılan portal (en-boy düzeltmeli yarıçap + fbm), ince hale + radyal kırılma/kromatik ayrışma; lab'da portal pencere %70 + A'ya dalış / B'de geri çekilme dolly.
- d3 yukleyici.js: `{ enAz = 2 }` — önbellekte yükleme anında bitince sayaç görünmüyordu (kök neden); sayaç en az enAz sn'de 100'e varır.

## Eşleşme (mekanizma: Gemini 3 koşu · nemotron · kendi bakışım)
- gecis: [8,7,7] med 7 · 8 · portal halkası + kırılma okunuyor; kalan farkların 2/3'ü içerik (parçacık/sis yoğunluğu, organik modeller) → icerik 5. 4 tur doldu, kapanmış say.
- yukleyici (d3 tur 1): [7,7,7] · 4 · sayaç artık karede (076), perde+dolly+harf girişi görünüyor; fark "perde/sayaç eğrisi standart, organik ivme yok". 1 tur hakkı kaldı: perdeye fbm kenarlı SVG/shader maske ya da sayaç rakamlarının dikey kayması.
- Eski tek-koşu puanları (d1/d2, temp 0.2): kamera-yolu 8 · post 9 · metin 9 · parcacik ~8 — yeni yargıyla yeniden ölçülmedi.
- Yargıçlar arası fark ±4 (yukleyici 7 vs 4): tek model karar değil; kapı = Gemini medyanı ≥9 VE kendi bakış.

## Kalan (sıra)
1. yukleyici tur 2 (son) → makro sıvı/köpük (TELVE S1 kullanıyor; `sahne/sivi-glsl.js` zaten var, önce oku) → ses (Tone/howler, kullanıcı açar) → tek renderer çok sahne.
2. Yeni yargıyla kamera-yolu/post/metin/parcacik yeniden ölçüm (12 çağrı = 1 koşu).
3. dist zip: `python tools/skill-paket/paketle.py web-sahne-desenleri "<konu>" dist/claude-ai-25 skills/web-sahne-desenleri` → `zip_denetle.py dist/claude-ai-25` temiz; CC onay betiği; lab-*.md zip'e (yerel yola bağlı kalmamalı). lab-gecis.md / lab-yukleyici.md d3 değişikliklerine göre güncellenmeli.
4. GSAP 3.15 lisansı: standart ücretsiz lisans (MIT değil), ticari kullanım serbest, GSAP'a rakip araçta yasak — kapanış raporuna.
