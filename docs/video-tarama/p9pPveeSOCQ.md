# Claude ile Premium Web Siteleri Yapmanın Sırrı | Claude Prompt Rehberi
kanal: Yıldız Dikme · süre: 11 dk · altyazı: otomatik tr
ana iddia: Aynı araç ve aynı görsellerle; marka, hedef kitle, tasarım dili, sayfa deneyimi ve teknik beklenti veren prompt premium site, genel prompt ise mavi-mor/neon, "yapay zekadan çıkmış" belli olan site üretir (yalnız görsel kıyas, ölçüm yok).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| diğer: Hostinger, React | YENİ | ELENDİ | Hostinger: açıklamada sponsor linki + indirim kodu, ücretli hosting, tasarım iş akışıyla ilgisiz · React: çok sayfalı/e-ticaret için önerilen stack, frontend-craft stack'i proje türünden (static/aspnet) belirliyor |
| Hedef kitle tanımı | YENİ | BİLGİ | SKILL.md'de hedef kitle alanı yok; video iddiası: e-ticarette buton ağırlığı, lüks sitede tasarım ağırlığı buna göre değişir |
| Sayfa deneyimi planı (bölüm yapısı + medya yeri) | YENİ | BİLGİ | belirtilmezse hero videosunun yerine AI karar verir (iddia); SKILL.md'de bölüm/medya yerleşim planı yok |
| Dört adımlı web prompt yapısı | ZATEN VAR | ELENDİ | marka → tasarım dili → sayfa deneyimi → teknik beklenti; Bölüm 0 + Bölüm 7 + Bölüm 8 kapsıyor, eksik parçalar yukarıda BİLGİ |
| Renk/font ve hareket brief'i (gold palet, lüks font, yumuşak scroll reveal, zarif hover, abartısız geçiş) | ZATEN VAR | ELENDİ | renksiz prompt → mavi-mor/neon iddiası; Bölüm 0 mor/indigo yasağı, Bölüm 3 YASAK/Animasyon/Interaktif, Bölüm 7 Renk/Tipografi/Hareket/aşırı glow |
| diğer: responsive'i açıkça isteme, semantik HTML/CSS + vanilla JS, ödüllü sitelerden ilham, asset klasörünü (public) belirtme, yeni portta açma, prompt'u marka adı/renk değiştirip yeniden kullanma, 4 adımı Claude/ChatGPT hafızasına verme | ZATEN VAR | ELENDİ | Bölüm 2/5 (390/768/1440, mobile-first, static çıktı), Bölüm 4 landmark, Bölüm 10, Bölüm 5 brand_assets/, Bölüm 1, Bölüm 7 DESIGN.md kalıcı hafıza, skill/CLAUDE.md |
## ölçütler (YENİ)
- Hostinger: bakım=bilinmiyor (repo yok, ticari servis) · çift=örtüşme yok · izin=ücretli hesap + login · context=yok (harici servis, Claude Code'a bağlanmıyor) · kurulum: —
- React: bakım=pushed_at 2026-09-15, 250456 yıldız, archived=false · çift=örtüşme yok (kurulu set stack değil; frontend-craft static/aspnet) · izin=proje başına npm bağımlılığı · context=yok (yalnız proje kodunda) · kurulum: —
- Hedef kitle tanımı: bakım=— (teknik, repo yok) · çift=örtüşme yok · izin=yok · context=SKILL.md'ye tek kural satırı, yalnız skill yüklenince · kurulum: —
- Sayfa deneyimi planı (bölüm yapısı + medya yeri): bakım=— (teknik, repo yok) · çift=örtüşme yok (Bölüm 5 yalnız "bölüm başına tek mesaj") · izin=yok · context=SKILL.md'ye tek kural satırı, yalnız skill yüklenince · kurulum: —
## hedefler (BİLGİ)
- Hedef kitle tanımı → frontend-craft Bölüm 0 (marka kimliği kararı ve ui-ux-pro-max sorgusu öncesi girdi)
- Sayfa deneyimi planı (bölüm sırası + medya yerleşimi, ör. hero'da video) → frontend-craft Bölüm 5 (İÇERİK)
---
## ek: tasarım
prompt:
kötü: "Lüks bir parfüm markası için güzel ve modern bir web sitesi yap. Etkileyici görünsün ve animasyonlar ekle." (sözlü)
iyi: "Cloud adına premium bir parfüm markası için responsive bir landing page boz" [ASR bozuk] (sözlü)
"Hedef kitlesi üst segment ürünlere ve görsel kaliteye önem veren kullanıcılar." (sözlü)
renk paleti altın/gold tonları, hero'da sinematik parfüm videosu oynatma istendi (sözlü özet, birebir değil); font adları ve sayfa yapısı metni altyazı/açıklamada yok — yalnız ekranda
"Yumuşak scroll reveal animasyonları." "zarif over effectleri kontrollü geçişler ekle. Animasyonları abartma." (sözlü)
"Masaüstüne sinematik bir deneyim oluştur. Mobilde düzeni sadeleştir. Ancak premium görünümü koru." (sözlü)
"Temiz ve semantik HTM CSS ve vanilya JavaScript kullan." (sözlü)
gönderirken ek: "yeni bir portta web siteyi aç." "Görselleri ve videoyu public dosyasının içerisinden al." (sözlü)
yeniden kullanım: "bundan sonra yazacağınız promplları bu dört adıma göre ver" (sözlü)
referans siteler: yok (adı verilmeden "ödül alan web siteleri" anılıyor; hostinger.com/YILDIZWEB yalnız sponsor linki)
stiller: premium/lüks, sinematik (hedef); neon/parlak, mavi-mor (kötü çıktı olarak)
premium kararlar:
1) Tasarım dilini açıkça vermek: altın/gold renk paleti (hover ve vurgulanan kelimelerde) ve lüks duran font; verilmeyince mavi-mor, neon, parlak çıktı (iddia, yalnız ekran kıyası)
2) Hero'da sinematik ürün videosu; masaüstünde sinematik deneyim, mobilde sadeleştirilmiş ama premium düzen
3) Yumuşak scroll reveal, zarif hover ve kontrollü geçişler; animasyonları abartmamak
