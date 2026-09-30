# Claude skills (yetenek ekleme)
ad: Claude skills (yetenek ekleme)
tur: skill
video: Wz4qYO-91zg
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (bu araştırmada doğrulanmadı; yerel skill dosyaları için ek telemetri beklenmez ama Claude'un kendi kullanım verisi Anthropic politikasına tabidir)
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Bu çalışma alanı (omer-skills) zaten skill mekanizmasını kullanıyor; Claude Code'un yerleşik skills özelliği bizde karşılık olarak mevcut. Ayrı kurulum gerekmez.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-4)
## Ne
Anthropic'in Claude için sunduğu Agent Skills özelliği: konuya özel talimat, betik ve kaynak içeren klasörlerle Claude'a alan yeteneği eklenmesi. Videoda (Wz4qYO-91zg) sonuç kalitesi için konuyla ilgili yetenekler eklemek öneriliyor.
## Mekanizma
Genel bilgiye dayalı, doğrulanmadı: Bir skill, SKILL.md (ad ve açıklama içeren frontmatter + talimatlar) ve isteğe bağlı betik/kaynak dosyalarından oluşan bir klasördür. Claude yalnızca ad/açıklamayı bağlama alır; görev uyduğunda tam içeriği yükler (kademeli yükleme). Bu araştırmada web/repo sorgusu yapılmadı; ayrıntılar resmi dokümanla teyit edilmeli.
## Kanıt
- Claude'a konuyla ilgili yetenekler (skills) eklemek sonuç kalitesi için önerilir → sınanamadı · Yalnızca video ifadesi var ('Sürekli yeni yetenekleri eklemeniz lazım... skills'); bağımsız test veya kaynak sorgulanmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code: skill klasörünü ~/.claude/skills/<ad>/ veya proje içi .claude/skills/<ad>/ altına SKILL.md ile koy
- Claude.ai: Ayarlar > Capabilities/Skills bölümünden yükle (plan gereksinimi doğrulanmadı)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude'un konuya özel işlerde tutarlılığını ve çıktı kalitesini artırır; tekrarlanan talimatlar yeniden kullanılabilir hale gelir.
## Maliyet/risk
Üçüncü taraf skill'ler içinde betik/talimat enjeksiyonu riski olabilir; kurmadan önce içerik incelenmeli. Video kanıtı çok kısa ve genel; belirli bir skill değil kavramdan söz ediyor. Ürün kapalı kaynak/platform özelliği olduğundan sürüm değişiklikleri Anthropic'e bağlı.
## Tasarruf
Token aracı değil. Dolaylı olarak kademeli yükleme sayesinde yalnızca gerekli skill içeriği bağlama girer (doğrulanmadı).
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-4/panel.md → Ömer sütunu
## Özellikler
## Destek
- Wz4qYO-91zg · 2:02 · Claude'a konuyla ilgili yetenekler eklemek sonuç kalitesi için önerilir. · kanıt: Sürekli yeni yetenekleri eklemeniz lazım. Bunu da örneğin skills.
