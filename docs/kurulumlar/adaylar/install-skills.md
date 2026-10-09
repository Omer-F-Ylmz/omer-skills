# install skills
ad: install skills
tur: skill
video: vfLtsYbtJf0
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kaynak kod incelenemedi)
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Diğer skill'ler arasında arama yapıp kullanım amacına uygun olanı bulan ve kurulu kodlama ajanlarına kuran bir skill. Tek kaynak videodaki altyazı ve kare; repo bulunamadı.
## Mekanizma
Bilinmiyor (repo/kaynak kodu yok). Videoya göre kullanıcı amacını verir, skill mevcut skill dizinlerinde arar, eşleşeni seçip kurulu ajanların (Claude Code, Codex vb.) skill klasörlerine kurar. Ayrıntılar doğrulanamadı.
## Kanıt
- Skill, diğer skill'lerde arama yapıp amaca uygun olanı kurulu kodlama ajanlarına kuruyor. → sınanamadı · Yalnızca video altyazısı/karesi var. `video getir` komutu ID ile çalışmadı (URL bekliyor), web aramasında bu ada ait repo çıkmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- bilinmiyor
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Skill keşfi ve kurulumunu tek adıma indirir; elle arama ve kopyalama gerekmez. Doğrulanmadı.
## Maliyet/risk
Repo, lisans ve kaynak kodu belirlenemedi. Üçüncü taraf skill'leri otomatik kurduğu için tedarik zinciri riski var: kurulan skill'ler talimat/komut içerebilir ve incelenmeden kurulmamalı. Aynı adda birden fazla proje olabilir. Adaylık kimliği belirsiz.
## Üretilebilir
hedef_tur: skill
tarif: Kendi 'skill-bul-kur' skill'imiz yazılabilir: (1) kullanıcıdan amaç al; (2) bilinen skill indekslerinde (GitHub repoları, `npx skills` ekosistemi, yerel omer-skills) anahtar kelimeyle ara; (3) adayları SKILL.md açıklamalarıyla listele; (4) kullanıcı onayından sonra, kurulumdan önce içeriği güvenlik taramasından (SkillSpector benzeri) geçirip ~/.claude/skills ve ~/.agents/skills altına kopyala. Orijinal kod incelenmeden birebir eşdeğerlik iddia edilemez.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
## Destek
- vfLtsYbtJf0 · 0:33 · Diğer skill'lerde arama yapıp kullanım amacına uygun olanı bulan ve kurulu kodlama ajanlarına kuran skill. · kanıt: Altyazı: 'It is called install skills and it is a skill that searches' (karede: Kare 0:33: arama kutusu ve büyüteç ikonu, 'And it is a skill that searches through all the other skills' yazısı.)
