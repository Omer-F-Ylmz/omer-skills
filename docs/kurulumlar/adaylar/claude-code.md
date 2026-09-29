# Claude Code
ad: Claude Code
tur: CLI
video: L9c49WVG_ho
repo: anthropics/claude-code
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/anthropics/claude-code
telemetri: README'ye göre kullanım verisi (kod kabul/ret), ilgili konuşma verisi ve /bug ile gönderilen geri bildirim toplanıyor. Saklama süresi sınırlı ve geri bildirim model eğitiminde kullanılmıyor deniyor. Ayrıntılar resmi veri kullanımı sayfasında. Kapatma ayarlarını doğrulamadım.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
Anthropic'in terminalde çalışan ajan tabanlı kodlama aracı. Kod tabanını anlıyor, rutin işleri yapıyor, kodu açıklıyor, git iş akışlarını doğal dille yürütüyor. Terminal, IDE ve GitHub'da (@claude) kullanılabiliyor.
## Mekanizma
Terminalde `claude` komutuyla açılan ajan döngüsü. Anthropic modellerini çağırıyor. Dosya okuma/yazma, kabuk komutu ve git gibi araçları kullanıyor. Eklentiler (komut, ajan, hook, skill), MCP ve ayar dosyalarıyla genişletiliyor. Repo yalnızca README, eklentiler, örnekler ve betikler içeriyor. Çekirdek kaynak kodu depoda görünmüyor. LICENSE.md var ama içeriğini okumadım.
## Kanıt
- Claude Code, ücretsiz anahtarın verildiği bir kodlama ajanıdır (videodaki iddia). → çürütüldü · Resmi README kurulumu ve kullanımı anlatıyor ama ücretsiz anahtardan söz etmiyor. Anahtar/hesap gerektirdiği varsayımı kesin doğrulanmadı. Bu yüzden 'ücretsiz anahtar' iddiası doğrulanamadı, çürütme yönünde zayıf kanıt var.
- Claude Code bir kodlama ajanıdır. → doğrulandı · anthropics/claude-code README: 'agentic coding tool that lives in your terminal'.
- Karede Claude simgesi görünüyor. → sınanamadı · Videoyu izlemedim. Kare kanıtı doğrulanmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- macOS/Linux: curl -fsSL https://claude.ai/install.sh / bash
- Homebrew: brew install --cask claude-code
- Windows: irm https://claude.ai/install.ps1 / iex
- WinGet: winget install Anthropic.ClaudeCode
- npm (kullanımdan kalkıyor): npm install -g @anthropic-ai/claude-code
- Proje dizininde `claude` komutunu çalıştır
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Terminalden kod yazma, açıklama ve git işlerini otomatikleştirir. Plugin, hook ve MCP ile genişletilebilir. Bu ortamın kendisi de bu araçla çalışıyor.
## Maliyet/risk
Videodaki "ücretsiz anahtar" iddiası resmi README'de yok. Anahtar dağıtan üçüncü taraf kaynaklar dolandırıcılık ya da anahtar sızıntısı olabilir. Resmi kullanım Anthropic hesabı veya API ile yapılıyor. curl/bash ve irm/iex kurulumları betiği doğrulamadan çalıştırıyor. Konuşma verisi Anthropic'e gidiyor. Lisans belirsiz, muhtemelen tescilli.
## Tasarruf
Token aracısı değil. Tasarruf mekanizması yok.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### Terminal, IDE ve GitHub (@claude) üzerinden doğal dille kodlama ve git iş akışları
kaynak: https://github.com/anthropics/claude-code
### Eklenti sistemi: code-review, commit-commands, hookify, feature-dev, plugin-dev, security-guidance, ralph-wiggum vb.
kaynak: https://github.com/anthropics/claude-code/tree/main/plugins
### /bug komutuyla geri bildirim ve hata bildirimi
kaynak: https://github.com/anthropics/claude-code
### Devcontainer ve örnek hook, ayar, MDM, gateway yapılandırmaları
kaynak: https://github.com/anthropics/claude-code/tree/main/examples
## Destek
- L9c49WVG_ho · 0:17 · Ücretsiz anahtarın verildiği kodlama ajanı · kanıt: Karede Claude simgesi görünüyor. · iddia: Anahtar Claude Code veya Cursor'a verilince ajan tamamen ücretsiz çalışıyor
- M9qgd_KJkWc · 0:00 · Terminale komut kopyalanarak kurulan, web sitesi üretiminde kullanılan kodlama aracı. · kanıt: First, install Cloud Code from the provided URL and copy the command into your terminal.
