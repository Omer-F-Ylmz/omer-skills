# Deneme: caveman-convert

video ? · 15 · bu dalgada koşulmaz (14b)

## Hipotez
yüklenen skill gövdesi görsel sayfayla ≥%40 daha az girdi token harcar, skill kuralına uyum düşmez (skill listesi metni değişmez).

## Metrik
skill yüklemesinde girdi token (provider-reported) ve kural uyumu (görev başarısı + Jev kalite, 18 kapısı).

## Bütçe
1 skill (video-uygula) × 18 kalite kapısı görev seti ≤18 claude -p, Jev ≤30, `--dry-run` önce.

## Geri alma
`caveman convert --revert`; skill dosyaları değişmezse geri alma yok.

## Başarı eşiği
girdi token −%40 ve 18 kapısı (başarı B ≥ A, kalite gürültü bandında).

