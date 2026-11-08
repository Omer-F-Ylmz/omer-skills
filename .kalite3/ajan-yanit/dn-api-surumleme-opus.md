Not: Çalışma dizini (C:\Users\pc\AppData\Local\Temp\olcum-w4mophgy) boş; incelenecek API kodu yok. Bu yüzden kanıtlar yüklenen skill dosyasından geliyor: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10\skills\api-and-interface-design\SKILL.md

1. Alan silme/yeniden adlandırma (yanıtta ya da istekte) KIRICI · kanıt: SKILL.md:141 · öneri: yeni alanı yanına ekle, eskisini deprecated işaretle, yalnız /v2'de kaldır.
2. Tip ya da format değişikliği (string→int, tarih formatı, enum anlamı) KIRICI · kanıt: SKILL.md:142 · öneri: eskisinin yanına yeni tipte yeni bir alan ekle (priorityLevel gibi); tipi asla yerinde değiştirme.
3. Yeni zorunlu istek alanı/parametresi ya da daha sıkı doğrulama KIRICI · kanıt: SKILL.md:125 (ek yap, değiştirme) · öneri: varsayılanı olan opsiyonel alan olarak ekle; zorunluysa yeni sürümde.
4. URL, HTTP metodu, durum kodu ya da hata gövdesi değişikliği KIRICI · kanıt: SKILL.md:340 · öneri: Asp.Versioning ile /api/v{n} rota sürümü, ProblemDetails şeklini sabit tut.
5. Belgelenmemiş davranış (sıralama, varsayılan sayfa boyutu, null yerine boş dizi) Hyrum yasası gereği KIRICI · kanıt: SKILL.md:22, :331 · öneri: gözlenebilir her davranışı sözleşme say, contract/snapshot testiyle kilitle.
6. Opsiyonel alan, yeni endpoint, yeni enum değeri KIRICI DEĞİL (istemci bilinmeyen değeri tolere ediyorsa) · kanıt: SKILL.md:125 · öneri: minor sürüm, aynı /v1.
7. Sürüm sayısı · kanıt: SKILL.md:33, :332 · öneri: aynı anda en fazla 2 major sürüm, kalıcı fork yok.
8. Eski sürümü kaldırma takvimi (öneri): T0 v2 yayını + v1 yanıtlarında `Deprecation` ve `Sunset` header'ları; T+3 ay v1 erişim logundan istemcilere bildirim; T+6 ay v1 sadece okunur ya da 299 uyarısı; T+9-12 ay v1 410 Gone.

Atlananlar: dosya incelenmediği için repoya özel bulgu yok; takvim süreleri varsayım, istemci SLA'sına göre ayarlanmalı.