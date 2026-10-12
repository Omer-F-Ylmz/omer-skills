---
name: departman-verimlilik
description: "Verimlilik müdürü: token/context tasarrufu, çıktı sıkıştırma, oturum hafızası sırası. Uzun oturum, büyük log ya da maliyet işinde oku."
---

# Departman: verimlilik — iş sırası

Katalog: `docs/departmanlar/verimlilik.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

Skill dizini: bu klasörde `dizin.md` (Claude Code: alandaki TÜM kurulu skill'ler) ve `dizin-web.md` (claude.ai: yalnız yüklü olanlar) — ad — ne zaman. Adımdaki araç işe tam uymuyorsa ortamına uyan dizinde Grep ile işin anahtar kelimesini ara (Read etme), bulunan adı Skill aracıyla çağır; listede yalnız adı görünen skill de çağrılabilir. `ajan:` kayıtları alt ajandır: Claude Code'da Agent aracıyla (subagent_type = ad), claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula.

## Adımlar
1. **Komut çıktısı** — kabuk komutları `rtk` ile yoğunlaşır; sonuç kullanışsızsa `rtk proxy`.
2. **Büyük içerik** — log/tarama önce `jev log|triage`; gerekirse `headroom` sıkıştırma.
3. **Keşif** — kod sorusu önce `graphify` query; yapısal arama `smart-explore`.
4. **Hafıza** — geçmiş iş `mem-search`; oturum devri `context-save` / `context-restore`.
5. **Context** — mantıksal aralarda `strategic-compact`; dalga başında /clear; alt ajana test/log/araştırma.

## Kapılar
- Env değerleri hiçbir komutla yazdırılmaz.
- Ölçülmeden "tasarruf" iddiası yok (girdi/çıktı token sayıyla).
