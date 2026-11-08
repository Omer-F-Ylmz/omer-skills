# Ölçülen imza

Qwen3.5-0.8B vs heretic, 473 ortak tensör: down_proj 20/24 değişmiş, göreli fark 2,96e-2, ilk tekil enerji 0,997, rank 3. out_proj 14/18, 4,27e-2, 0,998. o_proj 5/6, 4,11e-2, 0,998.

- Fark **rank-1** (enerji ≥%99,7).
- Yön **tek global**: 39 tensör arası ort |cos| 0,993 (min 0,966).
- Kısmi silme: `uᵀW` ≈%64 azalmış; güç 0,61→0,79 (katman 4→14), sonra 0,70–0,73.
- **Katman 0–3 değişmemiş.** embed, q/k/v, gate/up yok. Norm koruması yok.

35B MoE: `blk.19.attn_output` güçlü silme (oran 0,37), router (`ffn_gate_inp`) ve `attn_qkv` dokunulmamış.

`abliterate.py` varsayılanları buradan: yazıcı matrisler, tek yön, 4'ten sonra, 0,3–1,2, tepe 0,85.
