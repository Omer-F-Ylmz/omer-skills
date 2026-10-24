---
name: reel-plan
description: Kısa dikey video (Reels/Shorts/TikTok) için hook madenciliği, izleyici tutma merdiveni denetimi ve haftalık yayın takvimi. Kullanıcı nişindeki aykırı başarılı gönderilerden hook çıkarmak, bir reel taslağının tutmasını denetlemek ya da haftalık reel planı istediğinde kullan; konsept ve senaryo yazımı için reel-taste'e devret.
---

# Reel plan

Taslak (IG-40-KUR P3). Kaynak: Dd1zrTggHCW'deki ücretli skill setinin adları; yalnız mekanizma, metin kopyası yok. Konsept, cihaz rafı, kamera/geçiş ve taste audit **reel-taste**'te; bu skill onun önüne ve arkasına oturur.

## 1. Hook madenciliği (önce)
1. Girdi: nişteki gönderi linkleri ya da `docs/video-tarama/*.md` raporları. Yoksa kullanıcıdan 10 link iste.
2. Hesabın medyan izlenmesinin ≥3 katı olanları "aykırı" say; en çok 10 tane.
3. Her aykırının ilk 2 saniyesini tek kalıba indir: soru · aykırı iddia · sonuç önce · sayı · "pov" · yarıda kesilen eylem.
4. Çıktı: `kalip · örnek gönderi · neden işledi (tek satır)`. Konuyla birlikte reel-taste'e ver.

## 2. Tutma merdiveni denetimi (reel-taste senaryosundan sonra)
Senaryoyu 3–5 sn'lik basamaklara böl ve her basamağa bak:
- İlk 2 sn: ses kapalıyken anlaşılan tek görüntü + hook var mı?
- Her basamak yeni bilgi ya da görsel değişim getiriyor mu? Getirmeyen basamak kesilir.
- Hiçbir basamak 5 sn'yi aşmıyor mu?
- Son 2 sn: ödül (vaat edilen sonuç) + tek çağrı var mı?
Eksik → hangi basamak, ne eksik, tek satır; düzeltme reel-taste'e döner.

## 3. Haftalık plan
Pzt–Paz tablosu: `gün · konu · hook kalıbı · yayın saati · durum`. Aynı hook kalıbı haftada en çok 2 kez; arka arkaya aynı tarif yok (reel-taste kuralıyla aynı).
