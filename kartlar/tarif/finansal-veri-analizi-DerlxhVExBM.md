# finansal-veri-analizi (DerlxhVExBM)

**Amaç:** Finansal verileri (K-lines) anlama ve trend tahmini yapma.
**Araçlar:** Kronos Tokenizer (hierarchical discrete tokens), Autoregressive Transformer, K-line sequences (OHLCV data)

**Adımlar**
1. [] Finansal verileri (K-lines) tokenize etme: OHLCV verilerini katmanlı tokenlere dönüştürme.
2. [] Tokenize edilmiş veriler üzerinde ön eğitim yapma: Autoregressive Transformer kullanarak tokenleri işleme.
3. [] Finansal trendleri tahmin etme: Ön eğitimli modelin tahmin gücünü kullanarak finansal verileri anlamak.

**Prompt/kod/ayar:** Kronos tokenizer ve autoregressive Transformer modeli ayarları.
**Sonuç:** Finansal verilerin (K-lines) anlaşılması ve trend tahminleri için kullanışlı bir model.
**Bizde (öneri, modelden):** Kronos modelini kullanarak finansal verileri tokenize edip, ön eğitimli bir Transformer modeli ile trend tahminleri yapabiliriz.
**Daha iyi (öneri):** Modelin daha fazla finansal veriyle eğitilmesi ve tokenizasyon sürecinin iyileştirilmesi.
