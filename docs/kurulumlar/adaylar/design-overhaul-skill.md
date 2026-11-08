# Design overhaul skill
ad: Design overhaul skill
tur: skill
video: BiEvvC_66AQ
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kod incelenemedi)
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Videoda ("Top 5 Claude Code Skills", BiEvvC_66AQ) 60'tan fazla stil sunan ve genel yapay zeka çıktısını profesyonel görünüme çevirdiği söylenen bir tasarım skill'i. Videonun sayfa metni alınamadı (yalnızca YouTube altbilgisi geldi). Skill'in gerçek adı ve deposu doğrulanamadı.
## Mekanizma
bilinmiyor. Kaynak kodu görülmedi. Bu tür skill'ler genelde SKILL.md içine stil kuralları, tipografi, renk ve yerleşim yönergeleri koyar ve ajan bunlarla arayüz üretir. Bu skill için bu doğrulanmadı.
## Kanıt
- 60'tan fazla stil sunuyor ve jenerik yapay zeka çıktısını profesyonel gösteriyor → sınanamadı · Tek kaynak videonun özet cümlesi. Sayfa metni alınamadı, repo bulunamadı. Arama yalnızca benzer projeleri listeledi: claude-design-styles (50+ stil), awesome-claude-design (68 DESIGN.md).
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Kesin kurulum bilinmiyor; skill'in deposu bulunamadı.
- Benzer aday: npx skills add superdesigndev/superdesign-skill (aynı skill olduğu doğrulanmadı).
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Doğruysa, ajanın ürettiği arayüzlerin jenerik "AI görünümünden" çıkması ve hazır stil seçenekleri sunması.
## Maliyet/risk
Aday kimliği belirsiz. Aramada benzer projeler çıktı (superdesign-skill, claude-design-styles, awesome-claude-design, styleseed) ama hangisinin videodaki skill olduğu kanıtlanamadı. Lisans, bakım durumu ve içerik doğrulanmadı. Kimliği belirsiz bir skill'i kurmak kötü amaçlı talimat riski taşır; kurmadan önce SKILL.md okunmalı.
## Üretilebilir
hedef_tur: skill
tarif: Kendi skill'imizi yazabiliriz: skills/design-overhaul/SKILL.md. İçine her stil için kısa bir dosya koy (palet, font çifti, boşluk, bileşen kuralları, kaçınılacak AI klişeleri). Ana SKILL.md önce mevcut arayüzü denetler (hizalama, kontrast, tipografi hiyerarşisi), kullanıcıdan stil seçtirir, sonra seçilen stil dosyasını yükleyip yeniden yazar. Başlangıç stil kaynağı olarak MIT lisanslı açık depolar kullanılabilir, lisansları önce kontrol edilmeli.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### 60+ tasarım stili (videoda iddia edilen, doğrulanmadı)
kaynak: https://www.youtube.com/watch?v=BiEvvC_66AQ
## Destek
- BiEvvC_66AQ · 0:00 · 60+ stil sunan, genel yapay zeka çıktısını profesyonel görünüme çeviren tasarım skill'i. · kanıt: design overhaul skill with over 60 styles that makes generic AI outputs look professionally done
