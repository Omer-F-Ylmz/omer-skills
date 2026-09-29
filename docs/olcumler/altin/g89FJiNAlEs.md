# Altın set — g89FJiNAlEs (uzun token, 15:07) · "4 Free Repos That Cut Claude Code Token Usage" · Eric Tech

Özet (kalem): Araç/servis/ürün 4 · Açıklama bağlantıları 4 · Kurulum/komutlar 7 · Teknikler 6 · Kural/ipucu/iş akışı 2 · Promptlar 0 · Kareden bilgi 5 · Emin olunmayanlar 4 = 32

## Kaynaklar
- .kos/altin/g89FJiNAlEs/kaynak.txt (yt-dlp -J açıklama + 5 bağlantı + 6 bölüm; altyazı en-orig oto, 30 satır/30 sn; `tools/video/altin_mozaik.py`, seçim motorun `dil_sec`i)
- .kos/altin/g89FJiNAlEs/mozaik-01..04.png (30 kare, 30 sn aralık, 3×3)
- Tekil tam çözünürlük kare (2): kare-005 (02:01 rtk Quick Start), kare-012 (05:34 headroom Get started). Bu karelerden okunan kalem `[tekil]` işaretli.
- Motor raporu/paneli/adayları, paket.md, docs/video-tarama ve frontend kütüphanesi AÇILMADI.

Kanıt biçimi: zaman · kaynak (altyazı|kare|açıklama) · "alıntı ≤15 kelime" · önem.

## Araç/servis/ürün (4)
1. RTK (rtk-ai/rtk) · CLI proxy + hook · bash çıktısını kırpar (girdi jetonu) · açıklama "RTK proxies your bash commands and trims 60-90% off CLI output" · yüksek
2. Headroom (headroomlabs-ai/headroom) · istek proxy'si · konuşma geçmişini sıkıştırır (girdi jetonu) · açıklama "Headroom compresses conversation history without /compact losing context" · yüksek
3. Ponytail (DietrichGebert/ponytail) · Claude Code plugin/skill · daha az kod yazdırır (çıktı jetonu) · açıklama "Ponytail makes agents write less code for the same result" · yüksek
4. Graphify (Graphify-Labs/graphify) · bilgi grafiği · kod tabanı haritası, grep turlarını keser · açıklama "Graphify maps your codebase so agents stop grepping back and forth" · yüksek

## Açıklama bağlantıları (4)
1. https://github.com/rtk-ai/rtk · açıklama "Repos:" listesi · 00:30 kare "CLI proxy that reduces LLM token consumption by 60-90%" · yüksek
2. https://github.com/headroomlabs-ai/headroom · açıklama "Repos:" listesi · 05:03 kare "Compress tool outputs, logs, files, and RAG chunks" · yüksek
3. https://github.com/DietrichGebert/ponytail · açıklama "Repos:" listesi · 10:37 kare "MIT license" · yüksek
4. https://github.com/Graphify-Labs/graphify · açıklama "Repos:" listesi · karede repo sayfası gösterilmiyor · yüksek
(skool.com/erictech: topluluk reklamı, aday değil.)

## Kurulum/komutlar (7)
1. rtk kurulumu (macOS) · 01:31 kare "brew install rtk" · orta
2. rtk kancasını küresel kur · 02:01 kare [tekil] "rtk init -g  # Claude Code / Copilot (default)" · yüksek
3. rtk diğer ajanlar için · 02:01 kare [tekil] "rtk init -g --codex", "rtk init --agent hermes" · düşük
4. rtk tasarruf ölçümü · 02:30 altyazı "I can just run RDK gain" + 03:02 kare "rtk gain" · yüksek
5. headroom kurulumu · 05:34 kare [tekil] "uv tool install --python 3.13 \"headroom-ai[all]\"" (videoda npm seçildi, 05:30 altyazı) · yüksek
6. headroom ile ajan sarma + panel · 05:34 kare [tekil] "headroom wrap claude  # wrap a coding agent" / "headroom dashboard" · yüksek
7. ponytail plugin kurulumu · 10:37 kare "/plugin marketplace add DietrichGebert/ponytail" + "/plugin install ponytail@ponytail" · yüksek

## Teknikler (6)
1. Bash çıktısını LLM'e girmeden önce filtrele (hook ile otomatik yeniden yazım) · 02:01 kare [tekil] "git status  # Automatically rewritten to rtk git status" · yüksek
2. /compact yerine kayıpsız sıkıştırma (özetleme bağlam kaybettirir) · 04:30 altyazı "if we were summarize it, we will lose context" · yüksek
3. Her oturumu sarılmış ajanla başlat · 05:34 kare [tekil] "it is recommended you launch a wrapped agent session each time" · orta
4. Çıktı jetonunu kod satırı azaltarak düşür (1000 satır ≈ 1000 jeton) · 09:30 altyazı "1,000 lines of code here cost 1,000 tokens" · orta
5. Kod tabanını bir kez haritala, ajan grep yerine haritayı okusun · 12:30 altyazı "map your entire codebase once into a file or like a JSON file" · yüksek
6. Girdi (rtk+headroom) ve çıktı (ponytail) katmanlarını birlikte kullan · 13:39 kare "RTK (hook) → Bash Run → Compression → LLM API" · orta

## Kural/ipucu/iş akışı (2)
1. rtk anonim kullanım metriği topluyor; istemeyen reddeder · 02:00 altyazı "RTK collects anomous usage for the metrics once a day" · orta
2. ponytail plugin kapsamı: kullanıcı ya da proje; videoda proje kapsamı seçildi · 10:30 altyazı "I personally just going to choose the option two" · düşük

## Promptlar (0)
- yok

## Kareden bilgi (5)
1. rtk gain ilk ölçüm: 6 komut, 100 jeton (17.9%) tasarruf · 03:02 kare "Tokens saved: 100 (17.9%)" · orta
2. rtk gain ikinci ölçüm: 15 komut, 212 jeton (27.0%) · 03:32 kare "Tokens saved: 212 (27.0%)" · orta
3. headroom panel: 3.8M → 3.7M, 39.8k kaydedildi (%1.1) · 08:05 kare "SAVINGS 1.1%" · orta
4. headroom panel "Tool-schema deferral" 33.6k jeton · 07:35 kare "TOOL-SCHEMA DEFERRAL 33.6k tokens" · düşük
5. Mesaj maliyeti üçgensel büyür (her mesaj öncekileri yeniden gönderir) · 04:33 kare "Each new message resends every previous one" · orta

## Emin olunmayanlar (4)
1. Graphify'ın kurulum komutu ve repo sayfası videoda hiç gösterilmedi; yalnız kavram diyagramı (12:08) ve açıklama bağlantısı var.
2. Headroom'u videoda npm ile kurduğu söyleniyor ("mpm install for headroom"), README'deki npm paketi "TypeScript SDK" olarak etiketli; CLI'ın npm ile gelip gelmediği belirsiz.
3. "60-90%" iddiası README/açıklamadan; videodaki kendi ölçümü %17.9–27.0.
4. Ponytail önceki bir videoya atıfla kısa geçildi; skill içeriği/modları gösterilmedi.
