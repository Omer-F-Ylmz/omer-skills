# claude-mm
ad: claude-mm
tur: CLI
video: XemheY_aM1g
repo: MG-Cafe/claudecode-minimax-stack
lisans: yok
son_commit: 2026-06-03
arsiv: hayır
kaynak: yok
telemetri: yok
arastirma: tam

## Ne
Claude Code'un backend'ini `--bare --settings <json>` ile Anthropic yerine MiniMax M3'e (Anthropic-uyumlu endpoint `api.minimax.io/anthropic`) yönlendiren bir ayar dosyası + alias tarifi. Plain `claude` dokunulmadan kalır; `claude-m3` (videoda "claude-mm"/"claude /mm") alias'ı sadece o komut için MiniMax'a geçer. İki yol var: MiniMax doğrudan ($25 min top-up) ya da OpenRouter üzerinden `claude-code-router` proxy'si ($5 min top-up).

## Kanıt
yıldız 2 · son commit 2026-06-03 · lisans yok (repo'da LICENSE dosyası yok)

## Kurulum
- serbest komut: README'de shell betiği (mkdir/cat>/source ile ~/.config/mg-minimax altında env + JSON settings dosyası oluşturma), npm/mcp/plugin/uv/winget kalıbına girmiyor → gerekçe İzinler'de.

## İzinler
- `--bare` OAuth/Vertex/Bedrock kimlik doğrulamasını devre dışı bırakır, prompt ve kod içeriği Anthropic dışı 3. taraf (MiniMax, Çin merkezli; China endpoint `api.minimaxi.com` ayrı) sunucusuna gider.
- API anahtarı düz metin dosyada tutulur (`chmod 600` ile korunuyor ama şifrelenmemiş).
- Option B `npm install -g @musistudio/claude-code-router` ile 3. parti bir proxy paketi global kurulur, `127.0.0.1` üzerinde arka planda servis (`ccr`) çalıştırır.

## Duman testi
- komut: claude --version
- cikis: 0
- desen: \d+\.\d+

## Geri alma
- elle: `~/.config/mg-minimax` ve (varsa) `~/.claude-code-router` klasörleri + shell alias satırı silinir; npm paketi kurulduysa `npm uninstall -g @musistudio/claude-code-router` (paket kurulumu opsiyonel Option B'ye özgü).

## Köprü izni
- arac: claude
- altIzin: --version

## Önerilen katman
RED — gerekçe: (1) lisans: yok — repo'da LICENSE dosyası yok (license-gate: lisanssız repo kurulmaz); (2) güvenlik: `--bare` ile Anthropic auth bypass edilip prompt/kod 3. taraf (MiniMax) sunucusuna gönderiliyor, API anahtarı düz metin saklanıyor; (3) yapılandırılmış Kurulum kalıbına (npm/mcp/plugin/uv/winget) girmeyen serbest shell betiği. Elle (kullanıcı kendi sorumluluğuyla) uygulanabilir, otomatik KUR/DENE değil.

## Telemetri kapatma
- yok (Claude Code'un kendi telemetrisi bu tarifle değişmiyor; asıl veri akışı MiniMax'a giden istek/yanıt trafiği, telemetri anahtarı değil)

## Özellikler
### minimax-m3-backend-degisimi
ne: Claude Code'u tek komutluk `--bare --settings` bayrağıyla MiniMax M3 backend'ine geçirip token başına maliyeti düşürmek
kurulum: `~/.config/mg-minimax/claude-minimax-settings.json` içinde ANTHROPIC_BASE_URL/API_KEY/MODEL env override + shell alias (`claude-m3`); paket kurulumu yok (Option A)
lisans: yok
etiket: token
karar: RED
gerekce: lisans: yok (aday dosyasındaki bulgu, license-gate kuralı) · güvenlik: --bare OAuth bypass + veri 3. taraf (MiniMax) sunucusuna gidiyor, API anahtarı düz metin

## Mekanizma
### minimax-m3-backend-degisimi
nasıl: Claude Code, `--bare` ile OAuth/Vertex/Bedrock'u devre dışı bırakıp kimlik/endpoint bilgisini yalnız `--settings` JSON'undan okur; `ANTHROPIC_BASE_URL` MiniMax'ın Anthropic-uyumlu `/anthropic` endpoint'ine, `ANTHROPIC_MODEL`/`ANTHROPIC_DEFAULT_*_MODEL` "MiniMax-M3"e sabitlenir. Prompt/context/token içeriğinin kendisi hiç sıkıştırılmaz ya da değiştirilmez — yalnızca isteğin gittiği sunucu ve faturalanan model değişir; plain `claude` (flagsız) dokunulmadan eski backend'i kullanmaya devam eder.
neden: MiniMax M3 girdi/çıktı fiyatı ($0.30/$1.20 per 1M token) Claude Opus 5.5'e (~$4/$20 per 1M) göre ~13-17x ucuz; aynı işi yapan token hacmi için ödenen dolar tutarı düşer.
koşul: MiniMax M3 kalite skoru Opus'un altında (ör. bir agregatörde Intelligence 29.2 vs Opus 4.8'de 41.8, Coding 58.6 vs 74.3); daha zayıf model aynı görevi tamamlamak için daha fazla tur/deneme gerektirebilir, bu da token başına ucuzluğun gerçek görev-başı tasarrufa dönüşmesini azaltır. Ayrıca Anthropic'e özel prompt-caching/context-editing optimizasyonları MiniMax tarafında aynı fiyat/davranışla eşleşmeyebilir.
bizde: Karşılığı yok; bu bir backend-değiştirme operasyonel tekniği, KUR edilecek bir skill/araç değil — RED.

## Bağımsız kanıt
- https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/ (ve ilişkili fiyat toplayıcılar) — MiniMax M3'ün kendi API'sinde girdi $0.30/1M, çıktı $1.20/1M olduğunu, bunun Claude Opus 5.5'in $4/$20 fiyatına göre ~13-17x ucuz olduğunu doğruluyor.

## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Opus'a göre 5x ucuz | https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/ | abartılı | gerçek oran ~13-17x (video oranı olduğundan düşük tahmin etmiş, yön ters ama sayı yanlış) | - |
| 1M token ~0.30$ | https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/ | doğru | MiniMax M3 girdi fiyatı tam $0.30/1M ile eşleşiyor (çıktı ayrıca $1.20/1M) | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
