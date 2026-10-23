# prompt-hilesi (DbQx7UrM7Ud)

**Amaç:** Claude Code limitlerini aşan token tüketimini azaltmak ve otomatik model switch yapmak.
**Araçlar:** OmniRoute (GitHub açık kaynak araç), 200+ ücretsiz yapay zeka sağlayıcı (Anthropic, Meta LLaMA, NVIDIA, etc.), Token sıkıştırma algoritması

**Adımlar**
1. [0:06-0:10] Claude Code'u 200+ ücretsiz modelden birine otomatik bağlayarak token tasarrufu sağla.
2. [0:10-0:15] Limit dolduğunda otomatik olarak yeni modele geçiş yap.
3. [0:18-0:23] Prompt metinlerini token kullanımını %90 azaltacak şekilde ön işle.

**Prompt/kod/ayar:** OmniRoute GitHub'da 'OmniRoute' adıyla açık kaynaklı, Claude Code API ile entegrasyonu sağlar.
**Sonuç:** Limitler aşılmadan %90 token tasarrufu ve otomatik model switch.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl yapılır? OmniRoute gibi bir araç kurulumu ve yapay zeka sağlayıcı entegrasyonu gerektirir.
**Daha iyi (öneri):** Token sıkıştırma algoritmasını optimize ederek daha fazla tasarruf sağlayabilirsiniz.
