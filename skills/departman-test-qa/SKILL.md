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
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- `dotnet-test:assertion-quality` · Analyze assertion quality, depth, variety, and false confidence in existing tests · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/assertion-quality/SKILL.md`
- `dotnet-test:code-testing-agent` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/code-testing-agent/SKILL.md`
- `dotnet-test:code-testing-extensions` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/code-testing-extensions/SKILL.md`
- `dotnet-test:coverage-analysis` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/coverage-analysis/SKILL.md`
- `dotnet-test:crap-score` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/crap-score/SKILL.md`
- `dotnet-test:detect-static-dependencies` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/detect-static-dependencies/SKILL.md`
- `dotnet-test:filter-syntax` · Reference-only filter syntax for VSTest and MTP with MSTest, NUnit, xUnit v3, and TUnit · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/filter-syntax/SKILL.md`
- `dotnet-test:find-untested-sources` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/find-untested-sources/SKILL.md`
- `dotnet-test:generate-testability-wrappers` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/generate-testability-wrappers/SKILL.md`
- `dotnet-test:grade-tests` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/grade-tests/SKILL.md`
- `dotnet-test:migrate-static-to-wrapper` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/migrate-static-to-wrapper/SKILL.md`
- `dotnet-test:mtp-hot-reload` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/mtp-hot-reload/SKILL.md`
- `dotnet-test:platform-detection` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/platform-detection/SKILL.md`
- `dotnet-test:run-tests` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/run-tests/SKILL.md`
- `dotnet-test:scaffold-dotnet-test-project` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/scaffold-dotnet-test-project/SKILL.md`
- `dotnet-test:test-analysis-extensions` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/test-analysis-extensions/SKILL.md`
- `dotnet-test:test-anti-patterns` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/test-anti-patterns/SKILL.md`
- `dotnet-test:test-gap-analysis` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/test-gap-analysis/SKILL.md`
- `dotnet-test:test-smell-detection` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/test-smell-detection/SKILL.md`
- `dotnet-test:test-tagging` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/test-tagging/SKILL.md`
- `dotnet-test:testability-obstacle` · >- · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/testability-obstacle/SKILL.md`
- `dotnet-test:writing-mstest-tests` · > · `C:/Users/pc/.claude/plugins/cache/dotnet-agent-skills/dotnet-test/0.2.19/skills/writing-mstest-tests/SKILL.md`
<!-- profil-disi:son -->
