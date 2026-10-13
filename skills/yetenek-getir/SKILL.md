---
name: yetenek-getir
description: Searches the capability catalog (3.3k skills, agents, MCP, CLI, libraries, repo tools) by task to pick the right tool. Use when starting work, unsure which tool fits, or on out-of-domain work; most skills show only names. Not for running the tool itself.
---

# yetenek-getir — işe uygun aracı katalogdan bul

ajan-getir'in kardeşi. Skill listesinin çoğu yalnız ad gösterir; doğru aracı tahmin etme, ara.

## Ne zaman
- İşe başlarken uygun skill/ajan/MCP/CLI'dan emin değilsen.
- Alan dışı iş (departman-* kapsamında yok) ya da adından anlamı belli olmayan araçlar.

## Nasıl (iki aşama: betik geniş aday listesi verir, seçimi sen yaparsın)
1. Aday listesi: `python ~/.claude/skills/yetenek-getir/katalog_ara.py "<iş tarifi TR/EN>" [--aday N] [--tur …]`
   (katalog yanında: `yetenek.jsonl`) → ~80–95 aday, türe göre gruplu, satır başına `ad · ne işe yarar` (+ `nasıl çağrılır` yalnız grup başlığındaki kalıptan farklıysa).
   `a, b · …` satırı aynı açıklamalı kopyalardır (ilgiliyse hepsi seçilir). Varsayılan N=80 + her türden en az 10; dar iş için `--aday 40`. Eski kısa eşik listesi: `--esik` (geri çağırması düşük).
   Çıktıda kısaltma notu (`compressed … hash=…`, `lines omitted`) varsa önce `headroom_retrieve` ile tam listeyi al; kısaltılmış listeden seçme.
2. İlgili = bu işin herhangi bir adımında (hazırlık, yapma, doğrulama, hata ayıklama, belgeleme) doğrudan kullanılacak kayıt;
   aynı işi yapan alternatifler ve kopyalar da ilgilidir ("başka araç zaten var" bırakma gerekçesi değildir). İki geçiş:
   a) Listeyi baştan sona oku, ilgili HER kaydı seç.
   b) Öz denetim: atlanan her adayda "bu işin bir adımında kullanılır mı?" → evetse ekle; seçilen her birinde "işle ilgisiz mi?" → evetse çıkar.
3. Seçilenleri türe göre plana koy (skill · ajan · mcp · plugin · cli · kütüphane · bizim betik), her biri hangi adımda;
   `cagri` yolu: Skill adı · Agent tipi (listede yoksa Skill ajan-getir) · ToolSearch ile MCP aracı · Bash CLI.
- claude.ai (betik çalışmazsa) aynı mantık: bu klasördeki `yetenek.tsv` içinde iş sözcüklerini (ASCII: karanlik, cakisma)
  ve İngilizce karşılıklarını geniş ara (`grep -i -E "deadlock|kilitlen|postgres|lock" yetenek.tsv | head -100`),
  aday listesini oluştur, sonra 2–3. adımlar. Sütunlar: ad · tür · kaynak · is · tetik (TR+EN) · cagri · durum.

## Kurallar
- `durum` "kapalı(override off)" olanı önermeden önce kullanıcıya söyle; kurulu olmayanı kurma.
- Arama başına tek komut; aday listesini kullanıcıya yapıştırma, yalnız seçilenleri adıyla an.
