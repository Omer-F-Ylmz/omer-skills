# vphone-cli-kurulum (DdXZOxTihxj)

**Amaç:** Apple Silicon Mac'te sanal iPhone oluşturma ve test etme.
**Araçlar:** Apple Silicon Mac, macOS 15+ (Sequoia), Xcode + iOS SDK, SIP/AMFI relaxation (private entitlements), brew, python@3.13, aria2, wget, gnu-tar, openssl@3, ldid-procursus, vphone-cli GitHub repo

**Adımlar**
1. [] GitHub repo'sunu klonlama ve alt-modülleri çekme.
2. [] Bağımlılıkları kurma.
3. [] Araçları kurma ve yapılandırma script'lerini çalıştırma.
4. [] Sanal iPhone VM oluşturma.
5. [] Sanal cihazı başlatma ve kullanmaya başlama.

**Prompt/kod/ayar:** vphone-cli vm create myphone -Vjb
**Sonuç:** Sanal iPhone oluşturulur ve test edilebilir.
**Bizde (öneri, modelden):** Apple Silicon Mac'te kurulu araçlarla nasıl yapılır: Xcode + iOS SDK + SIP/AMFI ayarlarıyla entitlements izinleri sağlanarak.
**Daha iyi (öneri):** SIP/AMFI ayarları otomatikleştirilebilir veya daha kullanıcı dostu bir GUI arayüzü eklenebilir.
