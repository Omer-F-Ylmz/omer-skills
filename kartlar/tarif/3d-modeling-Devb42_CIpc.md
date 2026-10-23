# 3d-modeling (Devb42_CIpc)

**Amaç:** Kullanıcıların sözlü talimatlarla 3D modeller oluşturmasını ve düzenlemesini kolaylaştırmak.
**Araçlar:** CadQuery (Python tabanlı parametrik modelleme), Kullanıcı seçebileceği agentler (ClaudeCode, OpenCode, CodexCLI, Gemini CLI vb.), SOMA CLI aracı (soma build, soma analyze, soma render)

**Adımlar**
1. [] Kullanıcı, fiziksel parça hakkında basit sözlü açıklama yapar.
2. [] AI agent, kullanıcının talimatına göre CadQuery Python kodunu oluşturur ve 3D modeli gösterir.
3. [] Kullanıcı, modeli inceleyerek eksik veya yanlış olan yerleri ekranda işaretler.
4. [] AI, kullanıcının işaretlediği yerleri tespit ederek kodunu ve modeli günceller.
5. [] Kullanıcı, modelin dayanıklılığı ve 3D yazıcı uyumluluğunu kontrol ettikten sonra modeli dışa aktarır.

**Prompt/kod/ayar:** CadQuery Python kodunu kullanarak 3D model oluşturma ve düzenleme.
**Sonuç:** Kullanıcıların CAD becerileri olmadan 3D modeller oluşturmasına ve düzenlemesine olanak sağlayan bir araç.
**Bizde (öneri, modelden):** Kurulu araçlarla kullanıcıların sözlü talimatlarla 3D modeller oluşturmasını sağlayabiliriz. Örneğin, AI agentlerimizi CadQuery ile entegre ederek benzer bir deneyim sunabiliriz.
**Daha iyi (öneri):** Kullanıcıların daha hızlı ve doğrudan geri bildirim almasını sağlayacak ekran işaretleme özelliğini geliştirmek.
