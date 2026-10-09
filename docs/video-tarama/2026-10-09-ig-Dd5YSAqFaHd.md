# OpenShell is the safe, private runtime for autonomous AI agents.
## Künye
OpenShell is the safe, private runtime for autonomous AI agents. · git.radar · süre: 1:07 · ? · https://www.instagram.com/reel/Dd5YSAqFaHd/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-35 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 33396 tk · claude-haiku-5-5: claude-haiku-5-5 · 116871 tk
## Özet
Kısa reel, NVIDIA'nın Rust ile yazılmış OpenShell projesini tanıtıyor. OpenShell, otonom yapay zekâ ajanları için güvenli ve özel bir çalışma ortamı. Çekirdek düzeyinde politika uyguluyor, ajanın gerçek kimlik bilgilerini görmesini engelliyor ve politika değişikliklerini biçimsel doğrulamayla denetliyor. Video GitHub README sayfasını kaydırıyor. Quickstart kurulumu, skills kurulumu ve SDK'lar ekranda geçiyor.
## Bölümler
- 0:00 Giriş: ajanlara verilen fazla özgürlük sorunu
- 0:11 OpenShell nasıl çalışır, Quickstart
- 0:34 SDK'lar ve topluluk bölümleri
- 1:04 GitHub sayfasına yönlendirme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| OpenShell | yok | CLI | https://github.com/NVIDIA/OpenShell | Otonom AI ajanları için güvenli, özel çalışma ortamı; çekirdek düzeyinde politika uygular. | 0:00 | README başlığı OpenShell logosu ve 'safe, private runtime' paragrafı. (karede: GitHub NVIDIA/OpenShell README, OpenShell logosu, 'OpenShell is the safe, private runtime for fleets of autonomous AI agents' paragrafı) |
| Skills CLI | yok | skill | https://github.com/NVIDIA/OpenShell | npx skills add NVIDIA/OpenShell ile ajana OpenShell CLI'ı kullanmayı öğreten skill'leri kurar. | 0:27 | Ekran metni: npx skills add NVIDIA/OpenShell; skill'ler CLI'ı sürmeyi öğretir. |
| Docker | yok | teknik | yok | OpenShell için gereken konteyner ortamlarından biri (Docker, Podman veya host sanallaştırma). | 0:22 | Quickstart: 'plus Docker, Podman, or host virtualization'. (karede: Quickstart: 'You need Linux, macOS on Apple Silicon, or Windows with WSL 2 (experimental), plus Docker, Podman') |
| OpenCode | yok | CLI | yok | Run Your First Agent rehberinde ücretsiz OpenRouter modeliyle çalıştırılan örnek ajan. | 0:22 | Quickstart: 'it runs OpenCode against a free OpenRouter model'. (karede: 'To run a real agent, follow Run Your First Agent: it runs OpenCode against a free OpenRouter model') |
| OpenRouter | yok | teknik | yok | Örnek ajanın kullandığı ücretsiz model sağlayıcı servisi. | 0:22 | Aynı Quickstart cümlesinde 'free OpenRouter model' geçiyor. (karede: 'OpenCode against a free OpenRouter model' cümlesi) |
| Kubernetes | yok | teknik | yok | Gateway'in Helm ile dağıtıldığı ortam; CNI NetworkPolicy uygulamalı. | 0:22 | Explore Further: 'Kubernetes: deploy the gateway with Helm'. (karede: Explore Further listesinde Kubernetes satırı, 'must enforce NetworkPolicy') |
| Helm | yok | CLI | yok | Kubernetes üzerinde gateway dağıtımı için anılan paket yöneticisi. | 0:22 | 'deploy the gateway with Helm' ifadesi. (karede: Kubernetes satırı: 'deploy the gateway with Helm') |
| Python SDK (uv) | yok | teknik | yok | uv add openshell ile Python SDK kurulumu. | 0:34 | OCR: 'uv add openshell' ve Python satırı. · kanıt: yok |
| TypeScript SDK | yok | teknik | yok | npm install @nvidia/openshell-sdk ile TypeScript SDK kurulumu. | 0:35 | OCR: 'npm install @nvidia/openshell-sdk'. · kanıt: yok |
| Go SDK | yok | teknik | yok | Go için SDK (go get). | 0:36 | OCR: 'go get' ve sdk/go@latest yolu. · kanıt: yok |
| Rust SDK | yok | teknik | yok | cargo add openshell-sdk --git ile Rust SDK. | 0:37 | OCR: 'cargo add openshell-sdk --git'. · kanıt: yok |
| curl | yok | CLI | yok | OpenShell kurulum betiğini indirmek için kullanılan komut satırı aracı. | 0:22 | curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/i (karede: Quickstart kod bloğunda curl satırı; URL sonu kesik) |
| npm | yok | CLI | yok | TypeScript SDK paketini kurmak için kullanılan paket yöneticisi. | 0:35 | npm install @nvidia/openshell-sdk (karede: kanıttan) npm install @nvidia/openshell-sdk |
| cargo | yok | CLI | yok | Rust SDK'sını git deposundan eklemek için kullanılan paket yöneticisi. | 0:37 | cargo add openshell-sdk --git (karede: kanıttan) cargo add openshell-sdk --git |
| Podman | yok | CLI | yok | OpenShell için Docker alternatifi olarak gösterilen konteyner aracı. | 0:22 | plus Docker, Podman, or host virtualization (karede: Quickstart gereksinimleri metninde 'Docker, Podman' ifadesi) |
| WSL 2 | yok | teknik | yok | Windows'ta Linux çekirdeğini çalıştıran sanal alt sistem; OpenShell için deneysel destek. | 0:22 | Windows with WSL 2 (experimental) (karede: Quickstart gereksinimleri: 'Windows with WSL 2 (experimental)') |
| GitHub | yok | teknik | yok | OpenShell'in kaynak kodu, README ve issue/PR takibinin yapıldığı platform. | 1:04 | You can check it out yourself on their GitHub page. |
## Açıklama bağlantıları
- https://github.com/NVIDIA/OpenShell — OpenShell GitHub deposu · aday: evet (OpenShell) · Videoda anlatılan aracın deposu; izleyici kullanabilir. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/install.sh / sh | CLI'ı ve yerel gateway'i kurar (OCR'de komut kısmen okunuyor). (karede: Quickstart kutusunda 'curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/i' ve alt satır) | 0:22 | kare |
| openshell sandbox create --name demo | demo adlı sandbox oluşturur. (karede: Kutuda 'openshell sandbox create --name demo' satırı) | 0:22 | kare |
| npx skills add NVIDIA/OpenShell | OpenShell skill'lerini ajana ekler. | 0:27 | altyazı |
| uv add openshell | Python SDK'yı projeye ekler. | 0:34 | altyazı |
| npm install @nvidia/openshell-sdk | TypeScript SDK'yı kurar. | 0:35 | altyazı |
| cargo add openshell-sdk --git https://github.com/NVIDIA/OpenShell --tag | Rust SDK'yı ekler (etiket OCR'de okunmuyor). | 0:37 | altyazı |
| OPENSHELL_TELEMETRY_ENABLED=false | Gateway'de telemetriyi kapatır. | 0:50 | altyazı |
| curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/i… (kırpık) | OpenShell kurulum betiğini indirir; CLI ve yerel gateway'i kurar. (karede: Quickstart kod bloğunda curl satırı; URL sonu kesik) | 0:22 | kare |
| go get github.com/NVIDIA/OpenShell/sdk/go@latest | Go SDK'sını en son sürümle ekler. | 0:38 | kare |
| cargo add openshell-sdk --git https://github.com/NVIDIA/OpenShell --tag … (kırpık) | Rust SDK'sını git deposundan belirli bir etiketle ekler. | 0:37 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Proje 10.760 yıldıza ulaştı ve hızla büyüyor. | 0:00 | sayısal |
| Ajan onaylanmamış klasöre bakarsa veya güvenilmeyen siteye veri gönderirse OpenShell durdurur. | 0:00 | özellik |
| Güvenlik kurallarında gizli boşluk olmadığını kendi kendine kontrol eder. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | OpenShell | OpenShell | Proje adı konuşmada anılıyor. |
| açıklama | GitHub | aday değil: konu dışı | Yalnızca barındırma sitesi, depo bağlantısı OpenShell adayına bağlı. |
| açıklama | Rust | Rust SDK | Açıklamada dil Rust; SDK listesinde görünüyor. |
| açıklama | https://github.com/NVIDIA/OpenShell | OpenShell | Açıklama bağlantısı. |
| kare 0:22 | Docker | Docker | Quickstart gereksinimi. |
| kare 0:22 | OpenCode | OpenCode | Run Your First Agent cümlesi. |
| kare 0:22 | OpenRouter | OpenRouter | Ücretsiz model cümlesi. |
| kare 0:22 | Kubernetes | Kubernetes | Explore Further listesi. |
| kare 0:22 | Helm | Helm | Kubernetes satırı. |
| ekran 0:27 | npx skills add | Skills CLI | OCR komutu. |
| ekran 0:34 | uv add openshell | Python SDK (uv) | OCR komutu. |
| ekran 0:35 | npm install @nvidia/openshell-sdk | TypeScript SDK | OCR komutu. |
| ekran 0:36 | go get | Go SDK | OCR komutu. |
| ekran 0:37 | cargo add | Rust SDK | OCR komutu. |
| ekran 0:11 | WSL 2 | aday değil: başka adayın parçası (OpenShell) | Desteklenen platform notu. |
| ekran 0:50 | OPENSHELL_TELEMETRY_ENABLED | aday değil: başka adayın parçası (OpenShell) | Telemetri ayarı. |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı. |
## Kareden okunanlar
- 0:00: GitHub NVIDIA/OpenShell, Issues 314, Pull requests 183, README, Apache 2.0, PyPI openshell rozetleri, 'Important: New in OpenShell 0.1.x' notu.
- 0:11: How It Works: kernel-level enforcement ve formally verified policy changes maddeleri; Quickstart başlığı, WSL 2, Docker, Podman.
- 0:22: Quickstart curl komutu, openshell sandbox create --name demo, OpenCode/OpenRouter cümlesi, Explore Further listesi.
## Belirsizlikler
- Dil alanı belirsiz; konuşma İngilizce.
- Kare 0:00'da Issues 314, OCR akışında 3148 görünüyor.
- curl komutunun dosya adı (install.sh) ekranda tam okunmuyor; tahmin.
- Helm, Kubernetes, Python/TypeScript/Go/Rust SDK satırları README listesinde görünüyor; videoda kısaca kaydırılıyor.
- Yorumlar girişsiz alınamadı.
- Sözlük eşleşmeleri (React, Three.js, Inter, Claude vb.) gürültü; videoda kullanılmıyor.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/NVIDIA/OpenShell | açıklama | açıklama | evet |
| https://raw.githubusercontent.com/NVIDIA/OpenShell/main/ | 0:12 | ekran | evet |
| github.com/NVIDIA/OpenShell/sdk/go@latest | 0:38 | ekran | evet |
| https://github.com/NVIDIA/OpenShell | 0:39 | ekran | evet |
| https://github.com/NVIDIA/OpenShel | 0:48 | ekran | evet |
| https://github.com/NVIDIA/OpenShell--tag | 0:40 | ekran | hayır |
| https://github.com/NVIDIA/OpenShell-tag | 0:52 | ekran | hayır |
| https://ithub.com/NVIDIA/OpenShell--tag | 0:51 | ekran | hayır |
| https://raw.githubusercontent.com/NVIDIA/OpenShell/main/i | 0:13 | ekran | hayır |
| https://raw.githubusercontent.com/NVIDIA/OpenShell/main/i | 0:23 | ekran | hayır |
| https://raw.githubusercontent.com/NVIDIA/OpenShell/main/i | 0:29 | ekran | hayır |
| github.com/NVIDIA/OpenShel/sdk/go@latest | 0:51 | ekran | hayır |
## İş akışı
- 1. adım — GitHub'da OpenShell deposunu aç ve README'deki özet ile 'How It Works' bölümünü incele — araçlar: GitHub
- 2. adım — Quickstart'taki gereksinimleri kontrol et (Linux/macOS/WSL 2 ve Docker/Podman/host virtualization) — araçlar: Docker, Podman, WSL 2
- 3. adım — Kurulum betiğini indirip CLI ve yerel gateway'i kur — araçlar: curl, OpenShell
- 4. adım — Demo adında bir sandbox oluştur — araçlar: OpenShell
- 5. adım — Skill'leri npx ile ajana ekle — araçlar: npm, Skills CLI
- 6. adım — Python SDK'sını uv ile ekle — araçlar: uv, Python
- 7. adım — TypeScript SDK'sını npm ile ekle — araçlar: npm, TypeScript
- 8. adım — Go SDK'sını go get ile ekle — araçlar: Go
- 9. adım — Rust SDK'sını cargo ile git deposundan ekle — araçlar: cargo, Rust
- 10. adım — Gateway'de telemetriyi OPENSHELL_TELEMETRY_ENABLED=false ile kapat — araçlar: OpenShell
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
