# knowledge-graph-oluşturma (DYKXe-YjOrd)

**Amaç:** Claude Code için token kullanımını azaltmak ve projeyi daha hızlı anlama yeteneği kazandırmak.
**Araçlar:** pip install graphifyy && graphify install, Obsidian (ücretsiz), Graphify komutu

**Adımlar**
1. [] Graphify skill'i kurmak için pip install graphifyy && graphify install komutunu çalıştırın.
2. [] Graphify komutunu çalıştırarak tüm dosyaları tarıyor ve knowledge graph oluşturuyor.
3. [] Obsidian'i kullanarak çalışma alanınızı görselleştirin ve Graph view'a tıklayın.
4. [] CLAUDE.md dosyasına knowledge graph sorgulama kuralını ekleyerek token tasarrufu sağlayın.

**Prompt/kod/ayar:** ALWAYS query the knowledge graph first | Only read raw files if explicitly say so
**Sonuç:** 71.5 kat token tasarrufu
**Bizde (öneri, modelden):** kurulu araçlarla nasıl knowledge graph oluşturulur ve token kullanımını optimize edebiliriz?
**Daha iyi (öneri):** Graphify'nin daha hızlı ve daha verimli bir şekilde entegre edilmesi için CLI arayüzü geliştirilebilir.
