---
name: skill-ui-desktop
description: "skill-ui CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu."
---

# skill-ui — bu arac Claude Code'da kosar, Desktop'ta kosmaz

skill-ui, npm link ile bagli bir Electron uygulamasinin CLI ucu; repo (node_modules dahil) ~1.1 GB ve ana komutlari
(`mirror`, `upload`, `remote`) GitHub'a (@octokit/rest) yazar/okur. Desktop/claude.ai sandbox'ina ne boyut ne de ag erisimi nedeniyle gomulemez.

## Kullanim (yalniz Claude Code'da)

```text
skill-ui list
skill-ui read <skill>
skill-ui validate <skill-dir>
skill-ui mirror <github-url> [--dry-run]
```

## Desktop'te ne yapilir

1. `list`/`read`/`validate` ciktilari JSON'dir; kullanici yapistirirsa dogrudan alan alan yorumla (ad, aciklama, dosya listesi).
2. `mirror`/`upload` GitHub PR'i acar — Desktop'te tekrarlanamaz, kullaniciya Claude Code'da calistirmasini soyle.
3. Hata ciktisinda `--dry-run` bayragiyla calistirilmis bir sonuc varsa, gercek yazma islemi henuz olmadigini belirt.

## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k)

Bu arac sandbox'ta kosmaz, ama kullanicinin makinesinde **cc-kopru** MCP koprusu
kuruluysa Desktop sohbetinden gercekten kosturulabilir. Koprunun `komut` araci
Claude Code'un kendi allowlist'ini, PreToolUse/PostToolUse hook'larini ve
`permissions.deny` kurallarini uygular; kabuk yoktur, metakarakter reddedilir.

```
komut(arac="skill-ui", args=[...], cwd="C:/Projeler/<proje>")
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
