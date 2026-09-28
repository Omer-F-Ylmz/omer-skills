# codex-plugin-cc
ad: codex-plugin-cc
tur: plugin
video: LbBC5Wew4qs
etiket: yeniden:parti-c
repo: openai/codex-plugin-cc
lisans: Apache-2.0
son_commit: db52e28 2026-07-07
arsiv: doğrulanamadı (gh api çağrılmadı)
kaynak: yok
telemetri: doğrulanamadı
arastirma: yarım: araştırıcı 12 tur tavanında yalnız iskelet yazıp durdu (29.8k token · 12 çağrı); alanları ana ajan on.md (README + ağaç + Güvenlik ön taraması) ve sığ klonun LICENSE/git log'undan yazdı
## Ne
Claude Code içinden Codex'e kod incelemesi (`/codex:review`, `/codex:adversarial-review`) ve iş devri (`/codex:rescue`, `/codex:transfer`, arka plan işleri) yaptıran resmi OpenAI plugin'i; ChatGPT aboneliği ya da OpenAI API anahtarı + Node.js ≥18.18 ister.
## Kanıt
LbBC5Wew4qs (docs/video-tarama/2026-09-28-LbBC5Wew4qs.md): videoda marketplace add + install + configure adımları. on.md README: komut listesi, gereksinimler; LICENSE Apache License; klon HEAD db52e28 (2026-07-07).
## Kurulum
- plugin: marketplace add openai/codex-plugin-cc
- plugin: install codex@openai-codex
- npm: install -g @openai/codex
## İzinler
Codex CLI yerel çalışma ağacını okur (review salt-okur; rescue/transfer yazabilir); OpenAI hesabına kod gönderir, kullanım Codex limitinden düşer.
## Duman testi
- komut: codex --version
- cikis: 0
## Geri alma
- plugin: uninstall codex@openai-codex
- npm: uninstall -g @openai/codex
## Köprü izni
- yok
## Önerilen katman
RED — güvenlik: SkillSpector --no-llm HIGH/CRITICAL 4 (on.md Güvenlik ön taraması); zaten var: codex (gstack skill, OpenAI Codex CLI wrapper)
## Telemetri kapatma
- doğrulanamadı
## Özellikler
### codex-review
ne: `/codex:review` — çalışma ağacı ya da dal için salt-okur Codex kod incelemesi (`--base`, `--background`)
kurulum: plugin + Codex CLI
lisans: Apache-2.0
etiket: araç
karar: ZATEN VAR
gerekce: zaten var: codex (gstack skill; review/challenge/consult modları) · code-review skill
### codex-adversarial-review
ne: tasarım/varsayım sorgulayan, odak metni alan inceleme
kurulum: plugin + Codex CLI
lisans: Apache-2.0
etiket: araç
karar: ZATEN VAR
gerekce: zaten var: codex (gstack skill challenge modu) · agent-skills:doubt-driven-development
### codex-rescue-transfer
ne: işi ya da oturumu arka planda Codex'e devretme, durum/sonuç/iptal komutları
kurulum: plugin + Codex CLI
lisans: Apache-2.0
etiket: araç
karar: RED
gerekce: güvenlik: SkillSpector --no-llm HIGH/CRITICAL 4 (on.md); ikinci ücretli model aboneliği gerekir
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| `/codex:review`, Codex içindeki `/review` ile aynı kalitede inceleme verir | openai/codex-plugin-cc README | doğrulanamadı | yalnız üretici beyanı; ölçüm yok | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
