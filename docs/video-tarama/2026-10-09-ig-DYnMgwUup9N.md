# Comment “PYNK” and i send the workflow🤝
## Künye
Comment “PYNK” and i send the workflow🤝 · mr.pynk · süre: 0:38 · ? · https://www.instagram.com/reel/DYnMgwUup9N/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-38 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 27374 tk · claude-haiku-5-5: claude-haiku-5-5 · 31010 tk
## Özet
Kısa reel: Claude Code üzerinde kurulmuş özel bir sistemle marka URL'si verilerek 30 dakikada tam kampanya üretiliyor (marka DNA'sı, ürün görselleri, model görselleri, reklamlar). Örnek marka Rhode. Ekranda marka DNA'sı dosyası (renk, tipografi, fotoğraf stili), PYNK marka klasörü, karakter görsellerinin üretimi ve Rhode.com sitesi inşası görülüyor. Promptlar yorumda 'PYNK' yazanlara gönderilecek.
## Bölümler
- 0:00 Giriş: 30 dakikada tam marka kampanyası
- 0:05 Marka URL'sini Claude Code'a verme
- 0:10 Marka DNA'sı: renk, tipografi, fotoğraf stili
- 0:12 Ürün görselleri üretimi
- 0:18 Model/karakter görselleri üretimi
- 0:27 Rhode.com sitesi ve brand-dna-builder skill
- 0:29 Reklam görselleri ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Özel sistemin içinde çalıştığı ana yapay zekâ kodlama aracı | 0:00 | custom-built Claude code system |
| brand-dna-builder | yok | skill | yok | Marka DNA'sını çıkaran skill | 0:27 | Ekran metninde 'brand-dna-builder skill' satırı (karede: kanıttan) Ekran metninde 'brand-dna-builder skill' satırı |
| fal.ai | yok | MCP | yok | Görsel üretimi için kullanılan servis; FAL anahtarı kontrol ediliyor | 0:27 | 'FAL key is set' ekran metni (karede: kanıttan) 'FAL key is set' ekran metni |
| Python | yok | teknik | yok | Ürün görseli üretim betiği (generate-product-shot.py) | 0:12 | Read generate-product-shot.py (karede: Claude Code çıktısında 'Read generate-product-shot.py' satırı) |
| Marka DNA'sı çıkarma | yok | prompt | yok | Herhangi bir marka URL'si Claude Code'a bırakılır; sistem marka DNA'sını (renk, tipografi, fotoğraf stili) kilitler. | 0:00 | kaynak: altyazı |
| Rhode web sitesi kurma | yok | prompt | yok | Claude Code kuyruğunda 'Rhode.com website' inşa etme isteği bekliyor (Türkçe özet: Rhode için web sitesi oluştur). | 0:27 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Küçük harfli yuvarlak sans-serif başlık tipografisi (lowercase rounded sans-serif typography) | Marka DNA'sına göre başlık özel küçük harfli sans-serif, gövde hafif sans-serif geniş harf aralığıyla (karede: Typography bölümü: Headline custom lowercase sans-serif, Body light sans-serif generous tracking) | 0:28 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| ls [yol]/Ads/brands/PYNK/ | PYNK marka klasöründeki ürün ve referans dosyalarını listeler; ürün sayısı ve çekim kayıtları bu çıktıdan okunuyor. (karede: Bash çıktısında 'IN ls [yol]/Ads/brands/PYNK/' ve altında pole-guy-jacket, shot- satırları görünüyor.) | 0:12 | kare |
| ls [yol]/brands/ 2>/dev/null | Markalar klasörünü listeler; hata çıktısını gizler. Komutun tam metni kırpılmış görünüyor, '2>/dev,' olarak okundu. (karede: (karede OCR) nstall Python project d... Build Rhode.com website× * Build Rhode.com website www.rhode.com Thought for 1s > brand-dna-builder skill Thought for Os > Read SKILL. md Thought for 0s > Starting with Step) | 0:27 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Herhangi bir marka için 30 dakikada tam kampanya üretilebiliyor | 0:00 | sayısal |
| 29 ürün, 6 referans, 5 çekim var; 174 olası kombinasyon | 0:12 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Claude Code | Claude Code | custom-built Claude code system |
| kare 0:27 | brand-dna-builder skill | brand-dna-builder | brand-dna-builder skill |
| kare 0:27 | FAL | fal.ai | FAL key is set |
| kare 0:12 | generate-product-shot.py | Python | Read generate-product-shot.py |
| ekran 0:07 | www.rhode.com | aday değil: konu dışı | www.rhode.com |
| açıklama | Rhode markası | aday değil: konu dışı | We used Rhode |
## Kareden okunanlar
- 0:10: Color System: Lead warm cream #F5EEE6, Support stone gray #A09890, Accent soft blush #ea65e5ff, Background clean white #FAFAF8; Typography bölümü; yüzünde pembe gözlüklü sunucu
- 0:12: Claude Code terminali: markalar PYNK, allbirds, gymshark; 29 ürün, 6 referans, 5 çekim; 'Queue another message...' kutusu
- 0:28: Typography ve Photography Style bölümleri: ışık, renk derecesi, mekân, kompozisyon, mood
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Altyazıda 'pink' geçiyor; yorum anahtar kelimesi PYNK.
- fal.ai ekranda yalnız 'FAL key' olarak geçiyor; MCP mi API mi belli değil.
- Sözlükteki Next.js, Codex, Hermes Agent, context7, Lucide, Make eşleşmeleri bulanık; videoda kullanıldığı doğrulanmadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| www.rhode.com | 0:07 | ekran | hayır |
| Rhode.com | 0:27 | ekran | hayır |
## İş akışı
- 1. adım — Marka URL'sini Claude Code sistemine verme — araçlar: Claude Code
- 2. adım — Marka DNA'sını çıkarma (renk, tipografi, fotoğraf stili) — araçlar: Claude Code, brand-dna-builder
- 3. adım — Mevcut ürün ve referansları sayma, betikleri okuma — araçlar: Claude Code, Python
- 4. adım — Ürün görselleri üretme — araçlar: Claude Code, fal.ai
- 5. adım — Hedef kitleye uygun model görselleri üretme — araçlar: Claude Code, fal.ai
- 6. adım — Reklam görselleri üretme — araçlar: Claude Code
## Promptlar
- Marka DNA'sı çıkarma — Herhangi bir marka URL'si Claude Code'a bırakılır; sistem marka DNA'sını (renk, tipografi, fotoğraf stili) kilitler.
- Rhode web sitesi kurma — Claude Code kuyruğunda 'Rhode.com website' inşa etme isteği bekliyor (Türkçe özet: Rhode için web sitesi oluştur).
