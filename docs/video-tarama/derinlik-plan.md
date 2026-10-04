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
- ÇAĞRI SAYACI (Ömer, 4 Eki; O10 ~65, O12 ~56 tavanı aştı): her 10 araç çağrısında dalga.md'nin ilk satırına "çağrı N/45" yazılır;
  40'ta yeni madde başlatılmaz; 45'te commit + push ve DUR.
- ONAY KURALI (Ömer, 4 Eki): "Ömer onayı" etiketi yalnız Ömer'in o değişikliği açıkça onayladığı commit'e yazılır; eski testi
  değiştirmek gerekirse önce DUR, sor. (O12'deki KOD2 değişikliği — test_c3/test_c4, aynı OCR metni tek kare — sonradan onaylandı.)
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
A1 → A2 → A3 → A4 → A5 → A4b → C1 → C2 → C3 → C4 → D1 → C5 → D2 → D3 → B1 → B2 → B3 → B4 → B5 → E1 → E2 → E3 → F1 → F2 → F3 → A6 → A7 → A8

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
Koruma (Ömer, 4 Eki O6): whisper süre sınırı kalkar ama yalnız altyazı yoksa ya da bozuksa çalışır; başlamadan boş RAM ≥6 GB ve ağır
süreç yok (oyun, Blender, tam suit; ad listesi ayarda) — değilse "whisper atlandı (sebep)", video kare-yalnız sürer (`--paket-yeniden` ile
tekrar). Uzun ses parçalara bölünür (whisper.json'da parça parça); yarıda kalırsa ses silinmez, kaldığı parçadan sürer. Tahmini ve gerçek
süre kapsamın "konuşma" alanına yazılır. Test (sahte whisper).
**C2 Kare seçimi sabit aralık değil:** sahne değişimi (ffmpeg scene) + metin yoğunluğu + altyazıda ekrana/repoya/linke/komuta/prompta/
ayara işaret eden anlar. Algısal hash (Pillow, dHash) ile aynı ekran tekrar seçilmez. Test. (Pillow kurulu değilse DUR, sor.)
**C3 Yerel OCR:** Windows yerleşik Windows.Media.Ocr (kullanılamazsa DUR, sor); seçilen tüm karelerden metin çağrısız çıkarılır; URL,
owner/repo, kurulum komutu (npx, pip, uv, claude mcp add, /plugin install …), prompt ve ayar parçaları pakete metin olarak girer. Modele kare
yalnız OCR'ın anlamlandıramadığı (kod, şema, arayüz) anlarda gider. Video süresine göre kare tavanı ayarda; tavanı aşan anlar
"incelenmedi (sebep)". Test (OCR sahte).
C3 notu (Ömer, 4 Eki O8): İngilizce tanıyıcı kuruldu (Language.OCR en-US; tr-TR de kurulu). Her kare iki tanıyıcıyla (tr + en) okunur,
sonuçlar birleştirilir: URL/komut/kod için en, Türkçe arayüz metni için tr; çakışmada güven puanı yüksek olan. C3 bitince C2'deki geçici
metin yoğunluğu ölçüsü (JPEG bayt/piksel) OCR karakter sayısıyla değiştirilir.
**C4 Kapsam satırı (video başına):** sahne N · seçilen kare M · OCR'lanan K · modele giden J · altyazı kaynağı · incelenmeyen anlar.
Ölçüm planı: aynı uzun videoda eski ↔ yeni paket jetonu ve bulunan bahis sayısı (Ömer'in canlı koşusu için komut raporda). Test.
C4 eki (Ömer, 4 Eki O9): modele giden kare tavanı süreyle büyür — max(--kare, ceil(süre_dk / 3)); üst sınır ve video başına paket jeton
bütçesi ayarda. Tavan ya da bütçe yüzünden "incelenmedi" kalan anlar Kapsam satırında sayıyla görünür ve E1 denetim.md'ye girer.
`video paket <id> --incelenmedi` (partide `devam --incelenmedi`) yalnız bu anları ikinci geçişte işler. Test.
C4/C3 düzeltmesi (Ömer, 4 Eki O10; kanıt: canlı b2QkhmQ0sT0 20:31 → sahne 51 · seçilen 24 · OCR 17 · model 7 · incelenmedi 8, hepsi
"kare tavanı 7"; paket ~9.5k / 40k): (1) parti yolunda modele giden karelerde asıl sınır PAKET_BUTCE; kare tavanı KARE_UST (20) sabit,
süre_dk/3 yalnız taban; doğrudan `paket --kare N` aynen. C4 testleri buna göre (ayrı commit, "Ömer onayı: C4 tavan → bütçe"). Test: 20 dk,
24 seçilen, 17 OCR → 15 model karesi, incelenmedi 0. (2) OCR birleştirme: aksan katlanınca (ş→s ı→i İ→I ü→u ö→o ç→c ğ→g, büyük-küçük
harf yok sayılır) tr = en ise en; tr yalnız Türkçe ipucu (ve, bir, için, ile, bu, da, de, olarak, gibi…; ayarda) varsa. Gürültü satırı
(anlamlı kelime yok ya da anlamsız oranı yüksek) pakete yazılmaz; sayısı izleme'de "OCR gürültü N". Test (gerçek örnekler). (3) kare_sigdir
(40k girdi tavanı) düşürdüğü anlar kapsam.json incelenmedi'ye "girdi tavanı" sebebiyle; izleme sayısı güncellenir. Test.
C4/C3 ikinci düzeltme (Ömer, 4 Eki O11; kanıt: canlı b2QkhmQ0sT0 --kare 20 → seçilen 44 · OCR 25 · model 20 · incelenmedi 8 "kare
tavanı 20" · OCR gürültü 43 · ~7k metin + ~8.8k kare ≈ 15.9k / 40k; 66–90 sn'de 5 kare, 728/730 neredeyse aynı ekran): (1) tek girdi
hesabı: PAKET_BUTCE ve kare_sigdir (GIRDI_TAVAN) aynı fonksiyon — gerçek kare jetonu (_kare_tk) + OCR dahil tam paket metni; KARE_TK
1600 varsayımı kalkar. Test: ~440 jetonluk 28 kare + ~7k metin → kare düşmez. (2) model kare sınırı yalnız bütçe: KARE_UST güvenlik üst
sınırı 60 (ayarda); C4/O10 testleri buna göre (ayrı commit, "Ömer onayı: tavan 20 → bütçe"). Test: 44 seçilen, 28'i model gerektiren 20
dk → model 28, incelenmedi 0. (3) tekrar ayıklama: (a) katlanmış OCR metni benzerliği ≥0.9 (ayarda) iki kare tekrar, metni uzun olan
kalır; (b) OCR'sız/model karelerinde aynı sahne içinde ve dHash Hamming ≤10 (ayarda) tek sayılır, sahne değişimi varsa ayrı. Test:
66/67/70/75 tek kare, 728/730 tek kare, farklı OCR metinli iki kare kalır. (4) atılan OCR gürültü satırları <id>/ocr-gurultu.txt'ye
(zaman · satır). Test.
O11 (5) aday sayısı ile model tavanı ayrılır (Ömer kararı, 4 Eki): parti yolunda --kare model tavanını değil aday tabanını taşır (kare_sayisi,
eskisi gibi); model tavanı ayrı bayrak `paket --model-tavan M` (varsayılan = --kare, eski davranış korunur), parti M = KARE_UST (60). Aday
kümesi: sahne.json'daki HER sahneden bir kare (en yüksek skor değil, hepsi) + altyazı işaret anları + kare_sayisi kadar segment merkezi;
tekrarlar (3) ile ayıklanır; aday üst sınırı ADAY_UST (ayarda, ör. 150; aşan sahneler skor sırasıyla kesilir, "incelenmedi (aday tavanı)").
Test: 51 sahneli 20 dk video → aday ~51 + işaret + 8, 180 değil; doğrudan `paket --kare 20` eski davranış; `paket --kare 8 --model-tavan 60`
→ bütçe sınırlı model karesi.
**C5 Hızlı kurgu** (Ömer, 5 Eki O15; kanıt: 3. canlı ölçüm b2QkhmQ0sT0 --kare 8 --model-tavan 60 → seçilen 42 · OCR 26 · model 30 ·
incelenmedi 0 · OCR gürültü 62 · ~7k metin + ~13.3k kare; 1:06–1:09 montajında 66/67/68/69/70 sn beşi de modele, ~2k jeton): 5 sn içinde
≥3 sahne kesimi olan küme montaj sayılır; kümeden modele en çok OCR metni (eşitse en yüksek sahne skoru) taşıyan en fazla 2 kare gider,
diğerleri "tekrar (montaj)" sayılır. Test.

## D — İZ TABLOSU (hiçbir şey kaçmasın)
**D1** Her video raporunda "## İz": her bahis bir satır — kaynak (konuşma mm:ss · kare mm:ss · açıklama · yorum · linkli sayfa) · ne ·
bağlandığı aday ya da "aday değil: <sebep>" · kanıt. Sabit sebep listesi: genel kavram · başka adayın parçası (hangisi) · sponsor/reklam ·
konu dışı. "Zaten kurulu" aday değil sebebi DEĞİLDİR: kurulu araç da aday olarak karşılaştırılır (29 Eyl ilkesi). Test (rapor-denetle
sabit liste dışı sebebi ve "zaten kurulu"yu reddeder).
D1 (a) (Ömer kararı, 4 Eki O14): "## İz" yalnız yeni şemada zorunlu — rapor künyesine şema sürümü eklenir ("şema 2"); rapor-denetle İz'i
şema ≥2 raporlarda zorunlu tutar (satırsız tablo da eksik); şemasız eski raporlar ve eski fikstürler geçerli kalır (eski test değişmez).
D1 (b) motor kısmı (Ömer, 5 Eki O15; D1'in parçası, ertelenmez): parti raporu motor formundan üretir → İz motorda da: parti SISTEM metni +
form şeması "iz" alanı (kaynak · ne · bağlandığı · kanıt; aday değil sebebi sabit listeden) + form doğrulama (eksik/boş İz form_red) +
rapor_md "## İz" bölümünü ve künyeye "şema 2"yi yazar + motor-sema.md güncellenir. Eski formlar geçerli (iz alanı yoksa şema 1 yazılır).
video-tarayici-haiku.md'ye aynı şema satırı. Kırmızı test → kod → commit.
**D2 Çağrısız kaçak denetimi:** altyazı + OCR + linklerden çıkarılan aday benzeri her şey (sözlük = kurulu araçlar + tüm aday dosyaları;
desenler: URL, owner/repo, kurulum komutları, büyük harfli ürün adları) İz'de yoksa "KAÇAN?" işaretlenir. Test.
D2 eki (Ömer, 5 Eki O15): kaçak denetimi <id>/ocr-gurultu.txt'yi de tarar — gürültü satırındaki sözlük/desen eşleşmeleri (kurulu araç
adları, aday adları, kısa adlar dahil) İz'de yoksa "KAÇAN?". Kanıt: canlı gürültü satırlarında "OpenA1", "Open A I", "Meta Stan", "John Kim".
D2 iki ek (Ömer kararı, 5 Eki; D2 kancalamada uygulanır): (a) Sözlük = kurulu araçlar + tüm aday adları +
docs/video-tarama/bilinen-araclar.txt (yeni, kalıcı; ilk içerik: bugüne kadarki bütün aday adları + bilinen marketplace plugin adları;
her parti kapanışında yeni aday adları kendiliğinden eklenir, tekrar eklenmez). (b) İki kademe: engelleyen KAÇAN? = URL · owner/repo ·
kurulum komutu · sözlük eşleşmesi (D3'te parti kapat'ı durdurur). "KAÇAN? (düşük güven)" = cümle başında olmayan, yaygın İngilizce/Türkçe
kelime listesinde (ayarda) olmayan ve kaynaklarda ≥2 kez geçen büyük harfli tek kelime (ör. Cursor, Windsurf) — parti kapat'ı DURDURMAZ,
panel Denetim'de ayrı sayılır ve E1 denetim.md'ye girer. Test: "Cursor" iki kez geçen altyazı → düşük güven; cümle başı "The"/"This" →
hiç; sözlükteki "supabase" → engelleyen. Kanıt (4. canlı ölçüm, C5 sonrası): b2QkhmQ0sT0 --kare 8 --model-tavan 60 → seçilen 42 · OCR 26 ·
model 27 · incelenmedi 0 · OCR gürültü 62 · tekrar (montaj) 3 · ~7k metin + ~11.9k kare.
D2 ayırt edicilik + bağlam kuralı (Ömer kararı, 5 Eki): sözlük eşleşmesi ENGELLEYEN olur eğer (i) ad ayırt ediciyse — tire/rakam/nokta/iç
büyük harf içerir ya da ≥5 harf ve YAYGIN'da değil — YA DA (ii) aynı satırda araç işaretiyle geçiyorsa: önünde/arkasında skill · skills ·
plugin · MCP · CLI · extension · agent · server, "/ad" slash biçimi, "ad-skill"/"ad-mcp" tireli biçim, kurulum komutu ya da owner/repo/URL
içinde. İkisi de yoksa → düşük güven (kaybolmaz, denetim.md'ye girer). YAYGIN genişletilir (design, data, docs, do, review, taste, standup,
debug gibi; ayarda). İç büyük harfli tek kelime (LangGraph, ChatGPT) tek geçişte de düşük güven (≥2 şartı yalnız düz Büyük-harfli kelimeye).
Test: sözlük taste/design/superpowers — "taste skill kurdum" → engelleyen; "good taste" → düşük; "/design" → engelleyen; "design is hard"
→ düşük; "superpowers" yalın → engelleyen; "LangGraph" bir kez → düşük. Kuru koşu önce/sonra: docs/olcumler/d2-kuru.md.
D2 sıkılaştırma (Ömer kararı, 5 Eki): (a) owner/repo ENGELLEYEN yalnız iki taraf ≥2 karakter, ikisinde de harf var ve kalıp DESEN_YASAK'ta
değilse (ayarda: a/b, i/o, and/or, tcp/ip, ui/ux, input/output, w/o, 24/7 …; yasak → hiç); gürültü kaynağından gelen owner/repo her
durumda düşük güven. Test: "A/B" → hiç; "Z/57" (gürültü) → düşük; "affaan-m/everything-claude-code" → engelleyen. (b) URL raporun herhangi
bir bölümünde (Açıklama bağlantıları, Adaylar link sütunu, İz dahil) geçiyorsa kaçak değil; SOSYAL alan adları (ayarda: instagram, tiktok,
x, twitter, threads, bsky.app, linkedin, facebook, youtube, youtu.be, substack, patreon, discord.gg) → düşük güven. Test: raporda geçen URL →
hiç; raporda olmayan instagram profili → düşük; raporda olmayan github.com/x/y → engelleyen. (c) YAYGIN'a "me", "al". Kuru koşu "sonra-2"
(İz'i boş rapor + gerçek Açıklama bağlantıları bölümü olan rapor) d2-kuru.md'ye.
**D3** Panelde "## Denetim": bahis · bağlanan · aday değil (oran) · KAÇAN? sayıları. KAÇAN? > 0 iken `video parti kapat` durur (bağla ya
da sebep yaz). "Aday değil" oranı %5'i aşarsa uyarı. Test.
Ek (Ömer, 4 Eki O7): koruma whisper'ı durdurduğu ve altyazı da olmadığı videoda kapsam "konuşma alınamadı (sebep)" olur; bu durum KAÇAN?
gibi `video parti kapat`ı durdurur — giderilmesi: koşullar uygunken `--paket-yeniden` ile whisper. Test.
D3 eki (Ömer kararı, 5 Eki): eski formlar şema 1 olarak geçerli kalır; ama D1 sonrası açılan bir partide İz'siz (şema 1) rapor üreten
video (ör. kısmi kabul, diskteki eski form) panel Denetim'inde "İz yok" olarak sayılır ve KAÇAN? gibi `video parti kapat`ı durdurur —
giderilmesi: `devam --yeniden-tara` ile o video yeniden taranır. Test.

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
değil"lerin hepsi · "ONARIM BEKLİYOR"ların hepsi · C4 incelenmedi anı kalan videolar (durum.json izleme) · risk puanı en yüksek 5 · tohumlu rastgele 3. Her satırda Desktop'un açacağı TAM URL'ler
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
- Suit (tam ya da video) koşarken hiçbir dosyaya yazma yok (salt okuma serbest); kod suit sırasında değişmek zorunda kalırsa sonuç geçersiz,
  suit yeniden koşulur (Ömer, 4 Eki O7: O6'da suit sırasında kod/plan değişmişti).
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
O1 (4 Eki): plan yazıldı. O2 (4 Eki): A1 ✓ (video 569 yeşil). O3 (4 Eki): A2 ✓ · A3 ✓ (video 573). O4 (4 Eki): A4 ✓ · A5 ✓ (video 581). O5 (4 Eki): A4b ✓ (video 584). O6 (4 Eki): C1 ✓ + koruma (video 591). O7 (4 Eki): C2 ✓ (video 597). O8 (4 Eki): C3 ✓ (video 603). O9 (4 Eki): C4 ✓ + ek (video 607). O10 (4 Eki): C4/C3 düzeltmesi 3 madde ✓ (video 611). Sonraki: D1. O11 (4 Eki): O11 madde 1–2 ✓ (video 613), sonraki O11 (3) tekrar ayıklama, (4) ocr-gurultu.txt, sonra D1. O12 (4 Eki): O11 (3) ✓ · (4) ✓ (video 615), sonraki O11 (5), sonra D1.
