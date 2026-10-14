# context-mode — 10 benzersiz kayıt

**Amaç:** Komut ve dosya çıktısını sandbox'ta işleyip FTS5 ile indeksleyerek yalnız sonucu döndüren bağlam tasarrufu MCP'si; oturum sürekliliği ve tanılama skill'leri.

**İç yapı:** context-mode [mcp] + context-mode [plugin] + context-mode:<komut> skill'leri; kullanım (context-mode, ctx-index, ctx-search), izleme (ctx-stats, ctx-insight), bakım (ctx-doctor, ctx-upgrade, ctx-purge).

## En güçlü parçalar
- `context-mode:context-mode` — Büyük çıktıları Bash/cat yerine ctx_execute/ctx_execute_file ile işletir; ham veri bağlama girmez.
- `context-mode:ctx-search` — Daha önce indekslenen proje içeriği, doküman ve oturum verisinde FTS5 araması.
- `context-mode:ctx-index` — Yerel dosya/dizini kalıcı FTS5 bilgi tabanına indeksler.
- `context-mode:ctx-doctor` — Runtime, hook, FTS5, eklenti kaydı ve sürüm tanılaması.
- `context-mode:ctx-stats` — Oturumda ne kadar bağlam tasarruf edildiğini gösterir.

## Birlikte kullanım
- context-mode:ctx-index → context-mode:ctx-search: yerel dokümanı bir kez indeksle, sonra ara.
- context-mode:ctx-doctor + context-mode:ctx-upgrade: hook/ayar sorunlarını teşhis edip düzeltmek.
- context-mode:ctx-stats + context-mode:ctx-insight: tasarruf ölçümü.

## Tuzaklar
- context-mode:ctx-purge tüm indeksli içeriği ve oturum istatistiklerini kalıcı siler; yıkıcıdır.
- context-mode:ctx-insight panoyu varsayılan tarayıcıda açar ve barındırılan analitik katmanına dayanır.

## Üyeler
- mcp (1): context-mode
- plugin (1): context-mode
- skill (8): context-mode:context-mode, context-mode:ctx-doctor, context-mode:ctx-index, context-mode:ctx-insight, context-mode:ctx-purge, context-mode:ctx-search, context-mode:ctx-stats, context-mode:ctx-upgrade
