# inc — 16 benzersiz kayıt

**Amaç:** Kod inceleme ve kalite ajanları: diff risk puanı, kod kokusu, karmaşıklık/bağlaşım ölçümü, döngüsel bağımlılık, derin hata ayıklama, bitiş öncesi doğrulama, teknik borç, üretim hazırlığı.

**İç yapı:** Tümü [ajan], inc-<konu>; ölçüm (karmasiklik, baglasim, dongusel), inceleme (mimari, kod-kokusu, ponytail, test-kalitesi, ocr), hata (derin, dedektif), süreç (dogrulama, refaktor, borc).

## En güçlü parçalar
- `inc-dogrulama-oncesi-bitis` — İddia edilen işi test koşup çıktı görerek 'bitti' demeden doğrular.
- `inc-derin-hata-ayiklama` — Aralıklı hatalarda değişken yalıtma, bisect, enstrümantasyonla kanıta kadar.
- `inc-ponytail-kod` — Diff'te gereksiz soyutlama, kullanılmayan kod ve aşırı yapıyı bulur.
- `inc-diff-risk-puani` — Değişen dosyaları risk puanlar, git sahipliğinden reviewer önerir.
- `inc-hata-dedektifi` — Log, stack trace ve son değişiklikleri ilişkilendirip üretim hatası kökü.
- `inc-refaktor` — Testlerle korunan küçük davranış koruyan adımlarla refactor.
- `inc-ocr-coklu-inceleme` — open-code-review CLI ile çok perspektifli AI diff incelemesi.
- `inc-uretim-hazirligi` — Log, hata modu, güvenlik, rollout kontrol listesi.

## Birlikte kullanım
- inc-diff-risk-puani → inc-ponytail-kod → inc-test-kalitesi-inceleme → inc-dogrulama-oncesi-bitis.
- inc-karmasiklik-olcum + inc-teknik-borc + inc-refaktor.
- inc-dongusel-bagimlilik + inc-baglasim-uyum + inc-mimari-inceleme.

## Tuzaklar
- inc-ocr-coklu-inceleme open-code-review CLI kurulumu ister (cli ailesinde @alibaba-group/open-code-review).
- inc-uretim-hazirligi phoenix production-readiness-review ile çakışır.
- inc-tasarim-kaliplari yalnız gerçek karmaşıklığı kaldırdığında kalıp önerir.

## Üyeler
- ajan (16): inc-baglasim-uyum, inc-derin-hata-ayiklama, inc-diff-risk-puani, inc-dogrulama-oncesi-bitis, inc-dongusel-bagimlilik, inc-hata-dedektifi, inc-karmasiklik-olcum, inc-kod-kokusu, inc-mimari-inceleme, inc-ocr-coklu-inceleme, inc-ponytail-kod, inc-refaktor, inc-tasarim-kaliplari, inc-teknik-borc, inc-test-kalitesi-inceleme, inc-uretim-hazirligi
