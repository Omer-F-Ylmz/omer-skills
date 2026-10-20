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

## d2 SONUÇ (20 Eki 2026; Claude -p çağrısı 8/15, count_tokens ~100)
**d2a bağlam-diyeti** (`d2a_bolum.py`, `d2a_ab.py`, ajan profili, geçici --settings; kurulu ayar değişmedi):
- Blok dökümü (token): CLAUDE.md+hafıza dizini 4743 · ortam/ajan listesi 2374 · context-mode 1760 · claude-mem 1408+271 · superpowers 1292 · ponytail 934 + kod haritası 1159 · diğer 170. Hook toplamı ≈6.8k; kalan 7.3k hook değil.
- A (taban) 30 080 → B (superpowers/ponytail/context-mode kapalı + claude-mem gözlem 5) **25 335 (−4 745, −%15.8)**; görev testi iki kolda da doğru ('kur'); görev maliyeti 0.082→0.038 $ (tek ölçüm, gürültülü). **Kapı ≤22k KARŞILANMADI** (−3.3k eksik): kalan kaldıraç CLAUDE.md+MEMORY.md dizini (4.7k, kısaltma Ömer kararı) ve ortam/ajan listesi (2.4k).
- Ağırlıklı tahmin (hepsine uygulanırsa): 24 329 istek×4.7k×0.1 + 1262 oturum×4.7k×1.25 ≈ −19M ≈ %3.8 (plan varsayımı 19M ile tutarlı, 8k yerine 4.7k ile).
- **Önbellek disiplini**: `token_olc --ttl-sim` (66 oturum, 1691 istek): "baştan" yazma %31.8; sebep: ara>TTL yalnız %11.4, "diğer" %85.6 (oturum başı/ön ek değişimi). TTL tek başına hibrit −%4.1, 5m +%6.4 (1h'e göre). **Plandaki "cache yazma −%20" varsayımı DESTEKLENMİYOR**: TTL kolu ≈ −%4 × 53M ≈ −2M ağırlıklı (≈%0.4). Asıl kaldıraç ön ek sabitliği + oturum sayısı.
**d2b rtk2** (`rtk2.py`, `rtk2_set.py` kilit `rtk2_set.lock`, `rtk2_ab.py`): rtk çıktısı ham'daki dosya adı/hash belirtecini kaybederse eksikler sona eklenir; `ls` ad+boyut ile yerel üretilir.
- Eğitim 20 komut: ham 318 630 → rtk 163 022 (−%48.8) → **rtk2 179 386 (−%43.7)**; sıkı sinyal (her ham ad çıktıda) rtk 13/20 → **rtk2 20/20**. Held-out 4 (tek sefer): ham 20 890 → rtk 14 039 → rtk2 14 116 (−%32.4); sıkı **rtk 3/4 → rtk2 4/4**; tohum anahtar 3/4 (ikisinde de) — kaçan `git diff` anahtarı otomatik seçilen `a/tools/beyin.py` ön eki; dosya adı çıktıda var → anahtar yapaylığı, kalite kaybı değil. Maliyet: rtk2 süresi rtk'ye göre ~+%50 (iki süreç).
- Dürüstlük: 'ls' kompakt çıktısı büyük dizinde (`.kos/kopru` 40k→13.5k, rtk 590 ama ad kaybı) rtk'den çok daha uzun; kazanç −%43.7 < rtk −%48.8, bedeli kalite. Kapı "kalite 10/10 → RTK kazancı": sağlandı (20/20, 4/4). Varsayılan geçiş Ömer onayı.
- **sor2 (graphify hibrit) YAPILMADI** (tur tavanı); d3'e.

## ★ d3 TASLAK
1. sor2 (graphify hibrit) + held-out 5 soru metni yazıp kilitle; isabet ≥9/10, ≤1.5k token, <0.5 sn.
2. İş deseni kolu ölç: köprü şablonunda tur/okuma tavanı · ucuz alt ajan delegasyonu (ucretsiz_havuz+Haiku) · erken /clear · sabit ön ek; plan.md'de iki kolun toplamıyla %50-60 yolu sayıyla (şu an: araç ≈%4 + rtk2 + diyet ≈%3.8 + çıktı ≈%3 → ≈%10-12; kalan ≈%40 yalnız tur×bağlam azaltımından gelebilir).
3. Bağlam-diyeti ikinci adım: MEMORY.md dizin kısaltma + ortam/ajan listesi ile ≤22k (Ömer onayı) ve ham kalite setleri 20 madde/anlam hakemi.
4. d2c: bekleyen 6 aracın tabanı, hr2, çıktı-diyeti.
