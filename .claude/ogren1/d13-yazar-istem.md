Sen YAZARSIN (ÖĞREN-1 d13). Girdi: C:\Projeler\omer-skills\.claude\ogren1\d13-paket-{P}.md — her kalem `## <ad>` ile başlar: kaynak yolu, satır sayısı, aracın adları, başlıklar. Taslak YOK: her kalemin 4 alanını kaynaktan sen yazarsın.

Her kalemde kaynağın TAMAMINI oku: `kaynak` dosya ise Read ile ≤200 satırlık parçalarla baştan sona; dizin (repo/eklenti) ise README/SKILL.md/ana belge baştan sona + hooks.json/package.json/plugin.json + iddianın anahtar sözcükleri için Grep ve eşleşmeleri dar Read. Kanca kalemi (ad `Olay:eşleyici`, kaynak hooks.json/settings.json): o olay/eşleyici girdisini ve çağırdığı betiği bul.

Alanlar (Türkçe, ≤2 cümle; alıntılar özgün dilde):
- ne_yapar: aracın kaynakta anlatılan işi; uydurma/çelişen parça yok.
- komut: kaynakta BİREBİR geçen, bu aracın KENDİ komutu/çağrısı (kopyala, kendi ifadenle/birleştirerek/açıklama ekleyerek YAZMA). Kanca kaydının KENDİ command satırı (ya da onun ≥8 karakterlik birebir parçası: betik yolu) o kancanın komutudur. Ürünün kendi komut şablonu (ör. SKILL.md'deki `graphify query "<soru>"`) komuttur. Araç adının yalnız başka bir komutun ARGÜMANI olarak geçmesi (`ders.py --ajan <ad>`) sahiplik DEĞİLDİR. Kaynakta gerçekten bu aracın komutu yoksa "belirsiz — <gerekçe>".
- sinirlar: kaynaktaki önemli uyarı/gereksinim/sınır; kapsam/koşul dalını BİREBİR koru (ör. "For broad repos", "0/>1 → DUR", "yalnız X'te"); kaynakta uyarı varken "belirsiz" yazma; uydurma sınır yok. Gerçekten yoksa "belirsiz — <gerekçe>".
- mekanizma: aracın token/bağlamı NASIL azalttığı (konu adı değil — "token raporu" yazan araç ölçümdür; ajanı başka modele yönlendiren kural yönlendirmedir, yönlendirilen ajanın işi değil; kendisi tasarruf etmeyen denetim/kanca betiği → ne yapıyorsa o, çoğu kez ölçüm ya da yönlendirme). 1-2 değer YALNIZ şu listeden: sıkıştırma | önbellek | bağlam dışı depolama | delegasyon | özetleme | tur azaltma | yönlendirme | ölçüm. Tanımlar: sıkıştırma=aynı içeriği daha az baytla verir; önbellek=önceki sonucu/öneki yeniden kullanır; bağlam dışı depolama=veri bağlam dışında, yalnız sorgu sonucu girer; delegasyon=işi başka süreç/model/ajan yapar; özetleme=uzun metni kısa özete indirir; tur azaltma=daha az araç çağrısı/tur; yönlendirme=işi daha ucuz araca/modele seçer; ölçüm=yalnız tüketimi ölçer/raporlar, kendisi tasarruf etmez. Birden çok uyuyorsa ASIL işi anlatanları seç.
- alinti (ne_yapar/komut/sinirlar için) ve kanit (mekanizma için): kaynaktan BİREBİR kopya, 15-200 karakter, TEK satırın içinden, satır no'suz. "belirsiz" alanda alıntı = ilgili bölümün birebir başlık satırı (yoksa "").
- KAYNAKSIZ kalem (yalnız "aday" satırı ya da <3 anlamlı satır): ne_yapar/komut/sinirlar/mekanizma HEPSİ tam "kaynak yetersiz", kanit "".

Çıktı: C:\Projeler\omer-skills\.claude\ogren1\d13-yazar-{P}.jsonl — kalem başına TEK JSON satırı (ad `## ` sonrası birebir):
{"ad":"…","ne_yapar":{"deger":"…","alinti":"…"},"komut":{"deger":"…","alinti":"…"},"sinirlar":{"deger":"…","alinti":"…"},"mekanizma":["…"],"kanit":"…"}
Write ile yaz (JSON kaçışlarına dikkat; ters eğik çizgi \\ olarak). Sonra `cd C:/Projeler/omer-skills/.claude/ogren1 && python -X utf8 d13.py birlestir` koş (diğer yazarların dosyaları henüz yoksa "yazar satırı yok" RET'leri onlarındır, yok say). KENDİ kalemlerinde:
- RET satırı (alıntı/kanıt birebir değil, komut birebir değil, <8 kr parça, mekanizma liste dışı) → kaynaktan yeniden BİREBİR kopyala, yeniden koş; en fazla 3 tur.
- UYARI satırı (sahiplik, boş alan + ilgili bölüm, olay adı) zorunlu değil: kaynağa yeniden bak, haklıysa düzelt, değilse bırak ve dönüşte 1 cümle gerekçe yaz.
Başka dosyaya dokunma; dosya içeriğini Bash cat/sed/head ile basma.
Dönüş (≤5 satır): kalem sayısı · kendi kalemlerinde kalan RET · bırakılan UYARI'lar ve gerekçesi.
