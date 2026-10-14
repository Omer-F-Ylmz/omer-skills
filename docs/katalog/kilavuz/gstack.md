# gstack — 55 benzersiz kayıt

**Amaç:** Uçtan uca yazılım teslim paketi: plan incelemeleri (CEO/tasarım/mühendislik/DX), hata ayıklama, QA, güvenlik, gönderim/dağıtım, tarayıcı ve iOS araçları.

**İç yapı:** gstack-<eylem> adlı skill'ler; gstack / gstack-router yönlendirici, gstack-core ortak çalışma zamanı; gruplar: plan-*, design-*, ios-*, qa/qa-only, ship/land-and-deploy, freeze/guard/careful güvenlik.

## En güçlü parçalar
- `gstack-investigate` — Kök neden araştırmalı sistematik hata ayıklama.
- `gstack-review` — Birleştirme öncesi PR incelemesi.
- `gstack-ship` — Taban dalı birleştir, test koş, diff incele, VERSION/CHANGELOG, commit, push, PR tek akış.
- `gstack-qa` — Web uygulamasını sistematik QA test edip bulunan hataları düzeltir.
- `gstack-careful` — Yıkıcı komutlar için güvenlik korkulukları.
- `gstack-cso` — Statik bulgulu güvenlik denetimi; nitelikli profillerde yeniden üretim ve onarım adayı ekler.
- `gstack-spec` — Belirsiz niyeti beş aşamada kesin, yürütülebilir spesifikasyona çevirir.
- `gstack-browse` — Gerçek tarayıcı sürer: sayfa okur, akış tıklar, ekran görüntüsü, konsol hatası.

## Birlikte kullanım
- gstack-spec → gstack-autoplan (CEO, tasarım, mühendislik, DX incelemeleri) → gstack-review → gstack-ship.
- gstack-ship + gstack-land-and-deploy + gstack-canary: yayın ve sonrası izleme.
- gstack-context-save + gstack-context-restore: oturumlar arası bağlam.
- gstack-freeze / gstack-guard + gstack-careful: düzenlemeyi dizine kısıtla, yıkıcı komutu uyar.

## Tuzaklar
- gstack ile gstack-router aynı tanımlı yönlendirici; ikisi birden gereksiz.
- gstack-scrape ve gstack-setup-browser-cookies gerçek oturum açmış tarayıcı çerezlerini kullanır; hesap güvenliği riski.
- gstack-qa hata düzeltir; yalnız rapor isteniyorsa gstack-qa-only.

## Üyeler
- skill (55): gstack, gstack-autoplan, gstack-benchmark, gstack-benchmark-models, gstack-browse, gstack-canary, gstack-careful, gstack-codex, gstack-context-restore, gstack-context-save, gstack-core, gstack-cso, gstack-design-consultation, gstack-design-html, gstack-design-review, gstack-design-shotgun, gstack-devex-review, gstack-diagram, gstack-document-generate, gstack-document-release, gstack-freeze, gstack-guard, gstack-health, gstack-investigate, gstack-ios-clean, gstack-ios-design-review, gstack-ios-fix, gstack-ios-qa, gstack-ios-sync, gstack-land-and-deploy, gstack-landing-report, gstack-learn, gstack-make-pdf, gstack-office-hours, gstack-pair-agent, gstack-plan-ceo-review, gstack-plan-design-review, gstack-plan-devex-review, gstack-plan-eng-review, gstack-plan-tune …
