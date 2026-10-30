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

# TUR 14 (29 Eki)
- Kök neden: alt_skiller() yalnız */SKILL.md arıyordu; paketlerde alt skill gövdesi TALIMAT.md. Düzeltildi: TALIMAT/SKILL.md, ilk komut bloğu (KOMUT:), ≤600 kr/alt skill, toplam ≤6000. hazirla --ad eklendi; paket kartında kaynakta olmayan ornek boş string.
- 10 ret kartı + hakemde çıkan 15 eski ret (paket/tasarım) Haiku high ile yeniden üretildi (25 kart, 5 üretici). usta.jsonl 400.
- Hakem (bağımsız Haiku alt ajan, 40 kart, UTF-8 dosya): 1. koşu 25/40 (%62; 10 yenilenen kart hepsi geçti, 15 ret eski kartlar); 2. koşu 38/40 = %95 ≥ %87 KAPI GEÇTİ. Kalan ret: davila7-productivity-paket (genel), davila7-sports-paket (lig kapsamı kaynakta yok).
- Not: claude -p hakem 300 sn zaman aşımı; hakem --istem ile alt ajana verildi. Maliyet $ ölçülemedi; ~8 alt ajan ≈ 0,4M Haiku jetonu. Push yok.

# TUR 15 (29 Eki)
- 2 ret karti (davila7-productivity-paket, davila7-sports-paket) Haiku high ile yeniden uretildi (alt ajan; kaynakta olmayan iddia yasagi eklendi, yeniden hakeme sokulmadi).
- Sonraki 100 kartsiz kalem (hazirla --g 10 --n 100) 10 Haiku alt ajanla uretildi, usta.jsonl 527. Kalan kartsiz/eski: 6348 (say).
- Hakem 40 rastgele yeni kart (seed 15, liste hakem15-adlar.json): 1. kosu 10/40 GECERSIZ (hakem kaynagi 4000 karakterde kesik gordu); 2. kosu tam kaynak parcalariyla 4 bagimsiz Haiku hakem: 33/40 = %82 < %87 KAPI TUTMADI. Retler: github, number-details, engineering:code-review, mukul975-zero-trust-paket, open-gstack-browser, pinecone-query, n8n-expression-syntax (token_ipucu/tuzak'ta kaynakta olmayan ya da yaniltici iddia; paket karti yalniz dosya yonlendirmesi).
- Duzeltilmedi (tur siniri). Sonraki tur: 7 ret + token_ipucu'nda 'kaynakta yok' disi kaynaksiz iddia ureten kartlara dogrulama adimi; sonra kalan kalem.
- Maliyet $ olculemedi; 10 uretici ~0,2M, 4 hakem ~0,5M Haiku jeton. Push yok.

# TUR 16 (29 Eki)
- Kaynak-kanit kapisi eklendi (usta_kart.py): istem kanit_tuzak/kanit_token ister; isle() kaynakta birebir bulunmayan tuzak/token_ipucu'nu "Kaynakta belirtilmemis." yapar. 9 ret karti (tur 15'in 7'si + productivity/sports) yeniden uretildi.
- Sonraki 120 kalem 5 Haiku uretici ile uretildi; usta.jsonl 651. Kalan kartsiz ~6228. Kanitli token_ipucu 28/120 (92'sinde kanit yok -> "belirtilmemis").
- Hakem (4 bagimsiz Haiku, tam kaynak parcalari; 40 yeni + 9 yeniden uretilen = 49): 41/49 = %84 < %98 KAPI TUTMADI. Retler: supabase-postgres-best-practices, sentry-instrument-logging, setup-gbrain, ship, n8n-expression-syntax, spec, mukul975-zero-trust-paket, davila7-productivity-paket. Kok: kullanim satirlarinda kosul dusurme/genel paket yonlendirmesi; kanit kapisi yalniz tuzak/token'i kapsiyor, kullanim ve ornek'i degil.
- Sonraki tur: kanit kapisini kullanim+ornek'e genislet (kosullu iddialarda kosulu alintiya bagla), paket kartlarini kart yerine "paket yonlendirmesi" isaretle; 8 reti duzelt; sonra olcekle. Maliyet $ olculemedi (~13 Haiku ajan, ~1,4M jeton). Push yok.

# TUR 17 (29 Eki)
- Kanit kapisi kullanim maddelerine genisletildi (usta_kart.py: kanit_kullanim, kaynakta birebir yoksa madde dusurulur; kosul-dusurme ve paket uydurma yasagi istemde). 8 ret karti (tur 16 listesi) Haiku ile yeniden uretildi, usta.jsonl 651.
- Bagimsiz hakem KOSULMADI (tur siniri); %98 kapi bu 8 kart icin olculmedi. Olcekleme yapilmadi (kapi tutmadan 400-500 parti yok). Maliyet $ olculemedi (1 Haiku ajan ~110k jeton). Push yok.

# TUR 18 (30 Eki)
- Bagimsiz hakem (4 Haiku, tam kaynak; tur 17'nin 8 yeniden uretilen karti + 32 rastgele, seed 18): 35/40 = %87,5 < %98 KAPI TUTMADI. Tur 17 kartlari 8/8 gecti; 5 ret hepsi kapi oncesi eski kartlar (cloudflare-one-migrations, davila7-marketing-paket, pinecone-docs, netlify-agent-runner, mukul975-cryptography-paket).
- 5 ret karti Haiku ile yeniden uretildi (usta.jsonl 651); marketing ('Xquik' REST API) ve cryptography (kaynaksiz 'TALIMAT sirayla' tuzagi) elle yamandi. Yeniden hakeme sokulmadi. Kok: kanit kapisi sonrasi uretilmeyen eski kartlar. Sonraki tur: eski ~600 karti kanit kapisindan gecir (betikle kullanim/tuzak alinti kontrolu), sonra olcekle. Maliyet $ olculemedi (~10 Haiku ajan). Push yok.

# TUR 19 (30 Eki)
- Betik denetimi (tuzak/token_ipucu/kullanim'daki komut, bayrak, kod adi kaynakta var mi): 674 kartta tek supheli (agentation token_ipucu) -> "Kaynakta belirtilmemis." yapildi.
- Bagimsiz hakem (4 Haiku, seed 19, 40 rastgele kart, kaynak ilk 6000 kr): 26/40 = %65 < %98 KAPI TUTMADI. Ret 14: sentry-svelte-sdk, gemini-omni-flash-api (ikisi elle yamandi), swift-concurrency, baoyu-cover-image, canary, mukul975-threat-intelligence-paket, baoyu-image-gen, 3d-metal-material, n8n-mcp-skills, mukul975-data-protection-paket, premiere-mcp-paket, auditor-reunioes, horizontal-scroll-scenes, sentry-python-sdk.
- Kok siniflari: (a) sayi/olcu uydurma (6 boyut, 13 bolum, 0,1 ms, DPR ms), (b) kosul dusurme (tek/yalniz), (c) kaynak hakemde kesik oldugu icin dogrulanamayan (~5 ret: "kesik" notu) -> hakem gurultusu. Dize eslesmesi sayi/olcu ve nicelik sozcuklerini yakalamiyor.
- Sonraki tur: kapiya sayi/olcu denetimi (kartta gecen her rakam kaynakta olmali), hakemi tam kaynakla kos, 12 reti yeniden uret. Maliyet $ olculemedi (~4 Haiku hakem ~220k jeton). Push yok.
