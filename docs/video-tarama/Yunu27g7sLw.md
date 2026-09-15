# Fable 5 vs Opus 4.8: Web Sitesi Testi! Devrim mi, Pazarlama mı?
kanal: Yıldız Dikme · süre: 12 dk · altyazı: otomatik tr
ana iddia: Aynı kısa prompt ve aynı 3 screenshot'la Fable 5, animasyonlu parçacık referansını (imleç dairesi, bulutsu yapı) Opus 4.8'den iyi okudu; yazara göre "4-5 adım ileride" (ASR "45") ama devrim değil, abartı pazarlama (tek deneme gösterildi, ölçüm yok; "her denediğimde" iddiası kanıtsız).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| vercel/next.js + microsoft/TypeScript | YENİ | ELENDİ | promptta verilen tek teknik bilgi (ASR "NextJGS ve Type Script"); proje stack'i, ortam aracı değil; frontend-craft static/aspnet hedefliyor |
| mrdoob/three.js | YENİ | ELENDİ | Opus 4.8 parçacık yapısını Three.js'e kurdu (ASR "3GS"), açıklamada #threejs; proje bağımlılığı, Bölüm 3 "gereksiz kütüphane yok" ile gerilimli |
| hareketli referansta "statik görsel değil, parçacık efekti var" diye açıkça yaz | YENİ | BİLGİ | "yoksa onu bir görsel sanabilir" (sözlü); Bölüm 0 REF modu referanstaki hareketi ayrıca ele almıyor |
| hareketi aynı öğenin farklı durumlarını gösteren çoklu screenshot ile ilet | YENİ | BİLGİ | 3 kare: imleç dairesi farklı konumda, bulut uzun/toplanmış; mouse etkileşimi yazılmadan Fable 5 daireyi yakaladı, Opus 4.8 yakalayamadı (tek deneme) |
| diğer: "referansa bağlı kal, tasarımı değiştirme" · tüm cihazlara uyumlu · "hata çıkarsa sen çöz" | ZATEN VAR | ELENDİ | Bölüm 0 (REF iyileştirilmez) · Bölüm 2 (390/768/1440) · Bölüm 9 (kapalı çevrim); Opus 4.8 bu kısıta rağmen tasarımı değiştirdi |
| kısa, teknik olmayan prompt: detayı ve teknolojiyi modele bırak ("her detayı sen kendin seç") | YENİ | ELENDİ | Bölüm 0 marka kararı ve Bölüm 7-8 açık karar disipliniyle çelişir; Fable 5'te bile bulut dağınık, 3-4 ek prompt gerektiği söyleniyor (ASR "34") |
| aynı prompt+screenshot'ı iki modele ayrı klasör ve port (3000/3001) ile verip yan yana karşılaştırma | YENİ | ELENDİ | model seçimi deneyi, kural/araç değil; "birden fazla denemek lazım" deniyor ama tek deneme gösteriliyor |
## ölçütler (YENİ)
- vercel/next.js, microsoft/TypeScript, mrdoob/three.js: bakım=üçü de pushed 2026-09-15, arşivli değil (next.js 142.3k, TypeScript 111.1k, three.js 115.6k yıldız) · çift=örtüşme yok (context7 MCP yalnız dokümanlarını sorgular) · izin=projeye npm bağımlılığı · context=0 (ortama yüklenmez) · kurulum: —
- teknikler (statik değil notu, çoklu durum screenshot'ı, kısa prompt, iki model yan yana): bakım=— (teknik) · çift=örtüşme yok (Bölüm 0 REF hareketi kapsamıyor; Bölüm 11 üç yön üretir, model karşılaştırmaz) · izin=yok (yan yana test ikinci model erişimi ister; Fable 5'in API'de ayrı ücretli olacağı iddiası) · context=yalnız kural satırı · kurulum: —
## hedefler (BİLGİ)
- Hareketli/etkileşimli referansta screenshot'ın yanına "statik değil" notu ve davranış tarifi (parçacık, imleç etkileşimi) yazılır → frontend-craft Bölüm 0 (REF modu)
- Hareket, aynı öğenin farklı durumlarını gösteren birden çok screenshot ile verilir (videoda 3 kare) → frontend-craft Bölüm 0 (REF modu)
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda
- ekran görüntülerine sadık kal; tasarımı değiştirme, referansa bağlı kal (sözlü özet, birebir değil)
- Next.js ve TypeScript ile yap; teknik olarak başka hiçbir şey söylenmedi (sözlü özet, birebir değil)
- statik/sabit bir görsel yapma; partiküllü efekt var, ona bağlı kal (sözlü özet, birebir değil)
- hepsini smooth yap; her detayı sen kendin seç, referans görsele bağlı olarak teknolojiyi de kendin seç (sözlü özet, birebir değil)
- tüm cihazlara uyumlu yap; hata çıkarsa sen çöz (sözlü özet, birebir değil)
- mouse etkileşimi prompta yazılmadı, yalnız screenshot'lardaki daire konum farkıyla gösterildi (sözlü özet, birebir değil)
- takip: 3.000 portunda çalıştırır mısın (sözlü)
referans siteler: yok (referans, yazarın freelance müşteri projesindeki kendi animasyonlu sitesi; adı/URL geçmiyor)
stiller: parçacıklı (particle) tasarım, yapay zekadan esinlenen bulutsu yapı, dalga efekti, cursor-reactive particle ve 3D (açıklama)
premium kararlar:
1) Parçacıklardan oluşan bulutsu yapı; belirli aralıklarla gelen dalga efektiyle parçacıklar yayılıyor ve bulut formu değişiyor (uzun / toplanmış)
2) Mouse etkileşimi: imleç çevresinde dairesel boşluk ("kare delik gibi" deniyor) oluşuyor ve damlacıkları kendine doğru çekiyor
3) videoda yok
