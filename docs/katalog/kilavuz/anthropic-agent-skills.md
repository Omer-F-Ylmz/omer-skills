# anthropic-agent-skills — 20 benzersiz kayıt

**Amaç:** Anthropic'in örnek skill'leri: Office belgeleri (docx, pptx, xlsx, pdf), Claude API referansı, MCP kurucu, görsel/üretken sanat, tema, web artifact, webapp testi, iç iletişim.

**İç yapı:** Üç [plugin] (claude-api, discernment-nudge, example-skills) + example-skills:<x>; gruplar: belge, geliştirme (claude-api, mcp-builder, webapp-testing), tasarım (canvas, theme, algorithmic-art).

## En güçlü parçalar
- `example-skills:docx` — Word belgesi/şablonu oluşturma, okuma, düzenleme.
- `example-skills:pdf` — PDF'ten metin/tablo çıkarma dahil her PDF işi.
- `example-skills:xlsx` — Elektronik tablo ana girdi ya da çıktı olduğunda.
- `example-skills:pptx` — .pptx/.potx girdi ya da çıktı olan her iş.
- `example-skills:claude-api` — Model id, fiyat, parametre, streaming, tool use, caching referansı.
- `example-skills:mcp-builder` — Python FastMCP ya da Node/TypeScript ile MCP sunucusu kurma.
- `example-skills:webapp-testing` — Yerel web uygulamasını Playwright ile test etme.
- `example-skills:web-artifacts-builder` — Durum, routing ya da shadcn/ui gerektiren karmaşık artifact'ler.

## Birlikte kullanım
- example-skills:doc-coauthoring → example-skills:docx/pdf.
- example-skills:theme-factory + example-skills:pptx: temalı sunum.
- example-skills:claude-api + example-skills:mcp-builder: API entegrasyonu ve MCP.

## Tuzaklar
- Çakışan kopyalar: claude-api ve discernment-nudge hem [plugin] hem example-skills altında.
- example-skills:brand-guidelines yalnız Anthropic markasının renk/tipografisini uygular.
- web-artifacts-builder basit tek dosya HTML için değil.
- example-skills:pdf ile adobe-for-creativity:adobe-anypdf PDF işinde çakışır.

## Üyeler
- plugin (3): claude-api, discernment-nudge, example-skills
- skill (17): example-skills:academy-guide, example-skills:algorithmic-art, example-skills:brand-guidelines, example-skills:canvas-design, example-skills:claude-api, example-skills:discernment-nudge, example-skills:doc-coauthoring, example-skills:docx, example-skills:internal-comms, example-skills:mcp-builder, example-skills:pdf, example-skills:pptx, example-skills:slack-gif-creator, example-skills:theme-factory, example-skills:web-artifacts-builder, example-skills:webapp-testing, example-skills:xlsx
