# mcp — 51 benzersiz kayıt

**Amaç:** Kurulu MCP sunucuları: tasarım (figma, canva, stitch, 21st), kod keşfi (serena, codegraph, jev), belge/arama (context7, markitdown, brave-search, arxiv), oyun/3B (blender, godot, unity), platformlar.

**İç yapı:** Çoğu [mcp]; plugin:<eklenti>:<ad> önekliler eklenti içinden gelir; açıklamalarda 'için; X değil' ayrım kalıbı; '(tahmin)' işaretliler doğrulanmamış.

## En güçlü parçalar
- `serena` — LSP tabanlı sembol arama ve sembol düzeyinde düzenleme; büyük kod tabanında grep yerine.
- `context7` — Kütüphanelerin güncel dokümanı ve kod örnekleri.
- `jev` — Kod tabanında ilgili dosya bulur, log triage yapar; bağlamı daraltır.
- `headroom` — Araç çıktısını sıkıştırır, hash ile tam metni geri getirir.
- `playwright` — Tarayıcı sürme, tıklama, form, ekran görüntüsü; web otomasyon/test.
- `figma` — Tasarım, frame, bileşen okuyarak tasarımdan koda.
- `github` — Repo, issue, PR, kod arama; uzak GitHub işleri.
- `blender` — Çalışan Blender'ı uzaktan yönetir; doğrulama kapısı değil.
- `markitdown` — PDF, DOCX, PPTX, XLSX, HTML'i LLM için Markdown'a çevirir.
- `mslearn` — .NET/Azure için resmi Microsoft Learn belgeleri.

## Birlikte kullanım
- jev + serena + codegraph: dosya daraltma, sembol grafiği, sembol düzeyinde düzenleme.
- context7 + mslearn + drizzle-docs: kütüphaneye özel güncel doküman.
- blender + omer-araclar blender_dogrula/blender_gorunum: sahne yönetimi ve doğrulama kapısı.
- figma/stitch/21st + playwright: tasarımı çekip uygulanmış UI'ı tarayıcıda doğrulamak.

## Tuzaklar
- Çakışan araçlar: playwright/puppeteer, mcp-memory/claude-mem/codebase-memory-mcp, codegraph/serena.
- '(tahmin)' işaretli açıklamalar (canva, airtable, apify, gsc, hostinger vb.) doğrulanmamış.
- Hesap/anahtar isteyenler: github, figma, auth0, hostinger, apify, brave-search, canva, gsc.
- mcp-integration [skill] plugin-dev:mcp-integration'ın kopyası.

## Üyeler
- mcp (50): 21st, airtable, apify, arxiv, auth0, blender, brave-search, canva, cc-kopru, claude-design, claude-mem, clickhouse, code-review, codebase-memory-mcp, codegraph, context7, drizzle-docs, excalidraw, figma, github, godot, gsc, headroom, hfspace, hostinger, infinite-canvas, jev, markitdown, mcp-fetch, mcp-filesystem, mcp-git, mcp-memory, mcp-sequential-thinking, mcp-time, mslearn, n8n-mcp, netlify, obsidian, playwright, plugin:adobe-for-creativity:Adobe for creativity …
- skill (1): mcp-integration
