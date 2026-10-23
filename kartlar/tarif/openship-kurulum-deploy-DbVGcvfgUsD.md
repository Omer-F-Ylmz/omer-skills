# openship-kurulum-deploy (DbVGcvfgUsD)

**Amaç:** Kendi sunucunuza kodunuzu tek komutla dağıtmak ve CI/CD, SSL, mail ve yedekleme gibi entegrasyonları otomatik olarak yönetmek.
**Araçlar:** npm, curl, Docker, Docker Compose, Let's Encrypt (SSL), Mail Server, CI/CD Pipeline

**Adımlar**
1. [] OpenShip'i kurmak için `npm install -g openship` veya `curl -fsSL https://get.openship.io | sh` komutlarını çalıştırın.
2. [] Proje dizinine gidin ve `openship init` komutunu çalıştırarak projenizi OpenShip'e bağlayın.
3. [] Projenizi canlıya taşımak için `openship deploy` komutunu çalıştırın.
4. [] Docker kullanmayı tercih ederseniz, OpenShip repo'sunu klonlayın ve `docker compose up -d` komutunu çalıştırın.
5. [] Arka planda OpenShip'i çalıştırmak için `openship open` komutunu kullanın ve dashboard'ı açın.
6. [] OpenShip'i durdurmak için `openship stop` komutunu kullanın.

**Prompt/kod/ayar:** npm install -g openship || curl -fsSL https://get.openship.io | sh
**Sonuç:** Kendi sunucunuza kodunuzu tek komutla dağıtma, CI/CD, SSL, mail ve yedekleme entegrasyonları otomatik olarak yönetme.
**Bizde (öneri, modelden):** Kurulu Docker ve Docker Compose ile benzer bir otomasyonu nasıl kurabiliriz?
**Daha iyi (öneri):** Docker Compose dosyalarını daha detaylı yapılandırarak, farklı ortamlarda daha esnek bir yapı sunmak.
