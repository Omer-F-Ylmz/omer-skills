# RTK A/B · 2026-09-17
Görev: `Desktop\rtk-ab` (Money value object + 4 xUnit; .NET 10.0.400, xunit VSTest), `claude -p` Opus 5 high, `--max-budget-usd 3`, aynı `task.txt`.
A = rtk hook açık + CLAUDE.md "rtk dotnet" kuralı · B = hook kapalı + `--append-system-prompt "Bu oturumda rtk kullanma; dotnet komutlarını doğrudan çağır."`.
Taban: A `git stash -u`; B `git switch --detach base` (d0af0b5), HEAD ve temiz ağaç doğrulandı. 4 koşu 4/4 yeşil; ilk B turu (A2 commit'i yüzünden "zaten yapılmış") geçersiz sayılıp atıldı.
Karakter = jsonl'de `dotnet build|test` içeren komutların tool_result toplamı.

| koşu | girdi | cache okuma | cache yazma | çıktı | toplam | $ | tur | build/test çağrı · karakter | elle rtk |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 10 | 118,355 | 34,435 | 2,595 | 155,395 | 0.469 | 5 | 2 · 2,109 | 1 |
| A2 | 10 | 126,874 | 13,282 | 2,548 | 142,714 | 0.261 | 6 | 3 · 1,523 | 1 |
| B1 | 10 | 126,344 | 12,430 | 2,310 | 141,094 | 0.246 | 5 | 2 · 363 | 0 |
| B2 | 10 | 144,263 | 8,247 | 2,669 | 155,189 | 0.222 | 5 | 2 · 1,103 | 0 |

## Fark (A − B) / B
- Ortalama: toplam token +%0.6 (149,055 / 148,142) · cache yazma +%130.8 (23,859 / 10,339) · $ +%55.9.
- A2 vs B2 (ikisi sıcak): toplam token −%8.0 · cache yazma +%61.1 · $ +%17.4 · build/test karakter 1,523 / 1,103.
- A1 soğuk başladı (cache yazma 34,435), B1 başlamadı (12,430) → ortalama cache yazma ve $ farkı A'ya karşı şişik.
## Gözlem
- B'de model çıktıyı kendi süzüyor (`| grep -E "error|Passed!|Failed!"`, `| head -5`); A'da da `rtk dotnet … | tail -8`. rtk'nın kısaltacağı ham çıktı iki kolda da modele ulaşmıyor.
- Karakterin çoğu ilk derleme hatasının çıktısı (A1 1,981 · A2 1,260 · B2 962).
- A'da model CLAUDE.md kuralıyla `rtk dotnet` yazıyor (elle rtk 1'er); hook'a dönüştürecek komut kalmıyor.
- A2 işi ayrıca commit'ledi (+1 tur, kod dışı).
## Öneri
- Bu görevde rtk'nın ölçülebilir token kazancı yok: toplam fark ±%8 içinde, yön tutarsız, n=2. Hook ve kural değiştirilmez.
- Kaldırma/koruma kararı büyük çıktılı görevde (çok projeli build, kırmızı test dökümü) aynı düzenekle tekrarlanan A/B'ye bırakılır.
