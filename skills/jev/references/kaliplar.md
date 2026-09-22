# Jev kalıpları

**Fan-out** — https://docs.typesafe.ai/patterns/fan-out
Olası her aday eylem/özellik için dar soruları tek istekte birden sor; Jev hepsini aynı state üzerinde paralel değerlendirir, kazananı kod seçer. Seri "LLM karar ver → uygula" döngüsünün gecikmesini keser; 64k/32k bağlam bütçesine sığdır.

**Confidence routing** — https://docs.typesafe.ai/patterns/confidence-routing
Choice/score `confidence` değerini kapı yap: yüksekse kod otomatik ilerler, düşükse insan incelemesine ya da daha büyük modele düşer. Eşik sabitlerini tek dosyada tut, gözden geçirilebilir olsun.

**Composite scoring** — https://docs.typesafe.ai/patterns/composite-scoring
Aynı state hakkında birkaç bağımsız noul/score sorusu sor, cevapları kodda ağırlıklandırıp tek karara birleştir. Tek geniş soru yerine inceleyebileceğin ara yargılar üretir.

**Intent routing** — https://docs.typesafe.ai/patterns/intent-routing
Gelen girdiyi bir choice sorusuyla niyetlere sınıfla, her niyet için deterministik kod dalı çalıştır. Seçenek criteria'sında "neyi kapsar, neyi kapsamaz" yaz; aynı alan adlarını tüm seçeneklerde kullan.
