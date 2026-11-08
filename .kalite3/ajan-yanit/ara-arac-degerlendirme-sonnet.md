Yeni bir geliştirici aracını benimsemeden önce nasıl değerlendiriyorum

Soru ve ölçüt: Aracın hangi somut ihtiyacı karşılayacağını ve neyi ölçeceğimi baştan yazarım. Örnek: "X dakikayı Y'ye indirir", mevcut çözüm ve "hiçbir şey yapmamak" ile karşılaştırılır. Sıra, ucuz ve eleyici kontrolden pahalı olana doğrudur.

Kontrol sırası ve toplanacak kanıt:
1. İhtiyaç ve alternatifler. Kanıt: yazılı ihtiyaç cümlesi, 2-3 alternatif ve mevcut araçla fark.
2. Lisans (eleyici). MIT/Apache-2.0 gibi izin verici lisanslarda yalnızca telif ve lisans bildirimi korunur. GPL/AGPL gibi copyleft lisanslar türev işi aynı lisansla açmayı gerektirir (AGPL ağ üzerinden hizmette de). Kanıt: LICENSE dosyası. MIT/Apache değilse koşulları rapora yazarım. Kaynak: https://choosealicense.com/licenses/
3. Bakım ve sağlık. OpenSSF Scorecard şu kontrolleri 0-10 puanlar: Maintained, License, Vulnerabilities (OSV'ye göre), Code-Review, Pinned-Dependencies, Signed-Releases, Security-Policy, Dependency-Update-Tool. Kanıt: Scorecard çıktısı, son commit/release tarihi, açık güvenlik sorunları. Kaynak: https://github.com/ossf/scorecard
4. Güvenlik ve yetki. Hangi izinleri ve sırları istiyor, ağa ne gönderiyor, kurulum betiği ne çalıştırıyor? Kanıt: izin listesi ve bağımlılık ağacı. Bu kontrolü kaynak kodu okuyarak yaparım.
5. Kurulum ve uyum. Hedef platformda (ör. Windows) temiz kurulum çalışıyor mu, mevcut yığına uyuyor mu? Kanıt: izole ortamda kurulum kaydı.
6. Küçük deneme (pilot). Gerçek bir işte, süre ve çıktı kalitesi ölçülür, ihtiyaç cümlesindeki ölçütle karşılaştırılır. Kanıt: önce/sonra sayıları.
7. Karar. Benimse, reddet ya da süreli dene. Çıkış planı (aracı kaldırınca ne kırılır) da yazılır.

Çapraz doğrulama: Her iddia için en az iki bağımsız kaynak ararım: resmî doküman ve repo, artı üçüncü taraf (issue'lar, bağımsız yorumlar). Çelişki varsa birincil ve güncel kaynağa güvenirim.

Maliyet: Lisans, bakım ve güvenlik kontrolleri neredeyse ücretsizdir ve eleyicidir. Kurulum ve pilot kısmı mühendis saati ister. Kısa tutmak için ilk üç adımda elenen aracı pilota sokmam.

Risk: Tedarik zinciri (kötü niyetli paket veya betik), lisans yükümlülüğü, terk edilmiş proje (kilitlenme) ve gizli maliyet (token, abonelik, bakım yükü).

Atladığım ve doğrulamadığım şeyler: Phoenix research-pipeline skill'i yüklendi ama güvenlik içerik araştırması için olduğundan çalıştırmadım. Sadece iki kaynağı (Scorecard README ve choosealicense) WebFetch ile doğruladım. 4-7. adımlar genel pratiğimdir, kaynak linki yok. Bunlar doğrulanmış iddia sayılmamalı.

Kaynaklar:
- https://github.com/ossf/scorecard
- https://choosealicense.com/licenses/