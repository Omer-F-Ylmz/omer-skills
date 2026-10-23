# openwebui-kurulum (DefTRngy4bF)

**Amaç:** Self-hosted AI platform kurulumu ve takımlar için kolay erişim sağlama.
**Araçlar:** pip, Docker, Kubernetes, ollama, cuda, OpenAI-compatible API, GitHub

**Adımlar**
1. [] OpenWebUI'nin GitHub'dan indirilmesi ve kurulum komutu ile çalıştırılması.
2. [] Kurulum sonrası admin paneline erişim ve kullanıcı rollerinin ayarlanması.
3. [] Takım kanallarının oluşturulması ve ortak hafızanın etkinleştirilmesi.
4. [] Otomatik prompt ve agent çalışmaları için ayarların yapılandırılması.
5. [] Token kullanımının izlenmesi ve maliyet kontrolü için admin paneli kullanımı.

**Prompt/kod/ayar:** docker run -e SECRET_KEY=$(openssl rand -hex 32) openwebui/openwebui:latest
**Sonuç:** Self-hosted AI platform kurulumu tamamlandı ve takımlar için kullanıma hazır.
**Bizde (öneri, modelden):** Kurulu araçlarla Docker veya Kubernetes kullanarak OpenWebUI kurulumunu otomatikleştirmek için CI/CD pipeline'ları oluşturabilirsiniz.
**Daha iyi (öneri):** Kurulum sırasında kullanıcı rollerini ve izinleri daha detaylı ayarlayarak güvenliği artırabilirsiniz.
