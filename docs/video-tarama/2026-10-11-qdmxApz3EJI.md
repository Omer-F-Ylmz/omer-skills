# On Engineering AI Systems that Endure The Bitter Lesson - Omar Khattab, DSPy & Databricks
## Künye
On Engineering AI Systems that Endure The Bitter Lesson - Omar Khattab, DSPy & Databricks · AI Engineer · süre: 19:12 · en-orig · https://youtu.be/qdmxApz3EJI · şema 2
motor: parti 2026-10-11-short-3 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 51507 tk · claude-haiku-5-5: claude-haiku-5-5 · 77848 tk
## Özet
Omar Khattab (Databricks, DSPy yaratıcısı), AI Engineer World's Fair konuşmasında Rich Sutton'ın Bitter Lesson makalesini yapay zekâ yazılım mühendisliğine uyarlıyor. Erken optimizasyon, gereğinden alçak soyutlama düzeyinde elle mühendislik demektir. Prompt programlama için kötü bir soyutlamadır, çünkü görev tanımını modele özgü ayarlar, çıkarım stratejisi ve biçimlendirme kararlarıyla iç içe geçirir. Çözüm olarak ayrıştırma (separation of concerns) öneriyor. Sistem spesifikasyonuna, eval'lere ve kontrol akışı/araçlara yatırım yapılmalı; modeller, modüller ve optimizer'lar değiştirilebilir bırakılmalı. Konuşma DSPy ve Signatures kavramıyla bitiyor.
## Bölümler
- 0:00 AI Engineer World's Fair
- 0:22 Bitter Lesson'a Dayanan Yapay Zekâ Sistemleri Mühendisliği
- 0:32 Yapay Zekâ Yazılım Mühendisliğinin Zorlukları
- 0:40 The Bitter Lesson
- 4:50 Yapay Zekâ Mühendisliğinin Amacı
- 6:39 Çıkarım 1: Ölçeklenebilirlik İçin Mühendislik
- 7:19 Erken Optimizasyon
- 12:18 Prompt'ların Sorunu
- 14:26 Eski Dost: Sorumlulukların Ayrılması
- 17:11 Çıkarım 2: Ayrıştırmaya Yatırım Yap
- 17:21 LLM Yazılımı Piramidi ve DSPy
- 17:45 DSPy Kavramı: Bildirimsel Signature'lar
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| DSPy | yok | teknik | yok | Bildirimsel, kendini geliştiren Python çerçevesi. Sistem spesifikasyonunu Signature'larla tanımlar, modeller, modüller ve optimizer'lar değiştirilebilir kalır. | 17:21 | Slaytta DSPy logosu ve açılımı 'Declarative Self-improving Python' görünüyor. (karede: Slayt: DSPy logosu, 'Declarative Self-improving Python' ve piramit.) |
| Signatures | yok | teknik | yok | DSPy'nin tek temel kavramı. Girdi/çıktı yapısını ve görev tanımını bildirimsel olarak yazar. | 17:52 | Kodda ExtractInfo(dspy.Signature) sınıfı InputField ve OutputField alanlarıyla görünüyor. (karede: class ExtractInfo(dspy.Signature) kodu, InputField ve OutputField satırları.) |
| ColBERT | yok | teknik | yok | Konuşmacının yazdığı, uzun ömürlü kalan sinirsel bilgi erişim modeli. | 9:16 | Slaytta 'designing ColBERT ('19) and DSPy ('22)' yazıyor. (karede: Slayt: 'approach I took in designing ColBERT ('19) and DSPy ('22)'.) |
| The Bitter Lesson | yok | teknik | yok | Rich Sutton'ın, ölçeklenen genel yöntemlerin (arama ve öğrenme) kazandığını savunan 2019 denemesi. | 3:56 | Slaytta 'The Bitter Lesson, Rich Sutton, March 13, 2019' görünüyor. (karede: Slayt: 'The Bitter Lesson, Rich Sutton, March 13, 2019' ve Sutton fotoğrafı.) |
| Premature optimization | yok | teknik | yok | Knuth'un 'erken optimizasyon tüm kötülüklerin kökü' ilkesi. Konuşmacı bunu yapay zekâ yazılımına uyarlıyor. | 7:36 | Slaytta Knuth'un makalesi ve alıntısı görünüyor. (karede: Slayt: 'Structured Programming with go to Statements, DONALD E. KNUTH' ve alıntı.) |
| Separation of concerns | yok | teknik | yok | Görev tanımını model, çıkarım stratejisi ve öğrenme algoritmasından ayıran tasarım ilkesi. | 14:26 | Slaytta 'Trusty old Separation of Concerns...' yazıyor. (karede: Slayt: 'Trusty old Separation of Concerns...'.) |
| Evals | yok | teknik | yok | Modelden bağımsız olarak asıl önemsenen davranışı tanımlayan değerlendirme verisi. | 15:08 | Konuşmacı model değişse de eval'lerin önemsenen şey olarak kaldığını söylüyor. |
| Pyramid of LLM Software | yok | teknik | yok | Alttan üste spec, mimari/eval, öğrenme/çıkarım, adaptörler ve LLM katmanlarından oluşan model. | 17:21 | Piramit slaytında bu katmanlar listeleniyor. (karede: Piramit: System Spec, Architecture & Evals, Learning & Inference, Adapters, LLM.) |
| Adapters | yok | teknik | yok | LLM'leri yapılandırılmış girdi/çıktıya çeviren katman. Biçimlendirme, ayrıştırma ve yeniden denemeyi yönetir. | 17:21 | Piramit katmanında 'Format, Parse, Retries / Adapters' yazıyor. (karede: Piramit katmanı: 'Format, Parse, Retries' ve 'Adapters'.) |
| Prompt optimization | yok | teknik | yok | Prompt'u uygulamaya göre otomatik iyileştiren optimizer yöntemleri. | 16:27 | Konuşmacı RL ve prompt optimization'ı aynı soyutlama düzeyinde yapmaktan söz ediyor. |
| Reinforcement learning | yok | teknik | yok | Pekiştirmeli öğrenme. Optimizer olarak değiştirilebilir bir öğrenme algoritması olarak anılıyor. | 16:44 | Slaytta 'RL methods, prompt optimizers' listeleniyor. (karede: Slayt satırı: 'learning algorithms: RL methods, prompt optimizers'.) |
| Chain of thought | yok | teknik | yok | Çıkarım zamanı stratejisi. Agent'a geçişte prompt'un değişmesi gerektiği örneğinde anılıyor. | 13:26 | Slaytta 'adjusting from CoT reasoning to a tool-use Agent' yazıyor. (karede: Slayt: 'adjusting from CoT reasoning to a tool-use Agent'.) |
| Monte Carlo research | yok | teknik | yok | Konuşmacının değiştirilebilir çıkarım stratejisi örneği olarak saydığı arama yaklaşımı. | 16:27 | Konuşmacı zincirden agent'a, agent'tan Monte Carlo research'e geçişten söz ediyor. |
| BERT | yok | teknik | yok | Konuşmada, ColBERT ve DSPy'ın temel tasarımının korunduğu başlangıç modeli olarak anılıyor. | 9:32 | Slaytta 'Both have maintained their fundamental design since BERT' (karede: kanıttan) Slaytta 'Both have maintained their fundamental design since BERT' |
| text-davinci-002 | yok | teknik | yok | OpenAI dil modeli; konuşmada tasarımın korunduğu zaman aralığının başlangıcı olarak anılıyor. | 9:20 | from the days of birth text Davinci 2 up to four 04 mini · kanıt: yok |
| o4-mini | yok | teknik | yok | OpenAI modeli; konuşmada tasarımın korunduğu zaman aralığının sonu olarak anılıyor. | 9:20 | up to four 04 mini and they're bigger now than they ever were |
| Python | yok | teknik | yok | Gösterilen DSPy Signature kodunun programlama dili. | 17:52 | Kodda 'class ExtractInfo(dspy.Signature):' ve dspy.InputField/OutputField satırları görünüyor. (karede: kanıttan) Kodda 'class ExtractInfo(dspy.Signature):' ve dspy.InputField/OutputField satırları görünüyor. |
| Kötü prompt örneği (konuşmacının eleştirdiği) | yok | prompt | yok | Konuşmacı 'XML üret', 'JSON ile cevap ver', 'sen Profesör Einstein'sın', 'bahşiş vereceğim' gibi talimatları mühendislik değil, modele özgü ayar sayıyor. | 14:20 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.ai.engineer/newsletter — AI Engineer bülten abonelik sayfası · aday: hayır · Etkinliğin bülten sayfası. Videoda kullanılan bir araç ya da servis değil. · sınıf: diğer
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Prompt programlama için kötü bir soyutlamadır, ama yönetim için iyidir. | 12:18 | öneri |
| Erken optimizasyon, ancak gereğinden alçak bir soyutlama düzeyinde elle mühendislik yapıldığında olur. | 9:58 | karşılaştırma |
| ColBERT ve DSPy, BERT ve text-davinci-002'den o4-mini'ye temel tasarımlarını korudu. | 9:32 | özellik |
| Spec, kontrol akışı/araçlar ve eval'lere yatırım yap. Modeller, modüller ve optimizer'lar değiştirilebilir olsun. | 18:42 | öneri |
| Sutton'ın 'search' kavramı LLM dünyasında çıkarım zamanı ölçeklemeye karşılık gelir. | 4:40 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:22 | Databricks | aday değil: konu dışı | Konuşmacının kurumu, slaytta logo. |
| kare 0:06 | Microsoft | aday değil: sponsor/reklam | Presenting sponsor logosu. |
| kare 0:10 | AWS | aday değil: sponsor/reklam | Innovation partner logosu. |
| kare 0:10 | Graphite | aday değil: sponsor/reklam | Platinum sponsor logosu. |
| kare 0:10 | Windsurf | aday değil: sponsor/reklam | Platinum sponsor logosu. |
| kare 0:10 | MongoDB | aday değil: sponsor/reklam | Platinum sponsor logosu. |
| kare 0:10 | daily | aday değil: sponsor/reklam | Platinum sponsor logosu. |
| kare 0:10 | augment code | aday değil: sponsor/reklam | Platinum sponsor logosu. |
| kare 0:10 | WorkOS | aday değil: sponsor/reklam | Platinum sponsor logosu. |
| konuşma 3:42 | Rich Sutton / The Bitter Lesson | The Bitter Lesson | Makale ve yazarı anlatılıyor. |
| konuşma 4:44 | Çıkarım zamanı ölçekleme (inference-time scaling) | aday değil: genel kavram | Sutton'ın 'search' kavramının karşılığı olarak açıklanıyor. |
| kare 7:30 | Donald Knuth, Structured Programming | Premature optimization | Alıntının kaynağı olarak gösteriliyor. |
| kare 8:22 | Q_rsqrt kare kök kodu | Premature optimization | Erken optimizasyon örneği olarak gösteriliyor. |
| kare 8:08 | Archie Sengupta X gönderisi | aday değil: konu dışı | Kod ekran görüntüsünün kaynağı. |
| kare 9:16 | ColBERT | ColBERT | Slaytta anılıyor. |
| kare 9:16 | DSPy | DSPy | Slaytta anılıyor. |
| kare 9:32 | BERT | aday değil: başka adayın parçası (ColBERT) | Slaytta 'since BERT' olarak geçiyor. |
| kare 9:32 | text-davinci-002 | aday değil: genel kavram | Model örneği olarak geçiyor, kullanılmıyor. |
| kare 9:32 | o4-mini | aday değil: genel kavram | Model örneği olarak geçiyor, kullanılmıyor. |
| kare 11:02 | Omar Khattab tweeti | The Bitter Lesson | Mayıs 2024 tweeti, soyutlama savını anlatıyor. |
| kare 11:38 | 2006 çok dilli soru yanıtlama makalesi | aday değil: konu dışı | Modüler mimari örneği olarak gösteriliyor. |
| kare 12:28 | Prompt | aday değil: genel kavram | Kötü soyutlama olarak eleştiriliyor. |
| kare 13:26 | CoT reasoning ve tool-use Agent | Chain of thought | Çıkarım stratejisi örneği. |
| konuşma 13:18 | XML / JSON biçimlendirme | aday değil: genel kavram | Prompt'a gömülen biçim talimatı örneği. |
| konuşma 14:26 | Evals | Evals | Spec'in parçası olarak anlatılıyor. |
| kare 14:26 | Separation of Concerns | Separation of concerns | Slayt başlığı. |
| kare 14:26 | Pyramid of LLM Software | Pyramid of LLM Software | Piramit slaytı. |
| kare 16:44 | RL methods, prompt optimizers | Reinforcement learning | Değiştirilebilir öğrenme algoritmaları listesinde. |
| konuşma 16:27 | Monte Carlo research | Monte Carlo research | Değiştirilebilir strateji örneği. |
| konuşma 16:27 | Prompt optimization | Prompt optimization | Optimizer örneği olarak sayılıyor. |
| kare 17:22 | Adapters | Adapters | Piramitte 'Format, Parse, Retries / Adapters' katmanı. |
| kare 17:52 | dspy.Signature kodu | Signatures | ExtractInfo sınıfı. |
| konuşma 17:45 | dspy.ai | DSPy | Konuşmacı DSPy sitesi olarak söylüyor. |
| açıklama | https://www.ai.engineer/newsletter | aday değil: konu dışı | Etkinlik bülteni bağlantısı. |
| yorum | Karpathy'nin 'LLM'ler CPU gibi' fikri | aday değil: konu dışı | Yorumda geçiyor, videoda anlatılmıyor. |
| yorum | Demis Hassabis ve DeepMind | aday değil: konu dışı | Yorumda geçiyor, videoda anlatılmıyor. |
| açıklama | ColBERT erişim modeli | ColBERT | Açıklamada konuşmacının eseri olarak anılıyor. |
## Kareden okunanlar
- 0:00: AI Engineer açılış logosu
- 0:06: Microsoft, PRESENTING SPONSOR
- 0:10: AWS innovation partner; Graphite, Windsurf, MongoDB, daily, augment code, WorkOS platinum sponsorlar
- 0:22: Başlık: On Engineering AI Systems that Endure the Bitter Lesson, Omar Khattab, databricks, DSPy
- 2:28: Every day, a new learning algorithm or inference strategy promises to finally unlock great reliability.
- 4:40: Seventy years of AI... search and learning, work best! Sutton disclaimer
- 7:30: Knuth: Structured Programming with go to Statements; 'Premature optimization is the root of all evil.'
- 8:22: Q_rsqrt C kodu, 0x5f3759df, 'Not the most future-proof program possible!'
- 11:02: Omar Khattab tweeti, 11 Mayıs 2024: Bitter Lesson ve modüler uzmanlaşmalar
- 11:38: 2006 makalesi sistem mimarisi: Execution Manager, Question Analyzer, Retrieval Strategist
- 14:26: The Pyramid of LLM Software
- 17:52: ExtractInfo(dspy.Signature) kodu
- 18:42: Invest in Signatures, Essential Control Flow & Tools, Evals; swappable Models, Modules, Optimizers
## Belirsizlikler
- Sözlük eşleşmeleri (Three.js, Stripe, React, Notion vb.) bulanık ses eşleşmeleri. Videoda geçmiyorlar, aday yapılmadı.
- Piramit ilk slaytta 'Learning & Inference', 'Adapters' gibi katman adları var. DSPy'nin bunları nasıl uyguladığı konuşmada ayrıntılanmadı.
- Kurulum komutu gösterilmedi.
- Yorumdaki Karpathy ve Demis Hassabis sözleri videoda anlatılmıyor.
## Atlanan segment oranı
0/26 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| dspy.ai | 17:45 | ses | evet |
| https://www.ai.engineer/newsletter | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Bitter Lesson makalesi tanıtılıyor: genel yöntemler (arama ve öğrenme) kazanır. — araçlar: The Bitter Lesson
- 2. adım — Yapay zekâ mühendisliğinin amacı sorgulanıyor: güvenilir, kontrol edilebilir yazılım hedefleniyor. — araçlar: yok
- 3. adım — Çıkarım 1: ölçeklenen arama ve öğrenmenin ne için yapıldığı mühendislikle tanımlanır. — araçlar: Evals
- 4. adım — Erken optimizasyon ilkesi yapay zekâ yazılımına uyarlanıyor. — araçlar: Premature optimization
- 5. adım — ColBERT ve DSPy'nin uzun ömürlü kalma gerekçesi tartışılıyor. — araçlar: ColBERT, DSPy
- 6. adım — 2006 modüler soru yanıtlama mimarisi örnek gösteriliyor. — araçlar: yok
- 7. adım — Prompt'un programlama için kötü soyutlama olduğu gerekçeleriyle anlatılıyor. — araçlar: Chain of thought
- 8. adım — Sorumlulukların ayrılması önerilir: doğal dil tanımları, eval'ler ve kod. — araçlar: Separation of concerns, Evals
- 9. adım — Modeller, çıkarım stratejileri ve öğrenme algoritmaları değiştirilebilir bırakılır. — araçlar: Reinforcement learning, Prompt optimization, Monte Carlo research
- 10. adım — LLM Yazılımı Piramidi ve DSPy'nin katmanlara eşlemesi gösteriliyor. — araçlar: Pyramid of LLM Software, DSPy, Adapters
- 11. adım — Signature kodu örneği gösteriliyor. — araçlar: Signatures, DSPy
- 12. adım — Özet ve öneriler: Signatures, kontrol akışı/araçlar ve eval'lere yatırım yap. — araçlar: DSPy, Evals
## Promptlar
- Kötü prompt örneği (konuşmacının eleştirdiği) — Konuşmacı 'XML üret', 'JSON ile cevap ver', 'sen Profesör Einstein'sın', 'bahşiş vereceğim' gibi talimatları mühendislik değil, modele özgü ayar sayıyor.
ikinci göz KAPALI: --ikinci-goz yok
