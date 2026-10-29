---
type: summary
status: active
tags: [ertele-3, gizli-ajan, ajan-getir, katalog, context-dokum]
relatedTo: [ertele-2, ertele-1]
---
# ERTELE-3 TUR 1 (kanıt tmp/ertele7/)
- Döküm (/context, context-A.txt; gerçek API ~192k, fark kanca ekleri): Skills 52,4k (5752 satır: User 2375 ≈23,8k · sync ≈6k · ecc 3,8k · kalan plugin adları) · Custom agents 32,1k (ecc 6,2k, octo 4,3k, claude-ads 2,2k) · MCP talimat 16,2k · bellek 9,1k (global CLAUDE.md 5,2k) · sistem 2,2k.
- Kopya (kopya.py, sha256): 376 grupta 407 fazla dosya; listede aynı kısa ad çok kaynaktan 447 satır (≈4–5k) — en çok sync+user 30, core-skills+hyperframes 34, n8n plugin+user 13.
- Gizli 141 ajan: katalogda 141/141, yol geçerli 141/141 (gizli.json).
- GERİ ÇAĞIRMA ÖNCE: 30 Türkçe kör tarif (haiku, tarif.jsonl) → ertele_katalog ara 2/30, BM25 top-8 0/30. Katalog satırı İngilizce → gizli ajan Türkçe işten fiilen bulunamıyordu (erişilemezlik).
- DÜZELTME: skills/ajan-getir/ne_zaman.tsv (141 gizli ajana Türkçe anahtar, haiku) → ajan_katalog.py + ertele_katalog.py satıra ekliyor; katalog 296→586 satır (düşen 21'in dosyası yok). Geri çağırma 30 kör tarifte: ertele ara 2→18/30, BM25 top-8 0→23/30, birleşik 24/30 (%80). KAPI (≥%98) TUTMADI.
- Yapılmadı (oturum çağrı sınırı): 10 gizli ajan canlı koşu, açıklama yeniden yazımı + 3 tekrar seçim testi, ≤150k kapısı. ~/.claude ve settings.json değişmedi; gizlilikten çıkarma listesi hazırlanmadı.
- Sonraki: kalan 6 kaçan tarif için anahtar onarımı + ara'ya BM25 birleştirme, sonra canlı 10/10.
