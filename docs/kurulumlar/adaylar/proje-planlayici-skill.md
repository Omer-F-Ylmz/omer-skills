# Proje planlayıcı skill
ad: Proje planlayıcı skill
tur: skill
video: kMk4pvFJ13s
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kod yok; saf prompt tabanlı bir skill olsaydı kendi başına telemetri beklenmez)
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-01-uzun)
## Ne
Videoda (kMk4pvFJ13s, "5 Claude Skills That Will Be Worth $500K/Year by 2027") anlatılan, proje için plan dosyası yazan, adımları tek tek yürütüp işaretleyen ve güncel planı gösteren bir skill fikri. Yayımlanmış bir repo/paket yok.
## Mekanizma
Video bulgusuna göre: plan dosyası oluşturulur, her seferinde tek adım yapılır, plan güncellenir (tamamlanan adım işaretlenir), ilerleme gösterilir ve sonraki adıma geçilir. Skill'in iç yapısı (SKILL.md içeriği, dosya biçimi) doğrulanamadı; sayfa getirme yalnızca YouTube sayfa iskeletini döndürdü, transkript alınamadı.
## Kanıt
- Skill plan dosyası yazar, adımları tek tek yapıp işaretler ve güncel planı gösterir. → sınanamadı · Video sayfası getirildi ama yalnızca YouTube altbilgisi/bağlantıları geldi; transkript yok. Tek kanıt, aday kaydındaki alıntı: 'Plan, do one step, update the plan, show progress, and then move forward.' Repo olmadığı için çalıştırılıp denenemedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Kurulabilir bir kaynak yok: repo/paket bağlantısı verilmemiş.
- Kendi skill'imizi yazmak için bkz. uretilebilir.tarif.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Uzun işlerde ilerlemeyi dosyada kalıcı tutar; oturum/bağlam kaybında kaldığı yerden devam etmeyi ve adım adım denetimi kolaylaştırır.
## Maliyet/risk
Kaynak yalnızca bir video bulgusu; gerçek uygulama görülmedi, kalite ve güvenlik bilinmiyor. Başlık pazarlama odaklı ("$500K/yıl"), bilgi değeri sınırlı olabilir. Benzer işlevi Claude Code'un yerleşik plan modu ve todo listesi de karşılıyor.
## Üretilebilir
hedef_tur: skill
tarif: SKILL.md yaz (name: proje-planlayici; description: çok adımlı proje istendiğinde tetiklenir). Talimatlar: 1) İstekten PLAN.md üret: hedef, '- [ ] Adım N' onay kutulu adımlar, her adım için bitiş ölçütü. 2) Kullanıcıya planı göster, onay al. 3) Döngü: ilk işaretsiz adımı tek başına yap, doğrula, '- [x]' işaretle, kısa ilerleme özeti (n/toplam) ve güncel planı göster. 4) Sapma/engel olursa planı güncelle ve nedenini not et. 5) Oturum başında PLAN.md varsa kaldığı yerden devam et. İsteğe bağlı: hook ile oturum başında PLAN.md'yi bağlama ekle.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-01-uzun/panel.md → Ömer sütunu
## Özellikler
### Plan dosyası yazma, tek adım yapma, planı güncelleme, ilerlemeyi gösterme, sonraki adıma geçme (video bulgusu)
kaynak: https://www.youtube.com/watch?v=kMk4pvFJ13s
## Destek
- kMk4pvFJ13s · 10:30 · Plan dosyası yazar, adımları tek tek yapıp işaretler ve güncel planı gösterir. · kanıt: Plan, do one step, update the plan, show progress, and then move forward.
