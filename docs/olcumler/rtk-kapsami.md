# RTK kapsamı (21a K4)

`rtk gain`: 5338 komut, %76.6 tasarruf (3.6M token). `rtk discover --since 3`: 6590 Bash komutunun %29.7'si RTK'dan geçiyor; RTK'nın zaten desteklediği ama kaçırılan komutlar ~96k token (tail -c, grep -n, gh api, git …).

## Bash çıktısı en büyük 10 komut (son 3 gün, transcript tool_result, ~bayt/4)
| # | komut | çağrı | ~token | RTK |
|---|---|---|---|---|
| 1 | cat | 197 | 173.842 | hook ile rtk read |
| 2 | sed | 187 | 151.514 | yok (sed -n dilimi zaten dar) |
| 3 | grep | 328 | 93.565 | hook ile rtk grep |
| 4 | rtk proxy | 125 | 90.733 | bilerek süzülmez |
| 5 | echo | 143 | 74.238 | birleşik komutların çıktısı |
| 6 | ls | 192 | 50.184 | hook ile rtk ls |
| 7 | cd … && sed -n | 37 | 37.709 | yok |
| 8 | graphify | 34 | 37.394 | **yok → öneri (bekleyen/rtk-kural.md)** |
| 9 | python - (heredoc) | 162 | 34.917 | yok (tek seferlik analiz) |
| 10 | cd … && rtk proxy | 38 | 24.916 | bilerek süzülmez |

Süzülmeyen repo komutu: `node araclar/suit.mjs` / `npm test` (cc-kopru, 187 satır, discover "unhandled" 137× node). Kural `.rtk/filters.toml` cc-kopru-suit: yalnız `✔` ile başlayan satırlar ve boş satırlar süzülüyor.

## Önce/sonra (tests/fixture/rtk)
- cc-kopru-suit.txt: 187 → 16 satır (ℹ özet + ✔ ile başlamayan satırlar); karakterde %89 azalma.
- cc-kopru-suit-kirmizi.txt: 190 → 20 satır, %88 azalma; ✖ satırı, AssertionError ve yığın satırı, ℹ fail korunuyor.
- Mutasyon: `(?i)error` deseni eklenince test kırmızıya döndü, sonra geri alındı.

## M3a K0d ek ölçüm (2026-09-29)

Yöntem aynı: `rtk discover --since 3` (kapsam) · graphify çıktısı bayt (ham `graphify query` ↔ `rtk graphify query`).

- **Kapsam önce**: 513 komut RTK'dan geçiyor, **%26,9** (3 gün penceresi; önceki ölçüm %29,7). Kaçan 187 komut ~50,4K token.
- **`rtk trust -y`** (omer-skills): `.rtk/filters.toml` etkin; `rtk verify` 156/156.
- **Yeni filtre `graphify-sorgu`** (`graphify query|path|explain`): yalnız ` community=…` meta alanı ve boş satırlar süzülür.
  - Örnek sorgu "kapat kuyruk akil parti": **6577 → 5477 bayt (−%16,7)**. 5477'nin ~250 baytı aşağıdaki rtk uyarısı (stderr), filtrenin kendi etkisi ≈ −%20.
  - Bilgi kaybı kontrolü: NODE/EDGE ad kümesi önce/sonra **eşit (68/68)**; src ve loc korunur.
- **Bulgu**: rtk, mevcut `cc-kopru-suit` filtresini yok sayıyor ("match_command '(^|&&\s*)…' top-level branch does not start with '^' → Filter ignored"). Filtre trust'tan sonra da etkisiz. Düzeltmesi ayrı iş (bu dalgada dokunulmadı). İlk `graphify-sorgu` taslağı aynı nedenle etkisizdi, `^graphify…` ile düzeltildi.
- **Kapsam sonra**: aşağıdaki satır. discover geçmiş komutları sayar; trust/filtre kapsamı hemen değiştirmez. Kapsamı artıran şey hook'un komutu `rtk …`'ya yeniden yazmasıdır; graphify hook yeniden yazım listesinde değilse filtre yalnız `rtk graphify …` çağrısında devreye girer.
- Kapsam sonra (aynı pencere, trust + filtre sonrası): Already using RTK: 516 commands (27.0%)
