Sen KÖR HAKEMSİN (ÖĞREN-1 d13 kapısı). Bu özetleri sen yazmadın; başka hakemin kararını görmüyorsun.
Girdi: C:\Projeler\omer-skills\.kos\kopru\ogren\hakem-d13.jsonl — 28 satır, her biri {"ad","kaynak","ne_yapar","komut","sinirlar","mekanizma"}. Read ile oku.

Her kalemde 4 alanı (ne_yapar, komut, sinirlar, mekanizma) kaynağa göre puanla: D (doğru) ya da Y (yanlış).
- Kaynağın TAMAMINI kontrol et: `kaynak` dosya ise Read ile ≤200 satırlık parçalarla baştan sona; dizin (repo/eklenti) ise README/SKILL.md/ana belge + iddianın anahtar sözcükleri için Grep ve eşleşmeleri dar Read ile. Kanca kalemlerinde (ad `Olay:eşleyici`) kaynak hooks.json/settings.json'dır: o olay/eşleyici girdisini ve çağırdığı betiği bul.
- ne_yapar D: kaynağın anlattığıyla örtüşür, uydurma/çelişen parça yok.
- komut D: belgede BİREBİR geçen ve bu aracın KENDİ komutu (adının bir biçimi, kendi dizinindeki dosya ya da kendi manifest paket/ikili adı; kanca komutu satırın birebir parçası olabilir). Başka aracın komutu Y. "belirsiz — gerekçe": belgede gerçekten bu aracın komutu yoksa D, varsa Y.
- sinirlar D: kaynaktaki önemli uyarı/gereksinim/sınır doğru aktarılmış; kaynakta uyarı varken "belirsiz" Y; uydurma sınır Y; sayı/koşul dalı kaynakla birebir uyuşmalı.
- mekanizma D: liste değer(ler)i aracın ASIL tasarruf yolunu anlatıyor. Tanımlar: sıkıştırma=aynı içerik daha az bayt; önbellek=önceki sonucu/öneki yeniden kullanır; bağlam dışı depolama=veri bağlam dışında, yalnız sorgu sonucu girer; delegasyon=işi başka süreç/model/ajan yapar; özetleme=uzun metni kısa özete indirir; tur azaltma=daha az araç çağrısı/tur; yönlendirme=daha ucuz araca/modele seçer; ölçüm=yalnız tüketimi ölçer, kendisi tasarruf etmez. Asıl işi kaçıran ya da asıl işi olmayan değer içeren seçim Y.
- "kaynak yetersiz" yazan alan: kaynak gerçekten yalnız aday satırı/<3 anlamlı satır ise D, değilse Y.

Çıktı: C:\Projeler\omer-skills\.claude\ogren1\{H}.jsonl — kalem başına TEK JSON satırı, ad girdidekiyle birebir:
{"ad":"…","ne_yapar":"D","komut":"Y","sinirlar":"D","mekanizma":"D","gerekce":{"komut":"Y kararının 1 cümlelik gerekçesi + kaynak satırı"}}
28 satırın hepsi olmalı. Write ile yaz (JSON kaçışlarına dikkat). Başka dosyaya dokunma. Dosya içeriğini Bash cat/sed/head ile basma.
Dönüş (≤3 satır): satır sayısı · alan bazında Y sayısı · Y verilen (ad, alan) listesi.
