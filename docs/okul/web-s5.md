# DERS KİTABI — Web S5 Yayın ve kapanış
## A. En iyi yöntemler + tarif kartları (adım adım)
> "When it is time to deploy your app for production, simply run the `vite build` command." (resmi-vite-build.md)
*Üretim için uygulamanızı derlemek için `vite build` komutunu çalıştırın.*

> "By default, it uses `<root>/index.html` as the build entry point, and produces an application bundle that is suitable to be served over a static hosting service." (resmi-vite-build.md)
*Varsayılan olarak, `<root>/index.html` derleme giriş noktası olarak kullanılır ve statik barındırma hizmeti üzerinden sunulabilecek bir uygulama paketi üretir.*

> "When you are developing a browser-oriented library, you are likely spending most of the time on a test/demo page that imports your actual library." (resmi-vite-build.md)
*Tarayıcıya yönelik bir kütüphane geliştiriyorsanız, çoğunlukla kütüphanenizi içe aktaran test/demo sayfalarında zaman geçireceksiniz.*

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "If a lower target is set, Vite will still require these minimum browser support ranges" (resmi-vite-build.md)
*Düşük hedef tarayıcı sürümleri belirlenirse bile, Vite hala en az bu tarayıcı desteği gereksinimlerini korur.*

> "The legacy chunks are conditionally loaded only in browsers that do not have native ESM support" (resmi-vite-build.md)
*Eski tarayıcı desteği için oluşturulan parçalar, yalnızca ESM desteği olmayan tarayıcılarda koşullu olarak yüklenir.*

> "If you specify a different root, remember that `import.meta.dirname` will still be the folder of your `vite.config.js` file" (resmi-vite-build.md)
*Farklı bir kök dizini belirtildiğinde, `import.meta.dirname` hala `vite.config.js` dosyasının bulunduğu dizini gösterir.*

> "If the `package.json` does not contain `"type": "module"`" (resmi-vite-build.md)
*`"type": "module"` belirtmeyen `package.json` dosyaları için, Vite farklı dosya uzantıları üretir.*

> "If you are building non-browser libraries, or require advanced build flows" (resmi-vite-build.md)
*Kütüphane modu, yalnızca tarayıcı odaklı ve JS çerçeveleri için basit bir yapılandırma sağlar.*

> "If the hashed assets and public files aren't deployed together" (resmi-vite-build.md)
*Eşlenmemiş varlıklar için, `renderBuiltUrl` fonksiyonu ile ayrı yol yapılandırmaları sağlanır.*

> "If the live tools are unavailable" (skill-wq-accessibility.md)
*Canlı araçlar kullanılmazsa, Lighthouse CLI veya axe gibi otomatik araçlar kullanılır.*

## C. Kalite kapısı kontrol listesi
> "When it is time to deploy your app for production, simply run the `vite build` command. By default, it uses `<root>/index.html` as the build entry point, and produces an application bundle that is suitable to be served over a static hosting service." (resmi-vite-build.md)
Uygulamanın üretim için derlenmesi için varsayılan olarak `<root>/index.html` kullanılır ve statik bir barındırma hizmeti üzerinden sunulmaya uygun bir uygulama paketi oluşturulur.

> "By default, the production bundle targets the minimum browser versions compatible with [Baseline](https://web-platform-dx.github.io/baseline/) Widely Available as of a date fixed for each major release. The default browser support range for this major is:" (resmi-vite-build.md)
Varsayılan olarak, üretim paketi her büyük sürüm için belirli bir tarihte [Baseline](https://web-platform-dx.github.io/baseline/) tarafından belirlenen en düşük tarayıcı sürümlerini hedefler.

> "If you are deploying your project under a nested public path, simply specify the [`base` config option](/config/shared-options.md#base) and all asset paths will be rewritten accordingly. This option can also be specified as a command line flag, e.g. `vite build --base=/my/public/path/`." (resmi-vite-build.md)
Eğer projenizi iç içe geçmiş bir genel yolda dağıtıyorsanız, sadece [`base` yapılandırma seçeneğini](/config/shared-options.md#base) belirtin ve tüm varlık yolları buna göre yeniden yazılacaktır. Bu seçenek ayrıca bir komut satırı bayrağı olarak da belirtilebilir, örneğin `vite build --base=/my/public/path/`.

> "Vite emits `vite:preloadError` event when it fails to load dynamic imports. `event.payload` contains the original import error. If you call `event.preventDefault()`, the error will not be thrown." (resmi-vite-build.md)
Vite, dinamik içe aktarmaları yüklerken başarısız olduğunda `vite:preloadError` olayını yayar. `event.payload`, orijinal içe aktarma hatasını içerir. Eğer `event.preventDefault()` çağırırsanız, hata fırlatılmaz.

> "When a new deployment occurs, the hosting service may delete the assets from previous deployments. As a result, a user who visited your site before the new deployment might encounter an import error. This error happens because the assets running on that user's device are outdated and the code tries to import the corresponding old chunk, which is deleted. This event is useful for addressing this situation. In this case, make sure to set `Cache-Control: no-cache` on the HTML file, otherwise the old assets will be still referenced." (resmi-vite-build.md)
Yeni bir dağıtım gerçekleştiğinde, barındırma hizmeti önceki dağıtımlardan gelen varlıkları silebilir. Sonuç olarak, yeni dağıtımdan önce sitenizi ziyaret eden bir kullanıcı, içe aktarma hatasıyla karşılaşabilir. Bu hata, kullanıcının cihazında çalışan varlıkların eski olması ve kodun silinmiş eski parçayı içe aktarmaya çalışması nedeniyle oluşur. Bu olay, bu durumu çözmek için kullanışlıdır. Bu durumda, eski varlıkların hala başvurulduğunu önlemek için HTML dosyasına `Cache-Control: no-cache` ayarlayın.

> "If the live tools are unavailable, use Lighthouse CLI or axe for automated coverage and complete the same manual checks. Automated tools detect only a subset of accessibility barriers: a score of 100 is not WCAG conformance, and a low score does not replace issue-level evidence." (skill-wq-accessibility.md)
Canlı araçlar kullanılamıyorsa, otomatik kapsam için Lighthouse CLI veya axe kullanın ve aynı manuel kontrolleri tamamlayın. Otomatik araçlar yalnızca erişilebilirlik engellerinin bir alt kümesini algılar: 100 puan WCAG uyumluluğu değildir ve düşük puan sorun düzeyi kanıtı yerine geçmez.

> "Run live Lighthouse SEO and Agentic Browsing checks when that capability is available; with Chrome DevTools MCP, use `lighthouse_audit`." (skill-wq-seo.md)
Olasıysa canlı Lighthouse SEO ve Agentic Browsing kontrollerini çalıştırın; Chrome DevTools MCP ile `lighthouse_audit` kullanın.

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "When it is time to deploy your app for production, simply run the `vite build` command." (resmi-vite-build.md)
Vite ile üretim için derleme komutu çalıştırın.

> "You can specify custom targets via the [`build.target` config option](/config/build-options.md#build-target), where the lowest target is `es2015`." (resmi-vite-build.md)
Özel tarama hedeflerini ayarlayabilirsiniz, en düşük hedef es2015 olmalıdır.

> "If you don't know the base path in advance, you may set a relative base path with `"base": "./"` or `"base": ""`." (resmi-vite-build.md)
Temel yolunuzu önceden bilmiyorsanız, göreceli bir temel yol ayarlayabilirsiniz.

> "You can enable Rolldown watcher with `vite build --watch`." (resmi-vite-build.md)
Rolldown izleyicisini etkinleştirmek için `vite build --watch` komutunu kullanın.

> "If you specify a different root, remember that `import.meta.dirname` will still be the folder of your `vite.config.js` file when resolving the input paths." (resmi-vite-build.md)
Farklı bir kök belirliyorsanız, giriş yollarını çözerken `import.meta.dirname` hala `vite.config.js` dosyanızın klasörü olacaktır.

> "If the live tools are unavailable, use Lighthouse CLI or axe for automated coverage and complete the same manual checks." (skill-wq-accessibility.md)
Canlı araçlar kullanılamıyorsa, otomatik kapsam için Lighthouse CLI veya axe kullanın ve aynı el ile kontrolleri tamamlayın.

> "Prefer **bundling polyfills at build time** (Babel/SWC + `core-js`, or `@vitejs/plugin-legacy`) targeted by your supported-browsers list." (skill-wq-best-practices.md)
Desteklediğiniz tarayıcıların listesine göre derleme zamanında polyfill'leri paketlemeyi tercih edin.

> "If live tools are unavailable, use category-specific Lighthouse CLI output plus direct source and HTTP inspection." (skill-wq-seo.md)
Canlı araçlar kullanılamıyorsa, kategori özgü Lighthouse CLI çıktısı ile birlikte doğrudan kaynak ve HTTP incelemesini kullanın.

## E. Proje bağlantısı: freelance sitesi, TELVE
> "When it is time to deploy your app for production, simply run the `vite build` command. By default, it uses `<root>/index.html` as the build entry point, and produces an application bundle that is suitable to be served over a static hosting service." (resmi-vite-build.md)
Vite ile oluşturulan uygulamaların üretim için derlenmesi ve statik hosting servislerine uygun hale getirilmesi için `vite build` komutunu kullanın.

> "If you are deploying your project under a nested public path, simply specify the [`base` config option](/config/shared-options.md#base) and all asset paths will be rewritten accordingly." (resmi-vite-build.md)
Projenizi iç içe geçmiş bir public path altında yayınlıyorsanız, [`base` config seçeneğini](/config/shared-options.md#base) belirleyerek tüm asset yolları otomatik olarak yeniden yazılacaktır.

> "Comprehensive accessibility guidelines based on WCAG 2.2 and Lighthouse accessibility audits. Goal: make content usable by everyone, including people with disabilities." (skill-wq-accessibility.md)
WCAG 2.2 ve Lighthouse erişilebilirlik denetimlerine dayalı kapsamlı erişilebilirlik kılavuzları. Hedef: engelli kişiler dahil herkesin içeriğe erişebilmesi.

> "Modern web development standards based on Lighthouse best practices audits. Covers security, browser compatibility, and code quality patterns." (skill-wq-best-practices.md)
Lighthouse en iyi uygulamalar denetimlerine dayalı modern web geliştirme standartları. Güvenlik, tarayıcı uyumluluğu ve kod kalitesi desenlerini kapsar.

> "Search engine optimization based on Lighthouse SEO audits and Google Search guidelines. Focus on technical SEO, on-page optimization, and structured data." (skill-wq-seo.md)
Lighthouse SEO denetimlerine ve Google Arama kılavuzlarına dayalı arama motoru optimizasyonu. Teknik SEO, sayfa içi optimizasyon ve yapılandırılmış veriye odaklanın.

> "The build can be customized via various [build config options](/config/build-options.md). Specifically, you can directly adjust the underlying [Rolldown options](https://rolldown.rs/reference/)" (resmi-vite-build.md)
Derleme çeşitli [derleme yapılandırma seçenekleri](/config/build-options.md) aracılığıyla özelleştirilebilir. Özellikle, altta yatan [Rolldown seçenekleri](https://rolldown.rs/reference/) doğrudan ayarlanabilir.
