# brand-voice skill
ad: brand-voice skill
tur: skill
video: kMk4pvFJ13s
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Bilinmiyor; kaynak kod yok. Yalnızca talimat metni olduğundan ağ çağrısı beklenmez, ama doğrulanamadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-01-uzun)
## Ne
Ham metni marka sesine göre yeniden yazan bir Claude skill'i. Videoda ("5 Claude Skills That Will Be Worth $500K/Year by 2027") örnek olarak anılıyor; yayımlanmış bir repo ya da paket bulunamadı.
## Mekanizma
Video bulgusuna göre skill, talimat düzeyinde çalışıyor: ton sıcak, güvenli ve sade; fayda önde; kısa paragraf; tek net CTA. Kod veya harici bileşen olduğuna dair kanıt yok. Muhtemelen tek bir SKILL.md içindeki yazım yönergesi. Bu, çıkarım; doğrulanmadı.
## Kanıt
- Skill ham metni sıcak, güvenli, sade tonda; fayda önde, kısa paragraf ve tek CTA ile yeniden yazar. → sınanamadı · Video sayfası getirildi ama yalnızca YouTube sayfa iskeleti döndü; transkript yok. İddia yalnızca ön bulgudaki alıntıya dayanıyor. Skill'in kendisi yok, çalıştırılamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Repo/paket yok; kurulum komutu bilinmiyor.
- Kendi ortamımızda SKILL.md olarak sıfırdan yazılabilir.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Yazım tutarlılığı sağlar: aynı marka tonu her metinde uygulanır, elle yeniden yazma süresi azalır. Token tasarrufu sağlayan bir araç değil.
## Maliyet/risk
Kaynak doğrulanamıyor: repo, lisans ve bakım bilgisi yok. Video başlığı satış/abartı (clickbait) niteliğinde. Skill'in içeriği görülmedi, yalnızca kısa özet var. Genel bir ton tarifi, markaya özgü örnek ve yasak kelime listesi olmadan zayıf kalır.
## Üretilebilir
hedef_tur: skill
tarif: brand-voice/SKILL.md yaz. Frontmatter: name ve description (ne zaman tetiklenir: 'bu metni marka sesine çevir'). Gövde: (1) ton kuralları: sıcak, güvenli, sade; (2) yapı: ilk cümle fayda, paragraflar 2-3 cümle, sonda tek CTA; (3) yasaklar: jargon, abartı, birden fazla CTA; (4) 2-3 önce/sonra örneği; (5) çıktı biçimi: yalnızca yeniden yazılmış metin. Marka özelindeki kelime listesi ve örnekleri ayrı bir voice.md dosyasına koy.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-01-uzun/panel.md → Ömer sütunu
## Özellikler
### Ton: sıcak, güvenli, sade
kaynak: https://www.youtube.com/watch?v=kMk4pvFJ13s
### Fayda önde, kısa paragraf, tek net CTA
kaynak: https://www.youtube.com/watch?v=kMk4pvFJ13s
## Destek
- kMk4pvFJ13s · 3:04 · Ham metni marka sesine göre yeniden yazar: sıcak, güvenli, sade; fayda önde, kısa paragraf, tek CTA. · kanıt: Tone warm, confident, plain; lead with the benefit, short paragraph, one clear call to action.
