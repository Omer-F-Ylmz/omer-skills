# BEYIN-4 d4 — kapı GEÇMEDİ (2014 sayısal %95 · token %25,5; 2015 sayısal olmayan %100 · token %50)

- Yapılanlar: A istemi ikinci-tur yönergesiz, soru başına tek arama, tur tavanı 12 (`kapi.py` CEVAP_A/TUR_A). `beyin ara` zaten "(1)…(2)…" parçalı soruyu tek çağrıda birleştiriyor; yeni tohumlarda ilk arama cevabı içeriyor: 2014 19/20, 2015 18/20 (`kapsam.py`).
- Hakem: "(1)…(2)…" normalize (referans parça parça sorulur, tam puan = tüm parçalar; 2015 28/28 parça). Havuz `tools/ucretsiz_havuz.py` (nvidia/openai aileleri). 2015 A: groq(gpt-oss-120b) 20/20; openrouter(nvidia) 429 → ikinci aile yok, **aile uyumu ölçülemedi**.
- 2009 B 18/20, 2010 B 20/20 (taban düzeltmesi: B kimlikleri string geliyordu → 0/20 sahte; `int(id)`). Eski B dosyaları `kosu/eski/`.
- Doğruluk: 2014 19/20 = %95 (yanlış 201408), 2015 20/20 = %100 → doğruluk ≥%92 sağlandı.
- Token (modelUsage girdi toplamı): 2014 A 66,9k / B 262,7k = %25,5 (tavan %25'i 0,5 puan aşıyor); 2015 A 107,9k / B 216,2k = %50. API turu A 2, B 3; ihlal 0.
- Ölçülmüş alt sınır: A en az 2 istek (arama + cevap); sabit ilk istek ≈18–20k jeton, ikinci istek = sabit + arama çıktısı (20 soru ≈ 43k karakter ≈ 28k jeton → 46–47k). Yani istek başına bağlam tabanı ~19k, A tabanı ≈ 2×19k + çıktı ≈ 65k; B'nin hesaba giren toplamı 216–263k olduğundan oran B'ye bağlı: B ucuz kaldığı tohumda (2015, B 216k) %25 için A ≤54k gerekir, ama A'nın tabanı (sabit 38k + 20 soru için en az ~20k çıktı) ≈58k+ → 2015 tipinde ≤%25 yapısal olarak erişilemez; 2014 tipinde (B 263k) tavan 65,7k, A 66,9k → sınırda.
- Kayıp sınıfları: doğruluk kaybı yok (tek yanlış 2014 sayısal 1/20); kapıyı tutan tek şey token — sınıf "A-sabit-yük" (istek başına ~19k bağlam + 20 sorunun birleşik çıktısı). Düzeltme yolu betik değil, sorgu boyutu: soru başına çıktı bütçesi `--butce` (şimdi ~2,1k karakter) düşürmek, ya da parti boyunu 20→40 soruya çıkarıp sabit yükü bölmek; ikisi de bu kapı için denenmedi (kapı sorularına bakıp ayar yasağı).
- Sapmalar: 2015 B kolu (sayısal olmayan) hakemlenmedi (kapı A doğruluğu + token oranı); ikinci hakem ailesi 429.
- MAKARA-1 DEĞİL; SIRA satırı yazılmadı. Başka oturum açılmadı (2-4 kuralı dolu).
- Yollar: `.claude/beyin4/{kapi,kapsam,uret,kayip}.py`, `sorular-2014/2015.jsonl`, `kosu/d4-log2.txt`.
