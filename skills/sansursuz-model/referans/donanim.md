# Donanım

BF16 ≈2 GB/milyar, 4-bit ≈0,55 GB/milyar + %10–20.

| VRAM | Abliteration | Çıkarım |
|---|---|---|
| 12 GB | ≤3B BF16 / ≤14B 4-bit | ≤14B; 35B-A3B yalnız hazır GGUF, CPU |
| 24 GB | ≤9B BF16 / ≤30B 4-bit | ≤30B |
| 48 GB | ≤20B BF16 / ≤70B 4-bit | ≤70B Q4 |
| bulut | 120B–400B | Q4 karışık |

Bu PC (4070 Ti 12 GB, 32 GB, i7-14700K, 7 MB/s): 35B yerelde üretilemez, hazır heretic kullan. 4B ve altı tam akış. MoE'de `--n-cpu-moe` ile uzmanları RAM'de tut, `-ngl` ile dikkat katmanlarını GPU'ya al.
