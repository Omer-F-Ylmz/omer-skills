# Parti A brief — 2026-09-28 (Desktop ikinci görüş girdisi)

Kaynak: `video brief` × 4 tarama raporu + katman raporu (docs/kurulumlar/2026-09-28-uygula.md, ikinci koşu bölümü).

## brief: 2026-09-28-NyNScAc2u_o.md
### Özellik kararları
### Departman
### İddialar
### Linkler
- https://youtu.be/NyNScAc2u_o
- https://www.awwwards.com/sites/clou

## brief: 2026-09-28-Gg35_iQWx7g.md
### Özellik kararları
### Departman
### İddialar
### Linkler
- https://youtu.be/Gg35_iQWx7g
- https://skills.sh
- https://github.com/anthropics/skills
- https://openrouter.ai

## brief: 2026-09-28-JNM_rxqtlvY.md
### Özellik kararları
### Departman
### İddialar
### Linkler
- https://youtu.be/JNM_rxqtlvY
- https://github.com/JuliusBrussee/caveman
- https://github.com/phuryn/claude-usage

## brief: 2026-09-28-jGJ09wdTGDI.md
### Özellik kararları
### Departman
### İddialar
### Linkler
- https://youtu.be/jGJ09wdTGDI
- https://hostinger.com/YILDIZDIKME10

## brief: 2026-09-28-uygula.md (araştırılan 4 aday)
### Özellik kararları
- claude-usage/terminal-ozet → KUR — gerçek kullanımı gösteriyor, kurulumu geri alınabilir, ek risk yok.
- claude-usage/web-dashboard → DENE — hipotez: URL-durum + localStorage kalıcı panel deseni kendi iç panolarımızda tekrar filtre kurma turunu azaltır · metrik: aynı görünüme dönmek için gereken tıklama/istek sayısı · bütçe: 1 iç araç, ≤2 saat · geri_alma: deseni uygulamazsak mevcut sunucu-taraflı görünüm kalır · eşik: tıklama sayısı %30 düşerse benimse.
- claude-usage/vscode-entegrasyonu → ZATEN VAR — zaten var: terminal-ozet + web-dashboard aynı veriyi IDE bağımlılığı olmadan karşılıyor.
- skills-cli/skill-kurma → KUR — MIT, Snyk audit'li, mevcut katalogda benzer tek-komut skill kurucu yok.
- skills-cli/gecici-kullan → KUR — aynı artefakt, ek risk yok; kurulum öncesi inceleme için doğrudan kullanılabilir.
- nyns-3d-galeri-promptu/3d-dairesel-ring-galeri → ZATEN VAR — zaten var: docs/kurulumlar/bekleyen/teknik-3d-dairesel-ring-galeri-kart-dizilimi-transform-style-preserve-3d.md (aynı video, onaysız bekliyor)
- nyns-3d-galeri-promptu/scroll-mouse-parallax-rotasyon → UYARLA — fikir: scroll/mouse olaylarını tek ortak açı fonksiyonuna (angleOf) bağlamak · hedef: departman-frontend prompt şablonu notu · kod yazılmaz
- jgj0-claude-design-promptu/tek-prompt-e-ticaret-sitesi → UYARLA — kurulacak araç değil; fikir (asset+sıfat kısıtlı tek prompt kalıbı) kendi frontend-craft akışımıza aktarılabilir, kod yazılmaz.
- jgj0-claude-design-promptu/dogal-dille-iteratif-revizyon → ZATEN VAR — zaten var: commit 3321f38 (BIRLESTIR K15 -> omer-kurallar:10 iterasyon cümlesi) bu kalıbı zaten kataloglamış.
- jgj0-claude-design-promptu/ciktiyi-claude-code-a-tasiyip-optimize-etme → DENE — hipotez: tasarım-öncelikli çıktının performans açığı Claude Code'a aktarılıp optimize edilince ölçülebilir kapanır · metrik: Lighthouse performans skoru · bütçe: 1 örnek site, ≤30 dk oturum · geri_alma: iyileşme yoksa bırak · eşik: ≥85 Lighthouse.
### Departman
- claude-usage → verimlilik (0.71)
- skills-cli → surec-ajan-arac (1.00)
- nyns-3d-galeri-promptu → frontend (0.98)
- jgj0-claude-design-promptu → frontend (0.99)
### İddialar
- "logları okuyan bir dashboard/JSON API" → doğru (README (dashboard.py `/api/data`) + cli.py yorumları)
- session.jsonl'den input_tokens/output_tokens/cache_read okunuyor → doğru (scanner.py alan adları (on.md envanteri))
- araç veri göndermiyor / telemetri yok → doğru (ToolHunter incelemesi + pyproject.toml `dependencies = []`)
- npx skills add ile anthropics/skills gibi repolardan tek komutla skill kurulur → doğru (README.md (vercel-labs/skills))
- CLOU 2022'de Awwwards Site of the Day, puan 7,62/10 → doğru (awwwards.com/sites/clou)
- Tam profesyonel site fiyatı 50.000-100.000 dolar → doğrulanamadı (yok)
- Prompt hazırlığı ~2 gün sürüyor, 5-10 kez test ediliyor → doğrulanamadı (yok)
- Tek promptla birkaç dakikada tüm stil/renk paleti/taslak çıkar (3:15-4:18) → doğru (Claude Design ürün sayfası (claude.com/product/design))
- Performans zayıf, sadece optimizasyon eksik, tasarım güçlü (12:00) → doğru (agence-scroll.com 2026 Guide)
- İngilizce prompt yazmak AI'dan daha iyi sonuç verir (1:39) → doğrulanamadı (-)
### Linkler
