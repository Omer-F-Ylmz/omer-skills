# plugin-kurulumu (DYwe8NLjYWo)

**Amaç:** Claude'u 6 kişilik geliştirici ekibine dönüştürmek için gereken 23 yetenekli plugin'i kurmak.
**Araçlar:** Optionol CLI, Anthropic Security Guidance, gstack, Superpowers, Frontend Tasarım Ajanı, Kod İnceleme Ajanları, Hafıza Modülü

**Adımlar**
1. [0001-0002] CLI araçlarını kurmak için gerekli komutları çalıştırma (rpm install, emplotes, .Search).
2. [0003-0004] Superpowers ajanı için GitHub'daki repo'yu inceleme ve kurulumu başlatma.
3. [0005-0006] Frontend tasarım ajanı için gerekli ayarları yapma.
4. [0007-0008] Kod inceleme ajanı için 5 agentın çalışmasını sağlama.
5. [0010-0012] Güvenlik taraması için Anthropic Security Guidance v2.1.0 kurulumunu tamamlama.
6. [0017-0019] Hafıza modülünü kurma ve oturumlar arası hafıza özelliğini etkinleştirme.
7. [0019] Plugin kurulumunu tamamlayarak 23 yetenek ve 24 komut ile Claude'u 6 kişilik ekibe dönüştürme.

**Prompt/kod/ayar:** $claude/install anthropics/security-guidance v2.1.0, claude /install thedotm/gstack, claude /install obra/superpowers
**Sonuç:** 23 yetenekli plugin kurulumu tamamlandı ve Claude 6 kişilik geliştirici ekibine dönüştü.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl bu plugin'i kurabiliriz? Önce CLI araçlarını kurup, ardından Anthropic ve GitHub'daki repo'ları kullanarak ajanı entegre edebiliriz.
**Daha iyi (öneri):** Kurulum sürecini daha otomatikleştirmek için bir script yazmak veya Docker konteynerleri kullanarak entegrasyonu kolaylaştırmak.
