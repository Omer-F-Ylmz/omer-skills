# Upstream issue taslağı: rea-agents MCP, istemci `env` bloğu iletilmediğinde full şema profili (≈179 KB) yayınlanıyor

Paket: `rea-agents` 6.7.0 (`rea mcp`, stdio). Ortam: Windows 11, Node 24.19.0, Claude Desktop + Claude Code.

## Sorun
Claude Desktop, MCP sunucu yapılandırmasındaki `env` bloğunu REA sürecine iletmiyor (süreç ortamında
`REA_MCP_INPUT_SCHEMA_PROFILE` / `REA_MCP_OUTPUT_SCHEMA_PROFILE` yok; doğrulandı). Değişken yokken
`tools/list` varsayılan **full** girdi profiliyle döner: `compare_web_captures` tek başına ≈180 KB, toplam şema
bağlayıcının sınırını aşıyor ve araçlar reddediliyor/gizleniyor.

## Beklenen
- `env` iletilmese de güvenli (compact) varsayılan, ya da
- sürec argümanı: `rea mcp --input-schema-profile compact --output-schema-profile off`.

## Yeniden üretme
1. Yapılandırmada `env: {REA_MCP_INPUT_SCHEMA_PROFILE: "compact"}` ver; Desktop'tan başlat → süreç ortamında değişken yok.
2. `tools/list` → `compare_web_captures` inputSchema ≈180 KB.

## Geçici çözüm (bizde)
`tools/rea-mcp-compact.mjs`: değişkenleri süreç İÇİNDE sabitleyip `scripts/rea.mjs mcp`'yi import eder.
`tools/rea-sema-tara.py --profil sarmal`: araç şeması ≤32 KB, 207 araç, temiz.

## Ek gözlem
`compare_web_captures` girdisi `{before:{inspection:<normalized_result>}, after:{...}}` ya da `before_scenario/after_scenario`;
compact açıklaması bunu söylemiyor, hata iletisinden öğrenilir. Compact açıklamaya örnek girdi eklenmesi yararlı olur.
