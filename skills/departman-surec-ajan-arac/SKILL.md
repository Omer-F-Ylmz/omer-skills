---
name: departman-surec-ajan-arac
description: "Ajan araçları müdürü: skill, plugin, hook, MCP ve Claude API geliştirme sırası. Skill/plugin/hook/MCP yazarken oku."
---

# Departman: surec-ajan-arac — iş sırası

Katalog: `docs/departmanlar/surec-ajan-arac.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

Skill dizini: bu klasörde `dizin.md` (Claude Code: alandaki TÜM kurulu skill'ler) ve `dizin-web.md` (claude.ai: yalnız yüklü olanlar) — ad — ne zaman. Adımdaki araç işe tam uymuyorsa ortamına uyan dizinde Grep ile işin anahtar kelimesini ara (Read etme), bulunan adı Skill aracıyla çağır; listede yalnız adı görünen skill de çağrılabilir. `ajan:` kayıtları alt ajandır: Claude Code'da Agent aracıyla (subagent_type = ad), claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula.

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
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- claude-api (1): claude-api · `C:/Users/pc/.claude/plugins/cache/anthropic-agent-skills/claude-api/8a1541c4a3ff/skills/<ad>/SKILL.md`
- plugin-dev (7): agent-development, command-development, hook-development, mcp-integration, plugin-settings, plugin-structure, skill-development · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/<ad>/SKILL.md`
- typesafe (1): typesafe-ai · `C:/Users/pc/.claude/plugins/cache/typesafe-ai/typesafe/0.5.7/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->
