# Ölçülen heretic imzası (referans hedef)

Qwen3.5-0.8B orijinal vs saidutta69 heretic, 473 ortak tensör, tensör tensör:

| Matris | değişen | göreli fark | 1. tekil enerji | rank (>%1) |
|---|---|---|---|---|
| mlp.down_proj | 20/24 | 2,96e-2 | 0,997 | 3 |
| linear_attn.out_proj | 14/18 | 4,27e-2 | 0,998 | 2 |
| self_attn.o_proj | 5/6 | 4,11e-2 | 0,998 | 2 |

- Fark matrisi **rank-1** (enerji ≥%99,7; kalan bf16 gürültüsü).
- Yön **tek ve global**: 39 rank-1 tensörün sol tekil vektörleri arası ort |cos| 0,993 (min 0,966).
- Kısmi silme: `uᵀW` yalnız ≈%64 azalmış; silme gücü down_proj 0,61→0,79 (katman 4→14), sonra 0,70–0,73. Düz-geniş çekirdek, keskin tepe yok.
- **Katman 0–3 hiç değişmemiş.** embed, q/k/v, gate/up değişmemiş.
- Norm koruması yok (0,9993–0,9995).

35B-A3B MoE GGUF (Q8_0): `blk.0.ssm_out` fark 0; `blk.19.attn_output` enerji_ilk1 0,93, `uW_yeni/uW_orij` 0,37 (güçlü silme); `blk.20.ffn_gate_inp` ve `attn_qkv` 0 (router dokunulmamış).

Bu imza `abliterate.py` varsayılanlarının kaynağıdır: yazıcı matrisler, tek yön, 4. katmandan sonra, 0,3–1,2 rampa, tepe 0,85.
