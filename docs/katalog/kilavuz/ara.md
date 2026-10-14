# ara — 18 benzersiz kayıt

**Amaç:** Araştırma ajanları: araç/kütüphane/repo değerlendirme, lisans kontrolü, kaynaklı kanıt toplama, doküman arama, web/sosyal platform okuma ve video özeti.

**İç yapı:** Tümü [ajan], ad kalıbı ara-<iş>; gruplar: seçim/değerlendirme (arac-degerlendirme, kutuphane-secimi, repo-karsilastirma, teknoloji-secimi, lisans-kontrol), kanıt (kanit-toplayici, celiskili-kaynak-uzlastirma, dosya-sorusturmaci), okuma (defuddle-sayfa-cikarim, platform-okuma, youtube-ozet, web-kazima), yerel kod (graphify-sorgu, dokuman-indeksle).

## En güçlü parçalar
- `ara-kanit-toplayici` — Sınırlı tek soru için kaynaklı kanıt toplar; olgu, çıkarım ve belirsizliği ayırır.
- `ara-lisans-kontrol` — Dış kodu almadan önce repo lisansını okur, izinli kullanımı belirtir.
- `ara-arac-degerlendirme` — Yeni araç ya da MCP'yi ihtiyaç, maliyet, güvenlik ve alternatiflere göre tartar.
- `ara-graphify-sorgu` — Kod tabanı sorularını ham okuma yerine graphify query/path/explain ile yanıtlar.
- `ara-kutuphane-dokuman` — Güncel kütüphane dokümanından tam API, sürüm, örnek ve deprecation bilgisini bulur.
- `ara-celiskili-kaynak-uzlastirma` — Çelişen kaynakları bağımsızlık, güncellik ve birincil/ikincil ayrımıyla derecelendirir.

## Birlikte kullanım
- ara-repo-karsilastirma → ara-lisans-kontrol → ara-yeni-arac-kurulum-arastirma: dış repo benimseme akışı.
- ara-kanit-toplayici + ara-celiskili-kaynak-uzlastirma: kaynak çelişkisinde iddia derecelendirme.
- ara-defuddle-sayfa-cikarim / ara-platform-okuma ile web içeriği az jetonla okunur.

## Tuzaklar
- ara-web-kazima robots kuralı ve rate limit planlar; kurallar atlanarak kazıma yapılmamalı.
- Örtüşen seçiciler: ara-kutuphane-secimi, ara-repo-karsilastirma, ara-teknoloji-secimi ve ara-arac-degerlendirme; soru kapsamına göre tek biri seçilmeli.

## Üyeler
- ajan (18): ara-arac-degerlendirme, ara-celiskili-kaynak-uzlastirma, ara-defuddle-sayfa-cikarim, ara-dokuman-indeksle, ara-dosya-sorusturmaci, ara-graphify-sorgu, ara-kanit-toplayici, ara-kutuphane-dokuman, ara-kutuphane-secimi, ara-lisans-kontrol, ara-ogrenme-plani, ara-platform-okuma, ara-repo-karsilastirma, ara-teknoloji-secimi, ara-trend-analizi, ara-web-kazima, ara-yeni-arac-kurulum-arastirma, ara-youtube-ozet
