# brief: 2026-09-28-uygula.md
## Özellik kararları
- codex-plugin-cc/codex-review → ZATEN VAR — zaten var: codex (gstack skill; review/challenge/consult modları) · code-review skill
- codex-plugin-cc/codex-adversarial-review → ZATEN VAR — zaten var: codex (gstack skill challenge modu) · agent-skills:doubt-driven-development
- codex-plugin-cc/codex-rescue-transfer → RED — güvenlik: SkillSpector --no-llm HIGH/CRITICAL 4 (on.md); ikinci ücretli model aboneliği gerekir
- blz-sinematik-portfoy-promptu/uzun-detayli-prompt-ile-dosya-yapisini-dikte-etme → ZATEN VAR — zaten var: docs/video-tarama/kayit.jsonl (b-LZ_Y9wor8, 2026-09-24 toplu) — aynı kalıp "ZATEN VAR" karara bağlanmış
- blz-sinematik-portfoy-promptu/pencereden-iceri-giren-sinematik-scroll-girisi → ZATEN VAR — zaten var: docs/kurulumlar/bekleyen/teknik-kaydirmaya-bagli-sahne-gecisi-pencereden-iceri-girme-plan-metin-belirme.md (aynı video, onaysız bekliyor)
## Departman
- codex-plugin-cc → surec-inceleme (0.89)
- blz-sinematik-portfoy-promptu → frontend (0.90)
- lumen-sitesi-promptu → frontend (0.97)
- gsap → frontend (1.00)
- webgl → frontend (0.93)
- lenis → frontend (0.98)
- next-js → frontend (0.81)
- opus-model-seçimi → surec-ajan-arac (0.64)
- uzun-detaylı-prompt-yazma → frontend (0.55) · içerik türü site/UI (Jev surec-plan 0.55)
- prompt-içinde-dosya-yapısı-belirtme → surec-ajan-arac (0.62)
## İddialar
- `/codex:review`, Codex içindeki `/review` ile aynı kalitede inceleme verir → doğrulanamadı (openai/codex-plugin-cc README)
- jeskojets.com Awwwards ödüllü site → doğru (awwwards.com/sites/jesko-jets)
- ~25 dakikada tüm proje üretildi → doğrulanamadı (yok)
- Uzun/detaylı prompt ile %90-100 birebir sonuç alınıyor → doğrulanamadı (yok)
- Kanalın izleyicileri 50'den fazla ülkeden geliyor → doğrulanamadı (yok)
- Prompt kopyalanıp yapıştırılırsa sitenin %90 benzeri çıkar (5:04) → doğrulanamadı (-)
- scroll'a bağlı animasyonlar ve slider fizik efekti için kullanılan animasyon kütüphanesi (6:41) → doğrulanamadı (-)
- 3D jet objesinin ve sahnenin render edilmesini sağlayan teknoloji (6:41) → doğrulanamadı (-)
- yumuşak (inertia'lı) sayfa kaydırma kütüphanesi (7:42) → doğrulanamadı (-)
- sitenin kurulduğu React framework'ü, tercih edilebilir alternatif Vue/Angular (6:41) → doğrulanamadı (-)
- ağır/karmaşık siteler için Claude'da en güçlü modeli (Opus) seçmek (8:44) → doğrulanamadı (-)
- tasarım kararlarını adım adım anlatan uzun prompt yazarak %90-100 birebir sonuç almak (6:41) → doğrulanamadı (-)
- modelin kendi kafasına göre proje kurmasını önlemek için dosya yapısını prompt'ta zorunlu kılmak (7:42) → doğrulanamadı (-)
- görsel/3D obje yüklenirken sitenin bozuk görünmesini önlemek için yükleme ekranı eklemek (9:08) → doğrulanamadı (-)
- Awwwards kazanan bir siteyi bölüm bölüm inceleyip kendi tasarımına uyarlama süreci (0:51) → doğrulanamadı (-)
- proje slider'ının hızlı çevrildiğinde kağıt gibi sallanmasını sağlayan drag+physics efekti (3:47) → doğrulanamadı (-)
## Site/UI teknikleri
- kaydırmaya bağlı sahne geçişi (pencereden içeri girme, plan/metin belirme) · UYARLA · video b-LZ_Y9wor8 · 0:51 anlatım + k00196/k00578 kareleri · KABUL (Ömer 28 Eyl, 24c K7)
- yumuşak (inertia) kaydırma · UYARLA · video b-LZ_Y9wor8 · 7:42 "GSAP, Lenis" · KABUL (Ömer 28 Eyl, 24c K7)
- 3D obje (jet modeli, blueprint girişli) · UYARLA · video b-LZ_Y9wor8 · 3:47 anlatım · KABUL (Ömer 28 Eyl, 24c K7)
- sürüklenince fizik tepkili slider (kağıt sallanması) · UYARLA · video b-LZ_Y9wor8 · 3:47 anlatım · KABUL (Ömer 28 Eyl, 24c K7)
- tipografi ile odak (iki kelimenin sırayla belirmesi) · UYARLA · video b-LZ_Y9wor8 · 4:49 anlatım · KABUL (Ömer 28 Eyl, 24c K7)
- noktalı 3D dünya küresi (footer) · UYARLA · video b-LZ_Y9wor8 · 5:54 anlatım + k00377 karesi · KABUL (Ömer 28 Eyl, 24c K7)
## Prompt anatomisi
- Ödüllü siteyi bölüm bölüm inceleyip ilham alma · b-LZ_Y9wor8 0:51 · şablon: yok
- Dosya yapısını promptta zorunlu kılma (modele bırakmama) · b-LZ_Y9wor8 7:42 · şablon: dosya
- Uzun/detaylı prompt ile %90-100 birebir sonuç hedefleme · b-LZ_Y9wor8 6:41 · şablon: kabul
- Her şey hazır olana kadar loading screen ekletme · b-LZ_Y9wor8 9:08 · şablon: hareket
- Kaydırmaya bağlı kağıt fiziği slider tarifi · b-LZ_Y9wor8 3:47 · şablon: hareket
- 3D modeli stack adıyla ver: model + R3F/Three.js birlikte · iYwCzKy6W40 5:04 · şablon: teknoloji
## Linkler
- https://avenox.lol/codex.md`
- https://avenox.lol/codex.md,
- https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/
- https://www.kdnuggets.com/2026/08/abacus/honest-abacus-ai-review
- https://developer.chrome.com/docs/css-ui/scroll-driven-animations
