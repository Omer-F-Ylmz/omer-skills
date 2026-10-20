# BEYIN-4 d3 — kapı GEÇMEDİ (2012 sayısal %85, 2013 sayısal olmayan %90; token 3 tohumda >%25)

- Hakem: OmniRoute atlandı. Zincir OpenRouter :free (nemotron-super, gemma-4-31b 429 → minimax-m3.1-flash çalıştı) ve Groq gpt-oss-120b; Haiku'ya inilmedi (Groq cevap verdi), bulut çağrısı ~6. 2011 hakemi yapıldı: openrouter 20/20, groq 19/20 (%95–100).
- 2009 B 1/20 = ölçüm hatası: B cevap dosyasında "kaynak dosya bulunamadı" (B kolu dizin düzenini bilmiyordu). kapi.py B istemine dizin düzeni eklendi; 2009/2010 B yeniden koşulmadı.
- Kayıp türleri (`kayip.py`, tür düzeyi): A-aramada-yok (ilk aramada kaynak parçası çıkmıyor) · C-model (arama doğru, ajan yanlış okudu/tahmin etti) · B-parça-içi (B kolu biçim farkı: "(1) x (2) y" ile ham cevap; betik hakem sayar) · A-çok-kaynaklı (tek sorgu ikinci kaynağı dışarıda bırakıyor).
- Düzeltmeler (türe göre, soruya bakmadan): `tools/beyin.py` kimlik puanı gövde geçişini ikinci anahtara aldı; "(1)…(2)…" soruları parça başına aranıp birleştiriliyor (ilk-arama cevap içeriyor: 9 tohum-yanlışından 6'sı düzeldi); `uret.py` SAYI maskesi 127.0.0.1 gibi noktalı dizileri sayı saymıyor (2009 yanlışı 200902/04 = "127.0" vs "127", hakem sorunu); `kapi.py` bulut hakem zinciri.
- Sonuç (A kolu): 2012 sayısal 17/20 %85 (B 20/20) · 2013 sayısal olmayan openrouter 18/20 %90, groq 12/20 (çok-notlularda 0/8: hakem "(1) …" biçimini reddediyor, iki hakem çelişiyor) · 2011 %95–100.
- Token A/B: 2012 %38 · 2013 %33 · 2011 %42 → ≤%25 YOK. A kolu 30–31 tur; yeniden-arama azalmadı (ilk-arama kapsamı arttı ama ajan yine ikinci tur arıyor).
- Not: beyin.py değişikliği 2012/2013 A koşusundan SONRA yapıldı (kayip.py ilk-arama ölçümü yeni kodla); A kolu yeniden koşulmadı, tur/token ve %85–90 eski beyin.py ile.
- Kalan iş (başka oturum açılmadı): (1) A kolunu yeni beyin.py ile yeniden koş; (2) `beyin ara` ilk çıktıda yeterli bağlam vermeli ki ajan tek turda bitirsin: A_istemi "ikinci tur" yönergesini sil ya da arama bütçesini artır; (3) hakem: "(1)…(2)…" cevap biçimini normalize et (groq 0/8) ya da tek hakem ailesi + Haiku çapraz; (4) token tavanı %25 bu mimaride (35 turluk -p oturum, önbellek okuması) ulaşılmaz görünüyor — tavan A kolunun tur sayısıyla belirleniyor, B kolu da 41–45 tur.
- MAKARA-1 hazır DEĞİL; SIRA satırı yazılmadı (kapı geçmedi).
- Yollar: `.claude/beyin4/{kapi,uret,kayip}.py`, `sorular-2012/2013.jsonl`, `kosu/`, `tools/beyin.py`.
