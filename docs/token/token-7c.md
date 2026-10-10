# TOKEN-7c ölçümleri

## 7a paylaşımlı MCP (11 Eki 01:38–01:41, RAM yükü %80)

Düzenek: `.claude/t7c_oturum_olc.py`. Her koşu `claude -p --strict-mcp-config` (haiku) ile ~/.claude.json'daki 36 MCP'yi açar ve bir mcp-time çağrısı yapar. Süreç ağacının tepe değeri alındı; her kol ×2.

| ölçü | önce (ort) | sonra (ort) | fark |
|---|---|---|---|
| süreç / oturum | 180 (177, 183) | 88 (96, 80) | −51% |
| RAM / oturum | 5268 MB | 1446 MB | −73% |
| açılış + tek çağrı | 61 sn | 36.5 sn | −40% |
| sonuç | saat doğru | saat doğru | eşit |

- Paylaşımın sabit maliyeti: proxy ve 21 sunucu bir kez açılır, toplam 84–90 süreç / 3.5–4.1 GB. İlk oturumda başa baş çıkıyor; her ek oturum (CC, `claude -p`, köprü ajanı) ≈92 süreç / ≈3.8 GB kazandırır.
- Araç listeleri 21/21 eşit (stdio ve http aynı ad kümesi). godot 14/14 ve unity 80/80 doğrudan node ile eşit. Playwright'ın npx kolu kuru testte zaman aşımına uğradı (`@latest` çözümü), bu yüzden güvence gereği çevrilmedi.
- Hedef −%60: RAM'de tuttu (−73%), süreç sayısında tutmadı (−51%). Kalan süreçlerin çoğu eklenti MCP'leri (chrome-devtools ×2, azure, nano-banana, binlog, claude-mem, context-mode, universal-modder): bunlar plugin `.mcp.json` ile geliyor, kural gereği kapatılmıyor, kullanıcı yapılandırmasından da değiştirilemiyor.
- Bağlam ve kalite: araç tanımları birebir aynı olduğundan bağlam değişmiyor. G01 tam koşusu yapılmadı, yalnız işlev dumanı var.

Karar: UYGULANIR. Onay betiği `onay/token_7c_uygula.py`.
