# prompt-hilesi (DcrhGgKyBD8)

**Amaç:** AI kodlama ajantları ile kaliteli, hatasız kod üretimi için otomatik döngüleme sistemi oluşturmak.
**Araçlar:** Claude AI (veya benzer bir AI kodlama ajanı), Worker sub-agents (görevleri parçalayan ajantlar), Strict boss agent (kalite kontrolü yapan ajant)

**Adımlar**
1. [] Görevi bir 'task' satırı ile tanımlayın (örn: 'Create a Flask web app with login and dashboard').
2. [] Görevi en küçük parçalara ayırın (örn: 'login page', 'dashboard UI', 'database connection') ve her parçaya bir worker ajanı atayın.
3. [] Prompt'in üçüncü satırında bir 'strict boss' ajanı atayın: bu ajanın görevi, çıktının çalışıp çalışmadığını test edip hataları tespit etmektir.
4. [] Worker ajentler kod üretirken, boss ajanı çıktının çalışıp çalışmadığını sürekli kontrol eder. Eğer hata varsa, worker ajantlara düzeltme emri verir.
5. [] Prototip tamamlandığında, Boss Loop'u kullanarak son ürünü polişleyin (örn: performans iyileştirmeleri, UI düzenlemeleri).

**Prompt/kod/ayar:** ```prompt
1. [TASK] Build a [X] with [Y features].
2. Split into smallest judgeable pieces: [list of tasks].
3. Assign a strict boss agent to test and validate output until perfect.
```
**Sonuç:** Hatasız, kaliteli kod üretimi için otomatik döngüleme sağlayan bir sistem.
**Bizde (öneri, modelden):** Kurulu araçlarla (örn: LangChain, AutoGPT gibi) bu döngüyü simüle edebilirsiniz: worker ajantları olarak LLM'leri kullanarak kod parçalarını üretebilir, boss ajantı olarak ise bir test script'i veya kalite kontrolü yapacak bir LLM'i atayabilirsiniz.
**Daha iyi (öneri):** Boss ajantının test kriterlerini daha detaylı tanımlamak (örn: 'Pytest ile test et', 'Linter kurallarına uygun olmalı'), token ekonomisini optimize etmek için prototip aşamasını kısaltmak.
