# Yarım tarama — 27 Eki 2026

Üretim: `.kos/kopru/yarim_tara_27.py` (salt-okur). Birim: iş ailesi (…-devam/-r1/-rd/-lm kopyaları birleşik). 720 aile, 93 SONRA, 284 ek-kaynak satırı, 178 işlenmemiş video linki.

## Özet sayılar

- BİTTİ kanıtlı: **372**
- KOŞMUŞ-BİTMEMİŞ: **213**
- HİÇ GİRMEMİŞ: **121**
- ÖMER-KARARI: **14**
- SONRA (yarım sayılmaz): 93
- işlenmemiş video linki: 178

Kural: BİTTİ kanıtlı = son log BİTTİ/sonuç var + (rapor/<ad>.md ya da git commit konusunda ad) ve güçlü eksik kalıbı yok; KOŞMUŞ-BİTMEMİŞ = DUR/KURTAR-ATLA/BÜTÇE/'eksik kaldı' ya da kanıtsız sonuç; ÖMER-KARARI = sonuç metninde karar/onay/yükleme beklentisi; HİÇ GİRMEMİŞ = ne sonuç ne log. Model tahmini görev metni/kuyruk `model=` alanından sezgiseldir. 'Yapılmadı' geçen BİTTİ satırlarında `not:` ile işaretli.

## Tablo (iş · grup · son durum · ne kaldı · tahmini model)

| iş | grup | son durum | ne kaldı | model |
|---|---|---|---|---|
| beyin-canli-1 | beyin | ÖMER-KARARI | bekliyor. - `beyin-ozet.md` en çok 20 satır; SessionStart'ta oturuma giriyor. **Neden durmuştu (d):** `onay/beyin_dusun.py uygula` hiç koşul | sonnet |
| graphify-ultra-1-d2 | graphify | ÖMER-KARARI | karar gerekiyor: 1. Kancayı kendi CC'ne de almak ister misin? Onay betiği `--kuru` ile hazırlanır, sen koşarsın. 2. Artık 332 MB'a inen artı | haiku |
| graphify-ultra-1-d6 | graphify | ÖMER-KARARI | bekliyor. Kalan G0 ölçümü 15 Eki 21–23 arasındaki ayrı oturuma ait. **Katalog:** kullanılan graphify_sor, onay betiği kalıbı, zip_denetle, d | haiku |
| ogren-3-d1 | ogren | ÖMER-KARARI | karar gerekiyor: 1. **Alt ajan izni:** bu oturumda Agent çağrılarına izin vermen gerekiyor; verirsen 03–18'i hemen başlatırım. 2. **Oturum t | haiku |
| ram-opt-1-d3 | ram | ÖMER-KARARI | bekliyor. 5. **Headroom:** 23 dk çalışmış proxy 1.23 GB, ölçüm sırasında +92 MB büyüdü. Bu 20 dk'da sızıntı ile önbellek ayırt edilemedi. Ay | sonnet |
| suit-kirmizi-2 | suit | ÖMER-KARARI | karar gerekiyor. - **Güvenlik:** gitleaks ve sec-sir-tarayici değişen 3 dosyada temiz çıktı. `tools/katalog_ara.py` için semgrep de sessiz g | sonnet |
| ters-2-d8 | ters | ÖMER-KARARI | bekliyor.** | sonnet |
| token-2-d3 | token-2 | ÖMER-KARARI | yapılsın mı? - K1b için 6768 ayarlarının kopyasıyla yeniden koşuya izin var mı? Yapmadıklarım ve riskler: Düşünme payını kabaca tahmin ettim | sonnet |
| token-3-d6 | token-3 | ÖMER-KARARI | karar gerekiyor: 1. K15'i yeniden denemek için +1 claude -p onaylıyor musun? Atlanan iki kuralı skill'de öne alıp tek kolu yeniden koşacağım | haiku |
| token-rea-d20 | token-rea | ÖMER-KARARI | Onay gelirse `uygula` yapılır, birikim sonrası kapı ölçülür. Onay gelmezse ek iş yok, mem2 paraphrase tavanı yaklaşık 0.3–0.4 olarak kalır. | sonnet |
| video-764-1 | video | ÖMER-KARARI | bekliyor. Önce bozuk özetlerin Gemini'ye zorlanması ve Instagram indirme zaman aşımı gözden geçirilmeli. | sonnet |
| yarim-g3 | yarim-g3 | ÖMER-KARARI | bekliyor, ertelendi. Test sayısı 75 (`test_ajan_sira`). CI çalıştırılmadı. Notlar `.kos/kopru/ara/yarim-g3-devam-rd-lm.md` içinde, ruflo'ya  | sonnet |
| yarim-g7 | yarim-g7 | ÖMER-KARARI | bekliyor. Durum notu `.kos/kopru/ara/yarim-g7-devam.md` dosyasında. Ruflo'ya `basari` dersi (#277) kaydedildi. `rapor/yarim-g7.md` ve `yarim | haiku |
| yeniden-gecis-1-a2 | yeniden | ÖMER-KARARI | Karar gerekiyor**: eşzamanlı çalıştırma (örn. 4–7 paralel işçi, `toplu_gozetmen.py`) ile GPU/RAM ölçümü yapılsın mı? Onay gelirse önce 5 vid | sonnet |
| ajan-tam-yetki-1 | ajan | KOŞMUŞ-BİTMEMİŞ | KURTAR-ATLA: yaş >6 saat; Desktop'a soru: yeniden koşsun mu? | sonnet |
| arac-ajan-ozellik-1 | arac | KOŞMUŞ-BİTMEMİŞ | ÖMER:" maddesinin `dist/claude-ai/yukle-24eki` klasörüne taşınması yapılmadı. - **Ruflo:** pattern-store kaydı #294 olarak yazıldı. - **Ayrı | sonnet |
| arac-ajan-ozellik-1-devam-2 | arac | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| arac-ajan-ozellik-1-devam-2-r | arac | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 7 dk | haiku |
| arac-bul-2 | arac | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 4 dk | sonnet |
| arac-bul-2b-a2 | arac | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-frontend, frontend-craft, impeccable, pixeljury, playwright-cli,  | sonnet |
| arac-bul-2c | arac | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 12 dk | haiku |
| arac-indir-1-a2 | arac | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pixelj | ücretsiz |
| arka-aski-1 | arka | KOŞMUŞ-BİTMEMİŞ | bekliyordu. py-spy yığını `hakem` satırı 50'de duran iki thread gösterdi. - **Düzeltme:** deneme sayısı 8'e indi ve her denemede flush'lı sa | sonnet |
| arka-aski-1-a2 | arka | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| arka-kalici-1-a2 | arka | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video_derin, video-tarama, video-uygula, remotion-video-paket, hyperframes- | sonnet |
| atlas-1-d1b | atlas | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 13 dk | haiku |
| atlas-1-d1c | atlas | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 5 dk | haiku |
| atlas-1-d1d | atlas | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 5 dk | haiku |
| autoharness-fix-1-a2 | autoharness | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, mcp-builder, | sonnet |
| beyin-2-d1 | beyin | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. **Commit hataları (benim hatam):** - Kod dosyaları (`tools/beyin_al.py`, `tools | haiku |
| beyin-2-d2 | beyin | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| beyin-4-d1 | beyin | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| beyin-4-d2 | beyin | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: Kalan iş:** 1. Kota açılınca `kapi.py A2011` ile 2011'i yeniden hakemle. 2. A kolunun tur  | haiku |
| beyin-4-d3 | beyin | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: bulunamadı" yazıyor, yani B dizin düzenini bilmiyordu. `kapi.py` artık B'nin istemine düze | haiku |
| beyin-4-d4 | beyin | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| beyin-canli-1b-a2 | beyin | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, document-releas | sonnet |
| beyin-dusun-1 | beyin | KOŞMUŞ-BİTMEMİŞ | bekliyor: kancaların ve zamanlanmış görevin kurulumu (sizin onayınız), ve işin commit'i (yapmadım). - **Yapılan:** `tools/beyin_dusun.py` ye | sonnet |
| beyin-fix-1 | beyin | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 2 dk | haiku |
| beyin-kaydet-1-a2 | beyin | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, beyin, taste-sk | sonnet |
| butce-kapi-1 | butce | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| code-mode-rea-2-a2 | code | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: test-driven-development, systematic-debugging, ruflo, öğrenme:sonda | sonnet |
| cuda-kur-3-devam2-a2 | cuda | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pi | sonnet |
| cuda-kur-3-devam3 | cuda | KOŞMUŞ-BİTMEMİŞ | bekliyor. Şu an RAM %86,2; batch bu yüzden bekliyor. Asıl yük, başka oturumlardan kalan çok sayıda MCP/headroom/blender/git süreci. Bunları  | sonnet |
| cuda-kur-3-devam3-a2 | cuda | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: ffmpeg, video-tarama, video-uygula, remotion-video-paket, hyperframes-p | sonnet |
| cuda-kur-3-devam4-a2 | cuda | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pi | sonnet |
| cuda-kur-3-devam5-a2 | cuda | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, premiere-pro | sonnet |
| cuda-kur-3-devam6-a2 | cuda | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-backend-dotnet, test-driven-development, systematic-debugging | sonnet |
| cuda-kur-3-devam7-a2 | cuda | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-izle, daymade-ses-paket, mcp-video-analyzer, whisper-cli, video-t | ücretsiz |
| cuda-path-1 | cuda | KOŞMUŞ-BİTMEMİŞ | eksik kaldı. | haiku |
| cuda-path-1-a2 | cuda | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, video-tarama, vi | sonnet |
| derin-tamamla-1-a2 | derin | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pixe | sonnet |
| derin-toplu-7-a2 | derin | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, premie | sonnet |
| derin-yeni-1-a2 | derin | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| dns-sonrasi-1 | dns | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı, commit de atılmadı. **Kuyruğa alınanlar** (hepsi `-rd`, `gorev-<ad>-rd.md` yazı | sonnet |
| docker-kur-1 | docker | KOŞMUŞ-BİTMEMİŞ | ÖMER:** 1. Yönetici PowerShell'de `wsl --install --no-distribution` çalıştır. 2. Makineyi yeniden başlat. 3. Aynı yönetici PowerShell'de `wi | sonnet |
| egolite-kur | egolite | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | ücretsiz |
| engel-tarama-1 | engel | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 5 dk | sonnet |
| hakem-test-fix-2 | hakem | KOŞMUŞ-BİTMEMİŞ | bekliyordu, ADAY artık google·nvidia·alibaba·minimax·mistral. Kod doğruydu, testler eskimişti. - **Düzeltme:** `tools/tests/test_gorsel_hake | haiku |
| havuz-genis-2 | havuz | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| her-adim-1 | her | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: durduruldu. Bu yalnız bir arama komutuydu; çıktısına ihtiyaç kalmadı çünkü testi Grep arac | sonnet |
| hermes-kur-1 | hermes | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 8 dk | sonnet |
| hook-fix-1 | hook | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: bulunamadı, değişiklik yok. - **tools/cagri_sayac.py satır 66:** Hook JSON olaylarıyla exi | haiku |
| ig-giris-1-a2 | ig | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: agent-reach, video-tarama, video-uygula, remotion-video-paket, hyperframes- | sonnet |
| ig-toplu-2-a2 | ig | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, video-tarama, vi | sonnet |
| kaynak-kutuphane-1-p2 | kaynak | KOŞMUŞ-BİTMEMİŞ | eksik kaldı mı diye başka dosya aramadım. Çalışma ağacında başka işlerden gelen değişmemiş dosyalar var, onlara dokunmadım. | sonnet |
| kaynak-kutuphane-1-p5-r1 | kaynak | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: Kalan iş:** yok. - **Yapılmadı:** çalışma ağacındaki başka değişikliklere (`.claude/settin | sonnet |
| kaynak-site-1-a2 | kaynak | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pixelj | sonnet |
| kaynak-site-2-a2 | kaynak | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: gitleaks, semgrep, threejs-3d-paket, gsap-skills:gsap-core, web-sahne-desen | sonnet |
| kaynak-tam-3-a2 | kaynak | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: ruflo, gorsel_hakem | sonnet |
| kaynak-tam-4-a2 | kaynak | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, ruflo, | sonnet |
| konsol-gecis-1 | konsol | KOŞMUŞ-BİTMEMİŞ | bekliyor; benden önce bozuktu, dokunmadım. Commit'e `ajan_sira.py`'de zaten bekleyen ücretsiz-motor-2 değişiklikleri de girdi. Rapor `rapor/ | sonnet |
| kucuk-2 | kucuk | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| kucuk-2b | kucuk | KOŞMUŞ-BİTMEMİŞ | bekliyor (`baslat_argv` hep taze env döndürüyor). Dosyada 4 test geçti. Tam suite'i koşmadım. 2. `omer-makara-gece` zaten kuruluydu, yeniden | sonnet |
| kucuk-3 | kucuk | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı: Say.claude sayacı kodda sadece Haiku kaynak adını izliyor. 2. **Ertelenen:** ha | sonnet |
| kucuk-5 | kucuk | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc3221225786: rc 3221225786 1 dk | haiku |
| kurulum-dalgasi-1-a2 | kurulum | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: gitleaks, semgrep, departman-guvenlik, security-reviewer, skillspector, | sonnet |
| kurulum-dalgasi-2-a2 | kurulum | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: gitleaks, semgrep, awesome-rehber, video-tarama, video-uygula, remotion | sonnet |
| kurulum-dalgasi-2c | kurulum | KOŞMUŞ-BİTMEMİŞ | bekliyor. - **aile-2b zip uyarısı:** yanlış pozitif. `REFERANS.md` ve `KAYNAK-1.md`'deki 11 karakter U+200C/U+200D, Farsça metnin yazım işar | sonnet |
| kurulum-laya | kurulum | KOŞMUŞ-BİTMEMİŞ | bekliyorum. Yanıt gelmezse ölçüm ve ince ayara mevcut veriyle devam ederim. | sonnet |
| kurulum-v1-d1 | kurulum | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: bulunamadı). - 15 çift. - 7 ölü/arşiv. Bunların hepsi ad eşleşmesiyle bulundu, kaynak doğr | sonnet |
| kurulum-v1-d3 | kurulum | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| kurulum-v1-d4 | kurulum | KOŞMUŞ-BİTMEMİŞ | bekliyordu. Bunu kendi test sürecimde yeniden ürettim ama gerçek takılmanın aynı mekanizma olduğunu kanıtlayamadım. - **Düzeltme:** `run()`  | sonnet |
| kurulum-video-1b | kurulum | KOŞMUŞ-BİTMEMİŞ | bekliyor" durumunda; indirmeler sürüyor. - **commit:** `fa0de6c kurulum-video-1` (yalnız `docs/envanter/is-arac.md`) - **test:** Remotion re | haiku |
| kurulum-video-1d | kurulum | KOŞMUŞ-BİTMEMİŞ | bekliyor, 1g commit'lendi. - **Commit:** `b429863` "kurulum-video-1" (`docs/envanter/is-arac.md`, `skills/gorsel-uret/SKILL.md`, yalnız bu i | haiku |
| kurulum-video-1e | kurulum | KOŞMUŞ-BİTMEMİŞ | bekliyor. - **1e Wan/FLUX:** Wan GGUF at 3.4 GB and FLUX fp8 at 3.7 GB, both still downloading (PIDs 41936, 61584). Wan's VAE and text encod | haiku |
| kurulum-video-1v | kurulum | KOŞMUŞ-BİTMEMİŞ | bekliyor. - **Commit:** `57c34ee` (yalnız `docs/envanter/is-arac.md`; Wan GGUF tamam, PID'ler güncellendi) - **Test:** Remotion `out/kurulum | haiku |
| laya-2-a2 | laya | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pixelj | sonnet |
| laya-2c-a2 | laya | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, daymade-belge-fi | ücretsiz |
| limit-sonrasi-1 | limit | KOŞMUŞ-BİTMEMİŞ | KAPI BAŞLAMADI: limit-sonrasi-1 görevde 'NİHAİ 31+32' satırı yok | sonnet |
| link-27eki-1 | link | KOŞMUŞ-BİTMEMİŞ | KURTAR-ATLA: git log'da görev adı var (iş commit'lenmiş) | sonnet |
| link-sayim-1 | link | KOŞMUŞ-BİTMEMİŞ | bekliyor 14844 · derin_var 698 · silinmis 8 - **Post slaytları:** 499 postun 48'inin derin JSON'u var ve hepsinde `kare_sayisi` alanı mevcut | haiku |
| link-sayim-1-a2 | link | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, youtube-agent:yt-shorts, video-uygula, remotion-video-paket,  | sonnet |
| makara-1-d1 | makara | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı (turlar bitti). - **`ajan_sira.py` commit'i:** Başka oturumun commitlenmemiş değ | haiku |
| makara-1-d3 | makara | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı: repo ve secret yok, `act` kurulu değil. Zinciri sahte havuzla yerel klasörde si | sonnet |
| mcp-ac-2 | mcp | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 16 dk | sonnet |
| mem-fix-1 | mem | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. Rapor `.kos/kopru/rapor/mem-fix-1.md` içinde. 60 turluk bütçeyi aşmamak için du | sonnet |
| mem-fix-2 | mem | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı:** Claude-mem'de transkript içe alma yolu yok. `backfill.json` yalnız telemetri  | sonnet |
| mem-fix-4 | mem | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| nihai-duzelt-1 | nihai | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| nihai-kapi-1 | nihai | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| ocr-hiz-1-a2 | ocr | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pixelj | sonnet |
| ogren-0b-d14 | ogren | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 4 dk | haiku |
| ogren-0b-d4 | ogren | KOŞMUŞ-BİTMEMİŞ | bekliyordum: iş 7 çıktı dosyası bekliyordu, py06 hiç başlatılmadığı için 6'da kaldı. Yeniden başlatmadım. Değişen bir şey yok. py00–py05 par | haiku |
| ogren-1-d14 | ogren | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 18 dk | haiku |
| ogren-1-d8 | ogren | KOŞMUŞ-BİTMEMİŞ | bekliyor; uygulamadım.** Kararın ardından yeni, görülmemiş en az 25 kalemlik bir örneklemle ölçüm tekrarlanacak. Kontrol etmediğim bir konu: | haiku |
| ogren-2-d2 | ogren | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| ogren-3-d3 | ogren | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. SKILL.md adım 6'daki `docs/ogren/…` yolu claude.ai'de yok, metin kendi kendine  | sonnet |
| ogren-4-d3 | ogren | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| ogren-6-d1 | ogren | KOŞMUŞ-BİTMEMİŞ | bekliyor). Bu reddi aşmaya çalışmadım; d2'ye geçmek için senin izin kararın gerekiyor. ÖĞREN-3 ve ÖĞREN-4'te de aynı ret yaşanmış. - **Commi | haiku |
| ogren-oto-1 | ogren | KOŞMUŞ-BİTMEMİŞ | bekliyor, '3' geliyor. Bu testle benim eklediğim kısım ilgisiz görünüyor, olası neden başka oturumun commitlenmemiş değişikliği. Nedenini ka | sonnet |
| ogren-tur2-d2 | ogren | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| ogren-tur2-d4 | ogren | KOŞMUŞ-BİTMEMİŞ | bekliyor; önceki raporda yazdığım ★ d5 seçeneklerinden birini seçersen devam ederim (kosul/nasil format gevşetme ya da A+B havuzu + kart baş | haiku |
| ogrenme-2g | ogrenme | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| ollama-kim-1-a2 | ollama | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, premie | sonnet |
| olum-teshis-1-a2 | olum | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: gorsel_hakem | sonnet |
| onay-toplu-1-devam-2 | onay | KOŞMUŞ-BİTMEMİŞ | BEKLİYOR: Console geçişi. Ücretsiz motorla ölçüm yapılmadı. - **10 autoharness guide/doctor:** Yapılmadı. - **12 OLLAMA_KEEP_ALIVE:** Önceki | haiku |
| onay-toplu-1-devam-2-r | onay | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 7 dk | haiku |
| ordu-1-d4 | ordu | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| ordu-1-d6 | ordu | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| oyun-modu-1-a2 | oyun | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-diger, blender-uretim, test-driven-development, comfyui, gh, rtk, | sonnet |
| ram-bekci-2-a2 | ram | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: test-driven-development, graphify | sonnet |
| ram-bekci-3 | ram | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 2 dk | sonnet |
| ram-bekci-test-1 | ram | KOŞMUŞ-BİTMEMİŞ | bekliyordu, yani 600 MB eşiğine göre bayattı. 700 MB'a çekildi. - **Kalan durumlar:** Yönetici ajan altında değil, kökün üstünde olduğu için | sonnet |
| ram-bekci-test-1-a2 | ram | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: test-driven-development, graphify | sonnet |
| ram-opt-1 | ram | KOŞMUŞ-BİTMEMİŞ | bekliyorum. Bu ölçülmüş değil, süreç ağacı toplamlarından çıkardım. - **Geri alma:** `python onay/ram_opt_1_desktop.py --geri`. Yedek `claud | sonnet |
| ram-opt-1-d2 | ram | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| rea-agir-2-a2 | rea | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: blender-uretim, test-driven-development, comfyui, gh, graphify | sonnet |
| rea-fix-2-a2 | rea | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-backend-dotnet, test-driven-development, departman-veri-db | ücretsiz |
| rea-usta-1b-a2 | rea | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: security-reviewer, skillspector, mcp-builder, test-driven-development, syst | sonnet |
| rea-usta-1c | rea | KOŞMUŞ-BİTMEMİŞ | bekliyor. Notlar `.kos/kopru/ara/rea-usta-1c-a.md` dosyasında, ruflo'ya da 1 hata dersi yazıldı. Maliyet yaklaşık $0.20, hedefin altında. | sonnet |
| ret-kur-1b | ret | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 16 dk | sonnet |
| router-1-d3 | router | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| ruflo-2-d1 | ruflo | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| ruflo-2-d2 | ruflo | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: durdurulduğunu söylüyor. Bu iş artık gereksiz: aynı işi `tools/ruflo/kanit.py` yaptı ve ka | haiku |
| ruflo-2-d3 | ruflo | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı, çünkü 45 tur sınırına geldim. `claude -p` çağrısı kullanılmadı (0/11). - **A (` | haiku |
| ruflo-2-d4 | ruflo | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. Rapor `.kos/kopru/rapor/ruflo-2.md` içinde; `.kos` gitignore'da olduğu için com | haiku |
| skill-dogrula-2 | skill | KOŞMUŞ-BİTMEMİŞ | bekliyor. Repo'da olup CC'de olmayan 18 skill de (jev, tersine, video-* gibi) kurulmadı. - **Bütçe:** hedef $0.50'ydi, toplam yaklaşık $1.8  | sonnet |
| skill-dogrula-2-a2 | skill | KOŞMUŞ-BİTMEMİŞ | bekliyor. - **Başlangıç süresi (153–213 sn):** Kök neden tek bir yavaş MCP ya da hook değil. 407 eklenti ve 2983 skill sırayla yükleniyor. D | sonnet |
| slash-ogren-d2 | slash | KOŞMUŞ-BİTMEMİŞ | bekliyor. - **(3)** "Ölçülen kazanç" sütununda hâlâ yalnız watch ölçülmüş. Aday ölçümler: `graphify query`'ye karşı grep (boyut ve süre), `k | sonnet |
| slash-ogren-d5 | slash | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| sleep-1-d2 | sleep | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: durduruldu ve adopt yapılmadı. Ücretsiz modellerle gerçek koşu tamamlandı ama gate reddett | sonnet |
| sleep-1-d3 | sleep | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| stalemap-kur-2-a2 | stalemap | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: mcp_profil, departman-guvenlik, security-reviewer, skillspector, mcp-build | sonnet |
| suit-fix-1-devam | suit | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 6 dk | sonnet |
| suit-fix-1-devam-r | suit | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 8 dk | sonnet |
| suit-fix-1-devam-rd | suit | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| suit-fix-1-devam-rd-a2 | suit | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, semgrep, g | sonnet |
| suit-fix-2 | suit | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| suit-fix-3 | suit | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| suit-kirmizi-2-a2 | suit | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: sec-sir-tarayici, semgrep, gitleaks, ruflo, öğrenme:sonda | sonnet |
| takip-24eki-a | takip | KOŞMUŞ-BİTMEMİŞ | Eksik kaldı. 52 karelik OCR 20 dakikadan uzun sürdü ve süre sınırında kesildi. Önceki turdaki kare OCR'ı da repo ya da URL bulmamıştı. - **O | sonnet |
| takip-24eki-a2 | takip | KOŞMUŞ-BİTMEMİŞ | ÖMER: Devam komutu `rapor/video-repo-3-zycck.md` içinde. skillspector ve semgrep temiz çıkarsa kurulum yapılacak. Bundan sonra `video-kur-1- | sonnet |
| tarama-hiz-1 | tarama | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| ters-1-d2 | ters | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| ters-1-d3 | ters | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. Koşu 8. hedefte `KeyError: 'derlenmis'` ile çöktü; bu yüzden resmi `sonuc.md`/` | haiku |
| ters-1-d4 | ters | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. SIRA'ya yalnızca "TERS-1 d4 (kapı geçmedi)" satırı eklendi. **Yapılanlar** - ** | haiku |
| ters-2-d1 | ters | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. - **Commit `36f82285`** (yerel, push yok): `tools/ters/kapi_kos.py` ve `tools/t | haiku |
| ters-2-d2 | ters | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı: SKILL.md, zip, departman bağı, SIRA, Obsidian.** - **Commit:** yerel, push yok. | haiku |
| token-2-d4 | token-2 | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 24 dk | sonnet |
| token-2-d4b | token-2 | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 5 dk | haiku |
| token-2-d4c | token-2 | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 5 dk | haiku |
| token-olcum-27eki-a2 | token-olcum | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: Yapılmadı:** Madde 4'teki "uygulanabilir olanları ayrı görev olarak yaz" adımı. `.kos/kopr | ücretsiz |
| token-rea-d1 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| token-rea-d10 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. - **Ölçüm bütçesi:** `claude -p` 0/15, havuz 0/80. **d11 taslağı** `plan.md`'de | haiku |
| token-rea-d11 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. - **claude-mem (7 gözlem):** - Kalite: 30 soruda aramasız kapsam 0,43, aramayla | haiku |
| token-rea-d14 | token-rea | KOŞMUŞ-BİTMEMİŞ | bekliyor. - **Madde 2, 7–15 gözlem aralığı:** ayrı koşu yapmadım. mem2 aramada 0.93 isabet veriyor ama bu aralık için ayrıca ölçülmedi. - ** | sonnet |
| token-rea-d18 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| token-rea-d2 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı, d3'e kaldı. Commit `62367e17`. - **claude-mem:** gözlemci hâlâ düşük. Oturum ka | haiku |
| token-rea-d3 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| token-rea-d4 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| token-rea-d5 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. - **Held-out üreticisi:** `heldout_uret.py rtk2/sor2 <tohum>` komut ve soru set | haiku |
| token-rea-d6 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı; 45 tur tavanında yarım bırakmadım. Commit `18123085`, push yok. - **sor2:** Soğ | haiku |
| token-rea-d7 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| token-rea-d8 | token-rea | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı, ikisi de ★ d9 TASLAK'ta. - **Commit:** `token-rea d8: yontem skill + baglam kal | haiku |
| token-rea-d9 | token-rea | KOŞMUŞ-BİTMEMİŞ | bekliyor. - mem-search kullanılmazsa eşitlik için 10 gerekir. 3. **Tur × bağlam (yalnız ölçüm):** istek başına bağlamı 120k'nın üstünde olan | haiku |
| ucretsiz-havuz-2 | ucretsiz | KOŞMUŞ-BİTMEMİŞ | bekliyor, 60 sn sonra yine sığıyor. - **mem-yedek bağlantısı:** `serve` ve `mem_fix_omni.py havuz` bağlandı; uç 20190'da canlı ve test isteğ | sonnet |
| ucretsiz-motor-1 | ucretsiz | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 1 dk | sonnet |
| ucretsiz-motor-2-devam | ucretsiz | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 5 dk | ücretsiz |
| ucretsiz-motor-2-devam-rd-a2 | ucretsiz | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: idea-refine, brainstorming, interview-me, doubt-driven-developm | ücretsiz |
| unlimited-ocr-kur | unlimited | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| usta-blender-2 | usta | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| usta-web-1-a2 | usta | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-frontend, frontend-craft, scroll-craft, web-sahne-desenleri, thre | sonnet |
| usta-web-2 | usta | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| ustalik-1-p2 | ustalik | KOŞMUŞ-BİTMEMİŞ | bekliyor, canlı sınamadım. - **Kurulum betikleri:** npm, 5 paketin kurulum betiğini (puppeteer, esbuild, sharp, netlify, ocr) çalıştırmadı;  | sonnet |
| video-3-d1 | video | KOŞMUŞ-BİTMEMİŞ | bekliyor. - **Testler:** `tests/test_uzun.py` 3/3 geçti. Koşu sırasında birleştirmede bir hata çıktı (Gemini bir alanı liste döndürdü), düze | haiku |
| video-3-d8 | video | KOŞMUŞ-BİTMEMİŞ | bekliyor (TypeScript ×2, Framer Motion, Claude Code). - 3'ünde hat ürün adını buluyor ama altın küme daha ayrıntılı bir ad bekliyor (ör. "Tr | haiku |
| video-764-2 | video | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| video-764-3 | video | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| video-764-4 | video | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| video-764-4-d2 | video | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| video-764-4-d3 | video | KOŞMUŞ-BİTMEMİŞ | bekliyorum. | haiku |
| video-8uSAtG7Ohzg | video | KOŞMUŞ-BİTMEMİŞ | eksik kaldı. - **Raf:** `skills/omer-kutuphaneler/raf/`, sığ klon, `.gitignore`'a eklendi (lisanssız içerik commit'e girmesin). - **Lisans:* | haiku |
| video-denetim-1-a2 | video | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: video-tarama, video-uygula, remotion-video-paket, hyperframes-paket, pixe | haiku |
| video-ek-50 | video | KOŞMUŞ-BİTMEMİŞ | bekliyor. RAM'i boşaltmadım. - **KARAR yolu yok:** video-764-4 raporuna göre karar verici seçilmedi. Haiku altın sete %87,5 tuttu (eşik %95) | sonnet |
| video-kisa-token-1 | video | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 6 dk | ücretsiz |
| video-kisa-token-1b | video | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 6 dk | haiku |
| video-kur-1b | video | KOŞMUŞ-BİTMEMİŞ | bekliyor ve bu turda onları kurmadım. - **Commit:** `bf299f4c`, yalnız `video-kur-1-p2.md` raporu. Önceki turdan eksik kalan adım, `code-mod | sonnet |
| video-kur-1b-a2 | video | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: skillspector, semgrep, strix, ecc-agentshield | ücretsiz |
| video-sonrasi-1 | video | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: bulunamadı") eşlendi, çıktısı `arac-indir-2.tsv`: / Durum / Sayı / /---/---/ / Yeni indiri | sonnet |
| yarim-a1 | yarim-a1 | KOŞMUŞ-BİTMEMİŞ | ÖMER:** skill değişikliğinin claude.ai tarafı için dist zip yeniden üretilip yüklenmeli. Yüklenene kadar CC'de değişiklik görünmez (synced g | sonnet |
| yarim-a2 | yarim-a2 | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 2 dk | sonnet |
| yarim-a3 | yarim-a3 | KOŞMUŞ-BİTMEMİŞ | bekliyor, uygulamadım. Commit d7a36c87. 1. **autoharness-fix-1:** `autoharness_winfix.py` artık `tools/` altında; koşusu "zaten doğru" verdi | sonnet |
| yarim-b1 | yarim-b1 | KOŞMUŞ-BİTMEMİŞ | KURTAR-ATLA: yaş >6 saat; Desktop'a soru: yeniden koşsun mu? | sonnet |
| yarim-b1-devam-b-r1 | yarim-b1 | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | haiku |
| yarim-c1 | yarim-c1 | KOŞMUŞ-BİTMEMİŞ | ÖMER: yok. | sonnet |
| yarim-c2 | yarim-c2 | KOŞMUŞ-BİTMEMİŞ | ÖMER:** - Ruflo kapısı açık ve zorunlu kalıyor (Desktop 16:42 kararı); kapı geçmezse sebebi bulunup düzeltilecek. - Yetim headroom çocuğu pi | sonnet |
| yarim-e1 | yarim-e1 | KOŞMUŞ-BİTMEMİŞ | ÖMER:** `dist/claude-ai/yukle-24eki/` (6 zip) ve `yukle-23eki` gruplarını Desktop'tan claude.ai'ye yüklemesi gerekiyor. Yükleme kanıtı yok.  | sonnet |
| yarim-e2 | yarim-e2 | KOŞMUŞ-BİTMEMİŞ | bekliyor. Rapor `rapor/yarim-e2.md`, commit `0eb51c2b`, push yok. Yeni kod yazmadım, yalnız ölçüm ve rapor yaptım. Bu turda yalnız `tools/te | sonnet |
| yarim-e3 | yarim-e3 | KOŞMUŞ-BİTMEMİŞ | ÖMER: Aşağıdakilerden birini seç, işe oradan devam edeceğim: - (a) Kapıyı yeniden tanımla: "6 ve altı yakalama AUC ≥ 0.8 + ρ". - (b) Opus'un | sonnet |
| yarim-f1 | yarim-f1 | KOŞMUŞ-BİTMEMİŞ | ÖMER: yok. Başta ruflo pattern-search ile beyin ara'yı çalıştırmadım. Gerekçe: iş sadece doğrulamaydı, yeni bir şey üretmedim. Hawkscan sonr | sonnet |
| yarim-g2 | yarim-g2 | KOŞMUŞ-BİTMEMİŞ | bekliyor, başlamadım. Sende bekleyenler: `dist/kalite-1` ve ogren-4 zip yükleme, beyin-2/3/4 kapı kararı, `Omer-F-Ylmz/omer-makara` repo ona | sonnet |
| yarim-g2-devam | yarim-g2 | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok: yapılmadı. Kalan 16 maddenin hiçbiri bu oturumda başlatılabilir değil, ogrenme-2b ise zate | sonnet |
| yarim-g3-devam | yarim-g3 | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 5 dk | sonnet |
| yarim-g3-devam-rd | yarim-g3 | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 85 dk | sonnet |
| yarim-g3-devam-rd-a2 | yarim-g3 | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, semgrep, git | sonnet |
| yarim-g5 | yarim-g5 | KOŞMUŞ-BİTMEMİŞ | bekliyor: `animasyon_1_uygula.py`, `tasarim_1_uygula.py`, `tasarim_2_uygula.py` (+ zip) ve `HAWK_API_KEY`. Commit yok, test koşmadım. Kod de | sonnet |
| yarim-g6 | yarim-g6 | KOŞMUŞ-BİTMEMİŞ | BEKLİYOR:** G06–G12 ×1 ölçümü, Console API ya da limit açılınca. `DEVAM.md` yazılmadı. **Yapılmadı:** - `temiz-yeniden-1`'i kuyruğa alma. -  | sonnet |
| yarim-tam-2 | yarim-tam | KOŞMUŞ-BİTMEMİŞ | Ömer: `kurulum-video-1` 1g (Remotion kelime senkronlu altyazı) bitti mi, bakar mısın? OmniRoute'ta Qwen3.8-27b katalog eşitlemesi de sende.  | sonnet |
| yarim-tara-1-a2 | yarim-tara | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, semgrep, gitleak | sonnet |
| yonetici-api-1-devam-a2 | yonetici | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-backend-dotnet, test-driven-development, systematic-debugg | sonnet |
| yonetici-bagimsiz-1 | yonetici | KOŞMUŞ-BİTMEMİŞ | bekliyorum ve ardından commit atacağım. | sonnet |
| yonetici-bagimsiz-1b-a2 | yonetici | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, departman | sonnet |
| yonetici-bagimsiz-1c-a2 | yonetici | KOŞMUŞ-BİTMEMİŞ | DUR: 2 devam turundan sonra hâlâ eksik: departman-belge, headroom-compress, markitdown, summarize, herdr-pak | sonnet |
| yonetici-olum-3 | yonetici | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| zip-yukle-24eki-2 | zip | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 8 dk | sonnet |
| zorunlu-arac-2 | zorunlu | KOŞMUŞ-BİTMEMİŞ | BİTTİ-rc1: rc 1 1 dk | sonnet |
| zorunlu-kullanim-1 | zorunlu | KOŞMUŞ-BİTMEMİŞ | sonuç var, rapor/commit kanıtı yok | sonnet |
| DEVAM-KURALI | DEVAM | HİÇ GİRMEMİŞ | DEVAM-KURALI (TOKEN-3 K15, 14 Eki): bağlayıcı kurallar TEK dosyada — `C:/Projeler/omer-skills/skills/is-akisi/ | sonnet |
| SIRA | SIRA | HİÇ GİRMEMİŞ | - 22:46 CC kol/blender: BLENDER-1-devam-3 kök nedenler düzeltildi (g1 oto kamera zemini sayıyordu, g4 patlat k | sonnet |
| _sablon | _sablon | HİÇ GİRMEMİŞ | # <GÖREV-ADI> — <tek cümle amaç> (<tarih saat>) | sonnet |
| animasyon-1 | animasyon | HİÇ GİRMEMİŞ | ANİMASYON-1 — animasyon ve efektleri kendimiz yapacağız (Desktop 12 Eki 07:35; Ömer 07:29: "Blender olsun başk | sonnet |
| atlas-1 | atlas | HİÇ GİRMEMİŞ | # ATLAS-1 — elimizdeki her şeyin kullanım atlası (Desktop 14:55) — ajan_sira, cwd omer-skills | sonnet |
| atlas-2 | atlas | HİÇ GİRMEMİŞ | # ATLAS-2 — diğer kümelerin kullanım kitapları (14 Eki 18:00) | sonnet |
| awesome-1 | awesome | HİÇ GİRMEMİŞ | AWESOME-1 — sindresorhus/awesome'ı kendi kaynak rafımıza almak (Ömer 11 Eki 23:19: "sindresorhus awesome da ek | sonnet |
| beyin-1 | beyin | HİÇ GİRMEMİŞ | # BEYIN-1 — İkinci beyin (en öncelikli altyapı işi; Ömer 20 Eki: "şu ana kadarki en iyi işimiz olacak, elimizd | sonnet |
| beyin-2 | beyin | HİÇ GİRMEMİŞ | # BEYIN-2 — İkinci beyin Obsidian merkezli (Ömer 20 Eki 11:38: "Obsidian'ı daha iyi ve daha fazla kullanalım,  | sonnet |
| beyin-3 | beyin | HİÇ GİRMEMİŞ | # BEYIN-3 — ikinci beyin ARAMA KALİTESİ (parça seçimi) → kapı ≥%92 + token ≤%25 | sonnet |
| beyin-4 | beyin | HİÇ GİRMEMİŞ | # BEYIN-4 — result parçalama + kayıp türleri + yeni tohumlarla kapı | sonnet |
| beyin-fix-2 | beyin | HİÇ GİRMEMİŞ | BEYİN-FİX-2 (23 Eki 14:50). beyin-ozet ALARM: "23 14:40 döngü hatası: TypeError: '>=' not supported between in | sonnet |
| birlestir-1 | birlestir | HİÇ GİRMEMİŞ | BİRLEŞTİR-1 — biten dalları main'e almak (Desktop 12 Eki 03:10) | sonnet |
| birlestir-2 | birlestir | HİÇ GİRMEMİŞ | BİRLEŞTİR-2 — KABUL olan dalları main'e almak (Desktop 12 Eki 04:35) | sonnet |
| birlestir-3 | birlestir | HİÇ GİRMEMİŞ | BİRLEŞTİR-3 — kol/butce + kol/skill + Blender CC sürümü (Desktop 12 Eki 06:25; Ömer 06:23 "bugün bitmeli, en h | sonnet |
| blender-1 | blender-1 | HİÇ GİRMEMİŞ | BLENDER-1 — Blender'ı en iyi şekilde ve çok az jetonla kullanmak (Ömer 11 Eki 14:31). Hedef: en ağır Blender i | sonnet |
| blender-2 | blender-2 | HİÇ GİRMEMİŞ | BLENDER-2 — Blender'la ilgili HER ŞEY, bugün, en iyi şekilde (Desktop 12 Eki 07:35; Ömer 07:29: "Blender'ı çok | sonnet |
| code-mode-1 | code | HİÇ GİRMEMİŞ | CODE-MODE-1 (görev dosyası: C:\Projeler\omer-skills\.kos\kopru\gorev-code-mode-1.md) | sonnet |
| envanter-2 | envanter | HİÇ GİRMEMİŞ | # ENVANTER-2 — YETENEK KATALOĞU: kurulu her şeyin "ne işe yarar"ı hafızada, işte aranır (Ömer önerisi 13 Eki 2 | sonnet |
| envanter-3 | envanter | HİÇ GİRMEMİŞ | # ENVANTER-3 — öğrenim kataloğu + sağlam plan hattı (Ömer 13 Eki 23:01) | ücretsiz |
| envanter-4 | envanter | HİÇ GİRMEMİŞ | # ENVANTER-4 — DERİN KILAVUZ + BİRLEŞİM TARİFLERİ (Ömer 13 Eki 23:07) | sonnet |
| envanter-5 | envanter | HİÇ GİRMEMİŞ | # ENVANTER-5 — katalog seçimi BÜYÜK ÖLÇEKLİ ve KALICI ölçü (Ömer 14 Eki 00:54) | sonnet |
| envanter-6 | envanter | HİÇ GİRMEMİŞ | # ENVANTER-6 — DEĞER KAPISI: katalog nerede gerçekten değer katıyor? (Desktop 14 Eki 01:45) | sonnet |
| fable-1 | fable | HİÇ GİRMEMİŞ | FABLE-1 — Fable 5.1'in çalışma/düşünme tarzını kendi ajanlarımıza (Sonnet 5.5 · Haiku 5.5 · .claude/agents fil | ücretsiz |
| fable-ajan | fable | HİÇ GİRMEMİŞ | !! ÖMER 20:25 KAPSAM GENİŞLEDİ (GODMODE-HEPSİ): "bizim yaptığımız ajanlar + skill/MCP/plugin/CLI'lerden gelen  | sonnet |
| fable-video | fable | HİÇ GİRMEMİŞ | FABLE-VIDEO — FABLE-1'in KABUL edilen çalışma protokolünü video hattının Sonnet/Haiku adımlarına uygula (Deskt | ücretsiz |
| gorev-usta-blender-1 | gorev | HİÇ GİRMEMİŞ | # usta-blender-1, Blender dallı müfredat (S1 temel → S5 stüdyo). Seviye geçilmeden üstüne çıkılmaz; her seviye | sonnet |
| graphify-ultra-1 | graphify | HİÇ GİRMEMİŞ | # GRAPHIFY-ULTRA-1 — graphify'ı keşif token'ının ana yolu yap: daha doğru, daha hızlı, daha az token (Desktop  | haiku |
| guvenlik-yama-1 | guvenlik | HİÇ GİRMEMİŞ | GUVENLIK-YAMA-1 — ACİL (Ömer 23 Eki 17:00): Reel https://www.instagram.com/reel/DezQy4CCHfr/ izlenecek; PC'de  | sonnet |
| headroom-1 | headroom | HİÇ GİRMEMİŞ | # HEADROOM-1 — headroom-ai güncellemesini güvenle hazırla (UYGULAMA YOK) (Desktop 13 Eki 18:30) | sonnet |
| hook-3 | hook | HİÇ GİRMEMİŞ | HOOK-3 — gsd-core (çatal) kurulumu: ölçümle karar (rapor C:\Projeler\omer-skills\.kos\kopru\rapor\hook3.md; on | sonnet |
| ig-18-kur | ig | HİÇ GİRMEMİŞ | IG-18-KUR — Ömer'in 08:46'da gönderdiği 18 IG gönderisindeki araçları özenle kur (Desktop 12 Eki 09:32). Usul  | sonnet |
| ig-40 | ig | HİÇ GİRMEMİŞ | IG-40 — Ömer'in 40 Instagram linki (11–12 Eki; reel + karusel gönderi) tam hattan (Desktop 12 Eki 06:47; Ömer: | sonnet |
| ig-40-kur | ig | HİÇ GİRMEMİŞ | IG-40-KUR — 40 IG gönderisinde bulunan araçları ÖZENLE kur (Desktop 12 Eki 08:14; Ömer 07:29: "son yolladığım  | sonnet |
| jev-1 | jev | HİÇ GİRMEMİŞ | JEV-1 — Jev'in tam kullanımı: daha hızlı, daha kaliteli, daha az jeton (Ömer 11 Eki 14:31; yol haritası madde  | sonnet |
| jev-2 | jev | HİÇ GİRMEMİŞ | JEV-2 — Jev'i HER YERDE tam kullan: daha hızlı, daha kaliteli, daha az jeton (Desktop 12 Eki 07:45; Ömer 07:29 | sonnet |
| kalite-1 | kalite-1 | HİÇ GİRMEMİŞ | KALİTE-1 — doğru aracı seçme isabeti + gizli ajanlara erişim + G06/G07 | sonnet |
| kalite-2 | kalite-2 | HİÇ GİRMEMİŞ | KALİTE-2 — kurulu her aracın kendi kalite · performans · token iyileştirmesi (Ömer 10 Eki: "kurulu her aracın  | sonnet |
| kalite-3 | kalite-3 | HİÇ GİRMEMİŞ | KALİTE-3 — BÜTÜN skill filosu (~2.000 skill: ~/.claude/skills gevşek + 105 aile paketi alt skill'leri + plugin | sonnet |
| kalite-3-d14 | kalite-3 | HİÇ GİRMEMİŞ | KALİTE-3-devam-14 — d13 zinciriyle PARALEL: RET onarımı + ölçüm düzeltmeleri + 450 ötesi + godmode altyapısı ( | sonnet |
| kalite-3-hiz | kalite-3 | HİÇ GİRMEMİŞ | !! DÜZELTME 16:08: asıl neden cihazın dış ağının ~14:26'da kopması — o saatten sonraki yanıt dosyaları "API Er | sonnet |
| kanca-sayac-1 | kanca | HİÇ GİRMEMİŞ | # KANCA-SAYAÇ-1 — çağrı sayacı kancasını oturum başına ayır + bağlam eşiği (Ömer onayı 13 Eki 20:36) | sonnet |
| kapi-25 | kapi | HİÇ GİRMEMİŞ | # KAPI-25 — kapıdan geçmemiş 25 ajanın son durumu + sızıntı yolunu kapat (Desktop 13 Eki 16:10) | sonnet |
| katalog-kanca-1 | katalog | HİÇ GİRMEMİŞ | # KATALOG-KANCA-1 — zor işte katalog ön-enjeksiyonu (UserPromptSubmit), rutin işte sıfır maliyet (Desktop 14 E | sonnet |
| kaynak-kutuphane-1-p2-r1 | kaynak | HİÇ GİRMEMİŞ | DEVAM (DNS kesintisi sonrası) — önceki kısmi çıktı: ajan-sira/kaynak-kutuphane-1-p2-r1.json | haiku |
| kopru-effort-1 | kopru | HİÇ GİRMEMİŞ | # KÖPRÜ-EFFORT-1 — cc-kopru `ajan` aracına oturuma özel effort (13 Eki; TELVE tasarım/3D oturumları xhigh, glo | sonnet |
| kurulum-v1 | kurulum | HİÇ GİRMEMİŞ | # KURULUM-V1 — video adaylarından kurulum (SIRA: video → KURULUM → ÖĞREN 2. tur) | sonnet |
| kurulum-video-1 | kurulum | HİÇ GİRMEMİŞ | # KURULUM-VİDEO-1 (kids-shorts hattı) | sonnet |
| makara-1 | makara | HİÇ GİRMEMİŞ | # MAKARA-1 — kendi kendine gelişme döngüsü (döngü 1 + 2: iş sırasında + boşta PC açık) | sonnet |
| makara-plan | makara | HİÇ GİRMEMİŞ | # MAKARA — kendi kendine gelişme döngüsü (Ömer 20 Eki 11:55) — PLAN (Desktop; SLEEP-1 d2 + BEYIN-2 bitince MAK | haiku |
| mcp-hafif-1 | mcp | HİÇ GİRMEMİŞ | MCP-HAFIF-1 — arka plan claude -p oturumları her seferinde ~40 user MCP sunucusunu (Serena dahil) başlatıyor → | sonnet |
| mcp-hafif-2 | mcp | HİÇ GİRMEMİŞ | MCP-HAFIF-2 — RAM'i daha da düşür, token tasarrufunu ve kalite/performansı daha da artır (Desktop 12 Eki 18:20 | sonnet |
| model-politikasi | model | HİÇ GİRMEMİŞ | # MODEL POLİTİKASI — bütün köprü oturumları ve alt ajanlar (Ömer 20 Eki 12:15, haftalık %7'de; bağlayıcı) | sonnet |
| ogren-10 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-10 — veri-db (kategori_son=veri-db; müdür: departman-veri-db) | sonnet |
| ogren-11 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-11 — araştırma (kategori_son=araştırma; müdür: departman-arastirma-ogrenme) | ücretsiz |
| ogren-12 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-12 — pazarlama (kategori_son=pazarlama; müdür: departman-diger reklam/pazarlama bölümü) | haiku |
| ogren-13 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-13 — oyun-mod (kategori_son=oyun-mod; müdür: departman-diger oyun/mod bölümü + mod-atolyesi) | sonnet |
| ogren-14 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-14 — bilim + diğer-kalan (kategori_son=bilim ve ÖĞREN-0b sonrası hâlâ "diğer" kalanlar) | ücretsiz |
| ogren-2 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-2 — frontend-tasarım (kategori_son=frontend-tasarım; müdür: departman-frontend) | sonnet |
| ogren-3 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-3 — ajan-orkestrasyon (kategori_son=ajan-orkestrasyon; müdür: departman-surec-ajan-arac + departman-su | sonnet |
| ogren-4 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-4 — video-medya (kategori_son=video-medya; müdür: departman-diger video bölümü + video-tarama/video-uy | sonnet |
| ogren-5 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-5 — 3d + görsel üretim (kategori_son=3d; müdür: departman-diger 3D/görsel bölümü + blender-oturum/blen | sonnet |
| ogren-6 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-6 — test-qa (kategori_son=test-qa; müdür: departman-test-qa) | sonnet |
| ogren-7 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-7 — güvenlik (kategori_son=güvenlik; müdür: departman-guvenlik) | ücretsiz |
| ogren-8 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-8 — belge (kategori_son=belge; müdür: departman-belge) | ücretsiz |
| ogren-9 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN-9 — backend-dotnet (kategori_son=backend-dotnet; müdür: departman-backend-dotnet) | sonnet |
| ogren-ortak | ogren | HİÇ GİRMEMİŞ | # ÖĞREN ortak yöntem (her kategori oturumu bunu OKUR ve UYGULAR) — Desktop 15 Eki 00:55 | sonnet |
| ogren-tur2 | ogren | HİÇ GİRMEMİŞ | # ÖĞREN 2. TUR — kurulu + yeni HER ŞEYDE hakimiyet + KOMBO kataloğu (SIRA 20 Eki 17:54; KURULUM-V1 BİTTİ 21 Ek | ücretsiz |
| omni-ayir | omni | HİÇ GİRMEMİŞ | DESKTOP 02:32 (d2+ için; ÖĞREN-1 d5 bulguları, .kos/kopru/devir/ogren-1-devam.md): (a) OmniRoute YANIT ÖNBELLE | ücretsiz |
| omniroute-1 | omniroute | HİÇ GİRMEMİŞ | OMNIROUTE-1 — Haftalık plan limiti dolunca köprü ajanları OmniRoute'a geçsin (Ömer 13 Eki 05:40) | sonnet |
| ordu-1 | ordu | HİÇ GİRMEMİŞ | # ORDU-1 — "her şeyi alt ajanlar yapsın, biz derleyip iyileştirelim" (ücretsiz → Haiku → Sonnet → Opus) | sonnet |
| plan-kur-2 | plan | HİÇ GİRMEMİŞ | # PLAN-KUR-2 — plan aracını hem daha ucuz hem daha kaliteli yap (Ömer 14 Eki 06:32) | haiku |
| plan-kur-3 | plan | HİÇ GİRMEMİŞ | # PLAN-KUR-3 — iyi yanı al, bozan yanı düzelt (14 Eki 07:20) | haiku |
| plan-kur-4 | plan | HİÇ GİRMEMİŞ | # PLAN-KUR-4 — zor/rutin sınıflandırıcısını düzelt (14 Eki 09:58) | sonnet |
| router-1 | router | HİÇ GİRMEMİŞ | # ROUTER-1 — alt ajan yönlendirici + risk-doğrulama + geri besleme (Ömer 20 Eki: "goat makarası", çok az maliy | sonnet |
| ruflo-1 | ruflo | HİÇ GİRMEMİŞ | !!!! ÖMER 13 Eki 05:07: günlük öğrenme kancasında "kaliteyi performansı daha da arttıralım" → hedef yalnız ≥ t | sonnet |
| ruflo-2 | ruflo | HİÇ GİRMEMİŞ | # RUFLO-2 — gerçek Ruflo kurulumu + ders sistemi ana oturumlara + tek banka + işe yarayan dersler | sonnet |
| site-okulu-1 | site | HİÇ GİRMEMİŞ | # SİTE-OKULU-1 — ödüllü siteler nasıl yapılıyor: ekran + kod + hazır kaynak + eksiklerimiz (14 Eki 19:20) | sonnet |
| site-okulu-2 | site | HİÇ GİRMEMİŞ | # SİTE-OKULU-2 — teknik laboratuvarı: ekran görüntüsünden yeniden üret, dene, geliş (14 Eki 19:20) | sonnet |
| skill-butce-1 | skill | HİÇ GİRMEMİŞ | SKILL-BUTCE-1 — CC skill listeleme bütçesi taşıyor: skill'lerin çoğu açıklamasız görünüyor (Desktop 12 Eki 03: | sonnet |
| skill-paket-2 | skill | HİÇ GİRMEMİŞ | ERTELENDİ (Ömer 12 Eki 09:54): CC↔claude.ai farkı en sonda, video işi mükemmel hale geldikten sonra ÇİFT DİKİŞ | ücretsiz |
| skill-secim-1 | skill | HİÇ GİRMEMİŞ | SKILL-SECIM-1 — HER skill doğru işte seçilsin (CC + claude.ai), oturum jetonu artmadan (Desktop 12 Eki 10:58;  | ücretsiz |
| slash-ogren | slash | HİÇ GİRMEMİŞ | # SLASH-ÖĞREN — "/" ile çağrılan bütün skill/komutları öğren, CC + alt ajanlar kullansın | sonnet |
| sleep-1 | sleep | HİÇ GİRMEMİŞ | # SLEEP-1 — SkillOpt-Sleep "uyku döngüsü" sıfır maliyetli, kum havuzunda kurulum (.kos/sleep) | sonnet |
| sonra-muzik-kanali | sonra | HİÇ GİRMEMİŞ | # SONRA (Ömer, 22 Eki) — günlük müzik videosu otomasyonu | haiku |
| streetball-0 | streetball | HİÇ GİRMEMİŞ | # STREETBALL-0 — "yerel streetball" projesinin durum analizi (SALT OKUMA) | sonnet |
| tasarim-1 | tasarim | HİÇ GİRMEMİŞ | TASARIM-1 — AI-slop olmayan en iyi tasarımları araştır, öğren, bir üst seviyeye çık (Desktop 12 Eki 07:35; Öme | sonnet |
| tasarim-2 | tasarim | HİÇ GİRMEMİŞ | TASARIM-2 — yakınsamayı kır + bütün tasarım/frontend kaynaklarımızla AI-slop olmayan, çok daha kaliteli tasarı | sonnet |
| temiz-yeniden-1 | temiz | HİÇ GİRMEMİŞ | [BEKLEMEDE — Ömer 23 Eki 11:22: sıfırdan yazma yok; kodlar kullanılıp geliştirilecek. Yayın/müşteri için önce  | sonnet |
| ters-1 | ters | HİÇ GİRMEMİŞ | # TERS-1 — REA kurulumu + `tersine` skill'i (tersine mühendislik şeridi, ilk oturum) | sonnet |
| ters-2 | ters | HİÇ GİRMEMİŞ | # TERS-2 — `tersine` skill kapısı güçlü yazarla (Ömer 20 Eki 19:01 onayı: "1 ile halledelim") | sonnet |
| token-10 | token-10 | HİÇ GİRMEMİŞ | # TOKEN-10 — TÜM ajanlar listede kalsın, açıklamalar sıkışsın (Ömer kararı 13 Eki 20:41) | sonnet |
| token-11 | token-11 | HİÇ GİRMEMİŞ | # TOKEN-11 — skill listesi her istekte ne kadar tutuyor? ÖNCE ÖLÇ (Ömer onayı 13 Eki 20:59: "hee tamam") | sonnet |
| token-12 | token-12 | HİÇ GİRMEMİŞ | # TOKEN-12 — kaynaksız 87 agency-agents ajanının açıklaması sıkışır (Ömer onayı 13 Eki 22:34: "tamam yapalım k | sonnet |
| token-2 | token-2 | HİÇ GİRMEMİŞ | # TOKEN-2 — üst kademe: Blender + site + kullandığımız her şey (14 Eki 12:40, 12:45 ek) | sonnet |
| token-3 | token-3 | HİÇ GİRMEMİŞ | # TOKEN-3 — bir üst kademe: oturum başı, alt ajan, efor, ölçüm koşuları (14 Eki 17:50) | sonnet |
| token-4 | token-4 | HİÇ GİRMEMİŞ | # TOKEN-4 — araç katmanı: tasarruf yapan HER aracı bir üst seviyeye çıkar (Desktop 14 Eki 21:20) — ajan_sira,  | sonnet |
| token-7a | token-7a | HİÇ GİRMEMİŞ | TOKEN-7a — token araçları: envanter + yarım kalanları tamamla + kurulmayanları kur | sonnet |
| token-7b | token-7b | HİÇ GİRMEMİŞ | TOKEN-7b — ölçüm turu: her token ayarı/aracı A/B, kalite ≥ taban | sonnet |
| token-7c | token-7c | HİÇ GİRMEMİŞ | TOKEN-7c — kurulu token araçlarının kötü yanını gider, iyi yanını geliştir + model yönlendirme | haiku |
| token-8-f2b | token-8 | HİÇ GİRMEMİŞ | # TOKEN-8 f2b — iş 2 (ajan listesi) önce ÖLÇ, sonra yap; iş 3 ayrımı; iş 4 keşif (Desktop 13 Eki 16:12) | sonnet |
| token-8-f2c | token-8 | HİÇ GİRMEMİŞ | # TOKEN-8 f2c — iş 3 uygula, iş 2 v2 (seçim kaybını kapat), iş 4 kanca kısaltma (Desktop 13 Eki 16:40) | sonnet |
| token-8-f2d | token-8 | HİÇ GİRMEMİŞ | # TOKEN-8 f2d — iş 4 davranış kapısını güçlendir (Desktop 13 Eki 17:40) | sonnet |
| token-8-f2d-gorevler | token-8 | HİÇ GİRMEMİŞ | # TOKEN-8 f2d — 8 görev (Desktop yazdı, 13 Eki 17:55; transcript okunmadı — sınıflandırıcı kararı aşılmadı) | sonnet |
| token-9 | token-9 | HİÇ GİRMEMİŞ | # TOKEN-9 — köprü ajanı oturum verimliliği: keşif + ölçüm (kod/canlı değişiklik YOK) (Desktop 13 Eki 18:50) | ücretsiz |
| token-rea | token-rea | HİÇ GİRMEMİŞ | # TOKEN-REA — token + hafıza araçlarımızın daha iyi sürümleri (REA + tersine) | sonnet |
| tur-6c-b1 | tur-6c | HİÇ GİRMEMİŞ | TUR-6c-B1 — kurulum listesini temizle, araştır, sahnele (canlı ayara dokunmadan) | sonnet |
| tur-6c-b2 | tur-6c | HİÇ GİRMEMİŞ | # TUR-6c-B2 — sahnelenenleri canlıya hazırla (onay betiği) — Ömer 10 Eki "RED dışında her şey kurulsun, CC + D | sonnet |
| ua-test-3-sonuc | ua | HİÇ GİRMEMİŞ | # UA-TEST-3 sonuç | sonnet |
| ucretsiz-havuz | ucretsiz | HİÇ GİRMEMİŞ | # UCRETSIZ-HAVUZ-1 — elimizdeki BÜTÜN ücretsiz model kaynaklarını tek havuzda kullan | sonnet |
| video-13 | video | HİÇ GİRMEMİŞ | VİDEO-13 — yakalamayı yükselt (araç + link) + kare ayıklamanın kaliteyi düşürmeyen yeni sürümü (C3). Ömer 11 E | sonnet |
| video-14 | video | HİÇ GİRMEMİŞ | VİDEO-14 — UZUN video hattını hızlandır + iyileştir (Ömer 11 Eki 23:56) | sonnet |
| video-15 | video | HİÇ GİRMEMİŞ | VİDEO-15 — birleşik KABUL → varsayılan + main + uzun-6 devam (Desktop 12 Eki 06:33; Ömer 06:23/06:26 "bugün ek | sonnet |
| video-16 | video | HİÇ GİRMEMİŞ | VİDEO-16 — SHORTS/REELS HIZ + KALİTE (Desktop 12 Eki 07:03; Ömer 07:00: "uzun videoyu bugünlük erteleyelim; 40 | sonnet |
| video-3 | video | HİÇ GİRMEMİŞ | # VİDEO-3 — video hattı "mükemmel": uzun + kısa + carousel, uçtan uca (14 Eki 18:00) | sonnet |
| video-hiz | video | HİÇ GİRMEMİŞ | # VİDEO-HIZ-2 — uzun videoda hız + jeton + kalite (Ömer 11 Eki 03:33) | sonnet |
| video-kisa-2 | video | HİÇ GİRMEMİŞ | # VİDEO-KISA-2 — 180 linki yeni kısa video hattıyla işle (Desktop 14 Eki 20:30) — ajan_sira, cwd omer-skills | ücretsiz |
| video-kisa-token-2 | video | HİÇ GİRMEMİŞ | # VİDEO-KISA-TOKEN-2 — video başı Claude token'ını ~4–5× daha düşür, kalite/hız artsın (Desktop 14 Eki 20:50)  | sonnet |
| wt-arsiv-1 | wt | HİÇ GİRMEMİŞ | # WT-ARŞİV-1 — 7 eski birleşmemiş worktree arşivlenir, yer açılır (Ömer onayı 13 Eki 22:34: "tamam arşivleyeli | sonnet |
| yarim-g1-devam-2 | yarim-g1 | HİÇ GİRMEMİŞ | DEVAM (DNS kesintisi sonrası) — önceki kısmi çıktı: ajan-sira/yarim-g1-devam-2.json | ücretsiz |
| yonetici-api-1-devam | yonetici | HİÇ GİRMEMİŞ | DEVAM (limit kesintisi sonrası) — son kısmi çıktı: ajan-sira/yonetici-api-1-devam-a2.json | sonnet |
| ajan-akis-1 | ajan | BİTTİ kanıtlı (git af55760a ajan-akis-1: opus-akis çekirdeği haiku/sonnet/ücret) | — | sonnet |
| ajan-akis-2 | ajan | BİTTİ kanıtlı (git 737f3701 ajan-akis-2: 25 aday karar (6 UYARLA/11 ÖĞREN/8 RED) | — | sonnet |
| arac-bul-2b | arac | BİTTİ kanıtlı (git cf9ff31b YARIM-A1: ret-denetim-1 (193 satır sınıflandı, ELE→) | not: bulunamadı" row needs a filled reason column before a report is written. - `.kos/` is gitignored, so | sonnet |
| arac-denetim-1 | arac | BİTTİ kanıtlı (git fc71d0bd arac-denetim-1: kullanım denetimi tablosu (tools/ar) | — | haiku |
| arac-indir-1 | arac | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/arac-indir-1-a.json) | not: bulunamadı" satırının nedeni kaydedilmemiş ve rapor commit edilmedi. - **Tekil:** 112 satır (girdi 1 | sonnet |
| arac-kapi-1 | arac | BİTTİ kanıtlı (git 7c9ea9f1 YARIM-C2: rapor (arac-kapi-1b bitti, 5 zaten bitmiş) | — | sonnet |
| arac-kapi-1b | arac | BİTTİ kanıtlı (git 7c9ea9f1 YARIM-C2: rapor (arac-kapi-1b bitti, 5 zaten bitmiş) | not: yapılmadı. Rapor dosyasındaki "tam suit doğrulanmadı" satırı bu sonuçla güncel değil, düzeltmedim. | sonnet |
| arac-zorunlu-4 | arac | BİTTİ kanıtlı (git bdab1c58 arac-zorunlu-4: pasif çekirdek, canlı tam set, iş t) | — | sonnet |
| arac-zorunlu-4b | arac | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/arac-zorunlu-4b.json) | — | sonnet |
| arka-bekci-1 | arka | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/arka-bekci-1.json) | — | sonnet |
| arka-kalici-1 | arka | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/arka-kalici-1-a.json) | — | sonnet |
| atlas-1-d1 | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-1-d1.json) | — | haiku |
| atlas-1-d1e | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-1-d1e.json) | — | haiku |
| atlas-1-d1f | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-1-d1f.json) | — | haiku |
| atlas-1-d1g | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-1-d1g.json) | — | haiku |
| atlas-2-d1 | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-2-d1.json) | — | haiku |
| atlas-2-d1b | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-2-d1b.json) | — | haiku |
| atlas-2-d1c | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-2-d1c.json) | — | haiku |
| atlas-2-d1d | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-2-d1d.json) | not: yapılmadı. Çağrı tavanına (45) ulaştığım için burada durdum. - **Commit:** `c4ac9002`, main'de, push | haiku |
| atlas-2-d1e | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-2-d1e.json) | — | haiku |
| atlas-2-d1f | atlas | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/atlas-2-d1f.json) | — | haiku |
| autoharness-fix-1 | autoharness | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/autoharness-fix-1-a.json) | — | sonnet |
| autoharness-kur | autoharness | BİTTİ kanıtlı (git ed4fdb44 autoharness-kur-2: kayba autoharness kuruldu, hook ) | — | haiku |
| autoharness-kur-2 | autoharness | BİTTİ kanıtlı (git ed4fdb44 autoharness-kur-2: kayba autoharness kuruldu, hook ) | — | sonnet |
| autoharness-kur-2-a2 | autoharness | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/autoharness-kur-2-a2.json) | not: bulunamadı; ai-labs-paket model çağrısına kapalı. Bu dört araç kullanılamadı. - **Bütçe:** yaklaşık  | sonnet |
| base-kur-1 | base | BİTTİ kanıtlı (base-kur-1.md) | not: Kalan iş:** `base tune` için bekleyen bir kural geçişi var. `claude -p` kullanıcı ayarlarında `enabl | sonnet |
| base-kur-1-a2 | base | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/base-kur-1-a2.json) | not: yapılmadı. **Sapmalar:** - `katalog_kanca.py` çıktı vermedi. Çağrıldığını söyleyebilirim, çalıştığın | sonnet |
| baslangic-hiz-1 | baslangic | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/baslangic-hiz-1-a.json) | not: Yapılmadı:** toplu kayıt yaması. Kayıt API'sinde toplu çağrı yok. Yama, 24+ üçüncü taraf eklentinin  | sonnet |
| baslangic-hiz-2 | baslangic | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/baslangic-hiz-2-a.json) | — | sonnet |
| baslangic-hiz-2b | baslangic | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/baslangic-hiz-2b.json) | — | sonnet |
| baslangic-hiz-2c | baslangic | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/baslangic-hiz-2c.json) | — | sonnet |
| baslangic-hiz-2d | baslangic | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/baslangic-hiz-2d-a.json) | not: yapılmadı, Desktop/Ömer'e kalır. | sonnet |
| baslangic-hiz-2d-a2 | baslangic | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/baslangic-hiz-2d-a2.json) | — | sonnet |
| beyin-1-d1 | beyin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/beyin-1-d1.json) | — | haiku |
| beyin-1-d1b | beyin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/beyin-1-d1b.json) | — | haiku |
| beyin-1-d2 | beyin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/beyin-1-d2.json) | — | haiku |
| beyin-3-d1 | beyin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/beyin-3-d1.json) | — | sonnet |
| beyin-3-d2 | beyin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/beyin-3-d2.json) | — | sonnet |
| beyin-arac-kart-1 | beyin | BİTTİ kanıtlı (beyin-arac-kart-1.md) | not: yapılmadı+neden" formatında belgendi 8. Kural K2m uyarısı: oturum bittiğinde KAPANIR, arka plan işi  | sonnet |
| beyin-arac-kart-1-2 | beyin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/beyin-arac-kart-1-2-a.json) | — | haiku |
| beyin-canli-1b | beyin | BİTTİ kanıtlı (git 46f5439c YARIM-B1: beyin-canli-1b 4 görev tetikleri (oturum ) | not: yapılmadı. - **$0 kanıtı:** `tools/beyin_dusun.py` ve `beyin_kayit.py` Claude çağırmıyor (grep: yaln | sonnet |
| beyin-kaydet-1 | beyin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/beyin-kaydet-1-a.json) | not: yapılmadı. - **Test:** `tests/test_beyin_kaydet.py` 4/4 geçti. - **Tekrar koruması:** Aynı metni iki | sonnet |
| beyin-kayit-1 | beyin | BİTTİ kanıtlı (git 37d8b46d beyin-kayit-1) | — | haiku |
| bulut-1 | bulut | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/bulut-1.json) | — | sonnet |
| code-mode-ab-1 | code | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/code-mode-ab-1-a.json) | — | sonnet |
| code-mode-ab-1-a2 | code | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/code-mode-ab-1-a2.json) | — | sonnet |
| code-mode-rea-1 | code | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/code-mode-rea-1-a.json) | not: açık iş olarak duruyor. - **Araçlar:** - `gitleaks`: temiz. - `semgrep`: `tools/cm.py` taraması çıkt | sonnet |
| code-mode-rea-2 | code | BİTTİ kanıtlı (code-mode-rea-2.md) | — | sonnet |
| cuda-kur-1 | cuda | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/cuda-kur-1.json) | — | haiku |
| cuda-kur-2 | cuda | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/cuda-kur-2.json) | not: Yapılmadı:** `beyin kaydet` CLI'de yok (yalnız `ara`), ders ruflo pattern-store id 5'e yazıldı. Remo | haiku |
| cuda-kur-3 | cuda | BİTTİ kanıtlı (git 6253b9c1 cuda-kur-3-devam7: ekran adı düzeltici video_derin ) | not: Yapılmadı:** OCR'ı `tools/video_derin.py` hattına bağlama, 10 videoluk yeniden profil, WER testi (≤% | haiku |
| cuda-kur-3-devam2 | cuda | BİTTİ kanıtlı (git dc11b682 cuda-kur-3-devam2: GPU OCR video hattinda, adim pro) | not: yapılmadı. - OCR kapsama ≥%98 ve GPU log ≥%85: ölçülmedi. Önceki turda GPU kullanımı ~%11 idi. - Vid | sonnet |
| cuda-kur-3-devam4 | cuda | BİTTİ kanıtlı (git d4b7fdff cuda-kur-3-devam4: ASR large-v3 (WER %5,6 -> %2,75 ) | — | sonnet |
| cuda-kur-3-devam5 | cuda | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/cuda-kur-3-devam5-a.json) | not: kalan:** 42 belirsiz kelime (`belirsiz.json`) ucuz alt ajanla karara bağlanmadı; `karar.json` dosyal | sonnet |
| cuda-kur-3-devam6 | cuda | BİTTİ kanıtlı (git ba48778e cuda-kur-3-devam6: hakemli leave-one-out WER, ASR h) | — | sonnet |
| cuda-kur-3-devam7 | cuda | BİTTİ kanıtlı (git 6253b9c1 cuda-kur-3-devam7: ekran adı düzeltici video_derin ) | not: Yapılmadı:** `beyin kaydet` (CLI'de kaydet yok, memory'de not var). Commit yok; çalışma ağacında ilg | sonnet |
| dans-1 | dans | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/dans-1.json) | — | sonnet |
| denetim-ayar-1 | denetim | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/denetim-ayar-1-a.json) | — | sonnet |
| denklik-1 | denklik | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/denklik-1-devam.json) | — | sonnet |
| derin-tamamla-1 | derin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/derin-tamamla-1-a.json) | — | sonnet |
| derin-toplu-7 | derin | BİTTİ kanıtlı (git c959cdcd derin-toplu-7: toplu_gozetmen (rc!=0/BITIS'siz olum) | not: Kalan iş yok: son koşu 24 linki zaten denedi ve hepsi başarısız oldu. Yeniden başlatmadım, çünkü ayn | sonnet |
| derin-yeni-1 | derin | BİTTİ kanıtlı (git 75172b15 YARIM-G1: derin-yeni-1 raporuna 5 eksik link, kayna) | — | sonnet |
| ders-dongu-1 | ders | BİTTİ kanıtlı (git 471fa823 YARIM-B1: ders-dongu-1 otomatik ders üretimi (derin) | not: yapılmadı. Commit `08488471`. 15 test geçti (9 yeni ders_dongu, 6 ajan_cekirdek). Tam suit koşmadım. | sonnet |
| egitim-1 | egitim | BİTTİ kanıtlı (git 72d54cf1 egitim-1: damitma (damit.py, sablonlar), sarmal+hav) | not: yapılmadı. Önce kapının zorlaştırılması gerekiyor. - Alt ajan tanımlarına şablon eklenmedi; ajan tan | sonnet |
| envanter-kullan-1 | envanter | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/envanter-kullan-1.json) | — | sonnet |
| erisim-tam-1 | erisim | BİTTİ kanıtlı (git c648fe99 erisim-tam-1: arac kapisi (mcp_kapi), ToolSearch di) | — | sonnet |
| erisim-tam-1b | erisim | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/erisim-tam-1b.json) | not: Yapılmadı:** yüzey × kategori kapsama tablosu, sunucu başına 1 çağrı, 3 skill ve 3 CLI sınaması, mad | sonnet |
| erisim-tam-1c | erisim | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/erisim-tam-1c.json) | — | sonnet |
| erisim-tam-1d | erisim | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/erisim-tam-1d.json) | not: Yapılmadı** - **CC etkileşimli ve Desktop yüzeyi 3'er çağrı:** kapı kullanıcı MCP'sinde kayıtlı deği | sonnet |
| erisim-tam-1e | erisim | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/erisim-tam-1e.json) | — | sonnet |
| fable-kur-1 | fable | BİTTİ kanıtlı (git d1046198 fable-kur-1: fable-dusunme skill (marketplace plugi) | — | haiku |
| graphify-ram-1 | graphify | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/graphify-ram-1.json) | — | sonnet |
| graphify-ultra-1-d1 | graphify | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/graphify-ultra-1-d1.json) | — | haiku |
| graphify-ultra-1-d3 | graphify | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/graphify-ultra-1-d3.json) | not: yapılmadı. - **Kompakt sorgu (G3):** `graphify query --budget 400` 5 soruda 14–24 satır döndü, ≤40 h | haiku |
| graphify-ultra-1-d4 | graphify | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/graphify-ultra-1-d4.json) | — | haiku |
| graphify-ultra-1-d5 | graphify | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/graphify-ultra-1-d5.json) | — | haiku |
| hakem-fix-1 | hakem | BİTTİ kanıtlı (git 3cac10ae hakem-fix-1: ayrıştırma hatası kararsız (puan 0 değ) | — | haiku |
| havuz-genis-1 | havuz | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/havuz-genis-1.json) | not: yapılmadı. - **Envanter:** `.kos/kopru/havuz-envanter.tsv`, 112 satır (`tools/havuz_envanter.py`). H | haiku |
| havuz-genis-1b | havuz | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/havuz-genis-1b.json) | — | haiku |
| havuz-onar-1 | havuz | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/havuz-onar-1.json) | — | sonnet |
| ig-42 | ig | BİTTİ kanıtlı (git 9a29fac3 YARIM-D1: karusel postlar (125 /p tüm slayt) + ig-4) | not: yapılmadı. KUR oranı (29/44) şüpheli, çünkü özet yalnız ses transkripti ve ücretsiz modelle çıkarıld | haiku |
| ig-giris-1 | ig | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ig-giris-1-a.json) | not: yapılmadı:** çerez yokken aynı 24 link aynı giriş duvarına takılır; 0/24 ok. - **Test:** çerez fonks | sonnet |
| ig-ornek-1 | ig | BİTTİ kanıtlı (git 73d17214 ig-ornek-1 satir siniri (25)) | not: yapılmadı. `gorsel_hakem` 170 sn'de zaman aşımına uğradı. - **ÖRNEK AKIŞ:** on-söz 2c yalnız prompt' | haiku |
| ig-toplu-2 | ig | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ig-toplu-2-a.json) | — | sonnet |
| kaynak-kutuphane-1 | kaynak | BİTTİ kanıtlı (kaynak-kutuphane-1.md) | — | sonnet |
| kaynak-kutuphane-1-p3 | kaynak | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kaynak-kutuphane-1-p3.json) | not: bulunamadı; GitHub'da çıkan repolar (fflate, slick) üçüncü taraf bağımlılık, bu yüzden alınmadı. - H | haiku |
| kaynak-kutuphane-1-p4 | kaynak | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kaynak-kutuphane-1-p4-a.json) | — | haiku |
| kaynak-kutuphane-1-p5 | kaynak | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kaynak-kutuphane-1-p5-r1-rd.json) | not: Yapılmadı:** Sitelerin yeniden taranması ve `.kos/kopru/ara/` ilerleme notu yazılması. İkisi de gere | haiku |
| kaynak-site-1 | kaynak | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kaynak-site-1-a.json) | not: yapılmadı. - 1045 "belirsiz" tür için ad→tür eşlemesi ücretsiz model ile yapılmadı. Bu gereksinim ka | sonnet |
| kaynak-site-2 | kaynak | BİTTİ kanıtlı (git 72dac52e kaynak-site-2: 819 site sinifi, 217 derin kart, 245) | — | sonnet |
| kaynak-site-3 | kaynak | BİTTİ kanıtlı (git b2cda0a1 kaynak-site-3: semgrep 101/101, kart dogrulama 159/) | — | sonnet |
| kaynak-tam-1 | kaynak | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kaynak-tam-1.json) | not: yapılmadı, bütçe yetmedi. Tek ölçüm, 30 videoluk örneklemde 18 URL'nin hepsinin tabloda bulunması. B | sonnet |
| kaynak-tam-2 | kaynak | BİTTİ kanıtlı (git fff1b781 kaynak-tam-2: llm birlestir (42295 satir, prompt 10) | — | sonnet |
| kaynak-tam-3 | kaynak | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kaynak-tam-3-a.json) | not: Yapılmadı:** ruflo `pattern-store`. Ruflo MCP aracı bu oturumda yüklü değil, araç aramasında çıkmadı | sonnet |
| kaynak-tam-4 | kaynak | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kaynak-tam-4-a.json) | not: açık işlem kalmadı. Geçici `gl-tmp.json` silindi. | sonnet |
| kaynak-tam-fix-1 | kaynak | BİTTİ kanıtlı (git 9f8ef081 kaynak-tam-fix-1 ara notu) | — | sonnet |
| konsol-502-1 | konsol | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/konsol-502-1.json) | — | sonnet |
| konsol-defter-1 | konsol | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/konsol-defter-1-a.json) | — | sonnet |
| konsol-gecis-2 | konsol | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/konsol-gecis-2-r1.json) | not: yapılmadı. - **Ders:** ruflo `pattern-store` kaydedildi (id 290). Bütçe $0,15 hedefini aştım, işi bi | sonnet |
| kopru-cwd-1 | kopru | BİTTİ kanıtlı (git 8b12ba87 kopru-cwd-1: ajan-sira cwd= sütunu; klasör yoksa ba) | — | haiku |
| kucuk-1 | kucuk | BİTTİ kanıtlı (git 7c9ea9f1 YARIM-C2: rapor (arac-kapi-1b bitti, 5 zaten bitmiş) | not: yapılmadı, anahtar hiçbir yere yazılmadı, repo dosyası değişmedi (commit/push yok). Rapor: `.kos/kop | haiku |
| kucuk-4 | kucuk | BİTTİ kanıtlı (git fcc92528 kucuk-4: yetim.py (liste/durdur), mem_bekci 5 dk ye) | not: kalan:** 12 süreç, ~146 MB. Bunlar excalidraw node (67 MB) ve 1472 köküne bağlı conhost/cmd'ler. - * | sonnet |
| kucuk-5b | kucuk | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kucuk-5b.json) | not: yapılmadı. - **Adım 1 (blok):** `video-ek50.log` (53 satır) içinde `melez`, `karar-v2` veya `sonnet` | haiku |
| kucuk-5c | kucuk | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kucuk-5c.json) | not: yapılmadı:** `tek` sayacı daha önceki koşudan 60/60 doluydu. Düşük güvenli/ELE 4 video (2 ELE, 2 ÖĞR | sonnet |
| kucuk-6 | kucuk | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kucuk-6.json) | — | sonnet |
| kucuk-7 | kucuk | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kucuk-7.json) | — | sonnet |
| kucuk-8 | kucuk | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kucuk-8.json) | — | sonnet |
| kucuk-8b | kucuk | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kucuk-8b.json) | — | sonnet |
| kur-xerj-guard-1 | kur | BİTTİ kanıtlı (kur-xerj-guard-1.md) | not: durdurulduğunu söylüyor. Yeniden başlatmıyorum. Aynı bilgiyi PowerShell ile aldım ve sonuç yukarıdak | sonnet |
| kural-beyin-1 | kural | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kural-beyin-1.json) | — | sonnet |
| kurtar-fix-1 | kurtar | BİTTİ kanıtlı (git 3b6105bf YARIM-C1: rapor (1b/1c/teshis/arka-kalici zaten bit) | not: Yapılmadı:** Mevcut Desktop çağrılarını `--bagimsiz`'e geçirmedim; bayrağın verilmesi çağıranların i | sonnet |
| kurulum-dalgasi-1 | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-dalgasi-1-a.json) | not: Yapılmadı:** modlar yeniden çıkarma, linksiz adların çözümü, npm/pip CLI kurulumları, Desktop zip/MC | sonnet |
| kurulum-dalgasi-2 | kurulum | BİTTİ kanıtlı (git 731a70aa kurulum-dalgasi-2b: p1b/token/p2/p3 betikleri (cali) | not: Yapılmadı:** Betik çalıştırılmadı, duman testi koşulmadı, arac-tam.tsv güncellenmedi, commit yok. -  | sonnet |
| kurulum-dalgasi-2b | kurulum | BİTTİ kanıtlı (git 731a70aa kurulum-dalgasi-2b: p1b/token/p2/p3 betikleri (cali) | not: yapılmadı. Ders bunun yerine beyin kaydına yazıldı. Bu turda yeni commit yok; son commit 87b14fe4 (` | sonnet |
| kurulum-laya-2 | kurulum | BİTTİ kanıtlı (git 29a5408f kurulum-laya-2) | — | sonnet |
| kurulum-reel | kurulum | BİTTİ kanıtlı (git 6213b490 kurulum-reel-d: ig-41 durum betiği, scroll-image-se) | not: bulunamadı, en yakın `scroll-craft` alındı. - **Reddedilen:** `EnzeD/r3f-skills` (LICENSE dosyası yo | haiku |
| kurulum-reel-d | kurulum | BİTTİ kanıtlı (git 6213b490 kurulum-reel-d: ig-41 durum betiği, scroll-image-se) | — | haiku |
| kurulum-reel-e | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-reel-e.json) | — | haiku |
| kurulum-reel-e2 | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-reel-e2-devam.json) | not: yapılmadı; kod değişikliği olmadığı için test koşulmadı. araç: Bash (python -I json okuma, beyin --h | haiku |
| kurulum-ua | kurulum | BİTTİ kanıtlı (git 90349ade kurulum-ua: understand-anything zip satırı ve köprü) | — | haiku |
| kurulum-v1-d2 | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-v1-d2.json) | — | sonnet |
| kurulum-v1-d5 | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-v1-d5.json) | — | sonnet |
| kurulum-video-1c | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-video-1c.json) | — | haiku |
| kurulum-video-1f | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-video-1f.json) | not: yapılmadı. - **Commit:** 87863d0 (`docs/envanter/is-arac.md`, `skills/gorsel-uret/SKILL.md`) - **Tes | haiku |
| kurulum-video-1g | kurulum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/kurulum-video-1g.json) | — | haiku |
| laya-2 | laya | BİTTİ kanıtlı (git ebb5e855 YARIM-E3: laya-2c DUR raporu (rho kapisi gecmedi, k) | not: yapılmadı; bu, kapıdan önce yapılması gereken adım. - **Kapı:** henüz ölçülmedi (ρ, MAE, ≤50 ms). Ge | sonnet |
| laya-2b | laya | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/laya-2b.json) | — | sonnet |
| laya-2c | laya | BİTTİ kanıtlı (git ebb5e855 YARIM-E3: laya-2c DUR raporu (rho kapisi gecmedi, k) | not: yapılmadı ve neden:** v2/v3 istemiyle yeni kurul koşusu yapılmadı. Mevcut `kurul.jsonl` eski ayıklay | sonnet |
| logo-1 | logo | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/logo-1.json) | — | haiku |
| logo-2 | logo | BİTTİ kanıtlı (git f3e622f8 logo-2: gorsel_hakem --sema logo (özgünlük·akılda k) | — | sonnet |
| logo-4 | logo | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/logo-4.json) | — | sonnet |
| logo-4b | logo | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/logo-4b.json) | — | sonnet |
| logo-4c | logo | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/logo-4c.json) | — | sonnet |
| logo-final | logo | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/logo-final.json) | — | sonnet |
| makara-1-d2 | makara | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/makara-1-d2.json) | — | sonnet |
| makara-1-d4 | makara | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/makara-1-d4.json) | — | sonnet |
| makara-cek-1 | makara | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/makara-cek-1.json) | not: yapılmadı, çünkü `.kos/makara/cek.json` durumunu değiştirmek istemedim. Sonraki zamanlanmış koşu ger | haiku |
| mcp-ac-1 | mcp | BİTTİ kanıtlı (git 8289e458 mcp-ac-1: ajan_sira MCP profili) | — | sonnet |
| mem-fix-3 | mem | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/mem-fix-3.json) | — | sonnet |
| nihai-duzelt-2 | nihai | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/nihai-duzelt-2.json) | — | sonnet |
| ocr-hiz-1 | ocr | BİTTİ kanıtlı (git 9eeaa0ad YARIM-D2: ses-yazı/OCR yeniden ölçüm raporu (ocr-hi) | — | sonnet |
| ogren-0 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0.json) | — | sonnet |
| ogren-0b | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b.json) | not: yapılmadı. - **Kısmi oyla deneme:** `son` uçtan uca koştu. Kurulu 4293 satırın tamamında `kategori_s | sonnet |
| ogren-0b-d10 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d10.json) | not: yapılmadı, `sira_ekle` çağrılmadı. - **(1)(2) Tanım ve girdi:** `tanim-v7.md` kompakt hâlde yazıldı: | haiku |
| ogren-0b-d11 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d11.json) | — | haiku |
| ogren-0b-d12 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d12.json) | — | haiku |
| ogren-0b-d13 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d13.json) | not: yapılmadı. - **Hakem:** hk00–03'teki 378 kalemin hepsi `denetle` ile tam çıktı. `son` sonrası güven  | haiku |
| ogren-0b-d14b | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d14b.json) | — | haiku |
| ogren-0b-d2 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d2.json) | — | haiku |
| ogren-0b-d3 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d3.json) | not: yapılmadı. 45 çağrı tavanı aşıldığı için kapıya geçmeden durdum. - **Neden hepsi Claude'a gitti:** : | haiku |
| ogren-0b-d5 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d5.json) | — | haiku |
| ogren-0b-d6 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d6.json) | — | haiku |
| ogren-0b-d7 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d7.json) | — | haiku |
| ogren-0b-d8 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d8.json) | — | haiku |
| ogren-0b-d9 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-0b-d9.json) | — | haiku |
| ogren-1 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1.json) | not: yapılmadı. graphify_sor, harita ve timeline için kaynak bulunamadı. - **Mini koşular:** - rtk: `git  | sonnet |
| ogren-1-d10 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d10.json) | — | haiku |
| ogren-1-d11 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d11.json) | — | haiku |
| ogren-1-d12 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d12.json) | — | haiku |
| ogren-1-d13 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d13.json) | — | haiku |
| ogren-1-d14b | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d14b.json) | not: yapılmadı. Kalan iş `devir/ogren-1-devam.md`'de "d14b" başlığı altında. Yeni `.claude.json` testi ön | haiku |
| ogren-1-d15 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d15.json) | — | haiku |
| ogren-1-d15b | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d15b.json) | not: durduruldu ve hiçbir şey yazmadı. `0b-borc.tsv`'de `ogren1-geri` satırı tam 6 tane, çift kayıt yok.  | haiku |
| ogren-1-d2 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d2.json) | not: yapılmadı: bellek kullanımı %71.6, eşik %70. - ucuz_alt mini koşusu 1 çağrı (1400 jeton) yaptı. Comb | haiku |
| ogren-1-d3 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d3.json) | — | haiku |
| ogren-1-d4 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d4.json) | not: bulunamadığı için reddedildi. - headroom'da nemotron'un mekanizma alıntısı reddedildi. - **Kalıntı r | haiku |
| ogren-1-d5 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d5.json) | not: yapılmadı. Bu oturumda claude -p kullanılmadı. | haiku |
| ogren-1-d6 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d6.json) | — | haiku |
| ogren-1-d7 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d7.json) | — | haiku |
| ogren-1-d9 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-1-d9.json) | — | haiku |
| ogren-2-d1 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-2-d1.json) | — | haiku |
| ogren-2-d3 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-2-d3.json) | — | sonnet |
| ogren-3-d2 | ogren | BİTTİ kanıtlı (ogren-3-d2.md) | not: yapılmadı. Devir notu `ogren-devam.md` içinde. `graphify update .` koşulmadı. Oturum maliyeti ($) öl | haiku |
| ogren-4-d1 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-4-d1.json) | not: yapılmadı. - **Denetim:** `v1.py birlestir` çalıştı; 48 kalemde gerçek RET 0 ve 20 UYARI var. 155 RE | haiku |
| ogren-4-d2 | ogren | BİTTİ kanıtlı (ogren-4-d2.md) | — | sonnet |
| ogren-4-kapanis | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-4-kapanis.json) | — | sonnet |
| ogren-6-d2 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-6-d2-devam.json) | not: Kalan:** `ogren-6-borc.tsv` olduğu gibi duruyor (Desktop kararı). - **Sapma:** t67-b hakemi üç kayna | sonnet |
| ogren-6-d3 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-6-d3.json) | not: yapılmadı. `kart.jsonl` güncellenmedi. 5 kartın açıklaması 700 karakteri aşıyor (liste `ogren-6-borc | sonnet |
| ogren-6-d4 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-6-d4.json) | not: yapılmadı. - jev metin puanlaması ve Desktop kombini denenmedi. - **Dosyalar:** `kart.jsonl`'a 148 A | sonnet |
| ogren-6-kapanis | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-6-kapanis.json) | — | sonnet |
| ogren-tur2-d1 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-tur2-d1.json) | not: yapılmadı. Kategori içi 27 (frontend 5, ajan 4, video 3, test-qa 3, güvenlik 1, veri-backend 4, araş | sonnet |
| ogren-tur2-d3 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-tur2-d3.json) | not: yapılmadı. - **Kapı sonucu:** tohum 3111 %86,2 (69/80), tohum 3112 %95,6 (65/68). 3112'de 17 kart va | sonnet |
| ogren-tur2-d5 | ogren | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogren-tur2-d5.json) | — | sonnet |
| ogrenme-2 | ogrenme | BİTTİ kanıtlı (git 3ffcd61d YARIM-G2: ogrenme-2b sinav 20 kosuldu, ders farki +) | not: Yapılmadı: sınav (madde 3, 20 senaryo seti yok), kaynak kartı enjeksiyonu (madde 4), claude.ai zip ç | sonnet |
| ogrenme-2-a2 | ogrenme | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogrenme-2-a2.json) | not: Yapılmadı:** `task-observer` skill'inin istediği gözlem dosyası yazımı ve commit yok. Bu turda kod d | sonnet |
| ogrenme-2b | ogrenme | BİTTİ kanıtlı (git 3ffcd61d YARIM-G2: ogrenme-2b sinav 20 kosuldu, ders farki +) | not: Yapılmadı. kaynak-tam-1 commit'lenmiş (`e6161033`), USTALIK-1 kartlarına bakmadım. Bağlantı noktasın | sonnet |
| ogrenme-2c | ogrenme | BİTTİ kanıtlı (git 2b7800dc ogrenme-2c: ucuz_alt Claude yolu kapali (cikis 5, o) | — | sonnet |
| ogrenme-2d | ogrenme | BİTTİ kanıtlı (git 6c604bea ogrenme-2d: olay kaynak etiketi (cc-kanca/kopru-aja) | — | sonnet |
| ogrenme-2e | ogrenme | BİTTİ kanıtlı (git 5cf1a1e1 ogrenme-2e: sinav paralel+retry, hakem aile fallbac) | — | sonnet |
| ogrenme-2f | ogrenme | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ogrenme-2f.json) | — | sonnet |
| oktan-film-1 | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-film-1.json) | not: durduruldu: `oktan-film-1` commit'i tamam, açık PR yok, bekleyen adım yok. Film hâlâ yalnız yerelde; | haiku |
| oktan-film-2 | oktan | BİTTİ kanıtlı (git d21a2146 oktan-film-2a (ara kayıt): storyboard + 3 anahtar k) | — | sonnet |
| oktan-film-2b | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-film-2b.json) | not: durduruldu. Bu beklenen bir durum: ilgili 4 aday GLB'yi zaten Hugging Face'ten elle indirmiştim ve ` | sonnet |
| oktan-film-2c | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-film-2c.json) | — | sonnet |
| oktan-film-2d | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-film-2d-a.json) | — | sonnet |
| oktan-film-3 | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-film-3.json) | not: yapılmadı, ogrenme_eksik. | sonnet |
| oktan-kapanis-1 | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-kapanis-1.json) | — | haiku |
| oktan-yayin-1 | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-yayin-1.json) | — | haiku |
| oktan-yayin-2 | oktan | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oktan-yayin-2.json) | — | haiku |
| ollama-kim-1 | ollama | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ollama-kim-1-a.json) | — | sonnet |
| olum-teshis-1 | olum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/olum-teshis-1-a.json) | not: Kalan:** kök neden için GPU/TDR olay geçmişi ve 08:50 ölümünün kaydı gerekli. Rapor için yapılmadı.  | sonnet |
| omni-ayir-d1 | omni | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/omni-ayir-d1.json) | — | haiku |
| omni-ayir-d2 | omni | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/omni-ayir-d2.json) | — | haiku |
| omni-ayir-d2b | omni | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/omni-ayir-d2b.json) | — | haiku |
| onay-toplu-1 | onay | BİTTİ kanıtlı (onay-toplu-1.md) | — | sonnet |
| ordu-1-d1 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d1.json) | not: yapılmadı. Bayrak kapalı kaldı. d2 listesinden `graphify update .` maddesi düştü. `git commit --only | sonnet |
| ordu-1-d10 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d10.json) | — | sonnet |
| ordu-1-d11 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d11.json) | not: yapılmadı. **★ d12:** `runner_yenile` ile yeni önsözü canlıya al. Sonra 5–10 gerçek köprü işinde `to | sonnet |
| ordu-1-d12 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d12.json) | — | sonnet |
| ordu-1-d2 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d2.json) | — | sonnet |
| ordu-1-d3 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d3.json) | — | sonnet |
| ordu-1-d5 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d5.json) | — | sonnet |
| ordu-1-d7 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d7.json) | — | sonnet |
| ordu-1-d8 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d8.json) | — | sonnet |
| ordu-1-d9 | ordu | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ordu-1-d9.json) | — | sonnet |
| oyun-modu-1 | oyun | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/oyun-modu-1-a.json) | — | sonnet |
| parfum-ajan-1 | parfum | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/parfum-ajan-1-a.json) | — | sonnet |
| ram-1 | ram | BİTTİ kanıtlı (git 55538244 ram-1: ajan env node heap tavanı, önce/sonra notu) | not: yapılmadı. Commit `55538244`. - **Önceki turdan kalan:** ağaç ölçümü (`docs/ram/olcum.md`) ve kuyruk | sonnet |
| ram-az-1 | ram | BİTTİ kanıtlı (git 88b2b901 ram-az-1: keep_alive 0 (video_derin), bekci llama-s) | not: Yapılmadı:** - `NODE_OPTIONS` 2048→1024 değişmedi, çünkü ölçülebilir fark yok ve canlı A/B ücretli.  | sonnet |
| ram-bekci-1 | ram | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ram-bekci-1-a.json) | — | sonnet |
| ram-bekci-2 | ram | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ram-bekci-2-a.json) | — | sonnet |
| ram-bekci-3c | ram | BİTTİ kanıtlı (ram-bekci-3c.md) | not: Yapılmadı: - 47801 havuzunun makine açılışında başlatılması. Startup vbs yok, yeniden açılışta ajanl | sonnet |
| rc1-teshis-1 | rc1 | BİTTİ kanıtlı (rc1-teshis-1.md) | — | sonnet |
| rea-agir-1 | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-agir-1-a.json) | not: Yapılmadı:** HN ve orta boy SPA'da %98 örtüşme kapısı, figma, notion ve Electron hedefleri, `heavy-t | sonnet |
| rea-agir-2 | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-agir-2-a.json) | — | sonnet |
| rea-fix-2 | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-fix-2-a.json) | — | sonnet |
| rea-fix-3 | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-fix-3.json) | not: Bulunamadı. `rea_ajv.js` Desktop'un gerçek env'iyle (`compact` girdi, `OUTPUT_SCHEMA_PROFILE=off`) k | sonnet |
| rea-fix-4 | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-fix-4.json) | — | sonnet |
| rea-fix-5 | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-fix-5.json) | not: Yapılmadı:** ruflo `pattern-search` / `pattern-store` çalıştırılmadı (araç çağrı bütçem yetmedi). De | sonnet |
| rea-fix-5b | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-fix-5b-a.json) | — | sonnet |
| rea-kur | rea | BİTTİ kanıtlı (git 4eef9aa4 rea-kur: rea (mcp) + reverse-engineer-anything (ski) | — | sonnet |
| rea-usta-1 | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-usta-1-a.json) | — | sonnet |
| rea-usta-1b | rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/rea-usta-1b-a.json) | — | sonnet |
| ret-denetim-1 | ret | BİTTİ kanıtlı (git cf9ff31b YARIM-A1: ret-denetim-1 (193 satır sınıflandı, ELE→) | not: yapılmadı. Yapılan tek şey, sınıflanmamış bir envanter tablosu. - **Envanter:** `.kos/kopru/ret-dene | haiku |
| ret-kur-1 | ret | BİTTİ kanıtlı (git ed13ddef ret-kur-1-a: skillspector --no-llm taraması (7 repo) | — | sonnet |
| router-1-d1 | router | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/router-1-d1.json) | not: yapılmadı. - Haftalık özet bir betik değil, `yonlendir.py ozet` komutu. - Kayıt dosyası `.kos/` giti | haiku |
| router-1-d2 | router | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/router-1-d2.json) | — | haiku |
| router-1-d2b | router | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/router-1-d2b.json) | — | haiku |
| ruflo-bag-1 | ruflo | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ruflo-bag-1-a.json) | not: yapılmadı. | sonnet |
| saglik-1 | saglik | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/saglik-1.json) | not: yapılmadı; bu beyin CLI'sinde yalnız `ara` komutu var. Ruflo'ya test kayıtları yazıldı. araç: ruflo  | haiku |
| sayac-fix-1 | sayac | BİTTİ kanıtlı (git c1ad8124 sayac-fix-1: kuyruk ajanında çağrı sayacı DUR basma) | — | haiku |
| site-okulu-1-d1 | site | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/site-okulu-1-d1.json) | not: Kalan iş değişmedi: dist zip, zip_denetle, ~/.claude kopyası ve ATLAS kartları. Komutları `.kos/kopr | haiku |
| site-okulu-1-d2 | site | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/site-okulu-1-d2.json) | not: yapılmadı. Bu iş TELVE-R3'e ait, `telve-r3b` görevi de zaten açık. - `.claude/dalga.md` TOKEN-7b'den | haiku |
| site-okulu-2-d1 | site | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/site-okulu-2-d1.json) | not: yapılmadı, o yüzden hiçbir teknik için "BİTTİ" demiyorum. - **Commit:** `e85cabf1` (main'de, push yo | haiku |
| site-okulu-2-d2 | site | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/site-okulu-2-d2.json) | — | haiku |
| site-okulu-2-d3 | site | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/site-okulu-2-d3.json) | — | haiku |
| site-okulu-2-d4 | site | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/site-okulu-2-d4.json) | — | haiku |
| site-okulu-2-d5 | site | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/site-okulu-2-d5.json) | — | haiku |
| skill-dogrula-1 | skill | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/skill-dogrula-1-a.json) | not: Yapılmadı:** HawkScan (çalışan uygulama ve HAWK_API_KEY yok), ruflo pattern-search ve pattern-store  | sonnet |
| skill-dogrula-1-a2 | skill | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/skill-dogrula-1-a2.json) | — | haiku |
| skill-mode-2 | skill | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/skill-mode-2.json) | not: yapılmadı; test kümesi ölçümde görüldü, ancak kaçanlar listesi yazılan kodda test sorgularını da kap | sonnet |
| skill-mode-3 | skill | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/skill-mode-3-r1.json) | — | sonnet |
| skill-yukle-1 | skill | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/skill-yukle-1-a.json) | — | sonnet |
| skill-yukle-1b | skill | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/skill-yukle-1b-a.json) | not: Açık iş:** Ömer'in yapacağı bir adım yok. Önceki turdan kalan seo-cockpit 2c kök neden işi sürüyor.  | sonnet |
| slash-ogren-d1 | slash | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/slash-ogren-d1.json) | — | sonnet |
| slash-ogren-d3 | slash | BİTTİ kanıtlı (slash-ogren-d3.md) | not: Yapılmadı: - katalogun zip içine kopyası ve `dist/slash-2`; - 5 kart için gerçek ölçüm; - video-izle | sonnet |
| slash-ogren-d4 | slash | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/slash-ogren-d4.json) | not: yapılmadı. SIRA ve Obsidian kapanışını da yapmadım. Commit `b6524dd1`. `test_ajan_sira.py` 8/8 geçti | sonnet |
| sleep-1-d1 | sleep | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/sleep-1-d1.json) | not: yapılmadı, `~/.claude`'a hiçbir şey yazılmadı, commit yok. - **Sapma:** Koruma ölçümü sırasında `plu | haiku |
| sleep-1-d1b | sleep | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/sleep-1-d1b.json) | — | haiku |
| stalemap-kur-2 | stalemap | BİTTİ kanıtlı (stalemap-kur-2.md) | — | sonnet |
| streetball-0-d1 | streetball | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/streetball-0-d1.json) | — | haiku |
| suit-fix-1 | suit | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/suit-fix-1-devam-rd-lm.json) | not: Yapılmadı:** Düzeltmeden sonra tam suiti koşmadım (~11 dk sürüyor). Önceki üç tam koşuda başka kırmı | sonnet |
| tarayici-kapi-1 | tarayici | BİTTİ kanıtlı (tarayici-kapi-1.md) | — | sonnet |
| tekil-yonetici | tekil | BİTTİ kanıtlı (git d2edea50 tekil-yonetici: ajan_sira kilidi (pid+saat), canlı ) | — | haiku |
| ters-1-d1 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-1-d1.json) | — | sonnet |
| ters-2-d10 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d10.json) | — | sonnet |
| ters-2-d11 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d11.json) | — | haiku |
| ters-2-d11b | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d11b.json) | — | haiku |
| ters-2-d3 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d3.json) | not: yapılmadı. Kapı kararı olmadan kapanış olmaz. - **`sonuc.md`/`sonuc.json`:** Koşu tavanda `SystemExi | sonnet |
| ters-2-d4 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d4.json) | not: yapılmadı.** Koşu yazar çağrı tavanında (60/60) durdu ve `sonuc.md/json` yeniden yazılmadı. - **Koşu | sonnet |
| ters-2-d5 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d5.json) | not: yapılmadı: SKILL.md, zip, departman bağı, SIRA ve Obsidian adımlarına dokunmadım. Skill ortalaması 0 | sonnet |
| ters-2-d6 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d6.json) | — | sonnet |
| ters-2-d7 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d7.json) | — | sonnet |
| ters-2-d9 | ters | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ters-2-d9.json) | not: yapılmadı. Tur bütçesi (45) doldu ve `hedef-d9.json` oluşmadı, bu yüzden kuru doğrulama için de bir  | sonnet |
| token-2-d4d | token-2 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-2-d4d.json) | not: Kalan işler `devir/token-2-devam.md`'de: K7 site kiti, frontend-craft ve web-sahne-desenleri satırla | haiku |
| token-2-d5 | token-2 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-2-d5.json) | — | sonnet |
| token-2-d5b | token-2 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-2-d5b.json) | — | haiku |
| token-2-d5c | token-2 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-2-d5c.json) | — | haiku |
| token-3-d1 | token-3 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-3-d1.json) | — | haiku |
| token-3-d2 | token-3 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-3-d2.json) | — | haiku |
| token-3-d3 | token-3 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-3-d3.json) | — | haiku |
| token-3-d4 | token-3 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-3-d4.json) | — | haiku |
| token-3-d5 | token-3 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-3-d5.json) | — | haiku |
| token-3-d7 | token-3 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-3-d7.json) | not: kalan işler devire yazıldı. **Katalog:** kullanılan [kapi.py, arka.py, bekle.py, jev log, ucuz_alt.p | haiku |
| token-3-d8 | token-3 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-3-d8.json) | — | haiku |
| token-4-d1 | token-4 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-4-d1.json) | — | haiku |
| token-4-d2 | token-4 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-4-d2.json) | — | haiku |
| token-4-d2b | token-4 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-4-d2b.json) | — | haiku |
| token-4-d3 | token-4 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-4-d3.json) | — | haiku |
| token-4-d4 | token-4 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-4-d4.json) | — | haiku |
| token-kopru-1 | token-kopru | BİTTİ kanıtlı (git 1d0f67bc token-kopru-1) | — | haiku |
| token-olcum-27eki | token-olcum | BİTTİ kanıtlı (git 9cb00427 token-olcum-27eki: Desktop vs alt ajan token/$ rapo) | — | sonnet |
| token-rea-d12 | token-rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-rea-d12.json) | not: Yapılmadı:** claude-mem arama hızı ve context-mode tabanı. Önce A/B'yi bitirdim. - **Sapma:** Üç gör | sonnet |
| token-rea-d13 | token-rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-rea-d13.json) | not: yapılmadı. Çağrı tavanı 8'di ve 6'sı kullanıldı, ölçülen kota yükü yaklaşık $7,3 (tavan ~$8). Bu iki | sonnet |
| token-rea-d15 | token-rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-rea-d15.json) | — | sonnet |
| token-rea-d16 | token-rea | BİTTİ kanıtlı (token-rea-d16.md) | not: yapılmadı, çünkü çağrı tavanına yaklaştım. Commit `19d6446`, testler 2/2 geçti, CI'a bakmadım. - **K | sonnet |
| token-rea-d17 | token-rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-rea-d17.json) | — | sonnet |
| token-rea-d19 | token-rea | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/token-rea-d19.json) | — | sonnet |
| ua-test | ua | BİTTİ kanıtlı (git ff6a2b8f ua-test-3) | — | haiku |
| ua-test-2 | ua | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ua-test-2.json) | — | sonnet |
| ua-test-3 | ua | BİTTİ kanıtlı (git ff6a2b8f ua-test-3) | — | sonnet |
| ucretsiz-havuz-1 | ucretsiz | BİTTİ kanıtlı (git 17bef40d ucretsiz-havuz-1: tüm ücretsiz sağlayıcılar tek hav) | — | haiku |
| ucretsiz-havuz-3 | ucretsiz | BİTTİ kanıtlı (git 660f0269 ucretsiz-havuz-3: mistral ministral-8b + nvidia gpt) | — | sonnet |
| ucretsiz-motor-2 | ucretsiz | BİTTİ kanıtlı (ucretsiz-motor-2-devam.md) | not: Yapılmadı:** A2, yani hermes'i aynı 3 görevde ölçüp başa almak. Hermes zaten zincirin başında; karşı | sonnet |
| ucretsiz-motor-2-devam-rd | ucretsiz | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ucretsiz-motor-2-devam-rd-lm-a.json) | — | haiku |
| ucretsiz-motor-2-devam-rd-lm-a2 | ucretsiz | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/ucretsiz-motor-2-devam-rd-lm-a2.json) | — | haiku |
| usta-blender-1 | usta | BİTTİ kanıtlı (git 2e9d6012 kalan-6: video-13 K karari + usta-blender-1 hakem p) | — | sonnet |
| usta-blender-3 | usta | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/usta-blender-3-a.json) | — | sonnet |
| usta-blender-4 | usta | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/usta-blender-4-a.json) | — | sonnet |
| usta-blender-5 | usta | BİTTİ kanıtlı (usta-blender-5.md) | — | sonnet |
| usta-okulu-0 | usta | BİTTİ kanıtlı (git 38fb973d usta-okulu-0: müfredat envanteri, ders kitabı hattı) | — | sonnet |
| usta-web-1 | usta | BİTTİ kanıtlı (git a13ab521 usta-web-1: departman-frontend ders kitabı bağlantı) | not: Yapılmadı:** `hat.py` çelişki (B) geçişi koşulmadı. - **Atlanan araçlar:** İstediğin skill'leri (fro | sonnet |
| ustalik-1 | ustalik | BİTTİ kanıtlı (git 71400dcb ustalik-1 p1: 100 arac karti + deneme + fikir-karar) | not: bulunamadı. - **Commit:** `71400dcb`. Kartlar `kartlar/arac/` altında, aynıları Obsidian `30-araclar | sonnet |
| ustalik-1-kapi | ustalik | BİTTİ kanıtlı (ustalik-1-kapi.md) | — | sonnet |
| verim-hedef-1 | verim | BİTTİ kanıtlı (git fa21f02a verim-hedef-1) | — | sonnet |
| video-3-d10 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d10.json) | — | haiku |
| video-3-d2 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d2.json) | — | haiku |
| video-3-d3 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d3.json) | — | haiku |
| video-3-d4 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d4.json) | not: Yapılmadı: yanlış pozitif denetimi, ayrı sınama kümesi, carousel yanlış pozitif denetimi, V4/V5; hep | haiku |
| video-3-d5 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d5.json) | — | haiku |
| video-3-d6 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d6.json) | — | haiku |
| video-3-d7 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d7.json) | — | haiku |
| video-3-d9 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-3-d9.json) | — | haiku |
| video-aksiyon-1 | video | BİTTİ kanıtlı (git 09c40e06 YARIM-D3: video-aksiyon-1 tools/video_aksiyon.py + ) | not: bulunamadı, çünkü saf animasyon. Plan UYGULA bölümünde genel kaldı. Havuz çıktısındaki "karakter-vit | sonnet |
| video-denetim-1 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-denetim-1-a.json) | — | sonnet |
| video-kisa-token-1c | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1c.json) | — | haiku |
| video-kisa-token-1d | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1d.json) | — | haiku |
| video-kisa-token-1e | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1e.json) | — | haiku |
| video-kisa-token-1f | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1f.json) | not: yapılmadı. Oturumun çağrı sınırına (45) gelindiği için devir yazıp durdum. **Son ölçüm** (altın küme | haiku |
| video-kisa-token-1g | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1g.json) | — | haiku |
| video-kisa-token-1h | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1h.json) | — | haiku |
| video-kisa-token-1i | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1i.json) | — | haiku |
| video-kisa-token-1j | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1j.json) | — | haiku |
| video-kisa-token-1k | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1k.json) | not: yapılmadı. Sıradaki adım (RAM %85'in altına inince): devir notundaki tek komutla sınama koşusu (clau | haiku |
| video-kisa-token-1l | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1l.json) | — | haiku |
| video-kisa-token-1m | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1m.json) | — | haiku |
| video-kisa-token-1n | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1n.json) | — | haiku |
| video-kisa-token-1o | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-1o.json) | not: yapılmadı. SIRA.md'de başka bir oturumun commitsiz satırı var; ona dokunmadım, commit'e yalnız kendi | haiku |
| video-kisa-token-2-d1 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-2-d1.json) | not: yapılmadı; sıralı adımlar `devir/video-kisa-token-2-devam.md`'de. - Bytebase'in çıkarılması ve kırpı | haiku |
| video-kisa-token-2-d2 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-2-d2.json) | — | haiku |
| video-kisa-token-2-d3 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-2-d3.json) | — | haiku |
| video-kisa-token-2-d4 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-2-d4.json) | — | haiku |
| video-kisa-token-2-d5 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kisa-token-2-d5.json) | — | haiku |
| video-kur-1 | video | BİTTİ kanıtlı (git 8538507d video-kur-1 P2 1b-a2: LuaLS + CLIProxyAPI kuruldu, ) | not: bulunamadı, `yt-shorts` olarak çağırdım. Skill uzun videodan klip kesme içindir, bu sınıflama ve izl | sonnet |
| video-kur-1-a2 | video | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/video-kur-1-a2.json) | not: yapılmadı. - **Önceki tur:** 808 aday satırı 223 tekil adaya indi (`5283a6e7`). Karar dağılımı: / Ka | sonnet |
| video-repo-1 | video | BİTTİ kanıtlı (video-repo-1.md) | — | sonnet |
| video-repo-2 | video | BİTTİ kanıtlı (video-repo-2.md) | not: BULUNAMADI). Önceki turun raporu yerinde, bu tur eksik adımları tamamladım. Commit `8d24d7c0`. - **y | sonnet |
| video-yeniden-1 | video | BİTTİ kanıtlı (git 67282702 video-yeniden-1-p1: yerel derin tarama hattı (yt-dl) | — | haiku |
| yarim-b2 | yarim-b2 | BİTTİ kanıtlı (yarim-b2.md) | — | sonnet |
| yarim-bekci-1 | yarim-bekci | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yarim-bekci-1-a.json) | — | sonnet |
| yarim-d1 | yarim-d1 | BİTTİ kanıtlı (yarim-d1.md) | — | sonnet |
| yarim-d2 | yarim-d2 | BİTTİ kanıtlı (yarim-d2.md) | — | sonnet |
| yarim-d3 | yarim-d3 | BİTTİ kanıtlı (yarim-d3.md) | not: yapılmadı. Commit `3c1d460b`, push yok. Test koşmadım, hawkscan'i de koşmadım (çalışan uygulama ve H | sonnet |
| yarim-d4 | yarim-d4 | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yarim-d4.json) | not: kalan:** 95/95 kapısı, M5 paketi ve zip_denetle VİDEO-KISA-TOKEN-2'ye devredilmişti. TOKEN-2'nin d5  | sonnet |
| yarim-g-birlestir | yarim-g | BİTTİ kanıtlı (yarim-g-birlestir.md) | — | haiku |
| yarim-g1 | yarim-g1 | BİTTİ kanıtlı (git ace265a3 yarim-g1-devam-2: kart dogrulama 162/228 (havuz bos) | not: yapılmadı. Bu adım da aynı havuza bağlı. - **Güvenlik:** `departman-guvenlik` ve `security-reviewer` | sonnet |
| yarim-g4 | yarim-g4 | BİTTİ kanıtlı (yarim-g4.md) | not: Yapılmadı: RAM bekçisi ve bu tur için ayrılan ucuz bütçe buna elvermedi. - **laya-2 (ρ kapısı 0.6'yı | sonnet |
| yarim-h1-24eki | yarim-h1 | BİTTİ kanıtlı (yarim-h1-24eki.md) | — | haiku |
| yarim-tara-1 | yarim-tara | BİTTİ kanıtlı (yarim-tara-1.md) | — | haiku |
| yayin-tn-1 | yayin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yayin-tn-1.json) | — | haiku |
| yayin-tn-2 | yayin | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yayin-tn-2.json) | — | haiku |
| yeniden-gecis-1 | yeniden | BİTTİ kanıtlı (git 6749789f yeniden-gecis-1: video_derin /p/ gonderisi icin tum) | not: yapılmadı; bu yüzden tarama başlatılmadı (kural: değilse DUR). - Tüm hat (1.519 reel + 480 post + 59 | sonnet |
| yeniden-gecis-2 | yeniden | BİTTİ kanıtlı (yeniden-gecis-2.md) | — | sonnet |
| yonetici-api-1 | yonetici | BİTTİ kanıtlı (yonetici-api-1.md) | — | sonnet |
| yonetici-bagimsiz-1b | yonetici | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yonetici-bagimsiz-1b-a.json) | not: yapılmadı, suit kırmızı. - **Suit:** tests 729/736 (6 kırmızı), tools/video 1422/1424 (1 kırmızı), t | sonnet |
| yonetici-bagimsiz-1c | yonetici | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yonetici-bagimsiz-1c-a.json) | — | haiku |
| yonetici-olum-2 | yonetici | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yonetici-olum-2.json) | not: bulunamadı, ama kanıt düzeneği kuruldu (commit `f17c0eee`). Testler 49 geçti (yeni 4 + mevcut 45). G | sonnet |
| yonetici-yenile-1 | yonetici | BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/yonetici-yenile-1-a.json) | — | sonnet |
| yonetici-yenile-2 | yonetici | BİTTİ kanıtlı (yonetici-yenile-2.md) | — | sonnet |
| zip-yukle-24eki | zip | BİTTİ kanıtlı (zip-yukle-24eki.md) | — | haiku |
| zorunlu-arac-1 | zorunlu | BİTTİ kanıtlı (git fb73c79f zorunlu-arac-1: ön uçuş + son denetim) | — | sonnet |
| zorunlu-arac-3 | zorunlu | BİTTİ kanıtlı (git 05c4281e zorunlu-arac-3: kombinler (62) + tur setleri + çeki) | not: Yapılmadı:** yeni commit yok; çalışma ağacındaki diğer değişiklikler bu işe ait değil. araç: pytest, | sonnet |

## Ayrı kuyruklar

- skill-mode-2: BİTTİ kanıtlı (log BİTTİ rc0 + ajan-sira/skill-mode-2.json) · not: yapılmadı; test kümesi ölçümde görüldü, ancak kaçanlar listesi yazılan kodda test sorgularını da kap
- code-mode-rea-2: BİTTİ kanıtlı (code-mode-rea-2.md) · —
- ustalik-1: BİTTİ kanıtlı (git 71400dcb ustalik-1 p1: 100 arac karti + deneme + fikir-karar) · not: bulunamadı. - **Commit:** `71400dcb`. Kartlar `kartlar/arac/` altında, aynıları Obsidian `30-araclar
- stalemap-kur-1: HİÇ GİRMEMİŞ · görev dosyası/kuyruk/rapor yok; stalemap plugin'i kurulu görünüyor (mcp__plugin_stalemap), kayıt eksik · kalan: kuruluysa kapat, değilse görev yaz · model: haiku
- video-repo-2: BİTTİ kanıtlı (video-repo-2.md) · not: BULUNAMADI). Önceki turun raporu yerinde, bu tur eksik adımları tamamladım. Commit `8d24d7c0`. - **y
- claude-mods: KOŞMUŞ-BİTMEMİŞ · repo zycck/claude-mods (MIT, plan-progress eklentisi): gitleaks temiz, skillspector+semgrep dönmedi, kurulum YAPILMADI (rapor/video-repo-3-zycck.md) · kalan: skillspector+semgrep (arka.py) temizse kur · model: ücretsiz/haiku

## Ek kaynak satırları (docs/rapor; ilgili işe eklenemeyenler)

- `docs/yol-haritasi.md` — - 1b-2a DEVAM-1: rapor kalitesi + model karşılaştırması (Sonnet 5.5 / Haiku)
- `docs/yol-haritasi.md` — - 1b-2b ölçü notu (1b-2a DEVAM-2): anlamsal ölçü onaylanmadı. Öğrenim: künye/kareler/tablo ayırıcı satırları eşleşiyor (0.535 "kareler: görsel girdi", 0.564). site_ui: eş
- `docs/yol-haritasi.md` — Paralel projeler (kendi sohbetlerinde): BHS 5 konsept sitesi · TELVE (Blender'ı bekliyor) · Portale (hero görseli bekleniyor).
- `docs/kalan-27eki.md` — ## Ömer (kurulum blokları, CC'de, her biri öncesi /clear)
- `docs/kalan-27eki.md` — - 7 OpenMontage (blok sohbette)
- `docs/kalan-27eki.md` — - 8 deepseek-harness · 9 Harness2 + archify · 10 Roast Room (bloklar sohbette)
- `docs/kalan-27eki.md` — ## Desktop'ın yaptıkları
- `docs/kalan-27eki.md` — - De1u9y2D6Ix: IG reel silinmiş → KAPANDI
- `docs/kalan-27eki.md` — - qs-DetJr2nQ: TKGM parsel + Esri uydu + orbit kare + ffmpeg → skill adayı parsel-video (Obsidian: 2026-10-27-parsel-drone-video.md)
- `docs/kalan-27eki.md` — - Memvid notu (Obsidian: 2026-10-27-memvid.md), LINK-27 öğrenilenler (Obsidian)
- `docs/kalan-27eki.md` — ## Desktop'tan yapılamayan (~/.claude erişimi auto-mode'da reddedildi) → CC blokları
- `docs/kalan-27eki.md` — - HR KAPALI:env (statusline) + headroom MCP stats "HTTP 404" + proxy 1.5 GB RAM
- `docs/kalan-27eki.md` — - MCP tools 883k → mcptoon gateway
- `docs/kalan-27eki.md` — - memvid ↔ claude-mem chroma (0.9 GB) denemesi
- `docs/kalan-27eki.md` — - parsel-video skill'i
- `docs/link27-ek.md` — - [ ] F3 BEKLİYOR (docs/headroom-f3.md): Headroom: MCP "havuz 404" (~/.local/bin/headroom sürümü ≠ desktop 0.39.0) → MCP kopyasını 0.39.0'a yükselt; proxy 1.5 GB RAM → ay
- `docs/link27-ek.md` — - [~] F8 (plan docs/link27-uyarla.md, uygulanmadı) Programatik reels skill (kinetik altyazı + ses, De6cx6MRxbZ) → OpenMontage/Remotion ile reel otomasyon skill'i (UYARLA)
- `docs/link27-ek.md` — - [ ] F12 HF_TOKEN eklendi (Ömer 20:31, kullanıcı ortamı): yeni süreçte görünür olduğunu doğrula (değer yazma), tools/ucretsiz_havuz.py'de HF Inference model satırını aç 
- `docs/link27-ek.md` — - [ ] F12 BEKLİYOR: HF_TOKEN var, router.huggingface.co 402 (kredi yok); ücretsiz havuza HF satırı eklenmedi
- `docs/link27-kalan-kurulum.md` — - [x] A10 (tur 3 koştu, 5.86 KOŞULLU GİT) Roast Room: skills/roast-room + 7 persona ajan (geri-dönülebilirlik, nakit, müşteri, teknik risk, zaman/fırsat, hukuk/KVKK, şeyt
- `docs/link27-kalan-kurulum.md` — - [x] E2 (işçi havuzu yapıldı, self-check 4/4, canlı kuyruk koşulmadı) Ajan_sira / _tur.py ile açılan alt ajanlar da aynı kalıcı oturum kuralı; tek seferlik küçük iş = ha
- `docs/devir-28eki-0600.md` — - Uzun ajanlar köprüden DEĞİL Görev Zamanlayıcı ile: .kos/kopru/arka/<isim>.json → komut aracıyla `python C:/Projeler/omer-skills/tools/arka_ajan.py baslat <isim>` (Ömer 
- `docs/devir-28eki-0600.md` — 1. karar-14 — 14 ÖMER-KARARI işi, geri alınabilirlerin hepsine EVET (Ömer yetkisi). Soru kalırsa .kos/kopru/arka/karar-14-soru.md.
- `docs/devir-28eki-1432.md` — - video-764-1.json hazır (para işi 1/4, tavan $3, orta profil). Boş yer açılınca başlat; sonra token-2-d3 → graphify-ultra-1-d2 → token-8-f2d (sabit tur sınırı yok, az ot
- `docs/devir-28eki-1655.md` — 3. derin-hiz-3 — Ömer 16:35: TOPLU KOŞU YOK (onay gerekir); önce hattı geliştir: hedef saatte ≥300–400 link, az VRAM (≤5 GB), kapı ≥0,98 + araç/link %100. Yollar: altyazı
- `docs/devir-28eki-1655.md` — omer-eli-1 — ek-kur-karar ÖMER-ELİ maddeleri (Ömer 'sen yap' dedi, onaylı). İlk boşalan slotta başlat (5 iş sınırı).
- `.kos/kopru/devir/animasyon-1-devam.md` — Bekleyen: Ömer kararı (rapor/animasyon-1.md "Karar seçenekleri").
- `.kos/kopru/devir/atlas-2-devam.md` — # ATLAS-2 devam (d1 ara, 14 Eki ~19:00)
- `.kos/kopru/devir/blender-2-devam.md` — BLENDER-2 devam notu (d4 son 18:32; wt C:/Projeler/omer-skills-wt/blender2, dal kol/blender2, son 66f1c96)
- `.kos/kopru/devir/blender-2-devam.md` — 5. BİRLEŞTİR: kol/blender2 → main + push (Ömer) → Desktop: python onay/blender_2_uygula.py uygula; claude.ai'ye dist/blender-2 zip'leri.
- `.kos/kopru/devir/blender-5-plan.md` — Alınmayan: deterministik istek ayrıştırıcı (6 sabit görevde aşırı uyum, kör yargıyı yanıltır) · --effort low (−%16 çıktı ölçülmüştü; kalite riski, yalnız Ömer onayıyla) ·
- `.kos/kopru/devir/blender-5-plan.md` — 3. Pilot b5p: g1–g6 × tek5 × 1 (6 claude -p, yargı 0). Kapı: jeton ort ≤2150 ve kontrol 6×1.0; tutmazsa DUR raporu (sonraki kaldıraç Ömer kararı).
- `.kos/kopru/devir/blender-6-devam.md` — Sonraki (yalnız Ömer/Desktop kararıyla): sistem istemini (sistem5 ~1600 kr) ≤800 kr'e kısaltan tek7 pilotu, ya da kapıyı tek5'e göre yeniden tanımla. Harcanan claude -p 1
- `.kos/kopru/devir/blender-7-devam.md` — # BLENDER-7 devir (13 Eki 15:20) — f3 DUR, Desktop kararı bekliyor
- `.kos/kopru/devir/desktop-devir-14eki-gece.md` — # Desktop devri — 14 Eki 23:05 (eski sohbet doldu; Ömer "yeni sohbette devam edelim")
- `.kos/kopru/devir/desktop-devir-14eki-gece.md` — - Oturumlar 45 çağrıda ara kayıt + devir (`.kos/kopru/devir/<iş>-devam.md`) yazıp durur. Sen sonucu oku (`ajan-sira/<ad>.json` "result" alanı: cc-kopru `oku` aralik 1–1),
- `.kos/kopru/devir/desktop-devir-14eki-gece.md` — Güvenlik ayarları (permissions.deny, block-destructive, gitleaks, push-kapi) Ömer onayı olmadan değişmez · kurulu araç/skill/plugin/MCP kaldırılmaz/kapatılmaz · ortam değ
- `.kos/kopru/devir/desktop-devir-14eki-gece.md` — - TELVE-R3b-2 d6 (MCP, pid 48276, 23:00): /dunya/ K0–K3 kareleri R2 hero kalitesine, kalp asimetri, kapılar (60/45 fps, LH 90/90, örtüşme ≤2). Devir: devir/telve-r3b-deva
- `.kos/kopru/devir/desktop-devir-14eki-gece.md` — - video-3-d7 (22708): uzun video araç yakalama hâlâ <0.95. Devir: devir/video-3-devam.md.
- `.kos/kopru/devir/desktop-devir-14eki-gece.md` — - token-4-d2b (31588): Headroom STABLE_BOUNDARY A/B + claude-mem→Gemini çevrimdışı kıyas + RTK kaçakları. Devir: devir/token-4-devam.md.
- `.kos/kopru/devir/desktop-devir-14eki.md` — - Görev dosyaları: .kos/kopru/gorev/*.md; ortak kural DEVAM-KURALI.md (en üstte 3D/VARLIK ve TOKEN kuralları). Yeni görev = kısa dosya + ajan metni dosyaya atıf.
- `.kos/kopru/devir/desktop-devir-14eki.md` — ## Bağlayıcı kurallar (özet; tam liste bellekte ve DEVAM-KURALI'nda)
- `.kos/kopru/devir/desktop-devir-14eki.md` — ## Ömer onayları (bugün)
- `.kos/kopru/devir/desktop-devir-14eki.md` — - TOKEN-2 (gorev/token-2.md; devir/token-2-devam.md): K1b sonucu + ayar · K9 düşünme bütçesi testi (çıktı %32; kalite kapısıyla) · K8 ucuz_alt.py kör karşılaştırma · K3/K
- `.kos/kopru/devir/desktop-devir-15eki-0330.md` — - KAPI ≥%98 (02:07, kalıcı, her iş): "acıma yok, %98/99/100 olana kadar devam"; hata ≤%2, örneklem ≥100, uydurma 0, kart kapsamı %100; eşik düşmez — ücretsiz kol tutturam
- `.kos/kopru/devir/desktop-devir-15eki-0330.md` — Ortak yöntem: `.kos/kopru/gorev/ogren-ortak.md` (KAPI satırı, §2 katman A/B/C, §3 ücretsiz özet + doğruluk, §7 kombin + Desktop kombin, §8 3 bakış + kör denetçi, §10 kapı
- `.kos/kopru/devir/desktop-devir-15eki-0330.md` — Kuyruk (ajan-sira.tsv sonu): ogren-1-d6 (çalışıyor, pid 39136, 02:33'ten beri) · ogren-0b-d4 (çalışıyor, pid 16280, 02:47) · omni-ayir-d2b (ogren-1-d6 .json bitince) · og
- `.kos/kopru/devir/desktop-devir-15eki-0330.md` — 1. Bu dosya + desktop-devir-15eki-gece.md (kurallar) + ogren-devam.md üstü. 2. kontrol.py + ram_ust.py 8. 3. Biten oturumları oku → devirlerin üstüne DESKTOP kararı → dev
- `.kos/kopru/devir/desktop-devir-15eki-gece.md` — - Devir yerleri: `.kos/kopru/devir/<iş>-devam.md`; SİTE-OKULU-2 istisna: repo kökü `devir/site-okulu-2-devam.md`.
- `.kos/kopru/devir/desktop-devir-15eki-gece.md` — Güvenlik ayarları Ömer onayı olmadan değişmez · kurulu araç kaldırılmaz/kapatılmaz · env DEĞERİ yazdırılmaz · Ömer'in commitsiz dosyalarına dokunma (liste: desktop-devir-
- `.kos/kopru/devir/desktop-devir-15eki-gece.md` — ## YENİ ANA PLAN — ÖĞREN PROGRAMI + USTALIK KURALI (Ömer 15 Eki 00:15–00:19) — ÖNCE `.kos/kopru/devir/ogren-devam.md` OKU
- `.kos/kopru/devir/desktop-devir-15eki-gece.md` — Önce indirilen/kurulan HER ŞEY en ince ayrıntısıyla incelenir, kullanımı en üst seviyede öğrenilir; sonra işlere her şeyimizle devam. İlk kategori token tasarrufu; öğrenm
- `.kos/kopru/devir/desktop-devir-15eki-gece.md` — KURAL: ÖĞREN-1 bitene kadar iş oturumlarının DEVAMI kuyruğa eklenmez — bitenlerin kararları yalnız devir dosyalarına yazılır.
- `.kos/kopru/devir/desktop-devir-15eki-gece.md` — BİTTİ, OKUNMADI: site-okulu-2-d5 (00:24) · token-4-d4 (00:25) → oku, DESKTOP kararı yaz, devam KUYRUĞA EKLEME.
- `.kos/kopru/devir/desktop-devir-20eki.md` — # DESKTOP DEVİR — 20 Eki 12:25 (eski sohbet çok uzadı; yeni sohbet buradan devam eder)
- `.kos/kopru/devir/desktop-devir-20eki.md` — - Ömer onayları yapıldı: router_1b_force uygula (SUBAGENT_MODEL_FORCE kalktı), mem_bekci, beyin_1_uygula, yerel-uygulamalar repo gizli.
- `.kos/kopru/devir/desktop-devir-20eki.md` — - 14:40 (yeni sohbet): RAM %94-98 — ollama llama-server qwen3.5:4b 64k ctx ~7 GB; OmniRoute üzerinden sürekli /v1/chat/completions (claude-mem mem-yedek ollama halkası ve
- `.kos/kopru/devir/desktop-devir-20eki.md` — - 14:40 Ömer "sen yapsana" → `ollama_kapat.py` (taskkill ollama app/ollama/llama-server) → RAM %96→%69. Başladı: beyin-3-d2 · bulut-1 · ogren-6-kapanis (+ video-764-1). 1
- `.kos/kopru/devir/desktop-devir-20eki.md` — - 15:11 kontrol (RAM %75; rea-kur HÂLÂ ÇALIŞIYOR, pid 42748): ÖĞREN-6 BİTTİ (7ee2963a; t67 95/96 · t68 94/93; zip dist/ogren6-kapanis) → ÖĞREN G1-G4 HEPSİ BİTTİ (zip'ler 
- `.kos/kopru/devir/desktop-devir-20eki.md` — ## ÖMER 15:15 KARARLARI — yeni sohbetin İLK işleri (sırayla)
- `.kos/kopru/devir/desktop-devir-21eki-aksam.md` — ## Ömer'den bekleyen karar
- `.kos/kopru/devir/desktop-devir-21eki-gece.md` — - OKTAN (Omer-F-Ylmz/oktan-deneme özel): GitHub eşitle → Vercel (takım omer), CSP'den jsDelivr çıkar (kütüphaneler içeri), ZAP+gitleaks+semgrep, 30 sn tanıtım filmi. Verc
- `.kos/kopru/devir/desktop-devir-21eki-gece.md` — ## Ömer'in bugünkü kararları
- `.kos/kopru/devir/desktop-devir-21eki.md` — - TERS-2: d5 kapı ✗; d6 ölçüm 3 yerden bozuktu; d7 (3b7d2435) koşucu düzeltildi + 12 yeni hedef taslağı. Yeniden koşu = ÖMER ONAYI.
- `.kos/kopru/devir/desktop-devir-21eki.md` — ## SABAH LİSTESİ (Ömer kararı / elle)
- `.kos/kopru/devir/desktop-devir-21eki.md` — - Kuyruk: ordu-1-d8, telve-rework-d9. Köprü çağrı sayacı ~44/45 — sonraki Desktop oturumu bu nottan devam etsin.
- `.kos/kopru/devir/desktop-devir-22eki-1308.md` — # DESKTOP DEVİR — 22 Eki 13:08 (yeni sohbet buradan devam eder)
- `.kos/kopru/devir/desktop-devir-22eki-1308.md` — Bekleyen: saglik-1 (acil, Haiku) → bhs5-d2 (Short viB1dAHhUVw'den GERÇEK anons + BHS4 saha logosu→3D top→roma "V", ≤$3) → bhs5-d3 (tüm site anti-slop + interaktif + BHS1-
- `.kos/kopru/devir/desktop-devir-22eki-1308.md` — - BHS5 d2 videosu → Ömer onayı → d3.
- `.kos/kopru/devir/desktop-devir-22eki-1405.md` — Sıra: havuz-genis-1b → neffex-klon-6 (≤$2) · telve-v2-faz1d (≤$2) → bhs5-d3 (Ömer onayı) → ajan-akis-2 → ders-dongu-1 → arac-kapi-1 → denklik-1 → her-adim-1.
- `.kos/kopru/devir/desktop-devir-22eki-1405.md` — Bekleyen Ömer: bhs5-d2 onayı; zipler (opus-akis.zip, fable-dusunme 1.1) hazır olunca yolla.
- `.kos/kopru/devir/desktop-devir-22eki-1952.md` — - Kuyruk: telve-hazir-2 · dans-1 · ogren-oto-1 · arac-kapi-1b-devam · autoharness-kur-devam · denklik-1-devam · neffex-klon-7-devam ·
- `.kos/kopru/devir/desktop-devir-22eki-1952.md` — video-yeniden-1-devam · ogren-6-d2-devam · omer-site-ref-1-devam · cuda-kur-3-devam · kurulum-reel-e2-devam.
- `.kos/kopru/devir/desktop-devir-22eki-1952.md` — - Bugünkü 63 satır = 41 tam bitti · 6 bitti ama Ömer reddetti/iptal (bhs5-d0..d2b, telve-v2-faz1b-b, faz1c) · 6 yerine yenisi koştu · 9 yarım (devamları sırada) · 1 tekra
- `.kos/kopru/devir/desktop-devir-22eki-2112.md` — - Sıra: beyin-kaydet-1 (çalışıyor 21:00) → cuda-kur-3-devam2 → kural-beyin-1 → beyin-dusun-1 (koşul: rapor/kural-beyin-1.md içinde "ders").
- `.kos/kopru/devir/desktop-devir-22eki-2112.md` — - Bugün biten teknik işler: ogren-oto-1, video-aksiyon-1 (tools/video_aksiyon.py), ram-az-1, arac-zorunlu-4b (bdab1c5), arac-kapi-1b-devam,
- `.kos/kopru/devir/desktop-devir-22eki-2112.md` — autoharness-kur-devam, omer-site-ref-1-devam, cuda-kur-3-devam (yalnız OCR GPU, ~26x), telve-hazir-2 (Desktop\TELVE\v3), dans-1 (Desktop\dans\dans-5sn.mp4).
- `.kos/kopru/devir/desktop-devir-22eki-2112.md` — - DUR: neffex-klon-7-devam (klon klasörü yok → Ömer klon-5 yolu/AT URL verecek). Bekleyen proje işleri: BHS5 videoyu siteye bağla (intro-bhs.mp4 hazır), TELVE cezve bakır
- `.kos/kopru/devir/desktop-devir-22eki-ogle.md` — # DESKTOP DEVİR — 22 Eki 11:48 (yeni sohbet buradan devam eder)
- `.kos/kopru/devir/desktop-devir-22eki-ogle.md` — ## Bekleyen Ömer kararları / sıradaki
- `.kos/kopru/devir/desktop-devir-22eki-ogle.md` — - İleride: freelance site (B+C), fotoğraf uygulaması, Mai modu (kıyafet/bodysuit seçimi bekliyor).
- `.kos/kopru/devir/desktop-devir-23eki-0200.md` — - Video hattı: hız ≈75 → ≈535 video/saat (bd751cec), yt-dlp YouTube format düzeltmesi (b9f49ce6), GPU ≈%96 (d4b7fdff). Toplu iş BİTTİ: kalan 24 link Instagram giriş/çerez
- `.kos/kopru/devir/desktop-devir-23eki-0200.md` — - cuda-kur-3-devam5 (sonnet medium, pid 42964, 00:50'de başladı): WER altın referansı (Groq+Gemini+NIM çoğunluk oyu) → ≤%2 (şu an %2,75, tek-ASR referansıyla ölçüldü). 02
- `.kos/kopru/devir/desktop-devir-23eki-0200.md` — - Önceki devirden kalan: neffex-klon-7-devam DUR (klon yolu Ömer'de) · BHS5 video bağlama · TELVE cezve bakırı · cublasLt kalıcı PATH kararı · sonra-muzik-kanali.
- `.kos/kopru/devir/desktop-devir-23eki-0345.md` — - cuda-kur-3-devam5/6: altın referans (Groq+Gemini+Voxtral) + leave-one-out → yerel large-v3 %7,2 · Groq %8,8 · Gemini %9,1 (1962cbb, ba48778e). İnsan referansı olmadan ≤
- `.kos/kopru/devir/desktop-devir-23eki-0345.md` — - Ömer kararları (03:40):
- `.kos/kopru/devir/desktop-devir-23eki-0345.md` — 1. WER: "ekrandaki yazılar + STT skill'imiz" → cuda-kur-3-devam7 KUYRUKTA (sonnet high): kurulu STT skill envanteri, ekran altyazısı = insan referansı, ASR'yi ekran yazıs
- `.kos/kopru/devir/desktop-devir-23eki-0345.md` — - Önceki devirden: neffex-klon-7-devam DUR (klon yolu/AT URL Ömer'de) · BHS5 video bağlama · TELVE cezve bakırı · sonra-muzik-kanali.
- `.kos/kopru/devir/desktop-devir-23eki-0630.md` — ## Sıra (Ömer'in kararı)
- `.kos/kopru/devir/desktop-devir-23eki-0955.md` — 4. Bekleyenler (Ömer kararı): NIKKE (Ömer söyleyene kadar yok) · borsa botu (Laya karar katmanı, sanal ortam sürekli; Claude emir girmez/anahtar yazmaz) · shorts kanalı ·
- `.kos/kopru/devir/desktop-devir-23eki-1021.md` — ## Ömer kararı bekleyen
- `.kos/kopru/devir/desktop-devir-23eki-1625.md` — - .claude/kaynak_tam_llm.log ← tools/kaynak_tam.py llm --is 16 (600/700'den devam, önbellekli)
- `.kos/kopru/devir/desktop-devir-23eki-1625.md` — ogrenme-2c (ÇALIŞIYOR pid 42912; öğrenme döngüsü 4 kanıt) → zorunlu-kullanim-1 (boş haiku devam turları) → kurtar-fix-1 → kaynak-site-3 → kurulum-dalgasi-2b (_kur2.log BI
- `.kos/kopru/devir/desktop-devir-23eki-1625.md` — ## Bekleyen Ömer kararları
- `.kos/kopru/devir/devir-2026-10-24-0115.md` — KURALLAR: 31 (öğrenme döngüsü) + 32 (her şeyimiz) önce. Dosya silmek yok. Anahtar yazılmaz. Yerel Ollama yok. RAM <%89, C: ≥80 GB. Push/güvenlik ayarı Ömer onayıyla. Tara
- `.kos/kopru/devir/devir-2026-10-24-0115.md` — omer-skills push onayı · Corretto takibi · usta-blender hakem kotası · Ömer kararları: NEFFEX klon-7, NIKKE, borsa botu, shorts, YouTube trend, inFAMOUS, BHS5 video, TELV
- `.kos/kopru/devir/devir-2026-10-24-1555.md` — ★ 16:04 ÖMER KARARLARI (yeni chat): Docker Desktop KUR (docker-kur-1, .wslconfig memory=3GB, STRIX bitince wsl --shutdown) · A–H grupları + arac-ajan-ozellik-1 hepsi bite
- `.kos/kopru/devir/devir-2026-10-24-1555.md` — ★ 17:31 Ömer: omer-makara GitHub reposunu Desktop/ajan açıp push edebilir (özel repo, "sen hallet") — yalnız bu repo; diğer push'lar Ömer'de. onay-toplu-1 D maddesinde.
- `.kos/kopru/devir/devir-2026-10-24-1555.md` — KONTROL ZİNCİRİ: yeni chat'te send_later ile 20 dk tur kur (eski zincirin son tetiği 15:48'de çalıştı, yenisi KURULMADI). Tur: ajan-sira.log tail 40 · RAM · biten adlar →
- `.kos/kopru/devir/devir-2026-10-24-1555.md` — - yarim-a2-devam KABUL kısmi: cliproxy (Claude kapalı) · base · agentshield · gitleaks bitti. STRIX KOŞMADI: Docker yok + STRIX_LLM tanımsız → ÖMER kararı gerekiyor (Dock
- `.kos/kopru/devir/devir-2026-10-24-1555.md` — - yarim-b1-devam-a DUR: ders döngüsü tekrar 5/10 (hedef ≤1/10) → yarim-b1-devam-b kuyrukta. Maliyet sorusu cevaplandı: havuz teşhisi + iki tam ölçüm koşusu (toplam ~$2).
- `.kos/kopru/devir/devir-2026-10-24-1555.md` — - DENETİM yanlış arac_eksik (birleştirme/kurulum işine beyin fırtınası/tasarım skill'leri istiyor) + binlog/stage_skill + bin adları → gorev-ajan-tam-yetki-1-devam.md (8)
- `.kos/kopru/devir/devir-2026-10-24-1947.md` — - Yeni kurulumlar kuyrukta: kur-xerj-guard-1 (XERJ arama MCP + agent-usage-guard; guard sınırı 7, headless'ı kilitlememeli), hermes-kur-1 (Hermes Agent, ücretsiz modeller
- `.kos/kopru/devir/devir-2026-10-24-1947.md` — - ÖMER'e iş yükleme yok: raporlardaki "ÖMER:" satırları Desktop kararıyla görev dosyalarına yazılır (onay-toplu-1 / g6-devam kalıbı). Desktop yeniden başlatma gerekenler 
- `.kos/kopru/devir/devir-2026-10-24-1947.md` — ★ DESKTOP 00:40 (25 Eki): ajan-sira.konsol bayrağı 20:30'da başka bir Desktop oturumunca açılmıştı (Ömer 20:02 kararına aykırı; ~$11 harcandı). 00:08'den beri konsol yolu
- `.kos/kopru/devir/envanter-1-devam.md` — # ENVANTER-1 devam — d5 BİTTİ (KABUL): kol/envanter b70a413, Ömer onayı bekliyor
- `.kos/kopru/devir/envanter-1-devam.md` — Ömer'e: (1) `python onay/skill_secim_1_uygula.py` (wt'de) → CC; (2) 13 zip claude.ai'ye; (3) Instructions'a `· departman-diger (...)` eki (rapor d5); (4) kol/envanter → m
- `.kos/kopru/devir/envanter-2-devam.md` — # ENVANTER-2 devam — BİTTİ (14 Eki d15). Rapor: rapor/envanter-2.md. Sonraki: ENVANTER-5.
- `.kos/kopru/devir/envanter-3-devam.md` — # ENVANTER-3 devam — BİTTİ (d4, 14 Eki)
- `.kos/kopru/devir/envanter-3-devam.md` — AÇIK KARAR: Ömer — onay betiğine `uygula --satirsiz` (skill'ler kurulur, global CLAUDE.md satırı eklenmez) eklensin mi; şu hâliyle `uygula` önerilmez. dist/envanter-3/pla
- `.kos/kopru/devir/envanter-4-devam.md` — KALAN: yok. Canlı kurulum Ömer onayıyla: `python onay/envanter_4_uygula.py` (kurusuz; --kuru temiz geçti). main'e birleştirme BİRLEŞTİR-20'de.
- `.kos/kopru/devir/envanter-5-devam.md` — KALAN: 1. ENGEL: okuyucu yargıç alt ajanları (12 parti × 5 iş) auto-mode sınıflandırıcısına takıldı ("Auto-Mode Bypass"); aşılmadı. Desktop/Ömer kararı: (i) Agent izni ve
- `.kos/kopru/devir/envanter-6-devam.md` — AÇIK KARAR: DEVAM-KURALI (a) her işte katalog kuralını KOŞULLU yapmak + UserPromptSubmit kancası kurulumu — Ömer/Desktop (rapor/envanter-6.md Sonuç d2)
- `.kos/kopru/devir/envanter-kullan-1-devam.md` — # ENVANTER-KULLAN-1 devam (ara kayıt, ~45 çağrı)
- `.kos/kopru/devir/envanter-kullan-1-devam.md` — - Açık: dış çağrı denemeleri (openrouter nemotron :free metin+görsel, ollama gpt-oss:20b-cloud) sınıflandırıcıda reddedildi → Ömer onayı gerek, en fazla 3 çağrı, `.kos/ko
- `.kos/kopru/devir/fable-1-devam.md` — FABLE-1 devir (d6 KAPANIŞ, 20:45). wt C:/Projeler/omer-skills-wt/fable, kol/fable 95139af. Görev BİTTİ; devam oturumu gerekmez.
- `.kos/kopru/devir/fable-1-devam.md` — - Desktop'a kalan: (1) FABLE-AJAN ile tek seçim (aynı metin, çift yükleme olmasın; devir/fable-ajan-devam.md'ye yazıldı); (2) `python onay/fable_1_uygula.py` + claude.ai'
- `.kos/kopru/devir/fable-ajan-devam.md` — # FABLE-AJAN devam (d5 → d6, 13 Eki 01:37)
- `.kos/kopru/devir/fable-ajan-devam.md` — # FABLE-AJAN devam (d4 → d5, 13 Eki 00:25)
- `.kos/kopru/devir/graphify-ram-1-devam.md` — 4. rapor/graphify-ram-1.md (≤12 satır) · DEVAM-KURALI 20:58 satırına "sarmalayıcı: .kos/kopru/graphify_hafif.py" ekle ·
- `.kos/kopru/devir/graphify-ultra-1-devam.md` — d2 28 Eki: BİTTİ, kalan yalnız Ömer onay betiği + zip yükleme.
- `.kos/kopru/devir/headroom-1-devam.md` — BİTTİ (DUR): kırıcı değişiklik v0.40.0 + proxy masaüstü-yönetimli; ayrıntı rapor/headroom-1.md. Sonraki iş Ömer kararına bağlı (HEADROOM-1b: uv aracı 0.39.1 sabitleme bet
- `.kos/kopru/devir/ig-18-kur-devam.md` — IG-18-KUR devam notu — BİTTİ (d3, 12 Eki 18:40). Rapor: .kos/kopru/rapor/ig-18-kur.md. wt igkur18 kol/igkur18 commit 595bdba.
- `.kos/kopru/devir/ig-18-kur-devam.md` — Kalan yalnız Desktop/Ömer: onay/ig_18_kur_uygula.py --kuru → uygula · dist/ig-18/kendi zip claude.ai Replace · main'e birleştirme + marketplace update.
- `.kos/kopru/devir/ig-40-kur-devam.md` — # IG-40-KUR devam notu (d5 sonu, 12 Eki 18:08) — sira 1–40 parçası BİTTİ
- `.kos/kopru/devir/ig-40-kur-devam.md` — Açık kalan (devam oturumu gerekmez, Desktop/Ömer işi):
- `.kos/kopru/devir/ig-40-kur-p2-devam.md` — # IG-40-KUR P2 devam notu — BİTTİ (12 Eki 17:36)
- `.kos/kopru/devir/ig-40-kur-p2-devam.md` — Kalan yalnız Desktop/Ömer: `python onay/ig_40_kur_p2_uygula.py --kuru` → `uygula` (wt igkur-p2'den) · dist/ig-40-p2/kendi 3 zip claude.ai'ye Replace · kol/igkur-p2 → main
- `.kos/kopru/devir/ig-40-kur-p3-devam.md` — # IG-40-KUR P3 devam notu — BİTTİ (12 Eki 17:56)
- `.kos/kopru/devir/ig-40-kur-p3-devam.md` — Bekleyen (Desktop/Ömer): onay `uygula` · claude.ai zip yüklemesi · İNCELE 3 trailofbits plugin kararı · uyarla.md metin değişiklikleri ayrı dalga.
- `.kos/kopru/devir/ig-41-kur-devam.md` — # IG-41-KUR devam — BİTTİ (d4, 13 Eki)
- `.kos/kopru/devir/ig-41-kur-devam.md` — Ömer'e kalan: onay `python onay/ig_41_kur_uygula.py uygula` (canlı) · Desktop dist/ig-41-kur/LISTE.md 7 zip · 15 hesaplı KUR elle · tam envanter yenilemesi için tavan kar
- `.kos/kopru/devir/ig-41a-devam.md` — # IG-41A devam — BİTTİ (d2, 13 Eki 08:20)
- `.kos/kopru/devir/ig-41b-devam.md` — # IG-41B devam — BİTTİ (d1). Kalan yalnız: (1) DbLogAztbFN, DeZbmooNrmp Desktop Chrome okuması → b-08 (ig41b-yonerge.md ile) + `python .kos/kopru/ig41b_birlestir.py`; (2)
- `.kos/kopru/devir/ig-41c-devam.md` — # IG-41C devam — BİTTİ (06:08)
- `.kos/kopru/devir/ig-41d-devam.md` — # IG-41D devam
- `.kos/kopru/devir/jev-2-devam.md` — JEV-2 devam — BİTTİ (d5, 13 Eki 00:45). kol/jev2 son commit için `git -C C:/Projeler/omer-skills-wt/jev2 log -1`.
- `.kos/kopru/devir/kalite-2-devam.md` — KALİTE-2 devam — d3 BİTTİ (19:20). Rapor: rapor/kalite-2.md · wt C:/Projeler/omer-skills-wt/kalite2, kol/kalite2 331ffe4 (push yok).
- `.kos/kopru/devir/kalite-2-devam.md` — Bekleyen (Ömer/Desktop): onay/kalite_2_uygula.py --kuru → uygula (+ --guvenlik: block-destructive güvenlik hook'unu geri açar).
- `.kos/kopru/devir/kalite-3-d14-devam.md` — # KALİTE-3-d14 devam (d3 bitti 18:22 → d4)
- `.kos/kopru/devir/kalite-3-d14-devam.md` — - Godmode içeriği FABLE-1-d4 KABUL'üne bağlı; arayüz devir/ruflo-1-devam.md. d15 kuyruğu devir/kalite-3-hiz.md.
- `.kos/kopru/devir/kalite-3-d15-devam.md` — # KALİTE-3-devam-15 devam notu (d15, 12 Eki 19:52)
- `.kos/kopru/devir/kalite-3-d16-devam.md` — # KALİTE-3-D16 devam notu (d3, 13 Eki 03:05)
- `.kos/kopru/devir/kalite-3-d16-devam.md` — Kalan iş yalnız ölçüm: devir/kalite-3-hiz-devam.md'yi izle (koşucu kalite3c, günlük .kos/kopru/kalite3-hiz.log).
- `.kos/kopru/devir/kalite-3-d17-devam.md` — # KALİTE-3-D17 devam notu (d1 sonu, 13 Eki 06:20)
- `.kos/kopru/devir/kalite-3-hiz-devam.md` — # KALİTE-3-HIZ devam notu (D16 d3, 13 Eki 03:05)
- `.kos/kopru/devir/kalite-3-hiz-devam.md` — 2. Koşucu öldüyse: API ortamlı oturumdan `python .kos/kopru/arka.py --cwd C:/Projeler/omer-skills-wt/kalite3c .kos/kopru/kalite3-hiz.log tools/kalite3_hiz.py kos` (devam(
- `.kos/kopru/devir/kalite-3-hiz-devam.md` — BEKLE: .kos/kopru/kalite3-hiz.log `BİTTİ` (ya da çağrı ≥2550 / 07:00) olunca → adım 4. RAM %93'te olduğundan d3 oturumu bekleme yapmadan çıktı (DEVAM-KURALI 01:45).
- `.kos/kopru/devir/kalite-3-hiz.md` — # KALİTE-3-HIZ → KALİTE-3-devam-14 devir notu (12 Eki)
- `.kos/kopru/devir/kapi-25-devam.md` — # KAPI-25 devam — BİTTİ (13 Eki 16:56, kol/kapi25 622651b)
- `.kos/kopru/devir/kaynak-5-devam.md` — KAYNAK-5 devam (d1, 13 Eki ~05:00)
- `.kos/kopru/devir/kaynak-5-devam.md` — BİTTİ (13 Eki 05:50). Kalan yalnız Desktop/BİRLEŞTİR: kol/kaynak5 → main, sonra 'python onay/kaynak_5_uygula.py uygula' + dist/kaynak-5/kendi zip claude.ai Replace + 'cla
- `.kos/kopru/devir/mcp-hafif-1-devam.md` — MCP-HAFIF-1 devam (d3 17:40 yazıldı) — wt C:/Projeler/omer-skills-wt/mcphafif, dal kol/mcphafif (b9e8606)
- `.kos/kopru/devir/mcp-hafif-1-devam.md` — 4. YAZILDI (17:58): devir/kalite-3-hiz.md, animasyon-1-devam.md, fable-1-devam.md sonuna MCP-HAFIF bölümü.
- `.kos/kopru/devir/mcp-hafif-2-devam.md` — Onay (Desktop/Ömer, wt'de): onay/mcp_hafif_2_bekci.py uygula · onay/mcp_hafif_2_serena.py uygula · onay/mcp_hafif_2_paylas.py --kuru (auth0 init sonrası).
- `.kos/kopru/devir/ogren-1-devam.md` — DESKTOP 02:10 — KAPI YÜKSELDİ (Ömer 02:07: "acıma yok, %98/99/100 olana kadar devam; her şeyi en üst rütbede ustalıkla kullan, düşün, birleştir, kombinle"): özet hattı ka
- `.kos/kopru/devir/ogren-1-devam.md` — - d14 yarım işi sağlamdı (d14.py kaynak çözümü + test, denetim, tohum 11 örneklem, paket, yazar 1/3) → üstüne devam: yazar-2 (sonnet) → `d14.py birlestir` son 18 · RET 0 
- `.kos/kopru/devir/ogren-1-devam.md` — - MODEL: settings.json env CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 tanımlı → Agent model alanını ezebilir (yalnız rapor; değişiklik Ömer onayıyla). Tüm ajanlar model=sonnet is
- `.kos/kopru/devir/ogren-1-devam.md` — - 2. devam boşa: d9-kalan.txt CRLF → adlarda \r → 21 KeyError (image-compression yalnız o koştu: 3 kolda RET). \r silinip kalan 21 yeniden başlatıldı (arka plan, aynı log
- `.kos/kopru/devir/ogren-1-devam.md` — # ÖĞREN-1 devam (d2 → d3) — 15 Eki ~01:25
- `.kos/kopru/devir/ogren-devam.md` — DESKTOP 02:24 — Ömer 02:20 KARARI (cc-yedek-dis): "ikiye ayır" + daha gelişmiş sürüm → gorev/omni-ayir.md (ÖĞREN-1 token alt hattı; kuyrukta omni-ayir-d1, ogren-1-d5 biti
- `.kos/kopru/devir/ogren-devam.md` — DESKTOP 02:10 — KAPI KURALI (Ömer 02:07, kalıcı, ÖĞREN ve sonrası bütün işler): "acıma yok — %98/99/100 olana kadar devam; bundan sonra her şeyi en üst rütbede ustalıkla 
- `.kos/kopru/devir/ogren-devam.md` — YAPI: ortak yöntem gorev/ogren-ortak.md (katman A/B/C · ücretsiz özet + doğruluk · gerçek koşu · ustalık kartı · çakışma matrisi · kombin içi ≥5 arası ≥3 · 3 bakışlı ajan
- `.kos/kopru/devir/ogren-devam.md` — ÖĞREN-1 devamı (dN) için: katalog-son.jsonl'da ÖĞREN-0b'nin token'a taşıdığı ek kalemler de kapsama girer. ajan_sira.py ARGV'yi import anında kurar (runner PID 45564 A6'd
- `.kos/kopru/devir/ogren-devam.md` — DESKTOP 00:38: envanter-kullan-1 BİTTİ (docs/kullan-haritasi.md + envanter-oneri.md; öneriler video-3 · video-kisa-token-2 · site-okulu-2 · telve-r3b · token-4 devirlerin
- `.kos/kopru/devir/ogren-devam.md` — DESKTOP 00:18 — ÖĞREN PROGRAMI (Ömer 15 Eki 00:15): önce indirdiğimiz/kurduğumuz HER ŞEY en ince ayrıntısıyla incelenir, anlaşılır, kullanımı en üst seviyede öğrenilir; s
- `.kos/kopru/devir/omni-ayir-devam.md` — DESKTOP 02:48 — d2 ÖNCE BU: d1 KABUL (yedek + cc-ucuz-free + ucuz_alt v2 + iki kat ücretli kilidi + kesik yanıt kök nedeni + 9 test). Sıra: (1) GERİ ALMA betiyi ÖNCE (ona
- `.kos/kopru/devir/omniroute-1-devam.md` — OMNIROUTE-2 pilot BİTTİ: IG özet cc-yedek-dis 8.89 ≥ Claude 8.33, başarı 20/20 ≥ 19/20 → taşınabilir, ama combo ücretli (OpenRouter). Sonraki: Ömer Gemini/Groq bağlar → ü
- `.kos/kopru/devir/omniroute-2-devam.md` — OMNIROUTE-2 devam — d6 BİTTİ (13 Eki)
- `.kos/kopru/devir/plan-kur-3-devam.md` — # PLAN-KUR-3 devam (d4 ara kayıt, 14 Eki ~09:05)
- `.kos/kopru/devir/plan-kur-3-devam.md` — KAPANDI 14 Eki 09:25 (d5): ölçüm + kapı → KABUL; rapor/plan-kur-3.md "Sonuç (d4)". Açık: envanter_3_uygula.py uygula (Ömer onayı).
- `.kos/kopru/devir/plan-kur-4-devam.md` — 4. KABUL → skills/plan-kur/plan_kur.py = tools/plan_kur.py, dist/claude-ai-22/plan-kur.zip (main zip_denetle), onay/envanter_3_uygula.py --kuru (uygula Ömer onayıyla). RE
- `.kos/kopru/devir/plan-kur-5-devam.md` — KALAN: yok (dist/claude-ai-22 kapı gevşetilirse .claude/b22/yap.py ile üretilir — Ömer kararı).
- `.kos/kopru/devir/router-1-devam.md` — ROUTER-1 devam notu (d3, 12 Eki 18:38 başladı; kilit gorev/router-1-d3.kilit)
- `.kos/kopru/devir/ruflo-1-devam.md` — # RUFLO-1 devam (d2 → d3) — 12 Eki 12:55
- `.kos/kopru/devir/ruflo-1-devam.md` — - A/B 19:04'te DÜŞTÜ: kosucu.supur Get-CimInstance 60 sn zaman aşımı (cihaz donması) → TimeoutExpired. Düzeltme kol/ruflo 9de157c (supur yutar + test) + ab_olc `--devam B
- `.kos/kopru/devir/ruflo-1-devam.md` — - Yapıldı (kol/ruflo): 9de157c supur düzeltmesi + ab_olc --devam · e056811 cherry-pick (godmode_onsoz.py, kalite3b ile birebir → birleştirmede çatışmasız) · 39eae22 onsoz
- `.kos/kopru/devir/ruflo-1-devam.md` — - Ölçüm sürüyor (19:47 başladı, rapor5 dersli 1.0 bitti, video 1: 0.5=0.5). d5: (1) günlükte BİTTİ/TAVAN bekle — süreç yoksa ve yoksa nedenini bul, YENİDEN BAŞLATMA yalnı
- `.kos/kopru/devir/ruflo-1-devam.md` — - Ömer (3) FABLE-AJAN etkileşimi: bütçe kalırsa (Σ ≤$12) rapor ailesinde dersli+FABLE protokolü kolu; yoksa fable-ajan-devam.md'ye devir satırı.
- `.kos/kopru/devir/ruflo-1-devam.md` — - 00:58 d7 KAPANDI: kapı YOK (kalite +%24, jeton +%2.7); kod ailesi iki ölçütü geçiyor. Karar Ömer'de (rapor d7 kapanış). Ölçüm bütçesi bitti; yeni ölçüm yok. Ömer onay v
- `.kos/kopru/devir/sabah-22eki.md` — - ÖMER KARARI: 1) TELVE + NEFFEX Vercel (yeni proje) 2) logo-final + oktan-film görmek için klasör izni 3) freelance site yönü A/B/C (`Desktop\omer-site\docs\ref.md`, 8 i
- `.kos/kopru/devir/sabah-22eki.md` — - TELVE kapanis-1 (2bc4c5c) YANLIŞ siteyi (eski Astro) ölçtü → kapanis-2 yeni/ Vite sitesine kuyrukta. Ömer kararı: `public/cezve.m.glb` (kaynağı çelişkili, yeni sitede y
- `.kos/kopru/devir/sabah-22eki.md` — - TELVE KAPANIŞ TAMAM (dcbb556): Lighthouse mobil 97/100/100/100, masaüstü 100×4, axe 0, audit/semgrep 0, robots/sitemap/canonical/og/JSON-LD HowTo, dist 5,89 MB. → Verce
- `.kos/kopru/devir/sabah-22eki.md` — - NEFFEX KAPANIŞ TAMAM (1d5c681): reduced-motion liste (10 şarkı, canvas yok), kapanış kilidi NEFFEX × b1 eşit 34 px, uyarı ≥12 px, og.jpg, axe 0, a11y/SEO 100, gerçek GP
- `.kos/kopru/devir/sabah-22eki.md` — ## Ömer kararı bekleyen
- `.kos/kopru/devir/site-okulu-1-devam.md` — # SİTE-OKULU-1 devam (14 Eki, çağrı tavanı 45'te ara kayıt) — KAPANDI 19:55 @ 3c2d91d6 (1–3 bitti; 4 TELVE-R3 işi)
- `.kos/kopru/devir/tasarim-2-devam.md` — # TASARIM-2 devam — BİTTİ (d5, 02:00)
- `.kos/kopru/devir/tasarim-2-devam.md` — Kabul tuttu (rapor/tasarim-2.md "Son rapor"). Kalan yalnız Desktop: onay/tasarim_2_uygula.py uygula + dist/tasarim-2/frontend-craft.zip claude.ai yüklemesi; kol/tasarim2 
- `.kos/kopru/devir/tasarim-3-devam.md` — # TASARIM-3 devam (d3 sonu)
- `.kos/kopru/devir/tasarim-3-devam.md` — BİTTİ: (b) cafa95a teslim, (a) KABUL f31b1f3 frontend-craft 1.9.0. Kalan yalnız Ömer: onay/tasarim_3a_uygula.py uygula + dist/tasarim-3a/frontend-craft.zip Desktop yüklem
- `.kos/kopru/devir/telve-hazir-1-devam.md` — AÇIK KARAR: Ömer — (a) comfy_cafe HDR sıcak sahnelere mi (docs/yon/hazir-hdr-comfy_cafe.png) (b) Pixabay/Sonniss ses lisansı (öneri: kullanma, freesound CC0 yeter) (c) Sk
- `.kos/kopru/devir/telve-r1-devam.md` — # telve-r1 devir (R1 d1, 14 Eki) — BİTTİ (Ömer onayı bekliyor)
- `.kos/kopru/devir/telve-r1-devam.md` — AÇIK KARAR: comfy_cafe HDR · cezve avlasova11 CC-BY · ses yalnız freesound CC0 — varsayılanla işaretli; Fraunces frontend-craft refleks listesinde (Ömer kararı olarak bır
- `.kos/kopru/devir/telve-r2f-devam.md` — AÇIK KARAR: alan adı — astro.config.mjs `site` (varsayılan https://telve.vercel.app), Ömer onaylasın; tek satır.
- `.kos/kopru/devir/telve-r3b-devam.md` — DESKTOP 00:38 (d2 sonu + d3 için; envanter-kullan-1): görsel yargıya yerel kör kol ekle `pixeljury review <url> --provider ollama --model qwen3.5:4b --json` (kota yok; cl
- `.kos/kopru/devir/telve-token-1-devam.md` — # telve-token-1 devam (d4 → d5) — BEKLE
- `.kos/kopru/devir/telve-token-1-devam.md` — AÇIK KARAR: Ömer/Desktop — (1) d4 KAZA: `git worktree remove --force` junction'ları izleyip TELVE/node_modules, docs/r1/_ham/node_modules, docs/r1/_ham/yon/hdr içini sild
- `.kos/kopru/devir/ters-2-d3-taslak.md` — d3 adımları: (1) hakem tavanını artırmadan önce Ömer'e/DUR: tavan 70 → karar gerek (öneri: hata dönen çağrıyı sayma, yalnız başarılıyı say; tavan aynı kalır). (2) RAM <%8
- `.kos/kopru/devir/token-3-devam.md` — # TOKEN-3 devam (d8 → BİTTİ, onay bekliyor) — 14 Eki ~23:30
- `.kos/kopru/devir/token-4-devam.md` — DESKTOP 00:38 — ÖNCE BU: d4 KABUL (A6 sabit bağlam 53.6k → `--tools` 33.5k, −%37.6). `--kuru` planı doğru ("eklenecek") ama cp1254 konsolda `→` karakterinde UnicodeEncode
- `.kos/kopru/devir/token-4-devam.md` — # TOKEN-4 devam (d4 → d5) — 15 Eki ~00:25
- `.kos/kopru/devir/token-4-devam.md` — ÖMER ONAYI: `python onay/token_4_uygula.py --kuru` → uygula (ajan profiline araclar; yalnız köprü oturumları; --geri var).
- `.kos/kopru/devir/token-8-f2a-devam.md` — # TOKEN-8 f2a devam — d2 BİTTİ (13 Eki 16:05): iş 1 RET+revert, iş 3 RET; ayrıntı rapor/token-8-f2a.md "d2 sonuç". Sonraki aday: iş 3 Türkçe istem + yalnız bayrak (4 çağr
- `.kos/kopru/devir/token-8-f2b-devam.md` — # TOKEN-8 f2b devam — BİTTİ (13 Eki 16:32)
- `.kos/kopru/devir/token-8-f2c-devam.md` — # TOKEN-8 f2c devam
- `.kos/kopru/devir/token-8-f2c-devam.md` — BİTTİ (d3). Bekleyen yalnız Desktop/Ömer onayı: iş 2 ve iş 4 uygula (rapor/token-8-f2c.md Son rapor) + kol/token8 → main birleştirme.
- `.kos/kopru/devir/token-8-f2d-devam.md` — # TOKEN-8 f2d devam (13 Eki d2, BİTTİ — iş 4 RET)
- `.kos/kopru/devir/video-3-devam.md` — # VİDEO-3 devam (d9 → d10), 15 Eki ~00:00
- `.kos/kopru/devir/video-764-4-devam2.md` — - Kod: video764_karar2.py → `kapi` (held-out 30 tek-tek + toplu15 ×2; sonuç satırı "uyum a /30 ikinci b tutarlılık c /30"), `ver --verici sonnet --toplu N` (karar-v2'siz 
- `.kos/kopru/devir/video-kisa-token-1-devam.md` — - Bitince: rapor + M5 (SKILL.md + zip_denetle) + SIRA "VİDEO-KISA-TOKEN-1 BİTTİ" (dosya: .kos/kopru/gorev/SIRA.md — kuyruk bu satırı orada bekliyor; kapı geçmeden BİTTİ y
- `.kos/kopru/devir/video-kisa-token-1-devam.md` — DESKTOP 14 Eki 16:45 — ÖNCE BUNU OKU: (a) Madde 1'in kod düzeltmesi YAPILDI (Desktop, kisa.py commitsiz): MODELLER 3.8-flash önce, IZLE_ZAMAN=90, izle() TimeoutError/URLE
- `rapor/ajan-tam-yetki-1.md` — - DEVAM (b): (5) github=http MCP+gh, vercel CLI var; supabase/miro yok → ERİŞİM YOK. (6) zorunlu_arac.erisim_yok: PATH'te olmayan düz cli dolgu+yok işaretlenir, blokta "E
- `rapor/ajan-tam-yetki-1.md` — - ÖMER: canva ve claude-design OAuth girişi gerekli (claude-design 403: /design-login). Yönetici runner'ı slash bayrağı için yenilenmeli.
- `rapor/arac-ajan-ozellik-1.md` — - ÖMER: claude.ai tarafı için dist zip yeniden üretimi/yüklemesi (envanter + üretici betik zip içine), henüz yapılmadı.
- `rapor/beyin-arac-kart-1.md` — - DEVAM (BEYIN-ARAC-KART-1-2): Hermes'ten canlı çağrı ✓, `hermes mcp add arac-ara` (araclar/hermes-home/config.yaml, 2 araç), `hermes chat` nemotron:free ile arac_ara çağ
- `rapor/beyin-arac-kart-1.md` — - DEVAM-2 (suit): tools/tests 382/382 (kök neden: yetenek kopyası bayat → katalog_yenile; test_geri_cagirma beklentisinden stale `sec-sir-tarayici`/ajan adı çıkarıldı, 48
- `rapor/claude-p-asilma-1.md` — ÖMER: `enabledPlugins` (410 etkin) kullanıcı ayarı; kapatma listesine onay ver, ya da köprü profiline `pluginKapat` eklememi iste.
- `rapor/derin-tamamla-1-a2.md` — DERIN-TAMAMLA-1-a2 (yarim-tara-27eki: DUR, 2 devam turu sonrasi hala eksik)
- `rapor/docker-kur-1.md` — - ÖMER: yönetici PowerShell'de: `wsl --install --no-distribution` → makineyi yeniden başlat → `winget install Docker.DockerDesktop` → bana "docker-kur-1 devam" de.
- `rapor/kur-xerj-guard-1.md` — ## DEVAM-B-RD (25 Eki), KISMI
- `rapor/olum-teshis-1-a2.md` — OLUM-TESHIS-1-a2 (yarim-tara-27eki: DUR, gorsel_hakem eksik; kok neden kanitlanmadi)
- `rapor/onay-toplu-1.md` — 6-11: YAPILMADI (bütçe/tur; ayrı tur): jev-2 kart süzgeci, beyin-2/3/4 kabul turu, kalite-1 ücretsiz yeniden ölçüm (BEKLİYOR: Console geçişi), mcp-ac-2 A/B, autoharness k
- `rapor/onay-toplu-1.md` — ## Devam (oturum 3, ONAY-TOPLU-1-DEVAM)
- `rapor/ram-bekci-3c.md` — 1. Yeni kod kanıtı: yönetici (pythonw pid 5024, 18:16:23) ve video_derin (pid 54584/73248, 18:00:21), ac48f012'nin (15:26) ardından başladı → ajan_ram_bekci'yi yeni kodla
- `rapor/suit-kirmizi-2.md` — - YAPILMADI: madde 2, etiket_uret.py repoda yok; katalog şemasında 'etiket' alanı yok (kapsam belirsiz, DUR). Madde 3 kanıtı (3 ardışık tam suit): koşucu .kos/kopru/suit3
- `rapor/takip-24eki-a-devam.md` — - #3 VIDEO-REPO-3: repo zycck/claude-mods (OCR kare 0005 + transkript 168 sn); gitleaks temiz; skillspector/semgrep dönmedi → kurulum DEVAM (rapor/video-repo-3-zycck.md; 
- `rapor/takip-24eki-a.md` — - #1 CLAUDE-P-ASILMA: DEVAM→ÖMER (kök neden=410 eklenti toplam yük, 190sn; rapor/claude-p-asilma-1.md)
- `rapor/takip-24eki-a.md` — - #3 VIDEO-REPO-3: DEVAM (tur sınırı; yt-dlp/video_derin/OCR başlanmadı)
- `rapor/takip-24eki-a.md` — - #4 OMER-SITE-D1C: DEVAM (tur sınırı; gorsel_hakem 3x, hero100 mühür, vite pid kapatma başlanmadı)
- `rapor/tamamla-28.md` — ÖMER: claude.ai'de bu 12'yi Replace ile yükle (yukle-28eki'dekileri geçersiz say).
- `rapor/ucretsiz-motor-2-devam.md` — # UCRETSIZ-MOTOR-2-DEVAM, rapor
- `rapor/ustalik-1-kapi.md` — ## Muaf (ÖMER:)
- `rapor/yarim-a3.md` — - autoharness-fix-1: BİTTİ (kanıt yeni) — hook komutu `python3 -c ... CLAUDE_PLUGIN_ROOT` biçiminde; bu oturumda `~/.claude/autoharness/requests` mtime 12:34 → 13:14:54 d
- `rapor/yarim-a3.md` — - "Kullanılamayan 4 araç": görev 4'ü saymıyor; zorunlu set için ölçüldü: markitdown, summarize, semgrep, gitleaks CLI `--help` OK; departman-belge kurulu; headroom-compre
- `rapor/yarim-a3.md` — ÖMER: `python onay/katalog_kanca_uygula.py uygula` (settings.json değişir, yedek alır).
- `rapor/yarim-b1-devam-b.md` — YARIM-B1-DEVAM-B: DUR, dersli tekrar kabul (≤1/10) tutmadı; en iyi 2/10 kaçan (dersli 8/10 uygulandı), gevşetilmedi.
- `rapor/yarim-b1.md` — - beyin-canli-1 / 1b: BİTTİ (ölçümler) — DEVAM (görev zamanlayıcı tetikleri, aşağıda).
- `rapor/yarim-b1.md` — - ders-dongu-1: BİTTİ (otomatik üretim) — DEVAM (ölçüm). `ders_dongu.dongu()` + derin turda `ders_isle()` (topla→≤10 aday ücretsiz havuz→Obsidian, hata derini durdurmaz).
- `rapor/yarim-b1.md` — ÖMER: yok (giriş/onay gerekmiyor). Görev zamanlayıcı 5 dk'lık canlılık + oturum açılışı + uykudan dönüş tetikleri hâlâ yok (görev "Interactive only"); sistem zamanlayıcıs
- `rapor/yarim-b2.md` — - ogrenme-2 / 2b: DEVAM (`.kos/kopru/gorev-yarim-b2-devam.md`), yansıtma (73730a2), envanter, gösterge, alarm onarımı, sınav aracı VAR; ders etkisi ölçüldü ~0 (sinav3 +0.
- `rapor/yarim-b2.md` — - mem-fix-1 / mem-fix-2: ZATEN BİTMİŞ, mem-fix-4 DUR'daki "gözlem sabit" şimdi çözülü: gözlem 29449 → 33671 (`/api/stats`), son id 33688, worker ok, `omer-claude-mem-bekç
- `rapor/yarim-b2.md` — - egitim-1: DEVAM (`gorev-yarim-b2-devam.md`), kapı geçti ama doymuş (59/60, görevler kolay); LoRA başlatılmadı. Ölçüm: GPU RTX 4070 Ti 2.3/12.3 GB dolu, RAM 3.3 GB boş /
- `rapor/yarim-c1.md` — - yonetici-olum-2: DEVAM (gorev-yarim-c1-devam.md), kalp/önceki-ölüm düzeneği çalışıyor (yonetici-olum.log); 23.10 15:31–20:11 arası 40 dk periyodik ölüm 22:30'dan sonra 
- `rapor/yarim-c1.md` — - kurtar-fix-1: BİTTİ, SessionEnd `isle` artık `arka.py --bagimsiz` (commit 2dda26a). Diğer arka.py çağrıları (olcum/tasarim betikleri, skills/is-akisi metni) değişmedi: 
- `rapor/yarim-c1.md` — Sapmalar: HawkScan atlandı (uygulama/API anahtarı yok); bütçe hedefi aşıldı (≈$1.5; suit 31 dk, önceki iş sonuçlarını okuma); ÇALIŞAN YÖNETİCİYE dokunulmadı. ÖMER: yok.
- `rapor/yarim-c2.md` — # yarim-c2 (24.10), kısmi: 1 iş bitti, kalanlar DEVAM
- `rapor/yarim-c2.md` — - erisim-tam-1b/1d: DEVAM, kalan: 3 yüzey sınaması, 10/10 uçtan uca, ruflo kapıya alınsın mı. ÖMER: ruflo kapıya alma kararı.
- `rapor/yarim-c2.md` — - ram-1/ram-az-1: KISMEN, paylaşımlı playwright, yeniden başlatma sonrası RAM ölçümü yok. ÖMER: yetim headroom pid 57180 kapatma onayı; Ollama yeniden başlat (setx).
- `rapor/yarim-d1.md` — - derin-tamamla-1: DEVAM. Karusel/post: 126 bekleyen /p gönderisinin 125'i gallery-dl ile TÜM slaytlarla işlendi (derin/<kod>.json, kare_sayisi dolu); 1 kalıcı HTTP 400 (
- `rapor/yarim-d2.md` — - **cuda-kur-2/3 kelime WER <%2: DEVAM / ÖMER.** Ham dosyalardan bu oturumda yeniden hesaplandı (13 klip, 3998 kelime, referans `.kos/kopru/wer-altin/*.altin.txt`, normal
- `rapor/yarim-d2.md` — - ÖMER: 2–3 klibin (~300 kelime) altın metnini kulakla doğrula; ancak bağımsız referansla %2 iddiası doğrulanır ya da çürür.
- `rapor/yarim-d2.md` — ## DEVAM (24 Eki, akşam): kelime WER <%2, ROVER yolu
- `rapor/yarim-d3.md` — - kaynak-tam-1 / 3 / 4: ZATEN BİTMİŞ, e6161033, fff1b781, 78f5c16a, ae13ffe9, c2989dc5, 7cd6786b; kapı kaçırma 0, 247 tarif. ÖMER: kurulum kuyruğu (ilk 10) onayı; #1 gerç
- `rapor/yarim-d3.md` — - kaynak-site-1 / 2: DEVAM (.kos/kopru/gorev-yarim-d3-devam.md), sınıflama hata+diğer %11,5 (hedef ≤%2), kart doğrulama 0/228, semgrep 10/101; ÖMER: skill zip yükleme (cl
- `rapor/yarim-d3.md` — - video-aksiyon-1: BİTTİ (kod), 09c40e06, test 2/2. Karusel (gallery-dl) ve `--toplu` denenmedi → devam dosyası. ÖMER: dist/aksiyon-1/video-uygula.zip'i claude.ai'ye yükl
- `rapor/yarim-e1.md` — - token-rea d20: DEVAM. Mod uygulanmış (CLAUDE_MEM_MODE=code--anahtar, 21.10 19:23; 2149 işaretli omer-skills kaydı, işaret `subtitle` alanında). Kapı `.kos/kopru/token-r
- `rapor/yarim-e1.md` — - ÖMER: dist/claude-ai/yukle-24eki/ (6 zip) + yukle-23eki gruplarını Desktop claude.ai'ye yüklesin; yükleme kanıtı yok.
- `rapor/yarim-e2.md` — - rea-usta-1c: DEVAM (gorev-yarim-e2-devam.md). Bitti: REA çekirdekte, Corretto 21 + Ghidra 12.1.4 `-help`, env, wakaru_kurtar (6,4 sn), rea_bellek. Kalan: REA içinden ge
- `rapor/yarim-e2.md` — - rea-fix-5 (+5b): ZATEN BİTMİŞ (75bfd5cf, 21ca66e6, 57837013); compare_web_captures gerçek iki capture ile `changed` döndü. ÖMER: Desktop'u yeniden aç; oturum araç liste
- `rapor/yarim-e2.md` — DEVAM: (a) excalidraw'da kalan 1 birim (16 KB tek fonksiyon, 5 KB bölmede bile OOM) → %100 için o birim tek işçide 4 GB heap ile RAM <%70 iken denenmeli; notion'daki 1 bi
- `rapor/yarim-e3.md` — - laya-2 / laya-2c: **DEVAM (gorev-yarim-e3-devam.md)**, kurul↔Opus ρ kapısı (≥0.6) geçmedi; 3 istem denemesi + ridge bitti, DUR kuralı.
- `rapor/yarim-e3.md` — - ÖMER: (a)/(b)/(c) seçimi (tek cümle).
- `rapor/yarim-g-birlestir.md` — |, Şablon/kural dosyası, iş değil (_sablon, SIRA, DEVAM-KURALI) | 3 |
- `rapor/yarim-g2.md` — - beyin-2: ZATEN BİTMİŞ (kapı <%92 geçmedi), bf138f65. ÖMER: kapı/token kararı Desktop'ta.
- `rapor/yarim-g2.md` — - beyin-3: ZATEN BİTMİŞ (kapı geçmedi), 491ea91c. ÖMER: aynı karar.
- `rapor/yarim-g2.md` — - beyin-4: ZATEN BİTMİŞ (doğruluk ≥%92, token hedefi tutmadı), 70c544e2. ÖMER: aynı karar; MAKARA-1 bu karara bağlı.
- `rapor/yarim-g3.md` — | ajan-akis-1 | DEVAM + ÖMER | af55760a, test_akis_damit 8 yeşil; kabul tutmadı (ücretsiz 57→40/55/58, giriş jetonu +%4/+%8,5). Kalan: akis_olc.py madde-çıkarma ablation.
- `rapor/yarim-g3.md` — | arac-zorunlu-4 | DEVAM | bdab1c58, 39 yeşil; --oran 20 → arac_eksik %90 (hedef ≤%10) tutmadı; tools/cekirdek-genis.json yok |
- `rapor/yarim-g3.md` — | autoharness-kur | ZATEN BİTMİŞ + ÖMER | ed4fdb44; ÖMER: dist/autoharness/autoharness-learn.zip yükle, kayba hangi repoda koşsun söyle |
- `rapor/yarim-g4.md` — Sonuç: 22 işin 18'i kanıtla ZATEN BİTMİŞ, 4'ü DEVAM/DUR/ÖMER (erisim-tam-1-a, rea-agir-2-a2, laya-2-a, laya-2-a2). Yeni kod yok; yalnız doğrulama.
- `rapor/yarim-g4.md` — | erisim-tam-1-a | DEVAM (gorev-yarim-g4-devam.md) + ÖMER, 58de9fb5/6dbfdf4c/c648fe99 kapı + ertelemeli yükleme (651k→47k) yapıldı; docs/erisim-haritasi.md §6 açık |
- `rapor/yarim-g4.md` — | laya-2-a, -a2 | ZATEN İŞLENMİŞ / DUR, ebb5e855 (YARIM-E3): ρ kapısı 0.6 geçmedi, kök neden 8/10 bağlı değerler; yeni veri olmadan tekrar koşulmaz |
- `rapor/yarim-g5.md` — - animasyon-1: ZATEN BİTMİŞ (kol/animasyon main'de, rapor/animasyon-1.md) · ÖMER: Desktop'ta `python onay/animasyon_1_uygula.py`
- `rapor/yarim-g5.md` — - arka-aski-1-a2: DEVAM (gorev-yarim-g5-devam.md), graphify update süre sınırı, agentshield koşmadı
- `rapor/yarim-g5.md` — - arka-bekci-1-a: DEVAM, sonuç/rapor/commit yok
- `rapor/yarim-g6.md` — Kod değişikliği yok; yalnız durum taraması (görev dosyası + SIRA.md + git log --grep + ajan-sira result). 28 iş: 21 ZATEN BİTMİŞ, 3 DEVAM/DUR, 3 ÖMER, 1 BEKLEMEDE.
- `rapor/yarim-g6.md` — | token-7b, -devam, -devam-2 | DEVAM | ölçümler bitti (62bf1f69; TOKEN-7g a13f4e35 G06 rubriği daraltıp yeniden puanladı) ama karar/uygulama yok: docs/token/token-7b-sonu
- `rapor/yarim-g6.md` — | tur-6c-b2 | ÖMER | e939e0c4: taze tam G01 $4 tavanı yüzünden koşulmadı, onay komutu bekliyor |
- `rapor/yarim-g7.md` — | desktop-devir-21eki-aksam.md | ters-2-d10, ordu-1-d12 | DEVAM (kanıt yok) | ajan-sira.log 19:56 "BITTI rc0", kabul kaydı yok |
- `rapor/yarim-g7.md` — | desktop-devir-21eki-gece.md | ters-2-d11b | DEVAM (kanıt yok) | ajan-sira/ters-2-d11b.json bozuk |
- `rapor/yarim-g7.md` — | desktop-devir-22eki-1308.md | denklik-1 | DEVAM (kanıt yok) |, |
- `rapor/yarim-h1-24eki.md` — - BEKLEMEDE: telve-yeni, bhs5-* (d1b/d2b/d3/site-2/logo-2), sonra-muzik-kanali. SABLON: DEVAM-KURALI, model-politikasi.
- `rapor/yonetici-api-1.md` — - Tur: 20 dk; bugün Console ≥$2 → 40 dk (ölçüldü: bugün $2.87 → "sonraki tur 40 dk"). Biten iş → `kontrol_onoku.kontrol` (ücretsiz havuz önce, boş/biçimsiz ise Console ha
- `rapor/yonetici-api-1.md` — - DEVAM (27 Eki): (1) Console haiku kolu 3 gerçek raporla koşuldu: $0.0019+$0.0026+$0.0024 = $0.0069 → tur başı ≈$0.0023 (hedef ≤$0.03 TUTTU). Kök neden: defter `.2f` ile

## Video linkleri (docs/video-tarama/bekleyen-linkler.md ∖ kayit/kuyruk): 178

- https://www.instagram.com/p/DafbtU_M-Pt/
- https://www.instagram.com/p/Dd9RvQDiUVH/
- https://www.instagram.com/p/Dd9nkV-AC9G/
- https://www.instagram.com/p/DdQ_Js8AJVi/
- https://www.instagram.com/p/Dd_iThjj32v/
- https://www.instagram.com/p/DdbLPvsgm48/
- https://www.instagram.com/p/DdbkqpEH9t8/
- https://www.instagram.com/p/Ddc1db7Cj_D/
- https://www.instagram.com/p/DdeLN4ujZGN/
- https://www.instagram.com/p/DdjKZp4H-mG/
- https://www.instagram.com/p/Ddqym0VAqzU/
- https://www.instagram.com/p/Ddy0WIDAv8w/
- https://www.instagram.com/p/DeB_xCxDT_F/
- https://www.instagram.com/p/DeCUsonlChf/
- https://www.instagram.com/p/DeD8sC4gqrO/
- …

## SONRA (Ömer 24 Eki: yarım sayılmaz)

bhs5-d0, bhs5-d1, bhs5-d1b, bhs5-d2, bhs5-d2b, bhs5-d3, bhs5-logo-2, bhs5-site-2, logo-1b, logo-3, mod-mai-onizleme, mod-mai-onizleme-b-a2, neffex, neffex-d0, neffex-d1, neffex-d1r, neffex-d2, neffex-d2b, neffex-d2c, neffex-d2d, neffex-d2e, neffex-d2f, neffex-d2g, neffex-d2h, neffex-d2i, neffex-d2j, neffex-d3, neffex-kapanis-1, neffex-kapanis-2, neffex-klon-1, neffex-klon-2, neffex-klon-3, neffex-klon-4, neffex-klon-5, neffex-klon-6, neffex-klon-7, omer-site-d1, omer-site-d1b, omer-site-d1b-a2, omer-site-ref-1, omer-site-ref-1b, site-telve, telve, telve-hazir-1, telve-hazir-2, telve-kapanis-1, telve-kapanis-2, telve-kapanis-2b, telve-kapanis-3, telve-mini, telve-mini-2, telve-r0c, telve-r0d, telve-r2b, telve-r2c, telve-r2d, telve-r2e, telve-r2f, telve-r2g, telve-r2h, telve-r3a, telve-r3b, telve-rework, telve-rework-d1, telve-rework-d10, telve-rework-d2, telve-rework-d3, telve-rework-d4, telve-rework-d5, telve-rework-d6, telve-rework-d7, telve-rework-d8, telve-rework-d9, telve-token-1, telve-v2-faz1, telve-v2-faz1b, telve-v2-faz1c, telve-v2-faz1d, telve-v2-plan, telve-video-1, telve-yeni, telve-yeni-d1, telve-yeni-d1b, telve-yeni-d2, telve-yeni-d3, telve-yeni-d3b, telve-yeni-d3c, telve-yeni-d3d, telve-yeni-d3e, telve-yeni-d4, telve-yeni-d4b, telve-yeni-d4c, telve-yeni-d5
