DESKTOP 00:10 HIZ (Ömer: Gemini'yi BEKLEME, elimizdekini kullan): yargıç kolu Gemini'siz de kurulur — PixelJury (`pixeljury review <url> --provider claude-code --json`, yerel CLI girişi, API anahtarı yok; ya da --provider ollama kuruluysa) + nemotron-omni :free + jev (MCP/CLI, LLM çıktı puanlama). Kör A/B, üç yargıç medyanı; kapı değişmez (mekanizma ≥9). Gemini 10:00 sonrası yalnız ek kol. Yükleyici teyidi ve 4 tekniğin yeniden ölçümü ŞİMDİ bu yargıçlarla. claude-code kolu plan kotasından yer — koşu başı en fazla 4 çağrı.
DESKTOP 00:05 (d5) — ÖNCE BU: gecis 'kapanmış say' KABUL DEĞİL — mekanizma kapısı ≥9 tutmadı (Gemini med 7, nemotron 8); kalite eşiği altında kapanış yok. gecis tavanı 4→6 tur: farkın 'içerik' sayılan kısmı (parçacık/sis yoğunluğu) geçişin mekanizmasına dahil — portal geçişinde parçacık/sis katmanı + organik ivme ekle, sonra ölç. Rubrik değişmez. Yargı çağrıları (Gemini) yalnız 15 Eki 10:00 TR sonrası (video ile ortak günlük kota — koşu başı TAVAN 12 korunur). d5 sırası: ses (kullanıcı açar, varsayılan kapalı) → tek renderer çok sahne → gecis tur 5 kodu → 10:00 sonrası: yükleyici Gemini teyidi + gecis + 4 tekniğin yeniden ölçümü → zip. graphify update KOŞMA (doğru). Commit yalnız kendi yolların; .impeccable/config.json bastırması dar kalsın.
# SİTE-OKULU-2 devam (14 Eki 23:50, d4 ara kayıt — çağrı tavanı 45)
graphify update omer-skills'te 3.5 GB RAM yedi — bu işte graphify update KOŞMA.

## Yapılan (d1 e85cabf1 + d2 65b0c9b6 + d3)
- K7 modülleri `tools/site-kit/sablon/src/sahne/`: kamera-yolu · dongu · post · gecis · metin · yukleyici · parcacik. Lab'lar `labs/<teknik>/`, koşucu `python labs/kare.py <teknik>...`.
- d3 yargı (`labs/kare.py`): Gemini temp 0 × KOSU=3 → medyan (`<alan>_kosular` olcum.json'da) + ikinci bağımsız yargıç OmniRoute `openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` (yedek gemma-4 :free; A/B 4'lü ızgara, 2 görsel). Rubrik: `mekanizma` (kapı ≥9) + `icerik` (yalnız not). TAVAN 12 Gemini çağrısı/koşu (= 4 teknik).
- d3 gecis.js: çapraz cephe → merkezden açılan portal (en-boy düzeltmeli yarıçap + fbm), ince hale + radyal kırılma/kromatik ayrışma; lab'da portal pencere %70 + A'ya dalış / B'de geri çekilme dolly.
- d3 yukleyici.js: `{ enAz = 2 }` — önbellekte yükleme anında bitince sayaç görünmüyordu (kök neden); sayaç en az enAz sn'de 100'e varır.

- d4 yukleyici tur 2 (son): sayaç kilometre sayacı gibi kayan basamak şeritleri (modül), perde = SVG sıvı dalga kenarı (lab); kök neden düzeltme: `#yuk span` seçicisi şeritleri 16 px yapıyordu → `#yuk > span`. kare.py örnek noktası .45→.38 (perde ortası).
- d4 sıvı/köpük: yeni lab YOK — `sivi-glsl.js` zaten crema/worley/advekte (TELVE kabul); `docs/site-okulu/lab-sivi.md` yazıldı.

## Eşleşme (mekanizma: Gemini 3 koşu · nemotron · kendi bakışım)
- gecis: [8,7,7] med 7 · 8 · portal halkası + kırılma okunuyor; kalan farkların 2/3'ü içerik (parçacık/sis yoğunluğu, organik modeller) → icerik 5. 4 tur doldu, kapanmış say.
- yukleyici d4 tur 2: Gemini 429 (günlük kota) · nemotron 9/9 (2 koşu) · kendi bakışım 9 (076 sayaç büyük, perde orta-dil dalga) → 4 tur kapalı. Gemini dönünce 1 koşu teyit.
- yukleyici (d3 tur 1): [7,7,7] · 4 · sayaç artık karede (076), perde+dolly+harf girişi görünüyor; fark "perde/sayaç eğrisi standart, organik ivme yok". 1 tur hakkı kaldı: perdeye fbm kenarlı SVG/shader maske ya da sayaç rakamlarının dikey kayması.
- Eski tek-koşu puanları (d1/d2, temp 0.2): kamera-yolu 8 · post 9 · metin 9 · parcacik ~8 — yeni yargıyla yeniden ölçülmedi.
- Yargıçlar arası fark ±4 (yukleyici 7 vs 4): tek model karar değil; kapı = Gemini medyanı ≥9 VE kendi bakış.

## d5 (15 Eki 00:10–00:40, çağrı 45 doldu)
- ses: `sahne/ses.js` + `labs/ses/` (Web Audio sentez, bağımlılık yok); `lab.olc()` 4/4 ✓ — `docs/site-okulu/lab-ses.md`. Görsel yargı yok (kare.py LAB'a girmedi).
- cok-sahne: `sahne/cok-sahne.js` + `labs/cok-sahne/` (shopify rafı, 9 sahne 1 tuval); `lab.olc()` ✓; kare.py LAB'a eklendi (ref shopify) — `lab-cok-sahne.md`.
- gecis tur 5 KODU yazıldı (gecis.js: duman bandı + dışa uçan közler + kayan yırtık + ivme eğrisi); kendi bakışım: portal halkası + sis + köz okunuyor. Yargılanmadı.
- Öz-denetim koşucusu repo dışında (%TEMP%/so2d5/olc.py): playwright ile `lab.olc()` çağırır — gerekirse kare.py'ye `--olc` olarak taşı.

## Kalan (sıra) — 10:00 TR sonrası
1. `python labs/kare.py gecis yukleyici cok-sahne` (TAVAN 12 = bu 3 + 1 yer) → gecis ≥9 değilse tur 6 (son hak).
2. Yeni yargıyla kamera-yolu/post/metin/parcacik yeniden ölçüm (12 çağrı = 1 koşu).
3. dist zip: `python tools/skill-paket/paketle.py web-sahne-desenleri "<konu>" dist/claude-ai-25 skills/web-sahne-desenleri` → `zip_denetle.py dist/claude-ai-25` temiz; CC onay betiği; lab-*.md zip'e (yerel yola bağlı kalmamalı). lab-gecis/yukleyici/sivi.md güncel (d4).
4. GSAP 3.15 lisansı: standart ücretsiz lisans (MIT değil), ticari kullanım serbest, GSAP'a rakip araçta yasak — kapanış raporuna.
