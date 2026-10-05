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
- Sayaç hook'la tutulur (KÜÇÜK-2); elle satır yazılmaz.
- ONAY KURALI (Ömer, 4 Eki): "Ömer onayı" etiketi yalnız Ömer'in o değişikliği açıkça onayladığı commit'e yazılır; eski testi
  değiştirmek gerekirse önce DUR, sor. (O12'deki KOD2 değişikliği — test_c3/test_c4, aynı OCR metni tek kare — sonradan onaylandı.)
- Dalga içinde model çağrısı YOK (claude -p 0); canlı koşuları (parti, video indirme, model çağrısı) Ömer yapar; testler sahte veriyle.
- Okuma: dosya içeriği yalnız Read ile dar aralık (~20 satır); konum için Grep -n. PYTHONIOENCODING=utf-8. Yazma Write/Edit.
- Ters eğik çizgi içeren metin (Windows yolu, regex, kaçış) Bash heredoc/sed ile yazılmaz; Edit/Write aracı kullanılır
  (Ömer kararı 5 Eki; tuzak en az 3 kez yaşandı).
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
O19 sapması (Ömer kararı, 5 Eki): kapsam etiketi "altyazı yok; whisper atlandı (…)" olarak kalır; Denetim "konuşma alınamadı"yı ondan
türetir; test_c1.py:79 değişmez.
D3 eki (Ömer kararı, 5 Eki): eski formlar şema 1 olarak geçerli kalır; ama D1 sonrası açılan bir partide İz'siz (şema 1) rapor üreten
video (ör. kısmi kabul, diskteki eski form) panel Denetim'inde "İz yok" olarak sayılır ve KAÇAN? gibi `video parti kapat`ı durdurur —
giderilmesi: `devam --yeniden-tara` ile o video yeniden taranır. Test.

## B — İNTERNETİ TARAMA (yalnız GitHub değil)
**B1 Link toplama:** açıklama + yorum + OCR + altyazıda geçen URL/alan adları + linkli sayfalardaki ilgili linkler (1 derinlik). Sınıf:
github · gist · doküman · blog · ürün/marketplace · video · sosyal · diğer. Aynı URL bütün partilerde bir kez okunur (önbellek). Test.
**B2** Her link açılır (Agent Reach / Jina Reader), gövde temizlenir; araştırıcıya yalnız aday adlarının ve kurulum/ayar/sınırlama
kelimelerinin geçtiği pencereler gider. Erişilemeyen "erişilemedi (sebep)". Sayfadan yeni araç çıkarsa yeni aday + İz satırı. Test (sahte okuyucu).
B ek (Ömer kararı, 5 Eki): baglantilar.json'daki "video" sınıfı linkler (açıklama/yorum/sayfa) kuyrukta yoksa kuyruğa "bağlantılı video
(<kaynak video id>)" notuyla eklenir; kanalı otomatik takibe ALINMAZ (A3 yalnız Ömer'in gönderdiği videolar için); kuyrukta (her durumda)
varsa tekrar eklenmez. Kanıt: canlı B1 (b2QkhmQ0sT0) açıklamasında 2 youtu.be linki açılmıyor. Uygulama: `paket --kuyruk <md>` (parti verir;
tek video -J ile süre/başlık); paket'e --kuyruk verilmezse kuyruğa dokunulmaz. Test.
B2 erişilemedi (Ömer kararı, 5 Eki O21 — test_paket.py:54 değişmez): "## Bağlantılı sayfalar" paket.md'de yalnız derinlik-1'de yeni bağlantı
varsa yazılır; erişilemeyen sayfa paket.md'ye YAZILMAZ — baglantilar.json'da kalır, kapsam.json'a "erisilemedi": [[url, sebep]] (izleme
satırı değişmez). Panel ## Denetim: "erişilemedi N" + "- erişilemedi: <video> · <url> (sebep)"; parti kapat'ı DURDURMAZ. Test.
B ek düzeltmesi (Ömer kararı, 5 Eki): kaynak video başına bölüm AÇILMAZ — kuyrukta tek "## Bağlantılı videolar", kaynak not sütununda
(`tr.kuyruk_ekle`: aynı başlık varsa satırlar o bölümün sonuna); eski "## Bağlantılı videolar (b2QkhmQ0sT0)" bu başlığa taşındı.
`parti baslat` (kuyruk_parti) bu bölümün bekliyor satırlarını seçer (test_b2). Canlı B2 kanıtı (Ömer, 5 Eki): b2QkhmQ0sT0 → erisilemedi []
· substack sayfasından ilgili link 0 · kuyruğa 2 bağlantılı video (nQFtsehu7h0, mZzhfPle9QU).
**B3 Yapımcı nasıl yaptı (aday başına):** README + docs + CHANGELOG/sürüm notları + en çok tepki alan açık ve kapalı issue/discussion
başlıkları (gh api, en fazla N, ayarda) + yazarın duyuru/blog yazısı. Bilinen hata, sınırlama, şikâyet → A5 kötü yanı; yazarın önerdiği
ayar/çözüm → A5 onarımı (kaynak linkiyle). Test (sahte gh). Uygulama (O23): `getir.yapimci` on.md'ye "## Yapımcı nasıl yaptı" (sürüm notu · tepkiye göre açık/kapalı issue · discussion; en fazla N `getir.YAPIMCI`) — README/ağaç zaten `getir.repo`da; gh hatası (kota dahil) adayı düşürmez → kapsam.json erisilemedi (tekrar yok). Sapma: yazarın blog/duyurusu B4 web aramasına kaldı; discussion sıralaması canlıda doğrulanacak. Canlı doğrulama (ücretsiz, en fazla 3): `gh api "repos/anthropics/claude-code/releases?per_page=3" --jq ".[].tag_name"` · `gh api -X GET search/issues -f "q=repo:anthropics/claude-code is:issue is:open" -f sort=reactions -f per_page=5 --jq ".items[].title"` · `gh api graphql -f 'query=query{search(query:"repo:anthropics/claude-code sort:reactions",type:DISCUSSION,first:5){nodes{... on Discussion{title url}}}}'`.
Canlı B3 kanıtı (Ömer, 5 Eki): releases → v2.1.289/288/287 · search/issues sort=reactions → 2097, 1035, 1028, 893, 822 (azalan) · graphql
DISCUSSION "sort:reactions" (vercel/next.js) → 1304, 998, 954, 899, 840 (azalan; kodda ek sıralama gerekmez).
B3 eki (Ömer kararı, 5 Eki): gh arama uçları (search/issues, graphql search) dakikada 30 istekle sınırlı; çok adaylı partide aşılır.
Arama çağrıları arası ≥2.1 sn (`getir.ARAMA["aralik"]`); oran sınırı yanıtında (403/429 · secondary rate limit) Retry-After /
X-RateLimit-Reset kadar BİR kez bekle (üst sınır `ARAMA["bekle_ust"]` ≤60 sn; başlık yoksa üst sınır) ve BİR kez yeniden dene; yine
olmazsa erisilemedi (mevcut davranış). Başlıklar için arama çağrısı `gh api -i`. Uyku/saat enjekte (`getir.uyku`/`getir.saat`), testte
sahte (conftest no-op uyku). Test (test_b3_oran): 1. çağrı sınır → bekleme + ikinci deneme başarılı · iki kez sınır → erisilemedi ·
ardışık 3 arama arası ≥2.1 · releases beklemez.
**B4 Genel web araması** (aday başına en fazla N sorgu, ayarda; mevcut arama yolu = Agent Reach): inceleme, karşılaştırma, alternatif,
bilinen sorun. Forum/sosyal kaynaklar "düşük güven" etiketli. Test.
Uygulama (O24): `getir.web_ara` → on.md "## Web araması"; `mcporter call exa.web_search_exa` (Agent Reach yolu, anahtarsız), sorgular
`getir.SORGU` (inceleme · karşılaştırma · bilinen sorun · alternatif · yazarın duyuru/blog — B3'ten kalan), en fazla `WEB["sorgu"]`=5 ·
`WEB["sonuc"]`=3; web istekleri arası ≥2 sn; aynı URL bir kez; forum/sosyal (`DUSUK` = KACAN_SOSYAL + reddit/HN/SO/SE/lobsters, "forum"
alan adı) "düşük güven"; sorgu hatası → kapsam.json erisilemedi ["web: <sorgu>", sebep]. Yalnız `video on` (cli `web=True`) arar.
Çıktı biçimi (JSON results/content ya da "Title:/URL:" metni) canlıda doğrulanacak. Canlı doğrulama (ücretsiz, PowerShell 5.1, en fazla 3):
`mcporter call exa.web_search_exa query="graphify review" numResults=3` (biçim) ·
`gh api -i -X GET search/issues -f "q=repo:anthropics/claude-code is:issue is:open" -f sort=reactions -f per_page=1` (ilk satır HTTP/…, X-Ratelimit-Limit: 30) ·
`gh api -i graphql -f 'query=query{search(query:\"repo:vercel/next.js sort:reactions\",type:DISCUSSION,first:1){nodes{... on Discussion{title}}}}'` (başlık + boş satır + JSON).
Canlı B4 kanıtı (Ömer, 5 Eki): `mcporter.cmd call exa.web_search_exa` → metin biçimi "Title: / URL: / Published: / Author: / Highlights:"
(sonuçlar "---" ile ayrık) · search/issues -i → "HTTP/2.0 200 OK", X-Ratelimit-Limit 30, Resource search · graphql -i → X-Ratelimit-Limit
5000, Resource graphql (arama 30/dk sınırında değil; 2.1 sn aralık zararsız, kalır). PowerShell'de mcporter.ps1 kısıtlı politikada
çalışmaz → canlı komutlarda `mcporter.cmd`.
B4 düzeltmeleri (Ömer kararı, 5 Eki): (a) Highlights korunur: satır = sorgu · başlık · tarih (Published, yalnız gün) · url (+ düşük güven),
altında "  > " ile Highlights'tan ilk `WEB["ozet"]`=600 karakter (boşluklar sadeleşir, "..." ayraçları tek boşluk). (b) Sorgu belirsizliği:
repo biliniyorsa "{owner}/{repo} …", bilinmiyorsa "{ad} {tür} …" (tür = `video on --tur`, aday dosyasının tur alanı). (c) gh -i başlık/gövde
ayrımı CRLF'e dayanıklı (oran sınırı başlıkları dahil) — mevcut kod zaten dayanıklıydı (CRLF→LF), test kilit olarak eklendi (kırmızı görülmedi).
(d) `video on` → web=True ile web_ara (tür geçer). Test (test_b4). Canlı doğrulama (ücretsiz, PowerShell 5.1, en fazla 3):
`cd tools/video; python -c "from video import getir as g, cli; import json; print(list(json.loads(chr(10).join(g._gh_ara(cli.kos, 'search/issues', '-X', 'GET', '-f', 'q=repo:anthropics/claude-code is:issue', '-f', 'per_page=1')))))"`
(CRLF kanıtı: gövde JSON okunur → anahtarlar) · `mcporter.cmd call exa.web_search_exa query="safishamsi/graphify review" numResults=2` (Published/Highlights).
B4 eki (Ömer kararı, 5 Eki; kanıt: canlı exa → "You've hit Exa's free MCP rate limit…" düz metni, Title/URL yok): (a) sessiz boş YASAK —
exa çıktısında sonuç yok ve düz metin boş değilse (oran sınırı/hata/anahtar mesajı) hata sayılır; JSON boş sonuç ("[]", results/content
boş, boş çıktı) hata değildir. (b) sağlayıcı zinciri exa → Brave Search REST → erisilemedi. Brave (resmi belge, api-dashboard.search.brave.com:
GET api.search.brave.com/res/v1/web/search, başlık X-Subscription-Token, q · count ≤20 · extra_snippets=true · text_decorations=false;
yanıt web.results[] title/url/description/extra_snippets; page_age biçimi belgede yok → yalnız YYYY-MM-DD ise gün) BRAVE_API_KEY ortamdaysa,
istekler arası ≥`WEB["brave_aralik"]`=1 sn. Satırda sağlayıcı sorgudan sonra ("- sorgu · exa · …" / "· brave · …"); brave'de Highlights
yerine açıklama + ek parçacıklar aynı 600 kuralıyla (HTML etiketi ayıklanır). Anahtar yoksa brave atlanır, sebep erisilemedi'de birleşik:
"<exa sebebi> · brave: <sebep>" (test_b4:61 beklentisi buna göre — Ömer onayı, 5 Eki). Testler sahte urllib + kos.
Canlı doğrulama (PowerShell 5.1; python = video aracının uv ortamı; PS 5.1 iç çift tırnağı sildiği için kod yalnız tek tırnak, '' kaçışlı;
ağsız kısım O26'da denendi): `$py = "$(uv tool dir)\video-cli\Scripts\python.exe"` ·
`& $py -c 'import json; from video import getir as g, cli; print(list(json.loads(chr(10).join(g._gh_ara(cli.kos, ''search/issues'', ''-X'', ''GET'', ''-f'', ''q=repo:anthropics/claude-code is:issue'', ''-f'', ''per_page=1'')))))'`
(CRLF kanıtı: gövde anahtarları) · `& $py -c 'from video import getir as g; g.WEB[''sorgu'']=1; h=[]; print(g.web_ara(''graphify'', lambda a: (1, b'''', b''exa atlandi''), h, repo=''safishamsi/graphify'')); print(h)'`
(exa sahte hata → en fazla 1 Brave isteği; beklenen "- safishamsi/graphify review · brave · …" + "  > " satırı, h boş).
Ömer canlı B4 eki doğrulaması (5 Eki): gh -i → gövde JSON ayrıldı (total_count, incomplete_results, items, search_type) · exa sahte hata →
brave 3 sonuç + "  >" özetleri, hata listesi boş. Bulgu: "safishamsi/graphify review" Brave'de 2 sonuçta repo/sürüm sayfası, 1'de SourceForge
aynası getirdi (inceleme 0); exa'da "graphify review" gerçek incelemeler getirmişti.
B4 düzeltmesi-2 (Ömer kararı, 5 Eki; B4 düzeltmeleri (b) kuralı değişir): sorgu konusu her zaman "{ad} {tür}" (tür yoksa yalnız ad); repo
sorguya GİRMEZ, yalnız süzgeç: sonuçlardan repo'nun kendi GitHub sayfaları (github.com/<owner>/<repo> ve alt yolları) ile ayna siteler
(ayar `AYNA`: sourceforge.net/projects/*.mirror, gitee/gitcode aynaları) atılır, yerine sıradaki sonuç alınır (sağlayıcıdan
`WEB["sonuc"]` + `WEB["fazla"]`=3 istenir). test_b4 sorgu/numResults/count beklentileri buna göre (Ömer onayı, 5 Eki; ayrı commit).
Brave aralığı testi (O26 sapması kapandı): `_brave` doğrudan iki kez sahte saatle; ikinci istek ≥`WEB["brave_aralik"]` sonra (aralık kodu
geçici kapatılarak kırmızı görüldü). Canlı doğrulama (ücretsiz, tek Brave isteği; GitHub/ayna satırı beklenmez, h boş):
`& $py -c 'from video import getir as g; g.WEB[''sorgu'']=1; h=[]; print(g.web_ara(''graphify'', lambda a: (1, b'''', b''exa atlandi''), h, repo=''safishamsi/graphify'', tur=''skill'')); print(h)'`
**B5 Mekanizma incelemesi** — "aday değil" dışındaki HER aday (kurulu olanlar dahil; kuruluysa bizdeki kopya): repo seyrek klonlanır (S5
sınırları); graphify --code-only ve grep ile çağrısız konumlandırma: oturum başı enjeksiyon, hook'lar, başlatılan süreçler, ağ çağrıları,
izin kapsamı, ayar okuma noktaları, ağır döngüler. Modele yalnız bulunan ilgili dosyalar gider (aday başına en fazla N KB, ayarda). Aynı
repo + aynı commit bütün partilerde bir kez incelenir (önbellek). Çıktı: her kötü yanın nedeni (dosya:satır) + onarımın nereden yapılacağı
(ayar · sarmalayıcı · kendi sürüm) + iyi yanın nasıl güçleneceği → A5'e. Repo yoksa (servis/ürün) B2–B4 kaynaklarıyla aynı alanlar
doldurulur, "kod yok" yazılır. Test.
B5 aday notu (5 Eki): semgrep (çevrimdışı: --metrics=off --disable-version-check) — ilk canlı partide grep yanlış eşleşmesi yüksekse
geçilir; ölçüm: aday başına yanlış eşleşme sayısı.
B5 Ömer kararı (5 Eki, test_24e.py:37): seçenek (b) — test_24e değişmez; kurulu araçta B5 çıktısı on.md'ye değil
.kos/<video>/<ad>/mekanizma.md'ye yazılır ("ZATEN VAR, araştırıcı yok" akışı aynen, model çağrısı yok). Tüketici: akil.gelistir
(ZATEN VAR karşılaştırması) bu dosyayı <veri kaynak="bizde"> bloğuna ekler (test_gelistir_mekanizma_okur). A6–A8 notu: parti akışında
kurulu aday için `video on` koşmuyor (akil._on yalnız araştırılan + repo'lu adayda) → mekanizma.md parti içinde üretilmez; üretici bağlantısı A6'da.
B5 düzeltmesi (Ömer kararı 5 Eki): KONUM taraması yalnız kod dosyalarında — ayar KOD_UZANTI (.js .mjs .cjs .ts .tsx .py .sh .ps1 .cmd
.bat) + KOD_AD (hooks.json · settings*.json · plugin.json · .mcp.json); .md .txt .rst vb. belge taranmaz (README linkleri "ağ"ın satır
sınırını doldurup koddaki ağ çağrılarını gizliyordu). Yan etki: SKILL.md frontmatter allowed-tools artık konumlanmaz (izin kapsamı
yalnız settings/plugin json). Test: README 30 URL + a.js 1 fetch → ağda yalnız a.js satırı.
B5 canlı doğrulama (ücretsiz, ağsız; zaten klonlu repo, ilk 20 satır):
`& $py -c 'import tempfile; from pathlib import Path; from video import uygula as uy, cli; print(chr(10).join(uy.mekanizma({''kok'': Path(tempfile.gettempdir()), ''kos'': cli.kos}, Path(''C:/Projeler/omer-skills/tools/jev''), ''omer/jev'').splitlines()[:20]))'`
B5 frontmatter düzeltmesi (Ömer kararı 5 Eki; O28 sapma 1 kabul edilmedi): .md dosyalarında YALNIZ baştaki YAML frontmatter (ilk satır
"---" → kapanan "---") taranır, gövde taranmaz; frontmatter'da allowed-tools · tools · permissionMode · disallowedTools → "izin kapsamı",
hooks → "hook" (ayar `FM_KONUM`); satır no dosyadaki gerçek satır. test_b5 "izin kapsamı" beklentisi geri: SKILL.md:2 + .claude/settings.json:1
(Ömer onayı, ayrı commit). Test: agents/x.md "tools: Bash" → izin kapsamı · README gövdesi 30 URL + "allowed-tools" → yok · frontmatter'sız .md taranmaz.
B5 canlı bulgu düzeltmeleri (Ömer canlı ölçümü 5 Eki, tools/jev: "ağ"daki 5 satırın 5'i .venv/_virtualenv.py yorum URL'si; "oturum başı
enjeksiyon"da test satırları): (a) ayar `KOD_DISLA` (.venv venv env node_modules site-packages dist build __pycache__ .tox vendor .git)
klasörlerinin altı taranmaz · (b) "ağ"dan çıplak URL çıkar; yalnız çağrı kalıpları (fetch( · requests. · urllib.request · httpx · aiohttp ·
axios · http(s).get/request · WebSocket · curl/wget komutu) · (c) yorum satırı taranmaz (satır başı # // /* * --); Python docstring: satır
başı """/''' ile başlayan blok atlanır (satır başındaki dize her zaman ifade-dizesi, çalışan kod olamaz → kod gizlemez; x = """ ortası
taranır = fazla rapor, eksik değil) · (d) ayar `TEST_DISLA` (tests/ test/ __tests__/ test_*.py *_test.py *.test.* *.spec.*) taranmaz.
Ölçüm (önce/sonra, gözle yanlış eşleşme): docs/olcumler/b5-grep.md. Karar kuralı: düzeltme sonrası yanlış eşleşme toplamın %20'sini
aşıyorsa sıradaki madde semgrep geçişi (çevrimdışı: --metrics=off --disable-version-check).
Ölçüm sonucu (O29): önce 36 satır / 23 yanlış (%64) → sonra 14 / 4 (%28,6; hepsi kod içi belge/yardım dizesi) → kural tetiklendi:
semgrep geçişi B4 kanonik ad maddesinden sonra, E1'den önce.
B4 bulgusu (Ömer canlı ölçümü 5 Eki): repo taşınmış (safishamsi/graphify → Graphify-Labs/graphify, GitHub yönlendirmesi) → AYNA süzgeci
github.com/Graphify-Labs/graphify'ı kaçırdı. Çözüm: GitHub kanonik adı (gh api repos/{repo} → full_name) da süzgece eklenir; B3'te bu
yanıt alınmıyorsa tek REST çağrısı (arama değil). Test: repo=safishamsi/graphify, kanonik Graphify-Labs/graphify → github.com/Graphify-Labs/graphify atılır.
O30 (yapıldı): gh api repos/{repo} --jq .full_name yalnız ilk sonuç geldiğinde, aday başına bir kez; gh hata ya da owner/repo dışı değer →
süzgeç eski adla. Semgrep geçişi (Ömer kararı 5 Eki, O29 karar kuralı): KONUM kod taraması semgrep'e geçer — kurallar tools/video/semgrep/*.yml,
çevrimdışı (--metrics=off --disable-version-check --json), aynı kategoriler; dize ve yorum eşleşmez. KOD_DISLA/TEST_DISLA → --exclude.
.md frontmatter Python yolunda kalır. Yeni kategori "uç noktalar": kodda tanımlı http(s) adres sabitleri (yorum/belge dizesi değil), satır
sınırı aynı. Semgrep yoksa/hata → grep yolu + bölüme "semgrep yok: <sebep> · grep yolu". Testler sahte semgrep JSON'u (kos); kabul: tools/jev
üzerinde yerel semgrep → b5-grep.md "semgrep" sütunu (satır · yanlış · süre), yanlış < %20; tutmazsa DUR.
O30 varsayımı: semgrep'te dize yalnız tam değer olarak eşleşir (desen "SessionStart" bir yardım cümlesinin içindeki kelimeyi bulmaz) →
belge/yardım dizeleri düşer. O31 kabul (yapıldı): tools/jev 13 satır / 0 yanlış (%0; sınırda 2 yanlış sayılsa %15,4), 5,4 sn → KABUL.
Ölçümde hata bulundu ve düzeltildi: Windows'ta semgrep yml'i cp1252 okur → message bozulur → kategori artık kural kimliğinden (check_id).
B5 sertleştirme (Ömer kararı 5 Eki; ilke "sessiz düşme yasak" — O31'de 14 sonucun 8'i bu yolla kayboldu): semgrep sonucunun kural
kimliği SEMGREP_ID'de yoksa sonuç atılmaz → bölüme "### tanınmayan kural" altında "- <dosya>:<satır> · <check_id>" (yalnız varsa).
Test: bilinmeyen check_id → tanınmayan kural satırı; bilinen → kendi kategorisi.
Canlı doğrulama (O31, ağsız, ücretsiz; PowerShell 5.1; beklenen: "uç noktalar" altında cekirdek.py:19/37/39/41, "ağ" altında 133/135):
`$env:PYTHONIOENCODING = 'utf-8'; $py = "$(uv tool dir)\video-cli\Scripts\python.exe"; & $py -c 'import subprocess as s, tempfile, pathlib as P; from video import uygula as u; k = lambda a, timeout=300: (lambda p: (p.returncode, p.stdout, p.stderr))(s.run(a, capture_output=True)); print(u.mekanizma({''kos'': k, ''kok'': P.Path(tempfile.mkdtemp())}, P.Path(''C:/Projeler/omer-skills/tools/jev''), ''o/jev''))'`

## E — DESKTOP İKİNCİ BAKIŞ (hedefli, uyarlamalı)
**E1 Çağrısız risk puanı** (bahis/aday başına): KUR önerisi · güvenlik bulgusu · fork/kaynak farkı · kapsam eksikleri · "çözülmedi" kötü
yan · "aday değil" · KAÇAN? · yeni link sınıfı. `docs/kurulumlar/parti/<id>/denetim.md` (≤150 satır): KAÇAN?'ların hepsi · "aday
değil"lerin hepsi · "ONARIM BEKLİYOR"ların hepsi · C4 incelenmedi anı kalan videolar (durum.json izleme) · risk puanı en yüksek 5 · tohumlu rastgele 3. Her satırda Desktop'un açacağı TAM URL'ler
(videonun mm:ss linki, repo, ilgili dosya, issue, doküman) — Desktop yalnız sohbette görünen adresleri açabilir. Test.
E1 uygulama (O32): `panel` panel.md'nin yanına denetim.md yazar (akil.denetim_md; tek kaynak akil.denetim + panel kararları).
Risk puanı = sinyal sayısı: KUR önerisi (T1/T2/UYARLA) · güvenlik (HIGH/CRITICAL) · kaynak farkı (a.kaynak) · kapsam eksiği · çözülmedi
(ONARIM BEKLİYOR); eşitlikte ad sırası. "aday değil"/KAÇAN? video düzeyinde (aday puanına girmez, zaten hepsi listelenir); "yeni link
sınıfı" sinyali B1 sınıfı aday kaydında yok → şimdilik yok. Rastgele 3: random.Random(parti id), ilk 5 ve ONARIM dışındaki adaylardan.
URL: https://www.youtube.com/watch?v=<id>&t=<sn>s (İz kaynak hücresindeki mm:ss · aday videolar.zaman · kapsam.json incelenmedi ilk an)
+ https://github.com/<repo>. kur.py:368 ONARIM BEKLİYOR parti dışı (token takas tablosu) → denetim.md'ye girmez. >150 satır → kesilir + sayı.
E1 eki (Ömer, O33; D1 (a) ile tutarlı): akil.denetim KAÇAN?/düşük güven denetimini yalnız künyesinde şema ≥2 olan raporda yapar; eski
şemada denetim.md KAÇAN? altına "eski şema: <v> · İz yok, KAÇAN? denetimi yapılmadı" (kapat'ı durdurmaz; İz yok kuralı IZ_TARIH ile aynen).
Canlı kanıt (2026-10-03-short): önce her link/araç adı KAÇAN? (kapat kilitli) → sonra 8 "eski şema" satırı, KAÇAN? 0. Doğrulama (ağsız, model 0;
panel.md bayt yedeği geri yazılır): `$py = "$(uv tool dir)\video-cli\Scripts\python.exe"; & $py -c 'import json; from pathlib import Path as P;
from video import akil as a, cli, uygula as u; p=P(''.kos/2026-10-03-short''); d=json.loads((p/''durum.json'').read_text(encoding=''utf-8''));
m=P(u.KOK)/''docs/kurulumlar/parti''/d[''parti'']/''panel.md''; y=m.read_bytes(); a.panel(p,d,u.KOK,cli.KOK); m.write_bytes(y)'` (tek satır, repo kökünde).
**E2 Geri dönüş:** denetim.md sonunda "## Desktop" şablonu; Ömer Desktop'un verdiği satırları buraya yapıştırır; `video parti
denetim-isle <id>` bunları `docs/kurulumlar/desktop-denetim.jsonl`'a ve ilgili aday dosyasına işler. Test.
E2 satır biçimi (Ömer kararı 5 Eki): şablon satırı örnekle gösterir — tek satır, " · " ayraçlı: `- <aday ya da video id> · <tür> · <kanıt
URL> · <açıklama>`; tür sabit listeden (ayar akil.DESKTOP_TUR): KAÇAN-doğru · KAÇAN-yanlış · aday-değil-itiraz · kötü-yan · onarım ·
güçlendirme · not. Okuyucu hoşgörülü: baş/son boşluk, baştaki "- " isteğe bağlı, büyük/küçük harf, tür adında Türkçe/ASCII farkı
(kotu-yan = kötü-yan). jsonl kaydı: tarih · parti · aday · tur · url · aciklama · satir; aday dosyasında "## Desktop denetimi" altına
"- <tarih> · <parti> · <tür> · <url> · <açıklama>" (video id ise yalnız jsonl). Sessiz düşme yasak: okunamayan satır (ayraçsız/eksik alan ·
bilinmeyen tür · parti'de olmayan aday/video) → çıktıda ve jsonl'de "okunamadı: <satır> (<sebep>)", çıkış kodu 1; aynı (parti, satır) jsonl'de
varsa ikinci kez işlenmez. Şablon satırları (sabit) atlanır; panel denetim.md'yi yeniden yazarken ## Desktop altındaki satırlar korunur.
Tavan: üretilen kısım şablonla birlikte ≤150 (kesildi notu en son satır, okuyucu atlar); Ömer'in Desktop satırları kesilmez.
Canlı doğrulama (O34, ağsız, model 0; önce E1 komutuyla denetim.md'yi yeniden üret; denetim.md + jsonl bayt yedeği geri yazılır; beklenen
"1 işlendi · 1 okunamadı", rc=1): `$py = "$(uv tool dir)\video-cli\Scripts\python.exe"; $m = 'docs\kurulumlar\parti\2026-10-03-short\denetim.md';
$j = 'docs\kurulumlar\desktop-denetim.jsonl'; $y = [IO.File]::ReadAllBytes((Resolve-Path $m)); $jy = $null; if (Test-Path $j) { $jy =
[IO.File]::ReadAllBytes((Resolve-Path $j)) }; Add-Content -Encoding utf8 $m '- rABIViSQmsc · not · https://www.youtube.com/watch?v=rABIViSQmsc
· E2 deneme'; Add-Content -Encoding utf8 $m 'rABIViSQmsc ayraçsız satır'; & $py -c 'import sys; from video import cli;
sys.exit(cli.main([''parti'', ''denetim-isle'', ''2026-10-03-short'']))'; Write-Output ('rc=' + $LASTEXITCODE); Get-Content -Encoding utf8 $j;
[IO.File]::WriteAllBytes((Resolve-Path $m), $y); if ($jy) { [IO.File]::WriteAllBytes((Resolve-Path $j), $jy) } else { Remove-Item $j }` (tek satır).
**E3 Uyarlamalı örneklem:** son 3 partide Desktop bulgusu 0 ise rastgele 3 → 1; her bulgu +3 (en fazla 6). KAÇAN?, "aday değil", "ONARIM
BEKLİYOR" ve risk puanı en yüksek 5 her zaman kalır. Test.
E3 bulgu tanımı (Ömer kararı 5 Eki; örneklemin amacı uyarı taşımayan adaylardaki gizli sorunu ölçmek): bulgu = desktop-denetim.jsonl'de,
o partinin denetim.md "Rastgele" bölümündeki adaya yazılmış ve türü kötü-yan · onarım · güçlendirme · aday-değil-itiraz olan satır ("not",
"KAÇAN-yanlış", "KAÇAN-doğru" ve okunamadı kayıtları sayılmaz; KAÇAN/risk/ONARIM bölümlerindeki adaylara yazılanlar sayılmaz). denetim-isle
kaydına "bolum" alanı (adayın denetim.md'de ilk göründüğü "## " başlığı); alanı olmayan eski kayıt bulgu sayılmaz. Boy (akil.orneklem):
geçmiş = jsonl'deki diğer partiler, dosya sırasıyla; son 3 partide bulgu 0 → 1 (3 parti şart; 1-2 bulgusuz parti → 3); aksi halde
min(6, 3 + 3 × son partideki bulgu); geçmiş yok → 3. Hiç Desktop satırı yazılmamış parti jsonl'de görünmez, geçmişe girmez.
Canlı doğrulama (O35, ağsız, model 0; E1 ile denetim.md yeniden üretilir, Rastgele'deki ilk adaya kotu-yan yazılır; denetim.md + jsonl bayt
yedeği geri yazılır; beklenen "1 işlendi · 0 okunamadı" · "boy 6" · jsonl'de "bolum":"Rastgele 3 (tohum 2026-10-03-short)"): `$py = "$(uv tool dir)\video-cli\Scripts\python.exe";
$m = 'docs\kurulumlar\parti\2026-10-03-short\denetim.md'; $j = 'docs\kurulumlar\desktop-denetim.jsonl'; $y = [IO.File]::ReadAllBytes((Resolve-Path $m)); $jy = $null;
if (Test-Path $j) { $jy = [IO.File]::ReadAllBytes((Resolve-Path $j)) }; & $py -c '<E1 komutundaki python>'; $r = (Select-String -Path $m -Pattern
'^## Rastgele' -Context 0,1).Context.PostContext[0].Split(' ')[1]; Add-Content -Encoding utf8 $m ('- ' + $r + ' · kotu-yan · https://github.com · E3 deneme');
& $py -c 'import sys; from video import cli; sys.exit(cli.main([''parti'', ''denetim-isle'', ''2026-10-03-short'']))'; & $py -c 'from video import akil
as a, uygula as u; print(''boy'', a.orneklem(u.KOK, ''yeni''))'; Get-Content -Encoding utf8 $j; [IO.File]::WriteAllBytes((Resolve-Path $m), $y); if ($jy)
{ [IO.File]::WriteAllBytes((Resolve-Path $j), $jy) } else { Remove-Item $j }` (tek satır, repo kökünde).

## F — UCUZ ÇALIŞTIRMA (yalnız hattın arka plan model çağrıları; CC etkileşimli yönlendirme TOKEN-5'te)
**F1 Model yönlendirme adaptörü:** hattın model çağıran her adımı (tarama, araştırma, mekanizma, karşılaştırma, özet) için ayarda
sağlayıcı/model seçimi; varsayılan bugünkü gibi, DEĞİŞMEZ. Hedef OmniRoute (kurulu omni-* skill'leri; sunucu çalışıyor mu, kimlik bilgisi
var mı salt okunur kontrol — değer basılmaz, boolean; yoksa DUR, sor) ve videolarda geçen benzeri yönlendiriciler. Test (sahte sağlayıcı).
F1 kararı (Ömer, O35; ön kontrol: omniroute komutu var · 20128 dinlemiyor · kimlik env yok): adaptör sahte sağlayıcıyla yazılır; uç nokta,
istek/yanıt biçimi ve kimlik başlığı tahmin edilmez, kurulu omni-inference ve omni-auth skill belgelerinden doğrulanır (dosya:satır plana);
testteki sahte sağlayıcı o biçimi taklit eder. Gerçek bağlantı doğrulaması F1-KURULUM'dan sonra.
F1 biçim kanıtı (O35, okundu, kod yok; skill'ler MIT): omni-auth SKILL.md:54-58 OMNIROUTE_URL (varsayılan http://localhost:20128) +
OMNIROUTE_KEY, "Authorization: Bearer"; omni-inference SKILL.md:283-285 POST /v1/chat/completions (OpenAI) · /v1/messages (Anthropic);
istek :298-305 {"model","messages":[{"role","content"}]}; model adı önekli değil (:302), geçersiz → 400 invalid_model (:337). Sohbet YANITI
skill'lerde yok → yerel paket npm-global omniroute/dist/docs/openapi.yaml:9031 ChatCompletionResponse: choices[].message.content ·
usage.prompt_tokens/completion_tokens/total_tokens; :22 server localhost:20128; :1156 yol /api/v1/chat/completions (skill'deki /v1/… ile
ÇELİŞKİ → adaptör yolu ayar sabiti, F1-KURULUM'da canlı çağrıyla hangisi doğru belirlenir). Tasarım: OpenAI biçimi (yanıt şeması
belgeli olan); hafif.cagir imzalı adaptör, ikinci_goz.or_cagir kalıbı (gonder= enjekte, aynı dict: form/usage/usd/sure/hata); seçim
durum.json d["model"] yanında adım başı alan, varsayılan bugünkü (hafif.MODEL, claude -p). Sahte: test_24e1.py:55 __call__(url, basliklar, govde).
F1 yeşil (O36): video/yonlendir.py — omni_cagir (OMNI_URL ← env OMNIROUTE_URL, OMNI_YOL sabiti; /api/v1/chat/completions adayı F1-KURULUM'da) ·
sec(d, adim, …): durum.json "yonlendirme": {"<adim>": {"saglayici": "omniroute", "model": "…"}} (elle yazılır; CLI bayrağı yok); bağlı adımlar
parti "tarama" + akil._form_al adim adları; ikinci göz yargıcı yönlendirilmez. usd 0 (yanıtta maliyet yok → tavan yalnız çağrı sayısıyla).
ig._post HTTPError gövdesini korur (400 invalid_model sebebi). Canlı doğrulama (ağsız, ücretsiz; PowerShell 5.1):
  `$py = "$(uv tool dir)\video-cli\Scripts\python.exe"; & $py -c 'from video import yonlendir as y; print(y.sec({''model'': ''claude-sonnet-5-5''}, ''tarama'', ''hafif.cagir'', {}))'` → ('hafif.cagir', 'claude-sonnet-5-5')
  `& $py -c 'from video import yonlendir as y; print(y.OMNI_YOL, y.omni_cagir(''gpt-4o-mini'', {''OMNIROUTE_URL'': ''http://127.0.0.1:9''})(''s'', ''m'', {})[''hata''])'` → /v1/chat/completions ölçülemedi: URLError … 10061
**F1 eki — maliyet (Ömer, 5 Eki; O36 "usd 0" sapması F2'yi geçersiz kılardı):** yonlendir.FIYAT = {model: {"girdi": $/1M, "cikti": $/1M,
"kaynak": "<url · tarih>"}} boş başlar, değer tahmin edilmez (F1-KURULUM'da sağlayıcı sayfasından). Öncelik: yanıt başlığı
X-OmniRoute-Response-Cost (openapi.yaml:1173-1176, USD 10 ondalık) > 0 ise o; "0.0000000000" belgede "free/unpriced" (ayırt edilemez) →
usage × FIYAT; model FIYAT'ta yoksa usd None (0 değil). Defter satırı usd null + "maliyet": "bilinmiyor" (parti._maliyet; akil._form_al +
parti tarama); _defter toplamı None'u $ tavanına katmaz → o adım yalnız çağrı tavanıyla sınırlanır; panel Denetim: "- maliyet bilinmiyor:
<adım> · <model>" (tekil). ig._post(basliklar=True) yanıt başlıklarını döner (or_cagir değişmez). test_f1:47 usd 0.0 → None (Ömer kararı).
O37: kırmızı b06c38b · yeşil (mutasyon: başlık >0→>=0 ve None→0.0 kırmızı).
test_f1.py:47 usd 0.0 → None — Ömer onayı (sonradan, 5 Eki; F1 eki kararının doğrudan sonucu).
**F1-KURULUM (ayrı kurulum maddesi; iş oturumuna karışmaz):** OmniRoute sunucusunu kur + başlat, kimliği ekle (değer basılmaz); sonra
F1 adaptörüyle tek gerçek çağrı (tavan: en fazla 1 istek, en ucuz model) → sonuç plana.
F1-KURULUM yarım (5 Eki; sayaç 40/45'te durdu, gerçek çağrı 0, $0): OmniRoute 3.8.50 (npm-global) · `omniroute serve --daemon` 20128 ·
~/.omniroute/.env'e OMNIROUTE_SERVER_HOST=127.0.0.1 (ilk açılış 0.0.0.0 + anahtarsız uyarısı verdi) + REQUIRE_API_KEY=true · OpenRouter
sağlayıcısı `providers add openrouter --credential-env OPENROUTER_API_KEY` (bağlantı f7b8f5c3…) · yerel anahtar POST /api/keys (CLI token
başlığı; CLI'da "keys create" yok) id c9b6c9a1… → HKCU OMNIROUTE_KEY (stdin, değer basılmadı; var=True); OMNIROUTE_URL varsayılan, yazılmadı ·
bütçe: 3.8.50'de global bütçe YOK (`usage budget set --scope global` → 400 apiKeyId zorunlu; setBudgetSchema anahtar başı) → bu anahtara
aylık $5 (POST /api/usage/budget monthlyLimitUsd 5); REQUIRE_API_KEY ile anahtarsız /v1 isteği 401, fiilen tek kapı · otomatik başlatma
`omniroute autostart enable` → true (vbs-startup) · ücretsiz GET /api/v1/models: anahtarla 200 (1723 model), anahtarsız 401 → liste yolu
/api/v1/… kesin. KALAN (F1-KURULUM-2, yeni oturum): sohbet yolu tek gerçek çağrıyla · FIYAT (≤5 model, OpenRouter /api/v1/models fiyatı) ·
X-OmniRoute-Response-Cost · ikinci göz durum kontrolü · gitleaks/suite.
F1-KURULUM ✓ (F1-KURULUM-2, 5 Eki; gerçek çağrı 1, ≈$0.0000008): sohbet yolu OMNI_YOL /v1/chat/completions → 200 (404 yok, /api/v1/…
denenmedi; OMNI_YOL değişmedi) · model id OmniRoute'ta önekli: "openrouter/mistralai/mistral-nemo" · FIYAT = OpenRouter
https://openrouter.ai/api/v1/models (anahtarsız, 5 Eki) json_schema (structured_outputs) destekli en ucuz 5 ücretli model, $/1M girdi/çıktı:
mistral-nemo 0.019/0.03 · ling-3.0-flash-vl 0.021/0.0616 · l3-lunaris-8b 0.04/0.05 · gpt-oss-20b 0.018/0.09 · nex-n2.5-mini 0.025/0.1
(varsayım: :free/0 fiyatlı modeller dışarıda — maliyet yolu sınanacağı için) · çağrı: form {"renk": "mavi"} · usage 27/9 token ·
X-OmniRoute-Response-Cost GELDİ ama "0.0000000000" (fiyatsız) → usd FIYAT'tan 7.83e-7 · OmniRoute günlüğü (`omniroute usage logs`;
GET /api/usage/call-logs API anahtarıyla 403): openrouter · mistralai/mistral-nemo · 200 · Tokens 0 · Cost boş → OmniRoute bu modeli
fiyatlamıyor; maliyetin tek kaynağı FIYAT (F1 eki kararı doğrulandı) · ikinci göz: OPENROUTER_API_KEY süreçte var → ikinci_goz_kapali None
(KAPALI kalkar; çağrısız doğrulandı) · gitleaks temiz.
**F2 Adım bazlı A/B düzeneği:** aynı girdi, iki model; kalite (kör puan + görev başarısı) + $; karar A1'le düzeltilmiş 24 Eyl tablosuyla.
Yalnız AL çıkan adım yönlendirilir. Test.
F2 yeşil (O38): yon.ab(d, adim, girdiler, kol_b, cagir, env, puanla, *, basari=None, tekrar=2, tavan) — A = sec(d, adim), B = kol_b;
puanla kör ("GÖREV: … YANIT: <form json>", model adı yok); başarı = hata yok + şema required anahtarları (ponytail: tam JSON Schema değil);
gürültü = A tekrar puan farkı (max); karar kur.karar(A, B, None, gürültü, görev başarı çiftleri); usd None kol → "SOR (maliyet bilinmiyor:
<model>)"; 2×tekrar×girdi > tavan → "TAVAN n > tavan", çağrı yok; yonlendirme {adim: kol_b} yalnız AL'de (durum.json'a yazmaz; elle).
O38: kırmızı 955e336 · yeşil (758 passed; mutasyon: usd None kapısı ve AL kapısı kaldırılınca 2 kırmızı).
F2 düzeltmesi O39: kırmızı f1b72a0 · yeşil (761 passed; mutasyon: başarı → isinstance dict iken 3 kırmızı).
**F2 düzeltmesi (Ömer, 5 Eki; O38 "yalnız required" sapması kabul edilmedi — tip/enum hatalı yanıt başarılı sayılıp A/B'yi haksız AL'e
iterdi):** görev başarısı = hata yok + hattın kendi form doğrulaması parti._denet (akil.py:604'ün reddettiğini reddeden aynı fonksiyon;
yeni bağımlılık yok); _sema_gecer kalkar. Testler: required tamam ama tip yanlış → 0 · enum dışı → 0 · geçerli form → 1.
**F3** Ömer'in koşacağı canlı A/B komutu + tavan (en fazla N çağrı) raporda.
F3 (O39): komut docs/video-tarama/ab-canli.ps1 (PowerShell 5.1; Python here-string → `& $py -`, yalnız ASCII) — adım "tarama", A = hafif
(claude -p, hafif.MODEL), B = omniroute AB_MODEL; girdi = 1 paket.md (AB_VIDEO + AB_PAKET), tekrar 2; puan Jev KALITE_Q (kör).
**YALNIZ F1-KURULUM'DAN SONRA koşulur** (sunucu + kimlik + FIYAT/maliyet başlığı; FIYAT boşken B usd None → karar "SOR", AL çıkmaz).
Tavan: en fazla 4 model çağrısı (AB_TAVAN=4: 2 claude -p, hafif butce $0.50/çağrı → ≤ $1.00; 2 OmniRoute, $ FIYAT'tan) + Jev en fazla
4 HTTP isteği (istek_tavan=4). Kalan risk: OmniRoute düşükse A'nın 2 çağrısı harcanır, B başarı 0 → AL değil (≤ $1.00 boşa).
Ağsız deneme (O39): ayar yok → "hata: eksik ayar: AB_VIDEO, AB_PAKET, AB_MODEL" exit 1 · paket yok → "hata: paket yok: …" exit 1 ·
AB_TAVAN=3 → {"karar":"TAVAN 4 > 3"}, çağrı 0. Canlı komut: $env:AB_VIDEO='<id>'; $env:AB_PAKET='<paket.md>'; $env:AB_MODEL='<model>';
& 'C:\Projeler\omer-skills\docs\video-tarama\ab-canli.ps1'
F3 ön kontrol (Ömer kararı 5 Eki; O39 "kalan risk" kapanır): betik model çağrısından ÖNCE yon.omni_yokla(AB_MODEL, env) — ücretsiz
GET /api/v1/models (openapi.yaml:1681, BearerAuth; data[].id, Model şeması :9091); sunucu yok → "hata: OmniRoute yok: …" · 401 →
"hata: OmniRoute 401: kimlik reddedildi (OMNIROUTE_KEY …)" · model listede yok → "hata: model yok: <m> (listede N model)"; exit 1,
A tarafı dahil model çağrısı 0. ig._post govde=None → GET. Testler test_f3.py (4, sahte). O40: kırmızı eecd36e · yeşil (765 passed;
mutasyon 401 dalı → 1 kırmızı). Ağsız deneme: OMNIROUTE_URL=http://127.0.0.1:9 → "hata: OmniRoute yok: URLError … 10061" exit 1.
Not: sohbet yolu OMNI_YOL /v1/… (skill), liste yolu /api/v1/… (openapi) — F1-KURULUM ikisini birlikte kesinleştirir.
F3-HAZIRLIK (O49, 5 Eki; model çağrısı 0, kod/test yok — keşif sayaç 40'ta bitti, madde 1 DUR):
- test_f1.py:144 değişikliği — Ömer onayı (sonradan, 5 Eki; "FIYAT boş" geçici bir değişmezdi).
- Madde 1 (araç kapısı) DUR — eski test çakışması: test_f1.py:95 (2 param) ve :143 "arastirma" (araçlı) adımını _form_al ile OmniRoute'a
  yönlendiriyor; kural ikisini kırar. Öneri: bu iki teste araclar=() (araçsız çağrı; yönlendirme mekanizması sınanmaya devam eder).
  Tasarım: yon.red(d, adim, araclar) → metin|None; sec(..., araclar=()) reddedilirse (cagir, d["model"]); ab(..., araclar=()) → "RED (araç
  kullanıyor)", çağrı 0 (kwarg: test_f2 "arastirma"yı araçsız kullanıyor, bozulmaz); _form_al defter satırı form "yönlendirme reddedildi:
  <adım> araç kullanıyor" + panel Denetim. Araçlı adımlar (varsayılan ARASTIRMA_ARAC): arastirma akil.py:944 · ozellik :983 · anatomi :504;
  araçsız: gelistirme :471 · tarama parti.py:494.
- Madde 2 (OpenRouter /api/v1/models, anahtarsız, 5 Eki, 464 model): :free/0 fiyat + image + structured_outputs + bağlam ≥64k → yalnız 2:
  dots-studio/dots-3-note-preview:free (512k) · openrouter/free (200k; rastgele ücretsiz modele yönlendirici → A/B'de kol sabit değil).
  Ücretli uygun 253; fiyat sırası ilk 3 ($/1M girdi/çıktı): inclusionai/ling-3.0-flash-vl 262k 0.021/0.0616 · nex-agi/nex-n2.5-mini 262k
  0.025/0.1 · google/gemma-3-4b-it 131k 0.05/0.1 (ilk ikisi FIYAT'ta var → eklenecek yalnız gemma-3-4b-it). Mevcut mistral-nemo,
  l3-lunaris-8b, gpt-oss-20b görsel yok → tarama için uygun değil. Yorum (Ömer onaylasın): "ücretsiz liste" = anahtarsız liste; ücretsiz
  modellerde fiyat sırası anlamsız.
- Madde 3 keşfi: yon.ab kollara kareler GEÇİRMİYOR (tas(si, m, sema, model=)); gerçek tarama parti.py:493 hafif.GORSEL iken paket karelerini
  gönderir → A/B gerçek adımı ölçmüyor (A da B de karesiz). Düzeltme: girdi 4. öğe kareler (isteğe bağlı) iki kola aynı; ab-canli.ps1
  kareler = pt.paket_oku(p)["kareler"] (is_file, GORSEL ise). Görsel ön kontrol: OmniRoute GET /api/v1/models (1726 model) kaydında
  capabilities.vision (ling-3.0-flash-vl True, mistral-nemo yok; input_modalities alanı da var) → omni_yokla(..., gorsel=False) kwarg (test_f3
  1. test görsel alansız modelle None bekliyor), betik gorsel=True → "hata: model görsel girdi desteklemiyor: <m>", çağrı 0.
- AB_MODEL önerisi openrouter/inclusionai/ling-3.0-flash-vl (OmniRoute'ta var, vision True); madde 3 yeşilinden önce koşulmaz.

## A (devam)
**A6 (=Y4)** Son commit tarihi kurulu olmayan her repo için de alınır (stop-slop, marketingskills, ui-ux-pro-max-skill, vercel-labs/skills,
ruvnet/ruflo); sürüm numarasıyla kurulu plugin'de tag → commit → tarih (derinlik-3.md S3: bugün yalnız sha ile kurulu plugin'de `commits`
çağrısı var). Ömer notu (4 Eki): eski aday dosyasında `lisans:`/`son_commit:` satırı yoksa eklenir, mevcut içerik değişmez
(A2'nin `_eksik_tamamla` ponytail notu kapanır). Konum: alan bloğunun sonu (ilk `#`/`##` satırından önce) — uy.alanlar() yalnız o bloğu
okur; dosya sonuna eklenen satır panelde görünmez. Test.
O41: A6(a) kırmızı b9ec6d2 · yeşil 35e2474 (_eksik_tamamla satır yoksa alan bloğu sonuna, boş satırların üstüne; 766) · A6(b) kırmızı fe1d730 ·
yeşil e725acb (_guncellik etiket → repos/{r}/commits/{etiket} → tarih; kırılırsa ' · etiket X tarihi alınamadı (gh: …)'; 767). Canlı çağrı 0.
A6(c) açık (sayaç 40'ta başlatılmadı): kurulu adayda parti akışında mekanizma.md (cli.py:1138 üretici · akil._on :674 kurulu adayda koşmuyor).
Canlı doğrulama (ücretsiz, model yok; PowerShell 5.1):
1) `$py = "$(uv tool dir)\video-cli\Scripts\python.exe"; & $py -c 'from video import akil; print(akil.__file__)'` → repo akil.py (ağsız, denendi).
2) `$r = 'anthropics/claude-code'; $t = gh api "repos/$r/releases/latest" --jq '.tag_name'; gh api "repos/$r/commits/$t" --jq '.commit.committer.date'` → tarih (A6(b) zinciri, 2 REST).
O42 A6(c) keşfi (sayaç 40, kod yok): kurulu aday akil.py:910 durum "kurulu" → :921 araştırma döngüsü atlar. Yol: cli.on_ :1135-1139
bizdeki-kopya yazımı tek fonksiyona; akil'de durum=="kurulu" (kendi aracımız hariç) için çağrılır, mekanizma.md varsa dokunmaz; model 0.
Canlı A6(b) kanıtı (Ömer, 5 Eki): anthropics/claude-code releases/latest etiketi → commits/<etiket> → 2026-10-03T23:06:56Z (zincir canlıda çalışıyor).
O43 A6(c) yeşil (770): uy.bizdeki_mekanizma (cli.on_ + akil parti akışı aynı fonksiyon; durum "kurulu", kendi aracımız hariç; dosya varsa dokunulmaz; model 0).
Canlı doğrulama (ücretsiz, ağsız, model yok; PowerShell 5.1; geçici kök, repo değişmez):
1) `$k = Join-Path $env:TEMP ('a6c-' + [guid]::NewGuid().ToString('N').Substring(0,8)); New-Item -ItemType Directory -Force (Join-Path $k 'docs\departmanlar') | Out-Null; Copy-Item 'C:\Projeler\omer-skills\docs\departmanlar\envanter.json' (Join-Path $k 'docs\departmanlar'); $env:VIDEO_UYGULA_KOK = $k; video on canli graphify --tur skill; Get-Content (Join-Path $k '.kos\canli\graphify\mekanizma.md') -Encoding UTF8 -TotalCount 2`
   → "ZATEN VAR, araştırıcı yok" + "kaynak: bizdeki kopya · …/skills/graphify" (denendi).
2) Aynı oturumda: `$m = Join-Path $k '.kos\canli\graphify\mekanizma.md'; $t = (Get-Item $m).LastWriteTime; video on canli graphify --tur skill | Out-Null; (Get-Item $m).LastWriteTime -eq $t` → True (dokunulmadı; denendi).
A6(c) eki (Ömer kararı 5 Eki; O43 sapma 1 yan etkisi — plugin güncellenince eski inceleme kalırdı): bizdeki_mekanizma dosya varsa
"kaynak: bizdeki kopya · <yol>" yolunu şimdiki kurulu yolla karşılaştırır; aynıysa dokunmaz, farklıysa (sürüm klasörü) ya da yol yoksa yeniden
üretir. O44: kırmızı 1aa3f8a (eski "varsa dokunulmaz" fixture'ı aynı-yol satırı aldı) · yeşil a2efe90 (771). Sıra (Ömer, 5 Eki): A7 → A8 → F1-KURULUM.
O44 A7 keşfi (sayaç 40, kod/test yok): sebep altyazı da kare de değil — kablolama. Prompt adayı akil.py:911 durum "arac_degil" → _on
(:675-683, zaten rapor=None) ve araştırma koşmaz; getir.prompt_metni (getir.py:280; rapor tür=prompt satırının zamanı + paket segmentler.jsonl)
yalnız cli.on_ --rapor yolunda (cli.py:1139-1141). Panel _kapsam (akil.py:335/340) aday.md "## Prompt metni" bölümünü arar → yok → "alınmadı".
Kanıt: 2026-10-03-short, vfLtsYbtJf0 rapor satır 18 (0:50, kaynak: altyazı) mevcut; durum.json adayı arac_degil, deneme yok.
Öneri: akil döngüsünde (:912 yanı) tur=="prompt" için :879-881 raporlar listesinden o videonun metni + ctx["kok"]/<v>/segmentler.jsonl ile
gt.prompt_metni (model 0) → _kapsam'ın okuduğu yere; "metin alınamadı" ise sebep Kapsam'da kalır. Kırmızı kalıbı: test_m2b _parti/_actx/_rapor
(tür prompt satırı) + segmentler.jsonl → panel Kapsam "prompt metni ✓"; segment yoksa sebep satırı.
O45: A7 kırmızı 0f30072 · yeşil (773, pushlı): akil döngüsü tür=prompt + arac_degil → gt.prompt_metni (model 0) aday.md "## Prompt metni"
(yoksa yazılır, bir kez) · _kapsam "altyazı yok" → "alınamadı: altyazı yok (paket segmentleri bulunamadı)". Canlı (vfLtsYbtJf0, panel.md
değişmeden, yalnız prompt_metni): segment dosyası VAR ama metin boş. Kök neden kanıtlı: short'ta 2 segment (0–61.28, 61.28–…); prompt 0:50,
getir.py:291 `t <= x["bas"] < son` yalnız t'den sonra BAŞLAYANI alır → kapsayan segment düşer. A7 eki (sayaç 40, açılmadı): seçim
örtüşmeye çevrilir (`x["bas"] < son and x.get("son", x["bas"]) > t`; cli.on_ de aynı fonksiyonu kullanır). Kırmızı: bas 0 · son 61.3 ·
prompt 0:05 → metin alınır (taslak test_a7'den geri alındı, bir sonraki oturum).
Canlı doğrulama (ağsız, model 0, denendi 2 passed): `cd C:\Projeler\omer-skills\tools\video; uv run pytest tests/test_a7.py -q`
O46 A7 eki (Ömer, 5 Eki): (a) getir.py:291 seçim örtüşme (`bas < son and son_seg >= t`; son'suz segment eski davranış; cli.on_ aynı
fonksiyon). (b) "## Prompt metni" boş / "altyazı yok" / "alınamadı" ise yeniden yazılır, dolu bölüme dokunulmaz. Kırmızıda bulunan ikinci kök
neden: yazılmış aday.md → _onceki True → durum "onceki" → A7 dalı bir daha koşmazdı; dal artık arac_degil + onceki. Kırmızı f56b201 · yeşil
e315d6a (776, pushlı). Canlı (ağsız, model 0, yalnız prompt_metni): vfLtsYbtJf0 metin DOLU ("Stop installing Claude skills manually. …").
O46 A8 keşfi (kod/test yok; sayaç ~36, bitmez): kuyruk satırı `| id | dk | başlık | not | durum |` (tarama.py:250, 5 hücre). Hazır parça:
kanal._istek (kanal.py:245; ≥BEKLE sn arası, 429/403'te GERI ile ≤2 tekrar) — ama başarısızlıkta None döner, hata metnini kaybeder →
A8 için `_istek`'e hata metnini dışarı veren isteğe bağlı parametre (varsayılan davranış aynı). Örnek kullanım cli._bagli_video :399-411
(dk = round(duration/60,1), başlık [:40] '|'→'/'). Komut: cli.kuyruk :1109 (parser :1273) → `video kuyruk yenile` (isteğe bağlı konumsal
eylem). Satır yazımı CRLF korunur (kuyruk_isle gibi bytes). Kırmızı: sahte kos (rc 0 json → dk/başlık dolar · 429 ×3 → nota "meta hatası: …",
satır "?" kalır · "?" olmayan satıra istek yok).
O47 A7 eki-2 (Ömer, 5 Eki; O46 canlı: "ekran:" alanına "kaynak: altyazı" düştü — konumla okunan s[6] aslında kanıt sütunu): prompt_metni
Adaylar sütunlarını başlık adına göre okur (ad · tür · zaman · kanıt · kaynak; başlıkta yoksa "—"); "ekran:" → "kanıt:" + "kaynak:". Repodaki
tüm raporlar tek şema (ad|sözlük|tür|link|ne işe yarar|zaman|kanıt); "yeni şema" = ayrı kaynak sütunlu düzen. Kırmızı 9a7b41f (3 failed) ·
yeşil (779). Canlı (ağsız, model 0, yazmaz; denendi): `cd C:\Projeler\omer-skills\tools\video; uv run python C:\Projeler\omer-skills\docs\video-tarama\a7-canli.py`
→ "### Claude içinde … · 0:50" / "kanıt: kaynak: altyazı" / "kaynak: —".
O48 A8: kırmızı 345ba19 (5 failed) · yeşil (784). kanal._istek(hata=[]) None'da son hata satırını ("ERROR: " öneksiz) listeye ekler, varsayılan
aynı. cli.kuyruk `yenile` eylemi: 5 hücreli, id 11 karakter, dk ya da başlık "?" satıra istek; başarı → dk/başlık; başarısız → "?" kalır,
nota "meta hatası: <≤80>" (aynısı varsa eklenmez); yalnız değişen satır yeniden yazılır, satır sonu korunur. Gerçek kuyruk.md'de "?" satır 0.
Canlı (PowerShell 5.1, geçici dizin): (1) ağsız, denendi → "kuyruk: yenilendi 0/0 satır (0 istek)":
`$u = Join-Path $env:TEMP 'a8-bos.md'; Set-Content $u '| AAAAAAAAAAA | 3.0 | x | | bekliyor |' -Encoding ascii; video kuyruk yenile --dosya $u`
(2) ağlı, 1 istek, ücretsiz, denenmedi → 1/1 ve dk/başlık dolu (ya da notta "meta hatası: …"):
`$u = Join-Path $env:TEMP 'a8-canli.md'; Set-Content $u '| vfLtsYbtJf0 | ? | ? | | bekliyor |' -Encoding ascii; video kuyruk yenile --dosya $u; Get-Content $u`
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
O1 (4 Eki): plan yazıldı. O2 (4 Eki): A1 ✓ (video 569 yeşil). O3 (4 Eki): A2 ✓ · A3 ✓ (video 573). O4 (4 Eki): A4 ✓ · A5 ✓ (video 581). O5 (4 Eki): A4b ✓ (video 584). O6 (4 Eki): C1 ✓ + koruma (video 591). O7 (4 Eki): C2 ✓ (video 597). O8 (4 Eki): C3 ✓ (video 603). O9 (4 Eki): C4 ✓ + ek (video 607). O10 (4 Eki): C4/C3 düzeltmesi 3 madde ✓ (video 611). Sonraki: D1. O11 (4 Eki): O11 madde 1–2 ✓ (video 613), sonraki O11 (3) tekrar ayıklama, (4) ocr-gurultu.txt, sonra D1. O12 (4 Eki): O11 (3) ✓ · (4) ✓ (video 615), sonraki O11 (5), sonra D1. O21–O22 (5 Eki): B2 ✓ (erişilemedi → kapsam.json + Denetim, Ömer kararı) · B ek kablolama ✓ (video 662); sonraki B3. O23 (5 Eki): B ek düzeltmesi ✓ (tek bölüm, video 663). B3 ✓ (video 664); sonraki B4. · F1 ✓ (O36)
A6(c) eki canlı (ağsız, model yok; denendi, O44): O43 komut 1 kalıbı + mekanizma.md'deki yol 'C:/eski/1.0.0' yapılıp `video on canli graphify --tur skill` tekrar → satır gerçek yolla yeniden yazıldı. Not: `$py -m video` çalışmaz (video.__main__ yok); PATH'teki `video` kullanılır.
