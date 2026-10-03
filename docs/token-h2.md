# H2: ≤1 dk'daki 45 kırılmanın teşhisi

Salt okuma dalgası (2026-10-03): ayar, hook ve Headroom değiştirilmedi, claude -p 0. Veri: `olcum/token-h2-liste.json` (K1), `olcum/token-h2-k3.json` (K3), `olcum/token-h2-net.json` (sınıf ve net). K2 (okuyucu satır okuması) atlandı: auto-mode sınıflayıcısı reddetti, KARAR (b).

## K1: kapı
TOKEN-6c `r6c.pkl` penceresi (14 gün, etk·ana) içinde "diğer" sebepli ve arası 60 sn'den kısa 45/45 kırılma. Ham 5.49 M cache_creation; fazladan maliyet (yazma − okuma) ağırlıklı olarak 10.43 M, yani 14 günün %1.97'si. Dolar karşılığı $45.3, yani %2.75. etk·ana içindeki payı %3.10 / %3.67. Kapı geçti.
Transcript olaylarının hiçbiri kırılan istekleri kırılmayanlardan ayırmıyor: hook_success ve output_style 45/45'te var, kırılmayanların da ~%99'unda var. Model/effort değişimi 0, sidechain 0, away_summary 0.

## Sınıf tablosu

| sınıf | adet | ham cache_creation | ağırlıklı | $ |
|---|---|---|---|---|
| Headroom dönüşümü | 15 | 2.10 M | 3.99 M | 16.36 |
| kanıtsız (log öncesi 26 + 1 eşleşme toleransı dışında) | 27 | 3.11 M | 5.91 M | 26.76 |
| diğer | 3 | 0.28 M | 0.53 M | 2.18 |
| ham toplam | 45 | 5.49 M | 10.43 M | 45.30 |

19 → 14 farkı: log penceresine 19 kırılma düşüyor. Bunlardan biri (7fa44b18:214) dt 2.01 sn ile ±2 sn toleransın dışında kaldı, kanıtsız sayıldı; 18'i PERF'e bağlandı. Dördünün önceki isteği PERF'e bağlanamadığı için K3'ün ardışık çift analizine 14'ü girdi. "Diğer" sınıfının 3 kırılması (62, 80, 99) msgs=8 olan erken oturum istekleri; Headroom dönüşüm etiketi yok.

## K3: Headroom eşleşmesi
Log satırları yerel saatle yazılıyor (+03). `hr_<epoch>` kimliğiyle karşılaştırınca fark p50 0.57 sn çıkıyor. Eşleşme cache_read+cache_write birebir aynı olmak ve |dt| ≤ 2 sn şartıyla yapıldı. Arası 60 sn'den kısa 1353 ardışık çiftte kırılma oranı:
- `read_maturation` varsa 9/26 (%34.6), yoksa 5/1327 (%0.4)
- `deferred:kompress_background` varsa 9/39 (%23.1), yoksa 5/1314 (%0.4)
- `tool_search_deferral` araç sayısı değiştiyse 7/36 (%19.4), değişmediyse 7/1317 (%0.5)
- mat veya kmp varsa 13/58, yoksa 1/1295

## K4: kaynak (headroom-ai, uv tool)
`kompress_background`
- (i) Öneki değiştiriyor. `proxy/handlers/anthropic.py:1724-1729` yalnız `frozen_message_count == 0` iken çalışıyor. Ardından "cold-start fast pass" (`:1749-1810`) Kompress dışındaki bütün hattı tüm mesajlara eşzamanlı uyguluyor ve `comp_cache.update_from_result` ile oturumu bu biçime kilitliyor. Donmuş mesaj sayısı 0 olduğu için ilk mesajdan sonrası yeniden yazılıyor. Bu, kırılmalardaki cr kümeleriyle uyuşuyor: önbellekte yalnız system+tools'a denk düşen ~7.5k / 8.4k / 30.9k token kalıyor.
- (ii) Tetik: `frozen_message_count == 0` ve `original_tokens ≥ HEADROOM_BACKGROUND_COMPRESSION_MIN_TOKENS` (varsayılan 50000, `proxy/server.py:1134-1138`). Süre ya da istek sayısı koşulu yok. Donmuş sayının kaynağı `prefix_tracker.get_frozen_message_count()` (`:1497`); CACHE modunda `_strict_previous_turn_frozen_count` bunu kısıtlıyor (`:1509-1513`). Arası 60 sn'den kısa olduğu halde sayının neden 0'a düştüğü kanıtlanmadı.

`read_maturation`
- (i) Yalnız donmuş öneki dokunulmaz bırakıyor (`transforms/read_maturation.py:147-150`). Donmuş sayının ötesindeki Read sonuçlarını CCR işaretiyle değiştiriyor (`:295-319`). `relocate_cache_breakpoint` (`:322-337`) mesaj içi cache_control işaretini tutulan Read'lerin önüne taşıyor. Donmuş sayı 0 iken bu da ilk mesajdan sonrasını değiştiriyor; kırılmaların 9'unda kmp ile birlikte görülüyor.
- (ii) Tetik: dosyaya son dokunuştan beri 5 asistan turu geçmesi (quiesce) ya da okumadan beri 25 tur geçmesi (max_hold), ayrıca içeriğin ≥2048 B olması (`:290`; varsayılanlar `proxy/models.py:305-307`). Süre koşulu yok.

## Net hesap (Headroom sınıfı, 15 kırılma)
Kazancı şöyle hesapladım: Δtok_saved (kırılan istek − önceki istek) × [1h yazma ağırlığı + okuma ağırlığı × bir sonraki kırılmaya kadarki istek sayısı]. $ aynı formülle, model fiyatıyla.
Maliyet 3.99 M ağırlıklı ($16.36), kazanç 0.20 M ($0.60). Net kazanan kırılma 0/15. **Hüküm: kabul edilemez kırılma.** Dönüşümün kazandırdığı tasarruf, sıcak önbelleği kırmanın maliyetinin yaklaşık %5'i.

## Hüküm
- ≤1 dk kırılmalarının log içinde kanıtlanabilen kısmının (15/18) kaynağı Headroom: donmuş mesaj sayısı 0 iken uygulanan `kompress_background` fast pass'i ve `read_maturation`. Kaynak CC değil, o yüzden TOKEN-6e ya da TOKEN-5 kapsamına girmiyor. Log öncesindeki 27 kırılma kanıtsız; tablolaştırırken aynı oranı varsaymadım.
- Aday mekanizma (uygulama yok), **TOKEN-6f: dönüşümü soğuk önbelleğe hizalamak.** Kaynak buna izin veriyor. İhtiyaç duyulan iki bilgi, iki dönüşümün kapısından önce zaten hesaplanıyor: `idle_seconds` (`anthropic.py:1508`) ve isteğin TTL katmanı `_cc_ttl` (`:1530`). Hazır bir soğukluk testi de var: `is_cold_prefix(prefix_tracker, ttl_seconds=_cc_ttl)` (`transforms/cold_prefix.py`, şimdilik yalnız HEADROOM_COLD_RECOMPACT'te kullanılıyor, `:1537`). İki kapıya bu koşul eklenebilir: `:1724-1729`'daki `frozen_message_count == 0` testine "ve önek soğuk ya da oturum gerçekten ilk istekte (önceki iletilen mesaj yok, `:1496`)" şartı, `:2207`'deki read_maturation kapısına da "frozen > 0 veya önek soğuk" şartı. Sıcak önbellekte donmuş sayı 0'a düşerse dönüşüm ertelenir ve bir sonraki soğuk anda tek seferde uygulanır. Read olgunlaşmasının tetiği tur sayısına bağlı olduğu için, erteleme olgunlaşmış işaretlerin birikmesine izin veriyor (`_matured` durumu oturumda kalıyor). Açık soru: donmuş sayı sıcak önbellekte neden 0 oluyor (tracker kaybı ya da strict clamp). 6f bunu önce `_strict_previous_turn_frozen_count` ve `prefix_tracker` oturum anahtarında doğrulamalı. Upstream yaması mı yerel ayar mı olacağı (rollout'ta `read_maturation` kapatma vb.) 6f'nin kararı.
- Ayrı kalem, süreç: tur sayacı iki dalgada üst üste atlandı (TOKEN-6c 24/21, H2 19/17). Öneri: Stop hook'u ile mekanik sayaç. Hook asistan yanıtlarını sayar ve sayıyı `.claude/dalga.md`'ye ya da statusline'a yazar; 5'in katlarında ve tavanın %85'inde uyarı verir. Bu dalgada hook'a dokunulmadı.
