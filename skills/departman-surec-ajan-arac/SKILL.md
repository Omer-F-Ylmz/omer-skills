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

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- `claude-api:claude-api` · |- · `C:/Users/pc/.claude/plugins/cache/anthropic-agent-skills/claude-api/8a1541c4a3ff/skills/claude-api/SKILL.md`
- `plugin-dev:agent-development` · This skill should be used when the user asks to "create an agent", "add an agent", "write a subagent", "agent  · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/agent-development/SKILL.md`
- `plugin-dev:command-development` · This skill should be used when the user asks to "create a slash command", "add a command", "write a custom com · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/command-development/SKILL.md`
- `plugin-dev:hook-development` · This skill should be used when the user asks to "create a hook", "add a PreToolUse/PostToolUse/Stop hook", "va · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/hook-development/SKILL.md`
- `plugin-dev:mcp-integration` · This skill should be used when the user asks to "add MCP server", "integrate MCP", "configure MCP in plugin",  · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/mcp-integration/SKILL.md`
- `plugin-dev:plugin-settings` · This skill should be used when the user asks about "plugin settings", "store plugin configuration", "user-conf · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/plugin-settings/SKILL.md`
- `plugin-dev:plugin-structure` · This skill should be used when the user asks to "create a plugin", "scaffold a plugin", "understand plugin str · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/plugin-structure/SKILL.md`
- `plugin-dev:skill-development` · This skill should be used when the user wants to "create a skill", "add a skill to plugin", "write a new skill · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/skill-development/SKILL.md`
- `typesafe:typesafe-ai` · > · `C:/Users/pc/.claude/plugins/cache/typesafe-ai/typesafe/0.5.7/skills/typesafe-ai/SKILL.md`
<!-- profil-disi:son -->
