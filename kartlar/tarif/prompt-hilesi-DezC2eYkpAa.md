# prompt-hilesi (DezC2eYkpAa)

**Amaç:** Kandilleri tokenize ederek gelecek kandi tahmini yapmak.
**Araçlar:** Kronos (K-line Tokenization, Tokenizer Encoder, Tokenizer Decoder), Claude Opus 5.5 (TradingView entegrasyonu için), TradingView (ticaret platformu), GitHub (Kronos modeli ve kodu için)

**Adımlar**
1. [0:00-0:27] Kronos modelini tokenize ederek kandi verilerini işler. Her kandi, tokenlara ayrılır ve gelecek kandi tahmini yapılır.
2. [0001-0005] Modelin 12 milyar adet kandi üzerinde eğitildiğini ve 45 farklı borsa verisini kullandığını belirtir.
3. [0006-0008] Claude Opus 5.5 ile TradingView entegrasyonu yapılarak, Kronos'un tahminlerini otomatik olarak kullanıcıya sunan bir sistem oluşturulur.
4. [0008-0010] Gelecek 24 saatlik volatilite tahmini ve tahmin belirsizliği sesli olarak gösterilir.

**Prompt/kod/ayar:** Kronos modeli, candlestick verilerini tokenize ederek gelecek kandi tahmini yapar. Claude Opus 5.5 ile TradingView entegrasyonu yapılarak otomatik ticaret sistemine entegre edilir.
**Sonuç:** Kronos, tokenize edilmiş kandi verilerini kullanarak gelecek kandi tahmini yapar ve bu tahminler TradingView üzerinden kullanıcıya sunulur.
**Bizde (öneri, modelden):** Kronos modelini kurulu araçlarımızla nasıl tokenize ederek gelecek kandi tahmini yapacağımızı test edebiliriz. Ayrıca, Claude Opus 5.5 gibi entegrasyon araçları ile TradingView'a nasıl bağlayacağımızı araştırabiliriz.
**Daha iyi (öneri):** Modelin eğitim verilerini artırmak, daha fazla borsa verisini eklemek ve tahmin doğruluğunu artırmak için daha fazla tokenize etme yöntemi deneyebiliriz.
