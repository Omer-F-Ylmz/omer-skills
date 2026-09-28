# codex-skill
ad: codex-skill
tur: skill
video: 2n84xa99FRY
repo: avenoxai/avenoxskills
lisans: MIT
son_commit: 2026-09-25
arsiv: hayır
kaynak: yok (SkillSpector atlandı: tur tavanı — yerel klon yapılmadı)
telemetri: yok
arastirma: yarım: tur tavanı: skillspector-taraması, ek özellik derinliği araştırılamadı
## Ne
`skills/codex-fleet/SKILL.md` — Codex CLI'yi (openai/codex) Claude Code/Cursor gibi bir ajandan sürücü tek dosyalık skill. Üç şey yapar ve HER ZAMAN yürütür (yalnız anlatmaz): (1) `codex exec` ile genel kod görevleri, (2) Codex'in yerleşik `gpt-image-2` aracıyla görsel üretimi, (3) worktree izolasyonuyla paralel çoklu-kulvar "fleet" (arka planda çok sayıda `codex exec` çağrısı). Video, avenox.lol/codex.md adresinden auth'suz `curl` ile çekilip doğrudan `.claude/skills/` altına düşürülen bir kopyasını gösteriyor.
## Kanıt
70 yıldız · son commit 2026-09-25 · MIT · arşiv değil. Repodaki gerçek `skills/codex-fleet/SKILL.md` artık varsayılan modeli `gpt-6-astra` yapmış ve `--full-auto`'yu "artık mevcut değil" diyerek `--approve-for-me` ile değiştirmiş; ayrıca repo notu "gpt-5.6-sol/gpt-5.6-luna nesil-6 KAPALI, 2026-09-26 itibarıyla HTTP 400" diyor. on.md'deki (avenox.lol/codex.md, video kaynağı) kopya hâlâ eski `gpt-5.6-sol` modelini ve kaldırılmış `--full-auto` bayrağını öneriyor — yani videonun gösterdiği auth'suz curl kopyası kaynak repoya göre BAYAT ve önerdiği komutlar repo kendi belgesine göre hata verir.
## Kurulum
- (yok) paket yöneticisi yolu yok; kurulum yöntemi ya `git clone` + `cp -R skills/codex-fleet ~/.claude/skills/` (repo) ya da videonun izlediği `curl avenox.lol/codex.md > SKILL.md` (auth'suz, sürüm sabitlemesiz, bayat). İkisi de yapılandırılmış Kurulum türlerine (plugin/mcp/uv/npm/winget) girmiyor; gerekçe RED — bkz. Önerilen katman.
## İzinler
Skill kendi açıklamasında "ALWAYS EXECUTES, never just describes" diyor; `--sandbox danger-full-access` (ağ/geniş sistem erişimi) ve `--approve-for-me` gibi yüksek etkili bayraklar yalnız düzyazıda "kullanıcıya sor" notuyla yumuşatılmış, zorlayıcı bir onay kapısı yok. Ayrıca görsel üretim CLI-fallback yolu `OPENAI_API_KEY` ister.
## Duman testi
- komut: codex --version
- cikis: 0
- desen: \d+\.\d+
## Geri alma
- (yok) paket yöneticisi kaydı yok; elle: kopyalanan `~/.claude/skills/codex-fleet/` klasörünü sil.
## Köprü izni
- arac: codex
- altIzin: --version
## Önerilen katman
RED — gerekçe: güvenlik: kaynak (avenox.lol/codex.md) sürüm sabitlemesiz, auth'suz, herkes tarafından değiştirilebilir tek sayfa; şu an kaynak repoya göre bayat olduğu kanıtlandı (deprecated model + kaldırılmış bayrak) ve skill kendi tanımında onaysız otomatik yürütmeyi zorunlu kılıyor (`--sandbox danger-full-access` dahil). Repo kendisi (avenoxai/avenoxskills, MIT, 70 yıldız) meşru ama videonun önerdiği dağıtım yolu değil.
## Telemetri kapatma
yok (skill dosyasında telemetri kodu yok; bağımlı `codex` CLI'nin kendi telemetrisi bu adayın kapsamı dışında)
## Özellikler
### codex-exec-genel
ne: Kod inceleme/refactor/çok dosyalı düzenleme gibi görevleri ayrı bir Codex CLI oturumuna (`codex exec`) devreder.
kurulum: SKILL.md'deki komut şablonu; kurulum yok, `codex` CLI zaten kurulu+auth'lu olmalı.
lisans: MIT (repo)
etiket: token
karar: DENE
gerekce: hipotez: ağır çok-dosyalı analiz Claude oturumu yerine ayrı Codex aboneliğine devredilince Claude bağlamı/tokenı büyümez · metrik: token (devredilen görev başına Claude tarafında tüketilen token) · butce: 3 görev, gerçek repo üstünde · geri_alma: skill dosyasını sil · esik: devredilen görevde Claude token tüketimi devretmeyen eşdeğerine göre ≥%30 düşmeli
### imagegen
ne: Codex'in yerleşik `gpt-image-2` aracıyla görsel üretir (abonelik yeter, anahtar gerekmez); CLI-fallback yolu ayrı `OPENAI_API_KEY` ister.
kurulum: aynı SKILL.md içinde, ayrı kurulum adımı yok.
lisans: MIT (repo)
etiket: -
karar: RED
gerekce: güvenlik: skill "ALWAYS EXECUTES, never just describes" diyor ve fallback yolu ayrı bir API anahtarı + ayrı faturalama gerektiriyor; onay kapısı yok (kaynak: bu aday dosyasının İzinler bölümü).
### fleet-parallel
ne: Bağımsız N görevi tek mesajda `run_in_background: true` ile aynı anda ateşleyip toplam bekleme süresini kısaltır.
kurulum: SKILL.md talimatı, ek kurulum yok.
lisans: MIT (repo)
etiket: teknik
karar: ZATEN VAR
gerekce: zaten var: Claude Code'un kendi `run_in_background` Bash mekanizması + bu projenin `video toplu`/alt-ajan paralel dispatch deseni aynı fikri zaten karşılıyor.
### multi-image-referans-zinciri
ne: `-i, --image <FILE>...` bayrağının aç gözlü (greedy) parse hatası yüzünden prompt'u yutmasını `--` ayıracıyla önler.
kurulum: yok, komut kalıbı.
lisans: MIT (repo)
etiket: teknik
karar: ÖĞREN
gerekce: niş bir CLI kullanım ipucu; bilgi kartına değer ama kurulacak bir mekanizma değil.
## Mekanizma
### codex-exec-genel
nasıl: Görev metni aynen ayrı bir `codex exec` alt sürecine geçirilir; Claude oturumu yalnız komutu tetikler ve arka planda sonucu okuyup özetler — ağır okuma/analiz trafiği kendi bağlamına girmez, Codex'in kendi (ayrı faturalanan) modelinde kalır.
neden: Claude'un context penceresi büyük dosya kümesini okumak zorunda kalmaz; yalnız devredilen görevin özeti geri döner, bu da girdi tokenını düşürür.
koşul: Kullanıcıda ayrı bir Codex CLI kurulumu+aboneliği/OAuth yoksa hiç çalışmaz; kısa/tek dosyalık görevlerde devretme+özetleme ek gecikmesi kazancı yer.
bizde: Halihazırda benzeri bir devretme yok; T1 aday olarak `.kos` alt-ajan (Task) akışımızla örtüşüyor, ayrı kurulum gerektirmeden aynı devretme fikri zaten mevcut alt-ajan mimarisiyle karşılanıyor.
### fleet-parallel
nasıl: Bağımsız görevleri sıralı değil, tek mesajda birden çok arka plan Bash çağrısı olarak ateşler; her biri kendi worktree'sinde izole çalışır, tamamlanınca bildirim okunur.
neden: Duvar-saati toplamı N × süre yerine max(süre) olur; ayrıca sıralı context şişmesi yerine yalnız bitince özet okunur.
koşul: Tek bir görev varsa ya da görevler birbirine bağımlıysa (biri diğerinin çıktısını beklerse) kazanç yok, hatta `&&` zinciriyle sıralamak gerekir.
bizde: Bu ajan mimarisinin kendi `run_in_background` + Monitor deseni aynı kazancı zaten sağlıyor; ayrı kurulum gerekmez.
### multi-image-referans-zinciri
nasıl: `-i ref1.png -i ref2.png "prompt"` çağrısında CLI'nin argüman ayrıştırıcısı `-i` bayrağını variadic-greedy okur ve prompt metnini de dosya listesine katar; `--` eklenince ayrıştırıcı orada durur, prompt pozisyonel argüman olarak kalır.
neden: Prompt'un sessizce yutulup boş stdin hatasına düşmesini önler — bilgi kaybı değil, bir CLI ayrıştırma kusuruna karşı sözdizimi düzeltmesi.
koşul: Görsel referansı olmayan (yalnız metin) çağrılarda hiç devreye girmez; yalnızca `-i` kullanan görsel üretim/analiz çağrılarında geçerli.
bizde: Karşılığımız yok; bir CLI'nin kendi argüman ayrıştırma kusuru, bizim araç setimizde aynı bayrak yok.
## Bağımsız kanıt
- https://github.com/avenoxai/avenoxskills — kaynak repo MIT lisanslı, 70 yıldız, 2026-09-25'te güncellenmiş, CI'da skill-tests.yml var; avenox.lol/codex.md bu repodaki `skills/codex-fleet/SKILL.md`'nin bayat bir tek-dosya kopyası.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Avenox, Codex fleet + imagegen skill'lerini tek dosyada birleştirip herkese açık yayınladı (0:51) | github.com/avenoxai/avenoxskills skills/codex-fleet/SKILL.md | doğru | Tek SKILL.md hem `codex exec` genel görev hem yerleşik `gpt-image-2` görsel üretimini kapsıyor, avenox.lol üstünden açık yayınlanıyor. | - |
| Skill curl ile auth'suz çekiliyor (13:39) | on.md kaynak alanı (https://avenox.lol/codex.md, herhangi bir auth başlığı olmadan `video getir` ile erişildi) | doğru | Statik public sayfa, kimlik doğrulama yok; ayrıca sürüm sabitlemesi de yok. | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
