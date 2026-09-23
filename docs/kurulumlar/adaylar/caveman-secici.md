# caveman-secici
ad: caveman-secici
tur: ipucu
video: jf1sv2geEWo
zaman: 4:35
karar: ÖĞREN
kural: Caveman'ı her promptta değil, yalnız sohbet ağırlıklı (kod üretimi az) görevde `/caveman:caveman <prompt>` ile çağır.
iddia: Caveman yalnız iletişim metnini kısaltır; kod ağırlıklı uzun görevde oturum kullanımı değişmez, maliyeti thinking ve kod üretimi taşır.
guven: orta
dogrulama: https://github.com/JuliusBrussee/caveman (README iddiası) + docs/denemeler/caveman-sonuc.md (14b: çıktı −%20.7, maliyet +%7.7)
etiketler: token, caveman, olcum
not: sunucunun A/B'si (jf1sv2geEWo): iki koşuda da +4, fark yok
## Ne
Video Caveman'ı aynı Laravel görevinde (Opus, high effort) açık/kapalı koşturuyor: /usage ikisinde de +4 puan. Öneri: seçerek çağır.
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
yok: caveman/skill RED(ölçüm) (kayıt 6, docs/denemeler/caveman-sonuc.md); kısmen: bilgi/caveman-kural-maliyeti.md aynı yönde.
## Beklenen fayda
Kural olarak yok (skill kurulu değil); olgu olarak var: token tasarrufu iddialarını değerlendirirken "iletişim payı küçük" bilgisi.
## Maliyet/risk
Düşük. Video ölçümü kaba (/usage yüzde, n=1); kart guven orta.
## Karar
ÖĞREN: araç adı geçiyor (olgu); skill RED olduğu için seçerek-çağır kuralı işe yaramaz.
## Sonraki adım
caveman/proxy DENE (girdi tarafı) bu bulguyla tutarlı: kazanç varsa okuma tarafında aranır.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Caveman %65 token kesintisi (README) | docs/denemeler/caveman-sonuc.md | abartılı | bizde çıktı −%20.7, toplam maliyet +%7.7 | caveman-kural-maliyeti |
| 69→19 token, %75 azalma | https://github.com/JuliusBrussee/caveman | abartılı | tek cümlelik izole örnek; oturumu temsil etmez | caveman-kural-maliyeti |
| Caveman açık/kapalı oturum kullanımı aynı (+4 = +4 puan) | docs/denemeler/caveman-sonuc.md | doğru | bizde de toplam maliyet düşmedi (+%7.7) | |
| Maliyetin çoğu iletişim değil thinking | docs/cikti-notlari.md | kısmen doğru (çıktı içinde; toplam maliyette girdi baskın) | thinking çıktının %41'i; bizde girdi 94k ≫ çıktı 831 | |
| Caveman 40.000 yıldız | - | doğrulanamadı | gh api 2026-09-23: 107.495; video çekim anı bilinmiyor | |
