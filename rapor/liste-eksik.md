---
type: rapor
status: kismen
tags: [liste-eksik, video-tarama]
relatedTo: [ana-liste]
---
# LISTE-EKSIK

- Hedef: 885 tekil video (derin+derin-2+derin-3 − ana-liste kaynakları). Yedek: `_arsiv/liste-eksik-1/`.
- Kök neden 1: `llm-e.jsonl` (791 video) hiç birleştirilmemişti; `tools/liste_birlestir.py` girdilerine `llm-e`, `llm-f` eklendi.
- Kök neden 2: birleştirici `kaynak_video_idleri` sütununu 400 karaktere kesiyordu (kaynak kaybı); kesme kaldırıldı.
- Sonuç: ana-liste.tsv 17372 → 24140 → (kesmesiz) kalem; 885'in 853'ü kalemli, 32'si gerekçeli (`docs/video-tarama/liste-eksik-gerekce.txt`). 853+32 = 885 (%100).
- 11 videoya ücretsiz havuz + haiku ile yeniden çıkarım (llm-f.jsonl); 32 video iki turda kalem döndürmedi (çoğu konuşma 0 karakter, 4'ünün metni var: DfOnUkLCMZW, GKM1pHYY7F8, GRJaKcXZS94, w86c1q59QKU — elle bakılmadı).
- Kapı 2 (30 rastgele kalem, tam ad eşleşmesi): 26/30 = %86,7 → %98 ŞARTI TUTMADI. Kaçanlar: claude -p, URLSessionConfiguration, Code Vein, Open Git Source Control (LLM yazımı videodaki metinle birebir değil).
- Yapılmadı: yeni kalemler için `ana-liste-ozellik.tsv` + `yapilis/*.md` (liste_ozellik.py, ~6,8 bin kalem Haiku; sayısal tavan/onay yok) ve liste_bizde/kurulum sınıflaması.
- Silme/push yok; commit yok.
