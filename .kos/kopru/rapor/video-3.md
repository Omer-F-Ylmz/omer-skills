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

## d2 ara (14 Eki ~19:25) KABUL DEĞİL
Katalog: kullanılan [kisa.izle/metin_gec/birlestir/paket_linkleri, kisa_m4.ogeler/_kanit/olc (salt okuma), arka.py, bekle.py] · atlanan [plan-kur (tek alan), alt ajan (kural 0), claude -p (0/6, Claude adımı henüz yok)]
V2 uzun, yalnız Gemini kolu (Claude adımı yok) · aday araç önce→sonra: 1nGx 12→11/18 · aZe5 14→11/22 · d_UE 3→6/13 · FaCh 8→10/16 · YDAK 5→11/27 · toplam 42→49/96 (0.44→0.51; kapı 0.95 UZAK). HYMD 429 (6000/4800/1200/0 aralığı önbellekte, 2400/3600 eksik).
Süre: YDAK 33→110 sn (ÖTEKİ YÖNDE; aralıklı istekler sıralı) · diğer 4'ü 8–17 sn (taban 68–280). Ağır Claude jetonu: yeni kolda 0 (Claude adımı yok), taban 60k–635k.
V3 carousel (yeni: v3.py karusel; referans = eski hat formu ∩ paket.md kanıtı): DdrE araç 98/98=1.0 · DePQ araç 10/10, link 19/20 · Dd7W (slayt videolu) araç 0.667, link 0.6. Süre 267→21 / 178→11 / 201→73 sn. Ağır jeton taban 297k–344k → Claude 0.
"yp" 20/4/5 = referansta olmayan ad; gerçek yanlış pozitif mi, eski formun kaçağı mı DENETLENMEDİ → yp 0 kapısı bilinmiyor.
