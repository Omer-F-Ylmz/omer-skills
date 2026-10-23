---
name: departman-surec-ajan-arac
description: "Ajan araçları müdürü: skill, plugin, hook, MCP ve Claude API geliştirme sırası. Skill/plugin/hook/MCP yazarken oku."
---

# Departman: surec-ajan-arac — iş sırası

Katalog: `docs/departmanlar/surec-ajan-arac.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

## Adımlar
1. **Tür seçimi** — skill mi, hook mu, MCP mi: `plugin-structure`; otomatik davranış hook ister (`hook-development`, kural için `hookify`).
2. **Skill** — `skill-creator` ile taslak + eval; yazım disiplini `writing-skills`; plugin içinde `skill-development`.
3. **MCP** — sunucu `mcp-builder`, plugin'e bağlama `mcp-integration`.
4. **Claude API / ajan** — `claude-api` (model, önbellek, araç kullanımı); SDK uygulaması `agent-sdk-dev`; tipli yargı `jev`.
5. **Doğrulama** — plugin `plugin-dev` doğrulayıcısı; sonra `departman-surec-inceleme`.

6. **Ajan topluluğu / çoklu ajan** — çok adımlı akış `subagent-driven-development` (implementer'lar paralel değil), bağımsız ≥3 iş `dispatching-parallel-agents`; denetim ayrı kör alt ajan (tohum başı 2 hakem, kartı yazmayan). Ücretsiz alt adım OmniRoute :free (2 FARKLI aile; 429/404'te model değiştirme yok, tek yeniden deneme); Claude aboneliği OmniRoute'tan geçmez. Reddedilen Agent çağrısı istem değişmeden bir kez yeniden denenir. Model merdiveni: betik/ücretsiz → Haiku → Sonnet → Opus (yalnız ayrışma kararı). Ayrıntı: `docs/ogren/ajan-orkestrasyon.md` (yalnız CC).

## Kapılar
- Dış repo kodu/kuralı almadan önce lisans; MIT/Apache değilse koşul rapora.
- Skill description ≤200 karakter; gövde kısa, ayrıntı referans dosyada.
- Skill description 3. tekil kişiyle: ne yapar + ne zaman kullanılır; SKILL.md gövdesi ≤500 satır, fazlası references/ dosyasına (IG-40 DeXd4jID1y9).

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- claude-api (1): claude-api · `C:/Users/pc/.claude/plugins/cache/anthropic-agent-skills/claude-api/8a1541c4a3ff/skills/<ad>/SKILL.md`
- plugin-dev (7): agent-development, command-development, hook-development, mcp-integration, plugin-settings, plugin-structure, skill-development · `C:/Users/pc/.claude/plugins/cache/claude-plugins-official/plugin-dev/ab024cdcfa7c/skills/<ad>/SKILL.md`
- typesafe (1): typesafe-ai · `C:/Users/pc/.claude/plugins/cache/typesafe-ai/typesafe/0.5.7/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->


Slash katalog (iş türü → /komut·skill): `yetenek-getir/reference/slash-katalog.md` — Read; oturuma yüklenmez.

Kombo adayları (A/B ölçümü geçmedi; önerme, yalnız ipucu): ao-kademe-yonlendirme, ao-ucretsiz-havuz-hakem, ao-uzun-dalga, ao-kopru-yonetimi.

<!-- dizin:bas -->
## Dizin: adımdaki araç işe uymuyorsa `references/dizin.md` dosyasını oku, listeden adla çağır.
<!-- dizin:son -->
Yeni aileler (SKILL-YUKLE-1, 97): `references/yukle-1-aileler.md` — Read.
