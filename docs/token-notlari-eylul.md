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
  - `skillOverrides: off` plugin skill'ine işlemiyor (2.1.274'te skill-doctor: "Plugin skills can't be turned off individually — disable those plugins in /plugin"). Kapatma yalnız plugin düzeyinde; karar bekliyor.
- Kalem 5 → env `DOTNET_NOLOGO=1` (yalnız CC oturumları); CLAUDE.md satır 17 değişmedi.
  - `-v q` ELENDİ: RTK filtresiyle çift. MTP `--no-banner` gerekirse proje CLAUDE.md'sine.
  - Gerekçe: satır genişletmesi CLAUDE.md'yi ~1,301 → ~1,373 token yapıyordu (kısa varyant ~1,349), ≤1300 sınırını aşıyor.
## Ölçüm yöntemi
- `/context` 1k üstünü yuvarlar ("1.3k"). Kesin sayı: dosya iki yarıya bölünüp scratch projede `CLAUDE.md` + `CLAUDE.local.md` olarak ölçülür.
- Her dosya satırı ~5 token çerçeve yükü taşır (tek satır "x" = 7); iki yarının toplamından bir çerçeve düşülür.
## Alışkanlık
- Yan soru → `/btw`: cevap konuşma geçmişine girmez, sonraki turlarda yeniden okunan context büyümez.
