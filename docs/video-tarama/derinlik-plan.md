# DERİNLİK-MASTER — video hattı planı (4 Eki 2026)

Sonraki oturumlar YALNIZ bu dosyadan devam eder (transcript arama yok). Durum/KALAN her oturumda `.claude/dalga.md`'de; bu dosyada yalnız
"## İlerleme" satırı güncellenir.

## Hedef (Ömer, 4 Eki)
Videolarda çıkan skill/plugin/MCP/CLI ve tekniklerin %95–99'u bünyeye katılır, ama hiçbir kötü yanıyla değil: her kötü yan nedeninden
onarılır, iyi yan bizim araçlarımızla güçlendirilir. Kötü yanı çözülmemiş hiçbir şey kurulmaz; "aday değil" istisnadır. Videoda konuşulan,
ekranda görünen, açıklamada/yorumda/linkli sayfalarda geçen hiçbir şey kaçmaz. Uzun videolar dahil hepsi izlenir; token en az.

## Oturum kuralları (her oturum)
- Başta `.claude/dalga.md` (KARAR · kabul · durum · KALAN, ≤30 satır). Oturum başına en fazla 50 araç çağrısı (paralel çağrılar ayrı
  sayılır); 45'te commit + push, DUR, KALAN güncel.
- Dalga içinde model çağrısı YOK (claude -p 0); canlı koşuları (parti, video indirme, model çağrısı) Ömer yapar; testler sahte veriyle.
- Okuma: dosya içeriği yalnız Read ile dar aralık (~20 satır); konum için Grep -n. PYTHONIOENCODING=utf-8. Yazma Write/Edit.
- Agent aracı ertelenmiş: ToolSearch ile yükle; suite-kosucu yoksa DUR. Pytest borulanırsa `set -o pipefail`; kırmızılık commit'ten ÖNCE görülür.
- Eski test çelişirse DUR, sor; kuralı kendi başına daraltma. Yeni bağımlılık/kurulum/API anahtarı gerekirse DUR, sor.
- Önce mevcut araçlar: Agent Reach (Jina Reader ile sayfa okuma, arama), gh, yt-dlp, ffmpeg, `video whisper`, graphify.
- ~/.claude yalnız OKUNUR; değişiklik yalnız video motoru kodu (tools/video/video/), testleri (tools/video/tests/) ve docs/ altında.
- Ağ: GitHub için gh api; web istekleri arası ≥2 sn; 429/403 kuralı KÜÇÜK-1 K2'deki gibi (mevcut kuyruk metadata yolu).
- Model çağıran her yeni adımın tavanı ayarda (aday/video başına) ve defterde (kayit.jsonl) sayılır.
- Üçüncü taraf sağlayıcıya yalnız kamuya açık video/repo/sayfa içeriği gider; anahtar ve kişisel veri gitmez.

## SIRA
A1 → A2 → A3 → A4 → A5 → C1 → C2 → C3 → C4 → D1 → D2 → D3 → B1 → B2 → B3 → B4 → B5 → E1 → E2 → E3 → F1 → F2 → F3 → A6 → A7 → A8

Önerilen oturum bölümü (50 çağrı tavanına göre; sığmayan bir sonrakine kayar):
O2 A1–A4 · O3 A5, C1 · O4 C2–C4 · O5 D1–D3 · O6 B1–B3 · O7 B4–B5 · O8 E1–E3 · O9 F1–F3 · O10 A6–A8 + tam suit + arşiv + Ömer komutları.

## A — KARAR DOĞRULUĞU
**A1 Kalite takası kodu kurala uydurulur.** `tools/video/video/kur.py:348 takas(s, d, esik_ok)`: kalite düşüşü gürültü bandı içindeyse
(çağıran tarafta d=0'a indirilir, kur.py:372) her tasarruf AL sayılır (omer-kurallar 21; 24 Eyl tablosu). Bugün d==0'da esik_ok yanlışsa
"RED(token)" dönüyor (TOKEN-6e K4 ponytail %4.8 → RED(token) bu daldan). Test: düşüş gürültüde + tasarruf %4.8 → AL; düşüş >%20 +
tasarruf <%50 → RED. Çağıranlar: kur.py:378, kur.py:510, olcum_m4.py:179, olcum_m3b.py:374.
  Ömer kararı (4 Eki, seçenek a): test_takas.py:48 güncellenir (ayrı commit, mesajda "Ömer onayı: A1, omer-kurallar 21");
  takas(5, 0, False) → AL. Düşüş 0 ya da negatif (kalite arttı) her zaman "gürültü içinde" sayılır.
  ⚠ AÇIK SORU 2: test_24e2a.py:24 (düşüş 0, tasarruf %10 → "RED(token)") de yeni kuralla çelişir; onay yalnız test_takas.py:48 için.
  Yorum: "her tasarruf" = s > 0; s ≤ 0 (maliyet aynı/arttı) RED(token) kalır, d ≤ 0 & esik_ok AL kalır → test_girdi.py:84/98,
  test_kalite.py:34, test_kur.py:247 çelişmez.
  Kural metni (kaynak C:\Projeler\omer-kurallar.md madde 21–24, repo dışında; aynen):
  "Kaliteden taviz yok" = kalite takası. Düşüş = kalite puanı ve görev başarısındaki göreli düşüşün büyüğü.
  · düşüş gürültü içindeyse → her tasarruf AL
  · düşüş ≤%10 ve tasarruf ≥%25 → AL
  · düşüş ≤%15 ve tasarruf ≥%30 → AL
  · düşüş %15–20: tasarruf ≥%75 AL · %50–75 SOR (Ömer karar verir) · <%50 RED
  · düşüş >%20: tasarruf ≥%50 SOR · <%50 RED
  · tabloya uymayan ara durum → SOR
  Madde 24 (tasarruf ayrıştırma): RED/SOR çıkan alanda yalnız tasarruf mekanizması kendi sürümümüze alınır, kaliteyi bozan kısım
  ayıklanır/onarılır, yeniden ölçülür.
  Not: tablo yalnız tasarruf değişikliklerine uygulanır; kurulu aracı kapatan bir değişiklik tablo AL dese bile uygulanmaz (A5).
  Ömer kararı 2 (4 Eki, A1'e eklendi): kalite düşüşü kabul edilmez ama aday da elenmez. Tablonun RED(takas) ve SOR çıktıları
  "ONARIM BEKLİYOR (takas: düşüş X, tasarruf Y)" olur — madde 24 döngüsü: tasarruf mekanizması ayrıştırılır, kaliteyi düşüren kısım
  onarılır, yeniden ölçülür; uygulama yalnız sonuç AL'e düşünce. SOR (Ömer kararı) ancak onarım yolları denenip tükendiğinde, denenenler
  listelenerek. Ara durum (düşüş %0–10, tasarruf <%25) dahil. RED(token) aynen kalır. A5 bağı: takas onarımı A5'teki KALİTE kötü yanının
  onarımıdır (aynı "ONARIM BEKLİYOR" durumu, aynı onarım yolları listesi).
  Uygulama: kur.py `takas()` saf tablo olarak kalır (test_takas kademeleri değişmedi); karar katmanı `kararla()` eşler (karar() ve
  compress denemesi kullanır); ayristir_aday "ONARIM BEKLİYOR"u da ayrıştırır. olcum_m3b/m4 tarihsel ölçüm betikleri tabloyu ham basar.
  ✓ A1 bitti (O2): güncellenen eski testler test_takas:48, test_24e2a:24 · test_kur 228/229/237/247, test_kalite:21, test_takas:61.
**A2 (=Y2) --yeniden eksik kapsamı tamamlar:** "onceki"/"tamam" adaylarda model araştırması yok, ama Kapsam'da eksik olan çağrısız işler
koşulur: güvenlik taraması (S5 seyrek klon dahil; ruflo 591 MB → seyrek), lisans API'si, son commit tarihi. Test.
**A3 (=Y7) Kurulu fork:** kurulu marketplace reposu için `gh api repos/<repo>`; fork ise source/parent son commit'i. Fork bayrağı yoksa
video/karedeki sahip kurulu reponun sahibinden farklıysa aynı kontrol. Kapsam: "kaynak farklı: kurulu <repo> (son commit X) ↔ asıl <repo>
(son commit Y)", öneri "UYARLA / kaynağa geç". Test: worldflowai/everything-claude-code (2026-01-23) ↔ affaan-m/ECC (2026-10-02).
Kanıt: ~/.claude known_marketplaces.json 146-151 (ECC → worldflowai).
**A4 (=Y5) "bizde benzer" + kurulu kaynakların tamamı:** aday işlevi kurulu skill/plugin AÇIKLAMALARINDA aranır (ad eşleşmesi şart değil);
en yakın 3 kurulu karşılık panelde "bizde benzer". CSV stil/palet+arama betiği → ui-ux-pro-max; depo geneli güvenlik taraması →
security-assessment / Strix / gstack-cso. Kaynaklar: installed_plugins + ~/.claude/skills + plugin skill dizinleri (yalnız OKUNUR). Test:
nextlevelbuilder/ui-ux-pro-max-skill → kurulu ui-ux-pro-max (ZATEN VAR + güncellik); gstack → garrytan/gstack; paket içi security-review → ECC reposu.
**A4b "bizde benzer" İngilizce kaynakla (Ömer, 4 Eki):** aday tarafı adayın İngilizce kaynağıdır — repo açıklaması + README'nin ilk ~30
satırı (`gh api repos/<repo>` + `/readme`, istekler arası ≥2 sn; sonuç durum.json'da `kaynak_en`, tekrar istenmez); kurulu araç
açıklamalarıyla aynı sözcük örtüşmesi (A4 puanı değişmez). Türkçe video notu yalnız yedek (repo yok / gh yok / okunamadı). İlk 3 içinde
skor farkı küçük (1. − 3. < eşik) belirsiz durumda mevcut Jev eşdeğer yolu (uygula.esdeger deseni: en yakın 5 + "yok" choice) seçer;
aday başına en fazla 1 çağrı, sonuç `benzer_jev` (tekrar sorulmaz), defterde (defter.jsonl `benzer_jev`) sayılır. Test (gerçek envanter):
Türkçe notlu + İngilizce README'li tasarım adayı → ui-ux-pro-max ilk 3'te; depo geneli güvenlik tarama adayı → security-assessment / Strix /
gstack-cso ilk 3'te; belirsizde tek Jev çağrısı + defter satırı, açıkta çağrı yok. Prototip ölçümü: Türkçe notla ikisi de ilk 5 dışında.
**A5 KUR + ONARIM + GÜÇLENDİRME:** araştırıcı istemine (aday-arastirici) ve panele "## Kötü yan + onarım + güçlendirme" bölümü. Varsayılan
öneri KUR/UYARLA. Kötü yan sınıfları: token (oturum başı enjeksiyon + skill listesi payı; ölçülen/tahmin) · performans (RAM, süre, arka
plan süreci) · kalite (kurulu araçla çakışma, yanlış tetikleme) · güvenlik (SkillSpector, izinler). Her birinin onarımı (B5'in bulduğu
nedene göre): TOKEN-3 profili · Skill aracıyla tembel yükleme · aracın kendi hafifletme ayarı · sarmalayıcı · kendi uyarlanmış sürümümüz
(kod kopyalanmaz) · paketin yalnız taranmış kısmı. Güçlendirme: iyi yanın bizim araçlarımızla (graphify, Headroom, departman skill'leri,
kurulu benzerler) nasıl daha iyi çalışacağı. Kurulu aracı kapatan ayar onarım SAYILMAZ. Onarımı bulunmayan kötü yan "çözülmedi"; aday
"ONARIM BEKLİYOR" olur — kurulmaz, kötü yan katılmaz, elenmez. SOR/RED yalnız onarım yolları denenip tükendiğinde (denenenler listelenir).
Eski formlar geçerli (yeni alanlar isteğe bağlı). Test: çözülmedi kötü yanı olan aday KUR gösterilemez → ONARIM BEKLİYOR.

## C — İZLEME KAPSAMI + TOKEN (uzun videolar dahil)
**C1 Konuşma kaynağı:** altyazı yoksa ya da otomatik altyazı bozuksa (sözlük dışı/anlamsız kelime oranı eşiği ayarda) `video whisper`.
Kullanılan kaynak kapsamda yazılır. Test (sahte altyazı: temiz → altyazı; bozuk oran > eşik → whisper yolu; yok → whisper).
**C2 Kare seçimi sabit aralık değil:** sahne değişimi (ffmpeg scene) + metin yoğunluğu + altyazıda ekrana/repoya/linke/komuta/prompta/
ayara işaret eden anlar. Algısal hash (Pillow, dHash) ile aynı ekran tekrar seçilmez. Test. (Pillow kurulu değilse DUR, sor.)
**C3 Yerel OCR:** Windows yerleşik Windows.Media.Ocr (kullanılamazsa DUR, sor); seçilen tüm karelerden metin çağrısız çıkarılır; URL,
owner/repo, kurulum komutu (npx, pip, uv, claude mcp add, /plugin install …), prompt ve ayar parçaları pakete metin olarak girer. Modele kare
yalnız OCR'ın anlamlandıramadığı (kod, şema, arayüz) anlarda gider. Video süresine göre kare tavanı ayarda; tavanı aşan anlar
"incelenmedi (sebep)". Test (OCR sahte).
**C4 Kapsam satırı (video başına):** sahne N · seçilen kare M · OCR'lanan K · modele giden J · altyazı kaynağı · incelenmeyen anlar.
Ölçüm planı: aynı uzun videoda eski ↔ yeni paket jetonu ve bulunan bahis sayısı (Ömer'in canlı koşusu için komut raporda). Test.

## D — İZ TABLOSU (hiçbir şey kaçmasın)
**D1** Her video raporunda "## İz": her bahis bir satır — kaynak (konuşma mm:ss · kare mm:ss · açıklama · yorum · linkli sayfa) · ne ·
bağlandığı aday ya da "aday değil: <sebep>" · kanıt. Sabit sebep listesi: genel kavram · başka adayın parçası (hangisi) · sponsor/reklam ·
konu dışı. "Zaten kurulu" aday değil sebebi DEĞİLDİR: kurulu araç da aday olarak karşılaştırılır (29 Eyl ilkesi). Test (rapor-denetle
sabit liste dışı sebebi ve "zaten kurulu"yu reddeder).
**D2 Çağrısız kaçak denetimi:** altyazı + OCR + linklerden çıkarılan aday benzeri her şey (sözlük = kurulu araçlar + tüm aday dosyaları;
desenler: URL, owner/repo, kurulum komutları, büyük harfli ürün adları) İz'de yoksa "KAÇAN?" işaretlenir. Test.
**D3** Panelde "## Denetim": bahis · bağlanan · aday değil (oran) · KAÇAN? sayıları. KAÇAN? > 0 iken `video parti kapat` durur (bağla ya
da sebep yaz). "Aday değil" oranı %5'i aşarsa uyarı. Test.

## B — İNTERNETİ TARAMA (yalnız GitHub değil)
**B1 Link toplama:** açıklama + yorum + OCR + altyazıda geçen URL/alan adları + linkli sayfalardaki ilgili linkler (1 derinlik). Sınıf:
github · gist · doküman · blog · ürün/marketplace · video · sosyal · diğer. Aynı URL bütün partilerde bir kez okunur (önbellek). Test.
**B2** Her link açılır (Agent Reach / Jina Reader), gövde temizlenir; araştırıcıya yalnız aday adlarının ve kurulum/ayar/sınırlama
kelimelerinin geçtiği pencereler gider. Erişilemeyen "erişilemedi (sebep)". Sayfadan yeni araç çıkarsa yeni aday + İz satırı. Test (sahte okuyucu).
**B3 Yapımcı nasıl yaptı (aday başına):** README + docs + CHANGELOG/sürüm notları + en çok tepki alan açık ve kapalı issue/discussion
başlıkları (gh api, en fazla N, ayarda) + yazarın duyuru/blog yazısı. Bilinen hata, sınırlama, şikâyet → A5 kötü yanı; yazarın önerdiği
ayar/çözüm → A5 onarımı (kaynak linkiyle). Test (sahte gh).
**B4 Genel web araması** (aday başına en fazla N sorgu, ayarda; mevcut arama yolu = Agent Reach): inceleme, karşılaştırma, alternatif,
bilinen sorun. Forum/sosyal kaynaklar "düşük güven" etiketli. Test.
**B5 Mekanizma incelemesi** — "aday değil" dışındaki HER aday (kurulu olanlar dahil; kuruluysa bizdeki kopya): repo seyrek klonlanır (S5
sınırları); graphify --code-only ve grep ile çağrısız konumlandırma: oturum başı enjeksiyon, hook'lar, başlatılan süreçler, ağ çağrıları,
izin kapsamı, ayar okuma noktaları, ağır döngüler. Modele yalnız bulunan ilgili dosyalar gider (aday başına en fazla N KB, ayarda). Aynı
repo + aynı commit bütün partilerde bir kez incelenir (önbellek). Çıktı: her kötü yanın nedeni (dosya:satır) + onarımın nereden yapılacağı
(ayar · sarmalayıcı · kendi sürüm) + iyi yanın nasıl güçleneceği → A5'e. Repo yoksa (servis/ürün) B2–B4 kaynaklarıyla aynı alanlar
doldurulur, "kod yok" yazılır. Test.

## E — DESKTOP İKİNCİ BAKIŞ (hedefli, uyarlamalı)
**E1 Çağrısız risk puanı** (bahis/aday başına): KUR önerisi · güvenlik bulgusu · fork/kaynak farkı · kapsam eksikleri · "çözülmedi" kötü
yan · "aday değil" · KAÇAN? · yeni link sınıfı. `docs/kurulumlar/parti/<id>/denetim.md` (≤150 satır): KAÇAN?'ların hepsi · "aday
değil"lerin hepsi · "ONARIM BEKLİYOR"ların hepsi · risk puanı en yüksek 5 · tohumlu rastgele 3. Her satırda Desktop'un açacağı TAM URL'ler
(videonun mm:ss linki, repo, ilgili dosya, issue, doküman) — Desktop yalnız sohbette görünen adresleri açabilir. Test.
**E2 Geri dönüş:** denetim.md sonunda "## Desktop" şablonu; Ömer Desktop'un verdiği satırları buraya yapıştırır; `video parti
denetim-isle <id>` bunları `docs/kurulumlar/desktop-denetim.jsonl`'a ve ilgili aday dosyasına işler. Test.
**E3 Uyarlamalı örneklem:** son 3 partide Desktop bulgusu 0 ise rastgele 3 → 1; her bulgu +3 (en fazla 6). KAÇAN?, "aday değil", "ONARIM
BEKLİYOR" ve risk puanı en yüksek 5 her zaman kalır. Test.

## F — UCUZ ÇALIŞTIRMA (yalnız hattın arka plan model çağrıları; CC etkileşimli yönlendirme TOKEN-5'te)
**F1 Model yönlendirme adaptörü:** hattın model çağıran her adımı (tarama, araştırma, mekanizma, karşılaştırma, özet) için ayarda
sağlayıcı/model seçimi; varsayılan bugünkü gibi, DEĞİŞMEZ. Hedef OmniRoute (kurulu omni-* skill'leri; sunucu çalışıyor mu, kimlik bilgisi
var mı salt okunur kontrol — değer basılmaz, boolean; yoksa DUR, sor) ve videolarda geçen benzeri yönlendiriciler. Test (sahte sağlayıcı).
**F2 Adım bazlı A/B düzeneği:** aynı girdi, iki model; kalite (kör puan + görev başarısı) + $; karar A1'le düzeltilmiş 24 Eyl tablosuyla.
Yalnız AL çıkan adım yönlendirilir. Test.
**F3** Ömer'in koşacağı canlı A/B komutu + tavan (en fazla N çağrı) raporda.

## A (devam)
**A6 (=Y4)** Son commit tarihi kurulu olmayan her repo için de alınır (stop-slop, marketingskills, ui-ux-pro-max-skill, vercel-labs/skills,
ruvnet/ruflo); sürüm numarasıyla kurulu plugin'de tag → commit → tarih (derinlik-3.md S3: bugün yalnız sha ile kurulu plugin'de `commits`
çağrısı var). Ömer notu (4 Eki): eski aday dosyasında `lisans:`/`son_commit:` satırı yoksa eklenir, mevcut içerik değişmez
(A2'nin `_eksik_tamamla` ponytail notu kapanır). Konum: alan bloğunun sonu (ilk `#`/`##` satırından önce) — uy.alanlar() yalnız o bloğu
okur; dosya sonuna eklenen satır panelde görünmez. Test.
**A7 (=Y6)** Prompt adayında metin neden alınmadı teşhis edilir (altyazı mı, kare mi); düzeltilir; yine alınamazsa sebep Kapsam'da. Test.
**A8 (=K2)** `video kuyruk yenile`: kuyruk.md'de süresi/başlığı "?" olan satırları metadata ile yeniden doldurur (≥2 sn, 429/403 kuralı
mevcut gibi; yine başarısızsa hata metni satır notuna). Test (sahte yt-dlp).
Bağlam: 2026-10-03-short partisinin durum.json'u `.kos/2026-10-03-short/` altında; panel `docs/kurulumlar/parti/2026-10-03-short/panel.md`.

## KABUL (her oturum)
- Her madde kırmızı-önce ayrı commit · eski test değişmez (çelişirse DUR, sor) · oturum sonunda ilgili suite (tools/video).
- SON oturumda tam suit (suite-kosucu; koşarken yazma/commit yok; boş RAM ≥6 GB ve ağır süreç yok — oyun dahil).
- gitleaks (değişenler) · commit'te yalnız bu işin dosyaları (`git add <dosya>`; docs/kurulumlar/parti/, docs/kurulumlar/adaylar/,
  docs/video-tarama/ raporları ve .kos/ hariç).
- Son oturumda dalga.md → `.claude/dalga-arsiv/DERİNLİK-MASTER.md` (doğrulanır) · son commit + push · `graphify update .` ÖN PLANDA.

## TAVİZ YOK
Canlı koşu (parti, video indirme, model çağrısı; testler sahte veriyle) · beklemesiz istek · eski test değiştirmek · repo/kullanıcı dosyası
silmek · onaysız yeni kurulum veya anahtar · kötü yanı çözülmemiş adayı "KUR" göstermek.

## RAPOR
Her oturum ≤8 satır: commit'ler · suit · biten/kalan maddeler · DUR sebebi varsa · sapmalar. SON oturum ek: Ömer'in koşacağı komutlar
(short partisi: `video parti devam 2026-10-03-short --yeniden-tara --paket-yeniden` + `video parti akil 2026-10-03-short --yeniden`; bir
uzun video için C4 ölçümü; F3 A/B) + tahmini ek çağrı/$ tavanları. Dalga bitince /clear.

## Bilinen DUR noktaları
A1 test_takas.py:48 çelişkisi · C2 Pillow yoksa · C3 Windows.Media.Ocr erişilemezse (ek paket gerekirse) · F1 OmniRoute sunucu/kimlik yoksa
· suite-kosucu ajanı yoksa.

## İlerleme
O1 (4 Eki): plan yazıldı. O2 (4 Eki): A1 ✓ (video 569 yeşil). O3 (4 Eki): A2 ✓ · A3 ✓ (video 573). O4 (4 Eki): A4 ✓ · A5 ✓ (video 581). Sonraki: C1.
