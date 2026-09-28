## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- Okuma kuralı: dosya içeriği yalnız Read aracıyla ve dar satır aralığıyla (~20 satır) okunur; Bash cat/sed/head/tail/awk ya da grep -A/-B/-C ile içerik basılmaz, konum için Grep (files_with_matches / -n). Gerekçe: headroom Bash çıktısını sıkıştırır (okuma başına ~3 çağrı: döküm → okuma → headroom_retrieve); Read de ~200 kelimeyi aşınca sıkışır, dar aralık retrieve'ı önler.
