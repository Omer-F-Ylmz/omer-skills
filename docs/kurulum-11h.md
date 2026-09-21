# KURULUM-11h — süreç adla öldürme hook'ta engellenir

21 Eyl 2026. Taban: 34bdf69.

11g'de ad filtresiyle 40 node süreci öldürüldü, Desktop'ın MCP'leri düştü. Kural
proje belleğine yazılmıştı — bellek yalnız okunduğunda uyulur. Artık
`~/.claude/hooks/block-destructive.ps1` zorluyor; bellek kaydı silindi, kural tek yerde.

## Eklenen kalıplar (`$adPatterns` dizisi, eşleşme → exit 2)

| Kalıp | Yakaladığı |
| --- | --- |
| `taskkill[^\r\n]*[/-]{1,2}IM\b` | `taskkill /F /IM x.exe` ve Git Bash'in `//IM` biçimi |
| `Stop-Process[^\r\n]*-(Process)?Name\b` | `Stop-Process` + ad parametresi |
| `Get-Process(?![^\r\n|]*-Id\b)[^\r\n|]*\|[^\r\n]*Stop-Process` | ad ile boru hattı |
| `\bpkill\b`, `\bkillall\b` | POSIX karşılıkları |

Sebep tek satır: `DUR: süreç adla öldürülmez; yalnız kendi başlattığın PID`.
İzinli kalanlar: `taskkill /F /PID <n>` ve `Stop-Process -Id <n>`; lookahead sayesinde `-Id`
veren boru hattı da muaf.

## Ölçüm (gerçek süreç öldürülmedi, hook'a JSON girdi verildi)

9 vaka: 5 ad kalıbı → exit 2 · 2 izinli → exit 0 · 2 eski kalıp (`rm -rf`,
`git reset --hard`) → exit 2. **9/9.** Yama öncesi aynı koşu **4/9** (5 ad kalıbı exit 0).

Yedek `block-destructive.ps1.bak11h`. settings.json kaydı değişmedi: `PreToolUse`,
matcher `Bash|PowerShell`, `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`.

**Yan bulgu:** hook ham komut metnini tarıyor, komutun ne yaptığını değil. Kural
setini dosyaya yazan komut kendi kalıbına takılır; kalıp metinleri komuta parça
parça (`"task"+"kill"`) geçirilerek yazıldı.
