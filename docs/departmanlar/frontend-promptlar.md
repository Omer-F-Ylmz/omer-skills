# Site prompt kütüphanesi (frontend)

Videodan çıkan yapım promptu kalıpları; metin kopyalanmaz, kalıp yazılır. Kaynak: `video katman` (tur/etiket: prompt aday).

| kalıp | video | zaman | teknik | şablonda karşılığı | aday |
|---|---|---|---|---|---|
| referans siteyi kopyalama, atmosferinden ilham alan özgün tasarım iste | JfmAm3sxCSc | 2:01 | - | yok → bekleyen | jfm-yapim-promptu |
| kullanılacak teknolojileri tek tek say | JfmAm3sxCSc | 2:01 | 3D helezon galeri | şablon: teknoloji | jfm-yapim-promptu |
| dosya yapısını ayrı JS ve CSS dosyaları olarak belirt | JfmAm3sxCSc | 2:01 | 3D helezon galeri | şablon: dosya | jfm-yapim-promptu |
| galeri ayarlarını config dosyasında topla: görsel sayısı, hız, boşluk | JfmAm3sxCSc | 3:01 | 3D helezon galeri | şablon: config | jfm-yapim-promptu |
| ana sahneyi ayrıntılı, ikincil bölümleri kısa tarif edip ajana bırak | JfmAm3sxCSc | 3:01 | - | yok → bekleyen | jfm-yapim-promptu |
| düzeltme promptunda mevcut olanı bozma kısıtını açıkça yaz | JfmAm3sxCSc | 6:07 | - | yok → bekleyen | jfm-yapim-promptu |
| scroll ile tetiklenen yavaş yazı belirmesi iste | JfmAm3sxCSc | 6:07 | scroll reveal | şablon: hareket | jfm-yapim-promptu |
| sayfayı bölüm türlerine böl, her bölüm için ayrı prompt ver | JfmAm3sxCSc | 8:09 | bölüm kartları | yok → bekleyen | motionsites-ai-kopyala-yapistir-prompt |
| animasyonlu arka planı ayrı varlık olarak tanımla | JfmAm3sxCSc | 8:09 | animasyonlu arka plan | şablon: asset | motionsites-ai-kopyala-yapistir-prompt |
| "Tasarımı değiştirme, birebir üret" talimatı | NyNScAc2u_o | 3:37 | katı talimat tekrarı | şablon: kabul | nyns-3d-galeri-promptu |
| Dosya yapısını 4-5 kez tekrarlama (halüsinasyon önleme) | NyNScAc2u_o | 4:42 | redundant talimat | şablon: dosya | nyns-3d-galeri-promptu |
| Görselleri public/'a koy, AI otomatik alsın | NyNScAc2u_o | 4:42 | sabit klasör convention | şablon: asset | nyns-3d-galeri-promptu |
| Renk paleti ve fontu prompt başında sabitleme | NyNScAc2u_o | 5:44 | design-token önden kilitleme | şablon: config | nyns-3d-galeri-promptu |
| 3D perspective'i sayısal olarak belirtme (PERSPECTIVE 1600) | NyNScAc2u_o | 5:44 | CSS 3D transform parametresi | şablon: config | nyns-3d-galeri-promptu |
| Fisher-Yates shuffle ile görselleri kartlara dengeli dağıtma | NyNScAc2u_o | 4:42 | rastgele-dengeli dağıtım | şablon: asset | nyns-3d-galeri-promptu |
| Tüm sayısal sabitleri EXACT CONSTANTS altında toplama | NyNScAc2u_o | 6:14 | sabit-tablo izolasyonu | şablon: config | nyns-3d-galeri-promptu |
| E-ticaret sitesi yap, videoyu arka plana full yerleştir | jGJ09wdTGDI | 3:15 | asset referanslı prompt | şablon: asset | jgj0-claude-design-promptu |
| Kendi ürettiğim ürün görsellerini ver, bunları kullan de | jGJ09wdTGDI | 3:15 | asset zorunluluğu | şablon: asset | jgj0-claude-design-promptu |
| Premium, dark temalı, Shop Now CTA'li site iste | jGJ09wdTGDI | 3:15 | stil sıfatı + CTA belirtme | şablon: config | jgj0-claude-design-promptu |
| Ortadaki yazıyı kaldır, butonları köşeye al tek cümle | jGJ09wdTGDI | 5:36 | doğal dil revizyon | şablon: hareket | jgj0-claude-design-promptu |
| Bu web siteyi responsive yap tek cümle | jGJ09wdTGDI | 5:36 | doğal dil revizyon | şablon: kabul | jgj0-claude-design-promptu |
| AI üretimi kısa videoyu hero'ya scroll-scrub olarak yerleştir | 4cE9t4rE0-0 | 7:22 | scroll-timeline/GSAP ScrollTrigger | şablon: hareket | 4ce9-yat-sitesi-promptu |
| Aynı prompt akışını ürün türü değiştirerek tekrar kullan (yat/kahve/uçak) | 4cE9t4rE0-0 | 7:22 | parametrik prompt şablonu | yok → bekleyen | 4ce9-yat-sitesi-promptu |
