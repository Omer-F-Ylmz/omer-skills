# Claude’a Ödüllü Sitelerden İlham Alarak Site Yaptırdım | Yazılımcı Gözüyle
kanal: Yıldız Dikme · süre: 14 dk · altyazı: otomatik tr
ana iddia: Detaylı teknik bir prompt'la Claude, ödüllü bir siteden ilham alan sıvı (fluid) efektli premium portfolyo sitesini üretir; aynı prompt'la sonuç %90 benzer çıkar (iddia, ölçüm gösterilmiyor).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| mrdoob/three.js | YENİ | ELENDİ | sitenin sıvı efekti (ASR "3GS"); sayfa kütüphanesi, Claude ortamına kurulacak araç değil |
| greensock/GSAP | YENİ | ELENDİ | akan yazı animasyonu (ASR "GSEP"); sayfa kütüphanesi, kurulum kalemi değil |
| Efekt ayarlarını ayrı config dosyasında tutma | YENİ | BİLGİ | dönüş süresi, kenar gölgesi, efekt genişliği, akışkanlık tek dosyada |
| Dokunmatikte mouse efekti yerine kendi kendine dönen efekt | YENİ | BİLGİ | iPhone 14 Pro Max'te mouse yok, efekt yine de hareket ediyor |
| diğer: Hostinger, Netlify, YildizDikme/threejs-fluid-reveal-portfolio, "ilk prompt İngilizce", "prompt'a matematiksel işlem koy" | YENİ | ELENDİ | Hostinger sponsor/ücretli hosting; Netlify yalnız canlı demo; repo örnek çıktı; iki prompt tekniği ölçümsüz iddia, formül metni altyazıda yok |
| diğer: "ilham al, kopyalama" (Bölüm 10), teknoloji+dosya yapısı+font brief'i (Bölüm 5/7), görselleri proje klasörüne koyma (Bölüm 0 brand_assets/), mobil kontrol (Bölüm 2 390px), beyaz zemin üstü beyaz yazı düzeltmesi (Bölüm 4 kontrast), hover/parlama (Bölüm 3), Claude Design (claude-design MCP) | ZATEN VAR | ELENDİ | frontend-craft SKILL.md'de kural ya da kurulu |
## ölçütler (YENİ)
- mrdoob/three.js · greensock/GSAP: bakım=three.js pushed 2026-09-15, 115552★, arşiv değil / GSAP pushed 2026-04-13, 28425★, arşiv değil · çift=örtüşme yok (context7 yalnız dokümanını, ui-ux-pro-max yalnız GSAP preset verisini verir) · izin=yok (CDN/proje bağımlılığı) · context=0 · kurulum: —
- Efekt ayarlarını config dosyasında tutma: bakım=— (teknik) · çift=DESIGN.md Hareket alanı süre+easing'i kısmen kapsar · izin=yok · context=kurala eklenirse SKILL.md'ye 1 satır · kurulum: —
- Dokunmatik otomatik hareket: bakım=— (teknik) · çift=örtüşme yok (Bölüm 3 yalnız hover/focus-visible/active ve prefers-reduced-motion der) · izin=yok · context=kurala eklenirse SKILL.md'ye 1 satır · kurulum: —
- diğer: bakım=örnek repo pushed 2026-05-21, 9★, arşiv değil; Hostinger/Netlify bilinmiyor (servis) · çift=örtüşme yok · izin=Hostinger ücretli hesap, Netlify login · context=0 · kurulum: —
## hedefler (BİLGİ)
- WebGL/canvas efekt ayarlarını (süre, genişlik, gölge, akışkanlık) tek config dosyasında toplama → frontend-craft Bölüm 5
- Mouse/hover'a bağlı efektin dokunmatikte kendi kendine hareket eden bir durumu olmalı → frontend-craft Bölüm 3
---
## ek: tasarım
prompt:
Ana prompt: metin altyazı/açıklamada yok — yalnız ekranda (açıklamada yalnız Google Drive prompt linki var)
Sıfırdan proje oluştur; gösterilen ödüllü siteden ilham al, kesinlikle aynısını kopyalama; orijinal kişisel portfolyo sitesi (sözlü özet, birebir değil)
Teknolojiler: JavaScript, Three.js, CSS; dosya yapısı: index.html, script.js, shader.js (sözlü özet, birebir değil)
Sıvı efekt için config dosyası (belirli saniyede dönme, kenar gölgesi, genişlik, akışkanlık) + matematiksel işlemler + font stilleri (sözlü özet, birebir değil)
hero kısmındaki yazıları sayfa ile uyumlu farklı bir renk yapar mısın? Biraz daha dark renk seç. Bu sayede beyaz arka plandan ayrılsın. (sözlü)
referans siteler: landonorris.com
stiller: yok
premium kararlar:
1) Mouse hareket etmese de sürekli dönen sıvı efekt; mouse ile üstte ikinci (kasklı) fotoğrafı açığa çıkaran reveal — "ödüllü bir web site diye düşünürdüm" (iddia)
2) Tüm sitede görselle uyumlu çizgili formun korunması + GSAP ile akan yazı
3) Aşırı detaylı teknik prompt (teknoloji, dosya yapısı, config ayarları, matematiksel işlemler, fontlar); detaylı prompt İngilizce verilmeli (iddia, ölçüm yok)
4) Baş harfleri büyütüp farklı renk yapma ve üstüne gelince artan parlama efekti
