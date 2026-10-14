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
5. **Context** — mantıksal aralarda `strategic-compact`; dalga başında /clear; alt ajana test/log/araştırma; toplu metin özeti Claude-dışı :free model (`.claude/ogren1/ozet.py` kalıbı, curl UA).
6. **Ölçüm** — `rtk gain` · headroom savings · `tools/token_olc.py` (`claude-usage today` bugünü göstermiyor).

## Kapılar
- Env değerleri hiçbir komutla yazdırılmaz.
- Ölçülmeden "tasarruf" iddiası yok (girdi/çıktı token sayıyla).

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:vid-ffmpeg-donusturucu
ajan:vrm-alt-ajan-dagitim
ajan:vrm-baglam-butcesi: sessions feel bloated
ajan:vrm-bilgi-tabani-hazirla: the same facts are re-explained often
ajan:vrm-cikti-sikistirma: tool output is large
ajan:vrm-hafiza-arama: asked what was done before
ajan:vrm-log-ozetleyici: a log is too long to read
ajan:vrm-maliyet-denetci: bills or limits rise
ajan:vrm-oturum-kaydi: Saves a short session handoff with state, decisions
### yalnız Claude Code
aks-gpu-inference: : setup (airunway-aks-setup), non-GPU incidents (aks-troubleshooting), standalone VM
behavioral-consistency: Ensuring the AI behaves predictably across sessions, edge
cli:claude-monitor: plan limiti canlı izleme
cli:claude-usage: jeton/maliyet kullanım raporu
empathy-map: sharing user understanding quickly
freeze: Restrict file edits to a specific directory for
hicks-law: a screen offers too many options at once
mcp:codebase-memory-mcp: kod tabanı grafı: çağıran/çağrılan sorgu
mcp:codegraph: kod sembol grafı, etki analizi
mcp:context-mode: büyük çıktıyı kum havuzunda işle, indeksle
mcp:headroom: sıkışık araç çıktısının aslını hash ile al
mcp:qmd: yerel markdown notlarda arama
mcp:serena: LSP ile sembol bul/düzenle
millers-law: grouping fields, menu items, or steps
omni-resilience: Monitor provider health, circuit-breaker states, p50/p95/p99 latency metrics
tone-calibration: Adjusting formality, warmth, confidence, and style per context
<!-- dizin:son -->
