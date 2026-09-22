# Jev — .NET

Kopyalanabilir şablon: `templates/jev-dotnet` (omer-skills reposu, .NET 10). İçinde `IJevClient`/`JevClient` (typed HttpClient, `AddJev(IConfiguration)`, retry, çift tavan), record'lar, `JevBands` (0.85/0.60, noul max(p,1−p)), `BatchAsync` (≤200'lük parça, ≤8 eşzamanlı), kapatılamaz TR redaksiyonu (`TurkishRedactor` + ek `IStateRedactor`), `FakeJevClient` ve xUnit testleri var.

README'de şu kalıpların 10-15 satırlık örnekleri var: intent routing · composite scoring · confidence routing · select-not-generate (OCR adayından alan seçimi) · hiyerarşik sınıflama.

KVKK: state yurt dışına gider. Canlıya almadan önce `use-case-triage` çalıştırılır.
