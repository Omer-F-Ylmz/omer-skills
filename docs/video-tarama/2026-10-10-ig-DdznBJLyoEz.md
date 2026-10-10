# Comment “COMPACT” and I’ll DM you the link and the setup. Follow so the DM lands
## Künye
Comment “COMPACT” and I’ll DM you the link and the setup. Follow so the DM lands · nocodealex · süre: 0:28 · ? · https://www.instagram.com/reel/DdznBJLyoEz/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-17 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 13500 tk · claude-haiku-5-5: claude-haiku-5-5 · 27379 tk
## Özet
nocodealex, Claude Code için açık kaynak (MIT) bir eklenti olan fast-jev-compaction'ı tanıtıyor. Eklenti /compact özetini değiştirir: kullanıcı ve Claude mesajlarını kelimesi kelimesine korur, yalnızca eski araç çağrılarını ve sonuçlarını (daha önce okunan dosyalar gibi) siler. Silmeden önce ikinci bir model (Jev) her çağrı ve sonuç için tutma kararı verir. Yeterli yer açılamazsa Claude Code'un normal özetine döner. Video, bağlantı ve kurulum için 'COMPACT' yorumu yapılmasını ister.
## Bölümler
- 0:00 Giriş: /compact özetleme sorunu
- 0:05 Açık kaynak, MIT lisanslı Claude Code eklentisi
- 0:08 Mesajlar yeniden yazılmaz
- 0:12 Yalnızca araç çağrıları silinir
- 0:19 Jev ikinci modelin kontrolü
- 0:24 Orijinal mesajlar korunur, çağrı: COMPACT yorumu
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| fast-jev-compaction | yok | plugin | yok | /compact özeti yerine mesajları birebir tutup yalnızca eski araç çağrı ve sonuçlarını temizleyen Claude Code eklentisi | 0:05 | Ekranda 'A CLAUDE CODE PLUGIN' ve 'tamaratran /fast-jev-compaction' görünüyor; anlatıcı da tanıtıyor. (karede: kanıttan) Ekranda 'A CLAUDE CODE PLUGIN' ve 'tamaratran /fast-jev-compaction' görünüyor; anlatıcı da tanıtıyor. |
| Claude Code | yok | CLI | yok | Eklentinin çalıştığı Anthropic kodlama aracı; sürüm 2.1.274 veya üstü gerekir | 0:07 | Ekranda 'A CLAUDE CODE PLUGIN'; açıklamada sürüm şartı yazıyor. (karede: kanıttan) Ekranda 'A CLAUDE CODE PLUGIN'; açıklamada sürüm şartı yazıyor. |
| Claude | yok | teknik | yok | Sohbetin ve eklentinin bağlı olduğu ana yapay zekâ modeli | 0:00 | Stop Claude from summarizing your conversation which usually makes it stupid |
| Jev | yok | teknik | yok | Silmeden önce konuşmayı okuyup her çağrı ve sonuç için tutma kararı veren ikinci model | 0:19 | Ekranda 'JEV' etiketi; açıklamada ikinci model Jev anlatılıyor. (karede: kanıttan) Ekranda 'JEV' etiketi; açıklamada ikinci model Jev anlatılıyor. |
| /compact | yok | CLI | yok | Claude Code'un konuşmayı özetleyen yerleşik komutu; eklenti bunun yerine geçer | 0:00 | Blender üzerinde '/compact' yazısı ve 'missed' etiketi görünüyor. (karede: kanıttan) Blender üzerinde '/compact' yazısı ve 'missed' etiketi görünüyor. |
| TypeSafe | yok | teknik | yok | Jev için gereken API anahtarını sağlayan servis | açıklama | You'll need ... a TypeSafe API key for Jev. |
| Function hooks flag | yok | teknik | yok | Claude Code'da açılması gereken erken erişim işlev kancaları bayrağı | açıklama | early access function hooks flag on |
| Demo sohbetinde kullanıcının verdiği görev talimatı | yok | prompt | yok | Başarısız testi düzelt; src/generated dizinini asla düzenleme. | 0:08 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /compact | Claude Code'un yerleşik konuşma özetleme komutu; eklenti bunun yerine geçer (karede: Blender üzerinde '/compact' yazısı.) | 0:00 | kare |
| npm test | Karede örnek Bash araç çağrısı olarak test çalıştırır (karede: 'Bash(npm test)' kartı, 'ok, 9812 chars' sonucu.) | 0:12 | kare |
| Bash(npm test) | Demo sohbetinde Claude'un çalıştırdığı test komutu; kurulum komutu değil, örnek araç çağrısı. (karede: Silinen kartlardan biri: 'Bash(npm test) ok, 9812 chars') | 0:12 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Projenin GitHub'da yaklaşık 7.000 yıldıza ulaştığı söyleniyor. | 0:00 | sayısal |
| Mesajlar özetlenmez; kullanıcı ve Claude'un her sözü birebir korunur. | 0:08 | özellik |
| Yalnızca eski araç çağrıları ve sonuçları silinir, örneğin daha önce açılan dosyalar. | 0:12 | özellik |
| Silmeden önce ikinci bir model, çağrı ve sonucun tutulup tutulmayacağını kontrol eder. | 0:19 | özellik |
| Yeterli yer açılamazsa Claude Code'un normal özetine geri döner. | açıklama | özellik |
| Claude Code 2.1.274 veya üstü, function hooks bayrağı ve TypeSafe API anahtarı gerekir. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ses 0:00 | Claude | Claude | Stop Claude from summarizing your conversation |
| ses 0:00 | fast-jev-compaction | fast-jev-compaction | It's called fast-gev compaction |
| ses 0:00 | İkinci yapay zekâ kontrolü | Jev | a second AI checks first |
| ses 0:00 | Bağlam penceresi | aday değil: genel kavram | makes your context window pretty fat |
| ses 0:00 | Anne benzetmesi | aday değil: konu dışı | like your mom asking, are you still eating this |
| ses 0:00 | GitHub yıldız sayısı | aday değil: genel kavram | almost 7,000 stars |
| ses 0:00 | COMPACT yorum çağrısı | aday değil: sponsor/reklam | For the link in setup, comment compact. |
| kare 0:00 | /compact | /compact | Blender üzerinde '/compact' yazısı |
| kare 0:00 | auth.ts | aday değil: konu dışı | Found it. Fixing auth.ts. |
| kare 0:00 | src/generated kuralı | aday değil: konu dışı | Never edit src/generated. |
| kare 0:03 | Bash(npm test) | aday değil: başka adayın parçası (fast-jev-compaction) | Bash(npm test) ve TypeError: token is undefined |
| kare 0:03 | npm | aday değil: başka adayın parçası (fast-jev-compaction) | Bash(npm test) |
| kare 0:05 | Open source, MIT license | aday değil: genel kavram | OPEN SOURCE, MIT LICENSE |
| kare 0:05 | tamaratran/fast-jev-compaction | fast-jev-compaction | Ekranda repo yolu |
| kare 0:07 | Claude Code plugin | Claude Code | A CLAUDE CODE PLUGIN |
| kare 0:08 | Örnek mesajlar | aday değil: başka adayın parçası (fast-jev-compaction) | Fix the failing test. |
| kare 0:12 | Read, Grep çağrıları | aday değil: başka adayın parçası (fast-jev-compaction) | Read(README.md), Read(package.json), Grep("auth") |
| kare 0:19 | JEV | Jev | Ekranda 'JEV' etiketi |
| kare 0:27 | Yorum alanı | aday değil: sponsor/reklam | Add a comment... |
| açıklama | TypeSafe API key | TypeSafe | a TypeSafe API key for Jev |
| açıklama | function hooks flag | Function hooks flag | early access function hooks flag on |
| açıklama | Claude Code 2.1.274 | Claude Code | Claude Code 2.1.274 or later |
| açıklama | Hashtagler | aday değil: konu dışı | #claudeai #claude #claudetips #claudecode |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamıyor |
## Kareden okunanlar
- 0:00: 'KEEP CLAUDE SMART IN LONG CHATS' başlığı; blender içinde 'Found it. Fixing auth.ts.' ve 'Never edit src/generated.' kartları; '/compact' yazısı, 'missed' etiketi.
- 0:08: 'NOTHING GETS REWRITTEN' başlığı; 'Fix the failing test. Never edit src/generated.' ve 'On it. I'll read src/a.ts and leave src/generated.' mesajları.
- 0:12: 'ONLY TOOL CALLS CAN GO' başlığı; Read(src/a.ts), Bash(npm test) 9812 chars, Read(README.md) 8688 chars, Grep, Read(package.json) 830 chars kartları; 'it only clears' altyazısı.
## Belirsizlikler
- Altyazıda 'fast-gev compaction' yazıyor; açıklama ve ekranda 'fast-jev-compaction'.
- Repo sahibi ekranda 'tamaratran' olarak okundu; OCR düşük kaliteli, tam URL doğrulanamadı.
- 'TypeSafe' API anahtarı servisi açıklamada geçiyor, videoda gösterilmiyor; ad belirsiz olabilir.
- Yorumlar girişsiz alınamadı.
- Sözlük eşleşmeleri (Redis, Make, context7, Hermes Agent, Go) videoyla ilgisiz bulanık eşleşmeler.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/DdznBJLyoEz/ | açıklama | açıklama | hayır |
| tamaratran/fast-jev-compaction | 0:05 | ekran | evet |
## İş akışı
- 1. adım — Uzun sohbette /compact özetlemesinin bağlamı bozma sorununu anlatır — araçlar: Claude Code, /compact
- 2. adım — fast-jev-compaction eklentisini açık kaynak MIT projesi olarak tanıtır — araçlar: fast-jev-compaction
- 3. adım — Kullanıcı ve Claude mesajlarının birebir korunduğunu gösterir — araçlar: Claude Code
- 4. adım — Yalnızca eski araç çağrı ve sonuçlarının silinebildiğini gösterir — araçlar: fast-jev-compaction
- 5. adım — Jev'in her çağrı ve sonuç için tutma kararı verdiğini anlatır — araçlar: Jev
- 6. adım — Yetersiz yer açılırsa normal özete geri dönüşü ve kurulum şartlarını belirtir — araçlar: Claude Code, TypeSafe
- 7. adım — İzleyiciyi bağlantı için COMPACT yorumu yapmaya çağırır — araçlar: yok
## Promptlar
- Demo sohbetinde kullanıcının verdiği görev talimatı — Başarısız testi düzelt; src/generated dizinini asla düzenleme.
ikinci göz KAPALI: --ikinci-goz yok
