# site-cloner (DbevmteOKw9)

**Amaç:** AI coding agents ile web sitesini Next.js temeline dönüştürme.
**Araçlar:** GitHub repo klonu, AI coding agents (Claude Code), Next.js framework, Multi-phase pipeline (reconnaissance, foundation, component specs, parallel build, assembly & QA)

**Adımlar**
1. [0:03-0:38] Reconnaissance: Hedef sitenin ekran görüntüleri çekme, tasarım token çıkarma, etkileşim tarama (scroll, click, hover, responsive).
2. [0:38-0:43] Foundation: Fontlar, renkler, global ayarlar güncelleme, tüm varlıklar indirme.
3. [0:43-0:50] Component Specs: Ayrıntılı spesifikasyon dosyaları yazma (docs/research/components/), CSS değerleri, durumlar, davranışlar ve içerik.
4. [0:50-1:00] Parallel Build: AI agentleri git worktree'larında görevlendirme, her bir bölüm/komponent için ayrı çalışma.
5. [1:00+] Assembly & QA: Çalışma ağaçlarını birleştirme, sayfayı kurma, orijinal siteden görselli karşılaştırma.

**Prompt/kod/ayar:** /skills/clone-website
**Sonuç:** Orijinal sitenin Next.js kod temeline dönüştürülmüş hali.
**Bizde (öneri, modelden):** Kurulu AI agentlerimizle Next.js temeline dönüştürme için benzer bir pipeline kurabiliriz.
**Daha iyi (öneri):** AI agentlerinin daha hızlı ve doğru çalışması için token çıkarma ve spesifikasyon dosyaları için daha gelişmiş bir OCR/parsing yöntemi kullanmak.
