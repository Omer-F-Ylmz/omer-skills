---
type: analysis
status: partial
tags: [sansursuz, tersine, heretic, safetensors, gguf, svd]
relatedTo: [arastirma, karar-agaci]
---
# Tersine mühendislik: heretic ağırlıkları tensör tensör (3 Kas 2026)

Araçlar: `tools/sansursuz_tersine.py` (+ `_ozet.py`: iki safetensors klasörü, fark normu, SVD rank, yön benzerliği), `tools/sansursuz_gguf_diff.py` (HF'den HTTP Range ile tensör tensör GGUF farkı, 38 GB inmez). Ham çıktı: `tmp/ss3_t08.json`.

## 1. Qwen3.5-0.8B (Qwen/Qwen3.5-0.8B vs saidutta69/Qwen3.5-0.8B-heretic), ÖLÇÜLDÜ
473 ortak tensör; yalnız orijinalde 15 (MTP: `mtp.*`; heretic'te düşmüş). `embed_tokens` ve görsel kule farkı 0.

| Matris | tensör | değişen | göreli fark | 1. tekil değer enerjisi | rank (>%1) | katmanlar |
|---|---|---|---|---|---|---|
| `mlp.down_proj` | 24 | 20 | 2,96e-2 | 0,997 | 3 | 4–23 |
| `linear_attn.out_proj` | 18 | 14 | 4,27e-2 | 0,998 | 2 | 5–22 |
| `self_attn.o_proj` | 6 | 5 | 4,11e-2 | 0,998 | 2 | 7–23 |
| `linear_attn.norm.weight` | 18 | 18 | 1,8e-3 | – | – | 0–22 (küçük; bf16 yeniden kayıt gürültüsü olabilir, doğrulanmadı) |

Yorum:
- Fark matrisi **rank-1** (enerji ≥%99,7; kalan rank 2–3 bf16 yuvarlama): tek yön ortogonalleştirme `W' = W − w·r rᵀW`, LoRA rank-1 birleştirilmiş (arastirma-a Heretic: LoRA rank 1).
- **Yön tek ve global:** 39 rank-1 tensörün sol tekil vektörleri arasında ortalama |cos| = 0,993 (min 0,966) → tüm katmanlarda aynı `r`.
- **Kısmi silme:** `uᵀW` orijinaline göre yalnız ≈%64 azalmış (medyan oran 0,33); katman bazlı silme gücü `1−uᵀW'/uᵀW`: down_proj 0,61→0,79 (katman 4→14 artan, sonra ≈0,70–0,73), out_proj/o_proj 0,45–0,76. Keskin tepe yok, düz-geniş çekirdek; **katman 0–3 hiç değişmemiş**.
- **Norm koruması yok (ya da ihmal edilebilir):** sütun/satır norm oranı 0,9993–0,9995 (grimjim'in norm-koruyan sürümünden farklı; tam ortogonalleştirmenin beklenen küçük çekilmesi).
- Düzenlenen matrisler = yalnız "yazan" matrisler (kalıntıya yazan o_proj/out_proj/down_proj); `q/k/v`, `gate/up`, embed değişmemiş.

## 2. Qwen3.5-4B ikili (orijinal vs saidutta69 / huihui-ai), ÖLÇÜLEMEDİ
Neden: bütçe (60 tur) ve indirme hızı (~7 MB/s; orijinal 5,7/9,3 GB iken durduruldu). Betik hazır: `sansursuz_tersine.py <orijinal> <heretic> <json>`; indirme `tmp/ss3_indir.py` arka planda sürüyor (`.kos/kopru/arka/sansursuz-3-ilerleme.md`). huihui-ai (klasik abliteration) ile karşılaştırma bu yüzden yok.

## 3. Qwen3.6-35B-A3B heretic (MoE, GGUF Q8_0: unsloth MTP vs llmfan46 heretic), KISMİ
Mimari (başlıktan ölçüldü): `qwen35moe`, 41 blok (40 + MTP), 256 uzman, 30 katman doğrusal-dikkat (`ssm_out`) + 10 tam dikkat (`attn_output`), paylaşılan uzman (`ffn_down_shexp`) + yönlendirilmiş uzmanlar (`ffn_down_exps` [512×2048×256]), router `ffn_gate_inp` F32. Yerel dosya: Q4_K_S 19,5 GB (Masaüstü/Yerel Sansursuz Model).
- İlk sonuç: `blk.0.ssm_out.weight` fark 0,0 (katman 0 dokunulmamış, 0.8B bulgusuyla tutarlı).
- Uzman tensörleri, router ve diğer katmanların farkı: iş arka planda sürüyor (`tmp/ss3_gguf35.txt`, bitince `tmp/ss3_gguf35.json`); bu belgeye işlenmedi. **Router'ın değişip değişmediği ve uzman başına rank-1 yapısı ölçülmedi.**

## Sonuç (SANSURSUZ-2 için)
Heretic çıktısı = az sayıda yazıcı matriste rank-1, tek global yön, kısmi güç (~0,5–0,8), ilk 4 katman hariç. Arama uzayı (tek yön + katman çekirdeği) küçük; hızlı denemeler 0.8B/2B'de yapılabilir.
