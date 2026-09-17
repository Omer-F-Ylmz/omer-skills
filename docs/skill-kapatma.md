# Skill kapatma kaydı

Kapatma tarihi: 2026-09-15 · Claude Code 2.1.271 · Kapsam: kullanıcı (`~/.claude/settings.json`). Hiçbir şey silinmedi.

## Kapatılan gruplar ve geri açma

**dotnet-test** (tüm skill'ler + agent'lar) · mekanizma: `claude plugin disable -s user` · 2026-09-15
```
claude plugin enable dotnet-test@dotnet-agent-skills -s user
```

**dotnet-nuget** (tüm skill'ler) · mekanizma: `claude plugin disable -s user` · 2026-09-15
```
claude plugin enable dotnet-nuget@dotnet-agent-skills -s user
```

**plugin-dev** (tüm skill'ler + agent'lar + /create-plugin) · mekanizma: `claude plugin disable -s user` · 2026-09-15
```
claude plugin enable plugin-dev@claude-plugins-official -s user
```

**superpowers** (14 skill + `using-superpowers` SessionStart hook'u) · mekanizma: `claude plugin disable -s user` · 2026-09-15
Gerekçe: 14 skill'in 12'si eldeki transkript geçmişinde (09-05 → 09-15) 0 çağrı (brainstorming 2, test-driven-development 3). Hook `startup|clear|compact` ile her oturumda ve her /clear'da ≈880 token ekliyordu; `skillOverrides` hook'u kapatmadığı için plugin geneli kapatıldı. TDD + kök neden kuralı `~/.claude/CLAUDE.md` "Hedef-güdümlü" satırına taşındı. Kaynak: `docs/kaynak-tarama/6.md`, `99-sentez.md`.
settings.json: `enabledPlugins` altında `"superpowers@claude-plugins-official": false`; `env.SUPERPOWERS_DISABLE_TELEMETRY` geri açmada geçerli olsun diye yerinde bırakıldı.
```
claude plugin enable superpowers@claude-plugins-official -s user
```

**claude.ai / anthropic-skills** (canvas-design, docx, mcp-builder, pdf, pptx, skill-creator, theme-factory, web-artifacts-builder, xlsx) · mekanizma: `skillOverrides` → `"off"` · 2026-09-15
Geri açma önceki duruma döner (canvas-design, theme-factory, web-artifacts-builder önceden `name-only` idi; morning, import-memory önceden de `off`):
```
node -e "const f=require('os').homedir()+'/.claude/settings.json',fs=require('fs'),s=JSON.parse(fs.readFileSync(f,'utf8')),o=s.skillOverrides;['docx','pptx','xlsx','pdf','mcp-builder','anthropic-skills:skill-creator'].forEach(k=>delete o[k]);['canvas-design','theme-factory','web-artifacts-builder'].forEach(k=>o[k]='name-only');fs.writeFileSync(f,JSON.stringify(s,null,2)+'\n')"
```
Not: `skill-creator` anahtarı çıplak yazılmadı; `anthropic-skills:skill-creator` yazıldı ki `skill-creator:skill-creator` (plugin) açık kalsın.

**Built-in: dataviz, claude-api** · mekanizma: `skillOverrides` → `"off"` · 2026-09-15
```
node -e "const f=require('os').homedir()+'/.claude/settings.json',fs=require('fs'),s=JSON.parse(fs.readFileSync(f,'utf8'));['dataviz','claude-api'].forEach(k=>delete s.skillOverrides[k]);fs.writeFileSync(f,JSON.stringify(s,null,2)+'\n')"
```

**Global frontend-craft kopyası** (`~/.claude/skills/frontend-craft`, Bölüm 0–6 + Corvano'nun 09-14 düzenlemeleri) · mekanizma: klasör taşındı · 2026-09-15
```
Move-Item C:\Users\pc\.claude\skills-yedek\frontend-craft-1.1.0 C:\Users\pc\.claude\skills\frontend-craft
```
Teşhis: 09-09'daki kapatma `/plugins` menüsünden heryerde_2aa'nın `.claude/settings.local.json` dosyasına (`"frontend-craft": "off"`, local kapsam) yazılmıştı; user kapsamında hiç kapatılmadı. 8 çağrının 7'si 09-09 sonrası (Enver-abi 09-11, Corvano 09-14 ×6).

**dotnet-test-filter hook'u** (PreToolUse, matcher `Bash`, `if: Bash(dotnet test *)`) · mekanizma: `settings.json` `hooks.PreToolUse` bloğu silindi; script `~/.claude/hooks/dotnet-test-filter.ps1` yerinde · 2026-09-16
Gerekçe: RTK ile çift (`rtk hook claude`, Bash + PowerShell matcher). Geri açma komutu `settings.json.bak` (09-15) içindeki bloğu aynen geri koyar:
```
node -e "const f=require('os').homedir()+'/.claude/settings.json',fs=require('fs'),s=JSON.parse(fs.readFileSync(f,'utf8'));s.hooks.PreToolUse.push({matcher:'Bash',hooks:[{type:'command',command:'powershell.exe',args:['-NoProfile','-ExecutionPolicy','Bypass','-File','C:\\Users\\pc\\.claude\\hooks\\dotnet-test-filter.ps1'],if:'Bash(dotnet test *)',timeout:15}]});fs.writeFileSync(f,JSON.stringify(s,null,2)+'\n')"
```

**claude.ai'den senkronlanan plugin'ler: engineering, design, product-management, data** (35 skill + 1 komut + MCP sunucu tanımları) · mekanizma: `claude plugin disable <ad>@synced -s user` · 2026-09-17
Gerekçe: kullanılan MCP'ler mslearn, context7, 21st, claude-design; dördü de plugin'den gelmiyor. `claude mcp list`'te kimlik doğrulama bekleyen 19 sunucunun (15 "Needs authentication" + 4 "Incompatible auth server: does not support dynamic client registration") hepsi bu 4 plugin'den geliyordu. Sunucular plugin'den geldiği için plugin geneli kapatıldı; çoğu birden çok plugin'in `.mcp.json`'unda tanımlı.

| Sunucu | Durum | `mcp list` kaynağı | Aynı sunucuyu tanımlayan diğer plugin'ler |
|---|---|---|---|
| slack | Needs authentication | engineering | design, product-management |
| linear | Needs authentication | engineering | design, product-management |
| atlassian | Needs authentication | engineering | design, product-management, data |
| notion | Needs authentication | engineering | design, product-management |
| datadog | Needs authentication | engineering | — |
| figma | Needs authentication | design | product-management |
| intercom | Needs authentication | design | product-management |
| monday | Needs authentication | product-management | — |
| clickup | Needs authentication | product-management | — |
| amplitude | Needs authentication | product-management | data |
| amplitude-eu | Needs authentication | product-management | data |
| pendo | Needs authentication | product-management | — |
| fireflies | Needs authentication | product-management | — |
| similarweb | Needs authentication | product-management | — |
| hex | Needs authentication | data | — |
| asana | Incompatible auth server | engineering | design, product-management |
| github | Incompatible auth server | engineering | — |
| pagerduty | Incompatible auth server | engineering | — |
| bigquery | Incompatible auth server | data | — |

Aynı plugin'lerle kapanan diğer tanımlar: definite (data, "MCP endpoint not found"); google calendar, gmail (engineering, design, product-management; "Not configured"); snowflake, databricks (data; "Not configured").
settings.json: `enabledPlugins` altında `"engineering@synced": false`, `"design@synced": false`, `"product-management@synced": false`, `"data@synced": false`. Dosyalar `~/.claude/plugins/synced/` altında yerinde (`syncClaudeAiPlugins: false` hepsini `.trash`'e taşırdı; kullanılmadı).
```
claude plugin enable engineering@synced -s user
claude plugin enable design@synced -s user
claude plugin enable product-management@synced -s user
claude plugin enable data@synced -s user
```

**claude.ai bağlayıcıları (Claude Docs) + `anthropic-skills:docs`** · mekanizma: `disableClaudeAiConnectors: true` + `skillOverrides` → `"off"` · 2026-09-17
Gerekçe: kullanılan dört MCP dışında kalan son sunucu. Kapsam yalnız Claude Code'un kendi çektiği bağlayıcılar; skill senkronu ayrı anahtarda (`syncClaudeAiSkills`), dokunulmadı. Kaynak: code.claude.com/docs/en/mcp.md#disable-claude-ai-connectors. `anthropic-skills:docs` skill'i bağlayıcı olmadan çalışamayacağı için kapatıldı.
```
node -e "const f=require('os').homedir()+'/.claude/settings.json',fs=require('fs'),s=JSON.parse(fs.readFileSync(f,'utf8'));delete s.disableClaudeAiConnectors;delete s.skillOverrides['anthropic-skills:docs'];fs.writeFileSync(f,JSON.stringify(s,null,2)+'\n')"
```

**design-dna** (`zanwei/design-dna`, `~/.claude/skills/design-dna` kopyası) · mekanizma: `npx skills remove` · 2026-09-15 · etiket: DENENDİ-KALDIRILDI (15 Eyl, hex uydurma)
Gerekçe: deneme testi (aspensearch.com, 1440×900): skill'in 13 hex'inden 8'i görselde var (%61.5, eşik %80); şema tüm renk alanlarını doldurduğu için görselde olmayan hex üretiyor (warning/info/error) → frontend-craft "hex uydurma yok" ile uyuşmuyor. Deneme klasörleri ve `~/.agents/` onayla silindi. Geri kurma:
```
DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 npx skills add zanwei/design-dna -a claude-code -g -y
```

## settings.json'a eklenen/değişen blok

```json
  "skillOverrides": {
    "morning": "off",
    "import-memory": "off",
    "canvas-design": "off",
    "theme-factory": "off",
    "web-artifacts-builder": "off",
    "docx": "off",
    "pptx": "off",
    "xlsx": "off",
    "pdf": "off",
    "mcp-builder": "off",
    "anthropic-skills:skill-creator": "off",
    "dataviz": "off",
    "claude-api": "off"
  },
```
```json
  "enabledPlugins": {
    "plugin-dev@claude-plugins-official": false,
    "dotnet-test@dotnet-agent-skills": false,
    "dotnet-nuget@dotnet-agent-skills": false
  }
```
(Önceden üçü de `true`; `enabledPlugins` içindeki diğer satırlar değişmedi.)

## Ölçüm (C:\Projeler\omer-skills, `claude -p`)

| | önce | sonra |
|---|---|---|
| `/context` Skills | 12.3k | 4.2k (−%66) |
| `/context` toplam | 22k | 19.6k |
| Gerçek istek girdi token'ı (`--output-format json`, "Yalniz OK yaz.") | 38.888 | 27.107 (−11.781, −%30.3) |

`/context` toplamı düşüşü eksik gösteriyor: kapatılan skill token'ları "System tools" satırına aynen ekleniyor (2.7k → 10.8k). Gerçek istek ölçümü bunu doğrulamıyor. "Önce" gerçek ölçümü, settings.json'a dokunmadan `--settings` bayrağıyla (pluginler `true`, override'lar `"on"`) alındı; global kopya taşındığı için ~90 token eksik.

Kapatma adayı ararken ilk bakış `/skill-doctor` (kullanılmayan skill'ler + context maliyeti); kapatma kabulü yine gerçek istek girdi token'ıyla (`claude -p --output-format json`) ölçülür.

## Ölçüm — synced plugin kapatma (2026-09-17, Claude Code 2.1.274, C:\Projeler\omer-skills, `claude -p`)

| | önce | sonra |
|---|---|---|
| `claude mcp list` Needs authentication / Failed to connect / Not configured | 15 / 5 / 8 | 0 / 0 / 0 |
| `/context` Skills | 7.4k | 3.7k |
| `/context` System tools | 7.5k | 11.2k |
| `/context` MCP tools (deferred) | 23.4k | 23.4k |
| `/context` toplam | 19.3k | 19.3k |
| Gerçek istek girdi token'ı (`--output-format json`, "Yalniz OK yaz.") | 32.556 | 28.451 (−4.105, −%12.6) |

`/context` toplamı yine değişmiyor: kapanan skill token'ları System tools satırına ekleniyor (09-15'teki gibi). MCP satırları değişmedi; düşüş Skills satırında.

Claude Docs kapatma sonrası (`/context`, yeni oturum): toplam 18.7k, MCP tools satırı (591) yok, MCP tools (deferred) 21.7k, Skills 3.4k; `claude mcp list`'te yalnız mslearn, context7, claude-design, 21st.

`claude mcp list` çıktısı raporlanırken context7'nin `--api-key` alanı maskelenir (`<GİZLİ>`); ham çıktı oturum kaydına düşer (09-17'de düştü, transcript'lerde maskelendi).

17 Eyl: context7 anahtarı yenilendi (eski değer transcript/yedeklerde geçmişti).

## Denendi, uygulanmadı — plugin skill'lerinde user-invocable-only (2026-09-17, Claude Code 2.1.274, C:\Projeler\omer-skills, `claude -p`)

Hedef: skill-creator:skill-creator (~120), impeccable:impeccable (~310), claude-md-management:claude-md-improver (~130), 21st:21st-ui (~90), claude-md-management:revise-claude-md (~30) · `/context` listeleme ≈680 token.
`skillOverrides` → `"user-invocable-only"` etkisiz; settings-reference `skillOverrides`: "Overrides don't apply to plugin skills, which you manage through `/plugin`."

| | önce | sonra |
|---|---|---|
| `/context` Skills | 3.4k | 3.4k (beş skill tabloda aynı token'la) |
| Gerçek istek girdi token'ı (`--output-format json`, "Yalniz OK yaz.") | 26.340 | 26.340 |

settings.json geri alındı (override öncesi kopyayla birebir); geri alma satırı gerekmiyor. Plugin skill'i için kalan yollar user-invocable-only değil: plugin geneli `claude plugin disable <plugin> -s user` (skill kullanıcıya da kapanır; 21st'te MCP sunucusu da gider) · plugin cache SKILL.md frontmatter `disable-model-invocation: true` (her plugin güncellemesinde silinir).
