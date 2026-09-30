# Codex plugin for Claude Code
ad: Codex plugin for Claude Code
tur: plugin
video: V0XbuApxlhg
repo: openai/codex-plugin-cc
lisans: bilinmiyor (repoda LICENSE ve NOTICE dosyası var, metni okunamadı; büyük olasılıkla Apache-2.0 ama doğrulanmadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/openai/codex-plugin-cc
telemetri: bilinmiyor. README'nin okunan kısmında telemetri anlatılmıyor. Ancak işler Codex CLI üzerinden OpenAI'ye gittiği için kod ve istemler OpenAI'ye gönderilir.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
OpenAI'nin resmi Claude Code plugin'i. Claude Code içinden Codex'e kod incelemesi (review) yaptırmayı ve görev devretmeyi (rescue/transfer) sağlar. Arka plan işlerini status/result/cancel komutlarıyla yönetir.
## Mekanizma
Plugin marketplace üzerinden kurulur (/plugin marketplace add openai/codex-plugin-cc, ardından /plugin install codex@openai-codex). Yerel olarak kurulu Codex CLI'yi (npm @openai/codex) Node.js (>=18.18) betikleriyle çalıştırır. Repo ağacında bir broker/uygulama sunucusu (tsconfig.app-server, broker-endpoint testi) ve durum/süreç yönetimi (state, process, git testleri) görünüyor. Komutlar: /codex:review (salt okunur, --base ref, --wait/--background), /codex:adversarial-review (yönlendirilebilir, tasarım ve risk sorgulayan), /codex:rescue, /codex:transfer, /codex:status, /codex:result, /codex:cancel, /codex:setup. Ayrıca /agents içinde codex:codex-rescue alt ajanı gelir. Hepsi kullanıcının kendi Codex girişini kullanır. Dahili iş akışının ayrıntısı README'nin kesilen kısmında olduğu için okunamadı.
## Kanıt
- Claude Code arayüzünden Codex/GPT modellerine görev devretmeyi kolaylaştırır. → doğrulandı · Repo README'si /codex:rescue, /codex:transfer, /codex:status, /codex:result, /codex:cancel komutlarını ve codex:codex-rescue alt ajanını listeliyor.
- Claude'a 20x fazla ödüyorsunuz (video başlığı) → sınanamadı · Video sayfasından yalnızca başlık alındı. Transkript ve maliyet verisi yok.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- /plugin marketplace add openai/codex-plugin-cc
- /plugin install codex@openai-codex
- /reload-plugins
- /codex:setup (Codex eksikse npm ile kurmayı önerir; elle: npm install -g @openai/codex)
- Giriş yapılmadıysa: !codex login (ChatGPT hesabı, Free dahil, ya da OpenAI API anahtarı)
- Gereksinim: Node.js 18.18+
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude Code'dan çıkmadan ikinci bir modelden (Codex/GPT) bağımsız kod incelemesi almayı sağlar. Uzun işleri Codex'e arka planda devredip Claude kotasını rahatlatır. Karşıt (adversarial) inceleme tasarım risklerini yakalamaya yarar.
## Maliyet/risk
Codex kullanım limitinden düşer, ücretsiz ChatGPT hesabında kısıtlı olabilir. Kod OpenAI'ye gider (gizlilik). rescue/transfer Codex'in dosya değişikliği yapmasına yol açabilir, izin ayarlarına dikkat edilmeli. Büyük çok dosyalı incelemeler uzun sürer. Lisans, yıldız ve son commit doğrulanmadı.
## Tasarruf
Doğrudan token tasarrufu aracı değil. Dolaylı olarak inceleme ve görev yükünü Codex kullanım limitine kaydırır, Claude bağlamını ve kotasını korur. Bu iddia videonun başlığından ("20x daha az öde") gelen çıkarım. Sayısal bir doğrulama yok.
## Üretilebilir
hedef_tur: plugin
tarif: Zaten hazır plugin var, yeniden yazmaya gerek yok; doğrudan kurulabilir. Kendi sürümümüz istenirse: .claude-plugin/marketplace.json ile bir plugin oluşturulur. İçine slash komutları (review, rescue, status) konur. Bunlar Bash ile `codex exec` / `codex review` çağırır, çıktıyı dosyaya yazar, arka plan işleri için PID/iş kaydı tutar. İnceleme için ayrıca bir alt ajan tanımı eklenir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### /codex:review: mevcut değişiklikler ya da --base ile dal karşılaştırması için salt okunur Codex incelemesi; --wait/--background destekler
kaynak: https://github.com/openai/codex-plugin-cc
### /codex:adversarial-review: ek odak metniyle tasarım, varsayım ve risk sorgulayan yönlendirilebilir inceleme
kaynak: https://github.com/openai/codex-plugin-cc
### /codex:rescue, /codex:transfer ve codex:codex-rescue alt ajanı ile görev devri
kaynak: https://github.com/openai/codex-plugin-cc
### /codex:status, /codex:result, /codex:cancel ile arka plan iş yönetimi
kaynak: https://github.com/openai/codex-plugin-cc
### /codex:setup ile Codex hazır mı kontrolü ve npm ile kurulum önerisi
kaynak: https://github.com/openai/codex-plugin-cc
## Destek
- V0XbuApxlhg · 13:51 · Claude Code arayüzünden Codex/GPT modellerine görev devretmeyi kolaylaştırır. · kanıt: There is a Codex plugin for Claude code.
- V2RIVnGCy74 · 8:03 · OpenAI'nin resmi eklentisi; Codex/GPT'yi Claude Code'a bağlar, kod incelemesi, adversarial review ve Codex rescue ile iş devri sağlar. · kanıt: Resmî OpenAI eklentisi; Codex ve GPT modellerini Claude Code'a bağlıyor. (karede: İlgili kare yok; altyazıdan.)
