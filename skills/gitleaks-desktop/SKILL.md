---
name: gitleaks-desktop
description: "gitleaks CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu."
---

# gitleaks — bu arac Claude Code'da kosar, Desktop'ta kosmaz

gitleaks tek statik ikili (22.5 MB, 30 MB sinirinin altinda) ve ag istemiyor — boyut/ag acisindan (a) adayiydi.
Ama PATH'teki ikili Windows PE32+ formatinda; `tools/duman_claudeai.py`'nin kendi belgelediği sandbox varsayimi
Linux'dir (`/mnt/skills`, dosyalar 644). Bir PE32+ ikili Linux konteynerde calismaz (ELF yukleyici formati reddeder),
bu yuzden gercek sandbox'ta calisir kanit uretilemedi — yerel testte "gecti" gorunmesi Windows'de calisilmasindan,
gercek hedefte calisacagindan degil. Karar bu nedenle (b).

## Kullanim (yalniz Claude Code'da)

```text
gitleaks dir <yol>
gitleaks git <repo-yolu>
gitleaks detect --source <yol> --report-format json
```

## Desktop'te ne yapilir

1. Kullanicidan Claude Code'da taramayi calistirip ciktiyi yapistirmasini iste.
2. Her bulgu icin `RuleID`, dosya yolu ve satir numarasini oku; bulgunun DEGERINI (secret'in kendisini) asla tekrar yazdirma ya da raporla — yalniz kural adi ve konum bildir.
3. `--report-format json` ciktisi bir bulgular listesidir; bos liste = sizinti bulunmadi.

## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k)

Bu arac sandbox'ta kosmaz, ama kullanicinin makinesinde **cc-kopru** MCP koprusu
kuruluysa Desktop sohbetinden gercekten kosturulabilir. Koprunun `komut` araci
Claude Code'un kendi allowlist'ini, PreToolUse/PostToolUse hook'larini ve
`permissions.deny` kurallarini uygular; kabuk yoktur, metakarakter reddedilir.

```
komut(arac="gitleaks", args=[...], cwd="C:/Projeler/<proje>")
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
