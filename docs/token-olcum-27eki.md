# Token ölçümü, Desktop mu, alt ajanlar mı? (7 gün: 21–27 Eki 2026)

**Sonuç:** Token/$ ağırlığı alt ajanlarda (kuyruk + köprü CC oturumları). Desktop ana oturumunun kendi payı bu kaynaklardan ölçülemiyor (aşağıda "ölçülemeyen").

## Kaynaklar ve sınırlar
- `claude-usage week` (CC transkriptleri, tüm CC oturumları): **$716,56**, 13.835 tur, 1570 oturum. Sonnet $584,77 · Haiku $78,66 · Opus $53,13 · ücretsiz (nemotron) $0.
- `ajan-sira/*.json` (kuyruk işi başına, son 7 gün, 1196 dosya): 602 başarılı = **$511,75**; 552 dosyada modelUsage yok ($0, bkz. d); 41 hatalı = $8,52.
- `maliyet.tsv` (491 satır, 7g): $285,05 (yalnız defterlenen işler; ajan-sira'dan düşük, defter eksik).
- Fark: $716,56 − ~$520 = **~$196** kuyruk dışı CC oturumu (köprü/etkileşimli, bu repodaki oturumlar). Desktop (claude.ai uygulaması) oturumu `~/.claude/projects` altında değil; `cc-kopru` günlüğü bu makinede yok → **Desktop ana oturum $'ı ölçülemedi**, tahmin yazılmadı.

## Kırılım
| Dilim | $ (7g) | İş | Not |
|---|---|---|---|
| (b) Köprü/kuyruk, Sonnet baskın | 457,67 | 464 | iş başı ~$0,99; 14.6k tur, 786M önbellek okuması |
| (c) Opus baskın | 51,18 | 14 | iş başı **$3,66**; 527 tur |
| (c) Haiku baskın | 9,51 | 133 | iş başı $0,07 (Haiku ayrıca Sonnet işlerinin içinde alt ajan: toplam $78,66) |
| (c) Ücretsiz havuz | ~0 |, | claude-usage'da nemotron 50 tur, $0 |
| (d) Boşa/hatalı | 8,52 | 41 | 502: 19 iş ($0,40) · 429/limit: 17 ($5,37) · bütçe tavanı kesilen: 5 ($2,75) · kurtar 31 / kesik 4 / ramkesti 2 dosya |
| (d) modelUsage'sız | 0 | 552 | çoğu .json = boş/erken çıkış; maliyeti yok ama kuyruk sayacını şişiriyor |

Önbellek okuması maliyetin ana kalemi (Sonnet 786M jeton): uzun, çok turlu işler pahalı; çıktı jetonu küçük.

## En pahalı 10 iş (ajan-sira)
ogren-3-d2 $18,96 (2 tur, tek uzun çağrı) · ogren-4-d2 $11,18 (82 tur, 43 dk) · ogren-3-d3 $9,93 · ogren-4-d3 $9,78 · oktan-film-3 $8,77 (62 tur, 129 dk) · ogren-tur2-d1 $8,16 (75 tur) · telve-v2-faz1c $7,85 (1 tur) · ogren-6-d3 $7,09 · ogren-2-d3 $6,73 (80 tur) · neffex-klon-5 $6,69.
Örüntü: "ogren-*" öğrenme turları 7/10'u tutuyor ve tek turda $7–19 (büyük bağlam yükleme); uzun-tur işler (60–80 tur) bağlam şişmesiyle pahalanıyor.

## Doğru işe doğru model (ölçüme dayalı)
| İş türü | Önerilen basamak | Gerekçe |
|---|---|---|
| Özet, log süzme, sayım, biçim, sınıflama | Ücretsiz havuz (`ucuz_alt.py`, jev) | $0; Haiku iş başı $0,07 bile gereksiz |
| Okuma/araştırma, test koşusu | Haiku (okuyucu / suite-kosucu) | iş başı $0,07 vs Sonnet $0,99 |
| Kod yazma, tek-alan düzeltme | Sonnet medium | 'yarim' sonnet-medium iş başı $0,46 vs sonnet-high $0,79 (maliyet.tsv) |
| Çok-dosya mimari, kritik karar | Sonnet high | Opus gerektirmeyen çoğu iş |
| bhs/neffex/telve tipi büyük üretim | Opus yalnız son birleştirme | Opus iş başı $5,1–5,5, 2'şer iş = $31,7; ilk taslak Sonnet/ücretsiz |

## Desktop tasarruf önerileri
1. Kontrol turu tek çağrı: kuyruk durumu için tek `cm.py run` (özet dönsün); tur başına ayrı okuma yok.
2. Sonuç okuma: `.json`/log'u Desktop okumasın; `ucuz_alt.py --tur ozet` ile ücretsiz özet, yalnız ≤10 satır döner.
3. Tarif yazımı: iş başı hedef tavanı (`--max-budget-usd`) her tarifte; 5 iş tavana çarpıp kesildi ($2,75 boşa).
4. 429/502 işleri yeniden kuyruğa atmadan önce limit penceresi kontrolü (17+19 iş boşa).
5. Uzun-tur işleri (>40 tur) bölünsün; 60–80 tur işler $6–11.

## Ölçülemeyen / yapılmadı
- Desktop ana oturum $'ı: günlük yok (yukarıda). Önerilen ölçüm: Desktop köprü çağrılarına `cc-kopru` günlüğü eklemek (ayrı görev G1).
- `is-kaydi.tsv` adım/ağırlıklı sütunları kullanılmadı (kodlama bozuk, `kalite` sütunu metin).
- Haiku/Sonnet ayrımı ajan-sira'da "baskın model" ile yapıldı; alt ajan payı için claude-usage rakamı esas alınmalı.

## Uygulanabilir görevler (kuyruğa EKLENMEDİ, Desktop karar verir)
- G1: Desktop köprü çağrıları için `.kos/kopru/cc-kopru.jsonl` (zaman, iş, $) yazan tek satırlık kanca.
- G2: Kuyruk yürütücüsüne varsayılan `--max-budget-usd` ve 429/502 geri çekilme penceresi.
- G3: "ogren-*" turlarını ücretsiz havuza taşıma denemesi (7 iş = ~$70/hafta).
- G4: `ajan-sira` boş (modelUsage'sız) dosyaları sayıma almayan rapor süzgeci.
