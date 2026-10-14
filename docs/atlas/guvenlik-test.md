# Oyun kitabı — güvenlik + test (site kapanış listesi, ATLAS-2)

Karar kaynağı: `docs/atlas/kart.jsonl` (`karar` · `kosul`); aynı karar `docs/katalog/yetenek.jsonl` satırında. TELVE-R2f kapanış adımları bu listeyle sınanır.

## A. Site kapanış listesi (VARSAYILAN, bu sırayla)
| Adım | Araç | Komut | Kapı |
|---|---|---|---|
| A1 Sır taraması | `gitleaks` · `sec-gitleaks-gecmis` | `gitleaks detect --source . --redact` (geçmiş dahil) | Bulgu 0; varsa döndür + geçmişten temizle |
| A2 Statik analiz | `semgrep` · `sec-semgrep-kural` | `semgrep --config auto --error --quiet` | Yüksek 0; yanlış pozitif satır içi gerekçeyle |
| A3 Bağımlılık | `npm audit` (osv-scanner kurulu değil) | `npm audit --omit=dev --audit-level=high` · kullanılmayan: `npx knip` | Yüksek+kritik 0 |
| A4 Başlıklar | `sec-guvenlik-baslik` | Önizleme yanıtında CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy | Eksik başlık yok; CSP'de `unsafe-inline` gerekçesiz yok |
| A5 Performans | `lighthouse-chrome-devtools` | `npx lighthouse <url> --preset=desktop --output=json --chrome-flags=--headless` (+ mobil) | Perf/A11y/BP/SEO eşikleri tarifte |
| A6 Erişilebilirlik | `qa-erisilebilirlik-testi` | Playwright + axe-core (`@axe-core/playwright`) 390/1440 | serious+critical 0; klavye gezinti + `prefers-reduced-motion` |
| A7 Uçtan uca | `qa-e2e-playwright` · `playwright-cli` | headless; konsol hata 0, kırık bağlantı 0 | Varsayılan tarayıcı açılmaz |

## B. GEREKİNCE (koşul)
- `strix` / `*-with-strix` — ZAP kurulu değilken **yerel önizlemeye** dinamik tarama; canlı/üçüncü taraf hedef yok.
- `cso` — sürüm öncesi tek seferlik güvenlik görüşü; A1–A4'ten sonra, yerine değil.
- `sec-pentest-plani` · pentest skill'leri — yalnız sahipli/izinli hedefte, yazılı kapsamla; site kapanışında değil.
- `ecc:security-review` · `phoenix-security-review:*` — auth/ödeme/kullanıcı verisi olan kod değişikliğinde.
- `chrome-devtools-mcp:a11y-debugging` · `ecc:frontend-a11y` — A6 bulgusu düzeltilemiyorsa teşhis.
- `*-desktop` kopyaları — claude.ai/Desktop'ta; CC'de asıl CLI.
- `*-paket` (mukul975, erisilebilirlik vb.) — asıl araç yetmezse tarif kaynağı.

## KULLANMA
- `claude-ads:audit-*` — reklam hesap denetimi; güvenlik/test değil (ad eşleşmesiyle kümeye girdi).
- Ağ tarayıcıları (nmap/nuclei vb.) site kapanışında — izinli hedef ve kapsam yoksa hiç.

## İş sırası
A1 → A2 → A3 (kod; ucuz, ağsız) → derleme → A4 → A5 → A6 → A7 (önizleme sunucusu) → gerekirse B → tek kapanış tablosu (araç · sürüm · bulgu sayısı · karar).

## Token ipucu
- Tarama çıktısı ana bağlama girmez: `--quiet`/JSON + yalnız sayı ve ilk 5 bulgu.
- Lighthouse JSON'dan yalnız 4 skor + başarısız denetim adları çekilir.
- Aynı sürümde tekrar taramada önceki rapor bayatsa yeniden koş, değilse sayıyı taşı.
- Bulgu düzeltmesi: önce kırmızı test/yeniden tarama, sonra düzeltme (DEVAM-KURALI).
