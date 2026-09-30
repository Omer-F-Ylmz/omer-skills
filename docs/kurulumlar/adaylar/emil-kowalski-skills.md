# Emil Kowalski skills
ad: Emil Kowalski skills
tur: skill
video: Ysr7oNDajJI
repo: emilkowalski/skills
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/emilkowalski/skills
telemetri: Skill dosyalarında telemetri gördüğüm bir şey yok, ama içeriklerin tamamını okumadım. Kurulum `npx skills@latest` ile yapılıyor. skills CLI'ının kendi kullanım istatistiği toplayıp toplamadığını doğrulamadım (README'de skills.sh rozeti var). Bülten kaydı isteğe bağlı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: SkillSpector --no-llm taramasında 8 HIGH/CRITICAL bulgu çıktı. Ayrıntıları incelenmedi. LLM'siz taramada yanlış pozitif olabilir.
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Vercel ve Linear deneyimine dayanan, arayüz animasyonu ve tasarım mühendisliği için 13 agent skill'lik bir set. Ajanların sık yaptığı küçük tasarım hatalarını listeler ve nasıl düzeltileceğini anlatır. Örnekler: giriş animasyonunda ease-out yerine ease-in seçmek, yarı saydam gölge yerine düz kenarlık kullanmak. Skill'ler: emil-design-eng, animate, animate-expo, review-animations, improve-animations, find-animation-opportunities, animation-vocabulary, apple-design, write-swift, pick-ui-library, prototype, mobile-native, ask-sonner. Videoda "dokuz skill" deniyor. Repoda 13 skill klasörü var, yani sayı uyuşmuyor. Video muhtemelen daha eski bir sürümü anlatıyor.
## Mekanizma
Her skill, skills/<ad>/SKILL.md dosyasından oluşan bir talimat ve bilgi paketi. Ajan ilgili görevde (animasyon yazma, inceleme, denetim vb.) skill'i yükler ve içindeki kurallara göre eğri, süre, özellik seçer. Çalıştırılabilir kod yok gibi görünüyor, ama bunu doğrulamadım. Kökte performance-cheatsheet.md var. Kurulum skills CLI ile yapılıyor.
## Kanıt
- Videoda geçen 'dokuz skill' iddiası → çürütüldü · Repo README'si 13 skill listeliyor ve skills/ altında 13 klasör var. Video eski bir sürümü anlatıyor olabilir.
- Repoda Emil design engineering ve Animate skill'leri var → doğrulandı · README'de emil-design-eng ve animate girişleri var, ağaçta skills/emil-design-eng ve skills/animate klasörleri görünüyor.
- Apple design ve animation vocabulary skill'leri var → doğrulandı · README'de apple-design ve animation-vocabulary listeleniyor, ağaçta klasörleri var.
- Skill'ler ajanların animasyon hatalarını düzeltir → sınanamadı · Yalnızca README anlatımı var. Bir ajan çıktısı üzerinde denemedim.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 8
## Kurulum
- npx skills@latest add emilkowalski/skills
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajan çıktısında animasyon ve arayüz kalitesini yükseltir. Skill'ler bir inceleme (review-animations), denetim (improve-animations) ve fırsat bulma (find-animation-opportunities) akışı sağlar. Mobil (animate-expo, mobile-native) ve Swift desteği de var.
## Maliyet/risk
1) Lisans türü doğrulanmadı. LICENSE dosyası var ama içeriğine bakmadım. Kopyalamadan veya yeniden dağıtmadan önce kontrol edilmeli. 2) Ön tarama SkillSpector --no-llm ile 8 HIGH/CRITICAL bulgu verdi. Bulguların ayrıntısını görmedim. LLM'siz tarama markdown içeriğinde yanlış pozitif verebilir, ama kurmadan önce bulgular incelenmeli. 3) Skill'ler görüşe dayalı ve katı kurallar içeriyor, projenin tasarım diline uymayabilir. 4) Video ile repo arasında skill sayısı farkı var (9 ve 13).
## Tasarruf
Token aracı değil. Ajanın tekrar denemesini ve yanlış animasyonu düzeltme turlarını azaltarak dolaylı olarak token harcamasını düşürebilir, ama bu ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: Kendi arayüz skill'imizi aynı yapıda yazabiliriz: skills/<ad>/SKILL.md içinde 'ajanın sık yaptığı hata → doğru yaklaşım' çiftleri. Örnekler: giriş için ease-out, çıkış için ease-in, transform ve opacity dışı özellikleri animasyonlamama, süre aralıkları, prefers-reduced-motion. Ayrıca bir inceleme skill'i (kuralları kod tabanında tarayıp öncelikli plan çıkarır) ve bir animasyon sözlüğü skill'i eklenebilir. Doğrudan kopyalamak yerine, lisans doğrulanana kadar kuralları kendi ifademizle yazmak daha güvenli.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### emil-design-eng: animasyon ağırlıklı ana skill, biraz tasarım tavsiyesi de içerir
kaynak: https://github.com/emilkowalski/skills
### animate: doğru eğri, süre ve özellikleri seçerek sıfırdan animasyon kurar
kaynak: https://github.com/emilkowalski/skills
### review-animations ve improve-animations: kurallara göre katı inceleme ve kod tabanı denetimi, öncelikli planlar üretir
kaynak: https://github.com/emilkowalski/skills
### find-animation-opportunities: hareketten fayda görecek yerleri ve animasyon eklenmemesi gereken yerleri gösterir
kaynak: https://github.com/emilkowalski/skills
### animation-vocabulary: yapay zekaya doğru terimlerle animasyon tarif etmeyi öğretir
kaynak: https://github.com/emilkowalski/skills
### apple-design: WWDC tasarım konuşmalarından damıtılmış ilkeler, web'e uyarlanmış
kaynak: https://github.com/emilkowalski/skills
### mobile-native: web uygulamasını telefonda yerel hissettirir (100vh hatası, tap highlight, safe area vb.)
kaynak: https://github.com/emilkowalski/skills
### pick-ui-library ve prototype: güvenilir kütüphane seçimi ve çoklu UI varyantı prototipi
kaynak: https://github.com/emilkowalski/skills
## Destek
- Ysr7oNDajJI · 1:10 · 9 skill'lik set; Apple design, animation vocabulary, Emil design engineering ve Animate öne çıkıyor. · kanıt: there are not one but nine skills and each one changes a different part
