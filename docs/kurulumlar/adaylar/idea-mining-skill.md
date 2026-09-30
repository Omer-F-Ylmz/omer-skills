# idea-mining skill
ad: idea-mining skill
tur: skill
video: zKBPwDpBfhs
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (repo yok, kod incelenemedi). Analiz scriptinin ağ çağrısı yapıp yapmadığı doğrulanamadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
İçerik ve video fikirleri üreten bir Claude Code skill'i. Videoda (zKBPwDpBfhs, 7:46 civarı bölüm) örnek olarak gösteriliyor. Bulgulara göre kanal verisini, rakip listesini ve analiz scriptini proje dizininden referans alıyor.
## Mekanizma
Videodan çıkarılabilen kadarıyla: SKILL.md talimatı, proje dizinindeki dosyalara başvuruyor. Bunlar YouTube channel.md, bir JSON veri dosyası, rakip listesi ve analiz scripti. Skill çağrılınca Claude bu dosyaları okuyor, scripti çalıştırıp kanal ve rakip verisinden fikir üretiyor. "Seçenek B" bu referans yöntemini anlatıyor; seçenek A'nın ne olduğu bilinmiyor. Sayfa metni alınamadığı için iç işleyiş ayrıntıları doğrulanmadı.
## Kanıt
- Skill kanal verisi, rakip listesi ve analiz scriptini proje dizininden referanslıyor (seçenek B). → sınanamadı · video getir yalnızca YouTube sayfa iskeletini döndürdü (transkript yok). İddia sadece verilen video bulgusuna dayanıyor.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Kurulabilir bir repo veya paket yok. Videodaki skill dosyaları paylaşılmış mı, bilinmiyor.
- Elle kurulum: .claude/skills/idea-mining/SKILL.md dosyası oluştur.
- Proje dizinine channel.md, kanal JSON verisi, rakip listesi ve analiz scriptini koy. SKILL.md bunlara yol vererek başvursun.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Kanal ve rakip verisine dayalı, tekrarlanabilir bir fikir üretme iş akışı sağlıyor. Bağlam her seferinde elle yazılmıyor, dosyalardan okunuyor.
## Maliyet/risk
Kaynak kod yok, o yüzden denetlenemiyor. Analiz scripti yerelde çalıştığı için kaynağı bilinmeyen bir script çalıştırma riski var. Dokümantasyon ve sürüm takibi de yok. Bulgular tek bir videoya dayanıyor, sayfa içeriği alınamadı.
## Üretilebilir
hedef_tur: skill
tarif: Kendi idea-mining skill'imizi yazabiliriz. 1) .claude/skills/idea-mining/SKILL.md oluştur. Frontmatter'a name ve description yaz. 2) Gövdede şu adımları tanımla: channel.md oku (niş, kitle, ton), kanal JSON'unu oku (en iyi videolar ve metrikler), rakip listesini oku, analiz scriptini çalıştır (başlık kalıpları ve boşluk analizi). 3) Çıktı şablonu: 10 fikir, her biri için başlık, açı, rakip boşluğu ve gerekçe. 4) Script: rakip ve kanal JSON'undan görüntülenme, başlık kelimesi ve konu sıklığını hesaplayan küçük bir Python scripti. Ağ erişimi olmasın. 5) Veri dosyaları proje dizininde kalsın. SKILL.md göreli yollarla başvursun.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### İçerik ve video fikri üretimi
kaynak: https://www.youtube.com/watch?v=zKBPwDpBfhs
### Kanal verisi (channel.md, JSON), rakip listesi ve analiz scriptini proje dizininden referans alma
kaynak: https://www.youtube.com/watch?v=zKBPwDpBfhs
## Destek
- zKBPwDpBfhs · 7:46 · İçerik/video fikirleri üretir; kanal verisi, rakip listesi ve analiz scriptini proje dizininden referanslar (seçenek B). · kanıt: Idea mining skill; YouTube channel.md, JSON, rakip listesi ve analiz scripti referans.
