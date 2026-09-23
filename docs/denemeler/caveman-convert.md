# Deneme: caveman-convert

video ? · 15 · 20a: düzenek hazır, koşulmaz (caveman kurulumu ONAY bekler)

## Hipotez
yüklenen skill gövdesi görsel sayfayla ≥%40 daha az girdi token harcar, skill kuralına uyum düşmez (skill listesi metni değişmez).

## Metrik
girdi token · sıcak koşu $ (karar) · soğuk $ (bilgi) · görev başarısı + Jev kalite (18 kapısı).

## Bütçe
Önce `caveman convert --dry-run skills/video-uygula` (çıktı rapora; dosya değişmez). Sonra dönüştürülmüş gövde docs/denemeler/.kos/caveman-convert/SKILL.md'ye (repo skill'ine değil) yazılır ve `video dene caveman-convert --tavan 12 --istek-tavan 16`: 3 görev × 2 kol × 2 koşu = 12 claude -p, Jev ≤16.

## Geri alma
`caveman convert --revert`; skill dosyaları değişmezse geri alma yok.

## Başarı eşiği
girdi token −%40 ve kalite kapısı (18).

## Görevler
- 1-ozet
- 3-kapanis
- 6-talimat-izleme

## Kollar
- metin: temel · sistem skills/video-uygula/SKILL.md
- gorsel: sistem docs/denemeler/.kos/caveman-convert/SKILL.md

## Varsayım
Dönüştürülmüş gövdenin sistem istemine metin olarak verilebildiği varsayılır; convert yalnız görsel (görüntü) çıktı üretiyorsa `sistem` kolu kullanılamaz ve deneme yeniden tasarlanır (DUR).
