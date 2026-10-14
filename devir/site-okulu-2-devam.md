# SİTE-OKULU-2 devam (14 Eki 20:50, d2 ara kayıt — çağrı tavanı 45)

## Yapılan (d1 e85cabf1 + d2)
- K7 modülleri `tools/site-kit/sablon/src/sahne/`: kamera-yolu · dongu · post · gecis · metin · yukleyici · parcacik. Lab'lar `labs/<teknik>/`, koşucu `python labs/kare.py <teknik>...` (Gemini 1 çağrı/teknik).
- d2: gecis.js kenarı yeniden (çapraz cephe + fbm, çekirdek/hale/kıvılcım, kromatik ayrışma); yukleyici koreografisi (çubuk, yuvarlak perde, dolly hedefi başlıktan uzak, alt başlık) + modülde `acildi` (giriş bir kez); metin labı kontrast düzeltmesi (mix-blend difference → koyu zemin; dev tipe açık arka plan; impeccable detect temiz, susturma yok).
- `docs/site-okulu/lab-*.md` ×6 (modül koduna karşı doğrulandı; uygulanmayan mobil düşüşler "önerilen" diye işaretli).
- web-sahne-desenleri §6'ya modül + lab notu atfı (repo).

## Eşleşme puanı (Gemini 0-10; kendi bakışım ayrı)
kamera-yolu 8 · post 9 · metin 9 (d2 yeniden ölçüldü) · parcacik ~8 · gecis 7 (4 tur tavanı doldu: 7→7→4→7; B kamerasını aynı cezveye çevirmek 4 verdi, geri alındı) · yukleyici 7 (d2 tur 2, değişmedi).
Kendi bakışım (gecis kareleri): kenar ışıması artık açık görünüyor; kalan fark referansın parçacık yoğunluğu/3B içerik zenginliği — geçiş mekanizması değil. Gemini tek seferde ±3 oynuyor (aynı kod 7 ve 4 değil ama komşu sürümler); tek koşu güvenilir yargıç değil.
pixeljury CC'de yalnız `--provider mock` → yargıç olarak kullanılamadı.

## Kalan (sıra)
1. yukleyici tur 3-4: Gemini farkı "tipografi sahnesi + renk geçişi daha cesur" — kıyas karesine bak (`dist/site-okulu/yukleyici-kiyas.jpg`), ≤2 tur.
2. dist zip: `python tools/skill-paket/paketle.py web-sahne-desenleri "<konu>" dist/claude-ai-25 skills/web-sahne-desenleri` → `python tools/skill-paket/zip_denetle.py dist/claude-ai-25` temiz; CC onay betiği; lab-*.md'leri zip'e alıp almama kararı (skill yerel yola bağlı kalmamalı).
3. Yapılmayan teknikler: makro sıvı/köpük, ses (Tone/howler, kullanıcı açar), tek renderer çok sahne.
4. TELVE-R3b sinyali: kamera-yolu + post hazır (8/9) → SIRA'ya "SİTE-OKULU-2 ara: kamera-yolu/post R3b'ye hazır (tools/site-kit/sablon/src/sahne/)" yazılmalı (d2'de SIRA bulunamadıysa ilk iş).
5. GSAP 3.15 lisansı: standart ücretsiz lisans (MIT değil), ticari kullanım serbest, GSAP'a rakip araçta yasak — kapanış raporuna.
