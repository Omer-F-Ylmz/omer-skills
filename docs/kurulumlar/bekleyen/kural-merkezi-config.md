# ONAY kural merkezi-config
ad: merkezi-config
madde: Ayarlanabilir sahne parametrelerini (görsel sayısı, hız, boşluk) tek bir CONFIG nesnesi/dosyasında topla; prompt'ta bunu iste.
kaynak: video JfmAm3sxCSc, 15b
gerekce: İkinci tur ayarları tek dosyada; "diğerlerini bozma" riski düşer.
çift/çelişki: yok

Onay: `video kural-onay merkezi-config` · ret: dosyayı sil.

# merkezi-config
ad: merkezi-config
tur: ipucu
video: JfmAm3sxCSc
karar: KUR
kural: Ayarlanabilir sahne parametrelerini (görsel sayısı, hız, boşluk) tek bir CONFIG nesnesi/dosyasında topla; prompt'ta bunu iste.
## Ne
Görsel sayısı, dönüş hızı, aralık gibi değerler tek yerde; ince ayar kodu yeniden yazdırmadan yapılır.
## Kanıt
JfmAm3sxCSc 4:02 config dosyasında genel ayarlar; 6:37 karede script.js `CONFIG` (docs/video-tarama/2026-09-24-JfmAm3sxCSc.md).
## Bizde durum
yok: web-sahne-desenleri desen verir, parametre merkezileştirme kuralı yok.
## Beklenen fayda
İkinci tur ayarları tek dosyada; "diğerlerini bozma" riski düşer.
## Maliyet/risk
Kural dosyasına 1 satır; küçük işte gereksiz soyutlama riski (Simplest solution kuralıyla çelişebilir).
## Karar
KUR (T0 kural, ONAY bekler).
## Sonraki adım
bekleyen/kural-*.md → Ömer karar verir.
## Geri alma
omer-kurallar.md eklenen satırı sil
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Config dosyasıyla görsel sayısı tek yerden değişir (4:02) | https://github.com/YildizDikme/3D-threejs-spiral-gallery/blob/main/src/script.js | doğru | src/script.js:14 `const CONFIG = {` (gh api, 2026-09-24) | - |
