# DERS KİTABI — Web S4 Performans/Vite/a11y/SEO
## A. En iyi yöntemler + tarif kartları (adım adım)
> "The object form `output.manualChunks` option is not supported anymore. The function form `output.manualChunks` is deprecated." (resmi-c7-vite-build.md)
*Vite'de `manualChunks` nesne şekli artık desteklenmiyor. Fonksiyon şekli de kullanım dışı bırakıldı.*

> "Shows how to configure chunk splitting using `build.rolldownOptions.output.codeSplitting` as the replacement for the deprecated `manualChunks` option." (resmi-c7-vite-build.md)
*Chunk bölünmesini `build.rolldownOptions.output.codeSplitting` kullanarak yapılandırın. Bu, eski `manualChunks` seçeneğinin yerini alıyor.*

> "Forces an asset to be explicitly inlined as a base64 data URL with `?inline` or prevents inlining using `?no-inline`." (resmi-c7-vite-build.md)
*Bir varlığın base64 veri URL'si olarak içe aktarılmasını zorlamak için `?inline` kullanın veya içe aktarmayı engellemek için `?no-inline` kullanın.*

> "Vite emits `vite:preloadError` event when it fails to load dynamic imports." (resmi-vite-build.md)
*Vite, dinamik içe aktarma yükleme hatası durumunda `vite:preloadError` olayını tetikler.*

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "The object form `output.manualChunks` option is not supported anymore. The function form `output.manualChunks` is deprecated. Rolldown has the more flexible [`codeSplitting`](https://rolldown.rs/reference/OutputOptions.codeSplitting) option." (resmi-c7-vite-build.md)
*Vite 4+ sürümlerinde `manualChunks` nesnesi desteklenmiyor; fonksiyon biçimi de artık önerilmiyor. `codeSplitting` seçeneği ile kod bölümlendirmesi yapılır.*

---

> "If you use a framework, refer to their documentation for configuring how chunks are split." (resmi-vite-build.md)
*Çerçeveler kendi dokümantasyonlarında kod bölümlendirme yapılandırmasını ayrıntılı olarak açıklıyor. Örnek: React, Vue gibi çerçevelerde `manualChunks` yerine `codeSplitting` kullanımı önerilir.*

---

> "Forces an asset to be explicitly inlined as a base64 data URL with `?inline` or prevents inlining using `?no-inline`." (resmi-c7-vite-build.md)
*Vite, `?inline` ile kaynakları base64 olarak içe aktarırken, `?no-inline` ile içe aktarımı engeller. Bu, performans optimizasyonu için kullanılır.*

---

## C. Kalite kapısı kontrol listesi
> "When it is time to deploy your app for production, simply run the `vite build` command. By default, it uses `<root>/index.html` as the build entry point, and produces an application bundle that is suitable to be served over a static hosting service." (resmi-vite-build.md)
*Uygulamanızı üretim için derlemek için `vite build` komutunu çalıştırın. Varsayılan olarak, `<root>/index.html` giriş noktası olarak kullanılır ve statik barındırma hizmeti için uygun bir uygulama paketi üretir.*

---

> "By default, the production bundle targets the minimum browser versions compatible with [Baseline](https://web-platform-dx.github.io/baseline/) Widely Available as of a date fixed for each major release." (resmi-vite-build.md)
*Varsayılan olarak, üretim paketi her büyük sürüm için sabitlenmiş bir tarihe kadar geniş çapta kullanılabilir olan [Baseline] ile uyumlu en az tarayıcı sürümlerini hedef alır.*

---

> "You can specify custom targets via the [`build.target` config option](/config/build-options.md#build-target), where the lowest target is `es2015`." (resmi-vite-build.md)
*Özel hedefleri `build.target` yapılandırma seçeneği aracılığıyla belirtmek mümkündür. En düşük hedef `es2015` olarak ayarlanabilir.*

---

> "If you are deploying your project under a nested public path, simply specify the [`base` config option](/config/shared-options.md#base) and all asset paths will be rewritten accordingly." (resmi-vite-build.md)
*Projenizi bir alt klasörde barındırıyorsanız, `base` yapılandırma seçeneğini belirtin ve tüm varlık yolları otomatik olarak yeniden yazılır.*

---

> "JS-imported asset URLs, CSS `url()` references, and asset references in your `.html` files are all automatically adjusted to respect this option during build." (resmi-vite-build.md)
*JS içe aktarma varlık URL'leri, CSS `url()` referansları ve `.html` dosyalarındaki varlık referansları derleme sırasında bu seçeneği saygı göstererek otomatik olarak ayarlanır.*

---

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Forces an asset to be explicitly inlined as a base64 data URL with `?inline` or prevents inlining using `?no-inline`." (resmi-c7-vite-build.md)

> "The Vite dev server does hard caching of pre-bundled dependencies and implements fast 304 responses for source code." (resmi-vite-performance.md)

> "Vite allows you to warm up files that you know are frequently used, e.g. `big-utils.js`, using the [`server.warmup`](/config/server-options.md#server-warmup) option." (resmi-vite-performance.md)

> "The Vite dev server only transforms files as requested by the browser, which allows it to start up quickly and only apply transformations for used files." (resmi-vite-performance.md)

## E. Proje bağlantısı: freelance sitesi, TELVE
> "The object form `output.manualChunks` option is not supported anymore. The function form `output.manualChunks` is deprecated." (resmi-c7-vite-build.md)
*Vite 4.0+ sürümlerinde `manualChunks` yapılandırması artık desteklenmemekte ve fonksiyon şeklinde kullanımı da önerilmiyor. Rolldown'un `codeSplitting` özelliği kullanılması gerekiyor.*

> "Shows how to configure chunk splitting using `build.rolldownOptions.output.codeSplitting` as the replacement for the deprecated `manualChunks` option." (resmi-c7-vite-build.md)
*Yeni `codeSplitting` yapılandırması ile kod parçalanması (chunk splitting) yapılandırılabilir. Rolldown belgelerine göre detaylı kullanım önerileri mevcut.*

> "You can specify multiple Rolldown outputs with plugins that are only applied during build." (resmi-vite-build.md)
*Çoklu çıktı (output) yapılandırması ile build aşamasında belirli plugin'lar uygulanabilir. Rolldown'un `output` seçenekleri kullanılarak bu yapılandırma sağlanır.*

> "The legacy chunks are conditionally loaded only in browsers that do not have native ESM support." (resmi-vite-build.md)
*Eski tarayıcılar için `plugin-legacy` ile oluşturulan parçalar (chunks) sadece ESM desteği olmayan tarayıcılarda yüklenir.*

> "The Vite dev server does hard caching of pre-bundled dependencies and implements fast 304 responses for source code." (resmi-vite-performance.md)
*Vite geliştirme sunucusu önceden derlenmiş bağımlılıkları sabit olarak saklar ve kaynak kodu için hızlı 304 yanıtları sağlar. Bu, yeniden yükleme sürelerini optimize eder.*

> "The `buildStart`, `config`, and `configResolved` hooks should not run long and extensive operations." (resmi-vite-performance.md)
*Vite plugin'larında `buildStart`, `config` ve `configResolved` hook'ları uzun süreli işlemler için kullanılmamalıdır. Bu hook'lar dev sunucusunun başlatılmasını geciktirebilir.*

> "The `resolveId`, `load`, and `transform` hooks may cause some files to load slower than others." (resmi-vite-performance.md)
*Plugin'larda `resolveId`, `load` ve `transform` hook'ları bazı dosyaların yavaş yüklenmesine neden olabilir. Bu hook'ların performans etkilerini optimize etmek için `vite --debug plugin-transform` komutu kullanılabilir.*
