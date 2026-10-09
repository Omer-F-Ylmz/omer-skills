# Someone open-sourced a skill that makes Claude and Codex argue about your code b
## Künye
Someone open-sourced a skill that makes Claude and Codex argue about your code b · adilet.fndr · süre: 0:40 · ? · https://www.instagram.com/reel/DdeHmAstM_j/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-17 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 32476 tk · claude-haiku-5-5: claude-haiku-5-5 · 40700 tk
## Özet
Kısa reel, Claudex Loop adlı açık kaynak (MIT) bir skill'i tanıtıyor. Skill Claude Code ya da Codex içine eklenince iş iki modele yönlendiriliyor. Fable 5.1 planı yazıyor, GPT-6 Astra denetliyor ve en fazla 5 turda onay çıkıyor. Sonra roller değişiyor: GPT-6 Astra kodu yazıyor, Fable temiz oturumda farkı inceliyor. Ekranda /plugin marketplace add ve /plugin install ile kurulum ile 'claudex add auth' örneği gösteriliyor.
## Bölümler
- 0:00 Giriş: repo ve Claudex tanıtımı
- 0:09 Kurulum komutları (plugin marketplace)
- 0:12 Dört skill ve SKILL.md dosyaları
- 0:14 Yönlendirme ve plan turu
- 0:24 Plan onayı ve rol değişimi
- 0:28 GPT-6 Astra inşa eder, Fable inceler
- 0:33 Kendi kodunu denetlememe gerekçesi ve SPLIT çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claudex Loop | yok | skill | https://github.com/chaseai-yt/claudex-loop | Claude Code/Codex'e eklenen; planı bir modelin yazıp diğerinin denetlediği, sonra rolleri değiştiren çapraz model döngüsü skill'i. | 0:09 | /plugin marketplace add chaseai-yt/claudex-loop (karede: kanıttan) /plugin marketplace add chaseai-yt/claudex-loop |
| Claude Code | yok | CLI | yok | Skill'in kurulduğu ve çalıştırıldığı terminal aracı. | 0:00 | Welcome to Claude Code · ~/app (karede: kanıttan) Welcome to Claude Code · ~/app |
| Codex | yok | CLI | yok | Skill'in bırakılabildiği ikinci araç; gözden geçiren ve inşa eden taraf. | 0:00 | drop it inside your Claude or Codex |
| Fable 5.1 | yok | teknik | yok | Planı yazan ve sonra inşayı inceleyen model (claude-fable-5-1). | 0:22 | Fable 5.1 kartı, PLANNER etiketi, claude-fable-5-1 (karede: kanıttan) Fable 5.1 kartı, PLANNER etiketi, claude-fable-5-1 |
| GPT-6 Astra | yok | teknik | yok | Planı denetleyen, sonra kodu yazan model (gpt-6-astra). | 0:22 | GPT-6 Astra kartı, REVIEWER etiketi, gpt-6-astra (karede: kanıttan) GPT-6 Astra kartı, REVIEWER etiketi, gpt-6-astra |
| claudex-route | yok | skill | yok | İşi iki modele yönlendiren skill. | 0:12 | claudex-route · claudex-loop · codex-review · codex-build (karede: kanıttan) claudex-route · claudex-loop · codex-review · codex-build |
| codex-review | yok | skill | yok | Planı denetleyip bulgu üreten skill. | 0:12 | codex-review · round 1 · REVISE · 3 findings (karede: kanıttan) codex-review · round 1 · REVISE · 3 findings |
| codex-build | yok | skill | yok | Onaylı planı kodlayan skill. | 0:12 | codex-build · src/auth.ts +48 -3 (karede: kanıttan) codex-build · src/auth.ts +48 -3 |
| GitHub | yok | teknik | yok | Repo'nun barındığı ve görünürlüğünün public yapıldığı servis. | 0:01 | github · chaseai-yt/claudex-loop · visibility → public (karede: kanıttan) github · chaseai-yt/claudex-loop · visibility → public |
| TypeScript | yok | teknik | yok | Repo dili; tsc --noEmit ile kontrol edildi. | 0:06 | TypeScript MIT 212 forks; tsc --noEmit · ok (karede: kanıttan) TypeScript MIT 212 forks; tsc --noEmit · ok |
| ESLint | yok | CLI | yok | Lint kontrolü, 0 hata. | 0:06 | eslint · 0 errors (karede: kanıttan) eslint · 0 errors |
| Alembic | yok | teknik | yok | Veritabanı migrasyon aracı/klasörü; ekranda 'reading alembic/' satırında geçiyor. | 0:07 | reading alembic/ (OCR) (karede: kanıttan) reading alembic/ (OCR) |
| Claudex ile auth özelliği planlama ve uygulama | yok | prompt | yok | Auth özelliğini ekle: planla ve uygula; plan Fable ile yazılıp GPT-6 Astra ile denetlensin. | 0:14 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /plugin marketplace add chaseai-yt/claudex-loop | Claudex Loop marketplace'ini ekler. (karede: Kare gönderilmedi bu zamanda; OCR metni okundu) | 0:09 | kare |
| /plugin install claudex-loop@claudex-loop | Claudex Loop eklentisini kurar. (karede: Kare gönderilmedi bu zamanda; OCR metni okundu) | 0:11 | kare |
| claudex add auth - plan and implement it | Auth özelliğini iki model döngüsüyle planlatıp uygulatır. (karede: Terminalde claudex add auth — plan and implement it satırı (0:22 karesi)) | 0:14 | kare |
| tsc --noEmit | TypeScript tip kontrolünü dosya üretmeden çalıştırır; ekranda 'ok' döndürüyor. (karede: Gönderilmeyen 0:06 karesinin OCR okuması: 'tsc --noEmit · ok' satırı.) | 0:06 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Fable 5.1 plan yazar, GPT-6 Astra denetler, anlaşana kadar gider; sonra roller değişir. | 0:00 | özellik |
| Repo MIT lisanslı, 2k+ yıldız. | açıklama | sayısal |
| Planlama en fazla 5 tur sürer. | 0:18 | sayısal |
| Model kendi kodunu denetlemez; ikinci görüş en akıllı modelden gelir. | 0:00 | karşılaştırma |
| İş 10 kat hızlanır (ekranda 3.2× faster bench). | 0:07 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ses 0:00 | Claudex skill | Claudex Loop | It's a free skill called Claudex |
| kare 0:09 | /plugin marketplace add | Claudex Loop | /plugin marketplace add chaseai-yt/claudex-loop |
| kare 0:00 | Claude Code | Claude Code | Welcome to Claude Code |
| ses 0:00 | Codex | Codex | inside your Claude or Codex |
| kare 0:22 | Fable 5.1 | Fable 5.1 | claude-fable-5-1 PLANNER |
| kare 0:22 | GPT-6 Astra | GPT-6 Astra | gpt-6-astra REVIEWER |
| kare 0:12 | claudex-route, codex-review, codex-build | Claudex Loop | 4 skills - claudex-loop |
| kare 0:01 | GitHub repo | GitHub | github · chaseai-yt/claudex-loop |
| kare 0:06 | eslint | ESLint | eslint · 0 errors |
| kare 0:06 | tsc --noEmit | TypeScript | tsc --noEmit · ok |
| kare 0:07 | alembic/ okuma | aday değil: konu dışı | reading alembic/ (simüle çıktı) |
| açıklama | Instagram yorum SPLIT DM çağrısı | aday değil: sponsor/reklam | Comment SPLIT and I'll DM you |
| açıklama | MIT lisansı | aday değil: genel kavram | MIT, ★ 2k+ |
## Kareden okunanlar
- 0:00: chaseai-yt created a repository, Private, 8 yıldız, TypeScript, MIT, 212 forks; Claude Code karşılama terminali, no skills installed.
- 0:22: Fable 5.1 PLANNER, GPT-6 Astra REVIEWER, PLAN.md round 1/5, REVISE 3 FINDINGS; terminalde claudex add auth komutu.
- 0:24: they agree; PLAN.md round 3/5, APPROVED, plan approved · swapping roles.
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Fable 5.1, GPT-6 Astra modelleri ve repo sahibi gerçekliği doğrulanamadı; açıklamadaki 'Fable 5' ile 5.1 farkı belirsiz.
- Sözlükteki Go, Inter, Next.js, GPT-5 eşleşmeleri kanıtsız; aday yapılmadı.
- Ekrandaki 3.2× ve 10x iddiaları kurgu görseli olabilir.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/chaseai-yt/claudex-loop | 0:01 | ekran | evet |
## İş akışı
- 1. adım — Yayıncı yeni GitHub reposu oluşturup görünürlüğünü public yapar. — araçlar: GitHub
- 2. adım — Claude Code'u proje dizininde (~/app) açar. — araçlar: Claude Code
- 3. adım — Claude Code'a claudex-loop marketplace'ini ekler (/plugin marketplace add). — araçlar: Claude Code
- 4. adım — Claudex Loop eklentisini kurar (/plugin install). — araçlar: Claude Code, Claudex Loop
- 5. adım — Kurulan 4 skill'i (claudex-route, claudex-loop, codex-review, codex-build) listeler ve SKILL.md dosyalarını açar. — araçlar: Claude Code, claudex-route, codex-build
- 6. adım — Auth görevini verir: 'claudex add auth - plan and implement it'. — araçlar: Claude Code, Claudex Loop
- 7. adım — Görevi iki modele yönlendirir: Claude Fable 5.1 planlayıcı, GPT-6 Astra inceleyici. — araçlar: claudex-route, Claude Fable 5.1, GPT-6 Astra
- 8. adım — Fable 5.1 keşif yapar (38 dosya), gereksinimleri sorgular ve PLAN.md yazar. — araçlar: Claude Fable 5.1, Claude Code
- 9. adım — Plan incelemesi round 1: REVISE, 3 bulgu (cookie SameSite, lockout, CSRF testleri). — araçlar: codex-review, GPT-6 Astra
- 10. adım — Bulgulara göre planı düzeltir ve yeniden gönderir (round 2: 1 bulgu). — araçlar: Claude Fable 5.1, codex-review
- 11. adım — Round 3: 0 bulguyla APPROVED; plan onaylanır. — araçlar: codex-review, GPT-6 Astra
- 12. adım — Rolleri değiştirir: builder=Codex, inspector=Claude. — araçlar: Claudex Loop, Codex, Claude Code
- 13. adım — GPT-6 Astra kodu yazar (src/auth.ts +48 -3). — araçlar: codex-build, GPT-6 Astra
- 14. adım — Fable 5.1 diff'i taze oturumda inceler; 8 satır okur, 0 bulgu. — araçlar: Claude Fable 5.1, Claude Code
- 15. adım — Kontrol: tsc --noEmit ve ESLint çalışır; testler 4/4 geçer. — araçlar: TypeScript, ESLint
- 16. adım — Diff'i kontrol eder (SameSite, CSRF, sır yok) ve yayınlar (shipped). — araçlar: Claudex Loop
## Promptlar
- Claudex ile auth özelliği planlama ve uygulama — Auth özelliğini ekle: planla ve uygula; plan Fable ile yazılıp GPT-6 Astra ile denetlensin.
