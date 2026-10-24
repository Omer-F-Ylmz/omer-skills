---
type: summary
status: complete
tags: [yarim-tara, yarim-kalan-isler, ajan-sira, devir]
relatedTo: [ajan-sira, ajan-sira-log, devir]
---

# YARIM-TARA-1 — yarım kalan işler dökümü

Kaynak: `.kos/kopru/gorev*/` (görev dosyaları), `ajan-sira.tsv`, `ajan-sira.log`, `devir/` (son 3 gün). Ayrıntı: `rapor/yarim-tara-1.tsv`. Kod değişikliği yok.

Sayım (görev dosyası, hariç tutulanlar düşüldü):
- KUYRUĞA-GİRMEMİŞ: 190
- KOŞMUŞ-BİTMEMİŞ (son olay DUR / KAPI BAŞLAMADI / rc≠0): 94
- KISMİ-NİHAİ: 3
- RAPOR-YOK (`rapor/` istiyor, `rapor/<ad>*.md` yok): 97
- TAMAM: 171
- Devir maddeleri: 30 (eşleşen: 6 TAMAM, 6 KUYRUĞA-GİRMEMİŞ, 1 KOŞMUŞ-BİTMEMİŞ; 23 eşleşmedi)

En eski 10 (KOŞMUŞ-BİTMEMİŞ, son tarih = görev dosyası mtime):
1. token-2-d4 · 10-14 · BİTTİ rc 1
2. video-kisa-token-1 · 10-14 · BİTTİ rc 1
3. kucuk-5 · 10-20 · BİTTİ rc 3221225786
4. beyin-kaydet-1 · 10-22 · DUR (2 devam turu sonra eksik kaldı)
5. beyin-kaydet-1-a2 · 10-22 · DUR (aynı)
6. cuda-kur-3 · 10-22 · DUR (devam4-a2)
7. cuda-kur-3-devam2 · 10-22 · DUR
8. cuda-kur-3-devam2-a2 · 10-22 · DUR
9. cuda-kur-3-devam3 · 10-22 · DUR
10. cuda-kur-3-devam3-a2 · 10-22 · DUR

Sınırlar:
- Son durum, aile adına (ad = görev veya ad-*) göre zamana sıralı son olaydır; sonradan başarılı bir -devam koşusu varsa bu tarama onu görmez. Ayrı ayrı doğrulanmadı.
- "RAPOR-YOK" yalnız görev metninde `rapor/` geçen dosyalar için işaretlenir.
- Log satırlarında tarih yok (yalnız saat); "son tarih" dosya mtime'ıdır.
- Hariç tutulan (Ömer kararı): NEFFEX klon-7, NIKKE, borsa, shorts, YouTube trend, inFAMOUS, BHS5 video, TELVE cezve, müzik kanalı, site intro, mod-mai-onizleme, REA Desktop.
- Devir eşleşmesi kelime-tam-eşleşme ile; 23 maddenin görev karşılığı bulunamadı.

Devam: `python .kos/kopru/ara/yarim_tara_1.py` (sayımı yeniden üretir).
