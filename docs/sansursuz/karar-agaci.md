---
type: plan
status: draft
tags: [sansursuz, heretic, karar-agaci, gguf]
relatedTo: [arastirma, tersine]
---
# Model-bağımsız karar ağacı: yeni model geldiğinde ret kaldırma

Kaynak: arastirma-a.md, arastirma-b.md, tersine.md. Yalnız yerel/kendi kullanım. Eşikler SANSURSUZ-2 hedefidir (ret ≤%1 ölçüm payıyla %0, KL ≤0,01, kalite kaybı ≤1 puan); Heretic README'de Gemma-3-12B için gerçekçi sonuç ret 3/100, KL 0,16, yani KL ≤0,01 çoğu modelde sert kapıdır, sağlanamazsa "KL ≤0,2 + kalite ≤1 puan" ikinci kapı olarak yazılır.

## Adımlar
1. **Hazır heretic var mı?** HF'de `<model> heretic` ara (tersine.md örnekleri: Qwen3.5-0.8B/2B/4B ve Qwen3.6-35B-A3B için birden çok yayıncı var). Varsa → 5. Yoksa → 2.
2. **Heretic'i çalıştır** (AGPL-3.0, dağıtmadan kendi kullanım). Donanım uygunsa yerel (tablo), değilse ücretsiz bulut GPU (Modal/Kaggle/Colab; kota ve oturum süresi sınırı var). 100–200 deneme (30–60 rastgele başlangıç), hedef (ret, KL) Pareto'sundan en düşük ret ∧ KL ≤ kapı olanı seç. **Kapı A:** ret ≤%1–3 (100 kötü istem, ≥2 yargıç).
3. **Tek yön yetmedi mi?** (ret >%5 ya da düşünme izinde ret) → Heretic v2 ARA (rank ≤50) veya çok yönlü/alt uzay (arastirma-b Bölüm 1). Reasoning modelde düşünme izini ve son cevabı ayrı say.
4. **MoE ise:** her uzmanın down-proj'u düzenlenmeli, router'a dokunulduğu bildirilmemiş (Heretic kaynak okuması; tersine.md 35B router ölçümü tamamlanmadı). Bellek yetmiyorsa katman-katman yükleme ya da bulut.
5. **GGUF'a çevir** (llama.cpp convert + Q4_K_S/Q4_K_M/Q8_0). **Kapı B:** aynı test setini GGUF'ta yinele (kuantizasyon reddi geri getirebilir); ret farkı >%1 ise bir üst kuant.
6. **Çalışma anı yedeği:** kontrol vektörü (llama.cpp `--control-vector`) → prefill → sistem istemi; yalnız Kapı A/B sonrası kalan açık için.
7. **Ret yakalayıcı:** çıktıda ret işaretleri (marker listesi + küçük sınıflayıcı) tetiklenirse otomatik yeniden dene (prefill'li); ret sayacı `claude -p` görevlerinde izlenir.
8. **Kalite kapısı C:** MMLU/GSM8K tarzı ≥3 kıyas + 10 araçlı görev; kayıp ≤1 puan. Referans: Qwen3.6-35B-A3B heretic MMLU 83,39 vs 83,71, ret 10/100, KL 0,0015 (model kartı, SANSURSUZ-1 notu).

## Donanım tablosu (HESAP, ölçülmedi: BF16 ≈2 GB/milyar param, 4-bit ≈0,55 GB/milyar + %10–20 pay)
| VRAM | RAM | Heretic'i yerelde çalıştır | Çıkarım (GGUF Q4) |
|---|---|---|---|
| 12 GB | 32 GB | ≤~3B BF16 ya da ≤~14B 4-bit (bnb); 35B+ yok → bulut | ≤14B tam VRAM; 35B-A3B MoE: uzmanlar RAM'de (Q4_K_S dosya 19,5 GB ölçüldü), ≥32 GB RAM |
| 24 GB | 64 GB | ≤~9B BF16 ya da ≤~30B 4-bit | ≤30B tam; 35B-A3B rahat |
| 48 GB | 128 GB | ≤~20B BF16 ya da ≤~70B 4-bit; 35B-A3B 4-bit | ≤70B Q4 |
| ≥80 GB / bulut | 128 GB+ | 120B–400B: bulut (Modal/Kaggle ücretsiz katman yetmez, 400B için çok GPU) | 120B+ Q4 CPU+GPU karışık |

Bu PC (RTX 4070 Ti 12 GB, 80 GB civarı RAM belirtilmedi): 35B-A3B heretic yalnız hazır GGUF olarak çalışır, yerelde üretilemez (SANSURSUZ-1 ile uyumlu).

## Açık riskler
- Ret oranı ölçümü yargıç ve istem setine bağlı; tek set ile "%0" iddia edilmez.
- Yeni mimariler (hibrit doğrusal-dikkat + MoE, MTP katmanları) araç desteğini geciktirebilir; tersine.md'de Qwen3.5/3.6 için hangi matrislerin değiştiği ölçüldü.
- Savunmalı (Extended Refusal/AMRA tipi) modellerde tek yön çıkarma çalışmayabilir (arastirma-b 1.2).
