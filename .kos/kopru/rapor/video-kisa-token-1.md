# VİDEO-KISA-TOKEN-1 — ara rapor d1 (14 Eki ~16:15) — KABUL DEĞİL, ölçüm arka planda
Katalog: kullanılan [video CLI (hafif.cagir, tarama.sozluk_kur/eslestir, instagram.getir, cli._kullanici_env), ig-41 karar-birlesik.tsv, tools/ucuz_alt.py, gh api] · atlanan [plan-kur/katalog_ara (tek alan: video hattı kendi araçları yeterli), alt ajan (kural: 0)]

- M0 taban kaynağı: VİDEO-16 altın short kümesi (ig-DeW7JHrgsXb, ig-DeV9nZPtSsC, ig-DeHMM45NaFt), .kos/v16/{taban-1/2, low-ssb-1/2}.json — yeni claude -p yok. Taban = güncel varsayılan ssb (d9: 64 sn/video, $.087, çıktı 6.7k). `kisa_m4.py m0` video başı ağırlıklı jeton + kategori (metin · kare · sabit · rapor yazımı · araştırma 0) verir.
- M1: tools/video/video/kisa.py — Gemini (gemini-3.5-flash, yedek 2.5-flash; anahtar HKCU'dan, başlıkta) video + paket.md → gemini.json (şema: konusma_ozet, ekran_metni, araclar[{ad,ne_dedi,zaman}], linkler, komutlar, iddialar). Reel mp4 Files API, YouTube URL doğrudan, carousel görseller satır içi + slayt videoları + paket OCR. Duman: ig-DeW7 20.2 sn, 4 araç, `pip install airllm` yakalandı.
- M2: katalog() = ig-41 kararı > kurulu sözlük > bilinmeyen; bilinmeyen → repo_bul (link ya da gh arama, "doğrulanmadı" işaretli) + arastir (gh künye + README özeti ucuz_alt/OmniRoute; repo başı önbellek .kos/kopru/video/kisa/arastirma/).
- M3: oturum() tek claude -p (hafif.cagir, efor low) ≥8 videonun Gemini JSON'u + katalog → rapor araç başı 2 satır.
- Ölçüm: `kisa_m4.py kos` arka planda (8 video: 3 altın + 4 reel + 1 carousel; claude -p 1/4). Günlük .kos/kopru/video/kisa_kos.log.
- Test: tests/test_kisa.py 3/3 yeşil.
- Kalan: M4 puan (kapı), M5 skill + zip → devir/video-kisa-token-1-devam.md.
- d2 (16:45): fallback 2.5-flash emekli (404 'no longer available to new users') → 3.8-flash; hata gövdesi günlükte; kisa.calistir + `video kisa` + SKILL.md bölümü + zip TEMİZ. kos 3. videoda 3.5-flash zaman aşımıyla düştü → devir.

## d5 (14 Eki 18:00): recall artışı, ATLAS sözlüğü + paralel Gemini metin geçişi
- Kaçak analizi (kisa_m4.py kacak): d4 kaçaklarının çoğu pakette yazılı (pip, npm, Browser Use, Featherless, GliFormer, Llama); kalanı kavram ("Katman katman yükleme") ya da ad varyantı ("jev (GliFormer)").
- kisa.sozluk_tara: paket.md n-gram ∩ ATLAS envanter adları; videonun kendi raporundan gelen satır sayılmaz (sızıntı), belge sıklığı %20'yi aşan ad genel kelime sayılır. kisa.metin_gec: yalnız metin üzerinde çalışan Gemini (lite, ~2–7 sn, ücretsiz) adayları süzer, birlestir ile eklenir; izle ile paralel koşar. katalog() ATLAS'ı da tanır (bilinen 153/181).
- DF ≤%1 denemesi geri alındı: lite aday dışındaki sık adları (pip, npm, Llama) bıraktı.
- Ölçüm normalleştiricisi: "X (Y)" / "X, powered by Y" biçiminde çekirdek ad da eşleşir (tüm kollara eşit).

| kol | araç_yak | link_yak | yp/video | ağır_tk/video | sn/video |
|---|---|---|---|---|---|
| taban (1+2 ort.) | 0.850 | 0.584 | 0 | 236 348 | 131.5 |
| low-ssb (1+2 ort.) | 0.641 | 0.179 | 0 | 43 279 | 64.2 |
| yeni d5 | 0.861 | 0.449 | 0 | 10 020 (0.04×) | 32.7 (0.25×) |

- Kapı: araç ✓ · yp ✓ · token ✓ · süre ✓ · link ✗ (0.449 < 0.584). claude -p bu dilimde 1 (57 sn, 0.16 $).
