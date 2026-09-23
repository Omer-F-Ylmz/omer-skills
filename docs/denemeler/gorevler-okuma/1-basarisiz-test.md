Aşağıdaki pytest çıktısında başarısız olan testi ve nedenini bul. Yanıt en fazla 3 satır: test adı, dosya:satır, neden.
oku: fixture/test-ciktisi.txt
araclar: Read,Grep,Glob
beklenen:
- olgu: test_indirim_sinir_esik
- olgu: test_fiyat\.py:88
- olgu: (?i)(100 == 90|beklenen 90|90 yerine 100|100.*90)
- satir-en-fazla: 3
