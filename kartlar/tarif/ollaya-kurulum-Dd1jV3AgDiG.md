# ollaya-kurulum (Dd1jV3AgDiG)

**Amaç:** Ollaya'yı lokal olarak çalıştırmak ve model yönetimi yapmak.
**Araçlar:** curl, bash, TypeSafe API, ONNX Runtime, GitHub, Hugging Face

**Adımlar**
1. [0001-0003] Ollaya'yı indirmek için komut satırından aşağıdaki komutu çalıştırın:
2. [0001-0003] Ollaya daemon'u başlatmak için aşağıdaki komutu çalıştırın:
3. [0001-0003] Modeli çekmek için model adını kullanarak aşağıdaki komutu çalıştırın:
4. [0001-0003] Modeli çalıştırmak için aşağıdaki komutu kullanın:
5. [0001-0003] Model listesini görmek için aşağıdaki komutu çalıştırın:
6. [0001-0003] Model performansını ve hızını test etmek için aşağıdaki komutu kullanın:
7. [0001-0003] Daemon'u durdurmak için aşağıdaki komutu çalıştırın:

**Prompt/kod/ayar:** curl -fsSL https://ollaya.dev/install.sh | sh && ollaya serve && ollaya pull winnow:e4b && ollaya run winnow:e4b
**Sonuç:** Ollaya, lokal olarak çalıştırılabilen, TypeSafe uyumlu API ile çalışan, ONNX formatında hafif model dosyaları kullanan bir araçtır.
**Bizde (öneri, modelden):** kurulu araçlarla nasıl ONNX formatında hafif model dosyaları kullanılarak lokal olarak çalıştırılabilir bir API oluşturulur?
**Daha iyi (öneri):** Model performansını ve hızını daha da iyileştirmek için C++ optimizasyonları ve hafıza yönetimi teknikleri kullanmak.
