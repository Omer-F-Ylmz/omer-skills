# Ornith 1.5 Wrote Its Own Training Data  #aiagents #OpenWeights #Ornith
## Künye
Ornith 1.5 Wrote Its Own Training Data  #aiagents #OpenWeights #Ornith · Romi Patel · süre: 1:44 · en-orig · https://youtu.be/yNDwmWVXw9I · şema 2
motor: parti 2026-10-10-short-6 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 32432 tk · claude-haiku-5-5: claude-haiku-5-5 · 26191 tk
## Özet
Romi Patel'in kısa videosu, açık ağırlıklı Ornith 1.5 modelini anlatıyor: 35B parametreli, token başına yaklaşık 3B aktif, MIT lisanslı bir mixture-of-experts modeli. Model kendi eğitim görevlerini üretiyor, kendi scaffold'unu kuruyor ve pekiştirmeli öğrenmeyle çözümlerini ödüllendiriyor; üç parça birlikte optimize ediliyor. Video, model kendi sınavlarını yazdığında zorluğu kimin koruyacağı sorusuyla bitiyor.
## Bölümler
- 0:00 Giriş: Ornith 1.5 açık model ve teknik özellikler
- 0:25 Qwen 3.6 ve SWE-Bench karşılaştırması, model soyağacı
- 0:44 Ornith 1.0 ile 1.5 farkı: kendi görevlerini üretme
- 1:01 Scaffold kurma, rollout ve RL ödül döngüsü
- 1:14 Önemi: insan etiketli veri darboğazı
- 1:26 Açık soru: sınavların zorluğunu kim koruyacak?
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Ornith 1.5 | yok | teknik | yok | Kendi eğitim görevlerini üreten 35B MoE, MIT lisanslı açık ağırlıklı model. | 0:08 | Karede model kartı: ORNITH 1.5, OPEN WEIGHTS (karede: Model kartı: ORNITH 1.5, OPEN WEIGHTS, weights/config/readme düğmeleri) |
| Hugging Face | yok | teknik | yok | Model ağırlıklarının yayımlandığı model barındırma platformu. | 0:08 | Karede huggingface.co/ornith-1.5 adresi (karede: Üstte OPEN MODEL ve huggingface.co/ornith-1.5) |
| Qwen 3.6 | yok | teknik | yok | Karşılaştırma yapılan aynı boyuttaki model. | 0:00 | it beats Qwen 3.6 at the same size |
| SWE-Bench | yok | teknik | yok | Kodlama kıyaslama testi; Ornith önceki nesil 397B modeli geçiyor. | 0:00 | on SWE-Bench, it edges out a 397 billion parameter model |
| Gemma | yok | teknik | yok | Ornith'in üzerine inşa edildiği modellerden biri. | 0:00 | built on top of Qwen and Gemma |
| Qwen | yok | teknik | yok | Ornith'in üzerine inşa edildiği model ailesi. | 0:00 | built on top of Qwen and Gemma |
| Mixture of experts | yok | teknik | yok | Token başına yalnız ~3B parametrenin aktif olduğu mimari. | 0:00 | 35 billion parameters, mixture of experts, about 3 billion active |
| Reinforcement learning | yok | teknik | yok | Çalışan çözümleri ödüllendiren eğitim yöntemi. | 1:01 | reinforcement learning rewards what works |
| Scaffold | yok | teknik | yok | Modelin çalıştığı araç ve ortam iskeleti; model kendisi kuruyor. | 0:44 | It built its own scaffolds, but still practiced on a fixed task set |
## Açıklama bağlantıları
- https://www.linkedin.com/in/romippatel/ — Video sahibinin LinkedIn profili · aday: hayır · Kişisel profil; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://www.instagram.com/romippatel/ — Video sahibinin Instagram profili · aday: hayır · Kişisel profil; izleyicinin kullanacağı araç değil. · sınıf: diğer
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Ornith 1.5 35B MoE, token başına yaklaşık 3B aktif, MIT lisanslı. | 0:00 | sayısal |
| Kendi yayımladığı benchmarklarda aynı boyuttaki Qwen 3.6'yı geçiyor. | 0:00 | karşılaştırma |
| SWE-Bench'te önceki nesil 397B modeli geride bırakıyor. | 0:00 | karşılaştırma |
| Görev üretimi, scaffold ve rollout'lar ortak optimize ediliyor. | 1:01 | özellik |
| Kendi müfredatını üreten model, çok sayıda anotatör gerektirmeden ölçeklenir. | 1:01 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ekran 0:02 | Hugging Face | Hugging Face | huggingface.co/ornith-1.5 |
| altyazı 0:00 | Ornith 1.5 | Ornith 1.5 | Open with 1.5 partly trained itself |
| altyazı 0:00 | Mixture of experts | Mixture of experts | mixture of experts, about 3 billion active |
| altyazı 0:00 | MIT lisansı | aday değil: genel kavram | MIT licensed |
| altyazı 0:00 | Qwen 3.6 | Qwen 3.6 | beats Qwen 3.6 at the same size |
| altyazı 0:00 | SWE-Bench | SWE-Bench | on SWE-Bench, it edges out a 397 billion |
| altyazı 0:00 | Qwen | Qwen | built on top of Qwen and Gemma |
| altyazı 0:00 | Gemma | Gemma | built on top of Qwen and Gemma |
| altyazı 1:01 | Reinforcement learning | Reinforcement learning | reinforcement learning rewards what works |
| altyazı 0:44 | Scaffold | Scaffold | It built its own scaffolds |
| altyazı 1:01 | Rollout | aday değil: başka adayın parçası (Reinforcement learning) | rolls out full solutions |
| kare 1:40 | Romi Patel / Subscribe | aday değil: konu dışı | Kapanış karesi: Romi Patel, Subscribe |
| açıklama | LinkedIn bağlantısı | aday değil: konu dışı | linkedin.com/in/romippatel |
| açıklama | Instagram bağlantısı | aday değil: konu dışı | instagram.com/romippatel |
| yorum | Interesting analysis | aday değil: konu dışı | Interesting analysis |
## Kareden okunanlar
- 0:08: Model kartı: OPEN MODEL, huggingface.co/ornith-1.5, NEW THIS MONTH, ORNITH 1.5 OPEN WEIGHTS, weights/config/readme düğmeleri, IT TRAINED.
- 1:38: WHO KEEPS THE EXAMS HARD?, SELF-WRITTEN EXAM kartı, zorluk çubuğu, THE EXAM · NOT GUARDED, EXAM ROOM HARDENED.
- 1:40: Kapanış: THANKS FOR WATCHING, Romi Patel, @Romi_Patel, Subscribe düğmesi.
## Belirsizlikler
- Altyazıda model adı 'Open with' diye geçiyor (otomatik altyazı hatası); ekranda ve açıklamada Ornith.
- Açıklamadaki 19 Ağustos 2026 tarihi ve benchmark rakamları bağımsız doğrulanmadı.
- Sözlük eşleşmeleri (Three.js, Next.js, Matter.js, TypeScript, Inter) videoda kullanıldığına dair kanıt yok; aday yapılmadı.
- Açıklamadaki 'Qwen 3.5 397B' ile altyazıdaki 'önceki nesil 397B' aynı model varsayıldı.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| huggingface.co/ornith-1.5 | 0:02 | ekran | evet |
| https://www.linkedin.com/in/romippatel/ | açıklama | açıklama | hayır |
| https://www.instagram.com/romippatel/ | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Ornith 1.5 açık ağırlıklarının Hugging Face'te yayımlandığını ve teknik özelliklerini tanıtma — araçlar: Ornith 1.5, Hugging Face, Mixture of experts
- 2. adım — Benchmark karşılaştırması: Qwen 3.6 ve SWE-Bench sonuçları — araçlar: Qwen 3.6, SWE-Bench
- 3. adım — Model soyağacını anlatma: Qwen ve Gemma üzerine inşa — araçlar: Qwen, Gemma
- 4. adım — Ornith 1.0'ın sabit görev setini anlatma — araçlar: Scaffold
- 5. adım — Ornith 1.5'in kendi eğitim görevlerini üretmesini anlatma — araçlar: Ornith 1.5
- 6. adım — Modelin kendi scaffold'unu kurmasını anlatma — araçlar: Scaffold
- 7. adım — Rollout ve ödüllendirme: pekiştirmeli öğrenme döngüsü — araçlar: Reinforcement learning
- 8. adım — Sınav zorluğunu koruma sorusunu ortaya koyma — araçlar: Ornith 1.5
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
