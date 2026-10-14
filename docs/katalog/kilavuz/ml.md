# ml — 23 benzersiz kayıt

**Amaç:** Makine öğrenmesi ve LLM mühendisliği ajanları: EDA, özellik mühendisliği, sızıntı/dengesizlik, deney izleme, zaman serisi, görüntü/NLP, LLM değerlendirme, sağlayıcı yönlendirme, yerel çıkarım.

**İç yapı:** Tümü [ajan], ml-<konu>; klasik ML (scikit-learn, pandas, numpy, ozellik), derin öğrenme (tensorflow, goruntu), LLM (langchain, openai-api, llm-*), MLOps (deney, kayma).

## En güçlü parçalar
- `ml-veri-sizintisi` — Tüm satırda fit, gelecek bilgisi, hedef vekili; fazla iyi skorlar şüphesinde.
- `ml-kesifsel-analiz` — Yeni veri setinde dağılım, eksiklik, aykırı değer ve sızıntı kontrolü.
- `ml-llm-degerlendirme` — Altın örnek, rubrik puanlayıcı ve regresyon kapılı LLM değerlendirme setleri.
- `ml-llm-saglayici-yonlendirme` — Fallback zinciri, timeout, yetenek eşleme, format adaptörüyle sağlayıcı yönlendirme.
- `ml-yerel-llm-cikarim` — Kuantizasyon, VRAM bütçesi, bağlam uzunluğu, batching ile yerel çıkarım.
- `ml-scikit-learn` — Sızıntısız pipeline, CV, tuning ve sınıf dengesi metrikleri.
- `ml-dengesiz-sinif` — Nadir sınıflarda (dolandırıcılık) metrik, yeniden örnekleme, sınıf ağırlığı, maliyet eşiği.
- `ml-zaman-serisi` — Backtest, mevsimsellik, tatil ve baseline ile talep/satış tahmini.
- `ml-tahmin-kaymasi-izleme` — Canlı modelde girdi/tahmin kayması ve etiketi gecikmeli bozulma alarmı.

## Birlikte kullanım
- ml-kesifsel-analiz → ml-ozellik-muhendisligi → ml-scikit-learn → ml-model-metrik.
- ml-veri-sizintisi + ml-hiperparametre-arama: iç içe değerlendirmede sızıntı denetimi.
- ml-deney-izleme + ml-tahmin-kaymasi-izleme: eğitimden canlıya izleme.
- ml-llm-saglayici-yonlendirme + ml-llm-degerlendirme: yönlendirme kararını eval ile ölçmek.

## Tuzaklar
- ml-openai-api OpenAI API anahtarı ister; maliyet kontrolü kapsamında.
- ml-yerel-llm-cikarim VRAM bütçesine bağlı; donanım sınırı belirleyici.
- ml-dengesiz-sinif ile ml-model-metrik eşik/metrik konusunda örtüşür.

## Üyeler
- ajan (23): ml-deney-izleme, ml-dengesiz-sinif, ml-goruntu-isleme, ml-hiperparametre-arama, ml-kesifsel-analiz, ml-langchain, ml-llm-degerlendirme, ml-llm-saglayici-yonlendirme, ml-makale-uygulama, ml-model-metrik, ml-nlp, ml-numpy, ml-openai-api, ml-ozellik-muhendisligi, ml-pandas, ml-pekistirmeli-ogrenme, ml-scikit-learn, ml-tahmin-kaymasi-izleme, ml-tensorflow, ml-veri-bilimci, ml-veri-sizintisi, ml-yerel-llm-cikarim, ml-zaman-serisi
