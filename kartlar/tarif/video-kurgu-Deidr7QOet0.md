# video-kurgu (Deidr7QOet0)

**Amaç:** Uzun-format videoları kısa-format klip olarak dönüştürme.
**Araçlar:** Claude transkripsiyon ve analizi, re-motion (animasyon), FFmpeg (klip ekstraksiyonu), animated captions, segment scoring (hook strength, coherence, emotion, value density, ultimate payoff), cursor tracking (kelime/sentence kesintisiz dönüşüm)

**Adımlar**
1. [Preflight] Girdi video doğrulanır, disk alanı kontrol edilir, GPU tespit edilir.
2. [Transcribe] GPU-accelerated transkripsiyon (faster-whisper) kelime düzeyli zaman damgalarıyla yapılır.
3. [Detect Content] İçerik otomatik sınıflandırılır: talking-head, screen recording veya podcast.
4. [Analyze] Tam transkript okunur ve 8-12 aday segment puanlanır.
5. [Present] Adaylar formatlı bir tabloyla gösterilir (puanlar, hooklar, rationale).
6. [Approve] Kullanıcı segmentleri seçer, zaman damgalarını ayarlar, altyazı stili ve platformu belirler.
7. [Snap Boundaries] Kesme noktaları kelime sınırlarına, cümle bitişlerine ve ses sessizliklerine uygun olarak hizalanır.
8. [Prepare] Klipler FFmpeg stream copy ile çıkarılır ve uzun-format dönüşümü tamamlanır.

**Prompt/kod/ayar:** Claude transkripsiyon, segment scoring, FFmpeg, re-motion, cursor tracking.
**Sonuç:** Kullanıcıya en iyi kısa-format klip seçeneklerini sunan interaktif bir video dönüştürme aracı.
**Bizde (öneri, modelden):** Kurulu araçlarla uzun-format videoları kısa-formata dönüştürmek için FFmpeg, transkripsiyon ve segment puanlama algoritmaları kullanarak benzer bir sistem kurabiliriz.
**Daha iyi (öneri):** Kullanıcı deneyimini iyileştirmek için daha fazla interaktif öneri ekleyebilir, animasyonları daha zengin hale getirebilir ve platforma özel optimizasyonlar yapabiliriz.
