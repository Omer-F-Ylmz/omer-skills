# qa — 35 benzersiz kayıt

**Amaç:** Test ve kalite güvencesi ajan kadrosu: test stratejisi, birim/entegrasyon/e2e, yük, erişilebilirlik, flaky ve test kalitesi denetimi; ayrıca gstack'ten iki QA skill'i.

**İç yapı:** 33 [ajan] qa-<Türkçe konu> adlı (ör. qa-flaky-avci, qa-test-kokusu); gruplar: strateji/plan, çerçeveye özel (playwright, selenium, jasmine, ava, testcafe, pytest), performans/yük, kalite denetimi; 2 [skill] qa ve qa-only (gstack).

## En güçlü parçalar
- `qa-test-stratejisi` — Risk tabanlı kapsam, test piramidi düzeyleri ve kalite kapılarını tanımlar.
- `qa-flaky-avci` — Kararsız testi döngüyle yeniden üretip sıra/zamanlama yalıtımıyla kök nedenini bulur.
- `qa-hata-yeniden-uret` — Belirsiz/aralıklı hata raporunu minimum tekrar adımı ve kök nedene çevirir.
- `qa-test-bosluk-analiz` — Kapsam ve karmaşıklıkla test edilmemiş riskli yolları bulup önceliklendirir.
- `qa-mutasyon-denetci` — Testlerin gerçek hatayı yakalayıp yakalamadığını assertion incelemesi ve mutasyon fikirleriyle yargılar.
- `qa-sahte-uygulama-avcisi` — Üretimde kalmış mock, fake, stub, placeholder ve sabit kodlanmış kodu bulur.
- `qa-entegrasyon-testi` — Container, fixture ve yalıtımla gerçek bağımlılıklara karşı entegrasyon testi.
- `qa-test-kokusu` — Sleep, paylaşılan durum, determinizmsizlik, sıra bağımlılığı, assertion'sız test kokularını tespit eder.

## Birlikte kullanım
- qa-test-stratejisi → qa-test-bosluk-analiz → qa-mutasyon-denetci: kapsamı planla, boşluğu bul, testin gücünü sına.
- qa-hata-yeniden-uret + qa-flaky-avci: aralıklı hatada önce repro, sonra kararsızlık kök nedeni.
- qa-test-verisi + qa-entegrasyon-testi: gerçek kişisel veri içermeyen deterministik veriyle entegrasyon.
- qa-ci-test-duzeni + qa-uzun-suit-kosucu: yavaş CI'da hızlı/yavaş ayrımı ve parçalı koşu.

## Tuzaklar
- Örtüşen ajanlar: qa-e2e-playwright ile qa-playwright, qa-performans-yuk-testi ile qa-yuk-testi; birini seçmek yeterli.
- qa (gstack) hatayı düzeltir, qa-only yalnız raporlar; salt rapor isteniyorsa qa-only.
- Çerçeveye özel ajanlar (qa-jasmine-test, qa-ava-test, qa-testcafe, qa-selenium) yalnız o çerçeve kullanılıyorsa anlamlı.

## Üyeler
- ajan (33): qa-anlik-goruntu-testi, qa-api-test, qa-ava-test, qa-benchmark-regresyon-kapisi, qa-ci-test-duzeni, qa-disaridan-tdd, qa-e2e-playwright, qa-entegrasyon-testi, qa-erisilebilirlik-testi, qa-flaky-avci, qa-gorsel-qa, qa-hata-yeniden-uret, qa-jasmine-test, qa-manuel-test-plani, qa-mobil-qa, qa-mutasyon-denetci, qa-ozellik-paritesi, qa-ozellik-tabanli, qa-performans-yuk-testi, qa-playwright, qa-pytest-fikstur, qa-sahte-uygulama-avcisi, qa-selenium, qa-sinir-deger-analizi, qa-test-bosluk-analiz, qa-test-iskelet-dotnet, qa-test-kokusu, qa-test-stratejisi, qa-test-verisi, qa-testcafe, qa-ui-kapsamli, qa-uzun-suit-kosucu, qa-yuk-testi
- skill (2): qa, qa-only
