# SUIT-KIRMIZI-2 (kısmi)
- Madde 1 YAPILDI: test_geri_cagirma yeşil (45→46/48 = %95,8, eşik aynı). Kaçan 3: db-indeks-danismani (sıra 152), sec-sir-tarayici (sıra 3, kapsama 2/3), markitdown-mcp (sıra 18). Kök neden: katalog 4787 kayda büyüdü, TR sorgu terimleri EN kayıt metnine ES ile açılmıyor. Düzeltme: ES'e gecmis/sizmis/tara (katalog_ara.py).
- 1b YAPILDI: sec-sir-tarayici katalogda VAR (ajan, CC); beklenti geri alındı, artık sonuçta.
- Hâlâ kaçan: db-indeks-danismani, markitdown-mcp (ES denemesi kaldırmadı; kök neden ayrı çözüm ister).
- skill kopyası + docs/katalog katalog_yenile ile yenilendi; tools/tests/test_katalog_ara.py 6/6, tests/test_katalog_ek.py yeşil.
- YAPILMADI (bütçe $1,17 > hedef $0,60): 1c (suit2: 1423 geçti, 1 kırmızı test_yt1_paralel::test_boru_hatti_bariyersiz süre eşiği <1.2 sn, yük altında; 600 sn zaman aşımı parçalama), 1d headroom.test.mjs:91, 2 (etiket_uret.py repoda yok; katalogda 'etiket' alanı yok, 770 kayıtta boş tetik), 3 (3 ardışık tam suit).
- Devam: suit2 kırmızısı için `pytest tests/test_yt1_paralel.py -k bariyersiz` tek başına + yük altında karşılaştır.
