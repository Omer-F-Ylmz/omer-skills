# prompt-hilesi (Det4Eo5RgSk)

**Amaç:** Claude Code kullanıcılarına ücretsiz AI modellerinin token kotalarını birleştirerek sınırsız kullanım imkanı sağlamak.
**Araçlar:** FreeLLMAPI (MIT lisansı, open-source), 34 AI sağlayıcı (Google, Groq, Cerebras, Mistral, vb.), Claude Code, npx (Node.js paket yöneticisi)

**Adımlar**
1. [0:00-0:15] FreeLLMAPI kurulumunu gerçekleştirmek için bir komut çalıştırın: `$curl -fsSL freellmapi.co/install.sh | bash`. API anahtarları şifrelenmiş olarak saklanır.
2. [0:15-0:25] 34 AI sağlayıcısının ücretsiz token kotalarını birleştirerek 7.4 milyar token ayıklama.
3. [0:25-0:35] Claude Code ile bağlantıyı kurmak için `npx freellmapi setup-claude` komutunu çalıştırın ve fallback modelleri seçin (635 seçenek).
4. [0:35-0:45] Model limitine ulaşıldığında otomatik olarak diğer modeller arasında geçiş yaparak kontekst aktarımı sağlanır.

**Prompt/kod/ayar:** $curl -fsSL freellmapi.co/install.sh | bash
npx freellmapi setup-claude
**Sonuç:** 7.4 milyar token ayıklama ve sınırsız Claude Code kullanımı.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl yapılır? Öncelikle FreeLLMAPI'yi yerel makinada kurun, ardından Claude Code ile entegre edin ve fallback modelleri ayarlayın.
**Daha iyi (öneri):** Kullanıcıların kendi API anahtarlarını şifrelenmiş olarak saklaması ve 34 sağlayıcıdan token kotalarını birleştirerek daha verimli kullanım sağlanabilir.
