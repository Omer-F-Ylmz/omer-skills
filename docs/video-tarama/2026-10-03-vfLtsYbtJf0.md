# Stop Installing Claude Skills Manually, This Skill Does It For You
## Künye
Stop Installing Claude Skills Manually, This Skill Does It For You · InsiderForce · süre: 1:17 · en-orig · https://youtu.be/vfLtsYbtJf0
motor: parti 2026-10-03-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
## Özet
Kısa video, Claude/kodlama ajanları için uygun skill'i otomatik bulup kuran 'install skills' adlı bir skill'i tanıtıyor. Tek komutla kurulu ajanlar algılanıyor, kullanım amacına uygun skill'ler doğru yere kuruluyor; Claude içinde 'Is there a skill for this?' diye sorulabiliyor. Son kısım ebook için yorum yaptırma çağrısı.
## Bölümler
- 0:00 Sorun: binlerce skill, doğrusunu bulmak zor
- 0:24 Çözüm: 'install skills' skill'i
- 0:33 Nasıl çalışır: tek komut ve 'Is there a skill for this?'
- 1:01 Ebook çağrısı (comment human)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| install skills | yok | skill | yok | Diğer skill'lerde arama yapıp kullanım amacına uygun olanı bulan ve kurulu kodlama ajanlarına kuran skill. | 0:33 | Altyazı: 'It is called install skills and it is a skill that searches' (karede: Kare 0:33: arama kutusu ve büyüteç ikonu, 'And it is a skill that searches through all the other skills' yazısı.) |
| Skills CLI (npx skills) | yok | CLI | yok | Açık ajan skill ekosistemi için paket yöneticisi; skill arama (find), ekleme (add), kontrol (check) ve güncelleme (update) komutları var. | 0:43 | Karede 'What is the Skills CLI?' başlığı ve npx skills komut listesi görülüyor. (karede: Kare 0:43: 'Find Skills' belgesi; 'What is the Skills CLI?' altında npx skills find, add, check, update komutları; 'Browse skills at: https://skills.sh/'.) |
| Claude içinde mevcut göreve uygun skill'i aratıp önermesini sağlamak. | yok | prompt | yok | Is there a skill for this? | 0:50 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx skills find [query] | Anahtar kelimeyle skill arar. (karede: Kare 0:43: 'Key commands' altında npx skills find {query} [--owner <owner>].) | 0:43 | kare |
| npx skills add <package> | GitHub vb. kaynaktan skill kurar. (karede: Kare 0:43: 'npx skills add <package> - Install a skill from GitHub or other sources'.) | 0:43 | kare |
| npx skills check | Skill güncellemelerini kontrol eder. (karede: Kare 0:43: 'npx skills check - Check for skill updates'.) | 0:43 | kare |
| npx skills update | Kurulu tüm skill'leri günceller. (karede: Kare 0:43: 'npx skills update - Update all installed skills'.) | 0:43 | kare |
| npx skills find react performance | Örnek: React performansı için skill arar. (karede: Kare 0:52: 'How do I make my React app faster?' → npx skills find react performance.) | 0:52 | kare |
| npx skills add vercel-labs/agent-skills@react-best-practices | Örnek yanıttaki react-best-practices skill'ini kurar. (karede: Kare 0:52: 'Example response' kutusunda 'To install it' altında bu komut.) | 0:52 | kare |
| npx skills add <owner/repo@skill> -g -y | Skill'i kullanıcı seviyesinde, onaysız kurar. (karede: Kare 0:52: 'Step 6: Offer to Install' altında npx skills add ... -g -y (parametre adları kısmen okunuyor).) | 0:52 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Çoğu kişi bir skill'e değer mi diye anlamak için readme okurken 30 dakika harcıyor. | 0:14 | sayısal |
| Tek komut, kurulu her kodlama ajanını algılar ve skill'leri doğru yere kurar. | 0:43 | özellik |
| Skill, öneri öncesi kalite doğrular: kurulum sayısı, kaynak itibarı ve GitHub yıldızı kontrol edilir. | 0:52 | özellik |
| Kullanıcı onaylarsa -g bayrağı global kurar, -y onay istemlerini atlar. | 0:52 | özellik |
## Kareden okunanlar
- 0:04: 'Someone just build a skill that Finds and Installs' ve insiderforce.io filigranı.
- 0:14: 'The problem is finding the right one that actually matches what'.
- 0:24: 'Save this before you forget' ve yer imi ikonu.
- 0:33: 'And it is a skill that searches through all the other skills'.
- 0:43: Find Skills belgesi: When to Use, What is the Skills CLI?, npx skills komutları, skills.sh; altında tek komut/algılama metni.
- 0:52: Step 4 (kalite doğrulama), Step 5 (seçenek sunma), Step 6 (kurulum teklifi, -g -y).
- 1:02: 'claude puts out to sound like a' (ebook çağrısı).
- 1:12: Ebook sayfası görseli ve 'To make AI copy sound 100% HUMAN'.
## Belirsizlikler
- 'install skills' skill'inin repo/yazar bilgisi videoda yok; repo_url null.
- 'Is there a skill for this?' tam zamanı tahmini (~0:50); kare 0:52'de soru görünmüyor.
- Videodaki 'tek komut' açıkça söylenmiyor; karedeki npx skills komutlarıyla ilişkisi kesin değil.
- Karedeki küçük metinlerde parametre adları kısmen okunaklı.
## Atlanan segment oranı
0/2 (paket tam okuma, motor)
ikinci göz KAPALI: --ikinci-goz yok
