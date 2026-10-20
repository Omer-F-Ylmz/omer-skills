# TOKEN-REA d1 — PLAN (kendi sürümlerimiz)

Kural: kurulu araç silinmez/budanmaz; kendi sürüm yanında kurulur, A/B ile kazanırsa (taban üstü 4 eksende de, %98 kapı) Ömer onayıyla varsayılan olur. Ücretli çağrı yok, ölçüm Claude çağrısı ≤30.

## Önce veri: ağırlıklı taban 497.6M nerede? (taban.md profil tablosu, 14 gün)
| Kalem | Ağırlıklı | Pay |
|---|---|---|
| cache okuma (×0.1) | 192.5M | %38.7 |
| cache yazma (×1.25) | 178.0M | %35.8 |
| çıktı (×5) | 93.4M | %18.8 |
| girdi (×1) | 33.8M | %6.8 |
Sonuç: ağırlıklı maliyetin %75'i bağlam büyüklüğü + önbellek kırılması; komut çıktısı sıkıştırma (RTK/Headroom mesaj yolu) bunun yalnız küçük bir bölümünü hedefler. **Hedef "ek %50–60"ın yalnız araç sıkıştırmasıyla gelmesi beklenmez** — gerçek kaldıraç: sabit bağlam, önbellek yazma sıklığı, çıktı token'ı. Karar Ömer'de (aşağıda).

## Araç başı tasarım
| # | Sürüm | Tasarım | Beklenen kazanç (ölçülecek) | d2 kapısı |
|---|---|---|---|---|
| 1 | **bağlam-diyeti** (SessionStart + CLAUDE.md) | hook enjeksiyonu 14.6k → ≤6k: claude-mem gözlem sayısı (`CLAUDE_MEM_CONTEXT_OBSERVATIONS`), superpowers/using-superpowers tam metni yerine tek satır, kod haritası kısa; araç şeması 14.1k zaten ertelemeyle | istek başına −8k token; 24 329 istek × 8k × 0.1 = alt sınır ≈ −19M ağırlıklı (≈%4); cache yazma ilk turda ayrıca düşer | count_tokens sabit bağlam ≤22k; ilk-tur başarı (görev testi) eşit/üstü |
| 2 | **önbellek disiplini** (CC ayarları) | cache yazma %35.8: `token_olc --durma/--ttl-sim` ile TTL, /clear-compact zamanlaması, kurala bağlı | cache yazma −%20 ≈ −36M (≈%7) — varsayım, d2'de ttl-sim ile doğrulanır | aynı iş seti, ağırlıklı ≤ taban×0.93 |
| 3 | **rtk2** (sinyal-korumalı sarmalayıcı) | rtk + belirteç kapısı (yol/hash/sayı/error) → kayıpta ham; `ls` tüm ad, diff başlık, `git status` dizin sayımı | 10 komut seti −%30 → hedef ≥−%40 ve kalite 10/10 (şu an 8/10) | held-out 4 komut dahil kalite 100%, token ≥ baz |
| 4 | **sor2** (graphify hibrit) | etiket-önce + `git grep --seed` + token bütçesi ≤1.5k + kod-dışı ayrımı | sorgu başı 3.4k → ≤1.5k (−%55), isabet 6/10 → ≥9/10, 3.5 sn → <0.5 sn | held-out 5 soru, isabet ≥9/10 |
| 5 | **hr2** (Headroom yanı) | şema ertelemesi CC `ENABLE_TOOL_SEARCH` ile çakışma ölçümü; ML'siz soğuk yol; retrieve oranı telemetrisi | mesaj sıkıştırma ≈%2.6–4.8 → hedef +3 puan; çakışma çıkarsa tek katman bırakılır (A6 iki kol eşit: 22 319 ↔ 22 319) | üretim savings_events farkı, retrieve oranı <0.1 |
| 6 | **çıktı-diyeti** | çıktı ×5 ağırlığı %18.8: Concise stil + ajan çıktısı tavanı + alt ajan özet sınırı | çıktı −%15 ≈ −14M (≈%3) — varsayım | aynı iş seti çıktı token'ı, kalite hakemi eşit |
| 7 | claude-mem / BEYİN | arama zaten ~518 token/sorgu; enjeksiyon #1'de; BEYİN A/B %42–48 mevcut | ek kazanç yok, yalnız hakemli kalite seti (claude-mem 9/10 → hakemli) | hakem 19/20 altına düşmez |
| 8 | context-mode · OmniRoute · jev · qmd · NotebookLM · mcp-memory | d2'de önce taban ölçümü (MCP şema token'ı `tools/list` count_tokens; ücretsiz zincir kapıları var) | bilinmiyor | d2 taban |

**Toplam beklenen (varsayımlarla): ≈ −69M … −75M ağırlıklı ≈ %14–15** (1: 19M + 2: 36M + 6: 14M + diğer birkaç M). %50–60 hedefi (≥249M) için bu yetmez; kalan fark ancak iş desenini değiştirerek gelir (daha az tur, alt ajan/ücretsiz modele delege, kısa oturum). Bu bir kanıtlanmış sonuç değil, taban ağırlıklarından türetilmiş tahmindir; d2'de #1 ve #2'nin ölçümü hedefin gerçekçiliğini belirler.

## Sıra (d2 önerisi)
1. #1 + #2 (en büyük pay, kod yazmadan ayar/enjeksiyon; ölçüm betiği hazır: taban.py profil + token_olc ttl-sim).
2. #3 rtk2 sarmalayıcı (küçük, tohumlu set hazır) + #4 sor2.
3. #8 taban ölçümleri (bekleyen 6 araç) → durum `taban`.
4. #5, #6.
Mühür: held-out adları taban.json'da; kapıda tek seferlik.
