# TOKEN-6cR-H2: saha ölçümü ve kırılma sınıflaması

Salt okuma (2026-10-04 16:15). Ayar, hook, plugin, MCP ve Headroom değişmedi; claude -p 0. Betik `tools/h2_sinif.py`, testi `tests/test_h2_sinif.py`.

`docs/token-6c-r.md` yalnız bağlam olarak okundu. "Strict override" halkasına dayanan mekanizma cümlesi 6f K1 ile geçersiz, burada kullanılmadı.

## K1 Mühür
- `headroom_yama.py --durum`: `prefix_tracker.py` yamalı · `anthropic.py` yamalı.
- /health: `config.pid` 28372. runtime_env 5 anahtar, sha8 e5974b21 (değer basılmadı).
- Yamalı başlatmalar, proxy-6768.log "Headroom Proxy started" satırları: 10-03 20:11:20 ve 10-04 11:43:06.
- Headroom süreçleri 5 `headroom.exe`: 1 proxy (headroom-desktop altında) ve 4 `mcp serve` (her biri bir claude oturumunun alt süreci).
  - Sayının 1'den 6'ya çıkmasının sebebi: proxy tek; artış açık CC oturumu başına başlayan Headroom MCP sunucusundan geliyor.
- settings.json: `awaySummaryEnabled` = true. Son değişiklik 10-04 11:42:34; bu, Headroom Desktop'un açılışta env anahtarını yamaladığı an (6c K1).
- h2a_kayit:
  - Kayıtçı pid 36820, 10-04 15:17:00'den beri çalışıyor.
  - Ölçüm anında 1093 tekil istek (ham satırlarda tekrarlar request_id ile atıldı); "bosluk" satırı 0, hata satırı 0.
  - İlk ts 10-03 20:15:15, son ts 10-04 16:14:34.
  - En büyük aralık 03:05:08 → 14:49:22. 14:49–15:17 arasındaki satırlar, kayıtçı yeniden başlarken feed'den yazılan önceki istekler; kapsam yine 15:17:00'de başlıyor.

## K2 Pencereler
Filtre: etkileşimli · ana (ttl_sim). `Kendi-oyun-modlarim` klasörü ve claude -p iki pencerede de dışarıda.
- ÖNCE (6c-R (b) penceresi): 10-01 04:03:23 → 10-03 17:33:58. 39 oturum · 1105 istek.
- SONRA (yamalı başlatma): 10-03 20:11:20 → 10-04 16:15. 14 oturum · 449 istek.
  - awaySummaryEnabled bu aralıkta zaten true: SONRA'da 7 away çifti var.

## K3 6c-R: 4–60 dk çiftleri, aralarında away_summary var/yok

ÖNCE penceresi bugünkü `ttl_sim` mantığıyla yeniden hesaplandı.

| pencere | away var | away yok |
|---|---|---|
| ÖNCE, 6c-R'de yayımlanan | 33/43 %76.7 | 8/65 %12.3 |
| ÖNCE, bugün, eski filtre (oyun klasörü dahil) | 33/43 %76.7 | 8/65 %12.3 |
| ÖNCE, bugün, bu dalganın filtresi | 17/25 %68.0 | 5/38 %13.2 |
| SONRA | **0/7 %0** | **0/13 %0** |

Fark sebebi: 6c-R `Kendi-oyun-modlarim` oturumlarını dışlamıyordu (15 oturum · 924 istek). Eski filtreyle sayılar birebir tutuyor; yöntem değişmedi.

Ek maliyet. Kırılma başına baştan yazma ile okuma arasındaki fark, k6cr formülüyle hesaplandı.

| | ÖNCE | SONRA |
|---|---|---|
| tüm çiftler: kırılma | 43/1067 %4.0 | 9/435 %2.1 |
| ek ağırlıklı / çift | 9151 | 2604 (−%71.5) |
| ek $ / çift | 0.0376 | 0.0107 (−%71.5) |
| ek toplam | 9.76 M · $40.08 | 1.13 M · $4.65 |
| 4–60 away var ek | 4.44 M · $18.24 | 0 |

Hedef tuttu: özetli grup %68.0'dan (yayımlanan %76.7) %0'a indi. Bu, özetsiz grubun düzeyinin (%13.2'den %0'a) de altında.

Uyarı: SONRA'da away var grubu n=7. Bu, 6c-R kuralının n ≥ 10 kapısının altında, yani hüküm kesin değil.

## K4 H2 sınıflama (SONRA, kırılma 9)
Eşleştirme: transcript isteği ile h2a satırı, cache_read ve cache_write birebir eşit, ±120 sn. Kayıtlı dönemde 266/266 istek eşleşti.

| sınıf | adet | baştan yazma token | ek ağırlıklı | ek $ |
|---|---|---|---|---|
| (a) recap: away arada + Headroom öneki | 1 | 1 421 | 2 700 | 0.01 |
| (b) Headroom dönüşümü | 3 | 236 296 | 448 962 | 1.84 |
| (c) system/tools | 0 | 0 | 0 | 0 |
| (d) TTL aşımı | 0 | 0 | 0 | 0 |
| (e) sınıflanamayan | 2 | 137 918 | 262 044 | 1.08 |
| kayıt yok (20:11:20–20:15:15 · 03:05:45–15:17:00) | 3 | 220 578 | 419 098 | 1.72 |
| bosluk | 0 | 0 | 0 | 0 |

- (e) sebebi: 2'si de `mesaj_yok`. Kayıtçının ilk dakikalarında (20:17:53 ve 20:19:03) feed boş mesaj dizisi vermiş, karşılaştırma yapılamadı. Bu iki kırılmada cr=30884, yani yalnız system+tools okunmuş.
- (b)'nin üçünde de sıkıştırılmış dizi 1. indekste (role system) bozuluyor; CC öneki sağlam. cr=30884: bütün mesajlar yeniden yazılmış.
  - Ara 3–11 sn, yani sıcak.
  - 2'si `deferred:kompress_background` ve `read_lifecycle:stale` etiketli; 1'i yalnız `tool_schema_compaction`.
- Sınıflayıcı düzeltmesi (dalga içinde, testli): CC'nin kendi öneki her istekte sondaki 2–3 mesajda değişiyor (cache_control kayması). Bu yüzden "önek aynı mı" testi her kırılmayı "cc_onek" diye e'ye atıyordu. Yeni kural ilk farka bakar: sıkıştırılmış dizi CC'den daha önce bozulduysa kırılma Headroom'un.
- 6f karşılıkları:
  - "Yamalı kolda sıcak frozen=0": sahada (a)+(b) = 4 sıcak Headroom yeniden yazması. Yama soğuk/çatal durumunu kapattı ama sıcak kompress_background/read_lifecycle yolu açık kaldı.
  - "Sınıflanamayan 13": sahada 2 (yalnız kayıt eksikliği). cc_onek 0, eşleşmedi 0.

## Karar önerisi
- Literal kurallar:
  - (e) = 2/6, %33 > %20 → "önce sınıflandırıcı düzeltilir".
  - Ama (e)'nin tamamı kayıtçının ilk 4 dakikasında boş gelen feed. Sınıflayıcı hatası değil; tekrar etmez.
  - (e) dışarıda: (a)+(b) 4/4. Recap kaynaklı kırılma 4–60 bandında 0, kırılma başına maliyet −%71.5.
- **Öneri: TOKEN-6e'ye geç.** (c) 0, dolayısıyla system/tools sabitlemesi öne alınmaz.
- Açık iş: sıcak (b) kırılmaları kalıyor (3 adet, 236 k token). Kaynak `kompress_background` / `read_lifecycle:stale` yeniden yazması; 6e'de ya da 6f devamında ele alınmalı.
- away var n=7 < 10: aynı ölçüm birkaç gün sonra `h2_sinif.py` ile yeniden koşulup kapı doğrulanmalı.
