# Hafif çağrıda kare okuma (MOTOR-M2d K1)

- Test: 640×360 sentetik PNG, metin `TELVE-7342` + kırmızı kare; `hafif.cagir` gerçek yolu (stream-json `image`/`base64` bloğu), 1 çağrı, $0.0067.
- Model yanıtı: metin `TELVE-7342 (siyah renkli, sans-serif, normal kalınlıkta yazı; beyaz arka plan üzerinde sol üstte)` · şekil `Sağ altta, düz kırmızı renkte dolu bir kare (kırmızı kare) var.`
- Sonuç: **okundu**.
- Biçim düzeltmesi: media_type önceden sabit `image/jpeg` idi; artık dosya türünden (`mimetypes`). Motor kareleri `.jpg` olduğundan M2a-M2c taramalarında etiket doğruydu.
- Regresyon: tools/video/tests/test_m2d.py::test_gorsel_blok_bicimi (sahte taşıyıcıda blok yapısı + media_type).
- M9qgd_KJkWc'de `karede_gorulen` boşluğu kare okumamaktan değil, form/istem kaynaklı olmalı; bağlantı girdisi hatası ayrıca düzeltildi (docs/olcumler/url-hatasi-etki.md).
