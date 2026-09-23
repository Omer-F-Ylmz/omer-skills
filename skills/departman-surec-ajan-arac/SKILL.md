---
name: departman-surec-ajan-arac
description: "Ajan araçları müdürü: skill, plugin, hook, MCP ve Claude API geliştirme sırası. Skill/plugin/hook/MCP yazarken oku."
---

# Departman: surec-ajan-arac — iş sırası

Katalog: `docs/departmanlar/surec-ajan-arac.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.

## Adımlar
1. **Tür seçimi** — skill mi, hook mu, MCP mi: `plugin-structure`; otomatik davranış hook ister (`hook-development`, kural için `hookify`).
2. **Skill** — `skill-creator` ile taslak + eval; yazım disiplini `writing-skills`; plugin içinde `skill-development`.
3. **MCP** — sunucu `mcp-builder`, plugin'e bağlama `mcp-integration`.
4. **Claude API / ajan** — `claude-api` (model, önbellek, araç kullanımı); SDK uygulaması `agent-sdk-dev`; tipli yargı `jev`.
5. **Doğrulama** — plugin `plugin-dev` doğrulayıcısı; sonra `departman-surec-inceleme`.

## Kapılar
- Dış repo kodu/kuralı almadan önce lisans; MIT/Apache değilse koşul rapora.
- Skill description ≤200 karakter; gövde kısa, ayrıntı referans dosyada.
