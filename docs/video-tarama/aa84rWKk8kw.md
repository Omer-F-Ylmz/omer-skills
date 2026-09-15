# Claude ile Premium Web Sitesi Reklamı Ürettim (Fable 5 + Seedance 2.5)
kanal: Yıldız Dikme · süre: 15 dk · altyazı: otomatik tr
ana iddia: Tek ürün görseli ve kısa bir brief'le, Topview içinde Claude Fable 5 + Seedance 2.5 kullanarak ekip/stüdyo olmadan 30 sn premium reklam videosu üretilip prompt ve clip edit ile düzeltilebilir (sponsorlu video).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Topview AI | YENİ | ELENDİ | sponsor (ASR: Tabiew/TWV/TW); Fable 5 + Seedance 2.5 tek platformda, Canvas/Clip Edit/timeline özellikleri; ücretli, web arayüz aracı değil |
| Seedance 2.5 | YENİ | ELENDİ | ASR "CDS 2.5"; sesli video üretim modeli, Topview içinden ücretli; Claude Code'a kurulan araç değil |
| revizyonda yeniden tasarım yasağı ("yalnız belirli kısmı düzenle") | ZATEN VAR | ELENDİ | CLAUDE.md (cerrahi değişiklik) + frontend-craft Bölüm 7 (DESIGN.md miras alınır, yeniden üretilmez) |
| kısa brief: stil + tek mesaj + süre/format + tek referans görsel | ZATEN VAR | ELENDİ | frontend-craft Bölüm 0 (REF modu, tek satır karar), Bölüm 7 stil listesi (Dark/Premium), Bölüm 5 (bölüm başına tek mesaj) |
| hata listesi → düzeltme promptu → yeniden üretim (tek prompt yetmez) | ZATEN VAR | ELENDİ | frontend-craft Bölüm 2/9 tur döngüsü; videoda düzeltme sıfatla ("ışığı artır"), sayı yok, taşma hatası düzelmedi |
| exploded-view ürün kurgusu (parçalara ayrıl → içine gir → yerine otur) | YENİ | ELENDİ | video reklam senaryosu, web arayüz kuralı değil; konuşmacı Apple/Nike'ın "kalıplaşmış" kalıbı diyor |
| reklam videosunu web sitede scroll'a bağlı animasyonla kullanma | YENİ | ELENDİ | yalnız niyet ("yapacağım"), bu videoda gösterilmiyor; kural çıkaracak ayrıntı yok |
## ölçütler (YENİ)
- Topview AI: bakım=bilinmiyor (GitHub repo yok) · çift=örtüşme yok (kurulu sette video üretimi yok) · izin=login + ücretli plan/kredi (iddia: Ultra yıllık planda Seedance 2.5 60 gün sınırsız, kanıt yok) · context=0 (Claude Code dışı web platformu) · kurulum: —
- Seedance 2.5: bakım=bilinmiyor (GitHub repo yok) · çift=örtüşme yok · izin=Topview hesabı + kredi · context=0 (harici platformda model) · kurulum: —
- exploded-view ürün kurgusu: bakım=— (teknik) · çift=örtüşme yok · izin=yok; uygulamak video üretim aracı ister · context=yok · kurulum: —
- scroll'a bağlı reklam videosu: bakım=— (teknik) · çift=örtüşme yok (Bölüm 3 animasyon kuralları scroll videosunu kapsamıyor) · izin=yok · context=yok · kurulum: —
## hedefler (BİLGİ)
- yok
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda (videoda "promptu aşağıya bırakacağım" deniyor, açıklamada prompt yok)
- İlk prompt: karanlık, minimal, premium ("Dark Premium stüdyolu") reklam; mesaj "gürültüyü geride bırakın, önemli olana odaklanın"; 30 sn, 16:9; referans tek metalik kulaklık görseli (sözlü özet, birebir değil)
- İlk prompt akışı: 0-3 sn kulaklık → tek sıra halinde parçalarına ayrılır → kulaklığın içine girilir → çıkılır, parçalar yerine oturur (sözlü özet, birebir değil)
- Düzeltme promptu: 30 sn videoyu düzenle; en başta yeniden tasarım yasağı; parçalar ekrandan taşmasın; içine girilince ışık animasyonu artsın (sözlü özet, birebir değil)
- "Asla tasarım yapma. Sadece belirli kısımları düzenleyeceğiz" (sözlü; konuşmacının prompttan aktardığı ifade, ekrandaki metinle birebirliği doğrulanamaz)
- Clip edit: aynı düzeltme promptu yalnız seçili sahne aralığına yapıştırılıp "start edit" (sözlü özet, birebir değil)
referans siteler: topview.ai (açıklama, sponsor linki); tasarım referans sitesi yok — Apple ve Nike yalnız reklam kalıbı örneği olarak geçiyor (sözlü)
stiller: karanlık/dark, minimal, premium, Dark Premium stüdyo
premium kararlar:
1) Uzun teknik prompt yerine kısa brief + tek ürün görseli: yalnız stil (karanlık, minimal, premium), tek mesaj, 30 sn, 16:9; sonucu "şahane" diye niteliyor, ölçüm yok
2) Exploded-view kurgusu: ürün tek sıra halinde parçalara ayrılır, kamera içine girer ("gürültüyü almıyor" hissi), parçalar yerine oturur; Apple/Nike'ın kalıplaşmış reklam kalıbı
3) Düzeltme turunda yeniden tasarım yasağı + yalnız hatalı sahneyi clip edit ile düzenleme; yine de taşma hatası düzelmedi, çoklu prompt gerektiği kabul ediliyor
