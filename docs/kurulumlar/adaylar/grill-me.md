# grill-me
ad: grill-me
tur: skill
video: EJyuu6zlQCg
repo: mattpocock/skills
lisans: bilinmiyor (repoda LICENSE dosyası var, içeriği doğrulanamadı)
son_commit: bilinmiyor (repoda aktif changeset girdileri var)
arsiv: bilinmiyor
kaynak: https://github.com/mattpocock/skills
telemetri: Skill dosyasında telemetri yok, salt metindir. README'de telemetri beyanı görmedim. skills.sh yükleyicisinin kullanım istatistiği toplayıp toplamadığı doğrulanmadı, bilinmiyor. Kurulumdaki `npx` paketi ağ erişimi yapar.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-4)
## Ne
Kod yazmadan önce planı ya da tasarımı sorguya çeken bir agent skill'i. Kullanıcıyla ortak anlayışa varana kadar tasarım ağacının her dalı için sırayla soru sorar. Matt Pocock'un skills reposundaki skills/productivity/grill-me/SKILL.md dosyasıdır. Repo README'sine göre kod dışı kullanım içindir. Kod tabanlı sürümü grill-with-docs'tur. Başka repolarda (RobMitt, alirezarezvani, ericgandrade gibi) türev kopyaları var.
## Mekanizma
Saf prompt talimatıdır; kod, sunucu ya da bağımlılık içermez. Skill çağrılınca agent plan için karar ağacını çıkarır. Bağımlılıkları çözmek için dalları tek tek gezer ve her turda tek soru sorar. Soruyu kod tabanı yanıtlayabiliyorsa (Grep/Glob/Read ile) kullanıcıya sormadan kendisi bakar. Sorular kullanıcının henüz vermediği kararları, fark etmediği varsayımları ve kaçındığı ödünleşimleri ortaya çıkarmaya yöneliktir. Videodaki kanıt cümlesi: "Interview me relentlessly about every aspect of this plan until we reach a shared understanding." Repo tarafında soru aralarına yatay çizgi eklendiğini ve tire işaretlerinin kaldırıldığını gösteren changeset'ler var.
## Kanıt
- Skill, plan hakkında ortak anlayışa varana dek kullanıcıyı sorguya çeker. → doğrulandı · Video sayfası çıkarılamadı, ama arama sonuçları (gist, RobMitt/grill-me-skill, mcpmarket) aynı tanımı veriyor. Mattpocock/skills README'si de grilling session'ı 'agent'ın ne inşa ettiğini sana detaylı sorular sormasıdır' diye anlatıyor.
- Kod tabanından cevaplanabilen soruları kendisi araştırır. → doğrulandı · Arama özetleri, skill'in soru sormadan önce Grep, Glob ve Read ile kod tabanına baktığını belirtiyor. SKILL.md'yi doğrudan okumadım, bu yüzden ikinci el kanıt.
- Skill Matt Pocock'un reposunda bulunuyor. → doğrulandı · `video repo mattpocock/skills` README'si /grill-me'yi skills/productivity/grill-me/SKILL.md olarak bağlıyor ve 'non-code uses' için olduğunu söylüyor.
- Videoda geçen özet ve kanıt cümlesi ('Interview me relentlessly...'). → sınanamadı · `video getir` yalnızca YouTube sayfa iskeletini döndürdü, transkript yoktu. Video başlığı '5 Claude Code skills I use every single day' idi.
- Lisans, yıldız ve son commit bilgisi. → sınanamadı · Ağaçta LICENSE var ama içeriği okunmadı. Yıldız ve commit tarihi çıktıda yoktu.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code: `claude plugins install mattpocock-skills` (ya da oturum içinde `/plugin install mattpocock-skills`). Tüm seti salt okunur paket olarak kurar.
- Düzenlenebilir kopya için: `npx skills@latest add mattpocock/skills` çalıştırıp grill-me'yi seç. Dosyalar repona yazılır, güncelleme için `npx skills update` kullanılır.
- Plugin ve skills.sh'yi birlikte kurma. README'ye göre her skill iki kez kurulur.
- Tek skill yeterliyse skills/productivity/grill-me/SKILL.md dosyasını elle ~/.claude/skills/grill-me/ altına kopyalamak da olur. Bu yolu denemedim.
- Kullanım: `/grill-me` ile çağır ya da 'grill me' de.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Belirsiz isteklerde agent'ın varsayımla yanlış şey inşa etmesini önler. Kodla yanıtlanabilecek soruları kullanıcıya yüklemez. Tek soru ve tek tur düzeni karar vermeyi kolaylaştırır. Küçük, uyarlanabilir ve modelden bağımsız.
## Maliyet/risk
Düşük risk: kod çalıştırmayan bir prompt. Dikkat edilecekler: (1) Plugin ile kurulum salt okunurdur ve upstream değişince davranış kendiliğinden değişir. (2) Gereksiz uzun sorgu turu yaratabilir. Repoda .out-of-scope/question-limits.md var, soru sınırı bilinçli olarak eklenmemiş. (3) Kod tabanını okuyarak kendi başına araştırır, gizli dosyaları okuma izni ayarlarına bağlıdır. (4) Lisans doğrulanmadı, kopyalayıp dağıtmadan önce LICENSE dosyasına bak. (5) Yıldız sayısı ve son commit tarihi doğrulanmadı.
## Tasarruf
Token tasarrufu aracı değil. Amacı yanlış anlaşılan işi baştan yapmayı önlemektir, yani yeniden çalışma maliyetini düşürür. Kendisi çok turlu soru sorduğu için oturumda token harcar.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill olduğu için doğrudan uyarlanabilir. ~/.claude/skills/grill-me/SKILL.md dosyası yaz. Frontmatter'da name ve description olsun, description'a 'planı sına, grill me' gibi tetikleyiciler koy. Gövdeye şu kuralları yaz: (1) planın karar ağacını çıkar; (2) dalları bağımlılık sırasıyla gez; (3) her turda tek soru sor, önerdiğin cevabı da yaz; (4) kod tabanından yanıtlanabilecek soruyu sormadan önce Grep/Glob/Read ile ara; (5) varsayımları ve kaçınılan ödünleşimleri açığa çıkar; (6) ortak anlayışa varınca kararların özetini ver. Kendi dilimizde (Türkçe) yazılabilir, upstream metni birebir kopyalamak yerine lisansı doğruladıktan sonra uyarla.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-4/panel.md → Ömer sütunu
## Özellikler
### Tasarım ağacının her dalını sırayla gezerek sorgulama, bağımlılıkları çözerek
kaynak: https://gist.github.com/usirin/0f01923f7b2126b0cce817f9f8d97788
### Her turda tek soru sorup cevabı bekleme
kaynak: https://github.com/robmitt/grill-me-skill
### Kodla yanıtlanabilecek soruları Grep/Glob/Read ile kendisi araştırma
kaynak: https://github.com/robmitt/grill-me-skill
### Kod dışı kullanım için /grill-me, kod tabanı ve dokümanlı sürüm için /grill-with-docs
kaynak: https://github.com/mattpocock/skills
### Claude Code plugin olarak ya da npx skills ile düzenlenebilir kurulum
kaynak: https://github.com/mattpocock/skills
### grill-me skill'i çok kısa (videoda "yalnızca üç cümle") ve yine de çok etkili
video: EJyuu6zlQCg · iddia: Skill'ler uzun olmak zorunda değil; grill-me yalnızca üç cümle ve çok etkili.
sonuc: sınanamadı
arastirma: Kısalık kısmı büyük ölçüde destekleniyor, "üç cümle" sayısı doğrulanamadı. `video repo mattpocock/skills` çıktısında grill-me skill'i skills/productivity/grill-me/SKILL.md yolunda görünüyor. README onu "kod dışı kullanımlar" için /grill-me olarak tanıtıyor ve "en popüler skill'lerim" diyor. Kod tabanlı sürüm /grill-with-docs. Arama sonuçları SKILL.md'nin özünü şöyle özetliyor: (1) plan hakkında ortak anlayışa varana dek her yönü sorgula; (2) tasarım ağacının dallarını gez, kararlar arası bağımlılıkları tek tek çöz; (3) her soru için önerdiğin cevabı ver; (4) soruları teker teker sor; (5) soru kod tabanını inceleyerek cevaplanabiliyorsa kodu incele. Bu, kısa bir talimat kümesi. Bir kaynak (alphamatch blog) "altı satır" diyor. Bu, "üç cümle" iddiasıyla birebir örtüşmüyor. Bulduğum özet beş kadar talimat içeriyor, cümle sayısı kaynağa ve sürüme göre değişebilir. SKILL.md dosyasının ham metnine doğrudan erişemedim, bu yüzden tam cümle sayısı bilinmiyor. Repoda grilling'e ilişkin changeset'ler (soru arasına yatay çizgi ekleme, em dash kaldırma) var, yani metin zamanla değişmiş olabilir. "Çok etkili" kısmı öznel. README ve blog yazıları bunu övgü olarak söylüyor, ölçülmüş bir kanıt yok. Video sayfası/transkripti de okunamadı, bu yüzden Matt Pocock'un tam sözü doğrulanmadı.
kaynak: https://github.com/mattpocock/skills
## Destek
- EJyuu6zlQCg · 1:18 · Plan hakkında ortak anlayışa varana dek kullanıcıyı tasarım ağacının her dalı üzerinden sorguya çeker; kod tabanından cevaplanabilen soruları kendisi araştırır. · kanıt: Interview me relentlessly about every aspect of this plan until we reach a shared understanding. · iddia: Skill'ler uzun olmak zorunda değil; grill-me yalnızca üç cümle ve çok etkili.
