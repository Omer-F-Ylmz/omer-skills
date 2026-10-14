# find — 4 benzersiz kayıt

**Amaç:** Bulma odaklı skill'ler: animasyon fırsatı, daldaki hatalar, güncel dokümantasyon ve Strix ile kaynak kodda güvenlik açığı.

**İç yapı:** Tümü [skill], find-<hedef>; birbirinden bağımsız dört tarama.

## En güçlü parçalar
- `find-bugs` — Mevcut daldaki değişiklikleri hata ve güvenlik açısından inceler.
- `find-docs` — Her geliştirici teknolojisi için güncel doküman, API referansı, örnek.
- `find-security-vulnerabilities-in-code` — Strix ile kaynak kodu okuyan beyaz kutu güvenlik incelemesi.

## Birlikte kullanım
- find-bugs + find-security-vulnerabilities-in-code: genel ve derin güvenlik.
- find-animation-opportunities → yerel-diger'deki animate.

## Tuzaklar
- find-animation-opportunities mevcut animasyonu düzeltmek için değil.
- Strix tabanlı tarama yerel-diger'deki Strix skill'leriyle çakışır.

## Üyeler
- skill (4): find-animation-opportunities, find-bugs, find-docs, find-security-vulnerabilities-in-code
