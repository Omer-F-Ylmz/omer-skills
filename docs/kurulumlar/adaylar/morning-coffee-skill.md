# morning-coffee skill
ad: morning-coffee skill
tur: skill
video: zKBPwDpBfhs
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kaynak kod/repo bulunamadı; takvim ve ClickUp verisi bağlayıcılar üzerinden okunur)
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Bizde birebir karşılığı yok; Google Calendar ve ClickUp bağlayıcıları varsa üstteki tarifle kendi skill'imiz yapılabilir. Benzer açık kaynak örnek: xj-2045/morning-ritual.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Takvim ve ClickUp görevlerine bakıp günün planını (bugünün takvimi + acil/aksiyon maddeleri) çıkaran sabah brifingi skill'i. Videoda VS Code içinde 'Morning Coffee - February 26, 2026 (Thursday)' başlıklı çıktı görülüyor.
## Mekanizma
Kesin kaynak koduna ulaşılamadı. Videodan ve arama sonuçlarından çıkan olası yapı: skill tetiklenince takvim (Google Calendar) ve ClickUp bağlayıcılarından (MCP/connector) veri çeker, vadesi gelen/geciken görevleri filtreleyip sıralar, 'Today's Calendar' ve 'Urgent / Action Items' bölümlerinden oluşan bir markdown brifing üretir. Videodaki 'Pretend it is morning' sekmesi, brifingin test amacıyla sanki sabahmış gibi çalıştırıldığını düşündürüyor. Bu çıkarım doğrulanmadı; 'Coffee with Claude' (successwithsoul.co) adlı benzer bir ürünle ilişkisi de kanıtlanmadı.
## Kanıt
- Skill takvim ve ClickUp görevlerine bakıp günün planını çıkarır → sınanamadı · Yalnızca video karesi (Today's Calendar, Urgent / Action Items başlıkları) var. Repo yok; çalıştırılıp denenemedi.
- Benzer 'Coffee with Claude' ürünü ClickUp, Gmail ve Google Calendar'dan sabah brifingi üretir → doğrulandı · Arama sonucu özeti (successwithsoul.co). Bu adayla aynı olduğu doğrulanmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- bilinmiyor
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Güne başlarken takvim ve görevleri tek brifingte toplar; manuel tarama süresini azaltır. Token tasarrufu aracı değil.
## Maliyet/risk
Kaynak/repo ve lisans yok, kurulabilir bir paket doğrulanamadı. Takvim ve görev verisine erişim gerektirir (özel veri). Video yalnızca 0:30'luk bir kare; ayrıntı yok. `video getir` bu aday için çalıştırıldı ama girdi URL değil video kimliği olduğundan hata verdi; sayfa içeriği alınamadı.
## Üretilebilir
hedef_tur: skill
tarif: SKILL.md yaz: tetik 'sabah brifingi'. Adımlar: (1) Google Calendar MCP/connector ile bugünün etkinliklerini saat sırasıyla çek; (2) ClickUp MCP ile bugün vadeli ve gecikmiş görevleri çek, öncelik ve vadeye göre sırala; (3) çıktıyı 'Bugünün Takvimi' ve 'Acil / Aksiyon Maddeleri' başlıklarıyla markdown olarak üret, en üste günün tek odağını yaz; (4) test için tarih parametresi ('sabah gibi davran') ekle; (5) istenirse zamanlanmış görev (cron/schedule) ile otomatikleştir. Bağlayıcı yoksa kullanıcıdan manuel liste iste.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### Takvim + ClickUp görevlerinden günlük brifing (benzer ürün: Coffee with Claude; bu adayla aynılığı doğrulanmadı)
kaynak: https://successwithsoul.co/coffee-with-claude/
### Benzer açık kaynak örnek: takvim ve kanban'ı tek HTML sayfada birleştiren günlük brifing skill'i
kaynak: https://github.com/xj-2045/morning-ritual
## Destek
- zKBPwDpBfhs · 0:30 · Takvim ve ClickUp görevlerine bakıp günün planını çıkaran kişisel asistan skill'i. · kanıt: Morning Coffee briefing; 'Pretend it is morning' sekmesi, takvim ve acil işler listesi. (karede: VS Code'da 'Morning Coffee - February 26, 2026 (Thursday)' brifingi, Today's Calendar ve Urgent / Action Items başlıkları.)
