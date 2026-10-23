# superblocks-uygulama-gelistirme (Decg_eOD3UM)

**Amaç:** Kullanıcıların şirket verilerini bulutlarında tutarak güvenli bir şekilde AI ile uygulamalar geliştirmesini sağlamak.
**Araçlar:** Superblocks MCP (Claude entegrasyonu), Frontier modeller (zor mantık işlemleri için), Ucuz açık kaynaklı modeller (paralel geliştirme için), Güvenlik agentleri (oturum açma kaçırma, iş mantığı hataları, tedarik zinciri zayıflıkları kontrolü için), SSO, izin ve denetim kuralları (otomatik uygulama)

**Adımlar**
1. [0:00-0:12] Kullanıcı, istediği iş akışını veya uygulamayı tarif eder. Superblocks bu tariften hareketle AI ile uygulama geliştirir.
2. [0:12-0:19] Eğer kullanıcı Claude'da geliştirmiş bir uygulama varsa, Superblocks MCP aracılığıyla bu uygulama Superblocks'a entegre edilir.
3. [0:21-0:33] Superblocks, uygulamanın geliştirilmesi için uzmanlaşmış agent'ler kullanır. Öncelikle zor mantık işlemleri için önde gelen modeller kullanılır ve ardından ucuz açık kaynaklı modellerle paralel olarak geliştirme işlemi sürdürülür.
4. [0:36-0:46] Güvenlik agentleri, uygulamanın yayına çıkmadan önce oturum açma kaçırma, iş mantığı hataları ve tedarik zinciri zayıflıkları gibi riskler için kontrol edilir.
5. [0:48-0:57] Uygulama, şirket verilerinin bulutlarında kalmasını sağlayarak güvenli bir şekilde kullanıma sunulur. Bu sayede IT ve güvenlik kontrolü korunurken, kullanıcıların AI ile uygulamalar geliştirme özgürlüğü sağlanır.

**Prompt/kod/ayar:** Kullanıcı tarifini Superblocks'a göndererek AI ile uygulama geliştirme işlemini başlatır. Örnek: 'Bir CRM uygulaması oluştur, Snowflake'dan satış pipeline verilerini çek, Slack'a öneriler gönder.'
**Sonuç:** Güvenli, şirket bulutlarında çalışan AI ile geliştirilmiş uygulamalar.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl yapılır: Öncelikle kullanıcıya bir tarif alınır, ardından Superblocks'a gönderilir. Superblocks, bu tariften hareketle AI agent'leri kullanarak uygulama geliştirir ve güvenlik önlemleri uygulanır.
**Daha iyi (öneri):** Uygulamaların geliştirilmesi sırasında daha fazla uzmanlaşmış agent kullanılarak işlemlerin daha hızlı ve ekonomik bir şekilde tamamlanması sağlanabilir. Ayrıca, kullanıcıların daha detaylı tarifler yapabilmesi için interaktif bir arayüz sunulabilir.
