# Token notları · Eylül 2026 · 2026-09-17
Kaynak: Claude Code changelog (yerel önbellek, 2.1.274), KURULUM-2 dalgası, `/context` ve `/skill-doctor` ölçümleri.
## Kararlar
- Fable 5.1: ELENDİ. Net kazanç ~%2; build/dependency riski.
- RTK: ölçüm bekliyor (JetBrains: düşük effort'ta +%7.6). Kendi ölçümü gelmeden kural değişmez.
## Uygulanan (KURULUM-2)
- Sürüm 2.1.274, güncelleme gerekmedi; `claude doctor`: "No installation issues found".
- `~/.claude/settings.json` (yedek `settings.json.bak2`):
  - `maxEffortLevel: "high"` + `modelSettings.claude-opus-5.effortLevel` xhigh → high (tavan kalkarsa xhigh'a dönmesin).
  - env `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`: `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` her subagent'a uygulanır, agent tanımındaki model override'ı yok sayılır.
  - `bashEditDiffEnabled` ve `CLAUDE_CODE_ENABLE_TODO_TOOLS` zaten tanımsız.
- `omitClaudeMd`: `~/.claude/agents` ve omer-skills'te subagent yok → değişiklik yok.
  - İleride yazılacak verbose subagent'lara (test/log/CI/çok dosyalı keşif) `omitClaudeMd: true`; karar veren / kod yazan agent'a eklenmez.
- `/skill-doctor`: 11 plugin skill'i ve 3 claude.ai sync skill'i hiç çağrılmamış.
  - `skillOverrides: off` plugin skill'ine işlemiyor (2.1.274'te skill-doctor: "Plugin skills can't be turned off individually — disable those plugins in /plugin"). Kapatma yalnız plugin düzeyinde.
  - claude-md-management kapatıldı (geri: `claude plugin enable claude-md-management`); dotnet-data · dotnet-aspnetcore · frontend-design bilinçli açık; tetikleyici: 30 gün 0× kalırsa yeniden bak.
- Kalem 5 → env `DOTNET_NOLOGO=1` (yalnız CC oturumları); CLAUDE.md satır 17 değişmedi.
  - `-v q` ELENDİ: RTK filtresiyle çift. MTP `--no-banner` gerekirse proje CLAUDE.md'sine.
  - Gerekçe: satır genişletmesi CLAUDE.md'yi ~1,301 → ~1,373 token yapıyordu (kısa varyant ~1,349), ≤1300 sınırını aşıyor.
## Ölçüm yöntemi
- `/context` 1k üstünü yuvarlar ("1.3k"). Kesin sayı: dosya iki yarıya bölünüp scratch projede `CLAUDE.md` + `CLAUDE.local.md` olarak ölçülür.
- Her dosya satırı ~5 token çerçeve yükü taşır (tek satır "x" = 7); iki yarının toplamından bir çerçeve düşülür.
## Alışkanlık
- Yan soru → `/btw`: cevap konuşma geçmişine girmez, sonraki turlarda yeniden okunan context büyümez.
## Bölüm 2 (KURULUM-3)
- `promptCacheTtl: "1h"` eklendi (yedek `settings.json.bak3`). Abonelikte varsayılan zaten 1h (changelog: ayar API anahtarı/bulut için; "subscribers … 5-minute instead of 1 hour" düzeltmesi); açık yazıldı. env TTL yok.
- İngilizce-AB (iki yarı, 2× `claude -p "/context"`): TR 648+651−5 = 1,294 · EN 487+496−5 = 978 → −%24,4 → geçildi (eşik altı ama gürültü içinde; tavan altı ~320 token boşluk). `~/.claude/CLAUDE.md` İngilizce (26 satır, `@RTK.md` aynı, terimler Türkçe), yedek `CLAUDE.md.bak-tr`.
  - Gürültü: aynı MCP araçları 2. koşuda ~%5 yüksek sayıldı; sınırda sonuç, yeniden ölçüm ancak yeni tarifle.
- `claude doctor` Git Bash/PowerShell'den exit 255 döner ama "No installation issues found" yazar; çıkış kodu değil metin esas.
- opusplan → yalnız test/refactor dalgalarında A/B. FORCE-AB bekliyor. /rewind kuralı değişmedi.
- Divisima CLAUDE.md (bugün 30.4k karakter; tarifte 54 KB) → `.claude/rules` paths'e taşıma Divisima chat'inde.
### cclint (`@felixgeelhaar/cclint` 0.16.0; npm'de `cclint` adı 404)
- bakım=push 2026-09-14, 12★, archived=false, 0 açık issue · çift=claude-md-improver (kapalı plugin) ile kısmi, `/context` token ölçmez yalnız boyut · izin=MIT; `lint` yerel, ağ yalnız `why --ai` (ANTHROPIC_API_KEY, opt-in) · context=0 (npx CLI; MCP/LSP modu kurulmaz)
- SkillSpector `--no-llm`: 100/100 CRITICAL-skor, CRITICAL kural 0; HIGH/MEDIUM'lar test fixture (SecretDetectionRule), CHANGELOG/README `npx` satırları, lockfile (brace-expansion) kaynaklı → lint için kabul.
- `~/.claude/CLAUDE.md`: 1 hata · 3 uyarı · 6 info. Hata yanlış pozitif: `@RTK.md` dosya dizini yerine cwd'ye çözülüyor. Uyarılar "Project Overview/Development Commands/Architecture" eksik (global dosyaya uymaz).
- Divisima CLAUDE.md: 0 hata · 8 uyarı · 39 info (boyut 30k>10k, 2 dilsiz code block, kişisel bilgi olasılığı, önerilen bölümler).
- Düzeltme yapılmadı. Kural değişikliği yok; kalıcı araç olarak kurulmadı.
- Output style Concise aktif (2026-09-18, settings.json `outputStyle`). A/B: ilk 3 dalgada rapor satır sayısı ve tur sayısı öncekiyle karşılaştırılır.
