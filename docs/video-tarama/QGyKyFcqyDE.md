# Prompt Yazmak Yetmiyor! Claude’dan İyi Sonuç Almanın Sırrı
kanal: Yıldız Dikme · süre: 21 dk · altyazı: otomatik tr
ana iddia: Sonucu prompt'un uzunluğu değil context'in bilgi kalitesi belirler; mevcut projeye hazır prompt eklemeden önce yeni sohbette Claude'a kod yazdırmadan analiz ettirip dokunulmaz alanları söyleyince yeni bölüm hero'yu bozmadan doğru yere girer (tek demo, ölçüm yok).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| hazır tasarım promptunu mevcut siteye entegre etme kısıtları: dokunulmaz alanı adlandır (hero, mevcut animasyonlar), prompttan yalnız ilgili bölümü al, loading ekranını ve port satırını çıkar | YENİ | BİLGİ | kısıtsız ilk denemede bölüm yerine ikinci hero eklendi, scroll efekti iki kez; ikinci denemede bozulma yok (yeni sohbet+analiz+kısıt aynı anda değişti, tek demo) |
| aktif MCP/skill sayısını sınırla | YENİ | BİLGİ | iddia: eklenen MCP ve skill her mesajda yeniden okunur, yazar en fazla 2 aktif MCP kullanıyor (ölçüm yok); kurulu sette 4 MCP + çok sayıda skill, bu ortamda MCP şemaları ertelenmiş (ToolSearch) |
| önce salt-okuma analiz ("kod yazma, sadece analiz"), analiz kalıbını skill ya da hafızaya kaydetme | ZATEN VAR | ELENDİ | superpowers:brainstorming/writing-plans (kurulu) + CLAUDE.md kod keşfi kuralı; skill/hafıza Claude Code yerleşik |
| uzun ya da ciddi hatalı sohbette üstelemeden yeni sohbet (context window dolunca kafa karışması) | ZATEN VAR | ELENDİ | CLAUDE.md context disiplini (dalga başı /clear, uzun aradan sonra yeni oturum); "ciddi hatadan sonra" tetikleyicisi ayrıca yazılı değil |
| context içeriği: rol, "premium ve sinematik" hedefi, hedef kitle, mobil performans · görsel/video verip önce analiz ettirme | ZATEN VAR | ELENDİ | Bölüm 0 (sektör/ürün araması, REF modu reference/ görselleri) · Bölüm 7 (Stil adı) · Bölüm 4 (perf) |
| promptta tekrar eden kelime/cümle ve dikkat dağıtan gereksiz bilgi kullanma | YENİ | ELENDİ | genel yazım tavsiyesi, ölçülebilir eşik yok; "promptlarımın %80-90 kaliteli çıktısı bundan" iddiası ölçümsüz |
| diğer: token/kredi ayrımı ve modele göre tokenizasyon, context bütçe grafiği (25k/50k/5k/2k/18k), "loop engineering", scroll ile videonun içine giriş efekti | YENİ | ELENDİ | kavramsal anlatım; rakamlar videoda "random, karışık hesaplama" diye belirtiliyor; loop engineering yalnız ad (ileride video); efektin yapımı anlatılmıyor |
## ölçütler (YENİ)
- teknikler (entegrasyon kısıtları, MCP/skill sınırı, tekrarsız prompt): bakım=— (teknik) · çift=entegrasyon kısmen Bölüm 1 "ikinci instance açma"; MCP sınırı kısmen CLAUDE.md context disiplini; tekrarsız prompt örtüşme yok · izin=yok · context=kurala yazılırsa ~1 satır; MCP/skill sınırı uygulanırsa kalıcı context azalır · kurulum: —
- diğer (token anlatımı, context bütçe grafiği, loop engineering, scroll-video efekti): bakım=bilinmiyor · çift=örtüşme yok · izin=yok · context=0 · kurulum: —
## hedefler (BİLGİ)
- mevcut sayfaya harici prompt/bölüm eklerken önce salt-okuma analiz; dokunulmaz alanlar (hero, mevcut animasyonlar) yazılı listelenir, prompttan yalnız ilgili bölüm alınır, ikinci loading ekranı ve ayrı port/sunucu ayarı alınmaz → frontend-craft Bölüm 0
- aktif MCP/skill setini işin gerektirdiğiyle sınırla, kullanılmayanı devre dışı bırak (videoda iddia: en fazla 2 aktif MCP) → CLAUDE.md (context disiplini)
---
## ek: tasarım
prompt:
- zayıf deneme: "Şimdi sana verdiğim bu promptu projeye yerleştirmeni istiyorum. Ortalarda bir alan set [seç?] yeni section olarak ekle" (sözlü)
- context örneği, prompt "bana bir web site yap" + context: "frontend geliştiricisiyim. Premium ve sinematik görünmeli. Hedef kitle yaratıcı ajanslar, mobilde performansı olmalı" (sözlü)
- genel analiz kalıbı: "bu projeyi baştan sona analiz etmeni istiyorum. Hem ön yüzünü, UI'ı hem arka tarafı backend kısmı varsa işte UEx'i [UX?] ve genel düşüncelerini işte dosya yapılarını her şeyini öğrenmeni istiyorum" (sözlü)
- yeni sohbette analiz: "Bu projeyi sadece detaylı bir şekilde incele. Herhangi bir kod yazma. Sadece analiz edeceğiz." (sözlü)
- entegrasyon: "Şu anda projede var olan animasyonları asla değiştirme kısını [hero kısmını?] bozmanı istemiyorum. Sayfanın diğer kısımlarını da asla bozma. Sana vereceğim prompta sadece ilgili kısmı almanı istiyorum." (sözlü)
- entegre edilen uzun tasarım promptu: metin altyazı/açıklamada yok — yalnız ekranda; içindeki loading ekranı alınmamalı (çift yükleme ekranı olur), port satırı silindi (proje zaten 3000 portunda) (sözlü özet, birebir değil)
referans siteler: yok
stiller: yok (isimli stil geçmiyor; yalnız "premium", "sinematik", "animasyonlu", "3D obje" nitelemeleri)
premium kararlar:
1) Context'i zengin yazmak: rol (frontend geliştirici), "premium ve sinematik" hedefi, hedef kitle (yaratıcı ajanslar), mobil performans; iddia: promptlarının %80-90 oranında kaliteli çıktı vermesinin sebebi bu (ölçüm yok).
2) Prompt içinde tekrar eden kelime/cümle ve dikkat dağıtan gereksiz bilgi kullanmamak (iddia: tekrar modeli "takılmaya" iter).
3) Hero'da oynayan video + scroll ettikçe "bir şeyin içine giriyormuş" hissi veren efekt; nasıl yapıldığı anlatılmıyor, sonraki videoya bırakıldı.
