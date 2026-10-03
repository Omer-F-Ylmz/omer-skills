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
