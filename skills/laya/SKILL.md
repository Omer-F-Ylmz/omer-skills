---
name: laya
description: Yerel Laya (421M, ~10 ms) ince ayarlı karar modeli — görev metninden haiku|sonnet|opus seçimi, iş türü ve video konu sınıflaması. Model/efor seçerken ya da laya ince ayar/ölçüm istenince kullan.
---

# Laya yerel karar

- Karar: `python tools/laya_karar.py "<görev metni>"` → `{model, guven}`; çıkış 3 = ck/venv yok. `tools/yonlendir.py` `LAYA_YONLENDIR=1` ile guven ≥0,8 ise LLM çağrısı yapmaz (haiku→T1, sonnet→T3, opus→T4); bayrak yoksa davranış değişmez.
- Veri: `python tools/laya/veri_uret.py` (ajan-sira.tsv/log/json, ig-41/ig-42 tsv → `tools/laya/veri/{model,tur,konu}_{train,test}.csv`); etiket denetimi `dogrula.py`, düzeltme `etiket_haiku.py`.
- Eğit/ölç (venv python): `siniflandir.py egit <model|tur|konu> <bas|tam> [epoch]` · `siniflandir.py olc <ad> [ck-adı|sifir]`. ck `tools/laya/ck/` (git dışı, ~1,7 GB; yeniden üret).
- Kurulum: `tools/laya/.venv` (uv, torch cu126, laya 0.4.13), kaynak `tools/laya/src` (Apache-2.0).
