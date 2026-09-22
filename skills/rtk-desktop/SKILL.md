---
name: rtk-desktop
description: "rtk CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu."
---

# rtk — bu arac Claude Code'da kosar, Desktop'ta kosmaz

rtk tek statik ikili (10 MB, 30 MB sinirinin altinda) ve cekirdek alt komutlari (ls/tree/read/grep/json/diff/wc)
yerel/agsiz calisir — boyut/ag acisindan (a) adayiydi. Ama PATH'teki ikili Windows PE32+ formatinda; sandbox'in
kendi belgelenmis varsayimi Linux'dir (`tools/duman_claudeai.py`: `/mnt/skills`, dosyalar 644). Bir PE32+ ikili
Linux konteynerde calismaz; gercek hedefte calisir kanit uretilemedi. Karar bu nedenle (b).

## Kullanim (yalniz Claude Code'da)

```text
rtk read <dosya>
rtk grep "<desen>" <yol>
rtk tree <yol>
rtk diff <a> <b>
```

## Desktop'te ne yapilir

1. rtk sadece cikti yogunlugunu azaltan bir proxy'dir; Desktop'te dogrudan native araclari (grep, read) kullan.
2. Kullanici rtk ciktisi yapistirirsa: `[N lines omitted]` ya da `hash=...` isareti varsa, o kismin ozetlendigini bil — tam icerik gerekiyorsa kullanicidan `rtk proxy <komut>` ile tekrar calistirmasini iste.
3. `rtk json --keys-only` ciktisi yalniz anahtar adlarini listeler, degerleri degil.

## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k)

Bu arac sandbox'ta kosmaz, ama kullanicinin makinesinde **cc-kopru** MCP koprusu
kuruluysa Desktop sohbetinden gercekten kosturulabilir. Koprunun `komut` araci
Claude Code'un kendi allowlist'ini, PreToolUse/PostToolUse hook'larini ve
`permissions.deny` kurallarini uygular; kabuk yoktur, metakarakter reddedilir.

```
komut(arac="rtk", args=[...], cwd="C:/Projeler/<proje>")
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
