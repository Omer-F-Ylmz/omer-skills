# NVIDIA, Yapay Zekâ Skill’lerini Kurmadan Önce Tarıyor
## Künye
NVIDIA, Yapay Zekâ Skill’lerini Kurmadan Önce Tarıyor · İsa Nurdoğdu · süre: 0:46 · tr-orig · https://youtu.be/jYyHjpndukk · şema 2
motor: parti 2026-10-09-short-7 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 17065 tk · claude-haiku-5-5: claude-haiku-5-5 · 35280 tk
## Özet
İsa Nurdoğdu, skill dosyalarının yapay zekâya talimat veren metinler olduğunu ve kötü niyetli hazırlanabildiğini anlatıyor. NVIDIA'nın 42.000 herkese açık skill'i taradığını ve dörtte birinde güvenlik açığı bulduğunu söylüyor. Çözüm olarak NVIDIA'nın açık kaynak aracı SkillSpector'ı gösteriyor. GitHub linkini Claude veya Codex'e verip kurdurmayı, sonra kurulacak skill'leri bu araçla taratıp 'kur ya da kurma' kararı almayı öneriyor.
## Bölümler
- 0:00 Skill'lerin metin olması ve güvenlik riski
- 0:10 NVIDIA'nın 42.000 skill taraması
- 0:19 Çözüm: SkillSpector aracı
- 0:26 README ve Docker ile tarama
- 0:29 Linki yapay zekâya verip kurdurma
- 0:41 Kötü amaçlı skill'leri engelleme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| SkillSpector | yok | CLI | https://github.com/NVIDIA/SkillSpector | NVIDIA'nın yapay zekâ ajanı skill'leri için güvenlik tarayıcısı; kurulumdan önce zafiyet, kötü amaçlı desen, prompt injection ve veri sızıntısı arar. | 0:22 | Repo açıklaması: 'Security scanner for AI agent skills'. (karede: GitHub nvidia/skillspector sayfasında 'Security scanner for AI agent skills. Detect vulnerabilities...' ve 18.8k stars görünüyor.) |
| Claude | yok | CLI | yok | Linki verip SkillSpector'ı kurdurmak için kullanılan yapay zekâ ajanı. | 0:32 | Konuşmada 'Sonrasında Claude'a veya Codex'e verdiğiniz' deniyor. |
| Codex | yok | CLI | yok | SkillSpector'ı kurması için link verilebilecek alternatif yapay zekâ ajanı. | 0:32 | Konuşmada Claude'a veya Codex'e verilen GitHub linkleri anılıyor. |
| Claude Code | yok | CLI | yok | SkillSpector'ın taradığı skill ekosistemlerinden biri. | 0:22 | Repo açıklamasında 'Claude Code, Codex, and MCP skills' geçiyor. (karede: Repo açıklamasında 'chain risks in Claude Code, Codex, and MCP skills before you inst' yazıyor.) |
| MCP | yok | MCP | yok | SkillSpector'ın taradığı skill türlerinden biri. | 0:22 | Repo açıklamasında MCP skills anılıyor. (karede: Repo açıklamasında 'Claude Code, Codex, and MCP skills' yazıyor.) |
| Docker | yok | CLI | yok | SkillSpector'ı konteynerde çalıştırma yöntemi. | 0:27 | README'de docker run ve docker build komutları var. (karede: README'de 'docker run --rm -v "$PWD:/scan" skillspector scan' ve 'Build the image' görünüyor.) |
| Python | yok | teknik | yok | SkillSpector Python 3.12+ ile yazılmış; Docker imajı python 3.12-slim-bookworm tabanlı. | 0:26 | README rozetinde python 3.12+ yazıyor. (karede: README'de 'python 3.12+' ve 'License Apache 2.0' rozetleri görünüyor.) |
| Make | yok | CLI | yok | Docker imajını derlemek için make docker-build hedefi. | 0:27 | README'de make docker-build komutu var. (karede: 'make docker-build' ve '# or: docker build -t skillspector .' satırları görünüyor.) |
| GitHub | yok | teknik | yok | SkillSpector reposunun barındığı platform. | 0:22 | GitHub repo sayfası gösteriliyor. (karede: GitHub sayfasında nvidia/skillspector, Watch 74, Fork 1.6k görünüyor.) |
| SkillSpector'ı kurdurmak | yok | prompt | yok | Yapay zekâya SkillSpector GitHub linki verilip aracı kurması isteniyor; sonra GitHub skill linkleri bununla taranıp kur/kurma önerisi alınıyor. | 0:29 | kaynak: kare |
## Açıklama bağlantıları
- https://www.isanurdogdu.com/kaynaklar/nvidia-skillspector — Yazarın SkillSpector kaynak sayfası · aday: hayır · Yazarın kendi kaynak/yönlendirme sayfası; araç değil, referans sayfası. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| make docker-build | SkillSpector Docker imajını derler. (karede: README'de 'make docker-build' satırı görünüyor.) | 0:27 | kare |
| docker build -t skillspector . | Make'e alternatif olarak imajı skillspector adıyla derler. (karede: '# or: docker build -t skillspector .' satırı görünüyor.) | 0:27 | kare |
| docker run --rm -v "$PWD:/scan" skillspector scan | Geçerli dizini /scan olarak bağlayıp yerel dizini tarar. (karede: 'docker run --rm -v "$PWD:/scan" skillspector scan' satırı görünüyor.) | 0:27 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Skill'ler yapay zekâya talimat veren metin dosyalarıdır ve kötü niyetli hazırlanabilir. | 0:00 | özellik |
| NVIDIA 42.000 herkese açık skill'i tarayıp dörtte birinde kötü niyetli güvenlik açığı bulmuş. | 0:10 | sayısal |
| SkillSpector, verilen GitHub linklerini tarayıp kur ya da kurma talimatı verir. | 0:32 | özellik |
| SkillSpector'ı kendi yapay zekânıza mutlaka kurdurmalısınız. | 0:27 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Skill kavramı | aday değil: genel kavram | Skill'ler yapay zekâya talimat veren metin dosyaları deniyor. |
| konuşma 0:00 | Claude | Claude | Claude'a veya Codex'e verin deniyor. |
| konuşma 0:00 | Codex | Codex | Claude'a veya Codex'e verin deniyor. |
| konuşma 0:00 | GitHub | GitHub | GitHub linkleri taranıyor. |
| kare 0:10 | NVIDIA logosu ve 'SKILL=metin' | aday değil: genel kavram | Kare: SKILL=metin ve NVIDIA logosu. |
| kare 0:22 | SkillSpector reposu | SkillSpector | nvidia/skillspector sayfası. |
| kare 0:22 | Claude Code | Claude Code | Repo açıklamasında anılıyor. |
| kare 0:22 | MCP | MCP | Repo açıklamasında MCP skills. |
| kare 0:22 | Apache License 2.0 | aday değil: genel kavram | Repo lisansı. |
| kare 0:22 | prompt injection, data exfiltration | aday değil: genel kavram | Repo açıklamasında risk türleri. |
| kare 0:22 | docs.nvidia.com/skills/scanning-agent-skills | SkillSpector | Repo sayfasındaki doküman linki. |
| kare 0:26 | Python 3.12+ | Python | README rozeti. |
| kare 0:27 | Docker | Docker | docker run komutu. |
| kare 0:27 | make docker-build | Make | README komutu. |
| kare 0:27 | LLM analysis / .env | aday değil: başka adayın parçası (SkillSpector) | README'de LLM analizi için .env anlatılıyor. |
| kare 0:27 | Google Lens 'bu sayfa hakkında' önerisi | aday değil: konu dışı | Adres çubuğunda tarayıcı önerisi. |
| kare 0:29 | Sohbet arayüzü 'What's up next, isa?' | Claude | Link sohbet kutusuna yazılmış. |
| kare 0:29 | Fable 5.1 modeli | aday değil: konu dışı | Sadece istatistik panelinde görünüyor. |
| kare 0:29 | finanspanel klasörü | aday değil: konu dışı | Sohbet arayüzünde seçili proje klasörü. |
| açıklama | isanurdogdu.com kaynak sayfası | aday değil: konu dışı | Yazarın kaynak sayfası. |
| açıklama | github.com/NVIDIA/SkillSpector | SkillSpector | Bağlantılı sayfada repo linki. |
| açıklama | docs.nvidia.com evaluating-agent-skills | SkillSpector | NVIDIA doküman sayfası bağlantısı. |
| yorum | Sabit yorum linki | aday değil: konu dışı | Kaynak sayfası linki. |
## Kareden okunanlar
- 0:10: 'SKILL=metin' yazısı ve NVIDIA logosu
- 0:22: nvidia/skillspector: 18.8k stars, 1.6k fork, Issues 70, PR 80, Apache License 2.0
- 0:26: README: SkillSpector, python 3.12+, Apache 2.0
- 0:27: make docker-build ve docker run --rm -v "$PWD:/scan" skillspector scan
- 0:29: Sohbet kutusunda skillspector GitHub linki; Fable 5.1, Sessions 151, Messages 27,034
## Belirsizlikler
- Altyazıdaki '1örte birinde' ifadesi 'dörtte birinde' olarak yorumlandı.
- 'Skill Specter' altyazı yazımı; ekranda ve repoda ad SkillSpector.
- Sohbet arayüzündeki ana model 'Fable 5.1' görünüyor; videoda ayrıca anlatılmıyor, aday yapılmadı.
- Açıklamada 'nvidia' yazın denirken sesli anlatımda 'skill' yazın deniyor; tutarsızlık var.
- Tarama çıktısı gösterilmiyor; aracın sonucu yalnız anlatılıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.isanurdogdu.com/kaynaklar/nvidia-skillspector | açıklama | açıklama | hayır |
| https://www.isanurdogdu.com/kaynaklar/nvidia-skillspector | açıklama | yorum | hayır |
| docs.nvidia.com/skills/scanning-agent-skills | 0:22 | ekran | evet |
| https://github.com/nvidia/skillspe | 0:27 | ekran | evet |
| https://github.com/nvidia/skillspector | 0:29 | ekran | evet |
| https://github.com/NVIDIA/SkillSpector | açıklama | açıklama | evet |
| https://docs.nvidia.com/skills/evaluating-agent-skills | açıklama | açıklama | evet |
| https://www.isanurdogdu.com | açıklama | açıklama | hayır |
| https://www.isanurdogdu.com/#kur | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — NVIDIA'nın skill taramasının sonucu anlatıldı — araçlar: NVIDIA
- 2. adım — SkillSpector GitHub reposu açılıp açıklaması gösterildi — araçlar: GitHub, SkillSpector
- 3. adım — README'deki Docker ile kurulum ve tarama bölümü gösterildi — araçlar: Docker, Make, SkillSpector
- 4. adım — Repo linki tarayıcı adres çubuğundan kopyalandı — araçlar: GitHub
- 5. adım — Link yapay zekâ sohbet kutusuna yapıştırılıp kurdurma anlatıldı — araçlar: Claude, SkillSpector
- 6. adım — Skill GitHub linkleri SkillSpector ile taratılıp kur/kurma kararı alınması anlatıldı — araçlar: SkillSpector, Claude, Codex
## Promptlar
- SkillSpector'ı kurdurmak — Yapay zekâya SkillSpector GitHub linki verilip aracı kurması isteniyor; sonra GitHub skill linkleri bununla taranıp kur/kurma önerisi alınıyor.
ikinci göz KAPALI: --ikinci-goz yok
