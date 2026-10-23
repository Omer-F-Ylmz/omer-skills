# DERS KİTABI — Web S3 3D/WebGL sahne
## A. En iyi yöntemler + tarif kartları (adım adım)
> "Shows how to return a teardown function from a matchMedia callback for custom cleanup" (resmi-c7-gsap-scrolltrigger.md)
**GSAP ScrollTrigger'da eşleşme ortamı (matchMedia) kullanırken, eşleşmeyen breakpoint'ta temizleme yapmak için bir teardown fonksiyonu döndürme yöntemi.**

---

> "lenisRef.value.lenis.on('scroll', ScrollTrigger.update)" (resmi-c7-lenis.md)
**Lenis ile GSAP ScrollTrigger senkronizasyonu: Lenis'in scroll olayını GSAP ScrollTrigger'a aktararak scroll animasyonlarını senkronize eder.**

---

> "gsap.ticker.add(update)" (resmi-c7-lenis.md)
**Lenis'in `raf` metodunu GSAP ticker'a ekleyerek Lenis'in smooth scroll animasyonlarını GSAP ticker'la senkronize eder.**

---

> "gsap.ticker.lagSmoothing(0)" (resmi-c7-lenis.md)
**GSAP ticker'daki lag smoothing'i kapatarak scroll animasyonlarında gecikmeyi önler.**

---

> "tl.scrollTrigger.refresh()" (resmi-c7-gsap-scrolltrigger.md)
**GSAP ScrollTrigger animasyonunun başlangıç/bitiş noktalarını yeniden hesaplamak için kullanılır.**

---
**Not:** Tüm yöntemler referans dosyalarından birebir alıntı yapılarak sunulmuştur.

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "Shows how to return a teardown function from a matchMedia callback for custom cleanup. ScrollTrigger automatically kills all ScrollTriggers created inside the function when the breakpoint no longer matches, so the teardown is only needed for non-ScrollTrigger animations." (resmi-c7-gsap-scrolltrigger.md)
Teardown fonksiyonu, matchMedia callback'inden döndürülerek breakpoint eşleşmeyen durumda özel temizleme işlemleri yapar. ScrollTrigger otomatik olarak breakpoint eşleşmeyen durumda içindeki tüm ScrollTrigger'ları öldürür, bu yüzden teardown sadece ScrollTrigger olmayan animasyonlar için gereklidir.

> "Documentation for the optional teardown function in ScrollTrigger.matchMedia() callbacks." (resmi-c7-gsap-scrolltrigger.md)
ScrollTrigger.matchMedia() callback'lerinde isteğe bağlı teardown fonksiyonunun belgelenmesi. Bu fonksiyon, breakpoint eşleşmeyen durumda özel temizleme işlemleri yapmak için döndürülür.

> "You can \[optionally] **return a function** which will be called when that breakpoint no longer matches so that you can do custom cleanup routines like killing other animations that aren't ScrollTrigger-related." (resmi-c7-gsap-scrolltrigger.md)
Breakpoint eşleşmeyen durumda çağrılacak isteğe bağlı bir fonksiyon döndürebilirsiniz. Bu fonksiyon, ScrollTrigger ile ilişkili olmayan diğer animasyonları öldürmek gibi özel temizleme işlemleri yapabilirsiniz.

> "Create a timeline with a ScrollTrigger, then after adding all animations, manually call tl.scrollTrigger.refresh() to recalculate its start/end. Alternatively, use the static ScrollTrigger.refresh() to refresh all instances." (resmi-c7-gsap-scrolltrigger.md)
ScrollTrigger ile bir timeline oluşturun, ardından tüm animasyonları ekledikten sonra tl.scrollTrigger.refresh() çağırarak başlangıç/bitişini yeniden hesaplayın. Alternatif olarak, tüm örnekleri yenilemek için statik ScrollTrigger.refresh() kullanın.

> "Integrates Lenis with GSAP ScrollTrigger. It updates ScrollTrigger on scroll, adds Lenis's raf to GSAP's ticker, disables lag smoothing, and cleans up on invalidate. Requires registering ScrollTrigger and setting autoRaf to false." (resmi-c7-lenis.md)
Lenis'i GSAP ScrollTrigger ile entegre eder. Kaydırma sırasında ScrollTrigger'ı günceller, Lenis'in raf'ini GSAP'in ticker'ına ekler, gecikme yumuşatmasını devre dışı bırakır ve geçersiz kılındığında temizleme yapar. ScrollTrigger'ın kaydedilmesi ve autoRaf'ın false olarak ayarlanması gerekir.

> "Frees all internal resources allocated by the renderer when it is no longer needed." (resmi-c7-threejs.md)
Renderer tarafından artık gerekli olmayan tüm dahili kaynakları serbest bırakır.

> "Constructor destructuring shows antialias defaults to false and powerPreference is passed to the WebGL context. The JSDoc documents 'high-performance' as a valid powerPreference value for maximum GPU performance." (resmi-c7-threejs.md)
Yapıcı fonksiyonun destructuring'inde antialias varsayılan olarak false olarak ayarlanır ve powerPreference WebGL bağlamına geçer. JSDoc, maksimum GPU performansı için geçerli bir powerPreference değeri olarak 'high-performance' belgelendi.

> "Creates 100 sphere meshes and continuously reallocates new ShaderMaterial instances during render, logging renderer.info.programs.length before and after calling dispose()." (resmi-c7-threejs.md)
100 adet küre mesh'i oluşturur ve render sırasında sürekli olarak yeni ShaderMaterial örnekleri yeniden ayırır, dispose() çağrısından önce ve sonra renderer.info.programs.length değerini kaydeder.

> "A helper that stops requestAnimationFrame when the page body scrolls offscreen. While not in the core renderer, this pattern is used in official Three.js examples to pause rendering and save GPU resources when the viewport is not visible." (resmi-c7-threejs.md)
Sayfa gövdesi ekrandan kaydırıldığında requestAnimationFrame'i durduran bir yardımcı. Bu desen, viewport görünür olmadığında render işlemini durdurmak ve GPU kaynaklarını tasarruf etmek için resmi Three.js örneklerinde kullanılır, ancak çekirdek renderer'da değil.

## C. Kalite kapısı kontrol listesi
> "Frees all internal resources allocated by the renderer when it is no longer needed." (resmi-c7-threejs.md)
*WebGLRenderer'ın dispose() metodu çağrıldığında, tüm GPU kaynaklarını serbest bırakır ve bellek sızıntılarını önler.*

---

> "ScrollTrigger automatically kills all ScrollTriggers created inside the media query function when that media query no longer matches." (resmi-c7-gsap-scrolltrigger.md)
*ScrollTrigger.matchMedia() içindeki ScrollTrigger'lar, breakpoint uyumsuzluğunda otomatik olarak durdurulur; teardown fonksiyonu yalnız ScrollTrigger dışı animasyonlar için gereklidir.*

---

> "lenisRef.value.lenis.on('scroll', ScrollTrigger.update)" (resmi-c7-lenis.md)
*Lenis'in scroll olayını GSAP ScrollTrigger ile senkronize eder; Lenis'in raf döngüsü GSAP ticker'a eklenerek performans sorunları önlenir.*

---

> "gsap.ticker.lagSmoothing(0)" (resmi-c7-lenis.md)
*GSAP ticker'ın gecikme yumuşatmasını devre dışı bırakarak, Lenis ile GSAP ScrollTrigger arasındaki senkronizasyon gecikmesini ortadan kaldırır.*

---

> "ScrollTrigger.refresh()" (resmi-c7-gsap-scrolltrigger.md)
*ScrollTrigger'ların başlangıç/bitiş noktalarını yeniden hesaplamak için kullanılır; özellikle timeline'lar güncellendiğinde gereklidir.*

---

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Shows how to return a teardown function from a matchMedia callback for custom cleanup. ScrollTrigger automatically kills all ScrollTriggers created inside the function when the breakpoint no longer matches, so the teardown is only needed for non-ScrollTrigger animations." (resmi-c7-gsap-scrolltrigger.md)
*GSAP ScrollTrigger'de breakpoint değişince otomatik olarak temizlenen ScrollTrigger'lar dışındaki animasyonlar için teardown fonksiyonu döndürülür.*

---

> "lenis/vue > Examples > GSAP integration" (resmi-c7-lenis.md)
*GSAP ScrollTrigger ile Lenis entegrasyonu için Vue.js örneği sağlar (Lenis'in raf metodu GSAP ticker'a eklenir, lag smoothing devre dışı bırakılır).*

---

> "Initialize a new Lenis instance for smooth scrolling" (resmi-c7-lenis.md)
*GSAP ScrollTrigger ile senkronize edilebilir, ucuz ve hafif smooth scroll çözümü (Lenis).*

---

> "Frees all internal resources of the renderer. Call this method if the renderer is no longer in use by your app." (resmi-c7-threejs.md)
*Three.js render edicinin kaynaklarını serbest bırakmak için `dispose()` yöntemi kullanılır (GPU belleği temizler).*

---

> "Creates 100 sphere meshes and continuously reallocates new ShaderMaterial instances during render" (resmi-c7-threejs.md)
*ShaderMaterial'in performans etkilerini ölçmek için test ortamı sağlar (dispose() ile GPU belleği temizleme örneği).*

---

> "A helper that stops requestAnimationFrame when the page body scrolls offscreen" (resmi-c7-threejs.md)
*IntersectionObserver ile viewport dışına çıkıldığında render durdurulur (GPU kaynakları tasarruf edilir).*

---

> "Use `threejs` for a single interactive scene with no scroll-authored journey" (skill-build-threejs-scroll-worlds.md)
*Scroll ile ilgisi olmayan basit Three.js sahnesi için Three.js kütüphanesi önerilir (ucuz ve doğrudan kullanım).*

---

## E. Proje bağlantısı: freelance sitesi, TELVE
> "The exact [Kage demo](demo/index.html) proves the quality bar; it is staging, not a mandatory subject or layout. Use its detailed anatomy only when the requested direction benefits from it: [references/kage-anatomy.md](references/kage-anatomy.md)." (skill-build-threejs-scroll-worlds.md)
Kage demo'sunun kalite referansı olarak kullanılması gerektiği belirtiliyor. Bu, projenin kalite standartlarını belirlemek için kullanılan bir referans olduğunu gösterir.

> "Use `threejs` for a single interactive scene with no scroll-authored journey." (skill-build-threejs-scroll-worlds.md)
Three.js kullanımı, yalnızca tek bir etkileşimli sahne oluşturmak için uygun olduğu belirtiliyor. Bu, projenin temel teknolojik seçimini gösterir.

> "Use `scroll-world-storytelling` when deciding between real-time 3D, pre-rendered video, and DOM-first storytelling." (skill-build-threejs-scroll-worlds.md)
Kaydırma dünyası hikayesi, gerçek zamanlı 3D, önceden işlenmiş video ve DOM-first hikayeleri arasında seçim yapmak için uygun olduğu belirtiliyor. Bu, projenin hikaye anlatım stratejisini gösterir.

> "Use `scroll-scrubbed-visual-sequence` for a video or image sequence whose time is scrubbed by scroll." (skill-build-threejs-scroll-worlds.md)
Kaydırma ile incelenmiş görsel dizisi, zamanının kaydırma ile incelenmesi için uygun olduğu belirtiliyor. Bu, projenin görsel dizilerini nasıl kullanacağını gösterir.

> "Use `cinematic-scroll-storytelling` for DOM-first GSAP/Lenis choreography." (skill-build-threejs-scroll-worlds.md)
Sinematik kaydırma hikayesi, DOM-first GSAP/Lenis koreografisi için uygun olduğu belirtiliyor. Bu, projenin hikaye anlatım stratejisini gösterir.

> "Use this skill when objects must remain truly spatial and interactive while scroll moves through several compositions in one live WebGL world." (skill-build-threejs-scroll-worlds.md)
Bu beceri, nesnelerin gerçek zamanlı WebGL dünyasında birkaç kompozisyon boyunca kaydırma sırasında gerçekten uzamsal ve etkileşimli kalması gerektiğinde kullanılır. Bu, projenin 3D dünyasını nasıl kullanacağını gösterir.
