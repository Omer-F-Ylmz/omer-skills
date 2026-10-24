# YARIM-E3, Laya (24 Eki)

- laya-2 / laya-2c: **DEVAM (gorev-yarim-e3-devam.md)**, kurul↔Opus ρ kapısı (≥0.6) geçmedi; 3 istem denemesi + ridge bitti, DUR kuralı.
- Zaten bitenler (kanıt: 25937c55, 7b5add7b): puan ayıklayıcı `tools/laya/puan.py` + `test_laya_puan.py` (OmniRoute 0-puan hatası kök nedeni), sambanova kurul listesinde.
- Ölçüm (n=259 Opus etiketli): kurul ortalama ρ=0.36, ağırlıklı 0.39; ridge test ρ=0.37-0.41; en iyi tek sağlayıcı mistral 0.47. v1 ORT 0.465 (n=100), v2 0.444, v3 0.419 (n küçük, kota).
- Kök neden (kanıtlı): Opus etiketlerinin %92'si 8 (143) ya da 10 (96); ≤6 yalnız 20. Kurul bozuk yanıtı iyi yakalıyor (≤6 ayırma AUC kurul 0.82, mistral 0.94) ama 10↔8 ayrımı zayıf (AUC 0.64; mistral 0.61, gemini 0.52). Spearman bu bağlı-değer dağılımında 8/10 ayrımına bağlı → istem oyunuyla 0.6 beklenmez.
- Ölçüt değiştirilmedi. Karar Ömer'de: (a) kapıyı "≤6 yakalama AUC≥0.8 + ρ" olarak yeniden tanımla, (b) 8/10 ayrımı için Opus tekrar-etiket gürültü tavanını ölç (≤25 claude), (c) kurulu yalnız "kötü/iyi" filtresi olarak kullan, ρ'yu Laya eğitiminden ayır.
- ÖMER: (a)/(b)/(c) seçimi (tek cümle).
- Claude maliyeti: ~$0.5 (okuma/teşhis; ücretsiz çağrı 0, kota/yeni koşu yok).
