# Claude can't generate video. It can still edit yours. 🎬
## Künye
Claude can't generate video. It can still edit yours. 🎬 · claudetipsandtricks · süre: 0:00 · ? · https://www.instagram.com/p/DeHGj-mG-5V/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-9 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 28867 tk · claude-haiku-5-5: claude-haiku-5-5 · 38460 tk
## Özet
Instagram kaydırmalı gönderi (8 slayt): Claude Opus 5.5 yalnızca metin ürettiği için video kurgusunu kod olarak yazar. Tek bir HTML sahnesi her t anını çizer, Playwright kareleri yakalar, ffmpeg bunları H.264 MP4'e birleştirip sesi ekler. Hareketli grafikler, TTS ile seslendirme, transkriptten kaba kurgu ve sınırlar (yüz/hayvan için gerçek görüntü, fiziksel doğru ışık) anlatılır.
## Bölümler
- 0:00 Kapak: Opus 5.5 – Video for Editors
- 0:00 1. Nasıl çalışır: HTML sahnesi + Playwright döngüsü
- 0:00 2. Hareketli grafikler (Remotion / HyperFrames)
- 0:00 3. Ses ve seslendirme (TTS, MCP)
- 0:00 4. Transkriptten kurgu
- 0:00 5. Kurulum: Playwright, ffmpeg
- 0:00 6. Sınırlar
- 0:00 Kapanış: takip çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Opus 5.5 | yok | teknik | yok | Yalnızca metin üreten ve kurguyu kod olarak yazan ana yapay zekâ modeli | 0:00 | Kapakta 'OPUS 5.5'; slayt 2: 'Opus 5.5 outputs text only.' · kanıt: kare (karede: Kapakta OPUS 5.5 rozeti, 2. slaytta Opus 5.5 metni) |
| Claude | yok | teknik | yok | Betik yazan, TTS çağıran, kesim yapan asistan | 0:00 | 'Claude writes the script, then calls a TTS engine' (karede: 4. slayt metni) |
| HTML scene | yok | teknik | yok | Herhangi bir t anındaki kareyi çizen tek HTML sahnesi | 0:00 | 'Write one HTML scene that renders any frame at time t' (karede: 2. slaytta 'Write one HTML scene' kartı) |
| Playwright | yok | CLI | yok | Sahneyi kare kare ilerletip ekran görüntüsü alan yakalama döngüsü | 0:00 | 'Playwright steps the scene frame by frame.' (karede: 6. slayt: Playwright vurgulu, npm i -D playwright) |
| Chromium | yok | CLI | yok | Playwright'ın kullandığı tarayıcı | 0:00 | 'npx playwright install chromium' (karede: 6. slayt kartında npx playwright install chromium) |
| ffmpeg | yok | CLI | yok | Ekran görüntülerini H.264 MP4'e birleştirip sesi ekler | 0:00 | 'ffmpeg stitches those screenshots into an H.264 MP4' (karede: 6. slaytta ffmpeg vurgulu, brew install ffmpeg) |
| H.264 | yok | teknik | yok | Çıktı video codec'i (MP4) | 0:00 | 'into an H.264 MP4 and muxes in your audio' (karede: 6. slayt açıklama metni) |
| Remotion | yok | teknik | yok | Uzun açıklayıcı videolar için kompozisyon çerçevesi | 0:00 | 'ask for a Remotion or HyperFrames composition' (karede: 3. slayt metni) |
| HyperFrames | yok | teknik | yok | Remotion alternatifi kompozisyon seçeneği | 0:00 | 'ask for a Remotion or HyperFrames composition' (karede: 3. slayt metni) |
| TTS engine | yok | MCP | yok | MCP bağlayıcısı üzerinden çağrılan seslendirme motoru | 0:00 | 'calls a TTS engine through an MCP connector' (karede: 4. slaytta TTS engine vurgulu) |
| MCP | yok | MCP | yok | TTS motoruna bağlanma yolu | 0:00 | 'through an MCP connector' (karede: 4. slayt metni) |
| Lower third | yok | teknik | yok | İsim/unvan alt bantları HTML sahnesi olarak | 0:00 | 'Build a lower third' (karede: 3. slayt kartı) |
| Kinetic titles | yok | teknik | yok | Hareketli başlıklar HTML sahnesi olarak | 0:00 | 'Lower thirds and kinetic titles come out as HTML scenes' (karede: 3. slayt metni) |
| Transcript tabanlı kurgu | yok | iş akışı | yok | Ham görüntüyü yazıya çevirip metinden kesme, kendi render'ını kontrol etme | 0:00 | 'Transcribe the raw footage first. Claude cuts from the text' · kanıt: kare (karede: 5. slayt metni) |
| Word timestamps | yok | teknik | yok | Kelime zaman damgalarıyla hareketleri sese oturtma | 0:00 | 'Ask for word timestamps so every motion beat lands on the voice' (karede: 4. slayt metni) |
| npm | yok | CLI | yok | Playwright'ı kuran paket yöneticisi | 0:00 | 'npm i -D playwright' (karede: 6. slayt kartı) |
| Homebrew | yok | CLI | yok | ffmpeg'i kuran paket yöneticisi | 0:00 | 'brew install ffmpeg' · kanıt: kare (karede: 6. slayt kartı) |
| brew | yok | CLI | yok | Homebrew paket yöneticisi; ffmpeg'i kurmak için kullanılır. | 0:00 | Slayt 6: 'brew install ffmpeg' (karede: Slayt 6 kartının son satırında 'brew install ffmpeg' komutu.) |
| Lower third hareketli grafik | yok | prompt | yok | İsim ve unvan içeren bir lower third yap: 2 sn'de girsin, 4 sn dursun, marka renklerimle. | 0:00 | kaynak: kare |
| Sese senkron | yok | prompt | yok | Seslendirmeyi kelime zaman damgalarıyla üret; her vuruşu bir kelimeye denk getirerek kes. | 0:00 | kaynak: kare |
| Kaba kurgu | yok | prompt | yok | interview.mp4'ü yazıya çevir, dolgu sözleri at, en iyi 60 saniyeyi tut. | 0:00 | kaynak: kare |
| Aşırı pozlanmayı önleme | yok | prompt | yok | Fiziksel olarak doğru ışıklandırma kullan; bloom ve patlamış parlak alan olmasın. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm i -D playwright | Playwright'ı geliştirme bağımlılığı olarak kurar (karede: 6. slayt kartında komut) | 0:00 | kare |
| npx playwright install chromium | Playwright için Chromium tarayıcısını indirir (karede: 6. slayt kartında komut) | 0:00 | kare |
| brew install ffmpeg | ffmpeg'i Homebrew ile kurar (karede: 6. slayt kartında komut) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Opus 5.5 yalnızca metin üretir; kurguyu kod olarak yazar, bir çekimi değiştirmek bir satırı değiştirmektir ve her render aynı çıkar. | 0:00 | özellik |
| Yüzler ve hayvanlar yakından kaba şekillerle render edilir; insanlar için gerçek görüntü kullanılmalı. | 0:00 | öneri |
| Uzay sahneleri aşırı pozlanmaya eğilimlidir; gerçek renkler istenmeli. | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 · 0:00 | OPUS 5.5 | Claude Opus 5.5 | Kapak rozeti OPUS 5.5 |
| kare 2 · 0:00 | HTML scene | HTML scene | 'Write one HTML scene' |
| kare 2 · 0:00 | Playwright capture loop | Playwright | 'then a Playwright capture loop' |
| kare 3 · 0:00 | Remotion | Remotion | 'a Remotion or HyperFrames composition' |
| kare 3 · 0:00 | HyperFrames | HyperFrames | 'a Remotion or HyperFrames composition' |
| kare 3 · 0:00 | lower third / kinetic titles | Lower third | 'Build a lower third' |
| kare 4 · 0:00 | TTS engine | TTS engine | 'calls a TTS engine' |
| kare 4 · 0:00 | MCP connector | MCP | 'through an MCP connector' |
| kare 4 · 0:00 | word timestamps | Word timestamps | 'Ask for word timestamps' |
| kare 5 · 0:00 | transcript ile kesim | Transcript tabanlı kurgu | 'Transcribe the raw footage first' |
| kare 6 · 0:00 | ffmpeg | ffmpeg | 'brew install ffmpeg' |
| kare 6 · 0:00 | chromium | Chromium | 'npx playwright install chromium' |
| kare 6 · 0:00 | npm | npm | 'npm i -D playwright' |
| kare 6 · 0:00 | brew | Homebrew | 'brew install ffmpeg' |
| kare 6 · 0:00 | H.264 MP4 | H.264 | 'an H.264 MP4' |
| kare 7 · 0:00 | Physically accurate lighting prompt | aday değil: genel kavram | Işık/bloom isteği prompt metni; promptlar'da |
| kare 7 · 0:00 | bloom / blown highlights | aday değil: genel kavram | 'No bloom, no blown highlights.' |
| açıklama | Claude | Claude | 'Claude can't generate video.' |
| açıklama | Anthropic | aday değil: konu dışı | Yalnızca hashtag olarak geçiyor |
| açıklama | @claudetipsandtricks | aday değil: konu dışı | Hesap takip çağrısı |
| açıklama | Next.js, Framer Motion, Emotion, Stitch | aday değil: konu dışı | Sözlük eşleşmesi; gönderide geçmiyor |
| yorum | yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 1 (0:00): Kapak: OPUS 5.5 / VIDEO for Editors; Instagram claudetipsandtricks
- 2 (0:00): 1. How it works; Write one HTML scene, Playwright capture loop; Page 2/8
- 3 (0:00): 2. Motion graphics; Build a lower third; Remotion/HyperFrames; Page 3/8
- 4 (0:00): 3. Audio and voiceover; TTS engine, MCP connector; Sync to voice; Page 4/8
- 5 (0:00): 4. Cut from a transcript; Rough cut; interview.mp4; Page 5/8
- 6 (0:00): 5. Install the stack; npm i -D playwright, npx playwright install chromium, brew install ffmpeg
- 7 (0:00): 6. Know the limits; Physically accurate lighting, no bloom; Page 7/8
- 8 (0:00): One Claude tip, every day; Follow @claudetipsandtricks; save
## Belirsizlikler
- Video değil görsel gönderi; tüm zamanlar 0:00 olarak verildi, gerçek zaman yok.
- Açıklamada geçen Next.js, Framer Motion, Emotion, Stitch sözlük eşleşmeleri gönderide anılmıyor; aday yapılmadı.
- 'Opus 5.5' model adı gönderide yazıldığı gibi alındı, doğrulanamadı.
- Yorumlar girişsiz alınamadı.
- Kullanılan TTS motorunun adı belirtilmiyor.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/DeHGj-mG-5V/ | açıklama | açıklama | hayır |
## İş akışı
- yok
## Promptlar
- Lower third hareketli grafik — İsim ve unvan içeren bir lower third yap: 2 sn'de girsin, 4 sn dursun, marka renklerimle.
- Sese senkron — Seslendirmeyi kelime zaman damgalarıyla üret; her vuruşu bir kelimeye denk getirerek kes.
- Kaba kurgu — interview.mp4'ü yazıya çevir, dolgu sözleri at, en iyi 60 saniyeyi tut.
- Aşırı pozlanmayı önleme — Fiziksel olarak doğru ışıklandırma kullan; bloom ve patlamış parlak alan olmasın.
ikinci göz KAPALI: --ikinci-goz yok
