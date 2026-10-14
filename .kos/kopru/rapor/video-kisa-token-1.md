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
