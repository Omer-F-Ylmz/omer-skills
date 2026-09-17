# Kapanış araçları · 2026-09-17 (KURULUM-4)
Kapanış kontrol listesi (11 Eyl): 1 fonksiyon testleri · 2 güvenlik/sızma · 3 bağımlılık · 4 OWASP ZAP · 5 KVKK · 6 SEO, A11y & kapanış. Burada yalnız 2 · 3 · 6. Hepsi CLI; hook/MCP yok.
Sürümler: semgrep 1.177.0 (uv tool) · gitleaks 8.30.1 (winget) · @axe-core/cli 4.13.0 (npm -g).
## 2 · Güvenlik — semgrep
- `semgrep scan --config p/default --metrics=off --quiet --json | jq -r '.results[] | "\(.path):\(.start.line) \(.check_id)"'`
- Kısıt: yalnız bulgu satırı (dosya:satır kural). Sayı: `| jq '.results | length'`.
- `--config auto` metrics kapalıyken çalışmaz ("Cannot create auto config when metrics are off") → `p/default`.
- Windows: `PYTHONUTF8=1` (PowerShell: `$env:PYTHONUTF8='1'`).
## 3 · Bağımlılık — dotnet + gitleaks
- `rtk dotnet list package --vulnerable --include-transitive | grep -E '^\s+>'`
- Kısıt: yalnız `>` paket satırları; boş çıktı = açık yok.
- `gitleaks detect --no-git --redact --no-banner --source . --report-format json --report-path - | jq -r '.[] | "\(.File):\(.StartLine) \(.RuleID)"'`
- Kısıt: yalnız dosya:satır kural, secret redakte. Exit 1 = sızıntı var → DUR.
## 6 · A11y — axe CLI, 3 genişlik
- `for w in 390 768 1440; do echo "== $w"; axe <url> --chrome-options="window-size=$w,900" --exit 2>&1 | tail -n 15; done`
- Kısıt: genişlik başına son 15 satır (ihlal özeti); `--exit` ihlalde exit 1.
- Ön koşul: chromedriver. npm allow-scripts `chromedriver@153.0.1` kurulum betiğini engelledi, axe bu haliyle çalışmıyor (exit 2) → `npx browser-driver-manager install chrome` veya `--chromedriver-path <yol>`; ilk UI kapanışında kurulur.
## Duman testi (omer-skills, 17 Eyl)
- gitleaks `--no-git --redact`: ~2.27 MB, "no leaks found", exit 0.
- semgrep p/default: 84 dosya, 0 bulgu, 0 hata.
