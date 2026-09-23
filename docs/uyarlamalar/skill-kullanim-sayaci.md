# Uyarlama: skill-kullanim-sayaci

20b-devam K5 · kaynak: caveman learn `dead_load:skills` (docs/mekanizmalar/caveman.md) · kod yazılmaz; Desktop tarif verir · MIT/BSL kodu kopyalanmaz

## Fikir
Son 30 günün transkriptlerinde (`~/.claude/projects/*/*.jsonl`) her skill'in `Skill` aracıyla kaç kez çağrıldığını say; hiç çağrılmayanların description token maliyetini (her tur yüklenir) topla. Kaldırmak yok (omer-kurallar:22); çıktı yalnız "hangi skill departman müdürünün arkasına alınabilir / description kısaltılabilir" listesi.

## Hedef araç/dosya
tools/video/video/departman.py (`video departman` envanterine "kullanım (30g)" sütunu) · departman-verimlilik müdürü

## Beklenen etki
learn ölçümü: 60 skill ~1262 token/tur, kullanım yok (~%2 ilk tur istemi). Açıklaması kısaltılan/müdüre bağlanan her kullanılmayan skill bu payı düşürür; kalite etkisi yok (skill kurulu kalır).

## Kapsam
salt-okur sayaç + rapor; skill dosyası ya da ayar otomatik değişmez.
