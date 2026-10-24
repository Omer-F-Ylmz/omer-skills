---
name: xerj-kullanim
description: XERJ yerel arama motoru + MCP (Apache-2.0, tek Rust binary) kullanım rehberi. Kod/doküman/log aramada grep ya da tam dosya okuma yerine önce xerj araçlarını (xerj_search, xerj_code_search, xerj_map) kullan; dosyayı yalnız kanıt satırı için aç.
---

# XERJ kullanımı

Kural: kod/doküman aramada önce xerj, yoksa `graphify query`; dosyayı yalnız kanıt satırı için aç.

- Düğüm: `127.0.0.1:9200` (`--insecure`, yalnız loopback). Kapalıysa MCP araçları "request failed" döner; başlat: `python .kos/kopru/arka.py --bagimsiz araclar/xerj/arka.log araclar/xerj/baslat.py`.
- MCP: `xerj.exe mcp` (stdio), env `XERJ_URL=http://127.0.0.1:9200`, **`XERJ_DISABLE_FEEDBACK=true` şart** (yoksa otomatik field-report/GitHub PR gönderir).
- İndeks önekleri: `os-skills`, `os-tools`, `os-docs`, `os-rapor`, `os-mcp`, `os-templates`, `os-tests`, `claude-ile-yapilanlar`. Tam kök (`C:/Projeler/omer-skills`) Windows'ta `os error 33` (kilitli dosya) ile abort eder; alt klasör alt klasör indeksle.
- İndeksleme sırasında düğüm RAM'i ~5 GB'a çıkar ve sorgular zaman aşımına düşer; indeks bitince sorgula.
- Sorgu: `xerj_search` içinde `index` joker karakter kullanma; gerçek indeks adı ver (`_cat/indices?format=json`).
- Hatırlatma: claude.ai sandbox'ında yerel düğüm yoktur; bu skill yalnız yerel CC/Desktop içindir.
