# security — 6 benzersiz kayıt

**Amaç:** Güvenlik inceleme ve denetim skill'leri ile AppSec ve sır/kimlik bilgisi yaşam döngüsü ajanları.

**İç yapı:** Ad kalıbı security-<konu>; 4 [skill] (and-hardening, assessment, audit, review) + 2 [ajan] (appsec-engineer, secrets-credential-engineer).

## En güçlü parçalar
- `security-review` — Güvenlik incelemesi, zafiyet bulma ve OWASP incelemesi istendiğinde.
- `security-audit` — Güvenlik soruları, odaklı inceleme, zafiyet araştırması, denetim ve pentest için tam iş akışı.
- `security-and-hardening` — Girdi işleyici, kimlik doğrulama, veri saklama denetimi ve sertleştirme.
- `security-secrets-credential-engineer` — Sırların tespit, önleme, kasa, rotasyon ve sızıntı yanıtı yaşam döngüsü.
- `security-appsec-engineer` — Tehdit modelleme, güvenli kod incelemesi ve SAST/DAST ile SDLC güvenliği.

## Birlikte kullanım
- security-review + security-secrets-credential-engineer: kod incelemesi ve sır taraması.
- security-appsec-engineer + security-and-hardening: tehdit modelinden sertleştirmeye.
- addy-agent-skills (agent-skills:security-and-hardening) ile aynı kapsam; biri seçilmeli.

## Tuzaklar
- security-assessment açıklaması kesik ('Use whenever someone asks...'); kapsamı girdide belirtilmemiş.
- security-and-hardening, agent-skills:security-and-hardening ile aynı açıklamaya sahip çift kopya; security-audit ve security-review de örtüşür.

## Üyeler
- skill (4): security-and-hardening, security-assessment, security-audit, security-review
- ajan (2): security-appsec-engineer, security-secrets-credential-engineer
