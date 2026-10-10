# YUKLE-12 · bu gece CC'ye kurulan skill'ler claude.ai için (YUKLE-12b: jeton optimize)

Üretim: `.kos/kopru/y12.py` → `tools/yukle12b.py` (açıklama sıkıştırma + çift ayırma + yeniden numaralama) · `dist/yukle-12/parti-N` (20'şer zip, dist gitignore'da) · YÜKLEME YAPILMADI.

## Sayılar

- Önceki: 898 zip (45 parti). 12b sonrası: **894 zip · 45 parti** (44×20 + 14) · çift ayrılan 4 (`dist/yukle-12/_cift`, silinmedi) · lisanssız 8 (`_lisanssiz`) · kırmızı 68 (`dist/yukle-12-kirmizi`, yüklenmez).
- Açıklamalar: ≤110 karakter, tetikleyici başta; orijinal açıklama SKILL.md gövdesinin başında `Tam açıklama:` satırı (gövdeye başka dokunuş yok).

## Çift ayrılanlar (`_cift`)

| Ayrılan | Tutulan | Gerekçe |
|---|---|---|
| octo/skill-tdd | mattpocock-skills/tdd | aynı işlev; tdd tetikleyicisi net, 3659 B gövde |
| octo/skill-council | ecc/council | aynı işlev (çok-model konsey); ecc sürümü bağımsız, octo orkestrasyona bağlı |
| azure/deploy | azure/azure-deploy | `deploy` yalnız `azure-app-onboard` orkestratöründen çağrılır, kullanıcıya yönlendirilemez |
| azure/prepare | azure/azure-prepare | aynı gerekçe (prepare = orkestratör fazı 2) |

Tespit: ad çakışması + açıklama benzerliği (Jaccard) + anahtar sözcük taraması (tdd/review/frontend/security/debug...); bu partide birebir code-review/frontend-design çifti çıkmadı.

## Parti sırası (UI/video/3D → geliştirme → diğerleri)

| Kategori | Skill | Parti | Jeton |
|---|---|---|---|
| UI-tasarim | 152 | 1–8 | ~5061 |
| web-animasyon-3D-video | 33 | 8–10 | ~1145 |
| gelistirme-is-akisi | 325 | 10–26 | ~11452 |
| erisilebilirlik-kapsayici | 49 | 26–28 | ~1630 |
| arac-paketleri(daymade) | 59 | 28–31 | ~1960 |
| yapay-zeka-degerlendirme | 21 | 31–32 | ~612 |
| yonetim-surec | 57 | 32–35 | ~1336 |
| pazarlama-reklam | 93 | 35–40 | ~3172 |
| octo | 54 | 40–43 | ~1698 |
| azure-bulut | 51 | 43–45 | ~1703 |

## Jeton tahmini (ad+açıklama+25/skill etiket, ~4 karakter/jeton)

- **Önce: ~47029 jeton/sohbet** (898 skill, 165668 karakter). **Sonra: ~29771** (894 skill, 96734 karakter ad+açıklama) → **−%37**.
- Taban 367 skill ≈ ~19220 jeton; ek yük +%245 → ≈ +%155.
- Etiket payı (25/skill ≈ 5.6k jeton) sıkıştırılamaz; daha fazla düşüş yalnız skill sayısını azaltmakla olur. Öneri sırası aynı: parti 1–10 (~6.2k jeton), sonra 11–26.

## Lisanssız

- context-mode: context-mode, ctx-doctor, ctx-index, ctx-insight, ctx-purge, ctx-search, ctx-stats, ctx-upgrade (Elastic License 2.0: yeniden dağıtım kısıtlı).

## Kırmızı (yüklenmez)

68 zip: eksik yol referansı / ~/.claude / ayrılmış sözcük; ayrıntı `dist/yukle-12-eski/_satirlar.tsv` not sütunu.
