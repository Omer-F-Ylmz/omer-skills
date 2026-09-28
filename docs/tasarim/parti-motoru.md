# `video parti` motoru — tasarım notu (MOTOR-M1 K5)

Amaç: parti maliyetinin büyüğü olan ana Opus oturumunu (docs/olcumler/parti-maliyet.md: ana/alt 13,7×, 8,8M jeton/video) döngüden çıkarmak. Deterministik adımlar kodda koşar, model adımları hafif `claude -p` çağrısıdır, Opus yalnız sonucu inceler.

## K3 ölçümü: aynı görev, farklı yollar (29 Eyl)
Görev: tek paket.md'den (jf1sv2geEWo, 6,3k karakter) aday çıkarma, aynı system prompt ve JSON şema. Hafif yollarda `ANTHROPIC_BASE_URL` (headroom vekili) alt süreçte kaldırıldı; c yolu CC oturumunun kendi yolundan geçti. Toplam 5 model çağrısı.

| Yol | Model | Çalıştı | girdi · önb.okuma · önb.yazma · çıktı | Toplam | Süre | $ (CLI tahmini) | Form | Aday |
|---|---|---|---|---|---|---|---|---|
| a-bare `claude -p --bare` | — | hayır: "Not logged in · Please run /login" (`--bare` OAuth okumaz, API anahtarı yok) | 0 | 0 | 1,5 s | 0 | — | — |
| a0 ağır `claude -p --model sonnet` (tüm ayarlar) | claude-sonnet-5-5 | evet, 4 tur | 8 · 174.391 · 90.791 · 2.602 | 267.792 | 34,4 s | 0,424 | ✓ | 2 |
| **a1 hafif `claude -p`** | claude-sonnet-5-5 | evet, 2 tur | 2 · 0 · 3.648 · 1.315 | **4.965** | **11,6 s** | 0,028 | ✓ | 6 |
| a2 hafif `claude -p` | claude-sonnet-5 | evet, 2 tur | 2 · 0 · 3.791 · 2.468 | 6.261 | 27,3 s | 0,040 | ✓ | 3 |
| b1 Agent SDK 0.2.161 (Python) | claude-sonnet-5-5 | evet, 2 tur | 2 · 680 · 4.187 · 1.057 | 5.926 | 10,0 s | 0,030 | ✓ | 4 |
| c Agent alt ajanı (video-tarayici) | claude-sonnet-5-5 (FORCE) | evet, 3 istek | 13.789 · 23.446 · 11.787 · 1.088 | 50.110 | 16,7 s | — | ✓ (el ile) | 4 |

Hafif bayraklar (hepsi `claude --help`'te var): `--model claude-sonnet-5-5 --output-format json --json-schema <şema> --system-prompt <kısa> --tools "" --setting-sources "" --strict-mcp-config --safe-mode --disable-slash-commands --no-session-persistence --max-budget-usd 0.5`.

- Kimlik: `ANTHROPIC_API_KEY` ve `CLAUDE_CODE_OAUTH_TOKEN` tanımsız, `--bare` "Not logged in" döndü. a1/b1'in çalışması claude.ai (Max) oturumuyla çalıştıklarını gösteriyor.
- Sonnet 5.5 ↔ 5 (a1/a2): çıktı −%47, süre −%58, $ −%30, girdi −%4. Aday 6'ya 3; tek örnek, kalite ölçülmedi.
- Hafif yol ağır yolun 1/54'ü, alt ajanın 1/10'u kadar jeton harcıyor. Ağır `-p` bile 265k girdi yüklüyor (skill/araç/hook bloğu).
- SDK init'i `setting_sources=[]` ile de skill/plugin listesi taşıdı (sıkıştırılmış çıktıda 18/2 okundu, kesin değil). Toplam girdi yine ~4,9k.

**Seçilen yol: (a) hafif `claude -p` + `--json-schema`, model `claude-sonnet-5-5` (tam kimlik).** Gerekçe: Max ile çalışıyor, çağrı başı ~5k jeton / ~12 sn, ek bağımlılık yok. SDK aynı sonucu veriyor ama uv paketi ve gömülü CLI indiriyor, kazancı yok. SDK yalnız çok turlu araç döngüsü gerekirse yedek. Alt süreçte `ANTHROPIC_BASE_URL` kaldırılır.

## Aşamalar
| # | Aşama | Tür |
|---|---|---|
| 1 | kuyruk okuma, parti seçimi (kuyruk.md durum sütunu) | deterministik |
| 2 | indir · paket · kare · whisper (mevcut `video paket/kare/whisper`) | deterministik |
| 3 | tam tarama → tarayıcı formu (video başına 1 çağrı; short'lar toplu) | model (a1) |
| 4 | form doğrulama (red → en fazla 2 yeniden istek) + rapor md üretimi | deterministik |
| 5 | aday birleştirme: ad normalizasyonu (24e-1 ASCII slug) + repo_url eşleşmesi | deterministik |
| 6 | araç başına tek derin araştırma → araştırıcı formu (web araçlarıyla; araçlı hafif çağrı M2'de ölçülecek) | model |
| 7 | video başına destek: tarayıcı formundaki kanıt/iddia → aday destek[] | deterministik |
| 8 | önceki araştırmada olmayan video özgü özellik → ek araştırma çağrısı | model |
| 9 | karar paneli (panel.md) → `video karar` | Ömer kararı |
| 10 | maliyet defteri özeti → docs/olcumler | deterministik |

Aday merkezli akış: önce kuyruğun tamamı taranır (3-4). Adaylar tüm videolar üzerinden birleştirilir (5). Her araç **bir kez** ve daha derin araştırılır (6). Her video kendi bulgusunu araca "destek" olarak ekler (7). Önceki araştırmada olmayan özellik ayrıca araştırılır (8).

## Short toplu tarama
Short'lar (paket künyesindeki süre ≤ 60 sn; bu dalgada paket.md'den short ayırt edilemedi, M2'de künyeye `short` alanı eklenmeli) N'li gruplar halinde tek çağrıda taranır. Form `videolar: [tarayıcı formu]` dizisi olur. Tavan: çağrı başı girdi ≤ 40k jeton (K3: 6,3k karakterlik paket ≈ 3,6k jeton → ~8 short/çağrı).

## Durum dosyası: `.kos/<parti-id>/durum.json`
```
{"parti": "...", "guncelleme": "ISO", "videolar": {"<id>": {"<adim>": {"durum": "bekliyor|tamam|hata|form_red",
  "deneme": 0, "cikti": "yol", "usage": {...}}}}, "adaylar": {"<slug>": {"arastirma": "...", "destek": [...]}}}
```
- Her adım bitince atomik yazılır (tmp + `os.replace`).
- Yeniden başlatma: `video parti devam <parti-id>` `tamam` olanları atlar, `hata`/`bekliyor` olanları `deneme < 3` ise yeniden koşar. Model çağrısı dışında hiçbir adım bağlama bağlı değil, yeni CC oturumu gerekmez.

## Karar paneli: `docs/kurulumlar/parti/<parti-id>/panel.md`
Koddan üretilir: aday başına tek satır (ad · tür · destek video sayısı · lisans · önerilen karar · gerekçe) ve boş "Ömer" sütunu. `form_red` ve belirsiz birleştirmeler ayrı bölümde durur. Opus 5.5 yalnız bu paneli ve raporları inceler.

## Maliyet defteri: `.kos/<parti-id>/defter.jsonl`
Her model çağrısı için bir satır: adım · video/aday · model · girdi/önb.okuma/önb.yazma/çıktı · süre · CLI `total_cost_usd` · form sonucu. Parti tavanı: çağrı sayısı ve `--max-budget-usd` toplamı parti başında sabitlenir; aşılırsa motor durur (durum `tavan`).

## M2 kabul kriterleri (taslak)
1. `video parti <kuyruk> --en-fazla N` 1-10 aşamalarını koşar. Model adımları yalnız hafif `claude -p` (a1 bayrakları) ile yapılır, alt ajan kullanılmaz.
2. Kesinti sonrası `video parti devam` tamamlanan adımları yeniden çağırmaz (testte sahte taşıyıcı çağrı sayısı).
3. Zorunlu alanı boş form reddedilir ve yeniden istenir; üçüncü redde `form_red` durumuna geçer (test).
4. Üretilen rapor md'leri mevcut `video rapor-denetle` denetiminden geçer.
5. Her araç tek derin araştırma alır; ikinci video aynı araca yalnız `destek` ekler (test).
6. Defter toplamı ile parti tavanı raporlanır; canlı bir partide video başına ana (Opus) payı K1'deki 8,8M jetonun ≤ %10'u.
