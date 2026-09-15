# Claude’a Awwwards Ödüllü Bir Website Yaptırdım | Yazılımcı Gözüyle
kanal: Yıldız Dikme · süre: 12 dk · altyazı: otomatik tr
ana iddia: Ödüllü bir sitenin premium hissini (3D galeri, perspektif, hover, loading, ayrı mobil kurgu) parça parça çözüp keskin ve sınırlayıcı tek bir prompt'a çevirince Claude benzerini sıfırdan tek gönderimde üretir (prompt önceden 5-10 kez denenmiş; "50-100 bin dolarlık site" iddiası kanıtsız).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| greensock/GSAP | YENİ | ELENDİ | galeri dönüşü/smooth akış için "kesinlikle" istendi; proje başına JS bağımlılığı, ortama kurulacak araç değil |
| Awwwards (awwwards.com) | ZATEN VAR | ELENDİ | ilham kaynağı ("2022 günün sitesi" iddiası); frontend-craft Bölüm 10 listesinde |
| prompt kısıtları: "tasarımı değiştirme, geliştirme yapma" · renk+fontu baştan sabitle · dosya yapısını ver (index.html, CSS, script.js, public/) · 5-10 kez deneme | ZATEN VAR | ELENDİ | Bölüm 0 (REF iyileştirilmez, marka kimliği kararı) · Bölüm 5 (çıktı yapısı) · Bölüm 7 (Renk/Tipografi) · Bölüm 9 (kapalı çevrim) |
| 3D galeride perspektifi açıkça iste | YENİ | BİLGİ | "perspektif" denmeden görseller düz geldi (sözlü deneyim, ölçüm/kanıt yok) |
| etkileşimi durum ve cihaz başına tarif et (hover/boşta/scroll/mouse; mobilde sürükle) | YENİ | BİLGİ | tek kod, desktop ve mobil ayrı davranış; Bölüm 3 yalnız hover/focus/active durumu istiyor |
| tasarıma uygun loading ekranı + dönerek giriş, yoğun görsel (136) | YENİ | ELENDİ | proje-özgü stil kararı, genel kural değil; Bölüm 3 "gereksiz animasyon yok" ile gerilimli |
| diğer: Hostinger, Netlify, Google Drive, yazarın prompt ürünü | YENİ | ELENDİ | sponsor/barındırma/prompt paylaşımı; Claude ortam aracı değil, ürün henüz çıkmadı |
## ölçütler (YENİ)
- greensock/GSAP: bakım=pushed 2026-04-13, 28.4k yıldız, arşivli değil · çift=örtüşme yok (ui-ux-pro-max'ta yalnız GSAP preset verisi var) · izin=projeye npm/CDN bağımlılığı · context=0 (ortama yüklenmez) · kurulum: —
- perspektif / etkileşim tarifi / loading ekranı (teknikler): bakım=— (teknik) · çift=örtüşme yok (etkileşim kısmen Bölüm 3 Interaktif) · izin=yok · context=yalnız kural satırı · kurulum: —
- diğer (Hostinger, Netlify, Google Drive, prompt ürünü): bakım=bilinmiyor · çift=örtüşme yok · izin=hesap/login (Hostinger ücretli, ürün abonelikli) · context=0 · kurulum: —
## hedefler (BİLGİ)
- 3D/derinlik efektinde perspektifi açık token olarak yaz → DESIGN.md şablonu (Token'lar)
- etkileşimi durum ve cihaz başına davranış olarak tarif et; hover'a bağlı etkileşime dokunmatik karşılık → frontend-craft Bölüm 3 (Interaktif)
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda (tam metin açıklamadaki Google Drive klasöründe)
- 3D görsel galeri; tek sayfa vanilla JS, "herhangi bir kütüphane kullanmadım" (React/Vue opsiyonel) ama GSAP zorunlu; tasarımı değiştirme, geliştirme yapma, dediğimin aynısını çıkar (sözlü özet, birebir değil)
- minimal mimarlık sitesi; kart üstünde değilken ortada site adı, üstüne gelince kartlar yumuşakça değişir; scroll'da saat yönü ve tersi döner; mouse yukarı-aşağı ile galeri hareket eder (sözlü özet, birebir değil)
- görsel sayısı verilir (136); dosya yapısı: index.html, genel CSS dosyası, tüm kod script.js, görseller public/ içinden (sözlü özet, birebir değil)
- renkler ve font en başta verilir, bunların dışına çıkma; perspektif kullan, öndeki kartlar ince/yanlamasına (sözlü özet, birebir değil)
- bilgisayar/tablet/mobil davranışı ayrı; tasarıma uygun loading ekranı, yüklenince galeri dönerek gelir; index.html kod iskeleti verilir, dışına çıkma (sözlü özet, birebir değil)
referans siteler: clouarchitects.com/projects (ilham; Unseen Studio? yapımı, "2022 günün sitesi" iddiası), awwwards.com, studio-3d-archive.netlify.app (videoda üretilen site)
stiller: minimal (mimarlık), 3D circular archive / üç boyutlu dairesel galeri
premium kararlar:
1) Perspektifli 3D dairesel galeri: öndeki kartlar ince/yanlamasına, scroll ile saat yönü-tersi dönüş, mouse ile yukarı-aşağı hareket, akış GSAP ile smooth
2) Hover detayı: kartlar yumuşakça kenara çekilip değişir, boştayken ortada site adı
3) Tasarıma uygun loading ekranı ve galerinin dönerek girişi; desktop ve mobil ayrı kurgu (mobilde tutup sağa-sola döndürme), tek kod tabanı
