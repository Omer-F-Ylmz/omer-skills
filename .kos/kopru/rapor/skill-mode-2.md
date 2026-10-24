SKILL-MODE-2 · her_sey_ara doğruluğu (@80, skill bazında, %80 ayar / %20 ayrılmış test)
- Taban (karma+en, çeviri 600/600): ayar %98.1 · test %95.8
- Kök neden: sorgu-cevir.json'da 105/600 çeviri hizası kaymış (EN yeniden yazım başka sorgunun); cevir_duzelt.py (kosinüs<0.5 → 8'lik paket, doğrulamalı) → 2 kaldı. Tek başına: ayar %98.8 · test %100
- M3 üçüncü kol soz3 (ad×2/etiket×1/açıklama×1, etiket.json 7002 kayıt ücretsiz havuzla): ayar %99.4 · test %100 (@20 %96.7/%99.2)
- Kapı (≥%98 ikisi de): GEÇTİ. Ayar kümesine uydurma yok: test yalnız ölçümde görüldü; düzeltme genel hata (çeviri hizası)
- hsa_deney (mpnet) koşulmadı: gerek kalmadı
- Sonraki: gorev-skill-mode-3.md (katalog_ara/zorunlu_arac bağlama). PLAN.md Faz 1 KAPANDI.
- Uyarı: gitleaks etiket.json'da 1 generic-api-key (anahtar sözcüğü etiketi, yanlış pozitif; sır değil). semgrep: yalnız pickle (kendi önbelleğimiz).
- $ claude ≈1.5 / ücretsiz çağrı ≈650 paket
