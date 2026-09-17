# Kapanış araçları · 2026-09-17 (KURULUM-4)
Kapanış kontrol listesi (11 Eyl): 1 fonksiyon testleri · 2 güvenlik/sızma · 3 bağımlılık · 4 OWASP ZAP · 5 KVKK · 6 SEO, A11y & kapanış. Burada yalnız 2 · 3 · 6. Hepsi CLI; hook/MCP yok.
Sürümler: semgrep 1.177.0 (uv tool) · gitleaks 8.30.1 (winget) · jq 1.8.2 (winget) · @axe-core/puppeteer 4.13.0 (frontend-craft 1.5.2 node_modules; global @axe-core/cli kaldırıldı).
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
## 6 · A11y — axe (puppeteer), 3 genişlik
- `node tools/axe-scan.js <url>` (omer-skills) → 390/768/1440; frontend-craft'ın puppeteer Chromium'u, chromedriver yok.
- Kısıt: yalnız `id · impact · node sayısı · ilk selector` satırları; exit 1 = ihlal var. Uzunsa `| sort | uniq -c`.
- Ön koşul: frontend-craft Adım 0 (`npm ci --ignore-scripts` + browsers install chrome).
## Duman testi (omer-skills, 17 Eyl)
- gitleaks `--no-git --redact`: ~2.27 MB, "no leaks found", exit 0.
- semgrep p/default: 84 dosya, 0 bulgu, 0 hata. jq komutları (semgrep · gitleaks) koşuldu, exit 0.
- axe-scan garajim.runasp.net: her genişlikte 3 ihlal (aria-required-children critical · landmark-one-main · region), exit 1.
