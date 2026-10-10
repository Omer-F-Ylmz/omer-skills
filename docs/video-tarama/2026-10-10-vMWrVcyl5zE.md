# TypeLLM: Make Your LLM Answer in Exact, Valid Types
## Künye
TypeLLM: Make Your LLM Answer in Exact, Valid Types · Trending Open Source Projects · süre: 0:32 · en-orig · https://youtu.be/vMWrVcyl5zE · şema 2
motor: parti 2026-10-10-short-6 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 18257 tk · claude-haiku-5-5: claude-haiku-5-5 · 39327 tk
## Özet
32 saniyelik Shorts, TypeLLM adlı açık kaynak projeyi tanıtıyor. TypeLLM, SGLang üzerinde çalışan ve LLM çıktısını sayı, evet/hayır ya da sınırlı seçenek gibi tam olarak istenen tipte, geçerli biçimde döndüren bir kütüphane. Model mimarisi ya da ağırlıkları değişmiyor. README gösteriliyor: özellikler, JevBench sonuçları (231 görevde 228 doğru, düşünme açıkken) ve pip ile kurulum. Fiş ve bilet gibi belgelerden bilgi çıkarmak için öneriliyor.
## Bölümler
- 0:00 Bozuk JSON sorunu ve TypeLLM tanıtımı
- 0:07 Özellikler listesi
- 0:11 JevBench doğruluk sonuçları
- 0:14 Hızlı başlangıç: SGLang ve pip kurulumu
- 0:19 Örnek istek ve çıktı (fiş verisi)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| TypeLLM | yok | teknik | github.com/TypeLLM/TypeLLM | LLM çıktısını şemaya uygun tiplerle (string, integer, number, boolean, enum) sınırlayan kütüphane | 0:00 | Type LLM forces valid types; always answers in that exact shape. |
| SGLang | yok | teknik | yok | TypeLLM'in üzerine kurulduğu ve modeli sunduğu çıkarım sunucusu | 0:07 | Built on SGLang; serve with SGLang (karede: kanıttan) Built on SGLang; serve with SGLang |
| JevBench | yok | teknik | yok | 231 genel görevden oluşan doğruluk karşılaştırma seti | 0:11 | Evaluated on 231 public JevBench tasks. (karede: kanıttan) Evaluated on 231 public JevBench tasks. |
| Jev | yok | teknik | yok | TypeLLM'e ilham veren TypeSafe AI'ın tip güvenli üretim yaklaşımı | 0:06 | Inspired by TypeSafe AI's Jev (karede: kanıttan) Inspired by TypeSafe AI's Jev |
| Qwen3.8-27B | yok | teknik | yok | Örnekte ve testte kullanılan model | 0:17 | model="Qwen/Qwen3.8-27B" (karede: kanıttan) model="Qwen/Qwen3.8-27B" |
| TypeLLMClient | yok | teknik | yok | SGLang sunucusuna bağlanan Python istemci sınıfı | 0:17 | Point TypeLLMClient at the SGLang server's HTTP endpoint (karede: kanıttan) Point TypeLLMClient at the SGLang server's HTTP endpoint |
| Open-Jev 27B v1.1 | yok | teknik | yok | Karşılaştırma tablosundaki model | 0:11 | Tabloda Open-Jev 27B v1.1 %85.28 (karede: kanıttan) Tabloda Open-Jev 27B v1.1 %85.28 |
| GPT-5.6 Luna | yok | teknik | yok | Karşılaştırma tablosundaki model | 0:12 | Tabloda GPT-5.6 Luna (none) %89.18 (karede: kanıttan) Tabloda GPT-5.6 Luna (none) %89.18 |
| GPT-6 Astra | yok | teknik | yok | Karşılaştırma tablosundaki model | 0:12 | Tabloda GPT-6 Astra (low) %100.00 (karede: kanıttan) Tabloda GPT-6 Astra (low) %100.00 |
| RadixArk/Qwen3.8-27B-NVFP4-BF16-LMHead | yok | teknik | yok | TypeLLM'in kullandığı mevcut checkpoint, ince ayar yok | 0:14 | No fine-tuning was applied. · kanıt: kare (karede: No fine-tuning was applied.) |
| GitHub | yok | teknik | yok | README'nin gösterildiği kod barındırma servisi | 0:00 | github.com/TypeLLM/TypeLLM#readme (karede: kanıttan) github.com/TypeLLM/TypeLLM#readme |
| gittrend.io | yok | teknik | yok | Kanalın trend açık kaynak projeleri sitesi | 0:00 | More like this → gittrend.io (açıklama) |
| JSON Schema | yok | teknik | yok | Şemaya uygun çıktı garantisi için kullanılan şema biçimi | 0:06 | guaranteed outputs through JSON Schema (karede: kanıttan) guaranteed outputs through JSON Schema |
| Permutation averaging | yok | teknik | yok | Enum seçeneklerinde sıra yanlılığını azaltma tekniği | 0:08 | Reduce option-order bias on explicit enum questions (karede: kanıttan) Reduce option-order bias on explicit enum questions |
| KV caching | yok | teknik | yok | Ortak önek bağlamının yeniden işlenmesini önleyen önbellek | 0:07 | KV caching avoids reprocessing shared context. (karede: kanıttan) KV caching avoids reprocessing shared context. |
| pip | yok | CLI | yok | Python paket yöneticisi; 'pip install -U typellm' ile kütüphaneyi kurar/günceller. | 0:17 | 2. Run TypeLLM kod bloğunda pip install komutu (karede: 2. Run TypeLLM bölümünde kod bloğu; 'pip ir…' satırı altyazının altında kısmen kapalı) |
| Satıcı adını çıkarma | yok | prompt | yok | Yalnızca satıcı adını döndür (merchant, string) — fiş metninden Hilton London gibi bir ad. | 0:20 | kaynak: altyazı |
| Toplam tutarı çıkarma | yok | prompt | yok | Toplam tutarı GBP cinsinden çıkar (total, number). | 0:22 | kaynak: altyazı |
| Gider türünü seçtirme | yok | prompt | yok | Bu gider ne tür? Seçenekler meal, travel, equipment (expense_type, enum). | 0:22 | kaynak: altyazı |
| Geri ödeme kararı | yok | prompt | yok | Bu gider geri ödenmeli mi? (reimbursable, boolean). | 0:23 | kaynak: altyazı |
| Güven puanı | yok | prompt | yok | Ne kadar emin olduğun? (confidence, number; örnekte 0.75). | 0:24 | kaynak: altyazı |
| Serbest metin özeti | yok | prompt | yok | Özetle (summary, string); bağlam: 'The train ticket is for a client meeting.' Komut metni OCR'da kesik. | 0:31 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pip install -U typellm | TypeLLM paketini kurar ya da günceller (karede: 2. Run TypeLLM bölümünde pip install -U typellm kutusu) | 0:17 | kare |
| from typellm import TypeLLMClient | Python'da TypeLLM istemcisini içe aktarır (karede: Kod bloğunda from typellm import TypeLLMClient) | 0:17 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| TypeLLM, mevcut modelleri değiştirmeden her zaman istenen tipte yanıt verir | 0:00 | özellik |
| Genel testte 231 üzerinden 228 puan aldı | 0:00 | sayısal |
| Düşünme kapalıyken 195/231, açıkken 228/231 | 0:07 | sayısal |
| Fiş ve biletlerden bilgi çıkarmak için kullanışlı | 0:00 | öneri |
| Çıktı token maliyeti ihmal edilebilir düzeyde | 0:07 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | TypeLLM | TypeLLM | Type LLM forces valid types |
| altyazı 0:00 | JSON | aday değil: genel kavram | Your LLM keeps returning malformed JSON? |
| altyazı 0:00 | Fiş ve bilet çıkarımı kullanım alanı | aday değil: konu dışı | pulling details out of receipts or tickets |
| altyazı 0:00 | Repo linki için yorum çağrısı | aday değil: konu dışı | Comment type and I'll send you the repo link. |
| açıklama | gittrend.io | gittrend.io | More like this → gittrend.io |
| açıklama | #Shorts | aday değil: genel kavram | #Shorts |
| kare 0:00 | GitHub | GitHub | GitHub - TypeLLM/TypeLLM sekmesi |
| kare 0:00 | Apache-2.0 license | aday değil: genel kavram | Apache-2.0 license sekmesi |
| kare 0:07 | Image input | aday değil: başka adayın parçası (TypeLLM) | Image input maddesi |
| kare 0:07 | depends_on bağımlılık grafiği | aday değil: başka adayın parçası (TypeLLM) | declare depends_on to form a dependency graph |
| kare 0:07 | Thinking mode | aday değil: başka adayın parçası (TypeLLM) | Supports thinking mode |
| kare 0:07 | TypeSafe AI's Jev | Jev | Inspired by TypeSafe AI's Jev |
| kare 0:07 | SGLang | SGLang | Built on SGLang |
| kare 0:07 | KV caching | KV caching | KV caching avoids reprocessing shared context. |
| kare 0:07 | Permutation averaging | Permutation averaging | Reduce option-order bias |
| kare 0:07 | JSON Schema | JSON Schema | through JSON Schema |
| kare 0:11 | JevBench | JevBench | Evaluated on 231 public JevBench tasks. |
| kare 0:12 | Open-Jev 27B v1.1 | Open-Jev 27B v1.1 | Tablo satırı |
| kare 0:12 | Jev 1.13.0 | Jev | Tablo satırı Jev 1.13.0 |
| kare 0:12 | GPT-5.6 Luna | GPT-5.6 Luna | Tablo satırı |
| kare 0:12 | GPT-6 Astra | GPT-6 Astra | Tablo satırı |
| kare 0:14 | Qwen3.8-27B | Qwen3.8-27B | TypeLLM + Qwen3.8-27B satırları |
| kare 0:14 | RadixArk checkpoint | RadixArk/Qwen3.8-27B-NVFP4-BF16-LMHead | existing RadixArk checkpoint |
| kare 0:17 | pip | aday değil: genel kavram | pip install -U typellm |
| kare 0:17 | TypeLLMClient | TypeLLMClient | Point TypeLLMClient at the SGLang server's HTTP endpoint |
| kare 0:00 | gittrend.io rozeti | gittrend.io | Sağ altta gittrend.io rozeti |
| kare 0:00 | Homepage, Blog, Docs, Early Access, Contact bağlantıları | aday değil: başka adayın parçası (TypeLLM) | README bağlantı satırı |
| kare 0:17 | http://127.0.0.1:30000 | aday değil: başka adayın parçası (SGLang) | Yerel SGLang sunucu adresi |
## Kareden okunanlar
- 0:00: GitHub README: TypeLLM: LLMs with type-safe generation; Updates listesi; github.com/TypeLLM/TypeLLM#readme; gittrend.io rozeti
- 0:07: Features listesi: out-of-schema hallucination yok, shared-prefix reuse, depends_on bağımlılık grafiği
- 0:08: Supported output types: String, Integer, Number, Boolean, Enum choice; Features maddeleri
- 0:11: Features 5-8 ve JevBench sonuçları başlığı
- 0:12: Accuracy Benchmark tablosu: Open-Jev 27B v1.1 %85.28, Jev 1.13.0 %86.58, GPT-5.6 Luna %89.18, GPT-6 Astra %100.00
- 0:14: Tablo: TypeLLM + Qwen3.8-27B no thinking %84.42, thinking %98.70
- 0:17: Quick start: pip install -U typellm; TypeLLMClient
- 0:18: Kod: from typellm import TypeLLMClient; client = TypeLLMClient("http://127.0.0.1:30000", model="Qwen/Qwen3.8-27B")
## Belirsizlikler
- README'deki model ve sürüm adları (Qwen3.8-27B, GPT-6 Astra vb.) OCR ve kare çözünürlüğü nedeniyle tam doğrulanamadı.
- Kareler 0:08 ve 0:17'den sonrası için yalnız OCR vardı; kod örneğinin tamamı görülemedi.
- Videoda 'Type LLM' diye seslendirilen ad README'de TypeLLM yazılıyor.
- OCR'daki Radix UI ve Claude Code eşleşmeleri yanlış pozitif görünüyor; RadixArk checkpoint adından geliyor.
- Videonun ana yapay zekâ aracı belirtilmiyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/TypeLLM/TypeLLM#readme | 0:00 | ekran | evet |
| gittrend.io | 0:00 | ekran | evet |
| http://127.0.0.1:30000 | 0:18 | ekran | hayır |
## İş akışı
- yok
## Promptlar
- Satıcı adını çıkarma — Yalnızca satıcı adını döndür (merchant, string) — fiş metninden Hilton London gibi bir ad.
- Toplam tutarı çıkarma — Toplam tutarı GBP cinsinden çıkar (total, number).
- Gider türünü seçtirme — Bu gider ne tür? Seçenekler meal, travel, equipment (expense_type, enum).
- Geri ödeme kararı — Bu gider geri ödenmeli mi? (reimbursable, boolean).
- Güven puanı — Ne kadar emin olduğun? (confidence, number; örnekte 0.75).
- Serbest metin özeti — Özetle (summary, string); bağlam: 'The train ticket is for a client meeting.' Komut metni OCR'da kesik.
ikinci göz KAPALI: --ikinci-goz yok
