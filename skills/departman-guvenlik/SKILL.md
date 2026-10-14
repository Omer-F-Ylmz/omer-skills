---
name: departman-guvenlik
description: "Güvenlik müdürü: sır taraması, SAST, pentest, KVKK sırası. Auth, form, API, bağımlılık ya da yayın öncesi güvenlik işinde oku."
---

# Departman: guvenlik — iş sırası

Katalog: `docs/departmanlar/guvenlik.md`. Frontend işinde `departman-frontend` adım 7'den çağrılır.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

## Adımlar
1. **Sır taraması** — her commit öncesi `gitleaks` (temiz değilse commit yok). Env değerleri asla yazdırılmaz.
2. **Diff taraması** — değişen kod: `security-review` ya da `0day-scanner`; kural gerekiyorsa `semgrep`.
3. **Tasarım riski** — auth/RBAC, dış istek, yeni uç nokta: `threat-modeling` (STRIDE); ajan/MCP kodunda `tm-security-review`.
4. **Uygulama testi** — çalışan uygulama: `strix` (`web-app-penetration-testing`, API için `api-security-testing`); OWASP kapsamı `owasp-top-10-testing`; bulgu düzeltme `fix-security-vulnerabilities-with-strix`.
5. **Bağımlılık** — lisans (MIT/Apache dışı → koşul rapora) ve açık denetimi; `security-and-hardening`.
6. **KVKK** — yeni veri işleme: `use-case-triage` → gerekirse `pia-generation`; metin uyumu `policy-monitor`.
- Site kapanış güvenlik taraması sırası/kapıları: `docs/atlas/guvenlik-test.md` (ATLAS kararları `docs/atlas/kart.jsonl`).

## Kapılar
- gitleaks temiz olmadan push yok.
- Yıkıcı komutlarda `careful`; kapsam dışı hedef taranmaz (yalnız yetkili hedef).
- Tam denetim (`security-assessment`, `cso`) yalnız yayın öncesi ya da istendiğinde; her değişiklikte diff taraması yeter.

## Çakışma
- Diff düzeyi: `security-review` > `0day-scanner` > `tm-quick-security-assessment`.
- Pentest: yerel `strix` > yönetilen `managed-pentesting-with-strix` (ücretli; tavan sayıyla).

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- phoenix-cti-search (1): cti-domain-research · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-cti-search/1.0.0/skills/<ad>/SKILL.md`
- phoenix-sast-rules (2): opengrep-rule-generator, opengrep-rule-generator-research · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-sast-rules/1.0.0/skills/<ad>/SKILL.md`
- phoenix-security-review (6): 0day-scanner, security-assessment, security-reviewer, threat-modeling, tm-quick-security-assessment, tm-security-review · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-security-review/1.0.0/skills/<ad>/SKILL.md`
- pia-generation (1): pia-generation · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
- policy-monitor (1): policy-monitor · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:oyn-mod-guvenlik-kontrol
ajan:sec-ai-kod-guvenlik
ajan:sec-api-guvenlik
ajan:sec-bagimlilik-acik: updating packages or before release
ajan:sec-ci-guvenlik-tarama
ajan:sec-cikis-oncesi-guvenlik
ajan:sec-docker-guvenlik
ajan:sec-guvenlik-baslik
ajan:sec-guvenlik-raporu
ajan:sec-injection-denetci
ajan:sec-jwt-oturum
ajan:sec-kvkk-gdpr-kontrol
ajan:sec-loglama-gizlilik: adding logging or error handling
ajan:sec-pentest-plani
ajan:sec-sast-kosucu
ajan:sec-sifreleme-denetci
ajan:sec-sir-tarayici: committing, publishing or after a suspected leak
ajan:sec-tehdit-modelleme: designing a feature that handles sensitive data
ajan:sec-xss-csrf-denetci
ajan:sec-yetkilendirme-matrisi: an app has multiple user roles
ajan:sec-zero-trust-ag
### yalnız Claude Code
0day-scanner: ever someone asks to scan for vulnerabilities, check
cli:ecc-agentshield: Claude Code ayar/hook/MCP güvenlik taraması
cli:strix-agent: otonom pentest ajanı (yetkili hedef)
cso: Security audit: supported static findings; qualified profiles add
doubt-driven-development: you want every assumption cross-examined before proceeding, when
one-on-one: Run effective, recurring 1:1s that build trust and
opengrep-rule-generator: özel statik analiz/SAST kuralı yaz (opengrep/semgrep)
use-case-triage: Yeni veri işleme faaliyeti, ürün özelliği, tedarikçi, AI/model
<!-- dizin:son -->
