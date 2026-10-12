# ROUTER-1 ölçüm (12 Eki 19:31–19:40, olcum_sira, 12 çağrı + 1 duman)

`tools/olcum/router1_olc.py` · ham: olcum.tsv · A = düz `claude -p --model sonnet` (kullanıcı ayarları, MCP'ler dahil) · B = `model_sec.bayraklar(sınıf)` (aynı model).

| Kol | Doğru | Bağlam jetonu (girdi+cache) | USD | Süre |
|---|---|---|---|---|
| A | 6/6 | 478.704 (~79.8k/çağrı) | 1.751 | 163 sn |
| B | 6/6 | 19.433 (~3.2k/çağrı) | 0.053 | 30 sn |

KABUL ölçütü (tasarim.md): B doğruluk ≥ A ✔ · B bağlam ≤ A'nın %50'si ✔ (%4.1). Bağlam −%96, USD −%97, süre −%81.
Sınır: görevler kısa ve iki kol da tavanda (6/6) — kalite *korundu*, *artış* gösterilmedi; geri düşüş (kademe+1) tetiklenmedi.
Zor görevlerde effort high/xhigh'ın kalite katkısı ayrı ölçülmeli (ROUTER-2 adayı).
