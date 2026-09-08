# omer-skills

Ömer Faruk Yılmaz'ın Claude Code skill marketplace'i. Şu an tek eklenti: **frontend-craft**.

## Kurulum

```
/plugin marketplace add Omer-F-Ylmz/omer-skills
/plugin install frontend-craft@omer-skills
```

Yeni bir makinede skill'in screenshot/audit script'leri çalışmadan önce iki adım gerekir:

```
cd ~/.claude/plugins/marketplaces/omer-skills/plugins/frontend-craft/skills/frontend-craft
npm i
npx @puppeteer/browsers install chrome
```

`npm i` puppeteer'ı kurar; Chrome binary'si ayrı indirilir, ikinci komut olmadan `screenshot.mjs` çalışmaz.

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
