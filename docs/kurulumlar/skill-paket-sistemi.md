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
- `test_paketle.py` + `test_envanter.py` pytest (24 test): `python -m pytest tools/skill-paket -q`.
- `tek-sefer/` Desktop'ın yazdığı geçmiş betikler (`aile_paket`, `ecc_paket`, `tek_skillmd`, `p3`); /tmp ve /mnt yolları sabit, yeniden koşulmaz.

## Akış
1. Yeni skill önce **ailesinin paketine** `ekle.py` ile girer.
2. Çıkan zip claude.ai'de **Replace** ile yüklenir. Aynı ad gerekir; eski sürüm geçmişte kalır, yeni kayıt açılmaz.
3. Yeni aile ya da dolu paket (200 dosya) olursa **yeni kayıt** gerekir. O zaman Ömer, pakette doğrulanmış bir kopya kaydı kaldırır; Claude kayıt silemez.
4. **Doğrulama:** yüklenen paket geri indirilir, dosya sayısı üretilen zip'le karşılaştırılır.

## Arşiv
- `dist\yukle-12\_paket_yuklenen`: canlı paketler (51 zip + 3 tekil olacak). `mattpocock-paket.zip` `_paket_hazir`'dan buraya **kopyalandı** (orijinal yerinde). `dist/` git'te izlenmez.
- `dist\yukle-12\_paket_hazir`: bekleyen/eski paketler.

## Envanter (10 Eki 2026 10:30)
- claude.ai: **450/1000** kayıt = 389 eski + 51 paket + 9 paketsiz tekil (ideagram, web-design-engineer, banana, beautiful-article, img, orchestration, kb-retriever, last30days, webcmd-browser) + 3 kişisel tekil (fatura-kutusu, teklif-kutusu, prd-yaz).
- Kopyalardan 1 kayıt kaldı: `information-density`. Ömer kaldıracak.
- Paketlerde toplam **1358 skill**. 638 ikili dosya (213 MB) pakete alınmadı; asılları CC'de duruyor (REFERANS.md sonunda liste + asıl konum).
- Bu sabahki büyük yükleme: CC'de olup claude.ai'de olmayan 464 skill → 11 büyük paket + 3 tekil zip (`--buyuk` modunun atası: Desktop betiği `dist\yukle-12\_paket_yuklenen\buyuk_paket.py`).
- Not: yerel `_paket_yuklenen` klasöründe şu an 37 zip var (Desktop'ın 51 + 3'ü tam kopyalanmamış); canlı sayım claude.ai'dedir.

## Kural
Yeni skill önce temasının paketine `ekle.py` ile girer ve Replace ile yüklenir. Yeni tema varsa `paketle.py --buyuk` ile paket yapılır.

## Büyük mod ve envanter
- `paketle.py --buyuk <ad> "<konu>" <cikti> <skill_dizini>...`: alt skill başına en çok `TALIMAT.md` · `REFERANS.md` (tüm ek .md'ler `## [yol]` + ikili listesi ve asıl konum) · `KAYNAK-n.md` (diğer metinler `### yol` + kod bloğu, parça ~1.2 MB). Metin = ≤1 MB, NUL'suz, UTF-8. Tema taşarsa `<ad>-1`, `-2`… dengeli bölünür (≤200 dosya, zip ≤9 MB). Mevcut kurallar aynı.
- `envanter.py <claudeai_adlar.json> <cikti_dizini> [--home DIR]`: eski `envanter_fark` + `eksik_topla` + `eksik_metin` tek komutta. Girdi `{"giris": [...], "paket_uyesi": [...]}`; çıktı `envanter-fark.tsv` + `eksik-metin.zip`. Ad varyantları: `gstack-` öneki, claude→cc, `claude-` silme, `cc-` öneki. Son koşu: 464 eksik.
- Testler: `python -m pytest tools/skill-paket -q` (24 test).
