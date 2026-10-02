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

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- `phoenix-cti-search:cti-domain-research` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-cti-search/1.0.0/skills/cti-domain-research/SKILL.md`
- `phoenix-sast-rules:opengrep-rule-generator` · Use when the user wants to create opengrep/semgrep SAST rules, detect vulnerabilities in code, generate securi · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-sast-rules/1.0.0/skills/opengrep-rule-generator/SKILL.md`
- `phoenix-sast-rules:opengrep-rule-generator-research` · Use when the user wants to research vulnerabilities and create opengrep/semgrep SAST rules, conduct security r · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-sast-rules/1.0.0/skills/opengrep-rule-generator-research/SKILL.md`
- `phoenix-security-review:0day-scanner` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-security-review/1.0.0/skills/0day-scanner/SKILL.md`
- `phoenix-security-review:security-assessment` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-security-review/1.0.0/skills/security-assessment/SKILL.md`
- `phoenix-security-review:security-reviewer` · Multi-language security review for web apps, APIs, and CLIs · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-security-review/1.0.0/skills/security-reviewer/SKILL.md`
- `phoenix-security-review:threat-modeling` · > · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-security-review/1.0.0/skills/threat-modeling/SKILL.md`
- `phoenix-security-review:tm-quick-security-assessment` · The QUICK tier · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-security-review/1.0.0/skills/tm-quick-security-assessment/SKILL.md`
- `phoenix-security-review:tm-security-review` · The COMPREHENSIVE tier · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-security-review/1.0.0/skills/tm-security-review/SKILL.md`
- `pia-generation` · > · `C:/Users/pc/.claude/skills/pia-generation/SKILL.md`
- `policy-monitor` · > · `C:/Users/pc/.claude/skills/policy-monitor/SKILL.md`
<!-- profil-disi:son -->
