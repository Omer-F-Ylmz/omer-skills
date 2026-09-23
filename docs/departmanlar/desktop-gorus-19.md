# Desktop ikinci görüş — KURULUM-19 departmanlar

Genel: yapı doğru; 9 müdür, description 363/600 token. Dört düzeltme:

## 1. surec çok büyük (147 araç, tümünün %35'i)
147 araçlık bir müdür yönlendirici olamaz; "surec" artık "diğer" gibi çalışıyor. Önerim alt departmanlara bölmek:
- surec-plan: plan, spec, PRD, brainstorm, writing-plans, phoenix-*, make-plan/do
- surec-inceleme: code-review, ponytail-*, requesting/receiving-code-review, verification
- surec-git-yayin: git, ship, deploy, land, canary, vercel, hetzner, release
- surec-ajan-arac: skill/plugin/MCP/hook geliştirme, claude-mem, omni-*/cli-*, gstack yardımcıları
Her alt departman için müdür yalnız ≥3 araç kuralıyla.

## 2. 129 "gözden geçir" (%31)
Çoğu ad önekinden belli. elle-desen.json (önek → departman) önerisi, elle.json'dan sonra, Jev'den önce uygulanır:
gstack-* → (içeriğe göre surec-* alt departmanları; tasarım olanlar frontend) · design:* ve design-* → frontend · dotnet*/msbuild*/binlog*/*-ef-core* → backend-dotnet · data:* → veri-db · omni-*, cli-* (OmniRoute) → surec-ajan-arac · phoenix-* → surec-plan · *security*/*pentest*/strix/opengrep/0day/threat-* → guvenlik · *test*/playwright*/webapp-testing → test-qa.
Desen sonrası kalan Act altı liste raporda.

## 3. Frontend müdürüne eksikler
- Proje türü dalı (Ömer'in projeleri çoğunlukla ASP.NET Razor + Tailwind; bazıları Astro/React): adım 3'ten önce "yığın: Razor → dotnet-aspnetcore + frontend-craft; React/Next → vercel-react-best-practices + vercel-composition-patterns; Astro → frontend-craft".
- Performans adımı (a11y'den sonra): fixing-motion-performance · performance-optimization; React'te vercel-react-best-practices. Kapı: Lighthouse/Web Vitals sayısı raporda.
- Tasarım tuvali: yön keşfi görsel isterse Claude Design (claude-design MCP) · Figma · Stitch — "ne zaman" satırıyla; DESIGN.md yine önce.
- Premium landing/scroll işleri: web-sahne-desenleri · scroll-craft · high-end-visual-design — yalnız brief bunu istiyorsa, frontend-craft ana hattı altında.

## 4. Süreç notu
19 oturumunda `find / -iname "omer-kurallar*.md"` bütün diski taradı ve saatlerce açık kaldı. Dosya C:\Projeler\omer-kurallar.md (15'ten beri kural kaynağı). Kök (/) taraması yapılmamalı; bilinen yol ya da graphify.
