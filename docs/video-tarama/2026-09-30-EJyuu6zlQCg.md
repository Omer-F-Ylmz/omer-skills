# 5 Claude Code skills I use every single day
## Künye
5 Claude Code skills I use every single day · Matt Pocock · süre: 16:42 · en-orig · https://youtu.be/EJyuu6zlQCg
motor: parti 2026-09-30-uzun-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (6)
## Özet
Matt Pocock, Claude Code ile her gün kullandığı 5 skill'i anlatıyor: grill-me (plan hakkında amansız soru-cevap ile ortak anlayış), write-a-prd (PRD'yi GitHub issue olarak yazar), prd-to-issues (PRD'yi dikey dilimlere ve bağımlılık ilişkili issue'lara böler), tdd (kırmızı-yeşil-refactor döngüsü) ve improve-codebase-architecture (sığ modülleri derinleştirme, paralel alt ajanlarla farklı arayüz tasarımları, refactor RFC). Temel fikir: hafızasız ajanlara katı süreç gerekir; ajanlara insan gibi davranmak kod kalitesini artırır. Video sonunda 'Claude Code for Real Engineers' kohort kursu tanıtılıyor.
## Bölümler
- 0:00 Giriş
- 1:18 grill-me
- 3:55 write-a-prd
- 6:00 prd-to-issues
- 8:29 tdd
- 12:04 improve-codebase-architecture
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| grill-me | yok | skill | yok | Plan hakkında ortak anlayışa varana dek kullanıcıyı tasarım ağacının her dalı üzerinden sorguya çeker; kod tabanından cevaplanabilen soruları kendisi araştırır. | 1:18 | Interview me relentlessly about every aspect of this plan until we reach a shared understanding. |
| write-a-prd | yok | skill | yok | Ayrıntılı açıklama alır, repoyu inceler, kullanıcıyı sorgular, modülleri çizer ve PRD'yi şablonla GitHub issue olarak yazar. | 3:55 | Terminalde /write-a-prd-user çalıştırılıyor; 'step 4 — sketching out the major modules' yanıtı. (karede: EKSİK: karede_gorulen (kare gönderildi, karede görülen boş olamaz)) |
| prd-to-issues | yok | skill | yok | PRD'yi tracer-bullet mantığıyla dikey dilimlere, bloklama ilişkili bağımsız GitHub issue'larına böler. | 6:00 | it takes a PRD, takes the destination, and it turns it into a Kanban board |
| tdd | yok | skill | yok | Ajanı kırmızı-yeşil-refactor döngüsüne yönlendirir; arayüz değişikliklerini onaylatır, tek seferde bir test yazdırır. Refactor, mocking ve derin modül dokümanları içerir. | 9:30 | it basically forces the agent, or encourages the agent rather, to follow a red-green-refactor loop. |
| improve-codebase-architecture | yok | skill | yok | Kod tabanını keşfeder, derinleştirme adaylarını listeler, 3 paralel alt ajanla farklı arayüzler tasarlatır ve refactor RFC'yi GitHub issue olarak açar. | 12:04 | spawn three subagents in parallel, each of which must produce a radically different interface |
| Ralph loop | yok | iş akışı | yok | Her GitHub issue'yu bitene kadar döngüyle uygulayan otonom ajan döngüsü; TDD skill'iyle yönlendirilir. | 4:56 | I have a Ralph loop that just loops over each issue until it's done. |
| Araştırma dosyasıyla grill-me skill'ini başlatmak | yok | prompt | yok | @docs/research/incremental-document-editing.md /grill-me I'd like to think about adding this to the... | 2:48 | kaynak: kare |
| Grill oturumundan sonra PRD yazma skill'ini çağırmak | yok | prompt | yok | /write-a-prd-user | 4:25 | kaynak: kare |
## Açıklama bağlantıları
- https://aihero.dev/s/egrQdu — aihero.dev kısa link; içeriği doğrulanamadı (muhtemelen kurs veya skill deposu) · aday: hayır · Hedef görülmedi; videoda skill'lerin ve kursun linkinin aşağıda olduğu söyleniyor, hangisi olduğu belirsiz.
- https://aihero.dev/s/ooKL2Q — aihero.dev kısa link; içeriği doğrulanamadı · aday: hayır · Hedef belirsiz; muhtemelen arayüz/refactor veya red-green-refactor videosu ya da skill'ler.
- https://aihero.dev/s/tbyzF8 — aihero.dev kısa link; içeriği doğrulanamadı · aday: hayır · Hedef belirsiz; muhtemelen kurs sayfası.
- https://twitter.com/mattpocockuk — Matt Pocock'un Twitter profili · aday: hayır · Sosyal medya profili, araç/skill değil.
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kurs satış sayfası (landing): koyu tema, sol başlık/alt başlık, sağda fiyat kartı, CTA butonu ve geri sayım | AIhero 'Claude Code for Real Engineers' sayfası: US $477 (üstü çizili $795, %40 indirim), 'Enroll' düğmesi, 30 günlük iade garantisi, 7 gün 9 saat 25 dk 53 sn geri sayım, Andrej Karpathy alıntısı. (karede: Koyu sayfa; başlık 'Claude Code for Real Engineers', $477, üstü çizili $795, 'Save 40%', sarı 'Enroll' düğmesi, geri sayım 7/9/25/53.) | 1:09 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Kodun kalitesi bu skill'ler sayesinde belirgin biçimde arttı. | 0:00 | özellik |
| Kurs 2 haftalık kohort, 30 Mart'ta başlıyor ve 7 gün daha %40 indirimli. | 1:09 | sayısal |
| Grill-me oturumunda Claude, kod tabanını keşfettikten sonra numaralı sorular sordu; kareye göre 16. soru system prompt hakkındaydı. | 2:48 | sayısal |
| Skill'ler uzun olmak zorunda değil; grill-me yalnızca üç cümle ve çok etkili. | 3:19 | özellik |
| Grill-me oturumları karmaşık özelliklerde 30-45 dakika ve 30-50 soruya kadar sürebiliyor. | 3:19 | sayısal |
| Claude Code plan modunda ortak anlayış oluşmadan erken plan üretme eğiliminde; grill-me bunu engelliyor. | 2:18 | karşılaştırma |
| PRD, GitHub issue olarak gönderiliyor; örnekte #544 numaralı, kapalı 'Incremental Document Editing for Article Writer' issue'su. | 5:26 | özellik |
| Karmaşık PRD 4 dikey dilime bölündü; ilk dilim 28 testli saf fonksiyon düzenleme motoruydu. | 8:29 | sayısal |
| Modül planı: yeni Document Editing Engine (applyEdits, saf fonksiyon) ve replace/insert_after/rewrite düzenlemeleri; kararlar 16 maddelik özetle listelendi. | 5:26 | özellik |
| İyi TDD, ajan çıktısını iyileştirmenin en tutarlı yolu oldu. | 9:30 | karşılaştırma |
| LLM'ler kendi bağlamındaki kodu refactor etmeye isteksiz; bağlam temizlenirse daha az bağlı kalıyorlar. | 11:31 | karşılaştırma |
| Büyük refactor'da skill bazen 5 alt ajan başlatabiliyor; ideal olarak aynı anda tek aday üzerinde çalışılmalı. | 13:05 | öneri |
| Architecture skill haftada bir veya hızlı geliştirme sonrası çalıştırılmalı. | 14:06 | öneri |
## Kareden okunanlar
- 0:30: Kitaplıklı odada mikrofonlu, gözlüklü konuşmacı; ekranda metin yok.
- 1:09: AIhero kurs sayfası: Claude Code for Real Engineers, 30 Mart–10 Nisan 2026, $477 (üstü çizili $795), Save 40%, Enroll, 30-Day Money-Back Guarantee, geri sayım 7 gün 9 sa 25 dk 53 sn.
- 2:48: Terminal: Claude Code v2.1.76, Opus 4.6 (1M context), /clear, '/grill-me' komutu, 'Skill(grill-me) Successfully loaded skill', Explore (33 tool uses · 95.7k tokens · 1m 29s).
- 3:37: Question 16: The system prompt; tek prompt/koşullu araçlar veya koşullu prompt bölümleri seçenekleri; kullanıcı 'Yeah, conditional prompt sections.'
- 4:25: Karar özeti 5-16 (agent factory, writeDocument, editDocument, client-side tool execution, streaming, step count 5, persistence), '/write-a-prd-user', step 4 modül taslağı.
- 5:26: GitHub issue #544 (Closed), Problem/Solution/User Stories; split-pane editör, Monaco toggle, writeDocument ve editDocument araçları, localStorage.
## Belirsizlikler
- Açıklamadaki üç aihero.dev kısa linkinin hedefi doğrulanamadı; skill deposu ve kurs linki olabilir.
- Skill deposunun GitHub URL'si videoda verilmiyor; repo_url boş bırakıldı.
- Kare 2:48'deki grill-me komut metni kesik olduğundan tamamı okunamadı.
- Videoda kurulum/terminal komutu söylenmedi; yalnızca skill çağrıları (/grill-me, /write-a-prd-user) görüldü, kurulum komutu olmadığı için kurulum_komutlar boş.
- Adaylardaki ‘Ralph loop’ ayrı bir araç değil, yazarın kendi iş akışı; tanımı videoda ayrıntılandırılmıyor.
## Atlanan segment oranı
0/20 (paket tam okuma, motor)
