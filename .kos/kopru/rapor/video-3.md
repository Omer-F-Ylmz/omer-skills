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

## d3 ara (14 Eki ~20:20) KABUL DEĞİL
Katalog: kullanılan [kisa.metin_gec/_uret/sozluk_tara/katalog/blok/oturum, altin.puan, arka.py, bekle.py] · atlanan [plan-kur (tek alan), alt ajan (kural 0)]
Kök neden (kaçan analizi): kaçanların çoğu paket.md'de var, Gemini'de yok. (1) kisa.metin_gec paketi 24k'da kesiyor; 1nGx/YDAK/HYMD kaçanları 32k–177k'da. (2) uzun.izle aralık yolunda `teknikler` düşüyordu.
Değişiklik (uzun.py): pencereli metin geçişi (24k pencere, 1k örtüşme, 2 eşzamanlı) + aralık yolunda teknikler araçlara katılır; test 4/4.
Aday araç (6 altın) önce→sonra: taban 81/135 (0.60) · d2 Gemini 49/96 (5 video) → d3 89/135 (0.66): 1nGx 15/18 · aZe5 12/22 · d_UE 6/13 · FaCh 10/16 · HYMD 30/39 · YDAK 16/27. Teknik istem cümlesi: etkisiz (89→89), isabet hafif arttı; kaldı.
Claude adımı (kisa.oturum, 1 claude -p, efor low, 6 video tek oturum): ağır 169.6k = 28.3k/video; taban ort. 302.6k/video → 0.09× (kapı ≤0.30 GEÇTİ). Yakalama değişmedi (Claude ad eklemiyor).
Süre/video: Gemini 0–19 sn + oturum 115/6 ≈ 19 sn → ~25–40 sn; taban ort. 202 sn → ~0.15× (≤0.5 GEÇTİ).
KAPI: araç 0.66 < 0.95 KALDI. Kalan kaçanların ~yarısı pakette adı hiç geçmeyen kavram (Subagent, Claude memory, Effort ayarı…) ya da teknik; link 31/31 tam (yakalama kapısı geçer), yp denetlenmedi. claude -p 1/6.

## d4 ara (14 Eki ~21:10) KABUL DEĞİL
Katalog: kullanılan [kisa.sozluk_tara/birlestir, altin.gecer/_icerir/norm, kisa_m4 kuralları (teknik ayrı, kanıtsız paydadan çıkar), v3.py] · atlanan [plan-kur (tek alan), alt ajan (kural 0), claude -p (0 yeni; 1/6)]
Kapı tanımı kısa hatla eşitlendi (v3.py kacak): teknik araç sayımına/yp'ye girmez; altında pakette geçmeyen kalem "temiz" paydadan çıkar ve listelenir (3: HYMD Claude Code Desktop, YDAK Bodoni Moda + Hanken Grotesk); yp = altında eşi yok VE pakette geçmiyor.
Kök neden (yp 39): kisa.ISTEM'deki örnek adlar (Python, pip, npm, uv, GitHub, Hugging Face, PyTorch, Transformers, Apache-2.0, Qwen3.5-0.8B, Llama) FaCh ve HYMD'de aynı sırayla araç olarak dönüyor; pakette yoklar.
Değişiklik: uzun.son (sözlük adayı doğrudan eklenir + istem yankısı düşer; ≤4 harfli adda kelime sınırı, "pip"⊄"pipeline"), oturum adımına bağlandı; test_uzun 5/5.
Önce→sonra (6 altın, Claude'suz Gemini+son): araç 76/96 0.79 → 81/96 0.84 · temiz 76/93 0.82 → 81/93 0.87 · yp 39 → 4 (KAP×2, img, node).
KAPI: araç 0.87 < 0.95 KALDI, yp 4 > 0 KALDI. Jeton 0.09× / süre ~0.15× d3'ten değişmedi (yeni Gemini/Claude çağrısı yok).

## d5 (14 Eki ~22:00) — kalem başı önce → sonra (Claude'suz ölçü, `v3.py kacak yok.json son`)
- yp: 4 (KAP, img, node) → 0 · kök: sözlük ngram'ı ≤4 harfli adı URL/etiket/kelime parçasından (/img/, node_modules, "kap") alıyordu → uzun.kisa_ad.
- temiz araç: 81/93 = 0.871 → 0.871 · metin geçişine kisa d11 örnek birleşimi taşındı; yakalama değişmedi (oynama ±1).
- 12 kaçan teşhisi (v3_teshis.py): 6'sı DF_TAVAN üstü bilinen ad (TypeScript, Vite, Framer Motion, Claude Code) → uzun.yaygin_aday ile Gemini'ye aday; ÖLÇÜLMEDİ (Gemini 3 model 429 kota). Kalan: envanterde yok (3), sızıntı (2), OCR yazımı farklı (2).
- Katalog: kullanılan [ATLAS envanteri (sözlük), kisa.py ortak fonksiyonlar] · atlanan [video-uygula, plan-kur — d5 tek alanlı ölçüm düzeltmesi]. claude -p 0 (toplam 1/6), alt ajan 0.
