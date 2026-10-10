# Cloudflare, yapay zekâya yazdırdığın uygulamadaki güvenlik açıklarını bulan bir 
## Künye
Cloudflare, yapay zekâya yazdırdığın uygulamadaki güvenlik açıklarını bulan bir  · future_with_serdar · süre: 0:57 · ? · https://www.instagram.com/reel/DeHyIk7KEjW/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-12 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 16202 tk · claude-haiku-5-5: claude-haiku-5-5 · 81166 tk
## Özet
Kısa reel: Cloudflare'in açık kaynak (MIT) security-audit becerisi anlatılıyor. Claude Code'a tek komutla kurulur. Önce uygulamanın haritası çıkarılır, sonra her saldırı sınıfına ayrı avcı ajan atanır. Her bulgu, tek işi onu çürütmek olan bir verifier ajana gider. Sonunda doğrulanmış sorunlar ve en küçük düzeltmeyle rapor çıkar. Notlar: tek çalıştırma bulguların yaklaşık yarısını yakalar, birkaç kez koşturulmalı. Skill ücretsiz ama Claude Code kotası harcanır.
## Bölümler
- 0:00 Giriş: Cloudflare security-audit skill'i
- 0:19 Kurulum: tek komut ve Faz 1 keşif
- 0:23 Avcı ajan ekibi ve saldırı sınıfları
- 0:32 Çürütücü (verifier) ajan
- 0:40 Güvenlik raporu
- 0:45 İki not: birkaç kez koştur, kota harcanır
- 0:54 Yorum çağrısı: rehber
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| security-audit | yok | skill | https://github.com/cloudflare/security-audit-skill | Cloudflare'in açık kaynak, çok aşamalı güvenlik denetimi becerisi | 0:19 | Found 1 skill: security-audit · Installed to Claude Code (karede: kanıttan) Found 1 skill: security-audit · Installed to Claude Code |
| Claude Code | yok | CLI | yok | Skill'in kurulduğu ve çalıştığı kodlama ajanı | 0:19 | terminal · Claude Code (karede: kanıttan) terminal · Claude Code |
| Skills CLI | yok | CLI | yok | npx skills add ile skill kuran komut satırı aracı | 0:21 | npx skills add https://github.com/cloudflare/security-audit-skill (karede: kanıttan) npx skills add https://github.com/cloudflare/security-audit-skill |
| npx | yok | CLI | yok | Skills CLI'yi çalıştıran npm paket çalıştırıcı | 0:19 | $ npx sk (karede: kanıttan) $ npx sk |
| Codex | yok | CLI | yok | Skill'in çalıştığı belirtilen diğer kodlama ajanı | açıklama | Codex ve Cursor'da da çalışıyor |
| Cursor | yok | CLI | yok | Skill'in çalıştığı belirtilen diğer kodlama aracı | açıklama | Codex ve Cursor'da da çalışıyor |
| GitHub | yok | CLI | https://github.com/cloudflare/security-audit-skill | Skill deposunun barındığı servis | 0:21 | github.com/cloudflare/security-audit-skill · MIT (karede: kanıttan) github.com/cloudflare/security-audit-skill · MIT |
| Avcı ajanlar | yok | teknik | yok | Her saldırı sınıfına ayrı izole ajan atama (coverage-led hunting) | 0:23 | Faz 2 · Avcı ajanlar: her saldırı sınıfına ayrı, izole bir ajan (karede: kanıttan) Faz 2 · Avcı ajanlar: her saldırı sınıfına ayrı, izole bir ajan |
| Verifier ajan | yok | teknik | yok | Her bulguyu çürütmeye çalışan bağımsız doğrulayıcı ajan | 0:32 | tek işi o hatanın var olmadığını kanıtlamak olan ayrı bir ajana |
| npm | yok | CLI | yok | npx komutunu sağlayan paket yöneticisi; kurulum komutu npx ile başlıyor | 0:19 | $ npx sk (karede: Terminalde '$ npx sk' komutu görünüyor; npm adı OCR ile eşleşti, ekranda açıkça yazmıyor) |
| argon2 | yok | teknik | yok | Parola hash algoritması; örnek raporda düzeltme önerisi olarak gösteriliyor | 0:41 | düzeltme: argon2/bcrypt ile hash'le (karede: Örnek rapor satırında 'düzeltme: argon2/bcrypt ile hash'le' yazıyor) |
| bcrypt | yok | teknik | yok | Parola hash kütüphanesi; örnek raporda düzeltme önerisi olarak gösteriliyor | 0:41 | düzeltme: argon2/bcrypt ile hash'le (karede: Örnek rapor satırında 'düzeltme: argon2/bcrypt ile hash'le' yazıyor) |
| Güvenlik denetimini başlatma | yok | prompt | yok | Kurulumdan sonra Claude Code'a bu kod tabanının güvenlik denetimini yapmasını söyler. | 0:20 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit | security-audit skill'ini Claude Code'a kurar (karede: Terminalde komut ve 'Found 1 skill: security-audit · Installed to Claude Code' görünüyor.) | 0:21 | kare |
| security audit this codebase | Denetimi başlatan sohbet isteği (karede: Terminalde '> security audit this codebase' satırı.) | 0:20 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Cloudflare kendi 145 deposunda 7.245 doğrulanmış bulgu çıkardı. | 0:00 | sayısal |
| GitHub'da 24 bin yıldızı geçti, lisans MIT. | 0:19 | sayısal |
| Tek çalıştırma bulguların yaklaşık yarısını yakalar; birkaç kez çalıştırılmalı. | 0:45 | öneri |
| Skill ücretsiz, ancak kullanıcının kendi Claude Code kotası harcanır. | 0:51 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Cloudflare | aday değil: konu dışı | Cloudflare, yapay zekaya yazdırdığın uygulamadaki güvenlik açıklarını |
| konuşma 0:00 | security-audit skill | security-audit | güvenlik açıklarını bulan bir yapay zeka becerisi |
| kare 0:19 | Claude Code | Claude Code | terminal · Claude Code |
| kare 0:19 | npx | npx | $ npx sk |
| kare 0:19 | Skills CLI | Skills CLI | Skills CLI; Claude Code, Codex, Cursor vb. |
| açıklama | Codex | Codex | Codex ve Cursor'da da çalışıyor |
| açıklama | Cursor | Cursor | Codex ve Cursor'da da çalışıyor |
| konuşma 0:00 | GitHub | GitHub | GitHub'da 24000 yıldızı geçti |
| kare 0:21 | github.com/cloudflare/security-audit-skill | security-audit | github.com/cloudflare/security-audit-skill · MIT |
| açıklama | Anthropic | aday değil: genel kavram | kodun Anthropic'e gider |
| kare 0:23 | Avcı ajanlar | Avcı ajanlar | Faz 2 · Avcı ajanlar |
| ekran 0:32 | Verifier ajan | Verifier ajan | verifier · tek işi: çürütmek |
| ekran 0:23 | Saldırı sınıfı dosyaları (WEB-PROTOCOL-AND-AUTH, AI-LLM vb.) | aday değil: başka adayın parçası (security-audit) | sınıf dosyaları: WEB-PROTOCOL-AND-AUTH, ATTACK-CLASSES, DATA-ISOLATION |
| konuşma 0:00 | Prompt injection | aday değil: genel kavram | prompt injection bile |
| ekran 0:40 | REPORT.md / findings.json / architecture.md | aday değil: başka adayın parçası (security-audit) | REPoRT.md · security-audit · temsili örnek |
| ekran 0:41 | argon2/bcrypt, middleware, oran sınırı | aday değil: genel kavram | düzeltme: argon2/bcrypt ile hash'le |
| açıklama | MIT lisansı | aday değil: genel kavram | security-audit (MIT, 24 bin yıldız) |
| açıklama | yapay zeka avatarı ve klonlanmış ses | aday değil: konu dışı | yapay zeka avatarı ve klonlanmış ses kullanılmıştır |
| açıklama | #cloudflare #claudecode #siberguvenlik | aday değil: genel kavram | #cloudflare #claudecode #siberguvenlik |
## Kareden okunanlar
- 0:19: KURULUM; 'Claude Code'a tek komut'; terminalde 'npx sk' ve 'Found 1 skill: security-audit · Installed to Claude Code'; kaynak README ve GitHub API 24.653 yıldız, MIT.
- 0:21: Tam npx skills add komutu, 6 faz sekmesi (Keşif...Rapor), 'Faz 1 · Keşif' kutusu ve GitHub depo ekran görüntüsü.
- 0:23: AJAN EKİBİ; 'Faz 2 · Avcı ajanlar'; kaynakta sınıf dosyaları: WEB-PROTOCOL-AND-AUTH, ATTACK-CLASSES, DATA-ISOLATION, AI-LLM, MEMORY-SAFETY, SUPPLY-CHAIN, CLOUD, CLIENT-SIDE, DESKTOP-MOBILE.
## Belirsizlikler
- Video dili belirtilmemiş; altyazının son kısmı bozuk (Groq).
- Yorumlar girişsiz alınamadı; 'denetim' yorumuyla DM'den gelen rehber/link içeriği görülemedi.
- Altyazıda 'Claude Code kotası' bozuk çıkmış; ekran metni ve açıklamayla düzeltildi.
- Açıklamadaki 'kodun Anthropic'e gider' notu videoda sesli geçmiyor.
- Ekrandaki 7.245/145 depo kaynağı olarak Cloudflare blogu (18 Haz 2026) gösteriliyor; blog bağlantısı verilmedi.
- Rapordaki bulgular 'temsili örnek' olarak etiketli, gerçek çıktı değil.
- Videoda yapay zekâ avatarı ve klonlanmış ses kullanıldığı belirtiliyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/cloudflare/securit | 0:20 | ekran | evet |
| https://github.com/cloudflare/security-audit-skill | 0:21 | ekran | evet |
| github.com/cloudflare/security-audit-skill | 0:22 | ekran | evet |
## İş akışı
- 1. adım — Skills CLI ile security-audit skill'ini kurma — araçlar: npx, Skills CLI, Claude Code
- 2. adım — Denetimi başlatma: 'security audit this codebase' — araçlar: Claude Code, security-audit
- 3. adım — Faz 1 keşif: mimari, güven sınırları, giriş yüzeyleri haritası (architecture.md) — araçlar: security-audit
- 4. adım — Faz 2: her saldırı sınıfına izole avcı ajan atama — araçlar: Avcı ajanlar
- 5. adım — Faz 3: her bulguyu verifier ajanla çürütmeye çalışma — araçlar: Verifier ajan
- 6. adım — Kayıt ve doğrulama (findings.json, confirmed/rejected) — araçlar: security-audit
- 7. adım — Faz 6: REPORT.md ile doğrulanmış sorunlar ve düzeltmeler — araçlar: security-audit
- 8. adım — Denetimi birkaç kez yeniden çalıştırma — araçlar: Claude Code, security-audit
## Promptlar
- Güvenlik denetimini başlatma — Kurulumdan sonra Claude Code'a bu kod tabanının güvenlik denetimini yapmasını söyler.
ikinci göz KAPALI: --ikinci-goz yok
