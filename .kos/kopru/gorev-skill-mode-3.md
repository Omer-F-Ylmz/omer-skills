# SKILL-MODE-3 — her_sey_ara'yı katalog_ara / zorunlu_arac'a bağla

Girdi: .kos/kopru/skill-mode/ (her_sey_ara.py `Arayici.karma(q, n, en)` + `etiketle(etiket.json)`; sorgu_cevir.cevir; etiket.json; yetenek-tam.jsonl). Kapı SKILL-MODE-2'de geçti (ayar %99.4 / test %100 @80).

1. tools/katalog_ara.py ve .kos/kopru/zorunlu_arac.py: sorguyu sorgu_cevir.cevir ile İngilizceye çevir (ücretsiz havuz; önbellek sorgu-cevir.json; çeviri kosinüsü <0.5 ise tekrar çevir — cevir_duzelt.py mantığı, yoksa %17 çeviri kayar), Arayici.karma ile ara. Havuz kapalıysa çevirisiz karma (bm25+yogun+soz3) düş.
2. etiket.json + yetenek-tam.jsonl + vek.npy/bm25.pkl canlı katalogla eşitle (yeni kayıt → etiket_uret.py yalnız eksikler).
3. Doğrulama: ram-bekci-test-1 sorgusunda DENETİM blender-uretim/comfyui istememeli; olc3.py ölçümü ≥%98 kalmalı.
4. Kısıt: dosya silinmez; RAM ≤%89; python -E; push yok.
