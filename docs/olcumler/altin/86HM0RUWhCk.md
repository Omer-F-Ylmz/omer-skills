# Altın set — 86HM0RUWhCk (site, 27:51) · "Building Beautiful Websites with Claude Code Is Too Easy" · Nate Herk | AI Automation

Özet (kalem): Araç/servis/ürün 9 · Açıklama bağlantıları 2 · Kurulum/komutlar 0 · Teknikler 9 · Kural/ipucu/iş akışı 6 · Promptlar 3 · Kareden bilgi 6 · Emin olunmayanlar 4 = 39

## Kaynaklar
- .kos/altin/86HM0RUWhCk/kaynak.txt (yt-dlp -J açıklama + 10 bağlantı + 8 bölüm; altyazı en-orig oto, 56 satır/30 sn; `tools/video/altin_mozaik.py`, seçim motorun `dil_sec`i)
- .kos/altin/86HM0RUWhCk/mozaik-01..12.png (45 kare, ~37 sn aralık, 2×2)
- Tekil tam çözünürlük kare (3): kare-006 (03:04 CLAUDE.md), kare-009 (04:55 tweet), kare-044 (26:24 buton özeti). Bu karelerden okunan kalem `[tekil]` işaretli.
- Motor raporu/paneli/adayları, paket.md, docs/video-tarama ve frontend kütüphanesi AÇILMADI.

Kanıt biçimi: zaman · kaynak (altyazı|kare|açıklama) · "alıntı ≤15 kelime" · önem.

## Araç/servis/ürün (9)
1. frontend-design skill/plugin (Anthropic) · skill · UI'ı "vibe coded" görünümden çıkarır · 04:55 kare [tekil] "/plugin marketplace add anthropics/claude-code" · yüksek
2. Claude Code VS Code eklentisi · IDE eklentisi · ajan paneli · 00:30 altyazı "click on extensions and you're going to type in cloud code" · orta
3. Puppeteer · kütüphane · ekran görüntüsü döngüsü · 09:00 altyazı "we're just doing this using Puppeteer" · yüksek
4. 21st.dev · bileşen kataloğu · tekil bileşen (arka plan, buton, shader) · 17:30 altyazı "a website called 21st.dev, which has some of the best website components" · yüksek
5. Vercel · barındırma · GitHub'dan otomatik dağıtım · 21:30 altyazı "we set up a really cool autodeploy between Verscell and GitHub" · yüksek
6. GitHub · sürüm kontrolü · dağıtım hattının kaynağı · 22:00 altyazı "push these changes to GitHub, GitHub grabs the new changes" · orta
7. Dribbble / Godly / Awwwards · ilham siteleri · referans site bulma · 10:00 altyazı "one example called Dribble ... godly website ... Awards" · orta
8. Chrome DevTools "Capture full size screenshot" · tarayıcı özelliği · referans sitenin tam sayfa görüntüsü · 10:30 altyazı "control shiftp and search for screenshot" · orta
9. placehold.co · yer tutucu görsel servisi · CLAUDE.md kuralında · 03:04 kare [tekil] "images via `https://placehold.co/`" · düşük

## Açıklama bağlantıları (2)
1. https://x.com/trq212/status/1989061937590837678 · frontend-design plugin duyurusu · açıklama "Frontend Design Skills" · yüksek
2. skool.com/ai-automation-society (ücretsiz topluluk) · CLAUDE.md dosyası buradan indiriliyor · 02:30 altyazı "web designcloud.mmd file, which is the one we're going to be using" · orta
(Diğer 8: sponsor/sosyal/kurs bağlantıları; aday değil.)

## Kurulum/komutlar (0)
- yok

## Teknikler (9)
1. CLAUDE.md'yi sistem istemi gibi kullan, kısa tut · 02:00 altyazı "Just think of it as a system prompt" · yüksek
2. brand_assets klasörü (logo + marka kılavuzu) ve @ ile etiketleme · 05:00–06:00 altyazı "I'm going to call this brand_assets" · yüksek
3. Screenshot loop: ajan kendi çıktısını görüntüleyip iki tur düzeltir · 13:00 altyazı "two rounds at least of comparing" · yüksek
4. Site klonlama: tam sayfa ekran görüntüsü + Elements'ten kopyalanan stil kodu birlikte verilir · 11:00 altyazı "in the style section down here I'm just going to copy everything" · yüksek
5. Önce klonla, sonra kendi marka varlıklarını işlet · 15:00 altyazı "work in our brand assets" · yüksek
6. Tekil bileşeni 21st.dev "copy prompt" ile al, hero arkasına işlet · 18:00 altyazı "copy this prompt right here" · yüksek
7. Animasyonlu öğede screenshot döngüsünü kapat (sonsuz aşırı mühendislik) · 19:00 altyazı "it gets stuck in this loop" · yüksek
8. Değişiklikleri önce localhost'ta dene, açık izinle push et · 25:30 altyazı "Don't push it to GitHub until I tell you to." · yüksek
9. Geçici ekran görüntülerini temizle / adlandırma kuralı koy · 13:30 altyazı "more specific about the naming convention of the screenshots" · orta

## Kural/ipucu/iş akışı (6)
1. Her oturumda ön uç kodundan önce frontend-design skill çağrılır · 03:04 kare [tekil] "before writing any frontend code, every session, no exceptions" · yüksek
2. Referans görsel varsa düzen/boşluk/tipografi/renk birebir eşlenir · 03:04 kare [tekil] "match layout, spacing, typography, and color exactly" · yüksek
3. Referans varken tasarım "iyileştirilmez" · 03:04 kare [tekil] "Do not improve or add to the design." · yüksek
4. Referans yoksa sıfırdan yüksek zanaatla tasarla · 03:04 kare [tekil] "design from scratch with high craft (see guardrails below)" · orta
5. Çıktıyı ekran görüntüsüyle referansa karşı karşılaştır · 03:04 kare [tekil] "Screenshot your output, compare against reference, fix" · yüksek
6. Gizli bilgi (API anahtarı, parola) herkese açık repoya itilmez · 23:30 altyazı "Make sure that you're not putting any of your sensitive information" · orta

## Promptlar (3)
1. Tek cümle + varlık etiketi: 06:08 kare "build me a modern and professional landing page for our community called AI Automation Society." · yüksek
2. Klon istemi: 11:40 kare "I want you to spin up a new website for us ... clone this website" + Screenshot: + Style: · yüksek
3. Animasyon istemi: 19:02 kare "Because this is an animated background, do not use the Screenshot tool to compare." · yüksek

## Kareden bilgi (6)
1. Beş adımlı çerçeve: CLAUDE.md → Frontend Design Skill → Screenshot Loop → Inspiration Websites → Individual Components · 27:00 kare · yüksek
2. Screenshot loop dosyaları: screenshot.mjs, serve.mjs, localhost:3000; ekran görüntüleri "temporary screenshots/" · 07:59 kare "screenshot.mjs ... serve.mjs" · orta
3. 21st.dev isteminde shadcn + Tailwind + TypeScript varsayımı · 18:25 kare "shadcn project structure - Tailwind CSS - Typescript" · orta
4. VS Code ayarı "Allow Dangerously Skip Permissions" · 12:53 kare "Recommended only for sandboxes with no internet access." · orta
5. Buton parıltısı sonucu: gradyan #62ccff → #4FC1FF → #2ea8e8, hover'da animasyon durur · 26:24 kare [tekil] "Gradient surface — #62ccff → #4FC1FF → #2ea8e8" · düşük
6. Ajan kendi ön bellek notunu MEMORY.md'ye yazıyor (serve.mjs/screenshot.mjs yoktu) · 09:12 kare "Let me save the workflow notes to memory" · düşük

## Emin olunmayanlar (4)
1. CLAUDE.md'nin 9. satırdan sonrası (screenshot workflow bölümü, guardrails) hiçbir karede okunamadı; içerik yalnız anlatımdan (09:00).
2. Tweet'teki ikinci kurulum komutu (plugin install satırı) karede kesik; yalnız marketplace satırı görünür.
3. 21st.dev'den seçilen bileşenin adı ("Background Paths" kartı 17:48'de imleç üstünde) kesin değil; anlatımda "hero waves" deniyor.
4. "Bypass permissions" riski anlatıcı tarafından hafife alınıyor (12:30); öneri olarak alınmamalı.
