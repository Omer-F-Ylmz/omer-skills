# Skill paket sistemi

claude.ai kullanıcı yüklemelerinde 1000 kayıt sınırı var; skill'ler aile paketlerinde tek kayıtta toplanır.

## claude.ai sınırları
- Zip'te **tek SKILL.md** (paket girişi). Alt skill'in SKILL.md'si `skills/<ad>/TALIMAT.md`, daha derindekiler `SKILL-ornek.md` olur.
- Paket başına en fazla **200 dosya**. Aşılırsa alt skill'in ek .md'leri `REFERANS.md`'de `## [yol]` başlıklarıyla birleşir; yine aşılırsa `ValueError`.
- Paket adında **claude/anthropic yok**; açıklama ≤200 karakter; zip < 9.5 MB.
- Kullanıcı başına **1000 kayıt**.

## Araçlar (`tools/skill-paket/`)
- `paketle.py <paket-adi> "<konu>" <cikti_dizini> <skill_dizini>...` yeni paket zip'i üretir.
- `ekle.py [--uzerine] <mevcut.zip> <cikti_dizini> <skill_dizini>...` mevcut pakete skill ekler, aynı adla yeni zip üretir. Eski alt skill'ler bayt bayt aynı kalır. Aynı adlı alt skill varsa hata verir, `--uzerine` değiştirir. Sınır aşılırsa hata metni hangi skill'lerin yeni pakete gitmesi gerektiğini yazar.
- `test_paketle.py` pytest (12 test): `python -m pytest tools/skill-paket -q`.
- `tek-sefer/` Desktop'ın yazdığı geçmiş betikler (`aile_paket`, `ecc_paket`, `tek_skillmd`, `p3`); /tmp ve /mnt yolları sabit, yeniden koşulmaz.

## Akış
1. Yeni skill önce **ailesinin paketine** `ekle.py` ile girer.
2. Çıkan zip claude.ai'de **Replace** ile yüklenir. Aynı ad gerekir; eski sürüm geçmişte kalır, yeni kayıt açılmaz.
3. Yeni aile ya da dolu paket (200 dosya) olursa **yeni kayıt** gerekir. O zaman Ömer, pakette doğrulanmış bir kopya kaydı kaldırır; Claude kayıt silemez.
4. **Doğrulama:** yüklenen paket geri indirilir, dosya sayısı üretilen zip'le karşılaştırılır.

## Arşiv
- `dist\yukle-12\_paket_yuklenen`: canlı paketler.
- `dist\yukle-12\_paket_hazir`: bekleyen paketler. `dist/` git'te izlenmez.

## Envanter (dist'teki zip'lerden sayıldı; skill = `skills/<ad>/TALIMAT.md`)
Canlı (`_paket_yuklenen`, 22) + `mattpocock-paket` (canlı, zip `_paket_hazir`'da duruyor) = 23 paket.

| paket | skill | | paket | skill |
|---|---|---|---|---|
| azure-altyapi | 35 | | ecc-jvm | 18 |
| azure-uygulama-ai | 18 | | ecc-ml-bilim-saglik | 19 |
| context-mode | 8 | | ecc-orkestrasyon | 33 |
| designer-ai | 19 | | linkedin-agent | 11 |
| designer-liderlik | 57 | | marketing-skills | 49 |
| ecc-ag-homelab | 10 | | obsidian (v2) | 6 |
| ecc-ajan | 34 | | octo | 56 |
| ecc-backend | 25 | | reklam-ads | 33 |
| ecc-devops-guvenlik | 22 | | sepia | 6 |
| ecc-diller | 24 | | mattpocock | 32 |
| ecc-frontend | 24 | | | |
| ecc-icerik-pazarlama | 22 | | | |
| ecc-is-operasyon | 23 | | | |

Bekleyen 14 (`_paket_hazir`): adobe 14 · ai-etkilesim-tasarim 24 · android 25 · arayuz-iyilestirme 13 · chrome-devtools 7 · daymade-belge-finans-macos 21 · daymade-gelistirici 24 · daymade-ses 5 · erisilebilirlik 51 · hareket-altyazi-3d 9 · hyperframes 7 · tasarim-arastirma-strateji 38 · tasarim-etkilesim-ui 40 · tasarim-sistem-prototip 35.
