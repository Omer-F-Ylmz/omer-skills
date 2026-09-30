# Emil Kowalski motion skill
ad: Emil Kowalski motion skill
tur: skill
video: 0JZtdAtJiyk
repo: emilkowalski/skills
lisans: bilinmiyor (repoda LICENSE dosyası var ama içeriği okunamadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/emilkowalski/skills
telemetri: Skill dosyalarının kendisinde telemetri görmedim (yalnızca metin). Kurulum CLI'ı (skills.sh) kurulum sayısı tutuyor olabilir, doğrulanmadı. README'de skills.sh rozeti ve bülten kaydı bağlantısı var.
yildiz: bilinmiyor (bir arama sonucu ~35 bin yıldız ve ~250 bin kurulum diyor, doğrulanmadı)
alt_tur: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short)
## Ne
Emil Kowalski'nin (Vercel ve Linear geçmişi olan tasarım mühendisi) animasyon ve arayüz kalitesi için yazdığı Claude Code skill koleksiyonu. Ajanların animasyonlarda yaptığı küçük hataları listeler ve nasıl düzeltileceğini anlatır. Örnek hatalar: giriş animasyonunda ease-out yerine ease-in seçmek, yarı saydam gölge yerine düz kenarlık kullanmak. Videodaki "tek komutla gerçek hareket, bilinçli easing" iddiası bu koleksiyona uyuyor.
## Mekanizma
Her biri ayrı bir SKILL.md dosyasından oluşur. Bunlar ajanın bağlamına yüklenen kural ve öneri metinleridir. Kod çalıştırmazlar. Ajan, UI kodu yazarken ya da incelerken bu kurallara göre eğri, süre ve property seçer. Skill'ler şunlar: emil-design-eng (ana skill), animate, animate-expo, review-animations, improve-animations, find-animation-opportunities, animation-vocabulary, apple-design, write-swift, pick-ui-library, prototype, mobile-native, ask-sonner. Repoda ayrıca performance-cheatsheet.md var.
## Kanıt
- Tek komutla gerçek hareket, bilinçli easing ve anlamlı animasyon ekler (video, 0:30) → doğrulandı · README, animate skill'ini 'doğru eğri, süre ve property seçerek sıfırdan animasyon kurar' diye tanımlıyor. Easing hatalarının düzeltilmesi de 'Why use it?' bölümünde anlatılıyor. Tek komutla kurulum: npx skills@latest add emilkowalski/skills. Gerçek çıktı kalitesini çalıştırıp denemedim.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- npx skills@latest add emilkowalski/skills
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanın ürettiği animasyonların kalitesini artırır: doğru easing, süre ve property seçimi, mobil ve performans ince ayarları. Ayrıca mevcut animasyonları denetler ve animasyon eklenecek yerleri bulur.
## Maliyet/risk
Lisans belirsiz, yeniden dağıtmadan önce LICENSE dosyasını okumak gerekir. Kurallar yazarın kendi görüşüdür. Skill'ler bağlamı şişirir. Üçüncü taraf `npx` paketiyle kurulum yapılıyor, önce SKILL.md içeriği okunmalı. Videodaki mockup sitesinin (insiderforce.io) bu repoyla bağı doğrulanmadı.
## Tasarruf
Token aracı değil. Skill metinleri bağlama yük ekler. Tasarruf ancak yeniden çalışma turlarının azalmasından gelir, ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: Doğrudan kurulabilir, yeniden yazmaya gerek yok. Kendi sürümümüz için: skills/ altına SKILL.md aç. İçine easing kuralları (giriş için ease-out, ekran içi hareket için ease-in-out), süre aralıkları, yalnızca transform ve opacity animasyonu, prefers-reduced-motion desteği ve bir denetim kontrol listesi yaz. Bunları Emil'in yayımlanmış yazılarından (emilkowal.ski/ui/7-practical-animation-tips) kendi cümlelerimizle özetle. Metni kopyalamadan önce lisansı kontrol et.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short/panel.md → Ömer sütunu
## Özellikler
### emil-design-eng: ağırlıklı animasyon, biraz da tasarım tavsiyesi içeren ana skill
kaynak: https://github.com/emilkowalski/skills
### animate: doğru eğri, süre ve property ile animasyonu sıfırdan kurar
kaynak: https://github.com/emilkowalski/skills
### review-animations: animasyonları katı kurallara göre inceler
kaynak: https://github.com/emilkowalski/skills
### improve-animations: kod tabanını tarar, öncelikli ve bağımsız planlar üretir
kaynak: https://github.com/emilkowalski/skills
### find-animation-opportunities: hareketten fayda görecek yerleri ve animasyon eklenmemesi gerekenleri söyler
kaynak: https://github.com/emilkowalski/skills
### animate-expo, mobile-native, apple-design, animation-vocabulary, pick-ui-library, prototype, ask-sonner, write-swift yan skill'leri
kaynak: https://github.com/emilkowalski/skills
## Destek
- 0JZtdAtJiyk · 0:30 · Tek komutla gerçek hareket, bilinçli easing ve anlamlı animasyon ekler. · kanıt: Karede 'intentional easing' ve 'animations that actually make sense' listeleniyor. (karede: 'Directed by Shawn Levy' başlıklı koyu/açık siyah-beyaz web sitesi mockup'ı; altında 'intentional easing' ve 'animations that actually make sense' maddeleri, en altta insiderforce.io.)
