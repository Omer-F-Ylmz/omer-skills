---
name: departman-verimlilik
description: "Verimlilik müdürü: token/context tasarrufu, çıktı sıkıştırma, oturum hafızası sırası. Uzun oturum, büyük log ya da maliyet işinde oku."
---

# Departman: verimlilik — iş sırası

Katalog: `docs/departmanlar/verimlilik.md`.

## Adımlar
1. **Komut çıktısı** — kabuk komutları `rtk` ile yoğunlaşır; sonuç kullanışsızsa `rtk proxy`.
2. **Büyük içerik** — log/tarama önce `jev log|triage`; gerekirse `headroom` sıkıştırma.
3. **Keşif** — kod sorusu önce `graphify` query; yapısal arama `smart-explore`.
4. **Hafıza** — geçmiş iş `mem-search`; oturum devri `context-save` / `context-restore`.
5. **Context** — mantıksal aralarda `strategic-compact`; dalga başında /clear; alt ajana test/log/araştırma.

## Kapılar
- Env değerleri hiçbir komutla yazdırılmaz.
- Ölçülmeden "tasarruf" iddiası yok (girdi/çıktı token sayıyla).
