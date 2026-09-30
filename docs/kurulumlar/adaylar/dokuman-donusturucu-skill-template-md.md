# Doküman dönüştürücü skill (template.md)
ad: Doküman dönüştürücü skill (template.md)
tur: skill
video: kMk4pvFJ13s
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Skill düz markdown olduğu için kendi telemetrisi yok. Kaynak kod görülmedi, bu yüzden kesin değil.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-01-uzun)
## Ne
Dağınık toplantı notlarını özet, ana noktalar ve sahipli aksiyon listesine çeviren bir Claude skill'i. Çıktı biçimi için skill klasöründeki template.md referans alınıyor. Video başlığı "5 Claude Skills That Will Be Worth $500K/Year by 2027" olarak görünüyor; skill bu listedeki örneklerden biri.
## Mekanizma
Videonun sayfa çekimi yalnızca YouTube altbilgisini döndürdü; transkript alınamadı. Bu yüzden ayrıntılar yalnızca video bulgusuna dayanıyor. Bulguya göre SKILL.md, modele ham notu okutup şu üç bölümü üretmesini söylüyor: özet, ana noktalar, sahipli aksiyonlar. Çıktı şablonu ayrı bir template.md dosyasında duruyor ve SKILL.md bu dosyaya atıf yapıyor ("Format the output using template.md"). Kod yok, yalnızca talimat ve şablon var; bu skill'lerde olağan olan progressive disclosure düzeni. Bu düzen tahminimdir, doğrulanmadı.
## Kanıt
- Skill dağınık toplantı notlarını özet, ana noktalar ve sahipli aksiyon listesine çevirir. → sınanamadı · Yalnızca video özeti var. Sayfa çekimi sadece YouTube altbilgisini döndürdü, repo veya skill dosyası yok.
- Çıktı template.md referans alınarak biçimlendirilir. → sınanamadı · Video bulgusunda 'Format the output using template.md.' satırı var. Dosyanın kendisine erişilemedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Repo yok, hazır kurulum yok. Video sayfasında bağlantı bulunamadı.
- Elle kurulum: .claude/skills/toplanti-ozeti/ altına SKILL.md ve template.md oluştur.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Toplantı notlarını her seferinde aynı yapıda (özet, ana noktalar, sahipli aksiyonlar) üretir. Şablon sayesinde çıktı tutarlı olur ve tekrar eden prompt yazma işi azalır.
## Maliyet/risk
Kaynak ve repo yok, bu yüzden denetlenemez. Video başlığı abartılı ("$500K/year") ve tanıtım amaçlı görünüyor. İçerik transkriptle doğrulanmadı. Toplantı notları hassas veri içerebilir. Sahip atamalarını model uydurabilir; notta isim yoksa boş bırakması gerekir.
## Üretilebilir
hedef_tur: skill
tarif: Bir klasör oluştur: .claude/skills/toplanti-ozeti/. SKILL.md içine frontmatter yaz (name, description: 'Toplantı notlarını özet, ana noktalar ve sahipli aksiyonlara çevirir'). Gövdede şunları iste: notu oku, karar ve aksiyonları ayıkla, sahibi ve tarihi notta yoksa uydurma ve 'belirsiz' yaz, çıktıyı template.md'ye göre biçimlendir. template.md içine başlıkları koy: ## Özet, ## Ana Noktalar, ## Aksiyonlar (tablo: Aksiyon / Sahip / Tarih). Birkaç örnek not ve çıktı çifti ekleyerek sına.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-01-uzun/panel.md → Ömer sütunu
## Özellikler
### Toplantı notundan özet, ana noktalar ve sahipli aksiyon listesi üretir
kaynak: https://www.youtube.com/watch?v=kMk4pvFJ13s
### Çıktı biçimi template.md şablonuyla sabitlenir
kaynak: https://www.youtube.com/watch?v=kMk4pvFJ13s
## Destek
- kMk4pvFJ13s · 8:02 · Dağınık toplantı notlarını özet, ana noktalar ve sahipli aksiyon listesine çevirir; template.md'yi referans alır. · kanıt: Format the output using template.md.
