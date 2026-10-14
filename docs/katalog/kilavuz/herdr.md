# herdr — 4 benzersiz kayıt

**Amaç:** Kodlama ajanları için terminal çoklayıcı Herdr'ı kontrol etme, yayın öncesi denetim ve yalıtılmış yeniden üretim.

**İç yapı:** Tümü [skill]; ana herdr + iki iş akışı (pre-release-audit, throwaway-repro) + herdr-paket.

## En güçlü parçalar
- `herdr` — Kullanıcı Herdr'ı açıkça andığında terminal çoklayıcı kontrolü.
- `herdr-throwaway-repro` — Runtime, pane, süreç, API, kalıcılık sorunlarını yalıtılmış yeniden üretmek.
- `herdr-pre-release-audit` — Yayın öncesi docs/next ve issue ref denetimi.

## Birlikte kullanım
- herdr-throwaway-repro → herdr-pre-release-audit.

## Tuzaklar
- herdr yalnız açık Herdr talebinde kullanılmalı.
- herdr-paket ile tekil skill'ler çakışan kopya.

## Üyeler
- skill (4): herdr, herdr-paket, herdr-pre-release-audit, herdr-throwaway-repro
