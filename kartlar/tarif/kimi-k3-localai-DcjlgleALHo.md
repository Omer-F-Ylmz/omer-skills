# kimi-k3-localai (DcjlgleALHo)

**Amaç:** 2.78 trillion parameter modelin tek bir CPU'da 8 GB RAM ile çalıştırılmasını kanıtlamak.
**Araçlar:** C99 (176 KB engine), SSD (1.56 TB), Linux OS, Expert-routing (93% model weights on disk), Checkpoint compression (5.5 TB → 8.24 GB)

**Adımlar**
1. [0:00-0:07] Modelin tek bir CPU'da çalıştırılmasını gösterdi. 8.24 GB RAM kullanımı ile 2.78 trillion parametre modelin çalıştırılmasını kanıtladı.
2. [0:09-0:14] Tüm motorun 176 KB C99 koduyla yazıldığını ve GPU/frameworksiz çalıştığını açıkladı.
3. [0:14-0:22] Modelin %93'ünün SSD'de saklanarak RAM'e yüklenmediğini ve token routing ile gerektiğinde okunduğunu açıkladı.
4. [0:22-0:26] 5.5 TB modelin 8.24 GB RAM'e indirildiğini ve aynı çıktı kalitesini koruduğunu gösterdi.
5. [0:28-0:33] 33 saniye/token performansını açıkladı ve 33 token/saniye ile karıştırılmaması gerektiğini vurguladı.
6. [0:36-0:40] 1.56 TB SSD ve Linux sistem gerekliliğini belirtti.
7. [0:44-0:48] Disk alanının yetersizliği nedeniyle hiçbir token üretilmediğini belirtti.
8. [0:48-0:51] Disk alanının yetersizliği nedeniyle proje başarısız olduğunu açıkladı.
9. [0:51-0:53] RAM kullanımının model boyutundan ziyade hangi verilerin RAM'de tutulduğuna bağlı olduğunu vurguladı.

**Prompt/kod/ayar:** Kimi K3 modelin çalıştırılmasında kullanılan prompt: 'The capital of France is' (8 token test).
**Sonuç:** 2.78 trillion parametre modelin tek bir CPU'da 8.24 GB RAM ile çalıştırılmasının kanıtı sağlandı. Ancak disk alanının yetersizliği nedeniyle token üretimi başarısız oldu.
**Bizde (öneri, modelden):** Kurulu araçlarla Kimi K3 modelini benzer performansla çalıştırmak için SSD ve RAM optimizasyonu gereklidir. Expert-routing ve checkpoint compression teknikleri kullanılarak modelin RAM'e yüklenme miktarı azaltılabilir.
**Daha iyi (öneri):** Modelin daha hızlı çalışması için RAM miktarı artırılabilir (örn. 128 GB+), ancak aynı çıktı kalitesini korumak için disk alanının yeterli olması gerekmektedir.
