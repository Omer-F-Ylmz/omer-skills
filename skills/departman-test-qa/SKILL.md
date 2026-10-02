---
name: departman-test-qa
description: "Test/QA müdürü: test yazma, koşma, uygulamayı tarayıcıda deneme ve görsel QA sırası. Test, e2e, QA ya da 'çalışıyor mu' işinde oku."
---

# Departman: test-qa — iş sırası

Katalog: `docs/departmanlar/test-qa.md`. Frontend işinde bu müdür `departman-frontend` adım 5-6'dan çağrılır.

## Adımlar
1. **Kırmızı-önce** — davranış/bug için önce başarısız test: `test-driven-development` (hata ise `systematic-debugging` ile kök neden).
2. **Test yazımı** — .NET: `code-testing-agent` · `writing-mstest-tests`; diğer diller: proje test çatısı. Boşluk: `test-gap-analysis` · `find-untested-sources`.
3. **Koşma** — .NET `run-tests` (`rtk dotnet test`), JS/Python kendi runner'ı; büyük log alt ajana. omer-skills tam suit → `suite-kosucu` ajanı (6 sabit komut, ≤6 satır dönüş).
4. **Uygulamayı deneme** — gerçek uygulamada uçtan uca: `webapp-testing` ya da `playwright-cli`; oturum gerekiyorsa `browse` / `setup-browser-cookies`; akış QA `qa` (yalnız rapor `qa-only`).
5. **Görsel QA** — `pixeljury` görsel regresyon; screenshot 390/768/1440. Performans gerekirse `benchmark`.
6. **Doğrulama** — `verification-before-completion`: kanıtsız "bitti" yok; test sayısı ve çıktı rapora.

## Kapılar
- Kırmızı görülmeden yeşil kod yok; mutasyonla en az bir test kırmızıya düşmeli.
- Suite yeşil + gerçek uygulamada deneme olmadan kapanış yok (≤10 satır değişiklikte yalnız test koşusu yeter).
- a11y 0 hata (frontend) görsel QA'dan önce.

## Çakışma
- Tarayıcı aracı: `playwright-cli` > `webapp-testing` > puppeteer; aynı işte ikisini birden kullanma.
- Test kalitesi denetimi (`test-anti-patterns`, `assertion-quality`) yalnız istendiğinde.

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- dotnet-test (22): assertion-quality, code-testing-agent, code-testing-extensions, coverage-analysis, crap-score, detect-static-dependencies, filter-syntax, find-untested-sources, generate-testability-wrappers, grade-tests, migrate-static-to-wrapper, mtp-hot-reload, platform-detection, run-tests, scaffold-dotnet-test-project, test-analysis-extensions, test-anti-patterns, test-gap-analysis, test-smell-detection, test-tagging, testability-obstacle, writing-mstest-tests · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->
