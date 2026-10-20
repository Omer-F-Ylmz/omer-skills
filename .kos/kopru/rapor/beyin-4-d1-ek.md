# BEYIN-4 d1 EK (Desktop 16:20) — kapı koşuldu, EŞİK ALTI; sayısal olmayan doğruluk ölçülemedi

- Eklendi: `uret.py 2011:ad` = sayısal olmayan + çok notlu tohum (cümlede bir kez geçen backtick adı; betik üretir; 20 soru, 8 çok-notlu); `kapi.py` 2011'i koşar, hakem = iki aile (nvidia, google) OmniRoute :free, sayısalda betik.
- Sayısal doğruluk (betik hakem, A = `beyin.py ara`): 2009 16/20 (%80), 2010 19/20 (%95) → ≥%92 YALNIZ 2010'da. 2009 B kolu 1/20 (B hatalı/biçim sorunu şüpheli, B'nin cevap dosyası denetlenmedi).
- Token A/B: 2009 %79, 2010 %48, 2011 %42 → ≤%25 HİÇBİRİNDE. A kolu 31–35 tur harcıyor (yeniden arama).
- Sayısal olmayan (2011) doğruluk: ÖLÇÜLEMEDİ — iki ailenin tüm :free modelleri (nemotron-3.5-lightning/super/ultra, gemma-4-31b/26b) 10/10 denemede HTTP 429. İlk koşudaki "0/20" gerçek skor değil (kod bunu artık "YOK (429)" yazıyor). A/B cevapları `kosu/A2011.json` içinde duruyor; hakem kotası açılınca `kapi.py A2011` yeniden hakemler (önbellek: kosu/hakem-*).
- Sonuç: kapı GEÇMEDİ (doğruluk 2009 %80; token üç tohumda >%25). MAKARA-1 hazır DEĞİL.
- Kalan iş: (1) 2011 hakemini kota açılınca koş; (2) token ≤%25 için A kolunun tur sayısı (31–35) düşmeli — ilk aramada eksik kalınca yeniden arama; (3) 2009 B/A yanlışlarının türünü kayip.py ile sınıfla.
- Sapma: (a)'daki ≥10 ek soru 2011 ile karşılandı (20); (b) kısmen — bulut hakem kuruldu ama koşamadı; (c) iki ayrı doğruluk raporlanamadı.
- Yollar: `.claude/beyin4/{uret,kapi}.py`, `sorular-2011.jsonl`, `kosu/`. SIRA satırı yazılmadı (biçim bilinmiyor, kapı geçmedi).
