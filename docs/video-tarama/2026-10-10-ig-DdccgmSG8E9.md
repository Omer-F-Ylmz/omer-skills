# Comment ‘REPO’ and I’ll DM a full article breaking down each GitHub and how to u
## Künye
Comment ‘REPO’ and I’ll DM a full article breaking down each GitHub and how to u · buildwithneej · süre: 0:00 · ? · https://www.instagram.com/p/DdccgmSG8E9/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-8 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 36353 tk · claude-haiku-5-5: claude-haiku-5-5 · 134085 tk
## Özet
Instagram kaydırmalı görsel gönderisi (13 kart, altyazı ve ses yok): @buildwithneej, bir haftada yaklaşık 40.000 yıldız alan 5 GitHub deposunu tanıtıyor. Depolar: hypit (viral videoyu kodlama ajanıyla düzenlenebilir koda çevirir), Alibaba open-code-review (modelsiz, API anahtarsız kural eşleştirme), colibri (diskten uzman akışıyla dev MoE modelleri çalıştıran tek C dosyası), tinycast (ücretsiz yerel Mac başlatıcı, Raycast uzantılarını çalıştırır) ve Cloudflare security-audit-skill (altı aşamalı güvenlik denetimi). Her kartta kurulum komutu var. Yazar 'REPO' yorumuna DM ile makale vaat ediyor. Yalnızca ilk 8 kartın görseli geldi; 9-13 yalnız OCR metninden okundu.
## Bölümler
- 0:00 Kapak: haftanın 5 GitHub deposu, 40.000 yıldız
- 0:00 01 hypit: viral videoyu ajanla klonla
- 0:00 hypit: yeni kancayla yeniden çalıştır ve kurulum
- 0:00 02 open-code-review: göndermeden önce hatayı yakala
- 0:00 open-code-review: tek komut, API anahtarı yok
- 0:00 03 colibri: 744B modeli kendi donanımında çalıştır
- 0:00 colibri: dokuz model ailesi, tek motor
- 0:00 04 tinycast: ücretsiz kalan Mac başlatıcı
- 0:00 tinycast: 12 MB, Raycast uzantılarını çalıştırır (yalnız OCR)
- 0:00 05 security-audit-skill ve script doğrulaması (yalnız OCR)
- 0:00 Hangisini kullanırdım ve REPO yorum çağrısı (yalnız OCR)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| hypit | yok | CLI | hypit-ai/hypit | Referans viral videoyu kodlama ajanıyla senaryo, altyazı, B-roll ve yeni yapay zekâ karakteri içeren düzenlenebilir koda çevirir; kanca değiştirip yeniden çalıştırılır. | 0:00 | Clone any viral video with your coding agent. (karede: Kart 2: 01 hypit-ai / hypit başlığı, 9,848 yıldız, 1,208 fork, 7 issue.) |
| open-code-review | yok | CLI | alibaba/open-code-review | Alibaba'nın dahili kod inceleme aracı; değişen dosyaları yerleşik kural setiyle eşleştirip satır satır yorumlar, kural adımı model çağırmaz. | 0:00 | Alibaba open sourced the code review tool it runs internally. (karede: Kart 4: 02 alibaba / open-code-review, 36,335 yıldız, +12.8k bu hafta.) |
| colibri | yok | CLI | JustVugg/colibri | Tek C dosyalı motor; MoE modellerin az kullanılan uzmanlarını diskten akıtarak belleğe sığmayan modelleri çalıştırır. | 0:00 | Colibrì is one C file that streams a model's rarely used parts (karede: Kart 6: 03 JustVugg / colibri, 36,047 yıldız, 3,803 fork.) |
| tinycast | yok | CLI | abue-ammar/tinycast | Ücretsiz, yerel macOS başlatıcı; uygulama açma, pano geçmişi, snippet, pencere yönetimi ve Raycast uzantıları. | 0:00 | Tinycast is the free native alternative. (karede: Kart 8: 04 abue-ammar / tinycast, 6,379 yıldız, 292 fork.) |
| security-audit-skill | yok | skill | cloudflare/security-audit-skill | Cloudflare'in güvenlik denetim skill'i; altı aşamalı denetim, bulguları şemaya karşı script ile doğrular, 65 paket test içerir. | 0:00 | cloudflare / security-audit-skill — A coding-agent skill for multi-phase security audits. (karede: Görsel 10-11 yalnız OCR metni: cloudflare / security-audit-skill, 12,482 yıldız, JSON şema ve 65 test. Görsel gönderilmedi.) |
| Raycast | yok | CLI | yok | tinycast'ın alternatifi olduğu Mac başlatıcı; uzantıları tinycast'ta çalışır, dışa aktarımı okunur. | 0:00 | Raycast moved its AI to pay per credit on September 10 (karede: Kart 8: açıklama metni Raycast'in yapay zekâyı krediye geçirdiğini ve tinycast'ın ücretsiz alternatif olduğunu anlatıyor.) |
| npx skills | yok | CLI | yok | hypit ve security-audit-skill skill'lerini kurmak için kullanılan komut. | 0:00 | npx skills add hypit-ai/hypit -g · kanıt: kare (karede: Kart 3: HYPIT · GET IT kutusunda npx skills add hypit-ai/hypit -g.) |
| npm | yok | CLI | yok | hypit ve open-code-review paketlerini global kurar. | 0:00 | npm install --global @hypit/hypit (karede: Kart 3 ve 5: npm install komutları kutularda görünüyor.) |
| Homebrew | yok | CLI | yok | tinycast'ı brew tap ve cask ile kurar; Gatekeeper işaretini temizler. | 0:00 | install through Homebrew and it clears the Gatekeeper flag (karede: Görsel 9 yalnız OCR: brew tap ve brew install tinycast --cask satırları. Görsel gönderilmedi.) |
| mixture of experts | yok | teknik | yok | Yalnız gereken uzman parçaları uyandıran model mimarisi; colibri bu uzmanları diskten akıtır. | 0:00 | mixture of experts = a model that wakes up only the parts it needs (karede: Kart 6: altta mixture of experts tanım kutusu.) |
| coli | yok | CLI | JustVugg/colibri | colibri motorunun komutu; model dosyasına yönlendirilip 'coli chat' ile sohbet başlatılır. | 0:00 | COLI_MODEL=/path/to/model ./coli chat (karede: Kart 7: COLIBRÌ · GET IT kutusunda tar xzf ve COLI_MODEL komutları, üstte hummingbird sohbet örneği.) |
| ocr delegate | yok | CLI | alibaba/open-code-review | Değişen dosyalara hangi inceleme kurallarının uygulandığını modelsiz yazdırır; SQL injection kuralını 0.086 sn'de döndürdü. | 0:00 | Run ocr delegate and it prints which of its review rules · kanıt: kare (karede: Kart 5: koyu terminal kutusunda [ocr] code_search ve internal/auth/login.go:42-45 çıktısı.) |
| GitHub | yok | iş akışı | yok | Beş deponun barındığı platform; kartlarda depo kartı olarak gösterilir. | 0:00 | 5 GitHub repos that took off this week (karede: Kart 1: başlıkta GitHub logosu ve '5 GitHub repos that took off this week'.) |
| Node.js | yok | teknik | yok | Hypit için Node 22 veya üzeri gerekiyor; security-audit-skill'in doğrulayıcıları da Node ile yazılmış. | 0:00 | 'Node 22 or newer.' (Hypit kurulum notu) · kanıt: kare (karede: 3/13 slaytta kurulum kutusunun altındaki 'Node 22 or newer' notu.) |
| Git | yok | teknik | yok | open-code-review için Git 2.41 sürümü gerekiyor. | 0:00 | 'Needs Git 2.41. Alibaba's repo, another project shares the name.' (karede: 5/13 slaytta kurulum kutusunun altındaki 'Needs Git 2.41' notu.) |
| colibri'nin sohbet çıktısını göstermek (sinek kuşu örneği) | yok | prompt | yok | Colibri sohbetinde kullanıcı, sinek kuşunun havada nasıl asılı kaldığını üç kısa cümleyle açıklamasını istiyor. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx skills add hypit-ai/hypit -g | hypit skill'ini global kurar (karede: Kart 3: HYPIT · GET IT kutusunun ilk satırı.) | 0:00 | kare |
| npm install --global @hypit/hypit | hypit CLI paketini global kurar (Node 22+) (karede: Kart 3: HYPIT · GET IT kutusunun ikinci satırı.) | 0:00 | kare |
| npm install -g @alibaba-group/open-code-review | open-code-review CLI'ını global kurar (Git 2.41 gerekir) (karede: Kart 5: OPEN CODE REVIEW · GET IT kutusunun ilk satırı.) | 0:00 | kare |
| ocr delegate preview | Değişen dosyalara uygulanan inceleme kurallarını modelsiz önizler (karede: Kart 5: kutunun ikinci satırı.) | 0:00 | kare |
| tar xzf colibri-v1.11.0-macos-arm64.tar.gz | colibri hazır sürümünü arşivden çıkarır (karede: Kart 7: COLIBRÌ · GET IT kutusunun ilk satırı.) | 0:00 | kare |
| COLI_MODEL=/path/to/model ./coli chat | Model dosyasını gösterip colibri sohbetini başlatır (karede: Kart 7: kutunun ikinci satırı.) | 0:00 | kare |
| brew tap abue-ammar/tinycast | tinycast Homebrew deposunu ekler (karede: Görsel 9 yalnız OCR: brew tap abue-ammar/tinycast; görsel gönderilmedi.) | 0:00 | kare |
| brew install tinycast --cask | tinycast'ı kurar ve Gatekeeper işaretini temizler; OCR sırası karışık (karede: Görsel 9 yalnız OCR: brew install tinycast --cask; görsel gönderilmedi.) | 0:00 | kare |
| npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit | Cloudflare güvenlik denetim skill'ini kurar; OCR parçalı, kısmen yeniden kurgulandı (karede: Görsel 11 yalnız OCR: GET IT kutusu parçaları; görsel gönderilmedi.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 5 depo 7 günde toplam yaklaşık 40.000 yıldız aldı. | 0:00 | sayısal |
| hypit ücretsiz; çağırdığı video modelleri ayrıca faturalanır; README örneklerinin her biri yaklaşık bir dolar. | 0:00 | sayısal |
| hypit yeni yapay zekâ karakteri üretir, gerçek yüzü görüntüye yapıştırmaz. | 0:00 | özellik |
| open-code-review kural adımı API anahtarı ve model çağrısı olmadan 0.086 saniyede SQL injection kuralını döndürdü. | 0:00 | sayısal |
| README'ye göre 744 milyar parametreli model 25 GB'lık dizüstünde yaklaşık 10-20 saniyede bir token ile çalışıyor. | 0:00 | sayısal |
| colibri dokuz model ailesini 7 milyar ile 2.8 trilyon parametre arasında çalıştırır; hız diske bağlıdır, NVMe grafik karttan önemlidir. | 0:00 | özellik |
| Raycast yapay zekâsını 10 Eylül'de krediye geçirdi, beş gün sonra özür diledi; tinycast ücretsiz alternatiftir. | 0:00 | karşılaştırma |
| tinycast 12 MB, Raycast uzantılarını Swift ile yerel çalıştırır; beta 72.6 MB bellekte kalıyor; macOS 26+ gerekir. | 0:00 | sayısal |
| security-audit-skill altı aşamalıdır, bulgular JSON şemaya karşı doğrulanır, 65 test geçer, MIT lisanslı, 75 ajana kurulur, çok token harcar. | 0:00 | özellik |
| Yazarın tercihi: open code review ve security audit kuruyor, hypit ücretsiz araç ama ücretli render, tinycast'a geçiyor, colibri gerçek donanım ister. | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 | GitHub | GitHub | 5 GitHub repos that took off this week |
| kare 2 | hypit-ai/hypit | hypit | Clone any viral video with your coding agent. |
| kare 2 | coding agent tanımı | aday değil: genel kavram | coding agent = an AI that runs commands |
| kare 3 | npx skills add | npx skills | npx skills add hypit-ai/hypit -g |
| kare 3 | npm install --global | npm | npm install --global @hypit/hypit |
| kare 3 | Node 22 | aday değil: genel kavram | Node 22 or newer. |
| kare 3 | SWAP HOST/EFFECT/TOPIC ızgarası | hypit | REFERENCE, SWAP HOST, SWAP EFFECT, SWAP TOPIC |
| kare 4 | alibaba/open-code-review | open-code-review | Alibaba open sourced the code review tool |
| kare 4 | code review tanımı | aday değil: genel kavram | code review = a second pair of eyes |
| kare 5 | ocr delegate | ocr delegate | Run ocr delegate |
| kare 5 | code_search | aday değil: başka adayın parçası (open-code-review) | [ocr] code_search "password.*hash" |
| kare 5 | Git 2.41 | aday değil: genel kavram | Needs Git 2.41. |
| kare 6 | JustVugg/colibri | colibri | Colibrì is one C file |
| kare 6 | mixture of experts | mixture of experts | mixture of experts = a model that wakes up |
| kare 7 | coli chat | coli | type coli chat |
| kare 7 | NVMe sürücü | aday değil: genel kavram | a fast NVMe drive does more |
| kare 8 | abue-ammar/tinycast | tinycast | Tinycast is the free native alternative. |
| kare 8 | Raycast | Raycast | Raycast moved its AI to pay per credit |
| OCR görsel 9 | Homebrew | Homebrew | install through Homebrew |
| OCR görsel 9 | Activity Monitor ekran görüntüsü | aday değil: konu dışı | Activity Monitor screenshot shows 72.6 MB |
| OCR görsel 10 | cloudflare/security-audit-skill | security-audit-skill | cloudflare / security-audit-skill |
| OCR görsel 11 | https://github.com/cloudflare/security-audit-skill | security-audit-skill | https://github.com/cloudflare/ |
| OCR görsel 11 | JSON şeması ve Node doğrulayıcılar | aday değil: başka adayın parçası (security-audit-skill) | match a small JSON schema, two Node validators |
| açıklama | #claude #claudecode #codex | aday değil: konu dışı | #claude #claudecode #github #codex #opensource |
| açıklama | REPO yorum çağrısı ve DM | aday değil: konu dışı | Comment 'REPO' and I'll DM a full article |
## Kareden okunanlar
- Kare 1 (kapak): @buildwithneej; TRENDING · WEEK OF SEP 18; 5 GitHub repos that took off this week; 40,000 stars combined in 7 days; SAVE FOR LATER; 5 turuncu mascot.
- Kare 2: 01 hypit-ai/hypit: 7 issue, 9,848 yıldız, 1,208 fork; +9.5k bu hafta; coding agent tanımı.
- Kare 3: Rerun it with a new hook; REFERENCE/SWAP HOST/SWAP EFFECT/SWAP TOPIC; npx skills add ve npm install; Node 22.
- Kare 4: 02 alibaba/open-code-review: 230 issue, 36,335 yıldız, 2,587 fork; +12.8k.
- Kare 5: ocr delegate terminali, internal/auth/login.go:42-45, bcrypt ≥ 12 önerisi; npm install ve Git 2.41 notu.
- Kare 6: 03 JustVugg/colibri: 146 issue, 36,047 yıldız, 3,803 fork; +6.3k; 744B model.
- Kare 7: coli chat sohbeti (hummingbird); tar xzf colibri-v1.11.0-macos-arm64.tar.gz; Apache-2.0; v1.3.0 güvenlik yaması notu.
- Kare 8: 04 abue-ammar/tinycast: 56 issue, 6,379 yıldız, 292 fork; +3.3k; Raycast 10 Eylül kredi geçişi.
## Belirsizlikler
- Gönderi görsel olduğu için süre 0:00; tüm zamanlar 0:00 olarak yazıldı, kart sırası bölümlerde.
- Görsel 9-13 gönderilmedi; bu kartlardaki bilgi yalnız OCR metninden, brew ve Cloudflare komutları OCR'da karışık.
- #claude #claudecode #codex etiketleri yalnız hashtag; araçlar videoda gösterilmediği için aday yapılmadı.
- hypit'in hangi video modellerini çağırdığı belirtilmiyor.
- open-code-review için 'başka bir proje aynı adı taşıyor' notu var; hangisi belirtilmiyor.
- Yorumlar girişsiz alınamadı; yorumlardaki URL ve araçlar bilinmiyor.
- Dökümdeki 'Descript' sözlük eşleşmesi gönderide geçmiyor, alınmadı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/cloudflare/security-audit-skill | 0:00 | ekran | evet |
## İş akışı
- 1. adım — Kapak ve 5 repo listesini tanıtma (trend, toplam 40.000 yıldız) — araçlar: GitHub
- 2. adım — Hypit reposunu ve ne işe yaradığını tanıtma — araçlar: Hypit, GitHub
- 3. adım — Hypit skill'ini genel olarak kurma — araçlar: skills, npx
- 4. adım — Hypit CLI'ını global kurma (Node 22+ gerekir) — araçlar: npm, Node.js
- 5. adım — Referans videoyu coding agent'a verip düzenlenebilir dosyaya çevirme — araçlar: Hypit
- 6. adım — Hook, sunucu, dil ve en-boy oranını değiştirip tek komutla yeniden render etme — araçlar: Hypit
- 7. adım — open-code-review'ı npm ile global kurma (Git 2.41 gerekir) — araçlar: npm, Git, open-code-review
- 8. adım — ocr delegate preview ile değişen dosyalar için kuralları listeleme (modelsiz) — araçlar: open-code-review
- 9. adım — Bilerek bozuk login sorgusunu tarayıp SQL injection kuralını 0,086 sn'de yakalama — araçlar: open-code-review
- 10. adım — colibri arşivini tar ile açma — araçlar: tar, colibri
- 11. adım — COLI_MODEL ile model yolunu verip coli chat ile sohbet etme — araçlar: colibri
- 12. adım — tinycast'i Homebrew tap ve cask ile kurma — araçlar: Homebrew, tinycast
- 13. adım — tinycast'in Raycast dışa aktarımını okuduğunu ve Raycast eklentilerini çalıştırdığını anlatma — araçlar: tinycast, Raycast
- 14. adım — security-audit-skill'i npx skills ile kurma — araçlar: skills, npx, security-audit-skill
- 15. adım — Denetimi 6 fazda çalıştırma, bulguları script ile JSON şemasına doğrulama, 65 testi çalıştırma — araçlar: security-audit-skill, Node.js
## Promptlar
- colibri'nin sohbet çıktısını göstermek (sinek kuşu örneği) — Colibri sohbetinde kullanıcı, sinek kuşunun havada nasıl asılı kaldığını üç kısa cümleyle açıklamasını istiyor.
ikinci göz KAPALI: --ikinci-goz yok
