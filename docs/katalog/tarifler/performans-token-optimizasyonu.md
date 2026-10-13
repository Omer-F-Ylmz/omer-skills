# Performans ve jeton optimizasyonu — birleşim tarifi
Ne zaman: Yavaş sayfa/servis, Core Web Vitals sorunu ya da Claude jeton/maliyet tüketimi.

## Fazlar
1. Ölçüm: web için `web-perf` — Core Web Vitals ve Lighthouse performans puanı · jeton için `departman-verimlilik` + `claude-usage` jeton, maliyet ve oturum panosu.
2. Teşhis: `chrome-devtools-mcp:debug-optimize-lcp` — LCP hata ayıklama · birlikte: .NET için `dn-dotnet-performans`, animasyon için `fixing-motion-performance`, bellek için `chrome-devtools-mcp:memory-leak-debugging`.
3. Uygulama: `agent-skills:performance-optimization` — gerileme, N+1, Core Web Vitals · jeton tarafında `context-mode:context-mode` büyük çıktıyı bağlama dökmeden işler.
4. Regresyon: `benchmark` — web performans gerilemesi tespiti · birlikte: `context-mode:ctx-stats` oturumda kazanılan bağlamı gösterir.
5. Maliyet incelemesi: `vrm-maliyet-denetci` — kaçınılabilir jeton/API harcamasını bulur · birlikte: `vrm-plan-limit-izleme` plan limiti ve yanma hızı.
6. Kapanış: `superpowers:verification-before-completion` — önce/sonra sayısıyla.

## İnceleme ajanları
- `vrm-maliyet-denetci`: iş akışı ve log harcama incelemesi.
- `ponytail-review`: gereksiz bağımlılık ve kod.

## Güvenlik ve kalite kapıları
- Önce/sonra ölçümü aynı koşulda; tek sayı yerine tekrar.
- Davranış değişmedi: testler yeşil.
- Sıkıştırma ayarı sonrası çıktı hâlâ okunur.

## Tartışma konseyi
- Karar: hangi darboğaz önce; hız ile okunabilirlik arası.
- `ecc:council` — varsayılan Claude personaları: performans mühendisi, bakımcı, kullanıcı.

## Jeton bütçesi
- Ölçüm: küçük (~6k, tahmini). Teşhis: orta (~15k); profil ve log `okuyucu` alt ajanına. Uygulama: orta (~20k). Regresyon: küçük (~5k). Maliyet: küçük (~5k). Kapanış: küçük (~3k). Hepsi tahmini.

## Kaçınılacaklar
- `ecc:cost-tracking` kancası kurulu değilse veri yoktur; tüm satırları toplamak çoklu sayım yapar.
- Ölçmeden optimize etmek.
- CMS'e özgü ajanları (`engineering-wordpress-performance`, `engineering-drupal-performance`) o CMS dışında kullanmak.

## Aday (kurulu değil)
- `cmem_yama`: claude-mem worker yaması; tek atımlık compress çağrısı.
