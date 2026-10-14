# remotion — 13 benzersiz kayıt

**Amaç:** Remotion ile kodla video üretimi: proje oluşturma, altyazı, harita animasyonu, etkileşim, studio önizleme, render, sürüm yükseltme ve doküman arama.

**İç yapı:** Tümü [skill], ad kalıbı remotion-<konu>; yönlendirici remotion-best-practices; yaşam döngüsü (create, studio, render, upgrade), içerik (captions, maps, markup, multimedia, interactivity), yardımcı (docs, saas); ayrıca 47 skill'lik remotion-video-paket.

## En güçlü parçalar
- `remotion-best-practices` — Tüm Remotion skill'leri için yönlendirici; doğru alt skill'e götürür.
- `remotion-create` — Yeni Remotion videosu oluşturur.
- `remotion-render` — Remotion videosunu dışa aktarır.
- `remotion-captions` — Altyazıyı transkribe eder, gösterir ve canlandırır.
- `remotion-docs` — Remotion dokümanında arama yapar.

## Birlikte kullanım
- remotion-create → remotion-markup / remotion-captions → remotion-studio → remotion-render.
- remotion-upgrade + remotion-docs: paket yükseltmede güncel API'yi doğrulamak.
- remotion-video-paket HyperFrames şablonları ve web video skill'leriyle birlikte kullanılır.

## Tuzaklar
- remotion-video-paket 47 skill içerir ve tekil remotion-* skill'leriyle örtüşür; ikisi birden yüklenmemeli.
- Açıklamalar çok kısa (ör. remotion-multimedia yalnız 'Mediabunny'); kapsam girdide belirtilmemiş.

## Üyeler
- skill (13): remotion-best-practices, remotion-captions, remotion-create, remotion-docs, remotion-interactivity, remotion-maps, remotion-markup, remotion-multimedia, remotion-render, remotion-saas, remotion-studio, remotion-upgrade, remotion-video-paket
