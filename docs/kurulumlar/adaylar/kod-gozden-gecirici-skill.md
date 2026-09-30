# Kod gözden geçirici skill
ad: Kod gözden geçirici skill
tur: skill
video: kMk4pvFJ13s
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Yok; salt talimat dosyası. Skill'in kendisi ağ erişimi yapmaz. (Kaynak görülemedi, varsayım.)
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-01-uzun)
## Ne
Kodu değiştirmeden; biçim, okunabilirlik, isimlendirme ve performans kontrol listesiyle inceleyen, yalnızca sorun raporlayan bir Claude skill'i. Video "5 Claude Skills That Will Be Worth $500K/Year by 2027" başlıklı (kMk4pvFJ13s).
## Mekanizma
Videodaki bulguya göre skill talimatı: kodu yeniden yazma, değişken adlarını veya mantığı değiştirme, yalnızca sorunları raporla. Kontrol listesi dört eksende (biçim, okunabilirlik, isimlendirme, performans) kodu tarar ve bulguları rapor eder. Ayrıntılı SKILL.md içeriği doğrulanamadı; video sayfasından yalnızca başlık alınabildi, transkript gelmedi.
## Kanıt
- Skill kodu yeniden yazmadan biçim, okunabilirlik, isimlendirme ve performans kontrol listesiyle inceler. → sınanamadı · Yalnızca video bulgusundaki alıntı var: 'Do not rewrite the code, or do not change variable names or logic, or only report issues.' Sayfa getirme çıktısı yalnızca başlık ve altbilgi bağlantıları içeriyordu; transkript yok.
- Bu skill'ler 2027'ye kadar yılda 500 bin dolar değerinde olacak. → sınanamadı · Yalnızca video başlığında geçiyor; dayanak yok, doğrulanabilir değil.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Repo yok; hazır kurulum bilinmiyor.
- Kendi SKILL.md dosyanı .claude/skills/kod-gozden-gecirici/ altına koyarak kullanabilirsin.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Kod inceleme çıktısını salt rapora sınırlar; model kodu istenmeden yeniden yazmaz, böylece diff kirliliği ve istenmeyen mantık değişikliği önlenir.
## Maliyet/risk
Kaynak repo yok, içerik yalnızca videodaki kısa alıntıya dayanıyor; doğrulanamadı. Başlık "$500K/yıl" iddiası pazarlama abartısı gibi görünüyor. Kontrol listesi genel kalırsa yüzeysel bulgular üretebilir.
## Üretilebilir
hedef_tur: skill
tarif: SKILL.md oluştur. Frontmatter: name: kod-gozden-gecirici, description: 'Kod incelemesi istendiğinde kullan; kodu değiştirmeden yalnızca rapor verir'. Gövde: (1) Kural: kodu yeniden yazma, isim veya mantık değiştirme, dosya düzenleme; yalnızca sorun raporla. (2) Kontrol listesi: biçim (girinti, satır uzunluğu, tutarlılık), okunabilirlik (uzun fonksiyon, iç içe yapı, yorum), isimlendirme (anlamlı, tutarlı), performans (gereksiz döngü, tekrarlı hesap, N+1). (3) Çıktı biçimi: dosya:satır, önem (yüksek/orta/düşük), sorun, kısa öneri metni (kod yazmadan). allowed-tools'u Read, Grep, Glob ile sınırla ki düzenleme yapılamasın.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-01-uzun/panel.md → Ömer sütunu
## Özellikler
### Salt raporlama modu: kodu yeniden yazmaz, değişken adlarını ve mantığı değiştirmez.
kaynak: https://www.youtube.com/watch?v=kMk4pvFJ13s
### Biçim, okunabilirlik, isimlendirme ve performans kontrol listesi.
kaynak: https://www.youtube.com/watch?v=kMk4pvFJ13s
## Destek
- kMk4pvFJ13s · 5:33 · Kodu yeniden yazmadan biçim, okunabilirlik, isimlendirme ve performans kontrol listesiyle inceler. · kanıt: Do not rewrite the code, or do not change variable names or logic, or only report issues.
