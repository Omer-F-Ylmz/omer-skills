# YARIM-BEKCI-1 raporu (24.10)
Koşu (canlı durum, 12:46): açık 17 → H1:5 · H2:2 · H3:8 · H4:2 · H5:0 · H6:0. Otomatik düzeltilen: 0 (canlı kuyrukta H5/H6 yok; düzeltme yalnız testte kanıtlı).
- `yarim_bekci.py`: tarama + yarim.tsv + düzeltme; `--ozet` / `--devir` çıktıları. Muaf: `yarim-muaf.tsv` (Ömer'in 10 kararı, mod-mai-onizleme, REA uyarısı, 4 belge dosyası).
- Yönetici: `ajan_sira.py` her 10 dk çalıştırır, `YARIM <tür> <ad> <eylem>` / `YARIM-DUZELTILDI …` log'a yazar; yönetici `YENİLE BEKLE`'de, idle olunca yeni kodla açılır (öldürülmedi).
- `kontrol_tur.py` ve `kontrol_ozet.py` çıktısının ilk satırı `YARIM: n açık (…)`.
- Test: `test_yarim_bekci.py` 20 yeşil (kırmızı önce görüldü: modül yok). H5 düzeltmesi yalnız tsv'deki yolu değiştirir, görev dosyası içeriği ve dosya listesi aynı kalır; H6 yalnız görev dosyasına satır ekler.
Sapmalar: (1) H2'de `yapılmadı|durduruldu|BULUNAMADI` yalnız başarısız bitişte sayılır (başarılı raporlarda "Push yapılmadı" 56/69 gürültüydü); `Karar gerekiyor|onay gelirse|yapılsın mı` her durumda. (2) H1 `-a/-a2/-r` otomatik deneme adlarını saymaz. (3) Devir notunu üreten betik yok (elle yazılıyor): `python yarim_bekci.py --devir` blok basar, Desktop devire yapıştırır. (4) Pencere: H1–H4 son 3 gün.
Açık, Desktop'a: H3 `yarim-tara-1` ve `video-repo-2` son 2 saatte bitti, rapor yok; `gorev-usta-blender-1` gorev/ içinde yanlış adlı görünüyor (muaf değil).
