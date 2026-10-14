# youtube-agent-skill — 12 benzersiz kayıt

**Amaç:** Bir YouTube kanalını yöneten 11 skill: 21 hook formülüyle senaryo, başlık/thumbnail paketleme, SEO, bölümler, Shorts kesme, yorum yanıtlama, tutma analizi, kanal denetimi, viral araştırma.

**İç yapı:** youtube-agent [plugin] + youtube-agent:yt-<iş>; üretim (script, edit, chapters, shorts), paketleme (package, seo), analiz (audit, retention, viral), topluluk (comment), plan.

## En güçlü parçalar
- `youtube-agent:yt-script` — Video senaryosu, hook, açılış cümlesi.
- `youtube-agent:yt-package` — Başlık, thumbnail metni; CTR düşükse.
- `youtube-agent:yt-retention` — İzleyicinin neden bıraktığını tutma grafiği/CSV ile açıklar, tempoyu düzeltir.
- `youtube-agent:yt-audit` — Kanal URL'siyle neden büyümediğini denetler.
- `youtube-agent:yt-shorts` — Videoyu Shorts'a kesme ve yeniden kullanım.
- `youtube-agent:yt-edit` — Transkriptten ölü alanı kesip videoyu sıkılaştırma.

## Birlikte kullanım
- yt-plan → yt-script → yt-package → yt-seo → yt-chapters.
- yt-audit + yt-retention + yt-viral: analizden plana.
- linkedin-agent-skill ile aynı 21 hook formülü yaklaşımı.

## Tuzaklar
- Skill'ler yapıştırılan veri (CSV, transkript, URL) ile çalışır; YouTube API erişimi katalog metninde belirtilmemiş.
- vid ailesi ajanları (reel-kanca, kisa-klip-secici) ile Shorts kapsamı çakışır.

## Üyeler
- plugin (1): youtube-agent
- skill (11): youtube-agent:yt-audit, youtube-agent:yt-chapters, youtube-agent:yt-comment, youtube-agent:yt-edit, youtube-agent:yt-package, youtube-agent:yt-plan, youtube-agent:yt-retention, youtube-agent:yt-script, youtube-agent:yt-seo, youtube-agent:yt-shorts, youtube-agent:yt-viral
