---
name: departman-guvenlik
description: "Güvenlik müdürü: sır taraması, SAST, pentest, KVKK sırası. Auth, form, API, bağımlılık ya da yayın öncesi güvenlik işinde oku."
---

# Departman: guvenlik — iş sırası

Katalog: `docs/departmanlar/guvenlik.md`. Frontend işinde `departman-frontend` adım 7'den çağrılır.

## Adımlar
1. **Sır taraması** — her commit öncesi `gitleaks` (temiz değilse commit yok). Env değerleri asla yazdırılmaz.
2. **Diff taraması** — değişen kod: `security-review` ya da `0day-scanner`; kural gerekiyorsa `semgrep`.
3. **Tasarım riski** — auth/RBAC, dış istek, yeni uç nokta: `threat-modeling` (STRIDE); ajan/MCP kodunda `tm-security-review`.
4. **Uygulama testi** — çalışan uygulama: `strix` (`web-app-penetration-testing`, API için `api-security-testing`); OWASP kapsamı `owasp-top-10-testing`; bulgu düzeltme `fix-security-vulnerabilities-with-strix`.
5. **Bağımlılık** — lisans (MIT/Apache dışı → koşul rapora) ve açık denetimi; `security-and-hardening`.
6. **KVKK** — yeni veri işleme: `use-case-triage` → gerekirse `pia-generation`; metin uyumu `policy-monitor`.

## Kapılar
- gitleaks temiz olmadan push yok.
- Yıkıcı komutlarda `careful`; kapsam dışı hedef taranmaz (yalnız yetkili hedef).
- Tam denetim (`security-assessment`, `cso`) yalnız yayın öncesi ya da istendiğinde; her değişiklikte diff taraması yeter.

## Çakışma
- Diff düzeyi: `security-review` > `0day-scanner` > `tm-quick-security-assessment`.
- Pentest: yerel `strix` > yönetilen `managed-pentesting-with-strix` (ücretli; tavan sayıyla).
