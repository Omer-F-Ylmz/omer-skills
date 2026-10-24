# TOKEN-7b sonuç (24 Eki, YARIM-G6 devam)

Karar: **think10k + cmnudge** profili (`tools/olcum/profil-k7b-final.json`), cmnudge kanıtlı, think10k kısmi kanıtlı, birleşik tam set **tamamlanamadı** (G06–G12 yok). Uygulama onay betiğinde hazır, çalıştırmak Ömer'in kararı.

## 1. Veri (API'siz, 2026-10-10 t7b-tam, 12 görev × 2)

| profil | kalite ort | isabet ort | USD/koşu | tek-tur bağlam | kaçak(tur>20) |
|---|---|---|---|---|---|
| tam (taban) | 9.79 | 0.88 | 0.748 | 92.9k | 0 |
| k7b-cmnudge | 9.92 | 0.92 | 0.750 | 92.0k | 0 |
| k7b-birlesik (b40k+…) | 9.58 | 0.83 | 0.708 | 86.6k | 1 (G03) |

- cmnudge: kalite ve isabet ≥ taban, maliyet eşit → KABUL.
- think10k: 3 görevlik elemede 60/60 (taban 53), bağlam eşit; 12 görevlik tam kanıtı yok.
- birleşik (b40k dahil): G03 kaçak (1.60M bağlam) ve kalite düşüşü → REDDEDİLDİ, b40k elendi.
- b40k G06 isabet farkı: g06-yeniden-puan.tsv (TOKEN-7g rubriği) ile tam 1/4 · b40k 1/4 → fark gürültüydü.

## 2. Birleşik doğrulama (k7b-final × 1), kısmi

Ölçülen: G01 10 (ikinci koşu 8), G02 10, G03 10 (5 tur, kaçak yok), G04 10, G05 10 (isabet 0). Kalite düşüşü ve kaçak yok.
Ölçülmeyen: G06–G12 (7 görev). Kapı rubrik ≥233 / isabet ≥21 (24 koşuluk set) bu yüzden **hesaplanamadı**.
Neden durdu: claude -p tavanı 12 idi, 13 harcandı (G04'te süreç düştü, G01 yeniden koştu); kalan 7 koşu ≈ $9 (koşu başı $1.24–1.63) > oturum bütçesi $4; haftalık limit %93. Ayrıca bugünkü ortam büyüdü (tek-tur bağlam 158k, sabah-10 Eki'de 93k), mutlak USD/bağlam eski tabanla karşılaştırılamaz.

## 3. Uygula / geri al

`python C:\Projeler\omer-skills\.kos\kopru\onay\token_7b_uygula.py --kuru` (çalıştı: env'e iki anahtar eklenecek, ikisi de şu an yok) → `…token_7b_uygula.py` → `--geri`. Yalnız `env.MAX_THINKING_TOKENS=10000` ve `env.CONTEXT_MODE_BASH_NUDGE_MIN_COMMAND_BYTES=200`; yedek `settings.json.bak-t7b-<zaman>`. token_7a_uygula.py'ye dokunmaz.

Öneri: yalnız cmnudge (kanıtlı) istenirse betikten `MAX_THINKING_TOKENS` satırı çıkarılır; ikisi birden istenirse G06–G12 ×1 (≈7 koşu, Console API ya da limit açılınca) önce koşulur.

## 4. Kol 4–10

TOKEN-7c'ye devredildi (bkz. docs/token/token-7c.md); bu turda yeni iz toplanmadı.
