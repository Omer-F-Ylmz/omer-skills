# Araç kapısı (mcp_kapi) — +11k teşhisi (ERİŞİM-TAM-1D, 22 Eki)

Yöntem: yerel kayıt vekili (`.kos/kopru/kapi-teshis/vekil.py`, git dışı) `claude -p` ↔ headroom arasında istek gövdelerini kaydetti; `tools/erisim_olc.py` kolları `EO_PROXY` / `EO_DUMP` ile koşuldu. Headroom `--no-optimize` (geçiş) ile de aynı sayılar → headroom kaynak değil.

## 1. Kapının sabit yükü (istek başına, bayt → ~jeton)
| parça | bayt | ~jeton |
|---|---|---|
| `mcp__kapi__ara` + `cagir` şemaları | 400 | ~100 |
| sunucu `instructions` | yok (initialize dönmüyor) | 0 |
| ruflo doğrudan 5 araç (KEEP) | 5.5k | ~1.5k |
| ToolSearch (etkinse) | – | ~6.5k |
| yerleşik araçlar + sistem | 40k + 8.9k | ~14k (boş taban ile aynı) |

İlk istem (MCP bağlı, vekil günlüğüyle kanıtlı): boş taban 16.077 · kapı-tek 16.088–16.096 (**+%0,1**) · kapı+ruflo doğrudan: araç gövdesi +5,5k bayt. → "ilk istem ≤ taban +%1" kapı-tek için sağlanıyor; ruflo doğrudan ~+%9 getirir.

## 2. "+11k" nerede? (ikinci istem)
Kapı çağrısından sonraki istem 16,1k → 26,3–27,0k. Araç şeması, instructions, ruflo ve `ara` sonucu (<1k jeton) **kaynak değil**. Ablasyon (aynı gövde, tekrar oynatma):
| değişiklik (26.957 jetonluk 2. istemde) | toplam |
|---|---|
| hiçbiri | 26.957 |
| `server_tool_use`+`tool_search_tool_result` blokları silindi | 26.659 |
| **`thinking` bloğu silindi** | **17.298** |
| üçü de silindi | 17.000 |

Fark (~9,7k) asistanın geçmişteki `thinking` bloğundan geliyor (adaptif düşünme, imza); çıktı yalnız ~74 düşünme jetonu. Karşı kanıt: ruflo doğrudan çağrılan kolda (düşünme bloğu yok) 16.070 → 17.271 (+1,2k). Kapı kolunda haiku her seferinde düşünüyor (3/3), doğrudan kolda düşünmedi. `MAX_THINKING_TOKENS=0` ayar env'i etkisiz kaldı (2/2 koşu aynı 26,3k). Yani kalan yük **kapı şemasından değil, düşünme bloğunun API tarafı sayımından**; kaynağı kapı içinden sıfırlanamıyor (nedeni bilinmiyor, kanıtsız tahmin yazılmadı).

## 3. Kararlar
- Araç açıklamaları zaten ≤300 jeton (~100), instructions boş → kısaltma kazancı yok, dokunulmadı.
- **ruflo kapı arkasına ALINMADI** (görevin önerisine ters): kapıdan çağrı 2. istemi +10k şişiriyor (düşünme), doğrudan çağrı +1,2k. İlk istemde −1,5k kazanç < çok istemli iş kaybı. Ölçüm: ruflo doğrudan 16.070→17.271 · ruflo kapıdan 16.088→26.337.
- Teşhis yardımcıları: `erisim_olc.py` `EO_PROXY`, `EO_DUMP`; vekil `.kos/kopru/kapi-teshis/`.

## 4. Uçtan uca (köprü ajanı, haiku)
kapı→`ara` ✓ · kapı→mcp-git `git_status` ✓ · kapı→ruflo `memory_search` ✓ · ruflo doğrudan `memory_search` ✓ · hata 0 / 6 çağrı. Önceki 10/10 turu (docs/erisim-haritasi.md §5) yeniden koşulmadı.

## 5. Yapılmayan
- CC etkileşimli ve Desktop yüzeyinde 3'er çağrı: koşulmadı (kapı kullanıcı MCP'sinde kayıtlı değil; kayıt ayrı karar).
- auth0 zaman aşımı nedeni incelenmedi. figma/canva/claude-design OAuth (kapıdan 401) doğrudan kalır.
- Düşünme bloğunun neden ~9,7k saydığı ve `MAX_THINKING_TOKENS` ya da effort ile kapanıp kapanmadığı açık soru.

## 6. Tur 2 (22 Eki) — düşünme kolları + uçtan uca
Kapı-tek, haiku, `mcp__kapi__ara sorgu='git'` (`EO_AYAR` ile ayar kolları, `tools/erisim_olc.py`):
| kol | ilk → ikinci istem | not |
|---|---|---|
| taban (ENABLE_TOOL_SEARCH=false, köprü yolu) | 16.073 → 29.7k | sıçrama sürüyor |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` / `CLAUDE_CODE_DISABLE_THINKING=1` | 16.073 → 29.7k | etkisiz |
| `alwaysThinkingEnabled:false` + `MAX_THINKING_TOKENS=0` (3 koşu) | 29.6k · çağrısız · 29.7k | etkisiz; thinking bloğu 3/3 yine geliyor |
| ENABLE_TOOL_SEARCH=true (ToolSearch istemci aracı) | 22.8k → 23.1–23.7k → 25.3k | sıçrama yok, ama ilk istem +6,7k |
Yeni bulgu: araç şemasında ertelenmiş araç ve `ToolSearch` yokken bile model `server_tool_use tool_search_tool_regex` üretiyor, API çalıştırıyor (`pattern: kapi__ara|kapi`, 2 `tool_reference`); ikinci istemde önbellek öneki 14,1k→19,7k okuma + 10k yeni yazma. Sıçrama düşünme+sunucu-tarafı araç araması ikilisine bağlı; düşünme istemci ayarıyla kapanmıyor (beta başlıkları: `thinking-token-count`, `thinking-display-updates`). Kapı içinden sıfırlanamaz; kapıyı kullanmayan tek-istemli işte maliyet 0, ruflo doğrudan çağrıda +1,2k.
Karar: değişiklik yok (ENABLE_TOOL_SEARCH=true tek-istemli işte +6,7k kaybettirir, ikinci istemde başa baş; çok istemli işte kazanç sınırlı — ayrı karar).

Uçtan uca (köprü ajanı, haiku, tek koşu, 87 sn): skill yükleme 2/2 (yetenek-getir, graphify) · CLI 2/2 (rtk, markitdown) · ruflo doğrudan `memory_search` ✓ · kapı→mcp-time ✓ · kapı→mcp-git ✓ · kapı `ara` ✓ = 8/8, MCP hata 0. Testler: test_mcp_sec/paylasim/hafif_kabul/hafif_2_env 8 geçti.
Yapılmayan (değişmedi): CC etkileşimli + Desktop yüzeyi 3'er çağrı (kapı kullanıcı MCP'sinde kayıtlı değil → kayıt ayrı karar); auth0 zaman aşımı nedeni. Kabul "ilk istem ≤ taban +%1": kapı-tek 16.073–16.096 (+%0,1) ✓; ikinci istem yükü yukarıdaki tabloda gerekçeli.
