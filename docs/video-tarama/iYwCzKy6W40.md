# Claude’a Premium 3D Web Sitesi Yaptırdım | Yazılımcı Gözüyle
kanal: Yıldız Dikme · süre: 14 dk · altyazı: otomatik tr
ana iddia: Teknolojiyi (WebGL/Three.js/React Three Fiber) adlandıran, pozisyon ve font değerlerini kesin veren teknik bir prompt ve doğru 3D modelle Claude sıradan olmayan, scroll animasyonlu premium bir 3D site üretir.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| mrdoob/three.js, pmndrs/react-three-fiber, greensock/GSAP | YENİ | ELENDİ | 3D sahne (WebGL) + scroll animasyon kütüphaneleri; proje başına bağımlılık, Claude Code kurulumu değil; Bölüm 3 "gereksiz kütüphane yok" (GSAP yalnız açıklamada geçiyor) |
| Lighthouse (Chrome DevTools) | ÇİFT | ELENDİ | perf skoru ölçümü; frontend-craft audit.mjs perf kabulüyle (Bölüm 4) kısmen örtüşür; %96 / %92 desktop / %92 mobil skorları iddia, altyazıdan doğrulanamaz |
| diğer: Sketchfab, YildizDikme/3d-camera-landing-page, Hostinger, Netlify | YENİ | ELENDİ | kurulacak araç değil: ücretsiz 3D model sitesi, videonun çıktı reposu, hosting (Hostinger sponsor linki, Netlify demo adresi) |
| teknikler: font stil/px değerlerini kesin ver, elle ayarlı pozisyonları "asla değiştirme" diye kilitle, lokalde ayağa kaldırıp göster, mobil/tablet/desktop kontrol, "diğer kısımlara dokunma" | ZATEN VAR | ELENDİ | Bölüm 2 tolerans + Bölüm 7 Tipografi; Bölüm 0 REF "iyileştirilmez" + Bölüm 7 kalıcı hafıza; Bölüm 1; Bölüm 2 (390/768/1440); CLAUDE.md cerrahi değişiklik |
| teknikler: prompt'ta stack'i adlandır, sahne+ışık+kamera ayarını iste, intro bitene kadar scroll kilidi, tek seferde tutmazsa tekrar dene | YENİ | ELENDİ | stack Bölüm 0'da proje türünden gelir; sahne/ışık/kamera Three.js'in zaten zorunlu temeli; scroll kilidi a11y/reduced-motion riski (Bölüm 3); tekrar deneme kural değil |
| 3D model: düşük detaylı GLB (2 MB) seç, 6 MB değil | YENİ | BİLGİ | iddia: 6 MB "performansı çok etkiler, yavaş açılır"; ölçüm gösterilmiyor |
| Three.js resmi sitesi örnek galerisi (threejs.org?) | YENİ | BİLGİ | videodaki kamera fikrinin ilham kaynağı; kopyalanmadan, dönüş animasyonu artırılarak uyarlandı |
## ölçütler (YENİ)
- three.js / react-three-fiber / GSAP: bakım=three.js pushed 2026-09-15 ★115552 · R3F pushed 2026-09-13 ★32308 · GSAP pushed 2026-04-13 ★28425, hiçbiri arşivli değil · çift=örtüşme yok (ui-ux-pro-max'ta yalnız GSAP preset verisi var) · izin=proje başına npm bağımlılığı · context=0 (Claude Code'a yüklenmez) · kurulum: —
- diğer (Sketchfab, 3d-camera-landing-page, Hostinger, Netlify): bakım=3d-camera-landing-page pushed 2026-05-27 ★8 arşivli değil; servisler bilinmiyor · çift=örtüşme yok · izin=Hostinger ücretli hosting (sponsor), diğerleri bilinmiyor · context=0 · kurulum: —
- teknikler (GLB boyutu, Three.js galerisi, stack adlandırma, sahne/ışık/kamera, scroll kilidi): bakım=— (teknik) · çift=örtüşme yok · izin=yok · context=kurala yazılırsa SKILL.md'de ~1 satır · kurulum: —
## hedefler (BİLGİ)
- 3D model kullanılıyorsa düşük detaylı, küçük GLB tercih edilir (videoda 2 MB) → frontend-craft Bölüm 4 (perf)
- 3D/WebGL yönü aranırken Three.js resmi sitesindeki örnek galerisi referans alınır, kopyalanmaz → frontend-craft Bölüm 10
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda (tam metin açıklamadaki Google Drive "Prompt Linki"nde)
- teknik kısım: React Three Fiber / Three.js (WebGL) kullan, çok modern animasyonlu bir web site yap (sözlü özet, birebir değil)
- dosyaların nasıl kullanılacağını teknik olarak tarif et, komponentlere ayır (sözlü özet, birebir değil)
- kritik: animasyon pozisyonlarını "kesinlikle atlama", animasyonları ve yerlerini değiştirme (sözlü özet, birebir değil)
- 3D model için sahne, ışık ve kamera ayarlarını yap; konumları kamerayı bozmayacak şekilde ver (sözlü özet, birebir değil)
- font stilleri, boyutları, px değerlerini aynen uygula, "asla sözümden çıkma" (sözlü özet, birebir değil)
- bitince projeyi bilgisayarımda lokalde ayağa kaldır, göster; mobil ve bilgisayar için performansa dikkat et (sözlü özet, birebir değil)
- düzenleme: "Bu kısmı değiştir ama sayfadaki diğer kısımlara sakın dokunma" (sözlü)
referans siteler: Three.js resmi dokümantasyon/örnek siteleri (URL verilmiyor), sketchfab.com/3d-models/canon-eos-5d-mark-iv-33001ed6f05042d89ac8690ffaaed0a4, 3d-camera-landing-page.netlify.app (sonuç), github.com/YildizDikme/3d-camera-landing-page
stiller: yok (stil adı geçmiyor; yalnız "premium", "modern animasyonlu" nitelemeleri)
premium kararlar:
1) Sıradan "site yap" yerine teknolojiyi (WebGL/Three.js, React Three Fiber) adlandıran teknik prompt + doğru 3D model (Sketchfab'dan ücretsiz Canon EOS 5D Mark IV, 2 MB GLB).
2) Kamera/model pozisyonlarını elle tek tek ayarlayıp scroll'a bağlı dönüş: kullanıcı arka, yan, her yeri görür, sonda yan durur; Claude'a "asla değiştirme" denir (iddia: "cloud bu şekilde ayarlayamaz").
3) Loading ekranında yavaşça dönen model + animasyon bitene kadar scroll kilidi; üstten vuran ışıkla kenar parlaması.
