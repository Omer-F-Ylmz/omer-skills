---
name: yetenek-getir
description: Searches the capability catalog (3.3k skills, agents, MCP, CLI, libraries, repo tools) by task to pick the right tool. Use when starting work, unsure which tool fits, or on out-of-domain work; most skills show only names. Not for running the tool itself.
---

# yetenek-getir — işe uygun aracı katalogdan bul

ajan-getir'in kardeşi. Skill listesinin çoğu yalnız ad gösterir; doğru aracı tahmin etme, ara.

## Ne zaman
- İşe başlarken uygun skill/ajan/MCP/CLI'dan emin değilsen.
- Alan dışı iş (departman-* kapsamında yok) ya da adından anlamı belli olmayan araçlar.

## Nasıl
1. Betik (CC ve kod çalıştırabilen claude.ai): bu klasördeki `katalog_ara.py` (katalog yanında: `yetenek.jsonl`)
   `python <bu skill klasörü>/katalog_ara.py "<iş tarifi TR/EN>" [--tur skill|ajan|mcp|cli|kutuphane|arac|plugin] [--tam]`
   (klasör — CC: `~/.claude/skills/yetenek-getir`, claude.ai: `/mnt/skills/user/yetenek-getir`)
   → işle ilgili HER kayıt (sabit ilk-N yok), türe göre gruplu: `ad · ne işe yarar · nasıl çağrılır`;
   30'u aşarsa grup başına ilk 5 + sayılar, hepsi için `--tam`.
2. claude.ai (betik çalışmazsa): bu klasördeki `yetenek.tsv` içinde iş sözcüğünü (Türkçe karakter yerine ASCII:
   karanlik, cakisma) ve İngilizce karşılığını ara (`grep -i -E "deadlock|kilitlen" yetenek.tsv | head -40`);
   sütunlar: ad · tür · kaynak · is · tetik (TR+EN anahtar) · cagri · durum.
3. En uygun 1–2 sonucu `cagri` sütunundaki yolla kullan: Skill adı · Agent tipi (listede yoksa Skill ajan-getir) ·
   ToolSearch ile MCP aracı · Bash CLI. Sonuç yoksa sorguyu İngilizce eş anlamla yeniden dene, sonra mevcut bilgiyle devam et.

## Kurallar
- `durum` "kapalı(override off)" olanı önermeden önce kullanıcıya söyle; kurulu olmayanı kurma.
- Arama başına tek komut; çıktıyı bağlama yapıştırma, yalnız seçilen aracı adıyla an.
- "(taslak, doğrulanmamış)" etiketli kılavuz kartını kullanmadan önce kaynağı (aracın SKILL.md'si) oku.
