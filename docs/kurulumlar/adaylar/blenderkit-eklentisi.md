# BlenderKit eklentisi
ad: BlenderKit eklentisi
tur: plugin
video: q1QQN08ZK6I
repo: blenderkit/blenderkit
lisans: GPL-2.0-or-later (eklenti kodu, doğrulanmadı; varlıklar ayrı lisanslı: Royalty Free / CC0)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/BlenderKit/BlenderKit
telemetri: Bilinmiyor. Eklenti sunucuyla iletişim kurduğu için arama sorguları ve kullanım verisi muhtemelen BlenderKit'e gidiyor. Kaynak koddan doğrulamadım.
yildiz: bilinmiyor
alt_tur: servis
kullanim_kosullari: Varlıklar iki lisansla gelir. Ticari kullanım serbesttir. Royalty Free lisans, 3D modellerin değiştirilmiş halinin bile yeniden satışına izin vermez.
ucretsiz_katman: Free Plan: 10.000+ model, 10.000+ materyal, 250+ sahne, 1.000+ HDRI, 300+ fırça. Giriş gerekmez.
veri_gizliligi: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short)
## Ne
Blender içinden BlenderKit çevrimiçi kütüphanesindeki modelleri, materyalleri, sahneleri, HDRI'ları ve fırçaları arayıp sahneye eklemeyi sağlayan resmi eklenti. Videoda hazır bir beyin modelini sahneye eklemek için kullanılıyor.
## Mekanizma
Eklenti Blender arayüzüne bir arama paneli ekler. Panel BlenderKit sunucusunun API'sini sorgular, seçilen varlığı indirir ve sahneye ekler (append/link). Giriş, tarayıcı üzerinden yapılan OAuth ile olur. Kaynak koddan bunu doğrulamadım; web araması özetine dayanıyor.
## Kanıt
- BlenderKit eklentisiyle hazır bir beyin modeli sahneye eklenebilir. → sınanamadı · Videoda 0:40'ta 'go to the Blender Kit add-on and add a brain' deniyor. Kendim denemedim.
- Ücretsiz katman var ve giriş gerektirmiyor. → doğrulandı · Web arama sonuçları: Free Plan 10.000+ model sunuyor, giriş şart değil. Resmi sayfayı doğrudan açmadım.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Blender'ı aç: Edit > Preferences > Get Extensions / Add-ons bölümünde 'BlenderKit' ara ve kur (ya da blenderkit.com'dan zip indirip kur)
- Eklentiyi etkinleştir; 3D Viewport'ta N paneli > BlenderKit sekmesini aç
- İsteğe bağlı: ücretsiz hesapla giriş yap (Free Plan'da giriş şart değil)
- Aramaya 'brain' yaz ve çıkan modeli sahneye sürükle/ekle
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Hazır 3D varlıkları Blender içinden bulup eklemek, sıfırdan modelleme süresini azaltır. Ücretsiz katman çok sayıda varlık içerir ve giriş gerektirmez. Varlıkların ticari kullanımına izin verilir.
## Maliyet/risk
Tam kütüphane ücretli abonelik gerektirir. Varlıklara ait Royalty Free lisans, değiştirilmiş de olsa 3D modellerin yeniden satılmasına izin vermez. Eklenti çevrimiçi çalışır, ağ bağımlılığı ve veri paylaşımı vardır. Videodan yalnızca tek bir kullanım anı görüldü.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short/panel.md → Ömer sütunu
## Özellikler
### Blender içinden model, materyal, sahne, HDRI ve fırça arama/ekleme
kaynak: https://github.com/BlenderKit/BlenderKit
### Ücretsiz plan (10.000+ model, giriş şart değil) ve Full plan (27.000+ model)
kaynak: https://blender-addons.org/blenderkit/
### İki lisans türü, tüm varlıklarda ticari kullanım izni
kaynak: https://www.blenderkit.com/articles/free_and_paid_addons_onblenderkit/
## Destek
- q1QQN08ZK6I · 0:40 · Hazır beyin modelini sahneye eklemek için kullanılıyor. · kanıt: "go to the Blender Kit add-on and add a brain"
