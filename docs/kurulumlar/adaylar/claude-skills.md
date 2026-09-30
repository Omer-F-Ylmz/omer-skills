# Claude Skills
ad: Claude Skills
tur: skill
video: kMk4pvFJ13s
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Skill dosyaları yerel klasördür. Claude hizmetinin kendi kullanım verisi toplaması bu araştırmada incelenmedi.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Bizde karşılığı var. Bu depo (omer-skills) zaten skill klasörleri barındırıyor. Kurulum gereği: Claude uygulaması veya Claude Code ve bir Anthropic hesabı. Skill-creator'ın ayrı bir kopyası gerekmez.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-01-uzun)
## Ne
Anthropic'in Claude için sunduğu Agent Skills özelliği. İçinde SKILL.md bulunan bir klasör (isteğe bağlı betik, referans ve varlık dosyalarıyla) Claude'a yeniden kullanılabilir kurallar ve iş akışları öğretir.
## Mekanizma
SKILL.md dosyasının başında YAML frontmatter (name, description) bulunur. Gövdede Markdown talimatları yer alır. Yükleme üç kademelidir (aşamalı açılım). 1) Başlangıçta yalnız name ve description yüklenir (skill başına yaklaşık 100 token). 2) İstek description ile eşleşince SKILL.md gövdesi yüklenir (yaklaşık 5.000 token altı hedeflenir). 3) Paketlenmiş dosyalar yalnız gerektiğinde okunur. Betikler bash ile çalışır ve bağlama yalnız çıktıları girer. Videoda Customize > Skills ekranında skill-creator örneği görünüyor. Klasörde SKILL.md, agents, assets, eval-viewer, references, scripts ve LICENSE.txt var. Video çekme aracı URL beklediği için video içeriğini alamadım. Mekanizma bilgisi web arama özetlerine dayanıyor, resmî dokümanı doğrudan açmadım.
## Kanıt
- İçinde SKILL.md bulunan klasörle Claude'a yeniden kullanılabilir kurallar ve iş akışları öğretilir. → doğrulandı · Video bulgusu: Customize > Skills ekranında skill-creator klasörü ve SKILL.md görünüyor. Web arama sonuçları da Agent Skills'i SKILL.md merkezli klasörler olarak tanımlıyor.
- Skill'ler aşamalı açılımla yüklenir; başlangıçta yalnız name ve description (~100 token) bağlama girer. → doğrulandı · Claude Platform Docs Agent Skills sayfasının arama özeti (platform.claude.com). Sayfayı doğrudan açıp doğrulamadım.
- Skill'lerin telemetri davranışı ve lisansı. → sınanamadı · Bu konuda kaynak okunmadı. Video getirme komutu video kimliğiyle çalışmadı, çünkü tam URL bekliyordu.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude uygulamasında Customize > Skills ekranını aç ve skill klasörünü ekle ya da skill-creator ile oluştur.
- Claude Code için: skill klasörünü ~/.claude/skills/ altına (kişisel) veya proje içindeki .claude/skills/ altına koy. Bu yolu resmî dokümandan doğrulamadım, genel bilgiye dayanıyor.
- Klasörde en az bir SKILL.md olsun. Frontmatter'a name ve description yaz.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tekrar eden talimatları tek yerde toplar ve gerektiğinde otomatik yükletir. Ekip içinde paylaşılabilir, sürüm kontrolüne konabilir. Ayrıca skill-creator ile skill üretmeyi ve değerlendirmeyi kolaylaştırır.
## Maliyet/risk
Skill içindeki betikler çalıştırılabilir kod olduğundan güvenilmeyen kaynaktan gelen skill'ler risklidir. Kötü niyetli talimat ya da betik içerebilir. Description kötü yazılırsa skill tetiklenmez veya yanlış tetiklenir. Lisans ve kullanım koşulları belirsiz. Skill-creator klasöründe LICENSE.txt var ama içeriğini görmedim.
## Tasarruf
Aşamalı açılım sayesinde bağlam tasarrufu sağlar. Kullanılmayan skill'ler yalnız yaklaşık 100 token'lık üst veriyle yer tutar. Gövde ve ek dosyalar yalnız gerektiğinde yüklenir. Betik çıktıları bağlama girerken betik kodu girmez. Bu rakamlar arama özetinden alındı, kendim ölçmedim.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill biçiminde. Kendi skill'imiz için bir klasör açıp içine SKILL.md koy. Frontmatter'a name ve dar kapsamlı bir description yaz. Gövdeyi 5.000 token altında tut. Uzun içeriği references/ altına, tekrar eden işleri scripts/ altına taşı. Sonra skill-creator örneğindeki klasör düzenini (agents, assets, eval-viewer, references, scripts) izle.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-01-uzun/panel.md → Ömer sütunu
## Özellikler
### SKILL.md + YAML frontmatter (name, description) ile skill tanımı
kaynak: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
### Üç kademeli aşamalı yükleme (üst veri, gövde, ek dosyalar)
kaynak: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
### Betikler bash ile çalışır; bağlama yalnız çıktı girer
kaynak: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
### Skill yazım en iyi uygulamaları (SKILL.md kısa tutulur, ayrıntılar ek dosyalara bölünür)
kaynak: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
## Destek
- kMk4pvFJ13s · 1:53 · İçinde skill.md bulunan klasörle Claude'a yeniden kullanılabilir kurallar ve iş akışları öğretme. · kanıt: Customize > Skills ekranında skill-creator ve SKILL.md dosyası görünüyor. (karede: Customize sayfası: Skills sekmesi, Personal skills altında skill-creator klasörü (SKILL.md, agents, assets, eval-viewer, references, scripts, LICENSE.txt) ve SKILL.md açıklaması.)
