---
type: summary
status: active
tags: [yarim-a1, ret-denetim, arac-bul-2b]
relatedTo: [ret-denetim-1, arac-bul-2b]
---
# YARIM-A1 raporu

- arac-bul-2b: ZATEN BİTMİŞ — commit 2797cd03 (221 sınıflandı: bulundu 123 · OCR 39 · uygulama/site 28 · komut 27 · bilinmiyor 4 = %1,8; 118 repo + 27 büyük indirildi, gitleaks+semgrep temiz); çıktı rapor/arac-bul-2.tsv (221 satır). Girdi arac-indir-2.tsv bilerek değişmedi.
- ret-denetim-1: BİTTİ (kısmen: kurulumlar DEVAM → gorev/ret-kur-1.md). 193 satır sınıflandı (ret-denetim.tsv): geçerli ret 19 · yanlış ret→KUR 18 · KUR-sonra 19 · kurulamaz(kanıt) 5 · karar değil 112 (anma/düz metin) · özet tekrarı 20. Yanlış ret önce/sonra: 193 "ret" görünümü → 37 gerçek yanlış ret (+5 kurulamaz).
- Skill kuralı: eski ELE eşleşmesi artık ÖNCEDEN-GÖRÜLDÜ değil KUR-sonra (tarama.py + video-tarama/video-uygula SKILL.md); test kırmızı→yeşil, tarama+ogren 66 geçti. Tam tools/video suiti 10 dk'da bitmedi (arka plan zaman aşımı) → çalıştırılmadı.
- ÖMER: skill değişikliğinin claude.ai tarafı için dist zip yeniden üretilip yüklenmeli; CC tarafında skills/ kopyası synced gölgesi nedeniyle zip yüklenene dek görünmez.
- Yapılmadı: ajan-sira.tsv satırı ve zip üretimi (ret-kur-1 ile birlikte).
