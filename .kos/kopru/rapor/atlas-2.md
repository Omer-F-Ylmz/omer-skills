# ATLAS-2 d1 rapor (14 Eki)

- Kart: K1 121 + K2 292 (+3 ek: lighthouse-chrome-devtools, qa-erisilebilirlik-testi, erisilebilirlik-paket) → kart.jsonl 595, başarısız 0 (ucuz model, 25 çağrı).
- Opus kararı `.claude/atlas2/karar.py` (ATLAS-1 kararları korunur): V17 · G350 · K18 (K = claude-ads:audit-* 17 + video-tarayici-haiku). katalog_yenile koşuldu.
- Kitaplar: docs/atlas/video-icerik.md (0. ayrım satırı izle/tara/uygula/üret), docs/atlas/guvenlik-test.md (A1–A7 kapanış sırası; osv-scanner/knip kurulu değil → npm audit + npx knip).
- Atıf: departman-guvenlik, departman-test-qa, departman-arastirma-ogrenme (departman-video yok) — tek satır.
- Ölçüm (claude -p 3/3): taban K1/K2 10/11 (S41 → video-uygula kaçışı). Kitaplı tek koşu 18/18: site/3D alt küme 7/7 (ATLAS-1 12/14, kaçan S01 scroll-driven satır düzeltmesiyle), K1/K2 11/11 (+1, S41). Tekrar 1; n küçük, S41 düzelmesinin kitaptan mı atıf satırından mı geldiği transkriptten ayrılmadı.
- Kullanım izi: .kos/kopru/atlas_iz.py <kitap> [--gun N] (salt-okur, test 1). Kitap öncesi taban (son 3 gün): video-icerik 300 oturum (en çok `video` — genel sözcük, gürültülü), guvenlik-test 97 (gitleaks 71, semgrep 35). Sayım VİDEO-KISA / TELVE-R2f sonrası tekrar.
- Kalan: dist zip (claude.ai; departman skill'leri değişti), K3 belge-sunum (zaman kalmadı).
