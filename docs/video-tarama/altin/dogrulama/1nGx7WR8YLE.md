# 1nGx7WR8YLE: altın doğrulama günlüğü (2026-10-07)

Kaynaklar baştan sona okundu: aciklama · yorum · altyazi · groq · ocr (124 satır, tamamı). Şema kontrolü Python ile yapıldı: OK.

## Sayılar (önce → sonra)
| alan | önce | sonra |
|---|---|---|
| adaylar | 11 | 37 |
| linkler | 2 | 2 |
| site_ui | 3 | 10 |
| promptlar | 2 | 8 |
| komutlar | 0 | 0 |
| urller | 2 | 5 |
| is_akisi | 6 | 12 |

## EKLENEN adaylar (ad · tür · zaman · kaynak · kanıt)
- Topview MCP · MCP · 0:49 · ses · "Claude'la MCP kurarak bu videoyu üreteceğiz"; 2:58 mcp.topview.ai/mcp
- Codex · uygulama · 2:47 · ses · "Hem Codex'e hem Claude'a, Blender'a bağlayabiliyorsunuz"
- Blender · uygulama · 2:51 · ses · aynı cümle; 2:56 "Plugin for Blender"
- Pinterest · servis · 1:33 · ses · referans görsel kaynağı ("rezidans web site" araması)
- Behance · servis · 1:44 · ekran · pin kaynağı behance.net Luxury Residence case study
- Awwwards · servis · 0:34 · ekran · küçük resim "4 Claude Skills for Awwwards-Style Websites"; açıklamada "Awwwards tarzı"
- GPT Image 2.5 · model · 1:18 · ekran · Topview Image Edit "Select Model GPT Image 2.5 Flare" (belirsiz)
- Wan 3.0 · model · 2:56 · ekran · Topview yan menüsü (belirsiz: menüde göründü, kullanılmadı)
- Claude Code · uygulama · 3:18 · ekran · "Local | home-project", "Ran a command, read 2 files", "Type / for commands" (belirsiz: ad ekranda yazmıyor)
- Lighthouse · CLI · 11:55 · ekran · "...thouse scored 100 across all four categories" (belirsiz: OCR kısmi)
- Chrome DevTools · uygulama · 12:24 · ekran · "Dimensions: iPhone 14 Pro Max 430 × 932 | Elements | Console" (belirsiz: tarayıcı adı görünmüyor)
- Video akışı (görsel → video → site) · iş akışı · 0:42 · ekran · "VIDEO AKIŞI | VIDEO WORKFLOW" slaytı 03/04
- Villa fly-through Seedance promptu (sabit yorum) · prompt · 3:31 · yorum · "Bu promptu aşağıya bırakacağım"; sabit yorumda tam prompt
- Hard negatives · teknik · 3:18 · ekran · "No cuts / No scene changes / No dissolve"; 7:57 "HARD NEGATIVES"
- Giriş sürekliliği kuralı · teknik · 5:56 · ekran · "exterior → move forward ⇒ pass through the glass/opening → enter the interior"
- Başlangıç karesine dönüş (return shot) · teknik · 7:05 · ses · "evin nasıl girdiyse dışında da o şekilde"
- image_to_video (ilk/son kare) · teknik · 8:08 · ekran · "(25s, 16:9, image-to-video)"; yorumda first frame / end frame
- cut-and-extend · teknik · 0:00 · yorum · "Fix only the exit with cut-and-extend"
- Üretmeden önce onay iste · ipucu · 7:27 · ses · "promptu oku, ne anladığını söyle, onaylarsam üret"
- İki yapay zekayla çapraz kontrol · ipucu · 8:41 · ses · "ChatGPT'ye analiz ettiriyorum"; 9:34 "tek bir araç kullanmayın"
- Odada yavaşla, geçişte hızlan · ipucu · 4:21 · ses · "odanın içindeyken duruyor, bölümler arası hızlı geçiyor"
- Kamera hareketini drone/gimbal gibi tarif et · ipucu · 5:14 · ses · "fiziksel açıklarsanız yapay zeka çok iyi anlıyor"
- Videoda yazı üretme, metni kodla ekle · ipucu · 6:05 · ses · "çok iyi yazmıyor… ben kodla beraber yazıyorum"
- Prompt şablonunu genelleyip yeniden kullan · ipucu · 6:42 · ses · "bu genel bir şablon"
- Oda listesini ve sırasını prompta yaz · ipucu · 6:52 · ses · "yazmazsanız kendisi düşünür"
- Referans görseli doğru seç · ipucu · 2:35 · ses · "referans ilk görseli doğru seçmemiz gerekiyor"

## EKLENEN diğer alanlar
- site_ui +7: pinned sinematik sekans (11:47) · bölüm geçişleri (11:47) · sahne bazlı metin açılışları (0:24) · ayrı mobil yerleşim/responsive (11:55) · reduced motion (11:55) · videodan alınan karelerle bölüm görselleri (12:52) · italik editoryal tipografi (12:57). Ekranda ya da konuşmada kütüphane adı geçmiyor, kutuphaneler boş bırakıldı.
- promptlar +6: ChatGPT'ye yazı kaldırma (1:53 ses) · Claude'un final Seedance promptu (7:57) · onay mesajı "Approved, generate it with home-project.png" (7:57) · ChatGPT analizi (8:41 ses) · düzeltme mesajı (9:21) · "The exit at 22s has a cut, fix it and regenerate" (9:45).
- urller +3: https://mcp.example.com/mcp (3:09, Claude'un "Add custom connector" penceresindeki örnek URL) · https://pear.no/ (11:07, Astra promptundaki ilham sitesi) · localhost:4173 (11:55, OCR'da "t:4173"; Vite önizleme portu olarak çıkarım).
- is_akisi +6: Claude'un final promptunu okuma (7:57) · revize promptla üretim (9:19) · kare kontrolü ve çıkış düzeltmesi (9:45) · sonucu izleyip doğrulama (10:07) · DevTools'ta mobil test ve çözünürlük düşürme (11:57) · masaüstü gezinti (12:26).

## DÜZELTİLEN
- ffmpeg: tür "araç" → "CLI" ("araç" şemada geçerli bir tür değeri değil).
- Topview: tür "uygulama" → "servis" (web platformu). Alias'a Topvil (OCR), TopView AI ve topview.ai eklendi. MCP ayrı aday oldu.
- Seedance 2.5: zaman 0:00/açıklama → 0:34/ekran (kanal küçük resmi "VE SEEDANCE 2.5"). Alias'a seedance25 ve feetance 25 (OCR) eklendi.
- GPT Astra: 0:54/ses → 0:34/ekran. Alias'a "GPT-6 Astra" (11:07 model seçicideki resmi etiket) ve "Asra" (Groq) eklendi.
- Fable: 3:33 → 0:34 ("CLAUDE FABLE 5" küçük resmi). Alias'a Fable 5.1 (sohbette seçili model, effort High) ve Claude Fable 5.1 eklendi.
- Claude: 0:47/ses → 0:34/ekran.
- ChatGPT: 1:53/ses → 1:18/ekran. Alias'a Groq ve altyazının bozuk yazımları eklendi.
- scrollcraft: kanıt, OCR'daki "Use scrollcraft to design and implement the scroll experience" satırı oldu.
- promptlar: taslakta zorunlu "ozet" alanı yoktu, eklendi. 3:20 → 3:18 (OCR'daki ilk kare).
- urller: Behance URL'si kesikti, OCR'daki tam hâline (utm parametreleriyle) getirildi. mcp.topview.ai zamanı 2:58 → 2:45 (ilk göründüğü connector listesi).
- site_ui: oda etiketi tekniğinin zamanı 12:33 → 0:13 (ilk göründüğü kare; anlatım 12:33 mekanizmaya yazıldı). Scroll'a bağlı video mekanizmasına "scroll-controlled video progression" ve "yedi senkron sahne" eklendi. Çözünürlük düşürme maddesine Lighthouse 100 eklendi.
- is_akisi: Pinterest adımının araçlarına Pinterest ve Behance eklendi. MCP adımı 2:47 → 2:45 oldu ve Add custom connector ayrıntısı yazıldı. Onay ve üretim adımları sıralı alt adımlara ayrıldı.

## ÇIKARILAN / ALINMAYAN (gerekçe)
- Taslaktan çıkarılan bir şey yok.
- PowerPoint (5:06 ses) alınmadı: yalnız benzetme olarak geçiyor ("sunum dosyası gibi sahne koyuyor"), araç olarak kullanılmıyor.
- Claude connector dizinindeki adlar (2:45: Google Drive, Gmail, Google Calendar, Canva, Microsoft 365, Notion, Figma, Slack, HubSpot, Atlassian Rovo) alınmadı: arayüzde kendiliğinden görünen liste, videoda kullanılmıyor.
- Topview alt özellikleri (Canvas, AI Marketer, Film Studio, Drama Studio, Motion Studio, Avatar, Video Depth Extraction) alınmadı: platformun menü öğeleri.
- Wizerdui (Behance yazarı), VELOR, SEREIN, The Arc Residence alınmadı: stüdyo adı ve sitedeki marka adları.
- Bir izleyici yorumunda geçen "/plan modu" alınmadı: içerik üreticisi değil izleyici soruyor. Kaynağı yorum olduğu için komutlar alanına da girmiyor.
- iPhone 14 Pro Max alınmadı: DevTools cihaz ön ayarı (site_ui mekanizmasında geçiyor).
- komutlar boş kaldı: ekranda ve konuşmada terminal, CLI ya da slash komutu yok. ffmpeg yalnız yorumda düz yazı olarak geçiyor.

## Belirsiz kalanlar
- GPT Image 2.5: "Flare" eki ve videodaki rolü net değil. Yazı kaldırma ChatGPT'ye atfediliyor.
- Wan 3.0: yalnız Topview menüsünde görünüyor.
- Claude Code: arayüzden çıkarım. Ekranda "Local", "Ran a command" ve "Type / for commands" var, ama ad hiç yazmıyor.
- Lighthouse: OCR'da "thouse" olarak kısmi okunuyor.
- Chrome DevTools: tarayıcı adı görünmüyor.
- localhost:4173: OCR'da yalnız "t:4173" var.
- GPT Astra'nın çalıştığı arayüz ("What should we work on in villa-project-example?", "Approve for me", "Open in / Undo / Review") büyük olasılıkla Codex uygulaması. Adı ekranda geçmediği için is_akisi araçlarına yazılmadı.
