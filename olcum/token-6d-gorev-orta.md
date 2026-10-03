Görev: tools/video/video/kur.py içinde üç düzeltme yap; üretim kodu yalnız bu dosyada değişir.

1. `takas(s, d, esik_ok)`: d < 0 (kalite arttı) düşüş yok sayılır ve d == 0 ile aynı kararı verir (esik_ok ise "AL", değilse "RED(token)"). Dönen kademe metni "kalite arttı" ifadesini içerir; "düşüş >0" ya da "≤%10" içermez. d ≥ 0 davranışı değişmez.
2. `esik(s)`: yüzde işareti sayının sonunda da olabilir ("çıktı ≥ 30%", "maliyet 20,5 %"); mevcut önek biçimi ("çıktı −%30") çalışmaya devam eder. Bir alanın (çıktı · girdi · maliyet) sayısı yalnız kendi ifadesinden okunur: alan adıyla sayı arasına başka bir alan adı girerse o alan için eşleşme yok sayılır (ör. "çıktı ölçülmez · maliyet %20" → çıktı eşiği yok, varsayılan 25; maliyet 20).
3. `tasarruf(a, b)`: b'de alan yoksa ya da değeri None ise o alan 0.0 döner (hata fırlatmaz); mevcut davranış korunur.

Kabul: olcum/token6d/test_orta.py (bu dosyayı değiştirme) geçer — `cd tools/video && uv run --with pytest pytest -q -p no:cacheprovider ../../olcum/token6d` — ve tools/video suite'i yeşil kalır (`cd tools/video && uv run --with pytest pytest -q -p no:cacheprovider`). Commit atma.
