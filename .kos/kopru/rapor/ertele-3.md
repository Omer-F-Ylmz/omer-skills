---
type: summary
status: active
tags: [ertele-3, gizli-ajan, ajan-getir, katalog, context-dokum]
relatedTo: [ertele-2, ertele-1]
---
# TUR 3 (kanıt tmp/ertele8/, kod kanıtı rapor/ertele-3-rea.md)
- Açılış gerçek API (bas.py, haiku, kancalı, sırayla): A 175,7k · S0 `deny:["Skill"]` 107,9k (−67,8k) · S Skill+141 ajan reddi 89,0k. İlk basamak ≤150k TUTTU; ≤60k TUTMADI. Her oturum 337–419 sn (madde 5 açık).
- Canlı (S + ertele_istem, haiku): katalog→`tam` writing-commit-messages ✓ ($0,12) · `/departman-surec-plan` Skill reddiyle de açılıyor ✓. Gizli ajan geri çağırma 29/30 (tarif.jsonl; kaçak ecc:vue-reviewer), skill 20/20 (tur 2, katalog değişmedi). 30 yeni SKILL tarifi ve 10 canlı skill seçimi ÖLÇÜLMEDİ (tur bütçesi).
- Karar Ömer'e: `deny:["Skill"]` Skill aracını kapatır (skill'e erişim katalog `tam` + /komut ile kalır) — kural 21–24 açısından onay gerekir; ~/.claude'a uygulanmadı. Açık: madde 3 kopya, 5 (120 sn), MCP talimatı ertelemesi kodda yok (rea md madde 5).
# ERTELE-3 TUR 1 (kanıt tmp/ertele7/)
- Döküm (/context, context-A.txt; gerçek API ~192k, fark kanca ekleri): Skills 52,4k (5752 satır: User 2375 ≈23,8k · sync ≈6k · ecc 3,8k · kalan plugin adları) · Custom agents 32,1k (ecc 6,2k, octo 4,3k, claude-ads 2,2k) · MCP talimat 16,2k · bellek 9,1k (global CLAUDE.md 5,2k) · sistem 2,2k.
- Kopya (kopya.py, sha256): 376 grupta 407 fazla dosya; listede aynı kısa ad çok kaynaktan 447 satır (≈4–5k) — en çok sync+user 30, core-skills+hyperframes 34, n8n plugin+user 13.
- Gizli 141 ajan: katalogda 141/141, yol geçerli 141/141 (gizli.json).
- GERİ ÇAĞIRMA ÖNCE: 30 Türkçe kör tarif (haiku, tarif.jsonl) → ertele_katalog ara 2/30, BM25 top-8 0/30. Katalog satırı İngilizce → gizli ajan Türkçe işten fiilen bulunamıyordu (erişilemezlik).
- DÜZELTME: skills/ajan-getir/ne_zaman.tsv (141 gizli ajana Türkçe anahtar, haiku) → ajan_katalog.py + ertele_katalog.py satıra ekliyor; katalog 296→586 satır (düşen 21'in dosyası yok). Geri çağırma 30 kör tarifte: ertele ara 2→18/30, BM25 top-8 0→23/30, birleşik 24/30 (%80). KAPI (≥%98) TUTMADI.
- Yapılmadı (oturum çağrı sınırı): 10 gizli ajan canlı koşu, açıklama yeniden yazımı + 3 tekrar seçim testi, ≤150k kapısı. ~/.claude ve settings.json değişmedi; gizlilikten çıkarma listesi hazırlanmadı.
- TUR 2: ara alt-dizi sayımı → kök BM25 (eski 30: ara 18→22) + 141 ajana gündelik Türkçe ifade (haiku, test tariflerini görmeden; yedek ne_zaman.yedek-tur2.tsv) → eski 30: 29/30, görülmemiş 30 (tarif2, kesişim 0): 30/30 → 59/60 %98,3 TUTTU (kaçak ecc:vue-reviewer). Skill bulma ara_recall 20/20 korundu. Canlı (ajan-getir yolu tam→tanım→general-purpose haiku, 10 rastgele seed 29): 10/10, adımlar tanıma özgü (canli workflow wf_89f19ef8-dcd; paralel koştu, sapma).
- Açık: claude -p alt süreç bu ortamda 120 sn'de çıktı vermiyor (nedeni ölçülemedi) → açıklama yeniden yazımı + 3 tekrar haiku/sonnet seçim testi ve ≤150k kapısı ölçülemedi; gizlilikten çıkarılacak ajan yok (%98 tuttu). ~/.claude değişmedi.
