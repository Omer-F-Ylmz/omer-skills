# CODE-MODE-REA-3 (24 Eki)

**Sonuç:** M1–M5 yerel paketle (`.kos/kopru/ara/cm-yerel/`, 10 paket) örtüşüyor; sürüm farkı yok sayılacak düzeyde. Karşılaştırma `cm-src` (upstream kaynak .ts) ↔ yerel `dist`.

| Paket (yerel) | Sürüm |
|---|---|
| @utcp/code-mode | 1.2.13 |
| @utcp/code-mode-mcp | 1.2.1 |
| @utcp/code-mode-cli | 0.1.1 |
| @utcp/sdk | 1.2.0 |
| @utcp/mcp 1.2.0 · cli 1.1.3 · http 1.1.13 · file/text/dotenv-loader 1.1.0 | |

| Madde | cm-src (upstream) | Yerel dist | Durum |
|---|---|---|---|
| M1 tembel şema, `search_tools` limit varsayılan 10 | mcp-index:174, cli-index:320 | code-mode-mcp/dist:147, code-mode-cli/dist:300 | aynı |
| M2 zaman aşımı 30000 · bellek 128 MB · `max_output_size` 200000 · `isolated-vm` | client:182-189, mcp-index:286-298 | code-mode/dist:152-155, mcp/dist:260-271 (`3e4`=30000) | aynı |
| M3 ad×2 · etiket kısmi ×0.5 · açıklama kısmi ×0.5 · etiket alt-dize ×0.3 | tag_search_strategy:76,99,108,135 | sdk/dist:604,621,650 + `×0.3`, `length > 2` (625-642) | aynı |
| M4 `__interfaces`, `__getToolInterface`, "Access as: manual.tool(args)" | client:513-521 | code-mode/dist:23-26,125,383-390 | aynı |
| M5 `AGENT_PROMPT_TEMPLATE` | client:15-55 | code-mode/dist:10 (+ mcp/dist:98, cli/dist:275) | aynı |

Notlar:
- `cm-src` satır numaraları rea-1 (M:/C:/T:) ile aynı dosyalardan; yerel dist derlenmiş olduğundan satırlar kayık, değerler aynı.
- Upstream'in şu anki npm sürümüyle karşılaştırma YAPILMADI (cm-src'de sürüm etiketi yok; ağ/registry sorgusu kapsam dışı bırakıldı). Yerel sürümler kesin; "upstream güncel mi" bilinmiyor.
- İzin engeli (rea-2 madde 3) `cm-yerel` kopyasıyla aşıldı; Bash `rg`/`python -I` ile okundu.
