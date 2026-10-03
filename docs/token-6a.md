# TOKEN-6a — Headroom + oturum başı enjeksiyonları: teşhis ve ölçüm

Ayar, hook, skill, plugin, MCP ve Headroom ayarı değişmedi. Env değeri yazılmadı (varlık yalnız var/yok). Veri: `olcum/token-6a-k1.json`, `olcum/token-6a-k2.json`.

## K1 Headroom yönlendirmesinin sessiz kapanması

**Kök neden.** `env.ANTHROPIC_BASE_URL` ve `env.ENABLE_TOOL_SEARCH`'i silen ve geri yazan Headroom Desktop'tır (gglucass/headroom-desktop, MIT, `src-tauri/src/`, main dalı; satırlar kayabilir). Guard hook kök neden değil.

- Guard: `~/.claude/hooks/headroom-claude-guard.py:2` "managed by Headroom Desktop". SessionStart'ta (`settings.json:462-471`) çalışır, settings'i yalnız okur (`:80-91`), 127.0.0.1:6767'yi yoklar (`:72`, `:126`), `.headroom-guard-verdict.json`'a yalnız `{at, issues}` yazar (`:23-32`). Dosya her koşuda üzerine yazılır, geçmiş tutmaz; son durum `issues=[]`.
- Silen yollar: çıkış `lib.rs#L6947-6948` ("exit: clear_client_setups", RunEvent `#L7825`) · pause düğmesi `lib.rs#L6343` · proxy sağlık denetimi hatasında auto-pause `lib.rs#L10705` · uygulama çökerse ayrı bekçi süreç `lib.rs#L6767`, `client_adapters.rs#L1608-1616` · 6767'yi yabancı süreç tutuyorsa `client_adapters.rs#L1577` · kaldırma `client_adapters.rs#L1881-1920`.
- Geri yazan yollar: açılışta `restore_client_setups` (`client_adapters.rs#L2696`, çağrı `lib.rs#L7649`) · resume `lib.rs#L6246` · port geri alınınca `client_adapters.rs#L1594-1597` · bypass/auto-pause bitince `lib.rs#L4171`. Önceki değer `remembered_clients`'ta saklanır (`client_adapters.rs#L2696-2700`). `ENABLE_TOOL_SEARCH` yalnız boşsa yazılır (`#L20-28`).

**Kapalı dönemler** (`~/AppData/Local/Headroom/headroom-desktop.log`, `olcum/token-6a-k1.json` → `desktop_olay`):

| başlangıç | bitiş | süre | neden |
|---|---|---|---|
| 10-01 04:48:59 | 10-01 13:20:22 | 511 dk | proxy.log sessiz; desktop günlüğü 10-01 20:22'den başlar, neden kanıtsız |
| 10-02 16:22:02 | 10-02 ~16:24 | ~2 dk | güncelleme ("pre-update snapshot") |
| 10-02 22:23:50 | 10-02 22:25:30 | 100 sn | çıkış → açılış |
| 10-03 04:22:01 | 10-03 13:49:18 | 567 dk | çıkış → açılış |

Settings yedekleri aynı anları doğrular: `settings.json.headroom-backup-20261002192530` ve `-20261003104918` (adlar UTC) iki anahtarı da taşımaz; 09-20 17:19 öncesi yedekler Headroom kurulmadan önceye ait.

**Süre ölçülebilir mi.** Kısmen. Kesin kapalı süre yalnız desktop günlüğündeki çıkış/açılış çiftlerinden çıkar (günlük 10-01 20:22'den). `~/.headroom/savings_events.jsonl` (09-20 17:43'ten) istek izi verir ama boşta kalmayı kapalılıktan ayırmaz. `proxy.log` 10 MB rotasyonla yalnız 10-01'den beri var.

**14 günde kapalı-dönem payı** (pencere 09-19 14:00 → 10-03 14:19; transcript `requestId` tekil; "kapalı" = en yakın savings olayına uzaklık eşiği aşar; proxy dönemi = 10-01 04:01 sonrası, `x-claude-code-session-id` ↔ `sessionId` ±900 sn):

| giriş | istek | Headroom öncesi | sonra | >300 sn | >600 sn | proxy dönemi eşleşen |
|---|---|---|---|---|---|---|
| cli | 6444 | 1236 | 5208 | 0 | 0 | 1078/1078 |
| sdk-cli | 897 | 3 | 894 | 1 | 0 | 607/607 |
| sdk-ts | 707 | 5 | 702 | 5 | 2 | 0/285 |

- Headroom kurulduktan sonra cli+sdk-cli 6102 isteğin 600 sn eşiğinde 0'ı, 300 sn eşiğinde 1'i kapalı dönemde. Uzun kapalı pencereler gece boşta kalmayla çakışıyor. Kapanış sessiz, ama bugüne kadar maliyeti ≈%0.
- Yan bulgu: `sdk-ts` istekleri claude-mem observer oturumları (1044 transcript, `C--Users-pc--claude-mem-observer-sessions`, 50.4 oturum/gün). Proxy döneminde 285 isteğin hiçbiri proxy.log'da oturum eşleşmesi vermedi: Headroom'dan geçmiyorlar ya da başlıksız geçiyorlar (neden kanıtsız).
- Ölçüt: oturum kimliği eşleşmesi güvenilir. "compressed … hash=" işareti ve `headroom_retrieve` kullanımı yalnız var-yönlü; yoklukları bypass kanıtlamaz.

**Çözüm seçenekleri** (müdahale düzeyine göre):
1. Görünür uyarı: statusline'da `env` anahtarı var/yok + 6767 yoklaması ("HR kapalı"); ya da kendi SessionStart hook'umuzla tek satırlık uyarı. Guard dosyası Desktop'a ait, güncellemede yeniden yazılır; ona dokunulmaz. Tasarruf etkisi 0, kalite riski 0.
2. Otomatik geri yazma: Desktop'un `remembered_clients` mantığıyla yarışır; Desktop kapalıyken yazmak CC'yi ölü porta yönlendirir (API hatası). Önerilmez.
3. Headroom ayarı: çıkış/pause'ta temizleme tasarım gereği (proxy yokken istemciyi kırmamak). Değiştirmek önerilmez.

Öneri: 1. Pay ≈%0 olduğu için sorun maliyet değil görünürlük.

## K3 Çıktı kısaltma (L12) ayrıştırma tasarımı

**Mekanizma** (uv kurulumu headroom-ai 0.37.0, `~/AppData/Roaming/uv/tools/headroom-ai/Lib/site-packages/headroom/proxy/handlers/anthropic.py:3116-3175`; Desktop venv 0.39.0'da aynı blok `:3338`; 6767/6768'i hangisinin sunduğu kanıtsız):
- Treatment kolundaki her isteğe sistem isteminin sonuna `<headroom_output_shaping>` bloğu eklenir (`anthropic.py:3169-3171`, `output_steering.py:16`). Metin seviyeye göre (`output_verbosity_policy.py:13-36`); seviye 2 (okuma sıkışık geldi, alıntı yaklaşık): "Skip preamble and postamble; start with substance. Never restate code, file contents, diffs, or tool output already in this conversation — reference path and line instead. After tool call succeeds, continue without narrating result."
- Tur türü talimatı değiştirmez. `classify_turn` (`output_turn_policy.py:9-15`) yalnız effort yönlendirmesini etkiler: `MECHANICAL_CONTINUATION` turunda `output_config.effort` → `HEADROOM_MECHANICAL_EFFORT` (varsayılan `low`) (`output_shaper.py:204-239`). TOKEN-0 L12 satırındaki "tur türüne göre" bu yüzden kaba.
- Koşul: bypass değil (`anthropic.py:3121`) · shaper açık (`HEADROOM_OUTPUT_SHAPER` truthy ya da rollout `proxy_output_shaper` BETA; `output_shaper.py:116`, `rollout.py:105`) · kol treatment. Seviye sırası `HEADROOM_VERBOSITY_LEVEL` → autotune → `~/.headroom/verbosity.json` → 2 (`output_shaper.py:142-189`).
- Holdout istek ya da oturum başına değil: konuşma anahtarı `sha256(model + ilk user metni[:512])` (`output_savings_policy.py:108-130`), `sha256("arm:"+anahtar)[:8]/0xFFFFFFFF < oran` ise control (`:157-165`). Aynı ilk mesajla başlayan konuşmalar hep aynı kola düşer. Etiket `transforms_applied`'a (`anthropic.py:3167`), defter `~/.headroom/output_savings.json`'a (`output_savings.py:479`; şu an yalnız baseline 8 stratum, treatment/control boş).
- Bugün shaper kapalı: 8 proxy günlüğünde OutputShaper/stratum/holdout satırı 0; `HEADROOM_OUTPUT_HOLDOUT` tanımlı değil.

**Önceki ölçüm** (`docs/denemeler/headroom-ayar-sonuc.md:3-32`): 2026-09-24, sonnet, 4 okuma görevi, 3 kol (doğrudan · headroom-mevcut · headroom-wrap) × 2 koşu = 24 `claude -p`, $8.79, kalite 0-3 (gürültü bandı 0.34). Çıktı 582→358 (−%38.5), kalite 2.50→2.62, girdi −%37.4. Kollar yalnız proxy↔doğrudan farkını ölçer; shaper'ın o sırada açık olup olmadığı ayrılmadı. −%38.5 = sıkıştırma + (varsa) shaper + gürültü. Görev başına n=2; en büyük düşüş tek görevde (`2-json-alan`, `:21-22`).

**20 Eylül.** `~/.headroom/verbosity.json`: `learned_at 2026-09-20T14:37:39Z`, seviye 2, kaynak heuristic. `headroom learn --verbosity --apply` çalışan proxy'ye `POST /admin/runtime-env {"HEADROOM_OUTPUT_SHAPER":"1"}` gönderip shaper'ı açar (`cli/learn.py:404-425`, çağrı `:577`); yani learn shaper'ı açabiliyor. Kapatma gerekçesi repoda ve hafızada yok (kanıt yok); bugün kapalı olduğu günlükten kesin.

**HEADROOM_OUTPUT_HOLDOUT A/B tasarımı** (bu dalgada koşulmadı):
- Kollar: T = shaper açık + `HEADROOM_OUTPUT_HOLDOUT=0` (hepsi treatment) · C = shaper açık + `HEADROOM_OUTPUT_HOLDOUT=1` (hepsi control). Aynı proxy, aynı sıkıştırma; fark yalnız shaper talimatı. Oranlı holdout kullanılmaz: anahtar ilk mesaja bağlı, küçük n'de kol dengesi tutmaz.
- Geçiş: bayraklar proxy sürecinin env'i; Desktop'un proxy'sine koşu başına `POST /admin/runtime-env` (learn'ün yolu), bitince eski değer. Bu bir Headroom ayarı değişikliği → TOKEN-6b'de onayla.
- Geçerlilik: her koşuda proxy günlüğünde kol/stratum etiketi görülür; görülmezse koşu geçersiz.
- Görevler: rtk-ab kısa görev (`C:\Users\pc\Desktop\rtk-ab`, `docs/token-4a.md:94-98` tabanı) + orta görev (tools/video/video modülünde değişiklik + testi, ayrı worktree).
- Koşu: en fazla 6 — kısa 2T + 2C, orta 1T + 1C; T/C dönüşümlü; Opus 5.5.
- Metrik: görev başarısı (test/kabul) · kör puan (okuyucu, kol gizli, 0-3) · çıktı token · toplam ağırlıklı · $.
- Karar, madde 21 (`C:\Projeler\omer-kurallar.md:23`): kalite düşüşü = kalite puanı ve görev başarısındaki göreli düşüşlerin büyüğü. Gürültü bandındaysa her tasarruf AL · düşüş ≤%10 ve çıktı tasarrufu ≥%25 → AL · ≤%15 ve ≥%30 → AL · %15–20: ≥%75 AL, %50–75 SOR, <%50 RED · >%20: ≥%50 SOR, <%50 RED. Görev başarısı düşerse RED. n=6 küçük: AL çıkarsa varsayılan açılır ve `output_savings.json` defteriyle sahada izlenir.
