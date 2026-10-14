# VİDEO-3 — ara rapor d1 (14 Eki ~18:50) KABUL DEĞİL
Katalog: kullanılan [video CLI içi araçlar (kisa.izle/_uret/metin_gec/paket_linkleri, tarama.normal, altin.puan), docs/video-tarama/altin (6 doğrulanmış altın), .kos/*/defter.jsonl, arka.py, bekle.py] · atlanan [plan-kur/katalog_ara (tek alan, hattın kendi araçları yeterli), alt ajan (kural 0), claude -p (d1'de 0/6)]

V1 ölç (`v3.py olc`, 689 YouTube + 1033 IG video, eski hat defterleri):
- Jetonun %99.7'si tek adımda: tarama (sonnet+haiku). Uzun video başı ~383k ağır, kısa ~182k.
- Tarama içi en büyük 3 kalem (uzun): rapor yazımı (çıktı ×5) %72 · kare %14 · metin+sabit istem %13. Kısa: rapor yazımı %76 · metin+sabit %20 · kare %3.
- Sonuç: önce rapor yazımı (Claude tam form yazıyor) → Gemini JSON'a taşınır, Claude yalnız kısa karar JSON'u; kare zaten Gemini'de.

V2 uzun video (önce/sonra, altın 6; taban = eski hattın son formu, `v3/taban.json`):
- Taban araç yakalama: 1nGx 12/18 · aZe5 14/22 · d_UE 3/13 · FaCh 8/16 · HYMD 39/39 · YDAK 5/27 (toplam 81/135 = 0.60); ağır jeton 60k–635k/video, süre 33–364 sn.
- Yeni: tools/video/video/uzun.py — ≥25 dk videoda 20 dk'lık videoMetadata aralıkları (2 eşzamanlı, düşük çözünürlük), birleştirme tekrarsız, aralık önbelleği. Gemini koşusu 4/6 (14–17 sn/video, Claude 0); HYMD/YDAK ücretsiz kota 429 → puan d2'de.
- Testler: tests/test_uzun.py 3/3 yeşil (birleştirmede dizi dönen ekran_metni hatası koşuda yakalandı, düzeltildi).
V3/V4/V5: başlanmadı. Devir: devir/video-3-devam.md.
