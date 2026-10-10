# "model" yaz sana rehberi göndereyim.
## Künye
"model" yaz sana rehberi göndereyim. · alperenerbay · süre: 0:41 · ? · https://www.instagram.com/reel/DdEUwLgE-Sb/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-5 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 30495 tk · claude-haiku-5-5: claude-haiku-5-5 · 39756 tk
## Özet
Kısa reel, DeepSeek Harness adlı açık kaynak ajan çatısını tanıtıyor. Anlatıcıya göre proje, Claude Code'un ücretsiz sürümü gibi sunuluyor ve bir haftadan kısa sürede GitHub'da 180 bin yıldızı geçmiş. Her parça (model, araçlar, hafıza, ajan döngüsü) Cordis eklenti sistemiyle değiştirilebiliyor. Yerel model çalıştırma, Claude Code ve Codex alt ajanları ve 53 hazır araç anlatılıyor. Kurulum komutları (git clone, pnpm install, build, dsh web) ve yorumlara 'model' yazana gönderilecek kurulum/ajan kartı promptu gösteriliyor.
## Bölümler
- 0:00 DeepSeek Harness tanıtımı ve GitHub yıldızları
- 0:10 Her şey eklenti: özelleştirilebilir yapı
- 0:16 Kurulum komutları
- 0:23 Yerel model ve alt ajanlar
- 0:33 Ajan preset oluşturma ve 53 hazır araç
- 0:38 Kurulum rehberi promptu ve yorum çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| DeepSeek Harness | yok | CLI | https://github.com/deepseek-ai/deepseek-harness | Açık kaynak, eklenti tabanlı, özelleştirilebilir yapay zekâ ajan çatısı | 0:05 | Ekranda github.com/deepseek-al/deepseek-hamness ve 'Customize your DeepSeek Harness' yazıyor (karede: OCR'a göre depo adresi ve 'Customize your DeepSeek Harness' başlığı (kare görseli yok, OCR metni)) |
| Claude Code | yok | CLI | yok | Karşılaştırılan ajan aracı; Harness içinden alt ajanı çağrılabiliyor | 0:30 | içinde Cloud Code ve Codex'in alt ajanlarını da çağırabiliyorsun |
| Codex | yok | CLI | yok | Harness içinden alt ajanı çağrılabilen kodlama ajanı | 0:30 | Cloud Code ve Codex'in alt ajanlarını da çağırabiliyorsun |
| Cordis | yok | teknik | yok | Harness'in dayandığı eklenti sistemi | 0:11 | DeepSeek Harness is built on Cordis's plugin system (karede: Ayarlar penceresi üstünde 'Everything is a plugin' başlığı ve Cordis eklenti sistemi açıklaması; altında eklenti listesi) |
| DeepSeek-V3 | yok | teknik | yok | Model seçiminde ekranda görünen model | 0:23 | OCR 0:23 'DeepSeek-V3' (karede: OCR metni 'DeepSeek-V3' (kare görseli gönderilmedi)) |
| Gemma-4 | yok | teknik | yok | Yerel çalıştırılabilen model olarak ekranda görünen seçenek | 0:26 | OCR 0:26 'Gemma-4' (karede: OCR metni 'Gemma-4' (kare görseli gönderilmedi)) |
| pnpm | yok | CLI | yok | Bağımlılık kurma ve derleme için paket yöneticisi | 0:17 | $ pnpm instatt, $ pnpm run build (karede: Terminalde pnpm install ve pnpm run build satırları (OCR)) |
| Git | yok | CLI | yok | Depoyu klonlamak için kullanılıyor | 0:16 | $ git clone https://github.com/deepseek-ai/deepseek-harne... (karede: Terminalde git clone satırı (OCR)) |
| GitHub | yok | teknik | yok | Projenin barındığı ve yıldız sayısının gösterildiği servis | 0:00 | Bir hafta bile olmadan GitHub'da 180 bin yıldızı geçmeyi başardı |
| dsh | yok | CLI | yok | Harness web arayüzünü başlatan komut | 0:17 | $pnpm dsh web (karede: Terminalde pnpm dsh web satırı (OCR)) |
| editing-cordis-compositions | yok | skill | yok | Ajan preset oluştururken yüklenen Cordis düzenleme skill'i | 0:35 | skil - editing-cordis-compositions (karede: Koyu ajan arayüzünde Edit/Read dosya satırları, preset_validate araç çağrısı ve probe eklentisi kaldırma mesajı) |
| preset_validate | yok | teknik | yok | Ajan preset'ini doğrulayan araç çağrısı; code-review preset'i için çalıştırılıyor. | 0:35 | Tool call - preset_validate - code-review (karede: kanıttan) Tool call - preset_validate - code-review |
| preset_list | yok | teknik | yok | Kayıtlı ajan preset'lerinin listesini döndüren araç çağrısı; yeni preset'in listede göründüğü kontrol ediliyor. | 0:35 | Tool call - preset_list - () (karede: kanıttan) Tool call - preset_list - () |
| DeepSeek Harness kurulum rehberi | yok | prompt | yok | Projeyi (DeepSeek Harness deposu) baştan sona kur; kullanıcı kod yazmıyor. Kurulum bitince hazır araçları kategori kategori listele, hangi modeli bağlayacağını sor, ücretli seçenek önerirsen ücretsiz alternatif de yaz, model bağlanınca tek örnek soruyla test edip sonucu göster. | 0:38 | kaynak: kare |
| Tek işi olan küçük ajan kartı | yok | prompt | yok | Ajan kartına göre küçük bir ajan kur: ajan adı, tek işi, girdi, çıktı, sıklık, yazılacak yer; adımları maddele, hangi hazır aracı kullanacağını söyle, 53 aracın hepsini açma, planı yazıp onay al. | 0:40 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Yan menü (sidebar navigation) | Sol yan gezinme menüsü (karede: Sol yan menüde General, Models, Plugins ve Agent presets sekmeleri; Plugins seçili.) | 0:11 | kare |
| Arama kutusu (search input) | Eklenti arama alanı (karede: Üstte 'Search plugins' yazan arama kutusu.) | 0:11 | kare |
| Sekmeler (tabs) | Sekmeli panel (karede: 'Plugin configuration' ve 'Plugin list' sekmeleri; 'Plugin list' seçili.) | 0:11 | kare |
| Kart ızgarası (card grid) | Eklenti kart ızgarası (karede: Eklentiler iki sütunlu kartlar halinde; her kartta ad ve Enabled rozeti.) | 0:11 | kare |
| Rozet (badge) | Durum rozetleri (karede: Kartlarda 'Enabled' yeşil rozetleri görünüyor; bazı kartta 'Disabled' rozeti var.) | 0:11 | kare |
| Metin vurgusu (text highlight) | Başlık vurgusu (karede: 'Everything is a plugin' başlığı mavi arka planla vurgulanmış.) | 0:11 | kare |
| Koyu tema (dark mode) log paneli | Koyu tema ajan log paneli (karede: Siyah panelde Edit, Read, Think satırları ve araç çağrıları; monospace yazı.) | 0:35 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| cd deepseek-harness | Proje klasörüne girer (karede: Terminal satırı '$ cd deepseek-harness') | 0:16 | kare |
| git clone https://github.com/deepseek-ai/deepseek-harness.git | Depoyu klonlar (karede: Terminal satırı '$ git clone https://github.com/deepseek-ai/deepseek-harne ss.git') | 0:16 | kare |
| pnpm install | Bağımlılıkları kurar (karede: Terminal satırı '$ pnpm instatt') | 0:17 | kare |
| pnpm run build | Projeyi derler (karede: Terminal satırı '$ pnpm run build') | 0:17 | kare |
| pnpm dsh web | Web arayüzünü başlatır (karede: Terminal satırı '$pnpm dsh web') | 0:17 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Bir haftadan kısa sürede GitHub'da 180 bin yıldızı geçti | 0:00 | sayısal |
| Model, araçlar, hafıza ve ajan döngüsü dahil her parça özelleştirilebiliyor | 0:00 | özellik |
| İçinde 53 hazır araç var | 0:00 | sayısal |
| Tamamen ücretsiz ve açık kaynak | 0:16 | özellik |
| Claude Code'un ücretsiz sürümü olarak sunuluyor | 0:00 | karşılaştırma |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | DeepSeek Harness | DeepSeek Harness | Adı DeepSeek Harness |
| konuşma 0:00 | Claude Code | Claude Code | Cloud Code ve Codex'in alt ajanlarını çağırabiliyorsun |
| konuşma 0:30 | Codex | Codex | Codex'in alt ajanlarını da çağırabiliyorsun |
| konuşma 0:00 | GitHub | GitHub | GitHub'da 180 bin yıldız |
| kare 0:11 | Cordis | Cordis | built on Cordis's plugin system |
| kare 0:16 | git clone | Git | $ git clone https://github.com/deepseek-ai/... |
| kare 0:17 | pnpm install / build | pnpm | $ pnpm run build |
| kare 0:17 | dsh web | dsh | $pnpm dsh web |
| kare 0:23 | DeepSeek-V3 | DeepSeek-V3 | OCR 'DeepSeek-V3' |
| kare 0:26 | Gemma-4 | Gemma-4 | OCR 'Gemma-4' |
| kare 0:35 | editing-cordis-compositions skill | editing-cordis-compositions | skil - editing-cordis-compositions |
| kare 0:35 | probe-4 geçici eklenti | aday değil: başka adayın parçası (DeepSeek Harness) | Removed dynamic Plugin probe-4 |
| kare 0:35 | code-review preset | aday değil: başka adayın parçası (DeepSeek Harness) | preset_validate - code-review |
| kare 0:07 | Snake oyunu istemi | aday değil: konu dışı | Add a playable Snake gar... |
| kare 0:02 | React useState sayaç kodu | aday değil: konu dışı | const [count, setcount) - usestate(0); |
| ekran 0:38 | Kurulum promptu | aday değil: başka adayın parçası (DeepSeek Harness) | Şu projeyi benim için kur |
| konuşma 0:00 | Yerel model çalıştırma | aday değil: genel kavram | kendi bilgisayarında yerel bir şekilde çalıştırabiliyorsun |
| açıklama | Hashtag'ler (#claudecode vb.) | aday değil: genel kavram | #yapayzeka #deepseek #açıkkaynak #claudecode |
## Kareden okunanlar
- 0:11: 'Everything is a plugin' başlığı; Cordis eklenti sistemi açıklaması; Settings > Plugins listesi (api-gateway, timer, session vb.), altyazı 'Her yerinden özelleştirilebiliyor.'
- 0:35: Koyu ajan arayüzü: code-review preset dosyaları, preset_validate, 'Removed dynamic Plugin probe-4' mesajı, altyazı 'araç var.'
- 0:38: Kurulum promptu: 'Şu projeyi benim için kur: https://github.com/deepseek-ai/deepseek-harness', 'model' ve 'Yorumlara "model" yaz.' yazıları, Kopyala düğmesi
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Kurulum komutlarındaki depo adı OCR'da bozuk (deepseek-al/hamness); deepseek-ai/deepseek-harness olarak yorumlandı.
- 180 bin yıldız, 53 araç ve 'DeepSeek'in kendi çıkardığı' iddiaları doğrulanmadı; ekranda 159 eklenti görünüyor.
- DeepSeek-V3 ve Gemma-4'ün Harness içinde nasıl kullanıldığı net değil; yalnız OCR'da görünüyor.
- Ekranda 'Go' ve 'Snake game' gibi öğeler bir menüde görünüyor, videoda kullanıldığı belli değil.
- Konuşmadaki 'Kulod' ifadesi Claude'a işaret ediyor olabilir.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/deepseek-al/deepseek-harness | 0:03 | ekran | evet |
| https://github.com/deepseek-ai/deepseek-harne | 0:16 | ekran | evet |
| https://github.com/deepseek- | 0:38 | ekran | evet |
| https://github.com/deepseek-ai/deepseek-harness | 0:05 | ekran | evet |
| https://github.com/deepseek-ai/deepseek-harness | 0:16 | ekran | evet |
| https://github.com/deepseek-ai/deepseek-harness | 0:38 | ekran | evet |
## İş akışı
- 1. adım — Projenin GitHub deposu ve yıldız sayısı gösterilir — araçlar: GitHub, DeepSeek Harness
- 2. adım — Eklenti ayarları ekranında her parçanın eklenti olduğu gösterilir — araçlar: DeepSeek Harness, Cordis
- 3. adım — Depo klonlanır — araçlar: Git
- 4. adım — Bağımlılıklar kurulur ve proje derlenir — araçlar: pnpm
- 5. adım — Web arayüzü başlatılır — araçlar: pnpm, dsh
- 6. adım — Model seçimi gösterilir (DeepSeek-V3, Gemma-4) — araçlar: DeepSeek-V3, Gemma-4
- 7. adım — Ajan preset oluşturulur, doğrulanır ve geçici eklenti kaldırılır — araçlar: DeepSeek Harness, editing-cordis-compositions
- 8. adım — Kurulum promptu yapay zekâya yapıştırılmak üzere gösterilir — araçlar: DeepSeek Harness
## Promptlar
- DeepSeek Harness kurulum rehberi — Projeyi (DeepSeek Harness deposu) baştan sona kur; kullanıcı kod yazmıyor. Kurulum bitince hazır araçları kategori kategori listele, hangi modeli bağlayacağını sor, ücretli seçenek önerirsen ücretsiz alternatif de yaz, model bağlanınca tek örnek soruyla test edip sonucu göster.
- Tek işi olan küçük ajan kartı — Ajan kartına göre küçük bir ajan kur: ajan adı, tek işi, girdi, çıktı, sıklık, yazılacak yer; adımları maddele, hangi hazır aracı kullanacağını söyle, 53 aracın hepsini açma, planı yazıp onay al.
ikinci göz KAPALI: --ikinci-goz yok
