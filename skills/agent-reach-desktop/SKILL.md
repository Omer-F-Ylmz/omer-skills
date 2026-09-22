---
name: agent-reach-desktop
description: "agent-reach CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu."
---

# agent-reach — bu arac Claude Code'da kosar, Desktop'ta kosmaz

agent-reach bir uv-tool Python venv'i; temel islevi URL/RSS/video icerigini internetten cekmek (Jina Reader, yt-dlp, gh, web-search).
Desktop/claude.ai analiz sandbox'inda ag erisimi olmadigi icin boyuttan bagimsiz olarak calisamaz.

## Kullanim (yalniz Claude Code'da)

```text
agent-reach skill <alt-komut>
agent-reach format <url>
agent-reach transcribe <url-veya-dosya>
agent-reach doctor
```

## Desktop'te ne yapilir

1. Desktop'in kendi web-search/fetch aracini kullan; agent-reach yalniz Claude Code tarafinda calisan bir kisayoldur.
2. Kullanici Claude Code ciktisini yapistirirsa: `format` komutu temizlenmis metin dondurur, dogrudan icerik olarak oku.
3. `doctor` ciktisi platform/kimlik dogrulama durumunu satir satir listeler; hata satirlarini kullaniciya oldugu gibi ilet.

## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k)

Bu arac sandbox'ta kosmaz, ama kullanicinin makinesinde **cc-kopru** MCP koprusu
kuruluysa Desktop sohbetinden gercekten kosturulabilir. Koprunun `komut` araci
Claude Code'un kendi allowlist'ini, PreToolUse/PostToolUse hook'larini ve
`permissions.deny` kurallarini uygular; kabuk yoktur, metakarakter reddedilir.

```
komut(arac="agent-reach", args=[...], cwd="C:/Projeler/<proje>")
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
