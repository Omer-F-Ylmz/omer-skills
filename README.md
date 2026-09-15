# omer-skills

Ömer Faruk Yılmaz'ın Claude Code skill marketplace'i. Şu an tek eklenti: **frontend-craft**.

## Kurulum

```
/plugin marketplace add Omer-F-Ylmz/omer-skills
/plugin install frontend-craft@omer-skills
```

## Yeni makinede

Marketplace'i ekledikten sonra ortamın tam çalışması için gereken adımlar. Hepsi bir kez, makine başına yapılır.

**1. frontend-craft script bağımlılıkları**

Elle adım yok. Skill kurulu kopyadan yüklenince bağımlılıkları kendisi kurar; tek kaynak SKILL.md "Adım 0 · Bağımlılık".

**2. context7 MCP (kütüphane dokümantasyonu)**

```
npm i -g @upstash/context7-mcp
npm root -g          # global dist yolunu buradan al
```

MCP sunucusu `npx` ile değil, global dist'e doğrudan `node` ile bağlanır — `npx` Windows'ta stdin altında ölüyor:

```json
"context7": {
  "type": "stdio",
  "command": "node",
  "args": [
    "<npm root -g>\\@upstash\\context7-mcp\\dist\\index.js",
    "--api-key",
    "<context7 api key>"
  ]
}
```

**3. C# dil sunucusu**

```
dotnet tool install -g csharp-ls
```

`csharp-lsp` eklentisi bu tool'u bekler; kurulu değilse LSP sessizce devre dışı kalır.

**4. Hook'lar**

Hook'lar Windows PowerShell 5.1 ile çağrılır; `command` alanı `powershell.exe`, script `-File` ile verilir:

```json
{
  "type": "command",
  "command": "powershell.exe",
  "args": ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:\\Users\\pc\\.claude\\hooks\\<script>.ps1"]
}
```

pwsh 7 opsiyonel — kuruluysa `command` `pwsh` yapılabilir, ama 5.1 her Windows'ta hazır geldiği için varsayılan bu.

## frontend-craft ne yapar

Web arayüzüne (Razor/HTML/CSS/Tailwind) dokunan işlerde uygulanan disiplin:

- **Mod tespiti** — `reference/` klasörü varsa REF (birebir eşleme), yoksa FREE (marka kimliği kararı + guardrail'ler).
- **Screenshot döngüsü** — 390 / 768 / 1440 px, sapma tablosu, min 2 max 4 tur.
- **Anti-generic yasak listesi** — mor-indigo gradient, emoji ikon, "h1+p+2 buton" hero kalıbı, eşit kart tekrarı vb.
- **Kabul kriterleri** — `audit.mjs` PASS, a11y (landmark, alt, kontrast), perf (font bütçesi, CLS 0).
- **Bölüm 6 tur raporu** — rapor yazılmadan iş kapanmaz.

## Proje tipine göre ne kurulur

| Proje tipi | frontend-craft | Yanında | Not |
|---|---|---|---|
| Corvano, Divisima (e-ticaret web) | ✅ zorunlu | `ui-ux-pro-max` | Razor/Tailwind vitrin; FREE modda marka kararı önce |
| Oyunlar (web tabanlı) | ✅ menü/HUD ekranları için | `ui-ux-pro-max` | Oyun içi render skill kapsamı dışında |
| Roblox (Luau) | ❌ | — | Skill web DOM'una bağlı; Roblox UI'ına uygulanmaz |
| EgeYapı (kurumsal tanıtım sitesi) | ✅ zorunlu | `ui-ux-pro-max` | Referans görsel varsa REF modu |
| Garajım / Teknik Paket (panel) | ✅ zorunlu | `ui-ux-pro-max` | Yoğun form/tablo ekranları |
| Java (masaüstü / servis) | ❌ | — | Web arayüzü yoksa gerekmez |
| Sunum | ❌ | `pptx`, `canvas-design` | Claude Code ile birlikte gelen skill'ler |

`ui-ux-pro-max` bu marketplace'te değil; kendi kaynağından `~/.claude/skills/` altına kurulur. `pptx` ve `canvas-design` Claude Code ile birlikte gelir, ayrıca kurulum istemez.

## Kaynaklar ve atıflar

- Guardrail listesi ve tasarım kabul kriterleri, **Burhan Kocabıyık**'ın Claude Code kitinden uyarlandı.
- Renk/tipografi/design-system aramaları için **ui-ux-pro-max** skill'i referans alındı; frontend-craft FREE modunda marka kararı öncesi onu çağırır.

## Lisans

MIT — bkz. [LICENSE](LICENSE).
