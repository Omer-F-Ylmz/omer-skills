---
type: doc
status: active
tags: [code-mode, mcp, cloudflare, utcp, programmatic-tool-calling]
relatedTo: [code-mode, cloudflare-api]
---
# Code Mode: ne zaman hangisi (27 Eki 2026)

Kod kopyalanmadı; yalnız karşılaştırma. Cloudflare SDK bilgisi `packages/codemode/README.md` okumasından; Anthropic programmatic tool calling satırı bilgi birikimimden (bu oturumda doküman açılmadı, doğrulanmadı).

| | Cloudflare Code Mode MCP (`cloudflare-api`) | Code Mode SDK (`@cloudflare/codemode`) | Anthropic programmatic tool calling | Bizdeki code-mode (UTCP, `tools/cm.py`) |
|---|---|---|---|---|
| Ne | Hazır uzak MCP: tüm Cloudflare API'si 2 araçla (`search`, `execute`), ~1k token | Kendi araçlarını tek `codemode` aracına saran kütüphane; model TS tipleri görür, JS yazar | API tarafı: araçlar kod çalıştırma aracından çağrılır, ara sonuçlar bağlama girmez | Yerel MCP/CLI araçlarını UTCP ile tek çağrıda zincirler (isolated-vm sandbox) |
| Nerede çalışır | Cloudflare tarafı | Cloudflare Worker / DynamicWorkerExecutor; deneysel | Anthropic API konteyneri (Claude API uygulaması gerekir) | Yerelde, CC içinde (`cm.py list/search/info`) |
| Bizde kullanım | Cloudflare hesabı işi (DNS, Workers, R2) | Kendi ajan uygulaması Workers'ta kurulursa | Uygulamamız Claude API'yi doğrudan çağırıyorsa; CC oturumunda kullanılamaz | CC'de çok adımlı MCP zinciri, büyük çıktı süzme |
| Durum | Eklendi, **401** (anahtar Bearer token değil): bkz. aşağı | Kurulmadı | Kurulmadı | Çalışıyor |
| Risk | Yetki = token kapsamı; execute yazabilir, salt-okur token ver | "Experimental", API değişir | Beta başlığı gerekir | Yalnız yerel araçlar |

Seçim kuralı:
- Cloudflare hesabında iş → `cloudflare-api` (token düzelince); araç şeması bağlama girmez, mcptoon'a alınmaz.
- CC'de 2+ yerel araç zinciri / büyük çıktı → bizdeki `code-mode` (`tools/cm.py`).
- Kendi API uygulamamız çoğu araçla çalışıyorsa → Anthropic programmatic tool calling; Workers'ta ajan → Cloudflare SDK.
- Tek araç, küçük çıktı → hiçbiri, normal çağrı.

## cloudflare-api durumu
`claude mcp add --scope user --transport http cloudflare-api https://mcp.cloudflare.com/mcp --header 'Authorization: Bearer ${CLOUDFLARE_API_KEY}'` (`~/.claude.json`'da `${CLOUDFLARE_API_KEY}` literal; yedek `~/.claude.json.bak-codemode`). Ortamda `CLOUDFLARE_API_KEY` var ama sunucu HTTP 401 `invalid_token` döndü: değer büyük olasılıkla Global API Key (Bearer API token değil). BEKLİYOR: Cloudflare API token (OAuth ya da dash.cloudflare.com → My Profile → API Tokens → okuma izinli yeni token); değişken adı ya `CLOUDFLARE_API_KEY` kalır ya komut yeni adla yeniden eklenir. Token gelince sınama: yeni `claude -p` ile hesap/zone listesi.
