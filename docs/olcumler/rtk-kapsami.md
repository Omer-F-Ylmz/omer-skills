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
