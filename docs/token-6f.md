# TOKEN-6f — Headroom sıcak önbellek kırılması

## K1 Mühür (dalga başı)

- settings d624c65bfad79cee · hooks f226ffce582b5bdc · mcpServers 50d989fb836cac49 (üst + proje) · mcp 19 · plugin 47/53 · skill 2068. settings ve hooks sha8'i TOKEN-6c-R ile aynı.
- Çalışan proxy: pid 39584, `%LOCALAPPDATA%\Headroom\headroom\runtime\python\python.exe`, bayraklar `--port 6768 --no-http --no-rate-limit --log-messages`. Sürüm **headroom-ai 0.39.0**. Ayrıca uv tool olarak 0.37.0 kurulu; bu yalnız CLI, trafik ona gitmiyor.
- Yamalanacak dosyalar (runtime venv, site-packages): `headroom/proxy/handlers/anthropic.py` a01ca8042ad8f293 · `headroom/cache/prefix_tracker.py` 6ffca9b3da0a6a58 · `headroom/transforms/cold_prefix.py` 0a02799830e77857.
- Mod: `--mode` bayrağı yok, `HEADROOM_MODE` de tanımsız. Bu yüzden varsayılan **cache** geçerli (`cli/proxy.py:1266`).
- OUTPUT_SHAPER: User ortam değişkeni olarak tanımlı (boolean kontrolü; değer basılmadı). /health runtime_env sha8 391552c0.
- OUTPUT_HOLDOUT: User/Machine/Process ortamında tanımsız. /health'te değeri var (f875a380), yani bellek içi runtime-env override'ı (`proxy/runtime_env.py:83` `_overrides`, `:108` `set_overrides`, `POST /admin/runtime-env`); dosyası yok. Kaynak koddaki varsayılan `"0"`: `proxy/handlers/anthropic.py:3371`.
- VERBOSITY_LEVEL: HOLDOUT ile aynı durumda, runtime-env override'ı (cc11310c). Varsayılan `DEFAULT_VERBOSITY_LEVEL = 2`: `proxy/output_shaper.py:92`, okunduğu yer `:126`.
- Headroom kendi testlerini paketle dağıtmıyor: site-packages altında `tests`/`test*` dizini 0.

## K2 Teşhis (salt okuma + çevrimdışı)

Satır numaraları runtime venv 0.39.0'a ait.

**Mod düzeltmesi.** Proxy'yi `headroom-desktop.exe` başlatıyor ve gömülü ortamında `HEADROOM_MODE=token` var. `HEADROOM_DEDUPE`, `HEADROOM_COLD_RECOMPACT`, `HEADROOM_CACHE_TTL_LEARN` ve `HEADROOM_BACKGROUND_COMPRESSION` de orada. Günlükte de `Mode: token` yazıyor (`~/.headroom/logs/proxy-6768.log:28224`). K1'deki "cache" tespiti yalnız CLI varsayılanıydı. Token modunda `_strict_previous_turn_frozen_count` (anthropic.py:1592) çalışmaz; 6c-R'deki zincirin bu halkası yanlıştı.

**frozen_message_count nasıl hesaplanıyor.**
1. `anthropic.py:1567` `resolve_tracker` çağrılıyor. Bu, konuşma lineage'ına göre tracker seçiyor (`prefix_tracker.py:1421-1490`). Gelen geçmiş, bir lineage'ın son isteğinin EXACT/MESSAGE_APPEND/BLOCK_APPEND devamıysa ya da tek bir BLOCK_REWRITE_TAIL adayı varsa o tracker seçiliyor. Yoksa yeni lineage açılıyor: `:1488`, taze tracker.
2. `anthropic.py:1579` `get_frozen_message_count()`. Taze tracker'da `_turn_number == 0` olduğundan **0** dönüyor (`prefix_tracker.py:926`).
3. `anthropic.py:1827-1831` `prepare_turn` → `min(tracker_frozen, cache_count)` (`session_engine.py:134`).
4. frozen == 0 ise `anthropic.py:1835-1840` kompress_background kuyruğuna alınıyor; tüm geçmiş arka planda sıkıştırılıp sonraki turda devreye giriyor. Ayrıca `read_maturation` (`:2345`) bütün geçmişe uygulanıyor. Önek baytları değişiyor ve sıcak önbellek kırılıyor.

**Neden sıcak önbellekte 0'a düşüyor: iki mekanizma.**
- **(i) Yan istek çatalı (recap/away_summary).** CC away_summary'yi ayrı bir API isteğiyle üretiyor. Bu istek aynı model ve aynı system ile gidiyor, dolayısıyla aynı session_id'ye düşüyor: `292f6584d88847f5`. Kanıt `proxy-6768.log.2:26467` `hr_1790960151_000850`: msgs=27 (ana tur 25+2), tok_out=86, cache_read=146847 (%100), bitiş 19:55:53.812. Transcript'teki away_summary kaydı 16:55:53.850Z, yani 38 ms sonra. Bu istek ana geçmişin MESSAGE_APPEND devamı olduğu için ana tracker'ı alıyor ve lineage zincirini `H + recap_user` ile eziyor. Sonraki gerçek tur `H + user` ise zincirin devamı sayılmıyor; `:1488`'de yeni lineage açılıyor ve frozen 0 oluyor. Önek H bayt bayt aynı ve önbellekte. Bozan CC değil, Headroom'un tek zincirli lineage eşleştirmesi.
- **(iii) Tracker TTL'i önbellek TTL'inden kısa.** `prefix_freeze_session_ttl = 600` (`proxy/models.py:342`) → `server.py:1092-1096` → `is_expired` (`prefix_tracker.py:1160-1162`) → `_maybe_cleanup` (`:1549-1565`) 10 dk boşta kalan tracker'ı siliyor. CC'nin önbelleği ise 1 saat; 6c-R 4–60 dk bandında Headroom dışı kırılma 0/67. Silinen tracker'ın yerine yenisi geliyor ve frozen 0 oluyor.
- **(ii) runtime-env yeniden yüklemesi: reddedildi.** `POST /admin/runtime-env` (`server.py:4014`) yalnız `runtime_env._overrides` sözlüğünü yazıyor (`runtime_env.py:108`). Tracker deposu tek kez kuruluyor (`server.py:1092`) ve hiçbir yerde temizlenmiyor.

**Yeniden üretim** (`scratchpad/yeniden_uret.py`). Headroom'un kendi `SessionTrackerStore`'u kullanıldı, API çağrısı yok. Sentetik dizi gerçek away_summary yapısından üretildi: içerik maskeli, 203 karakter.

| senaryo | önceki frozen | sonraki frozen | aynı tracker |
|---|---|---|---|
| kontrol: yan istek yok | 26 | 28 | evet |
| recap yan istek → user | 26 | **0** | hayır |
| (a) recap → away ayrı mesaj + user | 26 | **0** | hayır |
| (b) recap → away son user'a ekli | 26 | **0** | hayır |
| (a') away ayrı mesaj, yan istek yok | 26 | 28 | evet |
| (iii) 700 sn boşluk | 26 | **0** | hayır |
| (iii) 300 sn boşluk | 26 | 28 | evet |

away metninin kendisi bozmuyor; iki biçimde de bozan, ondan önceki yan istek.

**Günlük sayımı** (proxy-6768.log*, 10-02 16:23 → 10-03 19:49). frozen=0 + kompress_background/read_maturation + cache_read ≈ yalnız system olan kırılma 29. Dağılım: 600 sn üstü boşluk 7 (4'ünde away var) · yan istek çatalı 9 (3'ünde away var) · diğer 13. "Diğer" grubu sınıflanamadı, çünkü Headroom tam mesaj kaydı tutmuyor.

**Sonuç.** Kök neden Headroom'da: lineage çatal toleransı yok ve tracker TTL'i 600 sn'ye sabit. CC tarafında önceki tur değişmiyor, dolayısıyla DUR koşulu oluşmadı.

## K4 Yama

`tools/headroom_yama.py` kök nedeni düzeltiyor; yedek korumaya (sıcakken ertele) gerek kalmadı.
- `prefix_tracker.resolve_tracker`: EXACT/APPEND/REWRITE eşleşmesi yoksa ve gelen geçmiş, aynı affinity'deki **tek** bir zincirin son mesajı hariç tamamını aynen içeriyorsa, aynı tracker'a dönülür. `_fork_clamp` frozen'ı çatal noktasına kısar ve `update_from_response`'ta sıfırlanır.
- `is_expired`: `max(session_ttl_seconds, _cache_ttl_hint)`. `anthropic.py`'de `_cc_ttl`'in hemen ardından `prefix_tracker._cache_ttl_hint = _cc_ttl or 0` damgalanıyor. 5 dk istemcide davranış eskisi gibi 600 sn.
- Soğuk önek eskisi gibi: TTL üstü boşlukta tracker silinir; önek değişmişse çatal sayılmaz ve taze lineage açılır. İkisinde de frozen 0, kompress_background ve read_maturation tetiklenir.
- Betik: 0.39.0 dist-info ve iki dosyanın sha16'sı kilitli; farklı sürüm ya da bilinmeyen sha görürse hiçbir dosyaya dokunmadan DUR. Idempotent; `.token6f-yedek` alır; `--durum` ve `--geri-al` var. Yamadan sonra derleme denetimi yapar, kırıksa geri alıp DUR. `cold_prefix.py`'ye dokunulmadı.
- Kuruluma uygulandı: iki dosya yamalı, runtime venv import ok. Test 20/20: kurulu + yamalı kopyada sıcak 4 + soğuk 3, betik testleri 6.
- Bilinen tavan: aynı öneki paylaşan paralel kardeş çağrılar ilk ayrışmada bir tracker'ı paylaşır, ikinci turda ayrılır. Bu durum yamasızdan daha fazla kırılma üretmez; ilk ayrışmadaki kırılma ortadan kalkar.

## K5 Kazanç

Sentetik oturumda gerçek `ReadMaturationManager` koşturuldu ve held Read kırılma noktası modellendi. Eski = `.token6f-yedek`, yeni = yamalı. Ayrıntı `olcum/token-6f.json`'da.

| kompress oranı R | dönüşüm kazancı eski → yeni | ağırlıklı girdi eski → yeni |
|---|---|---|
| 0.02 | 867 190 → 941 194 (+%8.5) | 1 000 167 → 821 624 (−%17.9) |
| 0.05 | 896 565 → 961 091 (+%7.2) | 1 000 167 → 821 624 (−%17.9) |
| 0.10 | 945 518 → 994 238 (+%5.2) | 1 000 167 → 821 624 (−%17.9) |

Kazanç düşmüyor, artıyor. Taze tracker eski kolda ReadMaturationManager durumunu da sıfırlıyordu; yamalı kolda tutulan Read'ler olgunlaşmaya devam ediyor. Düşüş olmadığı için madde 21 tablosu gerekmedi. Kalite etkisi yok: yama içerik dönüşümünü değiştirmiyor, yalnız hangi mesajların donduğunu değiştiriyor.
