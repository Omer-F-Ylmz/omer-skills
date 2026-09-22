# Jev (TypeSafe System One) — kaynak taraması (KURULUM-13a, 2026-09-22)

## Resmi kaynaklar
| Kaynak | Sürüm / SHA | Lisans |
|---|---|---|
| github.com/typesafe-ai/skills (plugin `typesafe@typesafe-ai` 0.5.7) | `65a39f393687675ce170e6094757de20370365b9` | MIT |
| github.com/typesafe-ai/typesafe-sdk-js (npm `@typesafe-ai/sdk` 0.6.0) | `66880ccded6cb642dc1809620c2b108c33730214` | MIT |
| docs.typesafe.ai/llms-full.txt · /api · /models · /agent-skill · /model-jaggedness | 2026-09-22 okundu | — |
| openrouter.ai/docs/guides/community/typesafe-sdk | 2026-09-22 okundu | — |

SkillSpector `--no-llm` (typesafe-ai skill): 0 bulgu, çalıştırılabilir betik yok.
claude.ai zip'i (`dist/yukle-13/typesafe-ai.zip`): description 660 → 170 karakter kısaltıldı (claude.ai 200 sınırı); gövde ve LICENSE aynen.

## Seçimler (kanıtla)
- **İstemci: resmi SDK.** `TypeSafeClient({ apiKey, baseURL })` iki backend'i karşılıyor: OpenRouter rehberi `baseURL: 'https://openrouter.ai/api'` gösteriyor, SDK `/v1/systemone` ekliyor. SDK retry varsayılanı tarifle aynı (408/429/5xx, en fazla 2, `retry-after`). `logLevel: "off"` koddan verilir; SDK debug seviyesinde gövdeyi logluyor (`client.ts`: `logger.debug(... "<- body", parsed)`), kod ayarı ortam değişkeninden önce gelir.
- **HTTP: MCP SDK `StreamableHTTPServerTransport` (stateless, JSON yanıt)**, mcp-handler değil: stdio için zaten gereken tek bağımlılık yetiyor, Vercel Node fonksiyonu `(req, res)` imzasını doğrudan alıyor.
- **Model eşleme istemcide yok:** OpenRouter çıplak `jev-1.13` / `jev-latest` adlarını kendisi `typesafe/jev-1.13` / `~typesafe/jev-latest`'e çeviriyor (rehber "Model IDs").
- **Bağlam sınırı:** docs yalnız model sınırını veriyor (64k toplam, state + en uzun soru 32k). OpenRouter'a özel 32k toplam izin verilen kaynaklarda doğrulanamadı; iki backend'e de docs değeri uygulandı. Token sayımı kaba (UTF-8 bayt/4); kesin sınırı sunucunun 422'si belirler.
- **Hata gövdesi:** docs alan adlarını vermiyor; SDK `message` / `error.message` / `detail` okuyor. Biz `message` + `error_type` alanlarını alıyoruz, gövdenin geri kalanını (girdi yankısı) atıyoruz.

## Ücret / limit (docs.typesafe.ai/models, Jev 1.13 = `jev-1.13.0`)
| Kalem | Değer |
|---|---|
| Girdi | $42 / Btok · $0.042 / Mtok |
| Çıktı | ücretsiz |
| Hız | 250.000 token/sn · 1.200 istek/dk (dinamik) |
| Bağlam | 64k/istek · state + en uzun soru 32k |
| Girdi türü | yalnız metin |
| ZDR | yalnız kurumsal plan |

Canlı duman (OpenRouter): noul isteği 284 girdi token, cost 0.0000119 $.

## Kurulmayan topluluk sunucuları
Hiçbiri kod düzeyinde incelenmedi; ortak gerekçe: resmi değiller (tarif: topluluk sunucusu kurulmaz) ve resmi SDK + `mcp/jev`'in 3 aracı aynı yüzeyi kapsıyor.
- itsmostafa: resmi değil, kurulmadı.
- parksjr/racecraft: resmi değil, kurulmadı.
- rashedInt32: resmi değil, kurulmadı.
- klukacin: resmi değil, kurulmadı. Hook'ları (subagent router · PreToolUse) **13b adayı**; `SUBAGENT_MODEL_FORCE` ile çakışır, önce o ayar çözülmeli.
- ThePFMind: resmi değil, kurulmadı.
Resmi olmayan host'lar (jev-ai.pro vb.) kullanılmadı.
