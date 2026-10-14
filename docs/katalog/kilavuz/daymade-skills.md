# daymade-skills — 60 benzersiz kayıt

**Amaç:** Daymade'in Claude Code/Codex için kanıt odaklı operasyon eklentileri: Git/GitHub güvenliği, belge/veri kazıma, LLM değerlendirme, ağ/tünel teşhisi, Çin platformları entegrasyonu.

**İç yapı:** Tümü [plugin]; daymade-* önekli suit'ler (audio, docs, financial, macos, skill, codex) birçok skill'i paketler, geri kalanı tek amaçlı eklentiler (github-*, *-doctor, *-scraper).

## En güçlü parçalar
- `git-safety-net` — Temizlik öncesi itilmemiş/yanlış dal commit'lerini, kirli worktree'leri denetleyip korur ve kurtarır.
- `github-review-pr` — PR'ı canlı tabana karşı değişmez nesneler ve üç yollu merge ile inceler; merge hazırlığı için.
- `deep-research` — Kaynak/iddia kayıtlı, özgün kaynak doğrulamalı kanıt izli araştırma raporu üretir.
- `fact-checker` — Belgedeki olgusal iddiaları web ve resmi kaynakla doğrulayıp onaylı düzeltme önerir.
- `github-sensitive-data-cleanup` — Repo geçmişinden sır, API anahtarı, özel alan adı/IP, PII tarayıp temizler.
- `repomix-safe-mixer` — Kod tabanını repomix ile paketlemeden önce gömülü kimlik bilgilerini otomatik ayıklar.
- `debugging-network-issues` — Ağ, akış ve protokol hatalarında yanlışlama öncelikli katmanlı deneylerle genel geri dönüş.
- `llm-eval-harness` — OpenAI/Anthropic uyumlu üçüncü taraf LLM uç noktasını erişim, sadakat, hız, eşzamanlılıkla sınar.
- `auto-repo-setup` — Reponun gerçek durumunu tespit edip kanıta dayalı kurulum, onarım ve güvenli Git akışı.
- `frontend-visual-qa` — Çizilmiş UI, deck, dashboard ve Markdown/Obsidian görsel yerleşimini denetler.

## Birlikte kullanım
- git-safety-net → github-review-pr → github-ops: yerel durumu koru, PR'ı incele, gh ile birleştir.
- repomix-safe-mixer + repomix-unmixer: sır temizlenmiş paketleme ve paketten dosya geri çıkarma.
- deep-research + fact-checker: kanıt izli rapor, ardından iddia doğrulama.
- prompt-optimizer (EARS) + promptfoo-evaluation: belirsiz istemi spesifikasyona çevirip Promptfoo ile ölçmek.

## Tuzaklar
- slides-creator kullanımdan kaldırıldı (deck-creator'a taşındı), çağrılmamalı.
- Çin platformlarına bağlı üyeler (bilibili, douban, feishu, wecom, kimi, ima, tibo-reset-codex) açıklamaları kısmen Çince ve hesap/oturum ister.
- windows-remote-desktop-connection-doctor macOS istemcisi içindir; daymade-macos Apple platformuna özel.
- daymade-financial Bigdata.com gibi veri sağlayıcılarına dayanır; erişim koşulu katalog metninde belirtilmemiş.

## Üyeler
- plugin (60): auto-repo-setup, bilibili-source, cli-demo-generator, cloudflare-troubleshooting, competitors-analysis, data-visualization-discipline, daymade-audio, daymade-claude-code, daymade-codex, daymade-docs, daymade-financial, daymade-macos, daymade-skill, debugging-network-issues, deep-research, douban-skill, download-gemini-images, excalidraw-use, fact-checker, feishu-doc-scraper, frontend-visual-qa, gemini-history-analyzer, ghostty-use, git-safety-net, github-contributor, github-ops, github-review-pr, github-sensitive-data-cleanup, i18n-expert, ima-copilot, kimi-use, llm-eval-harness, llm-icon-finder, llm-wiki-setup, marketplace-health-check, meme-creator, notify-wecom, openclaw, openclaw-model-switch, peer-message …
