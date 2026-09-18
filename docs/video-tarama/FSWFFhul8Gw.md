# Claude Code'da aktif kullandığım 5 yetenek

Burhan KOCABIYIK · 2026-09-18 · 50 sn · altyazı: tr-orig

ana iddia: Claude Code'da yüzlerce yetenek arasından kendi aktif kullandığı 5 tanesini (yetenek bulma yeteneği, Superpowers, cloud memory, impeccable, Task Observer) kısaca tanıtıyor.

- yetenek bulma aracı (altyazı/açıklamada ad yok; vercel-labs/skills `find-skills`, MIT, 31.9k★) → ELE · `npx skills find` CLI zaten kullanılıyor (design-dna), skill yalnız her oturuma açıklama ekler ve skillspector'sız `npx skills add`'e yönlendirir
- Superpowers → ZATEN VAR · superpowers@claude-plugins-official kurulu (disabled)
- cloud memory (chat'ler arası hafıza) → önceki: kaynak-tarama/uzun-oturum/github.md · muhtemelen thedotmack/claude-mem
- impeccable / front end design yeteneği → ZATEN VAR · impeccable@impeccable kurulu (enabled)
- Task Observer (rebelytics/one-skill-to-rule-them-all, CC BY 4.0, 2.7k★) → ELE · skill (hook opsiyonel), her oturum ilk araçtan önce 52 KB SKILL.md ≈13k token + 3 todo'da bir log yazımı; auto-memory feedback + skill-creator ile çift

not: video 50 sn, sadece isim listesi; teknik detay/link yok.
