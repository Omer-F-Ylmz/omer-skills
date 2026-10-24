# BASLANGIC-HIZ-2 · P4 — mod_yama uygulaması

**Sonuç: KAZANÇ YOK → `--geri` yapıldı, DUR.** Gerçek ayarlarda geçiş sayısı 27 → 27 (hedef ≤13 tutmadı).

## Yapılan
- `tools/mod_yama.py` (--uygula|--geri|--durum; SHA-256 kaydı `.kos/kopru/mod-yama.json`; yedek `.kos/kopru/yedek/mod-yama/<mod>/`; CRLF korunur; kalıp tutmayan ATLANIR). Birim testi `tools/tests/test_mod_yama.py` 5/5 (uygula→geri bayt bayt aynı, güncellenmiş mod dokunulmaz). Commit 3c0687c.
- `--uygula`: 10 mod yamalandı (agent-radar, browser-lanes, context-bar, glance, merge-gate, mission-control, prayer-times, session-saver, switchboard, where-am-i). 15 değil: now-playing (register'dan önce erken return), replay-theater/snake/heatmap (yalnız Pane render), cache-clock/reels (kalıp dışı) ATLANDI; kalan 8 modda zaten komut kaydı yok.
- Dosya düzeyi doğrulama: 10 modda register tek seferlik `ui.render` bloğunda (test + `--durum`).

## Ölçüm (`claude -p x --model haiku --debug-file --strict-mcp-config`)
| Kol | Süre | Geçiş |
|---|---|---|
| önce | 217 s / 212 s (+226 s MCP'siz değil: 29) | 27 / 27 (29) |
| sonra | 188 s | 27 (2. koşu 300 s zaman aşımı) |
Süre yük altında (başka `claude -p` işleri, RAM boş ~5 GB) ±%15 oynuyor; geçiş sayısı sabit 27 → yama etkisiz.
Sapma: `--strict-mcp-config` eklendi (gerçek ayarlı koşular MCP npx 240 s zaman aşımında asılıyordu: 4 koşudan 3'ü).

## Neden etkisiz (varsayım, doğrulanmadı)
P3 kontrolü 3 eklentiyle 4→3 gösterdi; 69 eklentili gerçek kurulumda `-p` geçişleri başka yükleme yollarından (log'da "workflows loaded: 7" tekrarları) geliyor, register satırı sayısı da önce/sonra 30. Kök neden kanıtlanmadan yeni deneme yok.

## Durum
Mod dosyaları orijinal (marketplace git temiz), `mod-yama.json` boş, `claude plugin list` etkilenmedi. Etkileşimli doğrulama yapılmadı (yasak). Süreç artığı: yok.
Maliyet ≈$1.3 (hedef $0.50 aşıldı: 4 koşunun MCP asılması + 2 zaman aşımı).
