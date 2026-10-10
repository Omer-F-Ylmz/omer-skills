# YUKLE-12 · bu gece CC'ye kurulan skill'ler claude.ai için

Üretim: `.kos/kopru/y12.py` (yukle8 işlevleri) · `dist/yukle-12/parti-N` (20'şer zip, dist gitignore'da) · YÜKLEME YAPILMADI.

## Sayılar

- Gece kurulan plugin skill'i (claude.ai'de olmayan, tekil): 974 · yüklenebilir 898 (45 parti) · lisanssız 8 (`dist/yukle-12/_lisanssiz`) · kırmızı 68 (`dist/yukle-12-kirmizi`, claude.ai kurallarına uymuyor, yüklenmez).
- Elenenler: synced/dist geçmişinde olan adlar, plugin+kopya çiftleri (tekil ad), ecc `docs/<dil>/` çeviri kopyaları zaten pakete girmedi (yalnız ecc/skills kök).

## Parti sırası (kategori önceliği: UI → video/3D → geliştirme → ...)

| Kategori | Skill | Parti | Jeton |
|---|---|---|---|
| UI-tasarim | 152 | 1–8 | ~8082 |
| web-animasyon-3D-video | 33 | 8–10 | ~1949 |
| gelistirme-is-akisi | 325 | 10–26 | ~18418 |
| erisilebilirlik-kapsayici | 49 | 26–28 | ~2709 |
| arac-paketleri(daymade) | 59 | 28–31 | ~3310 |
| yapay-zeka-degerlendirme | 21 | 31–32 | ~632 |
| yonetim-surec | 57 | 32–35 | ~1339 |
| pazarlama-reklam | 93 | 35–40 | ~5394 |
| octo | 56 | 40–43 | ~2034 |
| azure-bulut | 53 | 43–45 | ~3158 |

## Jeton tahmini

- Yüklenebilir 898 skill: ad+açıklama toplam 165668 karakter (+25/skill etiket) → ~47029 jeton, ortalama ~209 karakter/skill.
- Mevcut taban 367 skill × aynı ortalama ≈ ~19220 jeton; ek yük taban üstüne **+%245** (her sohbet).
- Öneri: hepsi (~47k jeton/sohbet) ağır; önce parti 1–10 (UI + video/3D, 200 skill, ~10903 jeton), sonra parti 11–26 geliştirme (ecc/mattpocock). Yönetim/pazarlama/octo/azure parti 31+ yalnız ihtiyaç olunca.

## Lisanssız

- context-mode/context-mode (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)
- context-mode/ctx-doctor (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)
- context-mode/ctx-index (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)
- context-mode/ctx-insight (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)
- context-mode/ctx-purge (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)
- context-mode/ctx-search (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)
- context-mode/ctx-stats (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)
- context-mode/ctx-upgrade (context-mode, Elastic License 2.0: yeniden dağıtım kısıtlı)

## Kırmızı (yüklenmez)

68 zip: eksik yol referansı / ~/.claude / ayrılmış sözcük; ayrıntı `dist/yukle-12/_satirlar.tsv` not sütunu.
