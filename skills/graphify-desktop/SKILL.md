---
name: graphify-desktop
description: "graphify CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu."
---

# graphify — bu arac Claude Code'da kosar, Desktop'ta kosmaz

graphify bir uv-tool Python venv'i (yerelde ~145 MB), kod agacini AST ile tarar ve `graphify-out/graph.json` uretir.
Desktop/claude.ai analiz sandbox'ina agsiz gomulemez: hem 30 MB sinirini asar hem de calismak icin proje kok dizinine erisim ister.

## Kullanim (yalniz Claude Code'da)

```text
graphify query "<soru>"
graphify path "<A>" "<B>"
graphify explain "<kavram>"
graphify update .
```

## Kompakt sorgu ve kesif sirasi (GRAPHIFY-ULTRA-1)

- Kesif sirasi: `graphify-out/GRAPH_REPORT.md` basliklari (harita) → kompakt sorgu → dosya yalniz kanit satiri icin dar aralikla (~20 satir).
- Kompakt sorgu: `python graphify_sor.py "<soru>" --kok <proje>` (omer-skills'te `.kos/kopru/graphify_sor.py`; claude.ai paketinde `scripts/graphify_sor.py`).
  Yalniz `graphify-out/graph.json` ister; cikti ≤40 satir: `sembol · dosya:satir · ozet` + cagiranlar/icerik.
  Sorudaki ad grafta yoksa `git grep` tanimi, o da yoksa `graphify query --budget 400`'e duser.
- Guncelleme: omer-skills'te `python .kos/kopru/graphify_hafif.py [kok]` (artimli ~4 sn, harita da yenilenir); ciplak `graphify update .` degil.
- claude.ai sandbox'inda graphify kosmaz, ama kullanici `graph.json` yuklerse (≤30 MB) `scripts/graphify_sor.py` onunla kosar.

## Desktop'te ne yapilir

1. Kullanicidan Claude Code'da yukaridaki komutu calistirip ciktiyi (ya da `graphify-out/GRAPH_REPORT.md` / `graphify-out/wiki/index.md` dosyasini) yapistirmasini iste.
2. Yapistirilan cikti bir dugum/kenar listesi ya da rapor metnidir; dogrudan bu metni oku ve soruyu ona gore yanitla — komutu Desktop icinde tekrar calistirmayi deneme.
3. `graphify path A B` ciktisi kisa yoldaki dugum adlarini sirayla listeler; `graphify explain X` ciktisi komsu dugumleri ve iliski turlerini verir.

## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k)

Bu arac sandbox'ta kosmaz, ama kullanicinin makinesinde **cc-kopru** MCP koprusu
kuruluysa Desktop sohbetinden gercekten kosturulabilir. Koprunun `komut` araci
Claude Code'un kendi allowlist'ini, PreToolUse/PostToolUse hook'larini ve
`permissions.deny` kurallarini uygular; kabuk yoktur, metakarakter reddedilir.

```
komut(arac="graphify", args=[...], cwd="C:/Projeler/<proje>")
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
