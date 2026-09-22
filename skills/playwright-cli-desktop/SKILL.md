---
name: playwright-cli-desktop
description: "playwright-cli CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu."
---

# playwright-cli — bu arac Claude Code'da kosar, Desktop'ta kosmaz

playwright-cli'nin kendisi kucuktur ama gercek islevi (tarayici otomasyonu) icin `playwright install` ile ayrica
indirilen tarayici ikilileri (Chromium/Firefox/WebKit, yuzlerce MB) gerekir. Desktop/claude.ai sandbox'inda ag
erisimi olmadigindan bu indirme yapilamaz; paket olarak gomulse bile calisir hale gelmez.

## Kullanim (yalniz Claude Code'da)

```text
playwright-cli open <url>
playwright-cli snapshot
playwright-cli click <hedef>
playwright-cli eval "<js>"
```

## Desktop'te ne yapilir

1. Desktop'in kendi tarayici/otomasyon araci (varsa) kullanilir; playwright-cli yalniz Claude Code tarafinda calisir.
2. Kullanici bir `snapshot` ciktisi yapistirirsa: bu, sayfadaki elemanlarin ref numarali agac gorunumudur — ref'lere gore elemanlari tarif et.
3. `eval` ciktisi JS ifadesinin donen degeridir; JSON ise alan alan yorumla.

## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k)

Bu arac sandbox'ta kosmaz, ama kullanicinin makinesinde **cc-kopru** MCP koprusu
kuruluysa Desktop sohbetinden gercekten kosturulabilir. Koprunun `komut` araci
Claude Code'un kendi allowlist'ini, PreToolUse/PostToolUse hook'larini ve
`permissions.deny` kurallarini uygular; kabuk yoktur, metakarakter reddedilir.

```
komut(arac="playwright-cli", args=[...], cwd="C:/Projeler/<proje>")
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
