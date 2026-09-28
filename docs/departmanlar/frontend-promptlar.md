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
| 3D perspektif ve eğimi promptta sayıyla açıkça yaz | NyNScAc2u_o | ? | 3D kart sahnesi | şablon: perspektif | kural-3d-perspective |
| görselleri public/ klasörüne koy, ajana klasörden aldır | NyNScAc2u_o | ? | - | şablon: klasör | kural-görselleri-public |
| video promptunu sahne sahne kamera, ışık ve atmosferle tarif et | 4cE9t4rE0-0 | ? | video üretimi | şablon: sahne | kural-detaylı-video-prompt |
| Ödüllü siteyi bölüm bölüm inceleyip ilham alma | b-LZ_Y9wor8 | 0:51 | tasarım analizi iş akışı | yok → bekleyen | blz-sinematik-portfoy-promptu |
| Dosya yapısını promptta zorunlu kılma (modele bırakmama) | b-LZ_Y9wor8 | 7:42 | redundant talimat | şablon: dosya | blz-sinematik-portfoy-promptu |
| Uzun/detaylı prompt ile %90-100 birebir sonuç hedefleme | b-LZ_Y9wor8 | 6:41 | ayrıntı seviyesi arttırma | şablon: kabul | blz-sinematik-portfoy-promptu |
| Her şey hazır olana kadar loading screen ekletme | b-LZ_Y9wor8 | 9:08 | yükleme durumu koruması | şablon: hareket | blz-sinematik-portfoy-promptu |
| Kaydırmaya bağlı kağıt fiziği slider tarifi | b-LZ_Y9wor8 | 3:47 | drag+inertia fizik | şablon: hareket | blz-sinematik-portfoy-promptu |
| 3D modeli stack adıyla ver: model + R3F/Three.js birlikte | iYwCzKy6W40 | 5:04 | React Three Fiber | şablon: teknoloji | lumen-sitesi-promptu |
| Dosya yapısını bileşen bileşen yaz, projeler arası aynı kalsın | iYwCzKy6W40 | 5:04 | bileşen ayrımı | şablon: dosya | lumen-sitesi-promptu |
| Elle ayarlanmış pozisyonları "atlama, değiştirme" diye kilitle | iYwCzKy6W40 | 5:04 | kritik blok | yok → bekleyen | lumen-sitesi-promptu |
| 3D'de sahne, ışık ve kamera ayarını ayrı ayrı iste | iYwCzKy6W40 | 5:04 | Three.js scene/light/camera | şablon: config | lumen-sitesi-promptu |
| Font stilini ve piksel boyutlarını prompt'ta belirt | iYwCzKy6W40 | 5:04 | tipografi tokenları | yok → bekleyen | lumen-sitesi-promptu |
| Uzun/detaylı prompt yazma — tasarım kararlarını adım adım anlatan uzun prompt yazarak %90-100 birebir sonuç almak | b-LZ_Y9wor8 | ? | - | yok → bekleyen | uzun-detaylı-prompt-yazma |
| Her şey hazır olana kadar loading screen — görsel/3D obje yüklenirken sitenin bozuk görünmesini önlemek için yükleme ekranı eklemek | b-LZ_Y9wor8 | ? | - | yok → bekleyen | her-şey-hazır-olana-kadar-loading-screen |
| Globe/dünya haritası footer — "global" marka mesajı vermek için footer'a noktalı dünya küresi koymak | b-LZ_Y9wor8 | ? | - | yok → bekleyen | globe-dünya-haritası-footer |
| Teknik prompt yazımı (teknoloji + stil belirtme) — Genel "site yap" yerine teknoloji/stil/kamera davranışını açıkça yazarak sıradanlıktan kaçınma | iYwCzKy6W40 | ? | - | yok → bekleyen | teknik-prompt-yazımı-teknoloji-stil-beli |
| fontlara, görsellere, boşluklara çok dikkat et | fCc97Rv-60w | 2:01 | tipografi/boşluk kalite çıtası | OLASI TEKRAR (DESIGN.md (frontend-craft:15) p=0.45) · bekleyen/olasi-klasik-prompt-sablonu-fontlara-gorsellere-bosluklara-cok-dik.md | klasik-prompt-şablonu |
| intro bölümünü bozma, sonrasını tamamla | fCc97Rv-60w | 2:01 | korunan bölüm + kapsam sınırı | OLASI TEKRAR (kalıp:12 p=0.50) · bekleyen/olasi-klasik-prompt-sablonu-intro-bolumunu-bozma-sonrasini-tamamla.md | klasik-prompt-şablonu |
| Awwwards seviyesinde yap, oradaki tasarım kurallarını uygula | fCc97Rv-60w | 2:01 | dış kalite referansı | yok → bekleyen | klasik-prompt-şablonu |
| önceki 4 skill'i kullan | fCc97Rv-60w | 3:03 | skill yığını | yok → bekleyen | klasik-prompt-şablonu |
| bu 4 skill'i kullan | 39IlNR-P3-Q | 8:47 | skill hatırlatması | K4: kalıp:50 (p 0.78) | scroll-site-promptu |
| bu videoyu referans al, kopyalama, ilham al | 39IlNR-P3-Q | 8:47 | referans video → tasarım | K4: kalıp:7 (p 0.70) | scroll-site-promptu |
| tüm cihazlarda çalışsın | 39IlNR-P3-Q | 10:56 | responsive kabul | OLASI TEKRAR (kalıp:27 p=0.57) · bekleyen/olasi-scroll-site-promptu-tum-cihazlarda-calissin.md | scroll-site-promptu |
