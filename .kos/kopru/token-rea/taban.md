# TOKEN-REA d1 — TABAN (20 Eki 2026)

Betik: `taban.py` (vekil yakalama + ücretsiz `count_tokens`, a6.py kalıbı) → ham veri `taban.json`. Token = gerçek API `count_tokens`; /context Skills satırı kullanılmadı.
Ölçüm maliyeti: 3 `claude -p` (başlık yakalama) + 56 count_tokens; RAM %75–79 (≤%88). A = araç kapalı (çıplak), B = araç açık.

## Araç başı 4 eksen
| Araç | Performans (süre) | Kalite (tohumlu set) | Kullanışlılık | Token katkısı (A→B) |
|---|---|---|---|---|
| RTK 0.49.0 | 1.73→2.23 sn / 10 komut | 10/10 → **8/10** (`rtk ls -la tools` dosya adını düşürdü; `rtk git diff HEAD~2` uzun adları düşürdü) | 0 adım (hook), hata 0/10 | 173 588→121 517 (**−%30.0**); `git status` 16 418, `git log --stat` 33 781, `rtk read` (+`-l aggressive`) 0 kazanç. Üretim: 39 554 komut, 44.8M, −%81.7 |
| Headroom 0.37.0 (proxy) | proxy şeffaf | üretimde sorun gözlenmedi; kütüphane `compress()` 6/6 | 0 adım | Üretim 14 gün: opus-5-5 −%28.1 (3.50G→0.98G tasarruf), sonnet-5-5 −%32.7, haiku-5-5 −%30.0, **toplam ≈1.78G / 6.20G = −%28.8**; sonnet-5 −%0.2 |
| Headroom `compress()` API (6 dosya) | 29.9 sn (ilk çağrı 21 sn: Kompress modeli HF'den hazır değil → 20 sn aşımında PASSTHROUGH) | 6/6 | uv python gerekir (`No module named headroom` sistem python'unda) | 76 909→76 283 (**−%0.8**) |
| graphify 0.9.88 query | 1.32→34.6 sn / 10 sorgu (3.5 sn/sorgu) | beklenen sembol **6/10** (git grep 9/10) | 1 adım, hata 0 | 52 535→41 693 (**−%20.6**); çıktı ≈3.4k sabit (soru ne olursa); graf 48.9k düğüm, kirli |
| claude-mem 13.31.0 search | 6.2 sn / 10 sorgu (0.6 sn) | isabet 9/10 (araç kapalı 0/10) | 1 adım (HTTP), hata 0 | 5 176 token / 10 sorgu (~518/sorgu); maliyet tarafı: SessionStart enjeksiyonu bkz. profil |
| BEYİN (`tools/beyin.py`) | — | hakem betik 19/20 (çok 7/8) | — | mevcut kapı verisi (`.claude/beyin4/kapi.log`, yeniden koşulmadı): token A/B = %48 (tohum 2010), %42 (tohum 2011) |
| CLAUDE.md/dalga.md/SessionStart + CC ayarları | — | — | — | Sabit bağlam (köprü ajan profili) **30 591 token**: araçlar 14 072 · sistem 1 896 · hook enjeksiyonu (claude-mem + superpowers + context-mode + ponytail …) **14 612** |
| context-mode · OmniRoute · jev · qmd · NotebookLM · mcp-memory | ölçülmedi | ölçülmedi | ölçülmedi | NEDEN: MCP yalnız etkileşimli CC'de (context-mode, mcp-memory); NotebookLM Google oturumu ister; OmniRoute/jev/qmd için tohumlu set d2'de. OmniRoute mevcut kapı: lisans 43/43, özet %92.9 (token.md) |

Held-out: her tohumlu sette (10 madde) ayrı 4–5 maddelik held-out adı `taban.json > held_out_muhurlu` altında mühürlü; d1'de koşulmadı, d2 kapısında tek seferlik kullanılır. Bunlar yalnız ad listesi; soru metni d2'de yazılacak (d1 sınırı).

## Toplam taban — 3 iş profili (gerçek API kullanımı, oturum jsonl, son 14 gün, mesaj-id tekilleştirilmiş)
Sınıflama proje klasörü adına göre (sezgisel): kod dalgası = omer-skills + worktree'ler; araştırma = ogren/video; köprü = kopru/ajan-sira/envanter/ig-chrome. claude-mem observer hariç.
| Profil | Oturum | Girdi+çıktı (cache hariç) | Ham toplam (cache dahil) | Ağırlıklı (girdi×1, okuma×0.1, yazma×1.25, çıktı×5) | Medyan oturum (ham) |
|---|---|---|---|---|---|
| Kod dalgası | 1000 | 47.5M | 1 979.4M | 454.8M | 1.53M |
| Araştırma | 78 | 0.73M | 15.2M | 4.7M | 8.6k |
| Köprü kontrolü | 184 | 4.17M | 125.1M | 38.1M | 222k |
| **Toplam** | 1262 | **52.4M** | **2 119.7M** | **497.6M** | — |

d2 hedefi: ağırlıklı 497.6M üzerinden ≥%50–60 ek tasarruf = ≤ 199–249M. En büyük kalem cache okuma (kod dalgası 1.80G ham): sabit bağlamı (30.6k/istek) ve tur sayısını küçültmek en büyük kaldıraç.

## Sınırlar / dürüst notlar
- Kalite setleri tohumlu ve küçük (10 madde); RTK/graphify "kalite" = beklenen anahtarın çıktıda kalması (anlam hakemi yok). claude-mem 9/10 isabet çoğu sorguda anahtar kelime zayıf; d2'de hakemli set.
- `taban.py` ilk koşusunda graphify süresi 34.6 sn toplam; süre eksenindeki RAM ölçülmedi (psutil yok, yalnız sistem RAM% öncesi/sonrası).
- BEYİN satırı yeniden ölçülmedi, mevcut kapı kaydıdır. REA native analiz Ghidra ister → kurulmadı.
