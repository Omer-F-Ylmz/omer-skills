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
