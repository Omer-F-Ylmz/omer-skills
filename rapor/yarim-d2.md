# YARIM-D2, Ses-yazı ve OCR doğruluğu (24 Eki 2026)

- **ocr-hiz-1: ZATEN BİTMİŞ.** Düzeltme `8e88e709` main'de (`git branch --contains` main'i listeliyor). Canlı doğrulama: `.kos/kopru/derin-profil.tsv` 2259 satır; ilk 597 klip `cpu`, sonraki 1662 klip `cuda`. Klip başına OCR süresi medyan 20,7→5,3 sn, p95 257,5→62,7 sn, ≤80 sn olan klip 523/597 (%88)→1609/1662 (%97). A/B kanıtı: 60 kare 389,4 sn (CPU) vs 20,1 sn (GPU), 450 satır birebir.
- **cuda-kur-3 araç/komut adı ≥%98: BİTTİ.** %97,7→%99,0 (912 ad, 379 video), commit `6253b9c1`. Bu oturumda yeniden ölçülmedi (ekran OCR atlası gerektiriyor); önceki ölçümün kaydı commit mesajında.
- **cuda-kur-2/3 kelime WER <%2: DEVAM / ÖMER.** Ham dosyalardan bu oturumda yeniden hesaplandı (13 klip, 3998 kelime, referans `.kos/kopru/wer-altin/*.altin.txt`, normalizasyon `wer_altin.norm`):

  | Kaynak | WER |
  |---|---|
  | groq | %2,95 (118 hata) |
  | yerel large-v3 | %6,10 (244) |
  | gemini | %10,13 |
  | mistral | %34,12 |

  Hedef tutmadı; en iyi tek kaynak Groq %2,95. Groq farkının bir kısmı klip kenarında kesilen kelimeler (`değerli→de`, `güncelleyebildiğimiz→g`), kalanı marka/ek yazımı (`claude→cloud`, `skill→skil`, `posthog→postdoc`). Referans, bu üç kaynağın oyundan çıktığı için Groq lehine yanlı; bağımsız bir ölçüm değil. Ekran altyazısı referansıyla da ölçülemiyor (altın bile %16,4).
  - `loo.json` yerel için %1,29 gösteriyor ama uzlaşılmayan bloklar joker sayıldığından alt sınır; hedefin kanıtı sayılmaz.
  - ÖMER: 2–3 klibin (~300 kelime) altın metnini kulakla doğrula; ancak bağımsız referansla %2 iddiası doğrulanır ya da çürür.
- Kod/test değişikliği yok, commit yok (yalnız rapor + plan satırı).

## DEVAM (24 Eki, akşam): kelime WER <%2, ROVER yolu
- **Kelime WER <%2: DEVAM / kanıtlanamadı.** Ömer'e elle transkript yok (karar 24 Eki 16:20). Gemini ses-girdili döküm zaten vardı; Mistral Türkçe desteklemiyor (%34), havuz dışı. ROVER: groq (pivot) + gemini + yerel large-v3, 4017 kelime, 342 ayrışma kümesi → `.kos/kopru/wer-altin/rover/<id>.txt` (`tools/rover_ref.py`).
- **Belirsiz** (üçü ayrışan): 98 kelime = %2,44 (≤%3) → zaman damgalı liste gerekmedi; blokları `rover/belirsiz.json`. ÖMER (isteğe bağlı): yok.
- **Ölçüm** (`tools/rover_olc.py`, ROVER ref lehine yanlı: üç kaynağın oyundan çıktı): yerel large-v3 %2,76 · groq %6,30 · gemini %6,52 · ROVER'ın eski altına farkı %5,0 (altın groq-pivotlu ve hatalıydı: `claude→klad`, `github reposu→gitar pripası`, `codex te→kodekste`; ROVER bunları düzeltiyor). Eski altına karşı groq %2,95 yanlıydı; gerçek sıralama yerel > groq ≈ gemini.
- **Hedef <%2 tutmadı/kanıtlanamıyor:** en iyi tek kaynak yerel %2,76 (biased alt sınır); ROVER üretim adayı olarak ölçülemez (kendi referansı), 3 kaynak çalıştırmak (Gemini kotası+Groq+GPU) video başına maliyetli. Bağımsız altın olmadan %2 iddiası doğrulanamaz.
- **Klip kenarı kesilmesi (adım 3): üretimde yok.** `video_derin.groq_asr` tam sesi tek dosya yollar (≤15 MB); kesik kelime ölçüm harnesinin klip kesiminden. Ayrışma kümelerinin yalnız 7/342'si (%2) klip kenarında → segment örtüşmesi eklenmedi (kusur yok, kırmızı test yok).
- **Ekran adı düzeltici (adım 4): bu 13 klipte etkisi 0.** Groq çıktısında 0 düzeltme (10 klipte OCR var, 3'ünde derin JSON yok; `posthog/claude` ekranda yazılı değil) → WER değişmedi (%6,30→%6,30 ROVER, %2,95→%2,95 altın). Etkiyi ölçmek için adın ekranda geçtiği klipler gerekir.
- Test: `tests/test_rover_ref.py` (2) + wer testleri 5 geçti. Commit aşağıda.
