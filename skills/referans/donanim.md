# Donanım / nerede koşulur

Hesap: BF16 ≈2 GB/milyar, 4-bit ≈0,55 GB/milyar + %10–20 pay. Ölçülmedi, hesap.

| VRAM | RAM | Abliteration | Çıkarım (Q4) |
|---|---|---|---|
| 12 GB | 32 GB | ≤3B BF16 / ≤14B bnb-4bit; 35B+ → bulut | ≤14B tam; 35B-A3B MoE uzmanlar RAM'de (Q4_K_S 19,5 GB), ≥32 GB RAM |
| 24 GB | 64 GB | ≤9B BF16 / ≤30B 4-bit | ≤30B tam |
| 48 GB | 128 GB | ≤20B BF16 / ≤70B 4-bit | ≤70B Q4 |
| bulut | — | 120B–400B (Modal/Kaggle, kota) | Q4 CPU+GPU karışık |

Bu PC (4070 Ti 12 GB, 32 GB RAM, i7-14700K, ~7 MB/s ağ): 35B-A3B yalnız hazır GGUF olarak çalışır, yerelde üretilemez → hazır heretic tercih kuralı. 4B ve altı yerelde tam akış. İndirme bütçesi: 4B çifti ≈15 GB ≈ 40 dk.

Bellek ölçümü: `torch.cuda.max_memory_allocated()`, `psutil.virtual_memory()`. %95 aşılırsa batch küçült, sonra katman katman, sonra bulut.
