---
name: video-uygula
description: "Video linklerinden işe yarayanı risk katmanıyla uygular: kural ve yalnız-md skill otomatik, çalıştırılabilir her şey ONAY bekler. /video-uygula url... [--tarama-atla]. Yalnız CC'de."
---

# video-uygula — tarama → değerlendirme → katmanlı uygulama

Kurulum yalnız Ömer'in ONAY'ından sonra `video onay` ile (yapılandırılmış adım, serbest kabuk yok); settings.json ve global CLAUDE.md hiç değişmez. claude.ai'de: okuma rehberi (sandbox'ta `video` yok).

## Akış (ana ajan)

```text
1. Tarama: /video-tarama akışı (skills/video-tarama/SKILL.md). --tarama-atla: bugünkü docs/video-tarama/<tarih>-toplu.md kullanılır, alt ajan taraması yok.
2. video projeler                      # docs/projeler.md: proje CLAUDE.md'lerinden 1-2 satır (mtime'la yenilenir)
   video durum                         # docs/durum.md (≤3k token): köprü katalogu · son kararlar · ölçüm bulguları · ELE; bütün envanter okunmaz
3. Seçim (ana ajan): toplu tablodaki UYGULA + BEKLE adaylarından en fazla 5; ölçüt projeler.md + dört ölçüt
   (bakım · CC'de çift mi · izin kapsamı · context maliyeti). Aday başına 1 satır gerekçe. Dört ölçütte düşen: aday.md'ye `red: <gerekçe>`.
4. Araştırma: araç adayı (skill/plugin/MCP/CLI/hook/uygulama) başına bir Agent (subagent_type: aday-arastirici — sonnet), ≤3 eşzamanlı.
   Prompt tek satır: `ad: <kebab> · tür: <tür> · video: <id> · ipucu: <tablodaki ne işe yarar / link>`. Çıktı docs/kurulumlar/adaylar/<ad>.md.
   İpucu/iş akışı adayında araştırılacak repo yok: aday.md'yi ana ajan yazar (alanlar: ad · tur · video · kural: <tek cümle kural>).
4b. video bizde <aday.md>...          # jev skill (2 istek/aday): p≥act skill'ler ## Bizde durum'a + `kurulum:` satırı (katalog → settings: kurulu-açık/kurulu-kapalı/yok; doğrulanmamış varsayım yazılmaz); ana ajan durum.md araç + ölçüm satırlarını ekler
4c. Değerlendirme (ana ajan): aday başına 6 bölüm Ne · Bizde durum (var/kısmen/yok + dosya/araç adı) · Beklenen fayda (ölçülebilir) · Maliyet/risk · Karar · Sonraki adım;
   alan `karar: KUR|DENE|ÖĞREN|ZATEN VAR|ALTERNATİF|RED`. Teknik iddia: resmi doküman (context7/mslearn/WebFetch, video başına ≤3); bulunamazsa `dogrulama: doğrulanamadı`, guven ≤ orta.
5. video katman docs/kurulumlar/adaylar/<ad>.md... [--yeniden] [--istek-tavan M]
6. Sohbete katman çıktısı (≤20 satır) + seçim gerekçeleri.
```

## Kararlar (15)

- Tarif/keşif öncesi: `jev ilgili "<konu>" C:/Projeler/omer-skills/bilgi` → ilk 3 kart (bayatsa `video bilgi --bayat`, yeniden doğrula).
- KUR → aşağıdaki katmanlar. DENE → docs/denemeler/<ad>.md (hipotez · metrik · bütçe · geri alma · başarı eşiği; 14b'de koşulur). ÖĞREN → bilgi/<slug>.md kartı. ZATEN VAR · ALTERNATİF · RED → yalnız kayıt.
- İpucu/iş akışı KUR: model/araç adı geçen (Fable, Opus, Sonnet, RTK, graphify…) kodla olgu; ad geçmiyorsa Jev {davranış kuralı, olgu}; olgu kural dosyasına girmez → ÖĞREN. Çift kart → kaynak mevcut karta eklenir.
- Yeni kural/olgu en yakın kural ya da kartla çelişirse ÇELİŞKİ: eklenmez, Ömer karar verir. Sponsor anındaki aday `sponsor` etiketli, seçimde sona.
- Eski işaretler: ÇİFT/ÖNCEDEN-GÖRÜLDÜ → ZATEN VAR; UYGULA/BEKLE → değerlendirmeye girer. Tam rapor docs/kurulumlar/<tarih>-uygula.md; sohbete ≤25 satır.

## Katmanlar (`video katman`, deterministik)

- Kayıtta (docs/kurulumlar/kayit.jsonl) olan ad atlanır; `--yeniden` zorlar.
- T0 ipucu/iş akışı: 12f kural karşılaştırması (≤2 Jev/aday); çiftse ZATEN VAR. Değilse kural dosyasına YAZILMAZ (15b): docs/kurulumlar/bekleyen/kural-<slug>.md (madde · gerekçe · çift/çelişki · kaynak) + raporda `ONAY kural <slug>`. Ömer onaylarsa CC'de `video kural-onay <slug>` C:\Projeler\omer-kurallar.md'ye `N. <kural> (video <id>, 15b)` ekler (çiftse eklemez). Köprüde yok; global CLAUDE.md'ye hiç yazılmaz.
- RED: `red:` alanı · lisans MIT/Apache-2.0/BSD/0BSD/ISC/CC-BY-4.0 değil ya da yok · arşivli · son commit >12 ay · skill'de SkillSpector koşmadı ya da HIGH/CRITICAL >0.
- T1 skill: kaynak klasörü gerçekten listelenir; yalnız .md (+LICENSE/NOTICE) → skills/<ad>/ + LICENSE + KAYNAK.md (repo@commit) + dist/yukle-14/yeni/<ad>.zip + skill_denetim; denetim hatası → geri alınır, T2.
- T2 geri kalan her şey: docs/kurulumlar/bekleyen/<ad>.md (`# ONAY <ad>` + aday.md). Biçim (aşağıda) geçmezse dosya başı `BİÇİM EKSİK: …` ve raporda `elle düzelt <ad>`; komut koşulmaz.

## Onay · geri al · dene (14b, yalnız CC; köprüde yok)

- Bekleyen biçimi: `## Kurulum` / `## Geri alma` → `- <plugin|mcp|uv|npm|winget>: <argümanlar>`; `## Duman testi` → `- komut:` · `- cikis:` · `- desen:` (ops.); ops. `## Köprü izni` (`- arac:` · `- altIzin:` yalnız salt-okur) ve `## Ayar` (`- üst.alt: <JSON>`, env altında yalnız `${AD}`). Metakarakter (`; & | > < \` $(`), indirici/kabuk (curl, iwr, iex, sh, cmd, powershell…), uzak betik, düz anahtar değeri → red.
- `video onay <ad> --kuru` → planı göster (argv, duman, geri alma, köprü, PowerShell bloğu); hiçbir şey koşmaz. Ömer "ONAY <ad>" derse `video onay <ad>`: adımlar sırayla → duman testi; adım ya da duman başarısızsa geri alma adımlarının hepsi koşar, kayıt `RED(adım|duman)`. Başarı: kayıt {karar KUR, kurulum_tarihi, geri_alma}; Köprü izni yeni araç girdisi olarak kopru.json'a (envGecir yok) → "Desktop yeniden başlatma gerekli". settings.json değişikliği KOŞULMAZ: PowerShell bloğu rapora, Ömer elle koşar.
- `video geri-al <ad>` → kayıttaki geri_alma adımları + eklenen köprü girdisi çıkar → kayıt "geri alındı".
- `video dene <ad> [--tavan 18] [--istek-tavan 30]` → docs/denemeler/<ad>.md (Hipotez · Metrik · Bütçe · Başarı eşiği · `## Talimat` yolu) + sabit 6 görev (docs/denemeler/gorevler/: özet · fonksiyon · kapanış · kod düzeltme · Türkçe soru · talimat izleme). A 2 tekrar (gürültü), B 1: `claude -p --model sonnet --output-format json`, B + `--append-system-prompt <talimat gövdesi>`; JEV_SKILL_HOOK=0; 3·görev > tavan → hiç koşmaz.
- Kalite kapısı (18, düşüşe pay yok): görev dosyasının `beklenen:` bölümü makine kontrolüdür (`- olgu: <regex>` · `- yasak: <regex>` · `- pytest: fixture/test_x.py` — yanıttaki son python bloğu `dosya:` yerine konup test koşar); modele gitmez. Satır sayısı ve biçim regex'le değil kodla: `- satir-en-fazla: N` · `- satir-en-az: N` · `- satir-desen: <regex>` (her boş olmayan satır tam eşleşir). Koruma: görev yüklenirken her regex 50 KB düşmanca metinde 1 sn'de bitmezse görev reddedilir (hiç çağrı yok); yanıt kontrolü ayrı süreçte 10 sn, aşılırsa başarısız. Her claude -p sonucu docs/denemeler/.kos/<ad>/<görev>-<kol>-<tekrar>.json'da (istem+talimat hash'i); aynı hash yeniden çağrılmaz, tavan yalnız yeni çağrıyı sayar; her çağrı sonrası tek satır ilerleme. KUR önerisi yalnız (1) token eşiği tutarsa VE (2) her görevde B başarı ≥ A başarı ortalaması VE (3) B kalite ≥ A − max(gürültü, 0.1) (gürültü = A1-A2 kalite farkı ortalaması). Yoksa `RED(token)` / `RED(kalite)` / ikisi. Sonuç: görev başına A/B başarı · kalite · çıktı token, toplam $.
- Kayıt satırı: {ad, katman, karar, tarih, video, kaynak_commit, geri_alma}.

## Derin inceleme (17)
- Birim araç değil özellik: aday.md `## Özellikler` (`### <slug>` + ne · kurulum · lisans · etiket · karar · gerekce) varsa `video katman` her özelliği ayrı karara bağlar; kayıt `{ad: aday/özellik, aday, ozellik, yargi, karar, gerekce}`.
- UYARLA: aracı kurmadan fikri kendi aracımıza → docs/uyarlamalar/<aday>-<özellik>.md (fikir · hedef · beklenen etki · kapsam); kod yazılmaz, Desktop tarif verir.
- Token etiketli özellik varsayılan DENE (deneme dosyasında token metriği zorunlu). RED yalnız kanıtla: `ölçüm:` var olan docs/denemeler/*-sonuc.md · `zaten var:` katalog/durum.md adı ya da var olan dosya · `güvenlik:`/`lisans:` aday dosyasındaki bulgu. Kanıt yoksa DENE + "K4: kanıt bulunamadı".
- Lisans: izinli liste yalnız T1 (repoya kopyalama). T2'de kaynak-erişilebilir (BSL-1.1, FSL, Elastic-2.0) RED değil, lisans notu. `telemetri: açık` ise `## Telemetri kapatma` yoksa biçim hatası.
- İddia sınama: aday.md `## İddia sınama` (iddia · kaynak · sonuç · not · kart); kaynaksız sonuç → doğrulanamadı; abartılı/yanlış + kart → bilgi/<kart>.md'ye not. Rapora İDDİA SINAMA tablosu + boş `## Desktop ikinci görüş`.
- `video brief <rapor>` ≤60 satır (özellik kararları · departman · iddialar · linkler); köprüde açık, Desktop ikinci görüşü buradan okur.
- Departman (19): KUR/UYARLA olan yeni araç tek Jev choice ile 10 departmandan birine → kayıt `departman:`, docs/departmanlar/envanter.json (`kaynak: katman`) + katalog, rapor DEPARTMAN bölümü; elle.json kazanır. Tüm envanter: `video departman [--yeniden] [--istek-tavan 450]`.

## Skill fabrikası (18, yalnız CC; köprüde yok)
- `video uret <ad>` girdisi docs/uyarlamalar/<ad>.md: `arac: talimat|skill` · `token_tavani` (yoksa 200) · `aday` · `ozellik` · `kaynak_metin` · `lisans`; bölümler Fikir · Kapsam · Alınmayacaklar · Başarı eşiği. Her yanıta etki eden davranış skill değil talimattır.
- Taslak yoksa uret brief basar (rc 3). Taslağı oturum modeli yazar: superpowers:writing-skills + skill-creator yüklenir; frontmatter `name` + `description` (yalnız tetik, "Use when …"/"… kullan"), gövde biçim tarifi (yasak listesi değil), FİKİR alınır METİN kopyalanmaz. Yol: talimat → docs/uyarlamalar/<ad>-talimat.md, skill → skills/<ad>/SKILL.md; sonra `video uret <ad>` yeniden.
- Denetim (hata → rc 2, dene koşmaz): gövde token ≤ tavan · description tetik · kaynak metinle 8-gram örtüşme ≤%10 · lisans MIT → KAYNAK.md atfı. Geçerse docs/denemeler/<ad>.md yazılır ve kalite kapısı (`dene`) otomatik koşar.
- KUR önerisi → docs/kurulumlar/bekleyen/<ad>.md: skill → T1 + dist/yukle-18/yeni/<ad>.zip; talimat → araç önerisi (global CLAUDE.md'ye `@<ad>.md`) PowerShell bloğu, ONAY, koşulmaz. RED → sonuç + bilgi/<ad>.md kartı.

## RED şablonu (18)
- RED adayında altı alan zorunlu değil: tek gerekçe satırı (`gerekce:`), boş alanlar raporda `-` ("(eksik)" üretilmez, eksik alan uyarısı yok).
- İddia sonucu: doğru · kısmen doğru · abartılı · yanlış · doğrulanamadı; parantezli nitelik serbest (`doğru (ikincil kaynak)`).

## Aday dosyası (≤40 satır)

Başta alan satırları: `ad · tur · video · repo · lisans (SPDX|yok) · son_commit · arsiv · kaynak (yerel skill klasörü|yok) · kural (ipucu) · red (isteğe bağlı)`.
Bölümler: Ne · Kanıt · Kurulum · İzinler · Duman testi · Geri alma · Köprü izni (yalnız salt-okur alt komutlar) · Önerilen katman.

## Tavanlar

Jev: tarama önbellekten 0; bizde aday başına 2; katman aday başına ≤5 (+sponsor 1, +departman 1); departman ≤450 (hash önbellek); dene/uret ≤30. claude -p: dene/uret ≤18 (görev × A 2 + B 1, tavan aşılırsa hiç koşmaz). Araştırıcı alt ajan ≤5. Çıktı: aday → karar → gerekçe · ÖĞRENİLENLER · ÇELİŞKİLER · DENENECEKLER · OTOMATİK UYGULANDI · ONAY BEKLİYOR · YÜKLENECEK ZIP · RED.
