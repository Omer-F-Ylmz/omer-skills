# Altın taban: 5 video tarama raporu puanı

Kaynak: C:\Projeler\.tmp-video\altin\<id>\ ham dump'ları (aciklama, altyazi, groq, ocr, yorum); altın JSON'lar `docs/video-tarama/altin/<id>.json` (Desktop doğrulaması: `dogrulama/README.md`), puan `video altin puan` (rapor: `docs/video-tarama/2026-10-07-<id>.md`), LLM/API çağrısı yok.

## Doğrulanmış altınla (2026-10-07)

Belirsiz adaylar paydaya girmez; parantezde "belirsiz bulundu". Öğrenim: raporun tüm metninde aynı satırda ≥4 harfli kelimelerin ≥yarısı.

| id | aday yakalama | isabet | ad yazım | öğrenim | site_ui | komut | url | iş akışı | link açıklama | link yorum |
|---|---|---|---|---|---|---|---|---|---|---|
| aZe5ZTYcF1M | 2/22 (belirsiz 0/1) | 2/2 | 1/2 | 4/22 | 0/23 | 0/1 | 0/3 | 0/14 | 1/1 (sınıf 0/1) | 1/1 (sınıf 0/1) |
| 1nGx7WR8YLE | 5/18 (belirsiz 0/5) | 6/11 | 3/5 | 4/14 | 3/10 | 0/0 | 0/5 | 0/12 | 1/1 (sınıf 0/1) | 1/1 (sınıf 1/1) |
| YDAK1lvVXho | 5/26 (belirsiz 0/5) | 5/12 | 1/5 | 4/9 | 1/18 | 0/0 | 0/2 | 0/15 | 1/1 (sınıf 0/1) | 1/1 (sınıf 1/1) |
| FaChtkkG9X4 | 3/16 (belirsiz 0/1) | 3/8 | 2/3 | 0/1 | 1/20 | 1/1 | 0/6 | 0/15 | 4/4 (sınıf 4/4) | 0/0 |
| d_UE-wHLoZY | 3/13 (belirsiz 0/13) | 3/4 | 2/3 | 0/1 | 0/2 | 0/0 | 0/1 | 0/15 | 0/0 | 0/1 (sınıf 0/0) |

url ve iş akışı rapor şemasında karşılığı olmayan alanlar (ALAN_YOK), bu yüzden 0 çıkar.

### Tür kırılımı (belirsizler hariç)

- aZe5ZTYcF1M: model 2/2 · servis 0/1 · uygulama 0/2 · kütüphane 0/6 · teknik 0/8 · font 0/2 · CLI 0/1
- 1nGx7WR8YLE: servis 2/4 · uygulama 2/4 · model 1/3 · MCP 0/1 · skill 0/4 · CLI 0/1 · teknik 0/1
- YDAK1lvVXho: servis 1/3 · model 2/2 · uygulama 2/2 · teknik 0/6 · kütüphane 0/4 · skill 0/4 · font 0/5
- FaChtkkG9X4: model 1/1 · uygulama 1/5 · CLI 0/1 · servis 1/3 · font 0/2 · teknik 0/4
- d_UE-wHLoZY: uygulama 2/2 · servis 1/1 · model 0/3 · teknik 0/7

### Kaçan adaylar

- aZe5ZTYcF1M: Awwwards (servis), Claude Code (uygulama), Three.js (kütüphane), WebGL (teknik), Canvas (teknik), Fragment shader (teknik), Framer Motion (kütüphane), Subagent (teknik), Built-in browser (uygulama), Vite (kütüphane), TypeScript (kütüphane), GSAP (kütüphane), Lenis (kütüphane), Neue Montreal (font), Inter Tight (font), Web Worker (teknik), Depth-of-field (teknik), Manyetik butonlar (teknik), npm (CLI), Claude memory (teknik)
- 1nGx7WR8YLE: Awwwards (servis), Fable (model), Seedance 2.5 (model), Topview MCP (MCP), Behance (servis), Codex (uygulama), Blender (uygulama), design-dna (skill), frontend-design (skill), design-taste-frontend (skill), scrollcraft (skill), ffmpeg (CLI), cut-and-extend (teknik)
- YDAK1lvVXho: Sketchfab (servis), Awwwards (servis), scroll-driven storytelling (teknik), exploded view (teknik), Three.js (kütüphane), GSAP (kütüphane), design-dna (skill), scrollcraft (skill), frontend-design (skill), design-taste-frontend (skill), TypeScript (kütüphane), reduced motion (teknik), Georgia (font), Times New Roman (font), Arial (font), contact sheet (teknik), ScrollTrigger (kütüphane), Bodoni Moda (font), Hanken Grotesk (font), parallax (teknik), rim light (teknik)
- FaChtkkG9X4: Figma (uygulama), Claude Code (CLI), Higgsfield (servis), ChatGPT (uygulama), Claude (uygulama), Claude Design (uygulama), Claude Artifacts (servis), Archivo (font), Instrument Sans (font), Vanilla JS (teknik), prefers-reduced-motion (teknik), Appear efekti (teknik), Parallax (teknik)
- d_UE-wHLoZY: GPT Image 2 (model), Nano Banana (model), Generate Image (teknik), Edit Image (teknik), Generate Model (teknik), Tripo v3.1 (model), Generate Multi-Views (teknik), Emission (teknik), Bezier curve (teknik), Principled BSDF (teknik)

## Taslak altınla (geçersiz)

Sonnet taslağı gerçeğin yaklaşık üçte birini tutuyordu; aşağıdaki puanlar bu yüzden olduğundan iyi görünür.

| id | aday yakalama | isabet | ad yazım | komut | url | iş akışı | link açıklama | link yorum | site_ui |
|---|---|---|---|---|---|---|---|---|---|
| aZe5ZTYcF1M | 2/3 | 2/2 | 1/2 | 0/0 | 0/1 | 0/3 | 1/1 (sınıf 0/1) | 1/1 (sınıf 0/1) | 1/4 |
| 1nGx7WR8YLE | 4/11 | 4/11 | 2/4 | 0/0 | 0/2 | 0/6 | 1/1 (sınıf 0/1) | 1/1 (sınıf 1/1) | 0/3 |
| YDAK1lvVXho | 2/9 | 2/12 | 0/2 | 0/0 | 0/1 | 0/3 | 1/1 (sınıf 1/1) | 0/0 | 1/6 |
| FaChtkkG9X4 | 2/5 | 2/8 | 1/2 | 1/1 | 0/4 | 0/6 | 4/4 (sınıf 4/4) | 0/0 | 1/2 |
| d_UE-wHLoZY | 3/5 | 3/4 | 2/3 | 0/0 | 0/1 | 0/6 | 0/0 | 0/1 (sınıf 0/0) | 0/1 |

Notlar: YDAK1lvVXho altınında `"not": "editör yok"` (≥2 dk gerçek editör/terminal görüntüsü yok; Astra/Claude sohbet arayüzü ve site gösterimi). Diğer dördünde not genel taslak notu. FaChtkkG9X4 ocr.txt ve yorum.txt çalışma sırasında tamamlandı, altın OCR ile de güncellendi.

Taslak kaçanlar:

- aZe5ZTYcF1M: Three.js (kütüphane)
- 1nGx7WR8YLE: Seedance 2.5 (model), Fable (model), design-dna (skill), frontend-design (skill), design-taste-frontend (skill), scrollcraft (skill), ffmpeg (araç)
- YDAK1lvVXho: Three.js (kütüphane), GSAP (kütüphane), ScrollTrigger (kütüphane), design-dna (skill), scrollcraft (skill), frontend-design (skill), design-taste-frontend (skill)
- FaChtkkG9X4: Claude Design (uygulama), Figma (uygulama), ChatGPT (uygulama)
- d_UE-wHLoZY: GPT Image 2 (model), Nano Banana (model)

## 1b-2a uçtan uca

Kurgu 2 = m4 sonnet (birincil) + m4 haiku birleşimi, kanıt süzgeci salt işaretle; `video altin puan` ile puanlandı (0 çağrı, DEVAM-4 B ile aynı betik). Eski satır: "Doğrulanmış altınla (2026-10-07)" tablosu, commit 20451a5 (2026-10-07).

Eski ölçüyle (aynı alanlar: aday yakalama · url · iş akışı):

| satır | aday yakalama | url | iş akışı |
|---|---|---|---|
| eski (2026-10-07, 20451a5) | 18/95 | 0/17 | 0/71 |
| kurgu 2 | 60/96 | 16/18 | 46/71 |

Paydalar: aday 95→96 (YDAK +1), url 17→18 (1nGx +1); altın DEVAM'larda büyüdü. Eskide url ve iş akışı ALAN_YOK olduğu için 0 çıkmıştı; şimdi rapor şemasında karşılıkları var.

Yeni ölçü, kurgu 2:

| id | kurulabilir | isabet | url | işe yarar url | komut |
|---|---|---|---|---|---|
| aZe5ZTYcF1M | 9/12 | 13/16 | 3/3 | 1/1 | 1/1 |
| 1nGx7WR8YLE | 15/17 | 19/22 | 5/6 | 3/4 | 0/0 |
| YDAK1lvVXho | 14/16 | 19/22 | 1/2 | 0/0 | 0/0 |
| FaChtkkG9X4 | 7/10 | 10/21 | 6/6 | 4/4 | 1/1 |
| d_UE-wHLoZY | 6/6 | 10/15 | 1/1 | 1/1 | 0/0 |
| toplam | 51/61 | 71/96 | 16/18 | 9/10 | 2/2 |

Sapma: birincil kurulabilir 51/61 (eşik 52, 1 aday farkla) · aZe5 9/10 · FaCh 7/8 — kabul, gerekçe: koşu oynaklığı ±3, çift dikişte yeniden işlenecek (Desktop kararı 2026-10-08). (Puanlayıcı paydası: aZe5 9/12, FaCh 7/10; kaçanlar `docs/yol-haritasi.md` "1b-2a kurgu 2 kaçanlar".)

İkincil (geçici ölçü, 1b-2b'de yeniden doğrulanacak): iş akışı 46/71 · promptlar 12/23 · site_ui 23/73 · öğrenim anlamsal 32/47.
