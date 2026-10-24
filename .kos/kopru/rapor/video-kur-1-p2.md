# video-kur-1 P2 (kurulum dalgası 1), KISMİ, kullanıcı kararı bekliyor

Disk C: 142 GB boş, RAM %74-82 (eşikler tamam). Tavan $0.50 → harcanan ≈$0.48.

## Kurulan
- code-modernization@claude-plugins-official v1.0.0, `claude plugin list`: enabled. 7 userConfig seçeneği ayarsız (`/plugin configure`).
- lua-lsp@claude-plugins-official v1.0.0, enabled. Not: lua-language-server ikilisi YOK (aşağıda).
- 9router 0.5.109 (npm -g, MIT, yazar decolua), paket kurulu; postinstall çalıştırılmadı (aşağıda). `9router` çalıştırılıp doğrulanmadı.

## Zaten kuruluydu (P1 "KUR" demişti, yanlış)
- vercel CLI 59.23.2 (`vercel --version`), ecc@ecc (plugin list), skillspector (~/.local/bin).

## Engellenen, izin gerekli
Auto-mode sınıflandırıcı şu toplu komutu "Untrusted Code Integration" diye reddetti; atlatmadım:
`npm i -g --allow-scripts=9router 9router` · `winget install LuaLS.lua-language-server` · `gh release download router-for-me/CLIProxyAPI v8.0.41 (windows_amd64.zip)`.
- 9router postinstall (hooks/postinstall.js, 26 satır): SQLite bağımlılıklarını ~/.9router/runtime'a ısıtır; okundu, zararsız, başarısızlık ölümcül değil, cli.js çalışınca kendini onarır.
- CLIProxyAPI v8.0.41 (MIT, 56k★, 2025-07): repo taraması temiz, kurulum bekliyor.
- LuaLS 3.19.1 winget (resmî): kurulum bekliyor.

## Güvenlik kapısı
- gitleaks: 9router repo 56 / npm tarball 51 / CLIProxyAPI 17 bulgu; hepsi dokümanda curl-auth örneği ya da sağlayıcı OAuth/istemci sabiti (generic-api-key, gcp-api-key, derlenmiş bundle'da 1 private-key dizgesi). Bizim sır yok. Değerler yazılmadı.
- semgrep p/security-audit: 9router 32 detect-child-process (CLI/tünel/güncelleyici, beklenen), CLIProxyAPI 83 WARNING (unsafe, math/rand), ERROR yok. İki resmî eklenti: gitleaks temiz, semgrep yalnız sha1 uyarısı.
- skillspector (`--no-llm`, API anahtarı yok): lua-lsp 12/100 LOW (README'deki sudo kurulum satırı). code-modernization 240 sn'de bitmedi (rc=124) → TAM TARANMADI (EKSİK). İlk toplu koşu anahtar yokluğuyla hemen hata vermişti; "asılı" saptamam yanlıştı. Kaynak Anthropic resmî pazaryeri olduğundan kuruldu.
- strix, ecc-agentshield: çalıştırılmadı (strix canlı hedef + LLM ister; agentshield kurulu değil). 
- Typosquat: nvidia/SkillSpector 21k★ Apache-2.0; 9router npm yazarı = repo sahibi decolua.

## Reddedilen / kurulmayan
- christopherkahler/base: lisans NOASSERTION → lisans kapısı (K2i: lisans uygun değilse muadil/yeniden yazım). Kurulmadı.
- zk/claude-mods: GitHub'da yok (zycck/claude-mods 58★ başka bir şey). Kaynak doğrulanamadı → kurulmadı.
- freeflow (zachlatta, MIT, macOS dikte uygulaması): masaüstü uygulama, bu parça kapsamı dışı → P-sonrası.
- skillspectd/skillspectrd: yazım hatası, nvidia/SkillSpector zaten kurulu.

## Kalan
CLIProxyAPI, LuaLS, 9router postinstall (izinle); base için lisans kararı; zk/claude-mods kaynağı için video QIevCKcRbUs/U6xZX4YWFkU'dan doğru repo adı.
Katalog: .kos/kopru/skill-mode/yetenek-ek-video.jsonl (4 satır).

## 1b-a ek (24 Eki)
- code-modernization yeniden tarandi: gitleaks temiz, semgrep yalniz sha1 cache anahtari (dusuk); skillspector --no-llm bitti ama analizorler degraded -> kesin 'temiz' denmez.
- Izin bekleyen 3 komut degismedi (9router postinstall, LuaLS, CLIProxyAPI): sinif. reddi, atlatilmadi.
