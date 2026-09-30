# Remotion
ad: Remotion
tur: skill
video: AAtagrbBOto
repo: remotion-dev/remotion
lisans: bilinmiyor (SPDX değil: özel "Remotion License"; LICENSE.md; bazı durumlarda şirket lisansı gerekir)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/remotion-dev/remotion
telemetri: bilinmiyor (kaynak kodu incelenmedi; README'de telemetri belirtilmiyor)
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-short-2)
## Ne
React koduyla video üreten çatı. Ajanlarla (Claude Code vb.) sohbet ederek animasyon/motion tasarım videosu üretmeye yarayan Agent Skills, Claude Code ve Codex plugin paketleri içerir.
## Mekanizma
Video, React bileşenleri olarak yazılır (kod tek doğruluk kaynağı). Skill ajana Remotion API'sini, animasyon ve kompozisyon kurallarını öğretir. Ajan React kodunu yazar, Studio'da önizlenir, CLI/Node API, Lambda, Cloud Run veya tarayıcı tarafında MP4'e render edilir. Repoda .claude/skills, .agents/skills, packages/claude-code-plugin, packages/codex-plugin ve packages/agent-plugin var. Ayrıntılı iç işleyişi doğrulamadım.
## Kanıt
- Claude Code içine tek komutla kurulan skill; sohbetle animasyon ve motion tasarım üretir. → sınanamadı · README, Agent Skills sayfası ve claude-code-plugin paketinin varlığını gösteriyor. Tek komut ve çıktı kalitesi çalıştırılarak sınanmadı. Video sayfasından yalnız başlık alınabildi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- npx create-video@latest (README'deki resmi başlangıç; Node.js gerekir)
- Agent skill kurulumu: https://www.remotion.dev/docs/ai/skills (videodaki 'tek komut' iddiasının tam komutunu doğrulamadım)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Sohbetle kodlanmış, tekrar düzenlenebilir animasyon ve tanıtım videosu üretimi. Şablon, geçiş, altyazı ve toplu render de sunuyor.
## Maliyet/risk
Özel lisans: şirketler için ücretli lisans gerekebilir, ticari kullanımdan önce LICENSE.md okunmalı. Skill'in içeriği ve telemetrisi incelenmedi. Render için Node ve ffmpeg benzeri bağımlılıklar ile kaynak gerekir.
## Tasarruf
Token aracı değil; geçerli değil.
## Üretilebilir
hedef_tur: skill
tarif: Remotion'un kendisi yeniden yazılmaz. Onun üzerine ince bir skill yazılır: SKILL.md içinde npx create-video ile proje iskelesi, kompozisyon ve animasyon kalıpları (interpolate, spring, Sequence), remotion render komutu ve markaya özel şablon kuralları anlatılır. Resmi Agent Skills içeriği referans alınır. Lisans şartı kontrol edilmelidir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-short-2/panel.md → Ömer sütunu
## Özellikler
### Ajanla (coding agent) sohbetle video üretimi ve Agent Skills
kaynak: https://www.remotion.dev/docs/ai/skills
### Programatik video, toplu render, Lambda/Cloud Run/Vercel render seçenekleri
kaynak: https://github.com/remotion-dev/remotion
### Şablonlar, geçişler, altyazılar, efektler, ses efektleri
kaynak: https://github.com/remotion-dev/remotion
### Remotion agent skill'i: Claude Code içine tek komutla kurulur ve sohbetle animasyon/motion tasarım videosu üretir. Videodaki iddia: "keyframe ve karmaşık yazılım gerekmiyor."
video: AAtagrbBOto · iddia: Remotion ile keyframe ve karmaşık yazılım gerekmiyor.
sonuc: doğrulandı
arastirma: Belgede var. Remotion'un resmi Agent Skills sayfası, Claude Code, Codex, Kimi Code ve Cursor gibi ajanlar için beste-practice skill'leri sunuyor. Kurulum komutu `npx skills add remotion-dev/skills`. Yeni proje açılırken `create-video` da skill eklemeyi öneriyor. Skill'ler: remotion-best-practices (hepsini kapsar), remotion-create (yeni proje/kompozisyon; örnek istem: "Make a promo video for a record store"), remotion-markup (kompozisyon, animasyon, düzen, yazı tipi, ses, zamanlama), remotion-studio (önizleme), remotion-render (video veya still render), remotion-maps, remotion-captions, remotion-saas, remotion-interactivity (Studio'da düzenlenebilir kod), remotion-docs, remotion-upgrade, remotion-multimedia. Mekanizma: video React kodu olarak yazılır ve kod tek doğruluk kaynağıdır. Ajan bu kodu yazar, Studio'da önizlenir, sonra CLI, Node API, Lambda, Cloud Run veya Vercel ile render edilir. "Keyframe gerekmiyor" iddiası kısmen doğru. Kullanıcı elle keyframe girmez, ajan kodu üretir. Ama çıktı yine React kodudur ve animasyon kodla (interpolate, spring gibi) tanımlanır. Node.js gerekir. "Karmaşık yazılım gerekmiyor" iddiası da kısmen doğru: klasik video editörü gerekmez ama Node ve Remotion projesi gerekir. Çıktı kalitesini çalıştırıp sınamadım. Lisans özel: bazı durumlarda şirket lisansı gerekir (LICENSE.md). Telemetri, son commit ve yıldız sayısı bilinmiyor.
kaynak: https://www.remotion.dev/docs/ai/skills
## Destek
- AAtagrbBOto · 0:00 · Claude Code içine kurulan skill; sohbetle animasyon ve motion tasarım üretir. · kanıt: It is called Remotion. One command and it installs directly inside Claude code. · iddia: Remotion ile keyframe ve karmaşık yazılım gerekmiyor.
