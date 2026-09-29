# URL hatası etki listesi (MOTOR-M2d, 2026-09-29)

**Hata:** `tools/video/video/cli.py` `_temizle`: sürücü harfi deseni `[A-Za-z]:[\\/]`, `https://` içindeki `s:/`'yi yerel yol saydı. Boşluğa kadar her şey `[yol]` oldu, açıklama bağlantısı `http[yol]` olarak kaldı. **Düzeltme:** desenin önüne `(?<![A-Za-z])` eklendi. Regresyon testi: `test_m2d.py::test_aciklama_baglantisi_cagri_girdisinde`, mutasyonla kırmızı.

## `_temizle`'yi çağıran yollar
1. **Motor taraması:** `parti._istem` (parti.py:171, temizleyici :276). Hafif `claude -p` çağrısına giden paket metni bu fonksiyondan geçiyor.
   - Etkilenen: `2026-09-29-short` partisinin 8 videosu (`.kos`'ta tek motor partisi bu). 7 short `tamam` durumdaydı ama bağlantısız girdiyle taranmıştı. M9qgd_KJkWc, skool.com bağlantısını hiç görmediği için `karar yok` hatasıyla takıldı.
   - Onarım: `video parti devam 2026-09-29-short --yeniden-tara` ile 8 video yeniden tarandı, ardından `parti akil` koştu. Harcama: hafif 5 çağrı, $0,4641. Panel farkı aşağıda.
2. **2a OpenRouter kolları:** `cli.tara` (cli.py:543-544), sistem mesajı ve paket metni `_temizle`'den geçiyor. TOKEN-DENEME-2a OpenRouter ölçümleri bozuk girdiyle yapıldı. Not docs/denemeler/ucuz-tarayici.md'de: RED kararı M3 onarım turunda yeniden ölçülecek.

## Doğrudan etkilenmeyen, dolaylı etkilenen
- **akil araştırma istemleri** (`akil._on`, `_form_al`): `_temizle` çağırmıyor. Ama aday ve repo bilgisi tarama raporlarından geldiği için, açıklamadaki repo/araç bağlantıları eski raporlarda eksikti. Bu yüzden akil yeniden koştu.
- **Alt ajanlı akış** (video-tarayici): paket.md'yi doğrudan okuyor, etkilenmedi. `video temizle` komutu (cli.py:942) `_temizle`'yi çağırmıyor.

## Yeniden tarama sonucu (2026-09-29-short)
- M9qgd_KJkWc: bağlantı hatası kalktı. Hâlâ `form_red`, çünkü `adaylar[1].karede_gorulen` boş ve raporda 3 kanıtın zamanı yok. Kare okuma sorunu değil: docs/bilgi/hafif-cagri-gorsel.md'deki K1 testinde kare okundu.
- NogIRR1B6gY: önce `tamam`dı, yeniden taramada `form_red` oldu (`karede_gorulen` boş). Eski raporu duruyor.
- task-observer: SOR (Jev 0.73) iken ZATEN VAR oldu (önek soyma).
- Panel: 35 satır değişti. Aday slug'ları değişince bazı satırlarda Ömer sütunu boş kaldı: harness-kavrami → harness-katmani-ajan-ara-katmani, ucretsiz-llm-api-listesi-reposu → ucretsiz-llm-api-deposu-adi-belirtilmemi. Kaybolan satırlar: otomatik-hafiza (ÖĞREN), coklu-paralel-oturum (RED), ajan-yardimci-ajan-orkestrasyonu (ZATEN VAR). webcmd türü skill'den CLI'ye döndü (UYARLA korundu). markitdown-microsoft satırı düştü (DENE). Ömer'in kararları panel kapanmadan yeniden girilmeli.
