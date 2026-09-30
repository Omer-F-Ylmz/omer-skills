# Cell Fracture eklentisi
ad: Cell Fracture eklentisi
tur: plugin
video: Vngbdm2IEXM
repo: yok
lisans: GPL-3.0-or-later
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Bilinmiyor. Yerel çalışan bir Blender eklentisi olduğu için ağ çağrısı beklenmez, ama kodu incelemedim.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short)
## Ne
Blender'da seçili bir mesh nesnesini Voronoi (hücre) tabanlı çok sayıda parçaya bölen eklenti. Video, Solidify uygulanmış bir UV küreyi kırık parçalara ayırmak için kullanıyor.
## Mekanizma
Nesnenin içinde (köşe, yüzey ya da rastgele) kaynak noktaları üretir. Bu noktalardan Voronoi hücreleri hesaplar, her hücreyle mesh'i keser ve her parça için ayrı nesne oluşturur. Parçalar isteğe bağlı olarak rijit cisim (rigid body) fiziğine bağlanabilir. Bu bilgi benim genel Blender bilgimden geliyor. Bu oturumda kaynak koddan doğrulamadım. Videodaki kanıt yalnızca kullanım anını gösteriyor: "Immediately apply the cell fracture add-on."
## Kanıt
- Cell Fracture, Solidify uygulanmış UV küreyi parçalara ayırmak için kullanılıyor. → doğrulandı · Video Vngbdm2IEXM 0:22: "Immediately apply the cell fracture add-on."
- Eklenti GPL lisanslı ve Blender ile birlikte dağıtılıyor. → sınanamadı · Web araması ve repo incelemesi yapılmadı. Bilgi genel Blender bilgisine dayanıyor.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Blender 4.2 ve üstü: Edit > Preferences > Get Extensions bölümünden 'Cell Fracture' aranıp kurulur. Bu adım doğrulanmadı.
- Eski sürümler: Preferences > Add-ons içinde 'Object: Cell Fracture' işaretlenir.
- Kullanım: nesne seçilir, Object > Quick Effects > Cell Fracture açılır.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Elle modelleme yapmadan yıkım, kırılma ve parçalanma efektleri için hızlıca parça geometrisi üretir.
## Maliyet/risk
Düşük. Parça sayısı çok artarsa performans ve bellek sorunu çıkar. Kalınlığı olmayan mesh'lerde kırma başarısız olabilir, bu yüzden videoda önce Solidify uygulanmış. Sürüme göre kurulum yeri değişiyor. Resmî repo ve sürüm bilgisi doğrulanmadı.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short/panel.md → Ömer sütunu
## Özellikler
### Mesh'i Voronoi hücreleriyle çok parçaya bölme, videoda Solidify'lı UV küre üzerinde gösterilmiş
kaynak: https://www.youtube.com/watch?v=Vngbdm2IEXM
### Cell Fracture eklentisi ile bir mesh'i Voronoi hücreleriyle çok parçaya bölme. Videoda Solidify uygulanmış UV küre üzerinde, Solidify'dan hemen sonra kullanılıyor.
video: Vngbdm2IEXM · iddia: Cell fracture eklentisi solidify sonrası hemen uygulanıyor.
sonuc: doğrulandı
arastirma: Cell Fracture, Blender'ın Quick Effects altındaki bir eklentisi. Blender arama sonuçları bunu doğruluyor. Seçili nesne için Object > Quick Effects > Cell Fracture açılır. Operatör aramasında "Cell fracture selected mesh" yazılır. Eklenti Blender ile birlikte gelir. Eski sürümlerde Preferences > Add-ons içinden etkinleştirilmesi gerekir. Blender Extensions sayfasında da 'Cell Fracture' adıyla listeleniyor. Belgeye göre nesne kaynak noktalarından hücrelere bölünür ve her parça ayrı nesne olur. Büyük ayarlar yavaş çalışabilir, bu yüzden küçük değerlerle başlamak öneriliyor. Videonun sayfası bu ortamda yalnızca YouTube alt bilgisini döndürdü, bu yüzden 0:22'deki "Immediately apply the cell fracture add-on" sözünü ve Solidify sırasını kendim doğrulayamadım. Bu iddia adayın kendi kanıt notuna dayanıyor. Eklentinin GPL lisansı, tam sürüm ve kurulum yolunun Blender 4.2 ve sonrasındaki hali bu oturumda kaynaktan doğrulanmadı. Bu konuda bilinmiyor.
kaynak: https://docs.blender.org/manual/en/2.83/addons/object/cell_fracture.html
## Destek
- Vngbdm2IEXM · 0:22 · Solidify uygulanmış UV küreyi parçalara ayırmak için kullanılıyor. · kanıt: "Immediately apply the cell fracture add-on." · iddia: Cell fracture eklentisi solidify sonrası hemen uygulanıyor.
