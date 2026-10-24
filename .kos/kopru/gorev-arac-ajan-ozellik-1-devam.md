# ARAC-AJAN-OZELLIK-1 devam (p1)

Durum: envanter iskeleti var (docs/envanter/arac-ajan-ozellik.tsv, 560 satır), eşleme doğruluğu 7/12 → kapı ≥%98 yok.

p1 (önce): tools/arac_ajan_envanter.py KURALLAR'ı düzelt, `learn` regex'i `\blearn\b|continuous-learning`; tasarım/güvenlik/debug/CLI-demo kuralları ekle; `ajan_sira (genel)` kovasını (202 satır) daralt; ne_yapar'ı ozellik kopyası yerine README ilk cümlesinden doldur. Sonra okuyucu ile 30 satır örnekle, ≥%98 olana dek tekrarla.
p2: çekirdek 15 araç için headless deneme (_deneme/arac-ajan/<araç>/): çıktı + süre + token + RAM tepe. ruflo swarm tek tek aç, pid kapat.
p3: ajan-özellik etiketi (her_sey_ara/katalog), görev şablonuna "bu işte kullanılacak araç-ajanları" satırı.
p4: 3 gerçek görevde transkript kanıtı; zorunlu 11 araç çağrısı.
Komut: python tools/arac_ajan_envanter.py
