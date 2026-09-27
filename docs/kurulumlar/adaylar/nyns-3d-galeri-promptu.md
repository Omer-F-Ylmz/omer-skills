# nyns-3d-galeri-promptu
ad: nyns-3d-galeri-promptu
tur: prompt
video: NyNScAc2u_o
repo: yok
arastirma: yarım: tur tavanı (12 tur · 67.9k token · araştırıcı rapor dönmedi; DENE verilmez, karar ÖĞREN/UYARLA sınırında)
## Ne
Yıldız Dikme'nin CLOU (Unseen Studio, Awwwards SOTD 2022) mimarlık sitesinden ilham alıp Claude'a verdiği 3D dairesel (ring) görsel galeri site yapım promptu. Vanilla JS + GSAP, tasarımı değiştirmeme talimatı, sabit design-token/geometri/sabitler. Kaynak: paket.md + docs/video-tarama/2026-09-28-NyNScAc2u_o.md + kare k00374_0.jpg (prompt ekran görüntüsü, DESIGN TOKENS/CORE GEOMETRY/EXACT CONSTANTS bölümleri).
## Kanıt
CLOU, Unseen Studio, Awwwards Site of the Day 21 Haz 2022, skor 7.62/10 (Design 7.77 · Usability 7.05 · Creativity 8.04 · Content 7.92) — bağımsız kaynakla doğrulandı. Aynı teknik (3D ring, preserve-3d) daha önce `docs/kurulumlar/bekleyen/teknik-3d-dairesel-ring-galeri-kart-dizilimi-transform-style-preserve-3d.md` içinde onaysız kayıtlı; bu aday aynı bulguyu tekrarlıyor, tekrar KUR edilmez.
## Prompt anatomisi
bolumler: 1) proje tanımı + teknoloji (vanilla JS + GSAP) 2) tasarımı değiştirmeme talimatı 3) davranış (hover/scroll/mouse/loading) 4) REQUIRED ASSETS 5) DESIGN TOKENS 6) CORE GEOMETRY 7) EXACT CONSTANTS
hareket: hover'da yumuşak kayma/uzaklaşma · scroll'a bağlı saat yönü/tersi rotasyon · mouse-Y parallax (yukarı/aşağı) · intro'da dönerek açılan loading screen · mobilde drag ile rotasyon
teknoloji: vanilla JavaScript (framework yok) + GSAP (sürüm görünmedi); CSS 3D transform (perspective, preserve-3d)
dosya: index.html · styles.css · script.js · public/ (image-1.png…image-15.png); dosya yapısı hallüsinasyonu önlemek için promptta 4-5 kez tekrarlanıyor
config: DESIGN TOKENS (--bg #f4f3f1, --ink #0d0d0d, --muted #8a8a86, --line rgba(0,0,0,.16), font Helvetica Neue/-apple-system); EXACT CONSTANTS (PERSPECTIVE 1600, ITEM_COUNT 136, TURNS 1, ROT_Y 86, RING_SCALE 0.88, PARALLAX 4, HOVER_OUT 16, HOVER_Z 12, HOVER_SCALE 1.02, MOBILE breakpoint 768px, MOBILE_DRAG_SPEED 0.35)
asset: 15 mimari fotoğraf public/'a konur, Fisher-Yates shuffle ile 136 karta dengeli/rastgele dağıtılır (eksik dosya = kırık görsel, inşa durmaz)
kabul: yazılı ölçüt yok; yazarın kendi dumanı: refresh'te intro rotasyonu, scroll cw/ccw, mouse parallax, hover kayma, mobilde drag+loading — hepsi çalışmalı
### Kalıplar
- "Tasarımı değiştirme, birebir üret" talimatı · 3:37 · teknik: katı talimat tekrarı · şablon: kabul
- Dosya yapısını 4-5 kez tekrarlama (halüsinasyon önleme) · 4:42 · teknik: redundant talimat · şablon: dosya
- Görselleri public/'a koy, AI otomatik alsın · 4:42 · teknik: sabit klasör convention · şablon: asset
- Renk paleti ve fontu prompt başında sabitleme · 5:44 · teknik: design-token önden kilitleme · şablon: config
- 3D perspective'i sayısal olarak belirtme (PERSPECTIVE 1600) · 5:44 · teknik: CSS 3D transform parametresi · şablon: config
- Fisher-Yates shuffle ile görselleri kartlara dengeli dağıtma · 4:42 · teknik: rastgele-dengeli dağıtım · şablon: asset
- Tüm sayısal sabitleri EXACT CONSTANTS altında toplama · 6:14 · teknik: sabit-tablo izolasyonu · şablon: config
## Özellikler
### 3d-dairesel-ring-galeri
ne: 136 kartı 360°'ye eşit aralıkla (inc=360/136) dağıtıp preserve-3d sahnede tilt+rotasyonla döndüren galeri
kurulum: yok (prompt tekniği, kütüphane değil)
lisans: yok
etiket: teknik
karar: ZATEN VAR
gerekce: zaten var: docs/kurulumlar/bekleyen/teknik-3d-dairesel-ring-galeri-kart-dizilimi-transform-style-preserve-3d.md (aynı video, onaysız bekliyor)
### scroll-mouse-parallax-rotasyon
ne: scroll ile saat yönü/tersi rotasyon, mouse-Y ile PARALLAX=4 sabiti kadar dikey kaydırma
kurulum: yok (GSAP ile rotationZ/translateY güncellemesi, prompt fikri)
lisans: yok
etiket: teknik
karar: UYARLA
gerekce: fikir: scroll/mouse olaylarını tek ortak açı fonksiyonuna (angleOf) bağlamak · hedef: departman-frontend prompt şablonu notu · kod yazılmaz
## Mekanizma
### 3d-dairesel-ring-galeri
nasıl: her kart iki iç içe eleman (hitbox + görünen çocuk); hitbox'a rotationZ=angleOf(kart) verilir, uzak transform-origin sayesinde sadece rotationZ değiştirerek kart ringin etrafında döner; görünen çocuğa sabit rotateY=86 verilip sadece ölçek animasyonlanır
neden: DOM/CSS transform ile 136 elemanı tek matematik formülüyle konumlar; WebGL/canvas yazmadan 3D his verir
koşul: kart sayısı arttıkça (>200) CSS transform reflow maliyeti artar; düşük GPU'da preserve-3d katman sayısı sınırlanmalı
bizde: departman-frontend prompt şablonuna not; kütüphane kurulmaz
### scroll-mouse-parallax-rotasyon
nasıl: ortak angleOf(kart)=idx*inc-90+ringOffset+introOffset fonksiyonu scroll, drag ve intro'yu aynı state'e yazar; mouse-Y sadece PARALLAX sabiti kadar ek offset ekler
neden: tek state kaynağı senkron rotasyonu garantiler, çakışan animasyon yarışını önler
koşul: yalnız sürekli scroll/mouse etkileşimli tek-sayfa sahnelerde kazandırır; form-ağırlıklı/kısa oturumlu sitede fayda yok
bizde: uygulanmadı; fikir departman-frontend notuna eklenebilir
## Bağımsız kanıt
- https://www.awwwards.com/sites/clou — CLOU, Unseen Studio, Site of the Day 21 Haz 2022, skor 7.62/10.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| CLOU 2022'de Awwwards Site of the Day, puan 7,62/10 | awwwards.com/sites/clou | doğru | skor ve tarih birebir eşleşiyor | - |
| Tam profesyonel site fiyatı 50.000-100.000 dolar | yok | doğrulanamadı | yazarın kişisel tahmini, kaynak gösterilmedi | - |
| Prompt hazırlığı ~2 gün sürüyor, 5-10 kez test ediliyor | yok | doğrulanamadı | doğrulanamayan kişisel iddia | - |
