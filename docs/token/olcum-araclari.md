# Ölçüm araçları — bugün yan yana (10 Eki 2026, TOKEN-7a 3a)

| araç | pencere | girdi | çıktı | cache okuma | not |
|---|---|---|---|---|---|
| `claude-usage today` (1.5.5, `scan` sonrası) | takvim günü, yerel | 2.48M | 975.1K | 95.75M | 1110 tur · 103 oturum · $97.91 (sonnet-5-5 $89.45) |
| `python tools/token_olc.py olc --gun 1` | son 24 saat, tüm projeler | 3.31M | 28.71M | 155.28M | 3169 istek · cache yazma 5m 52.97M / 1h 2.61M · 695 istek fiyatsız |

Fark nedeni: pencere (takvim günü / 24 saat) ve kapsam (token_olc alt ajan + tüm projeler jsonl'lerini sayar). Çıktı farkı 7b'de kalibre edilecek. claude-usage köprüden: `cc-kopru komut claude-usage today|week|stats|--version`.
