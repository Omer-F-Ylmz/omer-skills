# thedotmack — 25 benzersiz kayıt

**Amaç:** claude-mem bellek sıkıştırma sistemi ve yan skill'leri: oturumlar arası gözlem arama, plan-uygula, devir, kod tabanı öğrenme, zaman çizelgesi raporları, PR bekçiliği, bulut senkronu.

**İç yapı:** claude-mem ve claude-mem-cowork [plugin] + mcp-search [mcp] + claude-mem:<x> skill'leri: bellek (mem-search, knowledge-agent, mode-creator), iş akışı (make-plan, do, handoff, babysit), rapor (timeline, weekly-digests).

## En güçlü parçalar
- `claude-mem:mem-search` — 'Bunu daha önce çözdük mü, geçen sefer nasıl yaptık' sorularında.
- `claude-mem:smart-explore` — Tam dosya okumak yerine tree-sitter AST ile token tasarruflu yapısal arama.
- `claude-mem:make-plan` — Çok adımlı uygulamadan önce plan; do ile yürütülür.
- `claude-mem:handoff` — Oturum uzayınca ya da aynı bozuk çözüm tekrarlanınca devir.
- `claude-mem:babysit` — PR yorumları, review ve CI'ı tüm sorunlar çözülene dek izler.
- `claude-mem:learn-codebase` — Yeni/yabancı projeye başlarken kod tabanını öğrenme.
- `claude-mem:pathfinder` — Refactor öncesi yinelenen sistemleri birleştirme, mimari denetim.
- `claude-mem:timeline-report` — Proje geçmişi analizi ve tam proje raporu.

## Birlikte kullanım
- claude-mem:make-plan → claude-mem:do.
- mcp-search + claude-mem:mem-search: MCP ve skill üzerinden aynı bellek.
- claude-mem:timeline-report + claude-mem:weekly-digests: geçmişi rapor ve haftalık hikâyeye çevirmek.

## Tuzaklar
- claude-mem-cowork parçaları cmem.ai'ye akıtır (Pro); cloud-sync de buluta yedekler, gizlilik riski.
- claude-mem:Agent Cost Report OpenRouter fiyatıyla tahmin eder; fatura değil.
- claude-mem:design-is, wowerpoint, what-the bellek dışı; aileye adla bağlı.
- claude-mem:ccs-align yerel-diger'deki ccs-align ile çakışan kopya.

## Üyeler
- mcp (1): mcp-search
- plugin (2): claude-mem, claude-mem-cowork
- skill (22): claude-mem:Agent Cost Report, claude-mem:babysit, claude-mem:ccs-align, claude-mem:cloud-sync, claude-mem:design-is, claude-mem:do, claude-mem:handoff, claude-mem:how-it-works, claude-mem:knowledge-agent, claude-mem:learn-codebase, claude-mem:make-plan, claude-mem:mem-search, claude-mem:mode-creator, claude-mem:oh-my-issues, claude-mem:pathfinder, claude-mem:smart-explore, claude-mem:standup, claude-mem:timeline-report, claude-mem:version-bump, claude-mem:weekly-digests, claude-mem:what-the, claude-mem:wowerpoint
