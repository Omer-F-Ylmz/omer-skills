---
type: report
status: tur-2-bitti
tags: [borsa, trading, gelistir-1]
relatedTo: [borsa-botu]
---
# BORSA-GELISTIR-1 tur 2 (7 Kas 2026) — TUR BITTI, ADAY YOK
Gerçek emir/para/push/silme yok. Kod: Desktop\Claude ile yapılanlarorsa-botu (testler 61/61, 24 yeni kırmızı-önce + sızıntı testi).
**Eklenen (kaynak: rapor/kaynak-yontemler.md 'sıradaki 8'):** fractional-Kelly (risk.kelly_olcek) · olasılıksal rejim yönlendirici (ER+Hurst → p_trend) · GARCH(1,1) sabit-parametre + EWMA vol ölçekleme (vol_hedefle 0/1/2) · FOMC(Fed sayfası 2021-27)+NFP takvim filtresi · Hurst(varyans oranı)/ADF-t · hacim profili POC/VA ajanı · parametre komşuluk taraması (ADAY: kapı ≥%75 veri + komşu pozitif ≥%60) · short borç maliyeti %10/yıl · pairs (cift.py) · fonlama taşıma (funding.py) · özellik önbelleği · 5→12 veri (8 sembol, 45k saatlik bar ≈5 yıl; 4h ≈6,8 yıl).
**Önce/sonra (aynı 12 veri, aynı maliyet; test = son %40, ort beklenen R):** tur-1 lideri −0,042 (3/12 pozitif; BNB 4h +0,082, PF 1,35) → nesil ~5 lideri −0,088 (1/12 pozitif; ETH 4h +0,009). Eğitim skoru −0,124 → −0,089 (sahte kenarsız, 3-4,6k işlem). Eğitim yeni genlerle yeniden başladı, yakınsamadı (~3 dk/nesil, CPU yoğun); kapıya giren genom yok.
**Pairs (6 çift, sabit parametre, test):** 6/6 KALDI, R −0,09…−0,54, PF 0,3-0,8 (kayit/cift-olcum.json). **Fonlama taşıma (spot long+perp short), test net/yıl:** BTC %6,9 · ETH %6,5 · LINK %7,5 · ADA %6,3 · XRP %5,8 · DOGE %5,1 · SOL %1,9 · BNB %0,3; filtreli girişler zarar (churn); fonlama DD ≤%0,6-3,8. Baz/marj/likidasyon/borsa riski modellenmedi → 'risksiz' değil (kayit/fonlama-olcum.json).
**Kaynak taraması recall:** ÖLÇÜLEMEDİ — örnekleyici (borsa-botu/recall_olc.py: eşleşmeyenden 900 rastgele dosya + geniş bağımsız desen + 40 eşleşen, sonra bağımsız etiketleme) 250-600 sn'lik üç koşuda bitmedi (eğitim CPU'yu tutuyor, korpus büyük); recall sayısı yok, tur 1'deki '≥%98' iddiası doğrulanmış sayılmaz.
**Bağımsız hakem:** jev kanit (1/3 istek) 13 satırdan 'önce/sonra' p=0,33 Flag (ortalamalar kanıt dosyasında yoktu → kayit/tur2-ozet.json eklendi, yeniden koşulmadı), pairs 0,55 ve 'gerçek emir yok' 0,59 Escalate; kod iddiaları kod dosyası verilmediğinden düşük destek. Sert puanlayıcı (pixeljury) ve jev ile strateji puanı bu turda alınmadı (jev_evaluate MCP araçları oturumda yüklü değildi).
**Araçlar:** autoharness (guide+doctor koştu; doctor probe 3/3 başarısız=0,00 — komut elle 61 geçti, probe nedeni ölçülemedi; optimize döngüsü ücretli claude üretici gerektirir, koşmadı), jev kanit, beyin kaydet, rg/python tarama, Fed resmi sayfası.
**Sapmalar:** GARCH MLE ile uydurulmadı (sabit α=0,08 β=0,90); CPI tarihi yok; 2020 FOMC yok; Fed sayfasında 2025 Eylül ay etiketi 'August 16-17' çıktı, 16-17 Eylül alındı; ADAY kuralı 'hepsi'den %75'e gevşetildi (korele kripto, komşuluk şartıyla).
**Sıradaki:** eğitimi sürdür (ADAY yok); fonlama taşımayı ayrı paper modülüyle ileri test (spot+perp fiyatıyla baz riski ölçülerek); GARCH MLE; gerçek L2 order book; CPI takvimi.
