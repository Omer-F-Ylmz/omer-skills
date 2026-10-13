---
name: departman-surec-ajan-arac
description: "Ajan araçları müdürü: skill, plugin, hook, MCP ve Claude API geliştirme sırası. Skill/plugin/hook/MCP yazarken oku."
---

# Departman: surec-ajan-arac — iş sırası

Katalog: `docs/departmanlar/surec-ajan-arac.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

## Adımlar
1. **Tür seçimi** — skill mi, hook mu, MCP mi: `plugin-structure`; otomatik davranış hook ister (`hook-development`, kural için `hookify`).
2. **Skill** — `skill-creator` ile taslak + eval; yazım disiplini `writing-skills`; plugin içinde `skill-development`.
3. **MCP** — sunucu `mcp-builder`, plugin'e bağlama `mcp-integration`.
4. **Claude API / ajan** — `claude-api` (model, önbellek, araç kullanımı); SDK uygulaması `agent-sdk-dev`; tipli yargı `jev`.
5. **Doğrulama** — plugin `plugin-dev` doğrulayıcısı; sonra `departman-surec-inceleme`.

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

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:ajn-ajan-orkestrasyon
ajan:ajn-ajan-tanimi-yazar
ajan:ajn-claude-api-gelistirici
ajan:ajn-codex-claude-koprusu
ajan:ajn-hook-yazar
ajan:ajn-mcp-kurulum-denetci
ajan:ajn-mcp-sunucu-yazar
ajan:ajn-migrasyon-model
ajan:ajn-ogrenilen-ders
ajan:ajn-plugin-iskelet
ajan:ajn-prompt-denetci
ajan:ajn-skill-test
ajan:otm-ajan-is-akisi-kur
ajan:otm-google-sheets-akis
ajan:otm-mail-otomasyon
ajan:otm-n8n-akis-tasarimi
ajan:otm-n8n-hata-yonetimi
ajan:otm-n8n-ifade-kod
ajan:otm-otomasyon-izleme
ajan:otm-tarayici-otomasyon
### yalnız Claude Code
agent-reach: Reddit/X/YouTube/GitHub gönderi ve konu okuma
agp-9-upgrade: Upgrades, or migrates, an Android project to use
ask-matt: Ask which skill or flow fits your situation
chief-of-staff: Pursue a long-running goal in a single session
codebase-onboarding: 不慣れなコードベースを分析し、アーキテクチャマップ、主要なエントリポイント、規約、スターターCLAUDE.mdを含む構造化オンボーディングガイドを生成します。新しいプロジェクトに参加するか、リポでClaude Codeを初めてセットアップする場合に使用します。
configure-ecc: Claude Code、Codex、Kimi 内で ECC のインストール、更新、再設定を案内し、各ハーネスが実際に備えるプラグイン、スコープ、フック機能を守ります。
ecc-recipes: asked which commands run a workflow, the command
failure-recovery: What happens when an agent fails — retry
how-it-works: the user asks "how does claude-mem work?" or
ima-copilot: the user mentions IMA / 腾讯 IMA /
intent-driven-development: a user asks to clarify a feature, define
mem-setup: asks to "set up claude-mem", "pair claude-mem", "connect
model-sec: Betikte claude -p çağrısı kurulurken: modeli düşürmeden bağlamı
superpowers-using-superpowers: starting any conversation - establishes how to find
task-decomposition: Breaking complex user goals into subtasks that agents
using-superpowers: starting any conversation - establishes how to find
<!-- dizin:son -->
