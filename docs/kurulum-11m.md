# KURULUM-11m-A · Desktop token katmanı — köprü tarafı

22 Eyl 2026. **KARAR:** tasarruf köprüde olur — çıktı Desktop'a gelmeden küçülür.
Sohbet trafiği proxy'den geçmez (yapısal sınır); `headroom_compress` MCP'si içerik
zaten bağlamda olduğu için kazanç vermez, katman kapsamı dışında.

## K1 · Obsidian başlatıcısı

`tools/mcp-launch/obsidian.cmd` artık `mcp-remote`'u değil
`tools/cc-kopru/obsidian.mjs`'i çağırıyor. SDK 1.30'da `SSEClientTransport` var;
eklentinin HTTP+SSE ucuna doğrudan bağlanıldığı için aradaki mcp-remote katmanı düştü.

| davranış | eski (11g) | yeni (11m-A) |
|---|---|---|
| açılışta bağlantı | mcp-remote uca bağlanır | bağlanmaz |
| Obsidian kapalı · initialize | dönmez, Desktop sunucuyu düşmüş sayar | geçer |
| Obsidian kapalı · tools/list | — | son başarılı listenin önbelleği (`obsidian-semalar.json`) |
| Obsidian kapalı · araç çağrısı | asılı kalır | `Obsidian kapalı — aç ve tekrar dene` |
| Obsidian sonradan açılır | Desktop yeniden başlatılmalı | ilk çağrı bağlanır |

Bağlantı her hatada düşürülür (`baglantiDusur`), bir sonraki çağrı yeniden kurar —
yeniden bağlanma için Desktop'ı yeniden başlatmak gerekmez. İlk başarılı `tools/list`
şemayı diske yazar; önbellek yoksa kapalı uçta liste boş döner (uydurma araç yok).

## K2 · git salt-okuma

`kopru.json` → `izinli.git`: `altIzin` = **grep · ls-files · show**. Yazan ya da
koşturan her alt komut altIzin dışında kaldığı için reddedilir.

Yasak bayraklar `yasakOnekBayrak` ile uygulanır: git uzun seçenekte **benzersiz önek
kısaltmasını** kabul ediyor (`--out` = `--output`, `--no-ind` = `--no-index`), tam ad
eşitliği yetmiyor. Kural: uzun bayrakta ≥5 karakterlik her önek, kısa bayrakta bitişik
değer (`-Oless`). 5 karakter alt sınırı `--name-only`, `--no-color` gibi meşru
bayrakların `--no-index` önekine takılmasını engelliyor; daha kısa önekleri git'in
kendisi de "ambiguous" diye reddediyor.

Liste: `-O` · `--open-files-in-pager` · `--no-index` · `--untracked` ·
`--no-exclude-standard` · `-f`/`--file` · `--output` · `--ext-diff` · `--textconv`.
Son üçü yürütücü çağırıyor; `--no-index`/`--untracked`/`--no-exclude-standard`
gitignore'lu `bin/obj` ağacını taratıp Read deny kapısını baypas ediyordu.

`-c` · `--config` · `--exec-path` mevcut `TEHLIKELI_SECENEK` ağına takılıyor; kod
eklenmedi, yalnız red testi yazıldı.

`git grep -n -e A -e B -- docs/` **geçiyor** (22 Eyl'de git allowlist'te olmadığı için REDdi).

## K3 · `oku` aracı — claude-mem yerine graphify

claude-mem'in `smart_*` araçları **CC'de de çalışmıyor**; sorun Desktop'ın
cwd=System32'si değil. Onarım = tree-sitter-cli + ~20 gramer paketi + C derleyici;
ayrı karar.

Kanıt (22 Eyl, cwd=proje kökü, kısa ömürlü MCP süreci):

| kanıt | sonuç |
|---|---|
| `resolves outside the workspace` | cwd=kök ile **çözülüyor** (yol doğru) |
| `tree-sitter` PATH'te | yok |
| `require.resolve('tree-sitter-cli/package.json')` | MODULE_NOT_FOUND |
| `~/.claude-mem/tree-sitter-libs` | yok (gramerler .dll'e derlenmemiş) |
| `smart_search "komutDenetle"` | 170 dosya tarandı, **0 sembol** |
| `smart_outline` .mjs / .py | `Could not parse` |
| `smart_unfold` | `Could not parse` |

Yerine köprüye `oku` aracı geldi; kaynak `graphify-out/graph.json`. Düğümde
`source_file` (köke göreli) + `source_location` (`"L44"`) var, **bitiş satırı yok** —
sembol bir sonraki kardeşin başına kadar, son sembol dosya sonuna kadar okunur.

| mod | girdi | çıktı | graf gerekir mi |
|---|---|---|---|
| `iskelet` | dosya | semboller + satır numaraları, gövde yok | evet |
| `sembol` | dosya + ad | yalnız o sembolün satırları | evet |
| `aralik` | dosya + bas/bit (tavan 400 satır) | satır aralığı | hayır |

Kapılar: Read deny kuralları (`okumaDeny`) **her modda dosya okunmadan önce**;
graph.json dosyadan eskiyse `graph eski — graphify update .` (tahmin yapılmaz);
`graphify-out` yoksa açık mesaj + `aralik` önerisi.

## K4 · Headroom çıktı katmanı

`ciktiHazirla(metin, tavan, { ham, log })`:

1. `ham:true` → katman atlanır, çıktı yalnız tavanda kırpılır.
2. `< 8000` karakter → dokunulmaz.
3. **Sınıf kapısı** (`ciktiSinifi`): ölçüm sonrası yalnız `json` sıkışır; `log`,
   `markdown` ve `kod` sıkışmaz (aşağıdaki tablo). 11l'in 3-gram tekrar oranı kapısı kaldırıldı — tekrarsız ama
   sıkıştırılabilir log (farklı satırlar, aynı biçim) kapıya takılıyordu.
4. Ağ çağrısı yok: yerel `headroom mcp serve` stdio MCP'si.
5. Başarılı: ilk satır `[headroom %X · tam: <yol>]`.
   Kazanç yok / hata: `[headroom yok · tam: <yol>]` + ham çıktı (uydurma yüzde yok).
   Yalnız kırpma: `[kırpıldı · tam: <yol>]`.

Tam çıktı **yalnız** sıkıştırılan ya da tavanda kırpılan çıktı için, redaksiyondan
sonra `LOG_DIZIN`'e yazılır. Çağıranın zaten yazdığı bir log varsa (`komut` aracında
`kos()`'un logu) yeni dosya açılmaz. `LOG_DIZIN`'de son **200** dosya tutulur.

Hash: `headroom_retrieve` ile paylaşımlı depo **kanıtlanmadı** → çıktıya yalnız log
yolu basılır, hash basılmaz.

### Ölçüm (rtk hook'u açık, 22 Eyl 2026)

Tavan bilerek 10 M karakter: kırpma karışmasın, ölçülen yalnız katmanın kazancı.

| örnek | sınıf | yol | ham krk | katman sonrası | kazanç |
|---|---|---|---|---|---|
| `node --test` (2 dosya) | log | katman dışı (eşik altı) | 6 112 | 6 112 | %0 |
| `git log -100 --stat` | log | headroom → kazanç yok | 92 377 | 92 463 | **%0** (13,9 sn) |
| `katalog tur=skill` | markdown | katman dışı (sınıf) | 62 957 | 62 957 | %0 |
| `git log -100` JSON zarfı | json | headroom | 20 865 | 16 424 | **%21** (4,6 sn) |

**Karar:** `log` sınıfı katmandan **çıktı**. Headroom gerçek komut çıktısında hiç
kazanmıyor — 92 KB'lık `git log --stat` gövdesini aynen (86 karakter şişirerek) geri
veriyor. Yapay tekrarlı log gövdesinde %30 kazanıyor ama gerçek çıktıda değil; tarifin
%15 eşiği bu yüzden `log`'u eliyor. `json` %21 ile eşiğin üstünde, katmanda kalıyor.
Markdown/kod zaten kayıplı olduğu için (11l K7) dışarıda.

Büyük log çıktısının asıl kazancı sıkıştırmadan değil **tavanda kırpma + tam çıktının
log dosyasında kalmasından** geliyor: `git log -100 --stat` 92 377 → 30 142 karakter
(%67), tamamı `LOG_DIZIN`'deki dosyada.

Ölçüm betiği: `tools/cc-kopru/araclar/olc-11m.mjs`.


## 11m-B skill metinlerine girecek kurallar

- Eşik 8000 karakter; yalnız `json` sıkışır. `log`/`markdown`/`kod` sıkışmaz —
  büyük çıktı 30 000 karakterde kırpılır, tamamı log dosyasında kalır.
- `komut` aracında `ham:true` katmanı atlar — çıktının birebir gerekli olduğu işte kullan.
- Tam çıktı her zaman `[… · tam: <yol>]` satırındaki dosyadadır; retrieval yolu bu
  dosyadır, `headroom_retrieve` değil.
- `oku` imzası: `oku(proje_yolu, dosya, mod=iskelet|sembol|aralik, ad?, bas?, bit?)`.
  Dosyayı tam okumadan önce `iskelet`, sonra tek `sembol`. `aralik` graf gerektirmez.
- `graph eski` yanıtı alınırsa önce `graphify update .`, sonra yeniden `oku`.
- Obsidian kapalıysa araç çağrısı `Obsidian kapalı — aç ve tekrar dene` döner;
  Obsidian'ı açmak yeter, Desktop yeniden başlatılmaz.

## FIX-5 K1 — headroom "kazançsız" kararı nereden geliyor (ölçüm, 22 Eyl 2026)

- `headroom_compress` vekili KULLANMIYOR: `ccr/mcp_server.py:404 _compress_content`
  içeriği `{"role":"tool"}` mesajına sarıp `headroom.compress.compress()` çağırıyor;
  vekil yalnız erişilebilirlik sondası ve `/v1/retrieve` için (FIX-4'teki 6767 düzeltmesi
  "proxy unreachable" fail-open'ını kapattı, sıkıştırma kararını değiştirmedi).
- Kararı veren kural: `transforms/content_router.py:5347` (`route_counts["ratio_too_high"]++`),
  rapor satırı `:5637` → `unchanged (ratio>=1.00)`; `min_ratio` varsayılanı 1.0 =
  "herhangi bir küçülmeyi kabul et" (`:1606-1615`). `role=="tool"` içerik ek olarak
  geri döndürülebilirlik kapısından geçiyor (`:5339-5341`).
- Ölçüm (yerel CPU, ücretli API yok):
  - B `gh api …/commits` (132 072 kr): `router:noop`, %0, `route_counts={'ratio_too_high':1}`
  - A `gh api …/commits?sha=b214237` (130 671 kr): `router:mixed:0.51`, **%48,7**
  - B'nin eleman bazlı yarıları: ilk 15 commit %0 · son 15 commit **%25,7** (`router:mixed:0.78`)
  - B'nin commit `message` alanları boşaltılmış hâli: **%9,6** (`router:smart_crusher:0.96`)
  - B 32 KB'lık bayt parçalarına bölünüp denendi: **%0** (parçalar JSON yapısını bozuyor)
- Sonuç: kök neden köprüde değil — headroom bu gövdeyi kayıpsız/geri döndürülebilir
  biçimde küçültemiyor. Zorlanmadı; K2 etiketi kararı gösteriyor:
  `[headroom yok: kazançsız (router:noop) · tam: <yol>]`. Eleman bazlı bölme en iyi
  ihtimalle ~%12,3 veriyor (hedef %15'in altında), o yüzden katmana eklenmedi.
