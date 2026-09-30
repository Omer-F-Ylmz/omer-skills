# skill-builder skill
ad: skill-builder skill
tur: skill
video: zKBPwDpBfhs
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Skill içeriği incelenmedi. Dağıtım Skool platformu üzerinden, platformun kendi veri toplaması var.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Bizde birebir karşılık doğrulanmadı. Resmi skill-creator skill'i benzer iş görür, ancak bu depoda varlığı kontrol edilmedi. Uyarlama için yukarıdaki tarifle kendi skill'imiz yazılabilir.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Sorular sorarak yeni Claude Code skill'i oluşturan, mevcut skill'i optimize eden ve denetleyen bir skill. Videoya göre SKILL.md ve reference.md dosyalarından oluşuyor. Ücretsiz bir Skool topluluğunda dağıtılıyor.
## Mekanizma
Videoya göre kullanıcıya sırayla sorular soruyor, yanıtlardan skill iskeleti üretiyor. Mevcut skill'lerde optimize ve denetim kipleri var. Reference.md büyük olasılıkla en iyi uygulama kurallarını tutuyor. İç yapıya dair ayrıntı doğrulanamadı: repo yok, skill içeriği incelenemedi, video sayfası çekildiğinde yalnızca YouTube çerçevesi geldi, transkript alınamadı.
## Kanıt
- Skill yeni skill oluşturur, optimize eder ve denetler; SKILL.md + reference.md içerir. → sınanamadı · Repo yok, Skool içeriğine erişilemedi. video getir yalnızca YouTube sayfa çerçevesini döndürdü, transkript yoktu.
- Skill'i yükle, sana gereken her şeyi kurmana yardım eder. → sınanamadı · Yalnızca video anlatımı; bağımsız kaynak yok.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Kaynak kapalı: skill dosyaları ücretsiz Skool topluluğuna katılarak indiriliyor (bağlantı doğrulanamadı).
- İndirilen klasörü ~/.claude/skills/skill-builder/ altına koymak gerekir (Claude Code skill konumu, standart bilgi).
- Kullanım: Claude Code'da skill'i çağırıp sorulara yanıt vermek.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Skill yazımını soru-cevap akışına çevirir. Mevcut skill'leri denetleme ve optimize etme imkânı sunar. Yine de Anthropic'in resmi skill-creator skill'i ve kendi yazacağımız bir skill aynı işi karşılar.
## Maliyet/risk
Kaynak kapalı, lisans belirsiz, bir topluluk üyeliği arkasında. İçerik incelenmeden kurmak, skill talimatları Claude'a komut verdiği için risklidir. Kanıt yalnızca video başlığı ve sunucunun sözüne dayanıyor; içerik doğrulanamadı.
## Üretilebilir
hedef_tur: skill
tarif: skill-builder/SKILL.md yaz. Frontmatter: name, description (ne zaman tetiklenir). Gövde üç kip içerir. (1) Oluştur: amaç, tetikleyici, girdi/çıktı, araçlar, örnekler hakkında sırayla sorular sor, sonra SKILL.md taslağı üret. (2) Optimize: mevcut SKILL.md'yi oku, description netliği, uzunluk, gereksiz tekrar ve ayrıntıyı reference.md'ye taşıma açısından gözden geçir. (3) Denetle: kontrol listesi uygula (tetikleyici açıklığı, güvenlik, sırlar, dış komutlar, belirsiz talimatlar). reference.md'ye en iyi uygulamaları ve kontrol listesini koy. Anthropic'in resmi skill-creator skill'i referans alınabilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### Soru sorarak yeni skill oluşturma, mevcut skill'i optimize etme ve denetleme (video iddiası)
kaynak: https://www.youtube.com/watch?v=zKBPwDpBfhs
## Destek
- zKBPwDpBfhs · 8:48 · Sorular sorarak yeni skill oluşturan, optimize eden ve denetleyen skill; SKILL.md + reference.md içerir. Ücretsiz Skool topluluğunda. · kanıt: Skill builder'ı yükle, sana gereken her şeyi kurmana yardım eder.
