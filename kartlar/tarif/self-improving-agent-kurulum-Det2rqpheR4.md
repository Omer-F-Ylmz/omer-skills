# self-improving-agent-kurulum (Det2rqpheR4)

**Amaç:** Bir agentin deneyimlerini kaydetme ve tekrar kullanarak kendini iyileştirmesini sağlamak.
**Araçlar:** dosya kaydetme/okuma aracı (second tool), veri platformu (prices and filings), 7 şirket verisi (7 past years)

**Adımlar**
1. [0:00-0:17] Agentin şirketleri sıralama kriterleri (rank on) ve kaç şirketi seçeceği (keep X) konusunda 24 farklı kombinasyon oluşturma.
2. [0:17-0:25] Agentin her çalışmada 4 denemeyi 7 geçmiş yıl verisiyle karşılaştırma ve başarılı olanları kaydetme.
3. [0:25-0:31] Agentin her çalışma sonucunu bir dosyaya kaydetme ve sonraki çalışmalarda bu kaydı okuyarak tekrar denemeyi önleme.

**Prompt/kod/ayar:** rank_on: [PRICE_TO_BOOK, PRICE_TO_EARNINGS, NET_CASH_TO_VALUE, REVENUE_BROWTH, SHALLEST_FIRST], keep: [10, 20, 30, 40]
**Sonuç:** Agentin 24 denemeden 4'ünü her çalışmada test etmesi ve başarılı olanları kaydetmesiyle kendini iyileştirmesi sağlanmıştır.
**Bizde (öneri, modelden):** Kurulu araçlarla deneyimleri bir veritabanına kaydederek agentin tekrar denemeyi önlemesini sağlayabiliriz.
**Daha iyi (öneri):** Deneyimleri bir API üzerinden paylaşarak daha geniş ölçekte iyileşme sağlanabilir.
