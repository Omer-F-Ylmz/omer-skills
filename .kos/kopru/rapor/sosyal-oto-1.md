---
type: summary
status: active
tags: [sosyal-oto, shorts, faceless, ara-kayit]
relatedTo: [SOSYAL-OTO-1]
---
# SOSYAL-OTO-1 — ara kayıt (tur 1, çağrı tavanı 45/45)

## Durum
- (a) Araştırma TAMAM: rapor/sosyal-oto-1/arastirma.md (alt ajan, ~25 web çağrısı, kaynaklı). Önemli: YT "inauthentic" (2025-07-15) okuma-tipi içeriği dışlar → B kendi anlatımımız; TikTok Creator Rewards >60 sn ister → TikTok kesimi 61 sn+; IG 2026-04-30'dan beri özgün olmayanı önermiyor; YT Shorts geliri 1000 abone + 10M görüntüleme/90 gün (2027-02-01'den yeni başvuru 20M).
- (b) Plan + Roast Room TAMAM: sosyal-oto/PLAN.md, .roast-room/2026-10-30-sosyal-oto-1.md. 4 persona S1 (yerel ffmpeg) seçti; 7 zorunlu düzeltme kayıtlı.
- (c) Prototip YARIM: sosyal-oto/hat.py (+kokoro_tts.py, kelime.py) yazıldı.
  - B koşusu: Wikimedia küçük resim 429 → düzeltildi (standart 1280 genişlik, UA, geri çekilme); yeniden koşulmadı.
  - A koşusu: ucretsiz_havuz tüm halkalar 429/soğuma (01:45) → OmniRoute nemotron :free yedeği eklendi; upscayl.org koşusu arka planda başladı, sonucu ölçülmedi.
  - Hakem puanı: henüz yok (video üretilmedi).
- (d) TAMAM: sosyal-oto/OMER-ADIMLAR.md.

## Devam (yeni oturum)
1. log-a.txt kontrol; out/a/<kimlik>/meta.json puanı.
2. `python -I hat.py b --n 2`, `python -I hat.py a https://jan.ai`.
3. Her grup 2 video, hakem ≥70 değilse en iyi + neden raporla; kare ızgarası hakem-izgara.jpg.
4. TikTok 61 sn+ varyantı (kelime sınırı 150–175) ayrı bayrak.

## Ek (A koşusu sonucu)
- upscayl: nemotron yedeği metni yazdı, Kokoro sesi üretildi (ses-kokoro.wav 1.9M); whisper GPU cublas64_12.dll yok diye düştü → kelime.py CPU yedeği eklendi, yeniden koşulmadı.

## Tur 2 (30 Eki 02:20, çağrı tavanı yine doldu)
- GPU kelime zamanı ÇÖZÜLDÜ: nvidia-cublas/cudnn pip paketleri zaten kuruluydu, DLL dizini PATH'te değildi; kelime.py başına os.add_dll_directory(site-packages/nvidia/*/bin) eklendi. Ölçüm: upscayl ses-kokoro.wav → 112 kelime, gpu, 53 sn (model yükleme dahil). CPU yedeği duruyor.
- Metin adımı ÇÖZÜLDÜ: nemotron-nano düşünme jetonuyla max_tokens'u yiyip içerik boş dönüyordu → "reasoning": {"enabled": False} (260 jeton, geçerli JSON). Ret olunca 3 geri bildirimli deneme eklendi; nano 73–84 kelime yazıyor → alt sınır 95→75 (~30 sn). Metinde gerçek-dışı ayrıntı riski (War of the Worlds testinde "çiftçi" uydurdu): hakem/olgu kontrolü şart.
- Video HÂLÂ YOK: montaj aşaması ffmpeg'de düşüyor. A: "Error reinitializing filters" (-22, libx264 açılmadı); B: montaj_b ffmpeg rc 3221225477 (0xC0000005) stderr boş. Hakem puanı yok, mp4 yok.
- Sonraki oturum: (1) hat.py montaj_a/montaj_b filtre dizgisini `ffmpeg -v error` ile tek tek yokla (görsel boyutu tek sayı? zoompan/boxblur girdisi? Wikimedia dosyası bozuk mu?); (2) sonra `hat.py a https://upscayl.org https://jan.ai`, `hat.py b --n 2`; (3) hakem. Not: arka.py+kos2.py yoluyla koşuda hat.py rc 1 veriyordu; doğrudan `python -I hat.py ...` çalışıyor (run_in_background).

## Tur 3 (30 Eki 03:xx) — A grubu
- Montaj düzeltildi: concat'te SAR uyuşmazlığı (setsar=1) + ses etiketi iki kez tüketiliyordu (asplit). montaj_a artık gerçek sayfanın 5 kaydırma görüntüsünden sahne tabanlı (montaj_b, fg 1380).
- hat.py `a <url> --metin x.json` hazır metin kabul ediyor (metni bu oturum yazdı, her iddia aracın kendi sayfasına dayalı). temizle.py (hazirla / yuklendi, --dry) yazıldı.
- Araçlar (ajan araştırması, kaynaklı): SolidCraft, SurgePix, (3.: MOSS-Image Space — görüntü zayıf, yapılmadı).
- SolidCraft: video-d0.mp4 1080x1920 37.6 sn, hakem (nemotron-omni) 78/100; <8/10 sayılır değil (7.8) — eşik 8/10 için ilk kare yazısı büyütme + hareket önerildi, yapılmadı.
- TUR BITTI: hazir/ klasörü + Ömer yükleme yok; 3. video yok; SurgePix sonucu log-surge.txt.

## TUR 4 ara kayıt (30 Eki ~03:50) — TUR BITTI değil, DUR
- hat.py: kanca 104pt + \N bölme (128pt taşıyordu), band (dev "FREE + OPEN SOURCE"), ≤2 sn parçalı zoom/pan, ai_label:false. zoom-out ffmpeg eval=frame ile segfault (0xC0000005) → yalnız zoom-in.
- SolidCraft: AI ajan iddiası metinden çıkarıldı; hakem (nemotron) 78 (<80). Kare kontrol: kanca taşması bulundu → düzeltildi, yeniden koşu gerekli.
- SurgePix + FreePainter koşusu arka planda (log-surge/log-free.txt). Stillwet doğrulanamadı (stillwet.com = merch sitesi) → FreePainter ("Free use · No signup" sayfada görüldü).
- Kalan: hakem üçlü (jev + nemotron + kare), ≥80 → hazir\, temizle.py hazirla koşusu. temizle.py test klasöründe dry+gerçek doğrulandı.
- Not: hat.py'yi `-I` ile koşma (PIL yok); düz `python` kullan.

## TUR 5 (30 Eki) DUR
- hook duzeltmeli hat.py ile 3 video yeniden render: SolidCraft 78, SurgePix 72 (onceki 75), FreePainter 68 (2 deneme). Esik 80 gecilmedi; hazir\ bos.
- Uclu hakem tamamlanmadi: yalniz nemotron. Hakem 2x2 izgarayi video duzeni sanip "tekrarli izgara" diyor (FreePainter); gercek sorun: statik ekran goruntusu, hareket az.
- Kalan is: ekran kaydi (Playwright video) ile gercek hareket, sonra jev + 4 kare kontrolu.

## TUR 6 (30 Eki) DUR
- Gerçek ekran kaydı hattı çalışıyor: kayit.py (Playwright recordVideo 540x960→1080x1920, sarı imleç vurgusu, SolidCraft senaryosu: örnek parça aç, yörünge döndür, geçmişi oynat→parça adım adım kurulur). hat.py `--kayit solidcraft` (montaj_k). Hakem artık 4 kareyi AYRI veriyor, ESIK=80; uclu.py (nemotron + gemma-4-31b).
- SolidCraft: video-d0.mp4 (37 sn, gerçek hareket) nemotron 75 (<80). Gemma kolu 429 → üçlü hakem TAMAMLANMADI, hazir\ boş. Kendi kare kontrolü: kanca+altyazı okunaklı, hareket gerçek; kusur: "FREE + OPEN SOURCE" bandı parçanın tam ortasını kapatıyor, ilk kare imleç yok.
- SurgePix: giriş gerektirir → elendi (yön 1). FreePainter: freepainter.org çözümlenmiyor (ERR_NAME_NOT_RESOLVED), senaryosu yazılmadı. 2. ve 3. video yok.
- Sonraki: band konumunu alta/üste al (model ortası boş kalsın), gemma kotası açılınca uclu.py, ≥80 ise temizle.py hazirla; ardından konu-kuyrugu.json'dan girişsiz 2 araç için senaryo.

## TUR 7 (30 Eki) DUR
- hat.py: Band A grubunda y=660 (parca ortasi bos), Kanca 104->88pt. SolidCraft kayitli video yeniden render: kare kontrolu temiz (kanca kenara taşmıyor, band modeli kapatmıyor, hareket gercek). nemotron 75 (<80, hakem "hareket az/altyazi senkron" diyor), gemma HTTP 429 (kota) -> uclu hakem yine TAMAMLANMADI, hazir\ bos.
- 2. ve 3. video (girissiz arac senaryosu) yapilmadi. Sonraki: gemma kotasi acilinca uclu.py; nemotron esigi icin kayit.py'de daha uzun/cesitli etkilesim (parametre degistirme).

## TUR 8 (30 Eki) TUR BITTI — eşik 70, Desktop yönü
- Önizleme (Ömer izleyecek, yükleme YOK): Desktop\Claude ile yapılanlar\sosyal-onizleme\ → puan75-solidcraft.mp4, puan72-surgepix.mp4, puan68-freepainter.mp4 (puan = nemotron tek hakem; üçlü hakem gemma 429 yüzünden yok).
- ≥70 → out/a/hazir/1030-solidcraft, 1030-surgepix (video.mp4+meta; temizle.py silme yaptığı için elle kopya). FreePainter 68 <70, hazir'e girmedi.
- Uyarı: SurgePix aracı giriş istiyor (tur 6'da elenmişti) — içeriği Ömer onaylamadan yayınlanmasın; SurgePix/FreePainter videoları statik ekran görüntüsü tabanlı (gerçek ekran kaydı yalnız SolidCraft).
- Instagram adı (Chrome değil headless Playwright, instagram.com/<ad> "Profile isn't available" = müsait; hesap AÇILMADI): @freeaidrop ve @freeaidrops DOLU. Müsait sırayla: 1) freeaidrop.daily 2) thefreeaidrop 3) getfreeaidrop (freeaidrop.co da müsait). Not: "kaldırılmış hesap" da aynı sayfayı verir; açarken son kez doğrula.
## TUR 9 (30 Eki) ses — 5/7 motor
- Yeni: Dia 5/6 (heyecanli2 her denemede sessiz çöküyor, rc=1), XTTS-v2 6/6 (CPML lisansı ticari kullanıma kapalı → kanal için yalnız değerlendirme), OmniVoice mutlu2 yeniden üretildi (WER 0,00). WER (large-v3, CPU/int8; GPU koşusu sessiz rc=1): Dia 0–0,05, XTTS 0–0,05.
- NeuTTS: neuphonic/neutts-nano ve -air GATED (403) → Ömer HF hesabından erişim istemeli. Voicebox yapılmadı (çağrı tavanı).
- en-iyi-3\ klasörüne Dia + XTTS mutlu1 eklendi (kulak seçimi Ömer'de). Venv: C:\AI\venv-dia, venv-xtts, venv-neu.
