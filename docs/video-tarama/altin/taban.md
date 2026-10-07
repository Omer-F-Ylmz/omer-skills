# Altın taban: 5 video tarama raporu puanı

Kaynak: C:\Projeler\.tmp-video\altin\<id>\ ham dump'ları (aciklama, altyazi, groq, ocr, yorum); altın JSON'lar `docs/video-tarama/altin/<id>.json`, puan `video altin puan` (rapor: `docs/video-tarama/2026-10-07-<id>.md`), LLM/API çağrısı yok.

| id | aday yakalama | isabet | ad yazım | komut | url | iş akışı | link açıklama | link yorum | site_ui |
|---|---|---|---|---|---|---|---|---|---|
| aZe5ZTYcF1M | 2/3 | 2/2 | 1/2 | 0/0 | 0/1 | 0/3 | 1/1 (sınıf 0/1) | 1/1 (sınıf 0/1) | 1/4 |
| 1nGx7WR8YLE | 4/11 | 4/11 | 2/4 | 0/0 | 0/2 | 0/6 | 1/1 (sınıf 0/1) | 1/1 (sınıf 1/1) | 0/3 |
| YDAK1lvVXho | 2/9 | 2/12 | 0/2 | 0/0 | 0/1 | 0/3 | 1/1 (sınıf 1/1) | 0/0 | 1/6 |
| FaChtkkG9X4 | 2/5 | 2/8 | 1/2 | 1/1 | 0/4 | 0/6 | 4/4 (sınıf 4/4) | 0/0 | 1/2 |
| d_UE-wHLoZY | 3/5 | 3/4 | 2/3 | 0/0 | 0/1 | 0/6 | 0/0 | 0/1 (sınıf 0/0) | 0/1 |

url ve iş akışı sütunları rapor şemasında karşılığı olmayan alanlar (ALAN_YOK), bu yüzden 0 çıkar.

Notlar: YDAK1lvVXho altınında `"not": "editör yok"` (≥2 dk gerçek editör/terminal görüntüsü yok; Astra/Claude sohbet arayüzü ve site gösterimi). Diğer dördünde not genel taslak notu. FaChtkkG9X4 ocr.txt ve yorum.txt çalışma sırasında tamamlandı, altın OCR ile de güncellendi.

## Kaçan adaylar

- aZe5ZTYcF1M: Three.js (kütüphane)
- 1nGx7WR8YLE: Seedance 2.5 (model), Fable (model), design-dna (skill), frontend-design (skill), design-taste-frontend (skill), scrollcraft (skill), ffmpeg (araç)
- YDAK1lvVXho: Three.js (kütüphane), GSAP (kütüphane), ScrollTrigger (kütüphane), design-dna (skill), scrollcraft (skill), frontend-design (skill), design-taste-frontend (skill)
- FaChtkkG9X4: Claude Design (uygulama), Figma (uygulama), ChatGPT (uygulama)
- d_UE-wHLoZY: GPT Image 2 (model), Nano Banana (model)
