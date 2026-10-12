# Claude Code Tutorial: Skills (The Part Most Tutorial Miss)
## Künye
Claude Code Tutorial: Skills (The Part Most Tutorial Miss) · Sambit Automation Labs · süre: 8:29 · en-orig · https://youtu.be/zSngJFKTsrM · şema 2
motor: parti 2026-10-11-short-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 45865 tk · claude-haiku-5-5: claude-haiku-5-5 · 66818 tk
## Özet
Video, Claude Code'da Skill ile prompt'un farklı katmanlar olduğunu bir izin takip uygulamasındaki bakiye hatası üzerinden anlatır. Önce hata skill olmadan düzeltilir. Sonra haftalık tekrarlanan bir hata ayıklama süreci için bug-fix SKILL.md yazılır ve küçük prompt ile yeniden denenir. Karar testi: iş sözlerle mi biter, yoksa sistemi değiştiren tekrarlanabilir adımlar mı var? Üç vaka (yalnız prompt, skill, hiçbiri) gösterilir. Özet kural: sorunu prompt'la, süreci skill'le anlat. Bir skill'in bakım maliyeti olduğu vurgulanır.
## Bölümler
- 0:00 Çoğu Claude Code eğitimi Skill'leri neden kaçırıyor
- 0:45 Prompt ve Skill: farklı katmanlar
- 1:45 Tekrar ne zaman yapıyı hak eder
- 3:00 Bir Skill'i yeniden kullanılabilir yapan nedir
- 4:30 Bakım dengesi
- 5:30 Skill için 2 soruluk test
- 6:30 Sırada ne inşa edilecek
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Hatayı bulup düzelten, testleri çalıştıran ana yapay zekâ kodlama aracı | 0:00 | Does a Claude code skill replace a prompt? |
| Skills | yok | skill | yok | Gerektiğinde bağlama yüklenen yeniden kullanılabilir markdown talimatları | 0:45 | A skill is loaded only when needed. Its instructions live inside a markdown file. |
| bug-fix | yok | skill | yok | Leave-tracker için hata düzeltme iş akışını tanımlayan SKILL.md; /bug-fix olarak çalıştırıldı | 4:22 | Ran skill/bug-fix (karede: Etkinlik listesinde 'Ran skill /bug-fix' satırı vurgulanmış) |
| SKILL.md | yok | teknik | yok | Skill talimatlarını ve name/description front matter'ını tutan markdown dosyası | 3:44 | Allow Claude to write SKILL.md? (karede: İzin penceresi: .claude/skills/bug-fix/SKILL.md yazılıyor, name: bug-fix ve description satırları) |
| node --test | yok | CLI | yok | Node'un yerleşik test çalıştırıcısı; en küçük ilgili testi çalıştırmak için | 1:33 | node --test test/regression/balance.test.js (karede: SKILL.md içinde bash bloğunda node --test test/regression/balance.test.js) |
| npm | yok | CLI | yok | npm test ve npm run gen komutları için paket yöneticisi | 1:33 | Finish with npm test to confirm nothing else broke. (karede: SKILL.md'de 'npm test' ve 'npm run gen' geçiyor) |
| grep | yok | CLI | yok | Fonksiyonu kullanan testleri bulmak için arama komutu | 1:30 | Use grep -rn "<function or module name>" test/ (karede: SKILL.md bölüm 1'de grep -rn örneği) |
| gen-leave-types.mjs | yok | teknik | yok | src/generated dosyalarını üreten betik; elle düzenlenmemeli | 1:30 | src/generated/ is produced by scripts/gen-leave-types.mjs (karede: SKILL.md bölüm 2 metni) |
| JavaScript | yok | teknik | yok | Leave-tracker projesinin yazıldığı dil (.js/.mjs dosyaları) | 1:30 | src/approvals.js, test/decisions.test.js (karede: Dosya adları .js ve .mjs uzantılı) |
| Montserrat | yok | teknik | yok | Başlıklarda kullanılan kalın font (görsel olarak benzerlik; kesin değil) | 0:00 | Kalın geometrik başlık fontu · kanıt: kare (karede: 'SKILL VS PROMPT?' başlığı) |
| TextEdit | yok | teknik | yok | SKILL.md'yi açmak için macOS metin düzenleyicisi | 1:30 | Open with TextEdit (karede: SKILL.md önizlemesinde 'Open with TextEdit' düğmesi) |
| Node.js | yok | CLI | yok | node --test ile test dosyalarını çalıştıran Node yerleşik test çalıştırıcısı. | 1:32 | node —test test/regression/balance.test.js · kanıt: kare (karede: node —test test/regression/balance.test.js) |
| sed | yok | CLI | yok | October rapor fikstüründeki Priya satırını 10 days'ten 7 days'e değiştirmek için kullanılan metin düzenleme komutu. | 2:45 | sed -i '' 's/^Priya Raman 10 days$/Priya Raman 7 days/' (karede: kanıttan) sed -i '' 's/^Priya Raman 10 days$/Priya Raman 7 days/' |
| İzin bakiyesi hatasını skill olmadan düzeltmek | yok | prompt | yok | Onaylı iznin eski bakiyeyi neden koruduğunu bul. Değiştirmeden önce ilgili dosyaları oku. Hatayı düzelt ve ilgili testleri çalıştır. | 1:11 | kaynak: kare |
| Aynı hatayı bug-fix skill'i ile kısa prompt'la çözmek | yok | prompt | yok | Onaylanan izin bakiyeyi düşürmüyor. Nedenini bul ve düzelt. (bug-fix skill'i süreci sağlar) | 4:14 | kaynak: kare |
| Yalnız açıklama gereken vaka: yalnız prompt | yok | prompt | yok | Bir izin onaylandıktan sonra bakiyenin neden yanlış olduğunu açıkla; hiçbir şeyi değiştirme. | 5:44 | kaynak: kare |
| Farklı hatada skill'in yeniden kullanımını göstermek | yok | prompt | yok | Onay e-postaları gönderilmiyor; nedenini bul ve düzelt. | 6:56 | kaynak: kare |
| Üçüncü farklı hata örneği | yok | prompt | yok | Tarih doğrulaması bozuk: bir haftalık izin altı iş günü sayılıyor; nedenini bul ve düzelt. | 7:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| grep -rn "<function or module name>" test/ | Kodu kullanan tüm testleri bulur (karede: SKILL.md içinde grep -rn örneği) | 7:24 | kare |
| node --test test/regression/balance.test.js | En küçük ilgili testi çalıştırır (karede: SKILL.md bash bloğu) | 1:32 | kare |
| node --test test/regression/ | Etkilenen alanın regresyon paketini çalıştırır (karede: SKILL.md bölüm 4 bash bloğu) | 1:33 | kare |
| npm test | Tüm testleri çalıştırır (karede: SKILL.md: 'Finish with npm test') | 1:33 | kare |
| npm run gen | Üretilen dosyaları kaynak tablodan yeniden üretir (karede: SKILL.md bölüm 2) | 1:30 | kare |
| /bug-fix | bug-fix skill'ini çalıştırır (karede: 'Ran skill /bug-fix' satırı) | 4:36 | kare |
| node -e '...' (JSON'dan onaylı izinleri listeler) | data/leave.json ve October fikstürünü okuyup onaylı izin kayıtlarını listeler. (karede: Claude onay penceresinde 'Allow Claude to run List October decisions with request details?' ve node -e komutu görünüyor.) | 2:44 | kare |
| sed -i '' 's/^Priya Raman 10 days$/Priya Raman 7 days/' test/fixtures/expected/october-report.txt | October rapor fikstüründeki Priya satırını 10 days'ten 7 days'e değiştirir. (karede: Onay penceresinde 'sed -i' komutu ve 'Priya Raman ... 7 days' ifadesi görünüyor.) | 2:45 | kare |
| cat test/fixtures/expected/october-report.txt && npm test 2>&1 / grep -E "(tests/pass/fail)" | Fikstürü yazdırır, npm test çalıştırır ve yalnızca test sonuç satırlarını filtreler. (karede: Onay penceresinde komutun sonu 'npm test 2>&1 / grep -E' olarak görünüyor.) | 2:45 | kare |
| node --test --test-name-pattern="<test name>" | Tek bir test adını hedefleyerek yalnızca o testi çalıştırır. (karede: SKILL.md'de '--test-name-pattern="<test name>"' ifadesi okunuyor.) | 1:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Skill markdown'ı gerektiğinde Claude'un bağlamına yapıştırılmış gibi girer. | 0:45 | özellik |
| Skill, mevcut isteğin yerini almaz; tekrarlanan prosedürün yeniden yazılmasını önler. | 4:30 | öneri |
| Karar testi: iş sözlerle bitiyorsa yalnız prompt; sistem değişiyor ve adımlar tekrarlanıyorsa skill; hiçbiri tekrar etmiyorsa hiçbiri. | 5:30 | öneri |
| Her skill bakım gerektirir; iş akışı değiştikçe dosya da güncellenmeli. | 3:30 | karşılaştırma |
| Skill akıl yürütmeyi sihirli şekilde iyileştirmez. | 7:30 | özellik |
| Skill'siz çalışmada tüm 27 test geçti; skill'li çalışmada 26 test geçti. | 4:53 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Does a Claude code skill replace a prompt? |
| konuşma 0:45 | Skill | Skills | A skill is loaded only when needed. |
| kare 4:22 | bug-fix skill | bug-fix | Ran skill/bug-fix |
| kare 3:44 | SKILL.md | SKILL.md | Allow Claude to write SKILL.md? |
| kare 1:33 | node --test | node --test | node --test test/regression/balance.test.js |
| kare 1:33 | npm test | npm | Finish with npm test |
| kare 1:30 | grep | grep | Use grep -rn "<function or module name>" test/ |
| kare 1:30 | gen-leave-types.mjs | gen-leave-types.mjs | scripts/gen-leave-types.mjs |
| kare 1:30 | JavaScript dosyaları | JavaScript | src/approvals.js |
| kare 1:30 | TextEdit | TextEdit | Open with TextEdit |
| kare 0:00 | Başlık fontu | Montserrat | Kalın geometrik başlıklar |
| konuşma 0:00 | Prompt | aday değil: genel kavram | A prompt tells Claude what you need now. |
| konuşma 0:00 | İzin takip uygulaması | aday değil: konu dışı | You have an employee leave tracker. |
| konuşma 4:30 | Regresyon testi | aday değil: genel kavram | Then it runs regression coverage. |
| konuşma 7:30 | Terminal ve CLI videosu | aday değil: konu dışı | Next, we will open the terminal on purpose |
| açıklama | Sambit Automation Labs kanalı | aday değil: konu dışı | subscribe to Sambit Automation Labs |
| açıklama | Önceki ve sonraki bölüm | aday değil: konu dışı | Episode 4 ... Episode 6 |
| kare 2:44 | sed komutu | aday değil: genel kavram | sed -i '' 's/^Priya Raman 10 days$/... |
| sözlük | Three.js, Next.js, Descript, Inter, Matter.js | aday değil: konu dışı | Sözlük eşleşmesi bulanık; videoda kullanılmıyor |
## Kareden okunanlar
- 0:00: [ THE QUESTION ] SKILL VS PROMPT?
- 0:45: THREE JOBS, EVERY BUG: Read code, Change code, Verify fix
- 1:03: Bir prompt'un bileşenleri: Context, Constraints, Expected results
- 1:30: SKILL.md: name: bug-fix; 5 numaralı bölüm; üretilen dosyalara dokunma kuralı
- 3:01: Claude özeti: 27 test geçti; src/approvals.js düzeltildi, approvals.test.js eklendi, October raporu 10'dan 7'ye güncellendi
- 3:30: EVERY SKILL IS UPKEEP
- 4:36: Skill'li çalışmada 'Ran skill /bug-fix'; 26 test geçti
- 8:03: Prompt the problem. Skill the process. If nothing repeats, add nothing.
## Belirsizlikler
- Kare görselleri gerçek ekran kayıtlarıyla çizilmiş animasyonlar karışık; Claude Code'un sunucu tarafı model adı gösterilmiyor.
- Sözlük eşleşmeleri (Three.js, Next.js, Descript, Inter, Matter.js vb.) videoda kullanılmıyor, bulanık eşleşme sayıldı.
- Başlık fontu Montserrat tahmini görsel benzerliğe dayanır.
- Skill'siz çalışmada 27, skill'li çalışmada 26 test geçti; fark testin eklenip eklenmemesinden olabilir.
- Ses bölümünde söylenen 'cloud code' ifadesi Claude Code olarak yorumlandı.
- Terminal ve CLI konulu sonraki video yalnızca duyuruldu, kullanılmadı.
## Atlanan segment oranı
0/10 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://youtu.be/zSngJFKTsrM | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — İzin takip uygulamasında hatayı göster: onaylanan izin bakiyeyi düşürmüyor — araçlar: Claude Code
- 2. adım — Skill olmadan hatayı prompt ile tarif et — araçlar: Claude Code
- 3. adım — Claude kodu okuyup approveRequest'te sorunu bulur — araçlar: Claude Code
- 4. adım — Düzeltmeyi yapar ve testleri çalıştırır — araçlar: Claude Code, npm
- 5. adım — Eski fixture'ı güncelleyip testleri yeniden çalıştırır (27 test geçer) — araçlar: Claude Code, npm
- 6. adım — Skill'in katkısını değerlendirir: bu görevde gerekmedi — araçlar: Skills
- 7. adım — Haftalık tekrarlanan süreci bug-fix SKILL.md olarak yazar — araçlar: Claude Code, SKILL.md, bug-fix
- 8. adım — SKILL.md içeriğini inceler — araçlar: SKILL.md, TextEdit
- 9. adım — Aynı hatayı kısa prompt ile bug-fix skill'i kullanarak yeniden çalıştırır — araçlar: Claude Code, bug-fix
- 10. adım — Skill sürecini uygular: testleri incele, düzelt, küçük testi ve regresyonu çalıştır — araçlar: bug-fix, node --test, npm, grep
- 11. adım — Üç vakayı sınar: açıklama, haftalık iş akışı, tek seferlik olay — araçlar: Claude Code
- 12. adım — Farklı hatalarla (e-posta, tarih) skill'in yeniden kullanımını gösterir — araçlar: Claude Code, bug-fix
- 13. adım — Sonuç: sorunu prompt'la, süreci skill'le anlat — araçlar: Claude Code, Skills
## Promptlar
- İzin bakiyesi hatasını skill olmadan düzeltmek — Onaylı iznin eski bakiyeyi neden koruduğunu bul. Değiştirmeden önce ilgili dosyaları oku. Hatayı düzelt ve ilgili testleri çalıştır.
- Aynı hatayı bug-fix skill'i ile kısa prompt'la çözmek — Onaylanan izin bakiyeyi düşürmüyor. Nedenini bul ve düzelt. (bug-fix skill'i süreci sağlar)
- Yalnız açıklama gereken vaka: yalnız prompt — Bir izin onaylandıktan sonra bakiyenin neden yanlış olduğunu açıkla; hiçbir şeyi değiştirme.
- Farklı hatada skill'in yeniden kullanımını göstermek — Onay e-postaları gönderilmiyor; nedenini bul ve düzelt.
- Üçüncü farklı hata örneği — Tarih doğrulaması bozuk: bir haftalık izin altı iş günü sayılıyor; nedenini bul ve düzelt.
ikinci göz KAPALI: --ikinci-goz yok
