# claude-usage
ad: claude-usage
tur: CLI
video: JNM_rxqtlvY
repo: phuryn/claude-usage
lisans: MIT
son_commit: 2026-07-10
arsiv: hayır
kaynak: yok
telemetri: kapalı

## Ne
`~/.claude/projects/**/*.jsonl` oturum loglarını yerelde okuyup sqlite'a (`~/.claude/usage.db`) işleyen, terminalde özet ve tarayıcıda grafikli maliyet panosu üreten bağımsız Python aracı. Plan tipinden (API/Pro/Max) bağımsız çalışır; Cowork oturumları JSONL yazmadığı için kapsam dışı.

## Kanıt
2239 yıldız · son commit 2026-07-10 · MIT · bağımlılık yok (`dependencies = []`), yalnız stdlib `http.server`+`sqlite3`.

## Kurulum
- uv: git+https://github.com/phuryn/claude-usage

## İzinler
`~/.claude` altını salt okur; `usage.db` yazar; `dashboard` komutu yerel port (varsayılan 8080, Docker'da 9898) açar ve tarayıcı başlatır. `dashboard.py` grafik kütüphanesini (Chart.js) CDN'den yükler — veri yerel kalır ama internet olmadan grafik render olmaz.

## Duman testi
- komut: claude-usage --version
- cikis: 0
- desen: \d+\.\d+

## Geri alma
- uv: claude-usage

## Köprü izni
- arac: claude-usage
- altIzin: --version

## Önerilen katman
T2 (çalıştırılabilir CLI + yerel HTTP sunucu; kaynak MIT, tek dosya bağımlılıksız, kurulum tersine çevrilebilir).

## Özellikler
### terminal-ozet
ne: `today`/`week`/`stats` komutları token/maliyet özetini terminalde basar.
kurulum: `claude-usage scan` sonrası ilgili komut.
lisans: MIT
etiket: -
karar: KUR
gerekce: gerçek kullanımı gösteriyor, kurulumu geri alınabilir, ek risk yok.

### web-dashboard
ne: Chart.js grafikleri, model/tarih filtresi, katlanabilir panel durumunun localStorage'da hatırlanması, URL parametreleriyle işaretlenebilir (bookmarkable) filtreli görünüm.
kurulum: `claude-usage dashboard` → localhost:8080.
lisans: MIT
etiket: teknik
karar: DENE
gerekce: hipotez: URL-durum + localStorage kalıcı panel deseni kendi iç panolarımızda tekrar filtre kurma turunu azaltır · metrik: aynı görünüme dönmek için gereken tıklama/istek sayısı · bütçe: 1 iç araç, ≤2 saat · geri_alma: deseni uygulamazsak mevcut sunucu-taraflı görünüm kalır · eşik: tıklama sayısı %30 düşerse benimse.

### vscode-entegrasyonu
ne: VS Code eklentisi, panoyu webview içine gömer (`--no-browser` ile).
kurulum: VS Code Marketplace'ten `claude-usage` eklentisi.
lisans: MIT (vscode-extension/LICENSE de MIT)
etiket: -
karar: ZATEN VAR
gerekce: zaten var: terminal-ozet + web-dashboard aynı veriyi IDE bağımlılığı olmadan karşılıyor.

## Mekanizma
### web-dashboard
nasıl: `dashboard.py` sqlite'tan tek seferde toplulaştırılmış veri çekip tek HTML sayfası döner; grafik kütüphanesi CDN'den yüklenir, panel açık/kapalı durumu ve seçili filtre `localStorage` + URL query param'da tutulur, 30 sn'de bir client-side yenilenir.
neden: kullanıcı sekmeyi kapatıp geri döndüğünde filtre/panel durumunu yeniden kurmaz; aynı görünümü paylaşmak için tek URL yeter — tekrar eden etkileşim turlarını azaltır.
koşul: tarayıcı JS + localStorage gerektirir; CDN'e erişim yoksa grafikler render olmaz (veri kaybı yok, görsel eksik); tek kullanıcılı yerel araç, çok kullanıcılı senkronizasyon yok.
bizde: iç raporlama panolarımızda (ör. jev/video rapor arayüzü) aynı desen — beklenen etki: tekrar filtre kurma adımının kalkması, ölçüm DENE aşamasında netleşir.

## Bağımsız kanıt
- [Claude Code Usage Dashboard Review — ToolHunter](https://www.toolhunter.cc/tools/claude-usage) — bağımlılık yok ve buluta veri göndermiyor tespiti, MIT lisans ve 2239 yıldız teyidi.

## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| "logları okuyan bir dashboard/JSON API" | README (dashboard.py `/api/data`) + cli.py yorumları | doğru | dashboard sunucusu `/api/data` uç noktasını 10 sn içinde yanıtlamak zorunda (VS Code eklentisi kontrolü) | - |
| session.jsonl'den input_tokens/output_tokens/cache_read okunuyor | scanner.py alan adları (on.md envanteri) | doğru | scan komutu bu alanları sqlite'a işliyor | - |
| araç veri göndermiyor / telemetri yok | ToolHunter incelemesi + pyproject.toml `dependencies = []` | doğru | üçüncü taraf runtime bağımlılığı yok | - |

aday: docs/kurulumlar/adaylar/claude-usage.md · T2 (DENE ağırlıklı) · Yerel, bağımlılıksız, MIT token/maliyet panosu; ana risk yok, web-dashboard'un URL+localStorage deseni ayrı DENE olarak değerlendirilmeli.
