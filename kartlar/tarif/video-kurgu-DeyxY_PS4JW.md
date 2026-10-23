# video-kurgu (DeyxY_PS4JW)

**Amaç:** AI modelinin yerel çalıştırılma yöntemini anlatmak
**Araçlar:** GitHub repo, NVIDIA DGX Spark (121GB RAM), NVMe depolama, HuggingFace model formatı

**Adımlar**
1. [] SparkRun Recipes repo'sunu indir ve ana sayfasını incele.
2. [] 180B parametreli modelin yerel çalıştırılma yöntemini anlatır: lookup tablosunu NVMe'de depolarak RAM kullanımını azaltır.
3. [] GitHub repo'nun 'HARDRULE' bölümünü okur ve model yükleme kurallarını takip eder.
4. [] Modelin çalıştırılma performansını ölçer ve RAM kullanımını azaltan teknik detayları gösterir.

**Prompt/kod/ayar:** SparkRun Recipes repo'su ve NVIDIA DGX Spark kullanılarak yerel AI modeli çalıştırma.
**Sonuç:** 180B parametreli AI modelinin yerel çalıştırılma yöntemi ve RAM kullanımını azaltan teknik detaylar.
**Bizde (öneri, modelden):** Kurulu araçlarla yerel AI modelini çalıştırmak için SparkRun Recipes repo'sunu kullanarak, modelin NVMe'de depolanmasını sağlayarak RAM kullanımını optimize edebiliriz.
**Daha iyi (öneri):** Modelin performansını daha da artırmak için NVMe depolama kapasitesini artırabilir ve daha küçük boyutlu model formatlarını (örn. Q4_K_XL) kullanabiliriz.
