# Emil Kowalski skill
ad: Emil Kowalski skill
tur: skill
video: BK9P0rYIQY8
repo: emilkowalski/skills
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/emilkowalski/skills
telemetri: Skill'lerin kendisinde telemetri bulgusu yok, çünkü yalnızca markdown talimatıdır. Ancak README'deki skills.sh rozeti ve `npx skills` CLI'ı kurulum sayısı toplayabilir (Skillselion'daki install sayıları buna işaret ediyor). CLI telemetrisi doğrulanmadı, bilinmiyor.
yildiz: ~35 bin (yalnızca Skillselion sayfasına göre, doğrudan doğrulanmadı)
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short)
## Ne
Emil Kowalski'nin (Vercel/Linear tasarım mühendisi, Sonner ve Vaul yazarı) arayüz animasyonu ve tasarım tecrübesini agent skill olarak paketleyen koleksiyon. Ajanların sık yaptığı zevksiz hataları (enter animasyonunda ease-in, yanlış süre, düz kenarlık yerine yarı saydam gölge vb.) listeler ve düzeltmelerini anlatır. 13 skill içerir: emil-design-eng (ana skill), animate, animate-expo, review-animations, improve-animations, find-animation-opportunities, animation-vocabulary, apple-design, write-swift, pick-ui-library, prototype, mobile-native, ask-sonner.
## Mekanizma
Kod çalıştırmaz. Her skill bir SKILL.md (talimat + kural listesi) dosyasıdır. Ajan bağlama uygun skill'i yükler ve içindeki karar çerçevesine uyar. Arama sonuçlarına göre emil-design-eng sırayla dört soru sorar: animasyon gerekli mi, amacı ne, hangi easing, hangi süre. Kullanıcı tetiklediği şeyde ease-out varsayılandır, UI'de ease-in kullanılmaz, özel easing sabitleri kullanılır ve zorunlu bir Before/After inceleme tablosu üretilir. Ek skill'ler sıfırdan animasyon kurar, mevcut animasyonları denetler, önceliklendirilmiş uygulanabilir planlar çıkarır ve nerede animasyon yapılmaması gerektiğini söyler.
## Kanıt
- Claude'a gerçek hareket ve doğru easing ekletir, animasyonları anlamlı yapar (videolar). → sınanamadı · Çıktı kalitesi çalıştırılıp denenmedi. README, skill'lerin ajan hatalarını (ease-in enter vb.) listelediğini doğruluyor ama sonuç kalitesini ölçmüyor.
- Tek komutla kurulur. → doğrulandı · README: `npx skills@latest add emilkowalski/skills`.
- Repo mevcut ve birden çok animasyon skill'i içeriyor. → doğrulandı · `video repo emilkowalski/skills` çıktısı: skills/ altında animate, review-animations, improve-animations, emil-design-eng vb. dizinler.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- npx skills@latest add emilkowalski/skills
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude'un ürettiği UI'daki hareketi daha bilinçli yapar: doğru easing, süre ve animasyon yapılacak/yapılmayacak yerler. Her iki videoda da "gerçek hareket, doğru easing, anlamlı animasyon" faydası öne çıkıyor. Ayrıca mevcut kodu denetleme ve mobil/Expo desteği var.
## Maliyet/risk
Lisans türü doğrulanamadı (LICENSE dosyası var, içeriği okunmadı). Ticari kullanımdan önce kontrol edilmeli. `npx skills@latest` her seferinde en son sürümü çeker, sürüm sabitlenmiyor. Kurulmadan önce SKILL.md içerikleri gözden geçirilmeli, çünkü ajan talimatı olarak çalışırlar. Skill'ler görüşe dayalıdır (Emil'in zevki) ve her projeye uymayabilir. Skill'leri yüklemek bağlam tüketir. Videolar tanıtım niteliğinde, iddialar bağımsız test edilmedi.
## Tasarruf
Token tasarrufu aracı değil. Aksine skill içeriği bağlama token ekler. Dolaylı kazanç: yanlış animasyonu tekrar tekrar düzeltme turlarını azaltmak.
## Üretilebilir
hedef_tur: skill
tarif: Kendi skill'imizi yazabiliriz, kod gerekmez. (1) Lisansı doğrula, izin varsa doğrudan kur, yoksa yeniden yaz. (2) Kendi SKILL.md'mizi oluştur: 4 soruluk karar akışı (animasyon gerekli mi, amaç, easing, süre), varsayılan ease-out, UI'de ease-in yasağı, yalnızca transform/opacity animasyonlama, prefers-reduced-motion saygısı, Before/After tablo şablonu. (3) İsteğe bağlı 'review-animations' alt skill'i ile CSS/JS kodunda transition/animation grep denetimi ekle. Orijinal içeriği kopyalamadan kendi ifademizle yaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short/panel.md → Ömer sütunu
## Özellikler
### emil-design-eng: ana skill, animasyon ağırlıklı tasarım kuralları
kaynak: https://github.com/emilkowalski/skills
### animate: doğru eğri, süre ve özelliklerle sıfırdan animasyon kurar
kaynak: https://github.com/emilkowalski/skills
### review-animations ve improve-animations: katı inceleme ve kod tabanı denetimi, önceliklendirilmiş planlar
kaynak: https://github.com/emilkowalski/skills
### find-animation-opportunities: animasyona değer yerleri ve animasyon yapılmaması gerekenleri bulur
kaynak: https://github.com/emilkowalski/skills
### animate-expo, mobile-native, apple-design: React Native/Expo, mobil web ve Apple ilkeleri
kaynak: https://github.com/emilkowalski/skills
### pick-ui-library, prototype, ask-sonner, write-swift, animation-vocabulary yardımcı skill'leri
kaynak: https://github.com/emilkowalski/skills
## Destek
- BK9P0rYIQY8 · 0:05 · Claude'a gerçek hareket ve doğru easing ekleterek düz görünümü giderir. · kanıt: Claude real motion with proper easing. Animations that actually feel intentional.
- bAhPV1Sl-rg · 0:06 · Tek komutla Claude'a gerçek hareket, easing ve anlamlı animasyon ekletir. · kanıt: Claude starts adding real motion, proper easing, and animations that actually make sense.
