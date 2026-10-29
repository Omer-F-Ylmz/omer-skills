---
type: rapor
status: devam
tags: [video, kurulum, nihai-36]
relatedTo: [video-764-1, kurulum-v1]
---
# VIDEO-IZLE-KUR-1 — tur 1 (29 Eki) · ARA KAYIT
- ADIM 1 envanter: `video_izle_kur_1_envanter.py` → `ogren/video-izle-kur-1/envanter.tsv` 174 tekil (video-764-aday). KURULU 40 · KLONLU 32 · KURULACAK 84 · ELE-V1 18 (güvenlik/lisans kanıtlı). Kalan 116 → 3 tur (40/40/36).
- Kapsam dışı (ölçülmedi): v2'deki 235 UYARLA + 3 AL satırının araç adı sütunu yok; aday.tsv dışında kalan araç adı çıkarılmadı.
- Tur 1 (40): 23 kalemin derin json'u var, 17 eksik video `video_derin.py` (Groq ASR) ile kuyrukta; 29 repolu kalem `video_izle_kur_1_tara.py` (SkillSpector/gitleaks/semgrep, RAM kapısı %89) ile `C:\AI\indirilen\video-izle-kur-1`; ADIM 2 çıkarma `video_izle_kur_1_cikar.py` (ücretsiz havuz).
- ADIM 2 çıkarma (Groq, Claude $0): 40 kalemden 9 ok (`tur1-cikar.jsonl`), 14 model-yok (havuz düştü, yeniden koşulacak), 17 derin-yok.
- Derin izleme ~25 dk'da 0/17: ilk IG reel'inde yt-dlp indirmesi takıldı (süreç canlı, ilerleme dosyası değişmedi). Tarama: 29 repodan 1'i (magpie) SkillSpector'da, sonuç 0. RAM %92-95 (başka oturumun 4 haiku `claude -p` süreci), sonra %85.
- ADIM 3 kurulum ve ADIM 4 usta kartı: başlamadı (tarama sonucu yok). Arka işler oturum ölünce ölür (breakaway reddi); 3 betik kaldığı yerden devam eder.
- SIRA: `arka-istek` ile tara+derin yeniden başlat → model-yok 14 için cikar yeniden → MIT/Apache + tarama temiz olanları kur. Yeni 800-900 link için hazır DEĞİL (116 kalem kaldı).
