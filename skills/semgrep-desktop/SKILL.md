---
name: semgrep-desktop
description: "semgrep CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu."
---

# semgrep — bu arac Claude Code'da kosar, Desktop'ta kosmaz

semgrep bir uv-tool Python venv'i; kural motoru ve dil analizoruyle birlikte yerelde ~333 MB — Desktop/claude.ai
sandbox'inin 30 MB gomme sinirini cok asar, agsiz kurulum da mumkun degildir.

## Kullanim (yalniz Claude Code'da)

```text
semgrep scan --config auto <yol>
semgrep scan --config p/security-audit <yol>
```

## Desktop'te ne yapilir

1. Kullanicidan Claude Code'da taramayi calistirip ciktiyi (metin ya da `--json`) yapistirmasini iste.
2. Her bulgu icin dosya:satir, kural id'si ve mesaj alanlarini oku; onem sirasina gore (ERROR > WARNING > INFO) ozetle.
3. Desktop taramayi tekrar calistiramaz; yalniz yapistirilan ciktiyi yorumlar.

## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k)

Bu arac sandbox'ta kosmaz, ama kullanicinin makinesinde **cc-kopru** MCP koprusu
kuruluysa Desktop sohbetinden gercekten kosturulabilir. Koprunun `komut` araci
Claude Code'un kendi allowlist'ini, PreToolUse/PostToolUse hook'larini ve
`permissions.deny` kurallarini uygular; kabuk yoktur, metakarakter reddedilir.

```
komut(arac="semgrep", args=[...], cwd="C:/Projeler/<proje>")
```

Kurallar:

- `arac` allowlist'te olmali; `cwd` yalniz `C:/Projeler` ya da `C:/Users/pc/Desktop` altinda.
- Yasak alt komutlar (install/login/publish/token ...) ve inline kod bayraklari (`-e/-c/-p`) reddedilir.
- Cikti 8 KB'i asarsa Headroom'a verilir; `hash=...` gorursen tamamini
  `headroom_retrieve` ile ac.
- Kopru yoksa asagidaki bolumler gecerlidir: arac kosmaz, yalnizca sablon yorumlanir.

Koprunun oteki araclari: `ajan` (gercek `claude -p` oturumu), `oturum` (SessionStart +
CLAUDE.md), `katalog` (acik komut/agent/skill listesi), `durum` (statusline + Headroom +
claude-mem + gunluk token), `oturum_ozeti` (claude-mem ozeti), `kaydet` (gitleaks'ten
gecen not).
