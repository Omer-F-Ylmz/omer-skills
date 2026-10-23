# web-kod (Deiow9ut9lO)

**Amaç:** AI kod ajanı için görsel geri bildirim aracı ile eleman tıklama ve not ekleme yoluyla kod değişikliği yapma.
**Araçlar:** Agentation (GitHub araç), MCP (Multi-Cloud Proxy) ayarı, AI kod ajanı (örn. Claude)

**Adımlar**
1. [] GitHub'taki Agentation repo'sunu indir ve kurulum komutunu çalıştır.
2. [] MCP ayarını yapılandır ve cloud'da tıklanmaları doğrudan okumaya izin ver.
3. [] Web sayfasındaki değiştirmek istediğiniz elemanı tıklayın ve istediğiniz değişikliği yazın (örn. 'Make this card bigger with rounded corners').
4. [] Agentation, tıklanılan elemanın kontekstini (seçici, kaynak lokasyonu, sınıflar) AI'ya aktarır.
5. [] AI, tıklanılan elemanın tam kontekstini kullanarak istenilen kod değişikliğini yapar.

**Prompt/kod/ayar:** Agentation'ın yapılandırılmasında kullanılan MCP ayarı ve AI ajanı ile entegrasyon.
**Sonuç:** AI kod ajanı, tıklanılan elemanın tam kontekstini kullanarak istenilen kod değişikliğini yapar ve ekran görüntüleri veya açıklamalar gerektirmez.
**Bizde (öneri, modelden):** kurulu araçlarla nasıl Agentation benzeri bir sistem oluşturulabilir: tıklama ve not ekleme işlevleri ile AI entegrasyonu.
**Daha iyi (öneri):** MCP ayarı ile cloud'da doğrudan tıklanmaları okuma yeteneği ekleyerek kullanıcı deneyimini daha da iyileştirmek.
