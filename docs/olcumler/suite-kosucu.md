# suite-kosucu (21a K2)

Kümülatif token = istek başına input + cache_creation + cache_read + output toplamı (transcript usage).

| koşu | ajan | süre | araç çağrısı | kümülatif token |
|---|---|---|---|---|
| 19b-dönemi (00ca9a44) | general-purpose | 1701 s | 45 | 10.307.723 |
| 3f47de6f | general-purpose | 217 s | 22 | 3.558.945 |
| 3d3f21d7 | general-purpose | 168 s | 17 | 2.644.560 |
| 20b-devam (24a39bf9) | general-purpose | 98 s | 7 | 187.092 |
| **21a (655de819)** | **suite-kosucu** | **103 s** (claude -p toplam 137 s) | **7** | **168.629** |

Sonuç: video 248 · jev 81 · kök 50 · cc-kopru 171 · mcp/jev 40 · dotnet 22 = 612/612, kırmızı yok. Dönüş 6 satır. claude -p maliyeti $0.83.
En iyi general-purpose koşusuna göre %10 daha az token. Ortalamaya göre (4.2M) ~25 kat, en kötüye göre ~61 kat daha az. Asıl kazanç varyansın gitmesi: komut keşfi, arka plan, Monitor ve yeniden koşma yok.
