# VİDEO-HIZ-2 rapor (11 Eki 03:53)
Yapılan: süre ≥ goz.ANAHTAR_SN (3600) videoda dhash + kare çıkarma geçişleri `-skip_frame nokey` (yalnız anahtar kare; AV1 akışta ~3.7 sn'de bir). -ss tek kareleri ve <60 dk videolar eski yol. cli.py (3 satır) + goz.py (1 sabit) + tests/test_hiz2.py (3 test, değişiksiz kırmızı). devam-3 dosyalarına dokunulmadı.
Ölçüm (_xQnSNlBP_w 30 dk AV1 1080p60 kesit, .kos/kopru/arka.py, $0):
- 10 dk dhash geçişi: 52.3 sn → 0.7 sn
- 30 dk sahne aşaması: 190.2 → 3.1 sn; _goz_ocr_govde toplam 270.8 → 77.9 sn (−71%); OCR 81 → 75 sn
- sahne/kare: 438 → 400 (OCR kare sayısı = jeton girdisi −9%)
- kalite (yalnız OCR satırı, rapor değil): kelime geri çağırma 887/1286 (%69, yeni 1147 kelime); URL 1/2 — kaybolan tek URL OCR'ı bozuk docs.google satırı
Kalite DUR: kelime geri çağırma %69 kare zaman kaymasından mı (aynı slayt, farklı OCR gürültüsü) yoksa gerçek kayıptan mı ayırt edilmedi; rapor-düzeyi aday/araç geri çağırma (HYMDaMcuSGQ / mQBuZ6Dp0u0, ücretli ≤$8) koşulmadı → kabul "kalite ≥ taban" KANITLANMADI.
Suit: tools/video 1323 yeşil.
Geçiş (yalnız kalite ölçümü geçerse): runner'ı pid ile durdur → `python .kos/kopru/parti_devam.py 2026-10-11-short --paralel 2`. Geçmezse goz.ANAHTAR_SN büyütülür (eski yol).
Kalanlar: (1) rapor-düzeyi kalite A/B (taban kesit + iki kol rapor, aday/araç geri çağırma) (2) ffmpeg ilk geçiş (paket ~502, 3 kare önizleme) ve ses çıkarma uzun videoda ölçülmedi (3) OCR %95 hedefi, -ss/indirme çözünürlüğü, tekrar/dolgu ayıklama başlanmadı.
Ölçüm betiği .claude/hiz2_olc.py (izlenmez), veri C:\Projeler\.video-cache-hiz2\sonuc.json.

# VİDEO-HIZ-3 rapor (11 Eki 04:45)
Yapılan: (1) b481b3e anahtar-kare yolu bayrağa alındı, varsayılan KAPALI (env VIDEO_HIZ2=1; açıkken goz önbellek anahtarına hiz2). (2) ec15441 slayt düzeyi ölçüm + melez yol (VIDEO_HIZ2=2: dhash taraması anahtar kare, seçilen kareler tam çözme). Canlı runner'a dokunulmadı. Suit tools/video 1325 yeşil.
Ölçüm (_xQnSNlBP_w 30 dk AV1 kesit, $0; slayt = kare kelime kümesi Jaccard ≥.5 kümesi, geri çağırma = taban slaytın çekirdek kelimelerinin ≥%80'i yeni kolun bir karesinde, bulanık eşleşme .8):
| kol | süre | OCR kare (jeton girdisi) | slayt geri @80 / @60 | gerçek kayıp kelime | aday geri | USD |
| a eski (tam çözme) | 205.9 sn | 435 | taban (32 slayt) | — | ölçülmedi | 0 |
| b anahtar kare (=1) | 55.4 sn (−73%) | 396 (−9%) | %62.5 / %87.5 | 49 | ölçülmedi | 0 |
| c melez (=2) | 136.4 sn (−34%) | 391 (−10%) | %90.6 / %100 | 5 | ölçülmedi | 0 |
%69 kelime geri çağırmanın ayrışması (a→b, 384 eksik kelime / 1241): 203 bulanık (aynı kelimenin OCR gürültüsü) · 130 yalnız tek karede (örnekleme) · 49 gerçek kayıp; bulanık kelime geri çağırma %85.6. Yani kaybın çoğu gürültü ama gerçek kayıp var: 12/32 slayt %80 altında (anahtar kare ~3.7 sn'de bir → kısa slayt/derleme adımı kaçıyor). Melez gerçek kaybı 49→5'e indiriyor, hız kabulünü (≥%50) geçmiyor: tam çözmeli kare çıkarma tüm videoyu çözüyor (~77 sn/30 dk).
Karar: GEÇMEDİ → bayrak kapalı kalır (geçiş satırı yok). (3) rapor düzeyi A/B koşulmadı: sentetik 30 dk kesitin meta/altyazısı yok, parti/tarama akışı tur bütçesine sığmadı; ücretli çağrı $0.
Sonraki onarım: melezde kare çıkarmayı zaman dilimlerine bölüp 2–4 paralel `-ss dilim -t` sürecine dağıt (ya da seçilen t başına önceki anahtar kareden kısa pencere) → hedef ≤103 sn (−50%) + slayt@80 ≥%95 (kalan 3 slayt: eşik mi gerçek mi elle bak); sonra (3) gerçek uzun video (HYMDaMcuSGQ) iki kol rapor A/B ≤$8. Ölçülmeyenler aynen: ffmpeg ilk geçiş (paket ~502), ses çıkarma, 720p indirme.
Betikler .claude/hiz3_olc.py (kol a/b/c) + .claude/hiz3_analiz.py (izlenmez); veri C:\Projeler\.video-cache-hiz2\{a,b,c}.json, analiz-*.json.

# VİDEO-HIZ-4 rapor (11 Eki 04:55)
Yapılan (bayrak arkasında, varsayılan KAPALI): (1a) melezde (VIDEO_HIZ2=2) tam çözmeli kare çıkarma PARCA=4 zaman dilimine bölündü, dilim başına `-ss ızgara -t` süreci paralel; select n dilime göre, dosya numarası sahne sırasıyla sürer. Doğrulama (.claude/hiz4_dogrula.py): tek geçiş 84.9 sn → 4 dilim 38.0 sn, 425/425 kare piksel farkı 0 (aynı kareler). (1b) altyazıda araç/repo/URL/komut geçen satıra ızgara karesi (goz.altyazi_zaman, ±3 sn'de kare varsa atlanır). Test +2, suit tools/video 1327 yeşil.
Ölçüm (_xQnSNlBP_w kesit = 3400–5200 sn; altyazı kesite kaydırıldı; $0):
| kol | süre | slayt@80 / @60 | OCR kare (jeton girdisi) | aday geri | USD | karar |
| a eski | 205.9 sn | taban (32) | 435 | ölçülmedi | 0 | — |
| c melez (HIZ-3) | 136.4 sn (−34%) | %90.6 / %100 | 391 | ölçülmedi | 0 | geçmedi |
| d melez + paralel + altyazı karesi | 94.9 sn (−54%) | %90.6 / %100 | 391 (altyazı +0) | ölçülmedi | 0 | geçmedi (slayt) |
Hız kabulü geçti (≤103 sn), slayt@80 geçmedi (29/32, eşik 31/32). Kalan 3 kayıp elle: (i) "capitol ififii iiiii rkcc" çekirdeği OCR çöpü → eşik/gürültü; (ii) t≈780 ve (iii) t≈1348 yoğun metinli kaydırılan ekran paylaşımı (PR/agent belgeleri), kolun ±2–4 sn'de karesi var, kapsam .72/.74 → kaydırma durumu farkı; anahtar-kare taraması kaydırma ortasındaki sahne değişimini görmüyor (a 435 vs d 391 kare). Altyazı karesi 30 dk'da 0 ekledi: taban ızgarası (5 sn) zaten ±3 sn'yi dolduruyor; etkisi taban aralığı büyüyen ≥1 sa videoda — orada ölçülmedi.
(2) ffmpeg ilk geçiş (paket ~546) yalnız IG karusel yolunda (≤3 kare), uzun YouTube yolunda yok; ses çıkarma yalnız ASR yolunda (altyazısız video) — iki uzun aday videoda (HYMDaMcuSGQ, _xQnSNlBP_w) altyazı var, kritik yolda değil → ölçülmedi. 720p indirme ölçülmedi (tur bütçesi).
(3) koşulmadı: önkoşul "(1) geçerse" sağlanmadı; ücretli $0. (4) VIDEO_HIZ2 varsayılanı KAPALI.
Bulgu (eski, düzeltilmedi): kare çıkarma 438 sahneden 425 dosya üretiyor (neden kanıtlanmadı; olası: aynı ızgara n'ine düşen iki sahne → tek çıktı); `zip(sahne, sorted(s*.jpg))` ilk boşluktan sonra kare zaman etiketlerini kaydırıyor (a ve tüm kollarda). Slayt metriği zamandan bağımsız, ama pakette kare zamanı yanlış olabilir.
Sonraki onarım: (a) zaman etiketi kayması: sahne'yi kare_sec sonrası ızgara n'ine göre tekilleştir (en küçük düzeltme); (b) slayt: kaydırma ekranları için anahtar-kare taramasında art arda iki anahtar kare dhash farkı yüksekse aradaki orta ızgara karesini de seç (kare +~%10, paralel çıkarma ~+4 sn → bütçe ~103 içinde) ya da slayt metriğinde OCR-çöp küme (çekirdek sözlük dışı) dışlansın; (c) sonra HYMDaMcuSGQ rapor A/B ≤$8; 720p slayt OCR isabeti.
Betikler .claude/hiz4_dogrula.py, hiz4_kayip.py, hiz3_olc.py kol d (izlenmez); veri C:\Projeler\.video-cache-hiz2\d.json, analiz-a-d.json; dogrula1/dogrula4 kare dizinleri (silinebilir).

# VİDEO-HIZ-5 rapor (11 Eki 05:20)
(a) commit ef7e5cc — kök neden kanıtlı: kare_sec taban karesi round(t·f) ile sonraki sahnenin ızgara n'ine düşüyordu (ör. 2+5=7 sn → n 4 = 8.0 sn); select tek kare üretiyor, `zip(sahne, sorted(s*.jpg))` ilk çiftten sonra tüm zamanları kaydırıyordu. Düzeltme kare_sec içinde (tüm çağıranlar, tüm partiler): tekil ızgara n, aynı n'de sahne (yüksek Hamming) kalır. Kırmızı-önce test_kare_sec_izgara_n_tekil. Gerçek 30 dk AV1 (.claude/hiz5_a.py): 425 sahne = 425 dosya (önce 438 → 425); 20 örnekte -ss referans karesiyle fark: 11/20'de kendi karesi komşudan yakın, kalanlar durağan ekranda komşuyla eşit düzey (≤±2 sn içerik aynı) — sistematik kayma yok.
(b) commit 15a1aa0 — goz.ara_kare: anahtar-kare ızgarasında art arda iki anahtar kare Hamming > ARA_HAM=5 → aradaki orta ızgara karesi (yalnız VIDEO_HIZ2=2). Eşik taraması: >5 → 12 kare, >10 → 11, >20 → 3 (hiz5_esik.py).
| kol | süre | slayt@80 / @60 | OCR kare (jeton girdisi) | aday geri | jeton | USD | karar |
| a eski (HIZ-4 ölçümü) | 205.9 sn | taban (32) | 435 | taban | — | 0 | — |
| d melez+paralel (HIZ-4) | 94.9 sn (−54%) | %90.6 / %100 | 391 | ölçülmedi | — | 0 | geçmedi (slayt) |
| e d + ara kare (HIZ-5) | 106.0 sn (−48.5%; sahne 32.6 + OCR 73.4) | %96.9 / %100 (31/32) | 464 | ölçülmedi | (c) yok | 0 | geçmedi (süre, 3 sn) |
Kelime geri e: tam %96.5, bulanık %98.2 (d: %90.5/%95.8). Kalan tek kayıp slayt = OCR-çöp küme ("capitol ififii iiiii rkcc", çekirdek sözlük dışı) — ayrıca raporlandı, metrik gevşetilmedi; %95'e gerçek karelerle ulaşıldı.
(c) koşulmadı (önkoşul: (b) tam geçmeli; süre −48.5% < −50%), ücretli $0. (d) VIDEO_HIZ2 varsayılanı KAPALI. 720p ölçülmedi.
Not: e tek koşum; OCR süresi kare sayısıyla doğrusal (464 vs d 391 → +18.5 sn). Kare artışı yalnız +12 ara kare değil: (a) düzeltmesi d'nin kaybettiği 13 kareyi de geri getirdi + altyazı/yoğun ek kareler.
Sonraki onarım: süre 3 sn aşımı OCR'da — (i) e kolunu bir kez daha koş (gürültü payı; d/e OCR süresi tek ölçüm), (ii) geçmezse ara kareyi Hamming > 10'a çek (−1 kare, etkisiz) yerine OCR'da ardışık ≥0.97 dhash eşi karelerin OCR'ını atla (aynı metin) ya da altyazı ek karesini ±3→±5 sn pay ile azalt; hedef ≤103 sn + slayt@80 ≥%95 korunur; sonra (c) HYMDaMcuSGQ A/B ≤$8.

# VİDEO-HIZ-6 rapor (11 Eki 05:55)
(1) e tekrar koşusu 112.4 sn (OCR 78; HIZ-5'te 106.0/73) → gürültü payı aleyhte, hâlâ >103. dHash ile OCR atlama simülasyonu (.claude/hiz6_sim.py, gerçek kare JPG'leri): 9×8 ≥0.97 → 237 kare atlanır ama yalnız 8'i aynı metin, slayt@80 %93.8 · 32×32/64×64 ≥0.97–0.98 → kelime geri %92–93 → dHash yazı değişimini görmüyor, ret. Piksel farkı (480 px gri, |fark|>40 oranı, .claude/hiz6_px.py): 0.002 → −36 kare kayıpsız (kelime bulanık %98.1) · 0.003 → −64 kare, kelime bulanık %97.7, slayt@80 %96.9 · 0.004 → gerçek kayıp 8, ret. Seçilen goz.es_kare ES_ORAN=0.003 (yalnız VIDEO_HIZ2=2), eş karenin satırları kaynaktan kopyalanır; kırmızı-önce test_es_kare_ardisik_esi_atlar.
| kol | süre | slayt@80 | kelime geri (tam/bulanık) | OCR kare (jeton girdisi) | aday geri | USD | karar |
| a eski | 205.9 sn | taban (32) | taban | 435 | — | 0 | — |
| e HIZ-5 | 106.0 / 112.4 sn | %96.9 | %96.5/%98.2 | 464 | — | 0 | süre ✗ |
| e + es_kare (HIZ-6) | 92.6 sn (−55%) | %96.9 | %96.1/%97.9 | 400 OCR (−64 eş; pakete giden ekran metni satırı aynı) | ölçülmedi | 0 | (1) GEÇTİ, tek ölçüm |
Jeton: OCR çağrısı −14% (464→400 kare); model girdisine giden kare sayısı _ocr_model seçimine bağlı, eş kare aynı satırı taşıdığından paket metni değişmez → paket jetonu ~aynı (ölçülmedi). Suit: 1329 yeşil + 1 (test_rapidocr_birincil) suit koşusunda kırmızı, eşzamanlı OCR ölçümüyle çakışma; tek başına 18/18 yeşil, değişiklik olmadan da aynı test yeşil.
(2) HYMDaMcuSGQ rapor A/B, (3) ≥60 dk varsayılan aç, (4) 720p + eski paket kayması: tur bütçesi (45) nedeniyle başlanmadı; VIDEO_HIZ2 KAPALI kalır.
Sonraki onarım: (i) e+es_kare bir kez daha koş (süre gürültüsü 106↔112 gördük; ≤103 iki koşuda), suit tek başına yeşil teyidi; (ii) HYMDaMcuSGQ eski vs VIDEO_HIZ2=2 tarama raporu A/B ≤$8 (aday/araç/URL geri ≥ eski + rapor-denetle); (iii) geçerse ≥60 dk için varsayılan; (iv) eski kodla paketlenmiş 6 uzun video kare kayması: yalnız sahne sayısı ≠ dosya sayısı olanlar yeniden paketlenir (kontrol ücretsiz: paket.md kare zamanı sayısı vs kareler/ dosya sayısı).

# VİDEO-HIZ-7 rapor (11 Eki 06:25, ara)
(i) GEÇTİ — e + es_kare tekrar (.claude/hiz7_e.log, kod 2e399cf): 97.2 sn (sahne 29.7 + OCR 63.3; HIZ-6 92.6) → iki koşu da ≤103 sn; slayt@80 %96.9 (31/32) / @60 %100, kelime geri %96.1/%97.9, OCR 464 kare (64 eş atlanır). Suit tek başına: A/B'nin OCR'ı bittikten sonra koşulacak (eşzamanlı OCR test_rapidocr_birincil'i bozuyor).
(ii) SÜRÜYOR — mevcut 2026-10-11-HYMDaMcuSGQ.md kullanılamaz: paketi 02:16 (kare_sec düzeltmesi ef7e5cc ve JETON C varsayılanı 00531bb öncesi) → iki kol aynı kodla yeniden. .claude/hiz7_ab.py: eski (VIDEO_HIZ2=0) → hiz2 (=2) sırayla; kol başı ayrı VIDEO_CACHE (indirme düzeyi dosyalar tohum, goz/paket yeniden), ayrı VIDEO_TARAMA_DIZIN + VIDEO_UYGULA_KOK (canlı 2026-10-11-short açıkken HYMDaMcuSGQ'yu "açık parti" diye reddediyordu, ilk deneme rc=3 $0), JETON varsayılan C, ikinci göz yok, kol başı $3 tavan.
(iv) kayma YOK, ama 4 videoda hiç kare yok (ücretsiz kontrol: ocr.json sahne vs k*.jpg = ham − yoğun):
- wjXowoQ7E8c (86 dk) sahne 665 = 665 dosya · z4zXicOAF28 (518 dk) 859 = 859 → kayma yok, yeniden paketleme gereksiz.
- _xQnSNlBP_w (609 dk) · xmbSQz-PNMM (537) · wyUdpmj9-64 (507): "kare yok: ffmpeg: zaman aşımı (1800 sn)" (eski tam çözme yolu 9–10 sa AV1'de tavanı aşıyor) · O_IMsEg91g8 (551): "kare yok: yt-dlp: zaman aşımı (900 sn)". Paket ekran metni (OCR) hiç yok → kalite boşluğu.
Öneri (uygulanmadı): bu 4'ü VIDEO_HIZ2=2 ile yeniden paketle — 30 dk ölçüsünden doğrusal ~29 dk/video (anahtar-kare taraması ~9 dk < 1800 sn tavanı), O_IMsEg91g8 için yt-dlp 900 sn tavanı ayrıca yetmez (indirme süresi ölçülmeli); yeniden tarama ~$0.80–0.87/video (defter: _xQ 0.80, O_IM 0.87) → ≈$3.5–4 toplam. Canlı parti bitince, runner'a dokunmadan.

# VİDEO-8 rapor (11 Eki 07:5x, 45. tur)
## (1) HIZ-7 A/B — HYMDaMcuSGQ (106 dk), aynı kod, JETON C, ikinci göz yok (.claude/hiz7_ab.log BITTI; karşılaştırma .claude/v8_kars.py: ad bazında, normalize + içerme + difflib ≥0.8)

| ölçü | eski (VIDEO_HIZ2=0) | melez (=2) |
|---|---|---|
| aday geri çağırma (birleşim 80) | 40/80 | 69/80 |
| komut geri çağırma (birleşim 41) | 26/41 | 40/41 |
| URL geri çağırma (birleşim 37) | 23/37 | 37/37 |
| rapor-denetle | DUR (4 "iz sebebi" hatası) | GEÇTİ (2 EKSİK uyarısı) |
| sahne / OCR kare | 800 / 920 | 1541 / 1591 |
| OCR aşaması | 516 sn | 902 sn |
| kol toplam süre | 1351 sn | 1618 sn (+20%) |
| jeton | 147.7k | 313.1k (×2.1) |
| USD | 0.572 | 0.552 |

Yalnız eskide: aday 11 (çoğu yenide başka adla: "Gelen Kutusu hattı (A)" ↔ "Seviye A — Gelen kutusu"; gerçek kayıp "Git") · komut 1 (/usage) · URL 0.
KARAR: geri çağırma ≥ eski VE rapor-denetle GEÇTİ → VIDEO_HIZ2=2 ≥60 dk (ANAHTAR_SN 3600) VARSAYILAN AÇIK (4123aca; VIDEO_HIZ2=0 eski yol; test_bayraksiz_uzun_video_melez kırmızı→yeşil; suit 1331). Not: bu videoda melez daha YAVAŞ (2× sahne → 2× OCR); kazanç 9–10 sa AV1'de ffmpeg 1800 sn tavanını aşmamakta. Jeton ×2.1 ama USD −4% (önbellek okuma).

## (2) 4 kare-siz uzun video yeniden paket + tarama — SÜRÜYOR
- İndirme tavanı: goz-video yt-dlp `max(900, süre/2)` (O_IMsEg91g8 551 dk → 16530 sn). Test eklenmedi (≤5 satır; sapma).
- docs/video-tarama/kuyruk-yeniden-1.md (4 satır) → .claude/v8_yeniden.py (arka.py, pid 11736, 07:48 başladı, log .claude/v8_yeniden.log): ayrı VIDEO_CACHE C:\Projeler\.video-cache-v8 (indirme düzeyi tohum, paket.md yok), ayrı VIDEO_TARAMA_DIZIN .claude/v8/yeni + VIDEO_UYGULA_KOK → canlı runner/2026-10-11-short-2'ye dokunmaz; $5 / 16 çağrı tavanı, ikinci göz yok. RAM başlarken %72.9.
- Kalan: BITTI sonrası .claude/v8_kars.py ile docs/video-tarama/2026-10-11-<id>.md (eski) ↔ .claude/v8/yeni/yeniden-1-<id>.md farkı; yenisi zenginse eskinin yerine kopyala + commit. Parti kapanınca `video parti iptal yeniden-1-uzun` gerekebilir (VIDEO_UYGULA_KOK env'iyle).

## (3) VIDEO_JETON C onarımı — BAŞLANMADI (tur bütçesi)
Plan (hazır, ~10 satır): parti.kare_ayikla dHash (JETON_HAM 5) → goz.es_kare yöntemi (480×270 gri, |fark|>40 oranı < goz.ES_ORAN ise tutulana eş; tutulan TÜM karelerle, dönüp gelen ekran dahil), JETON_HAM kaldırılır, test_t7c3 iki testi piksel-fark kareleriyle güncellenir (yazı farklı/aynı-hash vakası eklenir). Karar kuralı: yakalama ≥ taban VE ad yazım ≥ taban VE jeton ↓ VE USD ↓; 2 tur (FaChtkkG9X4 · aZe5ZTYcF1M + 1nGx), ≤$3; sağlanmazsa parti.JETON="".

# VİDEO-9 rapor (11 Eki 09:1x)
C2 = parti.kare_ayikla(piksel=True): goz.es_kare yöntemi (480×270 gri, |fark|>40 oranı < ES_ORAN → tutulan TÜM karelere eş). VIDEO_JETON=C2 ayrı yol; C (dHash) değişmedi. Ölçüm .claude/v9_olc.py (.claude/v9_olc.log): 3 kol sırayla, FaChtkkG9X4+aZe5ZTYcF1M (short) · 1nGx7WR8YLE (uzun); ayrı VIDEO_CACHE C:\Projeler\.video-cache-v9 (paket dahil kopya → kollar aynı kareler), VIDEO_TARAMA_DIZIN/VIDEO_UYGULA_KOK .claude/v9/<kol>-<tur>; ikinci göz yok; parti başı $0.45.

| kol | yakalama | ad yazım | jeton/video | USD/video | süre | karar |
|---|---|---|---|---|---|---|
| taban (JETON kapalı) | 37/56 | 31/37 | 114.4k | 0.160 | 8 dk | referans |
| C (dHash) | 35/56 | 26/35 | 108.9k (−4.8%) | 0.195 (+21%) | 8 dk | 4 koşulun 4'ü de KALDI (yakalama −2, ad yazım −5, USD +21%) |
| C2 (piksel farkı) | 37/56 | 31/37 | 101.9k (−10.9%) | 0.163 (+1.7%) | 11 dk | yakalama =, ad yazım =, jeton ↓ GEÇTİ; USD ↑ KALDI |

Video başına: taban 8/6 · 14/11 · 15/14 | C 9/5 · 13/10 · 13/11 | C2 9/8 · 15/12 · 13/11 (yakalama/ad yazım; FaCh · aZe5 · 1nGx). Kol USD: short taban 0.304 / C 0.304 / C2 0.316 · uzun 0.177 / 0.280 / 0.173.
KARAR: kural sağlanmadı (C2 USD +1.7%; short partide +$0.012, uzun partide −$0.004) → VARSAYILAN DEĞİŞMEDİ (parti.JETON="C"). Onarım turu YAPILMADI: tur bütçesi (40) doldu; harcama $1.55 / $3. C bu turda üç turun en kötüsü (yakalama ve ad yazım tabanın altında, USD +21%) → "kalite ASLA düşmez" kuralına göre C açık kalmamalı.
Sonraki adım (≤$1.45 kaldı): USD artışı short partide; defter kırılımı (çıktı ve önbellek yazma jetonu) taban ve C2 short için karşılaştırılır. Kaynak bulunur ve onarılırsa 1 tur daha (taban/C2); yine sağlanmazsa parti.JETON="".
Suit: tools/video 1318 geçti, 14 kırmızı (KeyError 'uyku': cli._ram_kapi boş RAM < eşik, ölçüm sırasında; ölçüm bitince 4 dosya 36/36 yeşil; bu testler bos_ram'ı sahtelemiyor, ortama bağlı). test_rapidocr_birincil geçti.

# VİDEO-10 rapor (11 Eki 09:3x, 40. turda durdu)
## (1) Kök neden: kare çıkarma dilim RAM'i = dal başı mjpeg kodlayıcı iş parçacığı tamponları
Ölçüm .claude/v10_ram.py (.claude/v10_ram.log): xmbSQz-PNMM 3600–4200 sn, cli._kare_cikar'ın gerçek komutu, tek dilim; tepe = GetProcessMemoryInfo (kesin tepe) + 1 sn örnek; kareler md5 ile mevcut yola kıyaslandı.

| deneme | tepe RAM (özel / WS) | süre | kare piksel aynı mı | karar |
|---|---|---|---|---|
| K6 hw (mevcut) | 3.57 / 1.67 GB | 48–55 sn | referans | — |
| K3 hw | 2.00 / 0.92 GB | 53 sn | evet | RAM ∝ dal sayısı |
| K1 hw | 0.96 / 0.41 GB | 47–53 sn | evet | — |
| K6 hwsiz | 3.35 / 1.73 GB | 84 sn | evet | ret (yavaş) |
| K6 -threads 1 (çözücü) | 3.57 / 1.67 GB | 48 sn | evet | etkisiz |
| K6 -filter_complex_threads 1 | 3.54 / 1.64 GB | 46 sn | evet | etkisiz |
| K6 -threads 1 (kodlayıcı, dal başı) | 0.65 / 0.31 GB | 48 sn | evet | RAM −82% |
| K6 hwaccel_output_format cuda (+hwdownload) | 3.58 / 1.67 GB | 25 sn | evet | süre −49% |
| K6 cuda çıkış + extra_hw_frames 0 | 3.58 / 1.67 GB | 24 sn | evet | ek kazanç yok |
| K6 kombine (kodlayıcı -threads 1 + cuda çıkış) | 0.66 / 0.30 GB | 25 sn | evet (300/300 md5) | SEÇİLEN |
| K1 kombine | 0.48 / 0.18 GB | 23 sn | evet | — |

Uygulama UYGULANMADI, yama .claude/v10_ram.patch (cli._kare_cikar: hw yolunda -hwaccel_output_format cuda + "hwdownload,format=nv12," önek, 10-bit → hata → _ff eski yol; çıkış başı -threads 1; PARCA_GB 2.5 → 1; kırmızı-önce test test_kare_cikar_cuda_cikis_kodlayici_tek_is_parcacigi kırmızı görüldü → yeşil; conftest pt._bos_ram_gb=64). Yama ile 2 test kırmızı kaldı: test_hiz2::test_melez_kare_cikarma_paralel_dilim ('-start_number' not in list — sorted(fc) ilk öğesi; bakılmadı) ve test_yt1_paralel::test_sahne_en_iki_ocr_asla_iki_olmaz_tampon_uc (conftest 64 GB → _parca 4 dilim → SAHNE sayacı beklentisi; bu test daha önce gerçek düşük RAM'de 1 dilime düşerek geçiyordu, yani o da ortama bağlı). Canlı runner aynı ağaçtan alt süreç açtığı için kırmızı yama ağaçta bırakılmadı.
## (2) 4 kare-siz uzun video yeniden işleme — BAŞLATILMADI
Sebep: RAM onarımı ağaçta değil; v8_yeniden mevcut kodla aynı %98 riskine girer. Yama yeşil + commit sonrası başlatılmalı (RAM ≤ %80 kontrolüyle).
## (3) C2 USD
Defter kırılımı (v9 short, tarama satırı; girdi / önbellek yazma / önbellek okuma / çıktı / USD): FaCh taban 6/77.4k/18.2k/56.8k/$0.1518 ↔ C2 4/36.3k/0/42.4k/$0.1512 · aZe5 taban 4/44.6k/0/38.5k/$0.1521 ↔ C2 6/45.0k/21.9k/44.5k/$0.1646. +1.7%'nin tamamı aZe5'te: çıktı +6.0k (süre 180 → 381 sn); önbellek öneki bozulmuyor (C2 aZe5 önbellek okuma 21.9k > taban 0). Defter sonnet+haiku karışımını tek satırda topluyor, model başı kırılım yok → yapısal kaynak bulunamadı, kod onarımı yok (gürültü/çıktı farkı). Tekrar turu .claude/v10_olc.py (taban + C2, short + uzun, parti başı $0.36, Σ ≤ $1.44) arka planda koşuyor (.claude/v10_olc.log, .claude/v10/<kol>-<tur>); karar (iki turun ortalamasıyla kural) Desktop'a kaldı; parti.JETON "" (dokunulmadı).
## (4) Ortama bağlı testler
Yeniden üretim: pytest -p dusukram (.claude/v10p/dusukram.py, pt._bos_ram_gb=0.5) → 13 kırmızı (test_goz_t 2, test_hiz2 6, test_hiz3b 5; KeyError 'uyku'). Düzeltme conftest autouse pt._bos_ram_gb=64 (yamada); yukarıdaki test_yt1_paralel testinin beklentisi güncellenmeden yeşil olmuyor.
## (5) Suit / commit — YAPILMADI (kırmızı yama). Harcama: v10_olc ≤ $1.44 (sürüyor), başka API yok.

# Desktop kararı (10:15) — C2 2. tur (.claude/v10_olc.log)
| kol | short jeton / USD | uzun jeton / USD | PUAN farkı |
|---|---|---|---|
| taban | 288.7k / 0.350 | 307.1k / 0.198 | — |
| C2 | 235.9k (−18%) / 0.394 (+13%) | 105.9k (−65%) / 0.169 (−15%) | FaChtkkG9X4 3. sütun 8 → 6, diğerleri eşit |
Toplam USD 0.548 → 0.563 (+2.7%); iki turda da short partide USD ↑ ve bir videoda puan düşüşü → C2 RED. VIDEO_JETON kalıcı KAPALI (""); C/C2 hattı KAPANDI: maliyeti çıktı jetonu ve model karışımı belirliyor, kare ayıklama girdi jetonunu düşürüyor ama USD'yi güvenilir düşürmüyor ve kaliteyi riske atıyor. Kod (env VIDEO_JETON=C2) deney için kalır.

# VİDEO-11 rapor (11 Eki 10:27, 35. turda durdu)
- **Uygulandı, commit 97ac365** (yalnız cli.py, conftest.py, test_hiz3b.py). Yamada `-start_number` satır sonu yorumunun içinde kalmıştı → test_hiz2::test_melez_kare_cikarma_paralel_dilim kırmızısının kökü buydu (fc listesine öğe eklenmiyordu, öğe yorumla yutuluyordu); düzeltildi.
- test_yt1_paralel::test_sahne_en_iki_ocr_asla_iki_olmaz_tampon_uc: süre 10 sn < ANAHTAR_SN → `_parca` hiç çağrılmıyor; `_parca` yasaklayan eklentiyle (.claude/v11p/parcayok.py) de geçti → RAM'e bağlı değil, test değişmedi. conftest `pt._bos_ram_gb=64` dilim sayısını tüm suitte sabitliyor.
- Geri düşüş testleri: yeni `test_10bit_cuda_cikis_hatasi_yalniz_kare_cikarma_eski_yola_duser` (hwdownload,nv12 hatası → yalnız o komut eski yol, dhash/-ss cuda'da kalır, -threads 1 ve -start_number korunur); hwaccel hatası testine eski yolda cuda çıkış yok + -threads/-start_number sayısı eşit eki; cuda yok (AV1 değil) mevcut test.
- Suit: video 1340 yeşil (1338 + 2), 359 sn (.kos/kopru/suit.log 10:23).
- **v8 yeniden işleme BAŞLATILMADI**: commit sonrası RAM %86 (boş 4.3 / 31.7 GB) > %80. Tutanlar: claude -p pid 46328 4.2 GB, mcp-proxy 51972 3.8 GB, Desktop 1.8 GB (hiçbirine dokunulmadı). Tepe RAM ölçümü yok.
- Hazırlık yapıldı: eski `yeniden-1-uzun` partisi kendi env'iyle `video parti iptal` → dizin `.claude/v8/yeni-0828-iptal`; v8 önbelleğindeki 08:2x (eski kod) `_xQnSNlBP_w` paket.md/ocr-gurultu.txt/goz ve `xmbSQz-PNMM/goz` → `C:\Projeler\.video-cache-v8-eski0828` (indirmeler/altyazılar yerinde); `.claude/v8_yeniden.py` `--paralel 1`, USD tavan 5 → 4, çağrı 16.
- Sonraki adım: RAM ≤ %80 olunca `python .kos/kopru/arka.py .claude/v8_yeniden.log .claude/v8_yeniden.py`, ilk videonun kare çıkarmasında `python .kos/kopru/ram_top.py`. Harcama: bu turda API yok.

# VİDEO-13 rapor (11 Eki 14:1x, ~40. tur — ARA: API'li ölçüm başlamadı, RAM %83–85 > %80)
Faz A (API'siz, HYMDaMcuSGQ A/B "yalnız eskide" 11 aday + 1 komut; URL kaçan 0): (1) algı 0 · (2) model 2 · (3) etiket 0 · (4) eşleme 6 kesin + 4 belirsiz.
| aday | sınıf | kanıt | onarım |
|---|---|---|---|
| Gelen Kutusu/Araştırma Masası/Dava Dosyası/Dükkan hattı (A–D) | 4 | eski:54–57 ↔ melez:77–80 "Seviye X · Ad" | v8_kars kelime-kümesi eşlemesi (yapıldı) |
| Dosya klasörünü tarayıp… (ajan döngüsü) | 4 | eski:58 ↔ melez:83 "Ajan döngüsü gösterimi" | anlamsal; alias gerekir |
| Proje talimat dosyasını kurmak | 4 | eski:59 ↔ melez:40 CLAUDE.md, :68 /init | anlamsal; alias gerekir |
| D/C seviyesi…, Dükkan sabah koşusu, Araştırma masası sorgusu | 4? | eski:63/64/67/69; melezde karşılık belirsiz | prompt satırı mı aday mı — karar |
| Git | 2 | paket:479 git clone; melez yalnız komut | gürültü; onarım yok |
| /usage (komut) | 2 | paket:642 OCR "/USAGE - BU CLAUDE CODE"; melezde 0 | OCR büyük harf komutu casefold → komut adayı |
OCR bozulmaları (kaçışa yol açmadı): CLAuDE.md, pytnon3, IUSAGE. ASR kaynaklı kaçış bu videoda YOK.
Altın küme (FaChtkkG9X4 · aZe5ZTYcF1M · 1nGx7WR8YLE) sınıflanamadı: tools/video/tests/fixture/altin/altin.json sentetik fixture ("not":"fixture"), bu üç videonun gerçek altın JSON'u bulunamadı → ölçümün ön koşulu: altın JSON yeri/üretimi.
Faz B/C (bayraklı, varsayılan KAPALI; test_video13 3 test kırmızı→yeşil):
- ASR ad onarımı goz.asr_onar + cli Segmentler (env VIDEO_ASR_ONAR=1): 1–3 kelime bulanık ad → kanonik (eslesmeler ses kuralı), sözlük = sozluk.txt (altın-hariç).
- C3 (b) parti.kare_kucult (VIDEO_JETON harfi K, ör. C2K): model karesi uzun kenar 768→512 (görüntü jetonu ~−55%), kopya pdir/kucuk/<id>, önbellek karesi değişmez.
- Eşleme: .claude/v8_kars.py kelime-kümesi kuralı → HYMDaMcuSGQ melez aday geri çağırma 69/80 → 69/74 (birleşim daraldı), yalnız eskide 11 → 5 (Git + 4 anlamsal); not: "D seviyesi dükkan verisini…" gibi prompt satırları hat adına eşleşiyor (gevşek).
| onarım | önce→sonra | karar |
|---|---|---|
| VIDEO_ASR_ONAR | ölçülmedi | bayrakta (Faz A'da ASR kaçışı yok; kanıt yok) |
| C3 K (512 kenar) | ölçülmedi | bayrakta; ölçüm: altın küme ×3, C2 vs C2K, ad yazım + USD |
| v8_kars kelime kümesi | eşleme kaçanı 10→4 | ölçüm aracında |
Yapılmadı: haiku "kaçan tarayıcı" ikinci geçiş, OCR hedefli yüksek çözünürlük kare, C3 (a) OCR-metin-yerine-kare ve (d) sabit önek — tur bütçesi + Faz A'da algı/etiket kaçanı çıkmadı (öncelik eşleme + /usage). API harcaması $0.

# VİDEO-13-devam (11 Eki 18:5x — ARA: çağrı hook'u 45/45 DUR; ölçüm arka planda)
1. Altın küme: GERÇEK altın JSON zaten vardı — docs/video-tarama/altin/{FaChtkkG9X4,aZe5ZTYcF1M,1nGx7WR8YLE}.json (Desktop doğruladı 07 Eki; aday 17/23/23). Önceki rapordaki "yalnız sentetik fixture" bulgusu YANLIŞ (fixture/altin ayrı test verisi). HYMDaMcuSGQ.json yok → kör etiket alt ajanda (sonnet, ek API yok), aynı dizine yazıyor; dosya + belirsizler listesi commit'lenmedi, sonraki oturum doğrular.
2. /usage: kök neden OCR "/"yu "I" okuyor (paket:660 "IUSAGE - BU CLAUDE CODE SOHBETI"); goz.ocr_satirlar → _slash: satır başı [/Il|]+BÜYÜK ve casefold CC slash listesinde (goz.SLASH) ise "/usage". Kırmızı→yeşil (test_video13 4/4). Yalnız yeni paketlerde etkili; ölçüm kopya paketleri eski.
3. Eşleme: altin.eslesir zaten ad+alias+lev≤1 kullanıyor → HYMDaMcuSGQ.json alias'ları eşad tablosu. v8_kars kelime-kümesi altin.py'ye TAŞINMADI (puan testlerini değiştirir; ölçüm sonucu görülmeden yapılmadı).
4. Yapılmadı: C3 (a) OCR-metin-yerine-kare, (d) sabit önek, haiku kaçan tarayıcı — tur/çağrı bütçesi.
5. Ölçüm: .claude/v13_olc.py (v10_olc kopyası), olcum_sira --oncelik ile arka planda (günlük .claude/v13_olc.log): altın 4 video (short FaCh+aZe5 · uzun 1nGx+HYM) × {taban (VIDEO_JETON boş = varsayılan) · K · C2K} × 3 tekrar, tekrar dışta; ayrı VIDEO_CACHE (.video-cache-v13 kopya) / TARAMA_DIZIN / UYGULA_KOK (.claude/v13/); Σ USD ≥ 19 → dur. Çıktı satırları OZET (jeton/usd/süre) + PUAN (aday/ad yazım · komut · url · denetle_rc). HYMDaMcuSGQ PUAN'ı altın JSON yazılınca alınır (yoksa rapor var, puan yok).
   ASR_ONAR kolu yok: paket yeniden kurulumu gerektirir; Faz A'da ASR kaçışı 0 → bayrakta.
| mekanizma | önce→sonra | karar |
|---|---|---|
| /usage casefold | paket "IUSAGE" → "/usage" | varsayılan (düzeltme, bayraksız) |
| K (512 kenar) | ölçüm sürüyor | bayrakta, v13_olc.log bekleniyor |
| C2K | ölçüm sürüyor | bayrakta |
| ASR_ONAR · C3a · C3d · haiku | ölçülmedi / yazılmadı | bayrakta / yok |
Video suit bu oturumda tam koşmadı (yalnız test_video13 4/4) — runner ağacı goz.py değişikliğini yüklüyor; sonraki oturum ilk iş suit.
Sonraki: v13_olc.log OZET/PUAN → 3 tekrar ortalaması Kabul satırına göre K/C2K kararı; HYMDaMcuSGQ.json doğrula + commit; iki taraf yalnız varsayılan değişirse.
