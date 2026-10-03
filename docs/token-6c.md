# TOKEN-6c — effort kayması · "diğer" kırılma teşhisi

## K1 Effort kayması
- Neden: oturum içinde `/effort xhigh` yapıldı (mod işi), CC bunu kalıcı yazdı. `/effort`, userSettings'te `modelSettings.<oturum modeli>.effortLevel` anahtarına yazar; `max` yazılmaz.
  - Kanıt: `~/.local/bin/claude.exe` 2.1.288, bayt 205779411: "For userSettings, takes effortLevel only and saves it as the default for the session's current model, under modelSettings as /effort saves it ('max' is session-only and is not written…)".
- Headroom Desktop'un payı yok, çünkü settings.json'a **anahtar yaması** ile yazıyor: güncel dosyayı okuyor, yalnız `root["env"]` anahtarına dokunuyor.
  - Kanıt: gglucass/headroom-desktop `src-tauri/src/client_adapters.rs#L3827-3851` (`configure_claude_settings_env_impl`) ve `#L4090-4100` (env anahtarı bazında kur/kaldır).
  - Pre-update snapshot yalnız Headroom'un kendi 3 durum dosyasını kapsıyor, settings.json yok (`storage.rs#L70-74`). Etkilenen değişiklik listesi bu yüzden gerekmedi.
- **Kullanım:** xhigh gereken oturum `claude --settings $HOME\.claude\xhigh.json` ile açılır. Oturum içinde `/effort` kullanılmaz.
  - `~/.claude/xhigh.json`: `{"modelSettings":{"claude-opus-5":{"effortLevel":"xhigh"},"claude-opus-5-5":{"effortLevel":"xhigh"}}}`. Oturum başı bayrak dosyasıdır, settings.json'a dokunmaz.
- Prob (claude -p 1/5): `claude -p "ok" --settings ~/.claude/xhigh.json --model claude-opus-5 --output-format stream-json --verbose`.
  - Sonuç: transcript'te `effort: "xhigh"` (ff9ba222, 13:29:29Z). settings.json sha 02372fb94f3e5e29 koşudan önce ve sonra aynı.
  - Sapma: probda `--model claude-opus-5` kullanıldı. Nedeni: varsayılan model opus-5-5'in settings.json değeri zaten xhigh, prob ayırt etmezdi. opus-5 için settings.json değeri `high`.
  - Effort düzeyi stream-json init'inde yok, yalnız `per_turn_effort_active` var. Kanıt transcript'teki `effort` alanı.
- Kalıntı: settings.json'da `claude-opus-5-5` hâlâ `xhigh`. Bu dalgada dokunulmadı, K4'te seçenek olarak duruyor.

## K2 "Diğer" kırılma teşhisi

Veri: 14 gün etkileşimli ana oturum, 148 kırılma / 22.17 M baştan yazma, taban 8376 kırılmasız istek (B; ttl_sim sınıflayıcısıyla birebir).

Kendi doğrulamam — edcf592d:649 (req_011CfcQdE4FJ1AHEXrBK4GPe): :640 cr=216573 (22:49:39) → :643-644 stop_hook_summary/turn_duration → :645 away_summary (22:52:44) → :646-647 queue-operation×2 (23:45:56) → :649 cr=7537 cc=203616 (23:46:03). Ara 56.4 dk, önceki yazma 1h TTL: önbellek canlıyken mesajlar baştan yazıldı. B'nin satırı tuttu.

| olay (arada) | kırılma % | taban % | kaldıraç |
|---|---|---|---|
| system/away_summary | 41.2 | 0.32 | 127.9× |
| file-history-snapshot | 26.4 | 0.69 | 38.1× |
| system/turn_duration · stop_hook_summary | 54.7 | 3.47 | 15.7× |
| queue-operation | 31.1 | 6.20 | 5.0× |
| agent-name | 28.4 | 19.90 | 1.4× |
| deferred_tools_record | 25.7 | 20.65 | 1.2× |
| ai-title | 49.3 | 46.14 | 1.1× |
| hook_success | 100 | 98.48 | 1.0× |
| output_style | 70.3 | 97.10 | 0.7× |

compact · /clear · effort/model değişimi: 0.

| ara süre | kırılma | taban | kırılma oranı | kayıp |
|---|---|---|---|---|
| ≤1 dk | 45 | 7428 | %0.6 | 5.49 M |
| 1–5 dk | 23 | 813 | %2.8 | 3.70 M |
| 5–30 dk | 68 | 132 | %34.0 | 11.25 M |
| 30–60 dk | 12 | 3 | %80.0 | 1.73 M |
| >60 dk | 0 | 0 | — | (TTL aşımı "ara>ttl" sebebine düşer) |

cache_read-at-break: <7.4k 5 · 7.4–8.4k 85 · 8.4–20k 23 · 20–100k 16 · >100k 19. En sık: 7551×28 · 8440×23 · 7537×22 · 7426×21 · 7430×10. Kırılma çoğunlukla baştaki ~7.5k'dan sonra: system(+araçlar) korunuyor, ilk mesajdan itibaren her şey yeniden yazılıyor.

Hipotezler:
- H1 away_summary: kaldıraç en yüksek (128×), örnekte 3 dk sonra üretilmiş. CC'de kapatılabilir: `qKe()` → `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` env ya da settings `awaySummaryEnabled:false` ("disable recaps in /config"; claude.exe dizgeleri). Zamanlamayı açıklıyor; kırılmanın konumunu (baş) açıklamıyor, özet sona eklenir. settings.json'da anahtar yok (varsayılan açık).
- H2 oturum başı blok: ≤1 dk'daki 45 kırılma (5.49 M) boşta kalmayla açıklanamaz; konum yine baş (≈7.5k). İlk mesajdaki enjekte blok (SessionStart çıktısı) değişiyor olabilir; örnek f3511826:708 (4 sn ara).
- H3a Headroom soğuk-önek yeniden sıkıştırması: ELENDİ. Opt-in env kapısı `HEADROOM_COLD_RECOMPACT` (handlers/anthropic.py:1614-1618), User/Machine'de yok, Headroom yapılandırmasında anılmıyor; proxy-6768.log'da "cold-prefix recompaction" 0 satır. Eşik kodla: `idle > ttl + 60` (transforms/cold_prefix.py:33,67), TTL CC isteğindeki cache_control'den (1h → 3600; :117-157) → 3660 sn. Tüm "diğer" kırılmalar ≤3600 sn'de, örnek 56.4 dk.
- H3b Headroom oturum durumu TTL'i (yeni aday): proxy/server.py:1095 `session_ttl_seconds=config.prefix_freeze_session_ttl` (CACHE modunda donuk önek takibi) ve :1680-1715 `COMPRESSION_CACHE_TTL_SECONDS` tembel süpürmesi (boşta kalan oturumun sıkıştırma önbelleği düşer). Durum düşerse sonraki istek baştan sıkıştırılır → system sonrası bayt farkı → cr ≈ system. 5 dk sınırındaki sıçrama (%2.8 → %34) buna uyuyor. Değerler henüz okunmadı; K3b doğrudan sınar.

En güçlü: boşta kalma kırılmalarında (5–60 dk: 80 kırılma, 12.98 M, kaybın %59'u) H3b; ≤1 dk'dakilerde H2. H1 zamanlamayla birlikte gidiyor ama mekanizması kanıtsız.

### K2 ek — Headroom'un iki süresi (kodla)

| süre | varsayılan | kanıt | nereden ayarlanır | bizde |
|---|---|---|---|---|
| prefix_freeze_session_ttl (önek izleyici temizleme) | 600 sn | proxy/models.py:342 `prefix_freeze_session_ttl: int = 600`; cache/prefix_tracker.py:1160-1162 `is_expired: idle > session_ttl_seconds`; :1321 süresi dolan izleyici yenisiyle değişir | env/CLI bağı yok: tek okuyucu proxy/server.py:1095; Desktop proxy'yi `proxy --port 6768 --no-http2 --no-rate-limit --log-messages` ile başlatıyor | 600 (değiştirilemez, yalnız kod yaması) |
| COMPRESSION_CACHE_TTL_SECONDS (oturum sıkıştırma önbelleği süpürmesi) | 3900 sn (1h + 5 dk) | proxy/helpers.py:1449-1454 `max(600, env)`; server.py:1680-1715 tembel süpürme | env `HEADROOM_COMPRESSION_CACHE_TTL_SECONDS` | ayarlı değil → 3900, 1h TTL ile zaten hizalı |

Kapalı opt-in kapılar (User/Machine env yok): HEADROOM_COLD_RECOMPACT · HEADROOM_NET_COST_POLICY (300 sn P_alive bozunumu, content_router.py:1244-1272).

İnce bantlar (aynı 148 kırılma): 0–1 dk %1 · 1–4 %2 · **4–5 %12** · 5–6 %15 · 6–8 %16 · 8–10 %14 · **10–12 %54** · 12–15 %45 · 15–30 %62 · 30–60 %80. İki basamak var:
- 600 sn'de (%14 → %54): izleyici süresiyle birebir. >10 dk kırılmaları 64 adet / 10.29 M (kaybın %46'sı). H3b'nin izi.
- ~4 dk'da (%2 → %12): away_summary orada başlıyor (4–10 dk kırılmalarının 19/25'inde var, ≤1 dk'da 0/45). H1'in izi; mekanizması (özet sona eklenir, baş neden kırılır) hâlâ kanıtsız.

## K3 Aralıksız kontrol · boşta kalma deneyi

Aralıksız kontrol (olcum/token-6c-k3.json): açık/kapalı birer koşu, 9'ar istek, ara yok → kırılma 0/0 ($0.84 / $0.63). Kalan 2 koşu (RAM kapısında durmuştu) yapılmadı, yerine K3b.

K3b (olcum/token-6c-k3b.json): kol başı 1. istek (README Read, sonnet, plan modu) → 2100 sn bekleme → aynı oturum `--resume` ile 2. istek. Bekleme 35 dk: kodla eşik TTL+60 = 3660 sn, +2 dk = 63 dk 1h TTL'i aşar ve iki kolu da kırardı (ayırt etmezdi). 35 dk, izleyici süresini (600 sn) 3.5 kat aşar. Her çağrı öncesi boş RAM ≥4.3 GB.

| kol | 1. istek sonu önek | 2. istek cache_read | 2. istek cache_creation | kırık |
|---|---|---|---|---|
| Headroom açık | 73193 | 73193 | 0 | yok |
| Headroom kapalı | 77802 | 77802 | 3874 | yok |

Açık kolun öneki 4609 token küçük: Headroom 1. istekte sıkıştırdı, 35 dk sonra (izleyici süresi dolmuşken) aynı baytları yeniden üretti (helpers.py:1436-1441 byte-identical swap, 3900 sn önbellek). İki kolda da kırılma yok → boşta kalma ve izleyici süresinin dolması tek başına kırmıyor; H3b zayıfladı. Kırılma etkileşimli oturuma özgü: claude -p'de away_summary üretilmez (H1), oturum başı enjeksiyonu farklı (H2). Sınır: tek araç sonucu, 2 istek; uzun geçmişte çoklu sıkıştırma sınanmadı. claude -p: 7/7.
