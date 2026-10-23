---
name: departman-verimlilik
description: "Verimlilik müdürü: token/context tasarrufu, çıktı sıkıştırma, oturum hafızası sırası. Uzun oturum, büyük log ya da maliyet işinde oku."
---

# Departman: verimlilik — iş sırası

Katalog: `docs/departmanlar/verimlilik.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

## Adımlar
Ölçülmüş kartlar, kombin zincirleri ve karar ağacı: `docs/ogren/token.md` (ÖĞREN-1).
1. **Komut çıktısı** — kabuk komutları `rtk` ile yoğunlaşır; sonuç kullanışsızsa `rtk proxy`. Dosya yapısı (düzenleme değil): `rtk read -l aggressive` (−%86).
2. **Büyük içerik** — log/tarama önce `jev log|triage`; gerekirse `headroom` sıkıştırma; Desktop'a yapıştırmadan önce `headroom-compress` (JSON −%54).
3. **Keşif** — `.kos/kopru/harita` → sembol adıyla `graphify_sor.py` (−%99 ↔ query) → `graphify explain|path`; belge metni `qmd search`; yapısal arama `smart-explore`.
4. **Hafıza** — geçmiş iş `mem-search` (köprüde MCP yok: worker HTTP `/api/search`); oturum devri `context-save` / `context-restore`.
5. **Context** — mantıksal aralarda `strategic-compact`; dalga başında /clear; alt ajana test/log/araştırma; toplu metin özeti Claude-dışı :free model (`.claude/ogren1/ozet.py` kalıbı, curl UA); küçük yan iş (lisans/özet) → `tools/ucuz_alt.py --tur` (yalnız :free zincir `cc-ucuz-free`, doğrulanmazsa çıkış 3 → Claude doğrular; ücretliye kendiliğinden yükselmez).
6. **Ölçüm** — `rtk gain` · headroom savings · `tools/token_olc.py` (`claude-usage today` bugünü göstermiyor).

## Kapılar
- Env değerleri hiçbir komutla yazdırılmaz.
- Ölçülmeden "tasarruf" iddiası yok (girdi/çıktı token sayıyla).


Slash katalog (iş türü → /komut·skill): `yetenek-getir/reference/slash-katalog.md` — Read; oturuma yüklenmez.

Kombo adayları (A/B ölçümü geçmedi; önerme, yalnız ipucu): tk-log-okuma, tk-model-merdiveni.

<!-- dizin:bas -->
## Dizin: adımdaki araç işe uymuyorsa `references/dizin.md` dosyasını oku, listeden adla çağır.
<!-- dizin:son -->
