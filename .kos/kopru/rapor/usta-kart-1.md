# USTA-KART-1 tur5 (29 Eki)
- Karar: üretim Haiku'ya taşındı (alt ajan yolu; claude -p 399 sn soğuk başlatma atlandı). Aynı 32 kalem (40 değil: usta.jsonl'de 32 kart var).
- Haiku medium: hakem (bağımsız Haiku alt ajan) 29/32 = %91 < %92 → merdiven: Haiku high.
- Haiku high: 31/32 = %97 ≥ %92 KAPI GEÇTİ (tek ret: örnek codex exec, kullanım örneği değil).
- Maliyet: ölçülemedi ($ alınmadı); alt ajan jetonu: medium ~4×32k + hakem 58k; high ~4×43k + hakem 57k (toplam ≈ 0,45M Haiku jeton).
- Kod: usta_kart.py hazirla/isle komutları; çıktı .kos/kopru/usta-haiku/haiku.jsonl (medium sonuçları _medium/). usta.jsonl'e henüz birleştirilmedi; ikinci göz (ücretsiz doğrulama) Haiku hattında yok.
- Sıradaki: kalan kalemleri aynı hatla ölçekle (hazirla --g 8 genelleme gerekir: şu an yalnız mevcut kartlı kalemleri alır).

# TUR 8 (29 Eki)
- 100 yeni kart (13 Haiku high alt ajanı, 8'lik grup), usta.jsonl 200 kart. Boş ornek 48, boş kombin 47 (kaynakta yok → uydurma yok).
- Hakem (bağımsız Haiku alt ajan, 20 rastgele kart): 20/20 = %100 ≥ %92. Sınır: 5 kartta Read kaynağı kesti, o kısımlar doğrulanamadı; 15 kart tam doğrulandı.
- Maliyet: $ ölçülemedi; alt ajan jetonu 13 üretici ≈ 590k + hakem; kart başı ≈ 6k Haiku jetonu. Haiku medium ön denemesi yapılmadı (kısa kaynak ayrımı eklenmedi).
- Yedek: usta-haiku/_arsiv/tur7, usta.jsonl.bak. Push yok.

# TUR 9 (29 Eki)
- 100 yeni kart, usta.jsonl 300. hazirla: kaynak 6000'lik parçalara bölünüp hepsi veriliyor (--uzun: kaynağı >6000 olan mevcut 94 kartı yeniden üretmek için; bu turda koşulmadı), kısa kaynaklılar başa sıralanıyor.
- Haiku medium denemesi: yalnız 1 grup (8 kart, kaynak ≤1500, g0); hakem örnekleminde 1 kart düştü (gmod-addon-maker-paket: genel). 8 kartlık örnek karar için yetersiz.
- Hakem (bağımsız Haiku alt ajan, 20 kart, tam kaynak): 18/20 = %90 < %92 KAPI GEÇMEDİ. Red: davila7-gmod-addon-maker-paket (genel, medium), hairline-create (kaynakla çelişen satır, high).
- Boş ornek 43, boş kombin 43 (kaynakta yok → uydurma yok).
- Maliyet: $ ölçülemedi; 13 üretici ≈ 0,9M Haiku jetonu (ortalama 70k/grup) → kart başı ≈ 9k jeton (parçalı kaynak okuma yüzünden tur 8'den yüksek); hakem ≈ 123k.
- Sıradaki: iki red kartı Sonnet medium ile yeniden üret + yeniden ölç; sonra --uzun.

# TUR 10 (29 Eki)
- 2 red kart (gmod-addon-maker-paket, hairline-create) Haiku high ile yeniden üretildi (hairline 2 parça kaynakla); --uzun ile 6000'i aşan 94 kart parçalı kaynakla yeniden üretildi. usta.jsonl 300 (yedek usta.jsonl.bak). Üretici: 13 Haiku high alt ajan.
- Hakem (bağımsız Haiku, 40 kart, tam kaynak): 35/40 = %88 < %92 KAPI GEÇMEDİ. Yeniden üretilen 26 kartta 24/26 (%92; 2 red kart ikisi de geçti; 2 red: 1 kart "en sık hata" iddiası kaynakta yok, 1 "özet kullanıcıya seçtirilmez"); eski 14 kartta 11/14 (%79: 3 red, genel/tekrar ve token_ipucu çelişkisi).
- Maliyet: $ ölçülemedi; 13 üretici ≈ 1,1M Haiku jetonu (94+2 kart → ≈11k/kart), hakem 259k.
- Sıradaki: reddedilen 5 kartı yeniden üret; eski (parçalı kaynaksız üretilmiş) kartlardaki genel kartlar için --zayif benzeri "genel" süzgeç; sonra yeni 40'lık hakem. Push yok.

# TUR 11 (29 Eki)
- Parçalı kaynak öncesi üretilmiş 106 eski kart (tur 5-8; `hazirla --eski`) 14 Haiku high alt ajanıyla parçalı kaynakla yeniden üretildi; usta.jsonl 300 (yedek .bak, ileri/ _arsiv/tur10, tur10b).
- Hakem (bağımsız Haiku, yeniden üretilenlerden rastgele 40, tam kaynak): 39/40 = %97,5 ≥ %92 KAPI GEÇTİ. Tek ret: bir animasyon kartında "yalnız transform/opacity" kaynaktaki "unless necessary" istisnasıyla çelişiyor.
- Maliyet: $ ölçülemedi; 14 üretici ≈ 0,66M Haiku jetonu (≈6k/kart), hakem 120k. Tur 10'daki 5 ret ayrıca yeniden üretilmedi (94 uzun kart tur 10'da zaten yenilenmişti; 1 ret ek).
- Sıradaki: 300 kart tamam; kartsız kalan kalemler için `hazirla` yeni kalem verir, bir sonraki tur oradan.

# TUR 13 (29 Eki)
- 48 tur-12 paket karti alt skill kaynagiyla (kaynak() alt_skiller, hazirla --paket) Haiku high ile yeniden uretildi; animation-performance/systems "yalniz transform/opacity" ifadesi "varsayilan/mumkunse" yapildi. usta.jsonl 400.
- Hakem (bagimsiz Haiku, 40 kart): RED=10; kapi %87. Kaynaklar katalog tablosu oldugu icin paket kartlarinda ornek cogu TALIMAT.md yolu, komut yok. Maliyet: $ olculemedi; 8 uretici ~410k Haiku jeton (~8.5k/kart).
