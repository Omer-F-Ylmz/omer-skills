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
- `/skill-doctor`: 11 plugin skill'i ve 3 claude.ai sync skill'i hiç çağrılmamış; kaldırma kararı bekliyor.
- CLAUDE.md dotnet bayrakları (build/test `--nologo -v q`, build `--no-restore`, MTP `--no-banner`): DUR, uygulanmadı.
  - Dosya zaten ~1,301 token; tam satır +72 → ~1,373; kısa varyant ~1,349. Yalnız o satırla ≤1300 sağlanamıyor.
## Ölçüm yöntemi
- `/context` 1k üstünü yuvarlar ("1.3k"). Kesin sayı: dosya iki yarıya bölünüp scratch projede `CLAUDE.md` + `CLAUDE.local.md` olarak ölçülür.
- Her dosya satırı ~5 token çerçeve yükü taşır (tek satır "x" = 7); iki yarının toplamından bir çerçeve düşülür.
## Alışkanlık
- Yan soru → `/btw`: cevap konuşma geçmişine girmez, sonraki turlarda yeniden okunan context büyümez.
