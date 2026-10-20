# TERS-2 d6 — kayıp analizi + SKILL.md önerisi + d7 tasarımı

Kaynak: önbellek (%TEMP%/ters-kapi/onbellek, 222 dosya) + docs/ters/kapi/sonuc.json. Yeni yazar/hakem çağrısı 0. Döküm betiği: `d6-dok.py` (önbellekten notlar + oylar).
Bileşen ortalamaları (skill / zemin): js mekanizma 0.633 / 0.867 · dotnet 0.700 / 0.833 · site mekanizma 0.757 / 0.714 · site yeniden 0.743 / 0.734 · kanıt alıntısı her yerde 1.00 / 1.00.

## 1. Bulgular (sınıf bazında)
1. **js + dotnet — skill kolu kanıtsız koştu (ölçüm hatası).** `rea_kanit` `subprocess.run(["rea", …])` çağırıyor; Windows'ta `rea` yalnız `rea.cmd` (npm shim), shell yok → `FileNotFoundError`. Kanıt alanı 7/7 kod hedefinde `REA hata: FileNotFoundError` (27 karakter). Skill kolu = SKILL.md + ham kaynak + hata satırı; "REA → graphify → yeniden-yazım" adımları araçsız tek turda uygulanamaz, yalnız istem şişirir.
2. **ink-puppet (js, 0.60 / 0.80 · 0.60 / 1.00).** Skill notları davranışı (drawIn, choreograph, seek-safe) anlatıp yapı olgularını atladı: STAND sabit eklem tablosu (madde 2) ve INK_CLIPS arama/bilinmeyen klip (madde 4) iki tekrarda da hakemde 0. Zemin kolu bunları sıraladı.
3. **Fiyat.Tests (dotnet, 0.60 / 0.90 · 0.80 / 0.80).** Skill notları "ne sınanıyor" (110m, 51m girdileri) yazdı; yapı olguları (sealed [TestClass] sınıfı, paralel yürütme özniteliği) çıkmadı. Zemin kolu öznitelik ve sınıf düzeyini sayıyor. ortak-js tekrar 2 (0.70 / 0.90): skill window.lab sözleşmesini (madde 1) ve kur()'un dpr/resize ayrıntısını (madde 2) yazmadı (openai oyu B=[0,0,1,1,1]); bunun yerine Lenis zaman birimi gibi ikincil ayrıntıya yer verdi.
4. **site (post, gecis, kamera-yolu, parcacik, ses) — yeniden kurulum puanı geçersiz.** Orijinal kareler 5/7 hedefte düz renk (ortalama 20.0, std 0.0; post/gecis/kamera-yolu/parcacik, ses ≈0.7): headless prob sahneyi çizmiyor. Böyle referansta boş sayfa üreten kol 1.00 alıyor (post zemin#1 ve kamera-yolu zemin#2 ortalama parlaklık tam 20.0 = boş), içerik üreten 0.00 (post skill#1). Site farkı (+0.017) skill etkisi değil, hangi kolun boş sayfa yazdığının kuru gürültüsü. Tekrar sapması 0.119.
5. **Hakem ayrıştırmıyor.** Mistral çoğu çağrıda iki nota da hepsi-1 veriyor (ink-puppet 2/2 tekrar; diğerlerinde de sık), "ikisi onaylamazsa 0" kuralıyla fiilen tek hakem (openai) belirliyor → puan tek örnekleme gürültüsü taşıyor.

Sonuç: kapı başarısızlığı SKILL.md'nin kötü olduğunu kanıtlamıyor; ölçüm üç yerden bozuk (REA boş, site referansı boş, ikinci hakem sabit 1). js/dotnet'te skill'in gerçek zayıflığı yalnız "yapı envanteri yerine davranış yazma" eğilimi (bulgu 2-3) ve bu da kanıt olmadan ölçüldü.

## 2. SKILL.md önerisi (DOSYAYA YAZILMADI; d7'de uygulanır, kapı sorusu/ground truth'a bakılmadan, sınıf düzeyinde)
`## Adımlar (site hedefi)` bölümünden önce, yeni kısa bölüm:

```
## Kod hedefi (JS/.NET, tarayıcısız) — kısa yol
Site adımlarını (1-7) atla: tarayıcı, trace, ekran kaydı, design-dna yok. Sıra: (1) REA (`rea.cmd analyze-javascript-application` / `inspect-managed-members`) ya da verilen ham kaynak; (2) önce yapı envanteri, sonra davranış.
5 madde = 5 ayrı bileşen: tür/sınıf ve öznitelikleri · sabit ve veri tabloları · dış bağımlılık ve sürüm · ana akış (girdi → çıktı) · sınır durumu (null, bilinmeyen ad, hata, eşik).
Aynı bileşenin ikinci anlatımı madde sayılmaz. Davranış cümlesi yazmadan önce o bileşenin adı/değeri notta geçmiş olmalı.
```
Gerekçe: bulgu 2-3 (yapı olgusu düşüyor), bulgu 1 (araç adımları tek turda uygulanamıyor). Site bölümüne dokunulmuyor (bulgu 4 ölçüm sorunu).

## 3. Koşucu düzeltmeleri (ölçüm geçerliliği; SKILL.md ayarı değil) — d7 önkoşulu
a. `rea_kanit`: `shutil.which("rea")` (→ rea.cmd) ile çöz; `REA hata:` dönerse hedef hatalı sayılsın, sessiz geçmesin. Önce tek hedefte elle sına (çağrısız).
b. Site: orijinal karelerin std < 2 ise `c3 = None` (puana girmez), hedef "referans boş" diye raporlanır; ya da prob'a WebGL bayrağı (`--use-gl=swiftshader` / `--enable-unsafe-swiftshader`) ve sahne bekleme ekleyip kareyi doğrula. Hedef seçiminde süzgeç: orijinal std ≥ 10.
c. Hakem: ikinci aileyi seç ama hepsi-1 dönen aile "ayrıştırmıyor" sayılsın (A ve B'nin ikisi de 5/5 → oy geçersiz, sıradaki aileye geç). Mistral yerine google/alibaba önce.

## 4. d7 yeniden koşu tasarımı
- **Held-out:** bu analizde kullanılan 13 hedef sızmış sayılır (bulgular onlardan çıktı). Yeni 12 hedef: 5 js kütüphanesi, 4 .NET derlemesi/test projesi, 3 site (orijinal std ≥ 10 doğrulanmış). Ground truth elle, her madde Read ile doğrulanmış dosya+satır+alıntıyla (daefde dersi); skill değişikliğinden önce dondurulur.
- **Ön koşul (çağrısız):** 3.a-c düzeltmeleri + REA tek hedef elle sınaması + site adaylarında prob karesi std kontrolü.
- **Çağrı bütçesi:** yazar = 12 hedef × 2 kol × 2 tekrar = 48 + 4 kuru deneme = 52 → **tavan 56** (Sonnet, plan kotası). Hakem = 12 × 2 tekrar × 2 aile = 48 başarılı + ~%25 yeniden deneme → **tavan 80** (yalnız ücretsiz aileler; Haiku/ücretli 0). Zemin kolu eski önbellekten yararlanmaz (yeni hedefler).
- **Kapı:** skill ort ≥ 0.92 ve eşli fark GA95 alt sınırı > 0 (değişmez); ayrıca js/dotnet ve site için ayrı ortalama raporlanır. 12 hedefte GA genişliği ≈ ±0.06; fark gerçekte < 0.05 ise bu tasarım da ayıramaz — o durumda kapı "skill zeminden kötü değil" (GA alt > −0.03) + kanıt boşluğu kapandı diye ayrı bir kabul kararı Ömer'e sorulmalı.
- **Onay gerekli:** yeniden koşu, ground truth yazımı (12 × 5 madde) ve tavan artışı Ömer onayıyla (sabah listesi).
