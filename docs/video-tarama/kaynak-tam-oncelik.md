# KAYNAK-TAM-3 öncelik listesi (Desktop seçer)

Sıra: kare-doğrulu > kaynakta bulunan adım oranı > kare alıntısı > adım sayısı. Kaynak: tools/kaynak_tam.py dogrula; 247 tarif, 208 yüksek.

| # | tarif | video | adım | kaynakta | kare | gerekçe |
|--|--|--|--|--|--|--|
| 1 | bug-bounty-otomasyon-DdA-QjwAMh_ | DdA-QjwAMh_ | 5 | 5/5 | 5 | kare OCR doğruladı; yüksek öncelik |
| 2 | video-kurgu-Dery8BLNDJK | Dery8BLNDJK | 6 | 5/6 | 2 | kare OCR doğruladı; yüksek öncelik |
| 3 | otomasyon-DcQwBpXDSXs | DcQwBpXDSXs | 6 | 5/6 | 2 | kare OCR doğruladı; yüksek öncelik |
| 4 | video-kurgu-DeR11OUkobq | DeR11OUkobq | 4 | 3/4 | 3 | kare OCR doğruladı; yüksek öncelik |
| 5 | prompt-hilesi-DezC2eYkpAa | DezC2eYkpAa | 4 | 3/4 | 1 | kare OCR doğruladı; yüksek öncelik |
| 6 | motion-capture-DeaOQ2bD9Zl | DeaOQ2bD9Zl | 4 | 3/4 | 1 | kare OCR doğruladı; yüksek öncelik |
| 7 | video-kurgu-DcNOMyTCXmO | DcNOMyTCXmO | 10 | 7/10 | 7 | kare OCR doğruladı; yüksek öncelik |
| 8 | openship-kurulum-deploy-DbVGcvfgUsD | DbVGcvfgUsD | 6 | 4/6 | 4 | kare OCR doğruladı; yüksek öncelik |
| 9 | 3d-modeling-Devb42_CIpc | Devb42_CIpc | 5 | 3/5 | 1 | kare OCR doğruladı; yüksek öncelik |
| 10 | security-audit-DeJxR3-hR5b | DeJxR3-hR5b | 5 | 3/5 | 1 | kare OCR doğruladı; yüksek öncelik |

## Skill kaynak listesi önerisi
- Kare açıklaması (kare_aciklama) kayıplı; alıntı kaynağı yalnız konuşma + ekran OCR + video açıklaması olsun (kaynak_tam.py zaten böyle).
- Kapsam kapısı (30 video): kaçırılan 0; tsv'de satırsız 4 video (BsOtUUZgoHa, Db_OcWqjgnk, DbgU1g9FLmr, nT1KPAQL9_g), içerik var/llm yok 2 (DY8EtIPtKLC, nT1KPAQL9_g) → bir sonraki turda llm koş.
- Kart doğrulama: 247 tarifin 23'ü kare OCR ile, 29'u tüm adımları kaynakta; geri kalanı yalnız kısmen doğrulanmış, uygulamadan önce video-uygula risk katmanından geçsin.
