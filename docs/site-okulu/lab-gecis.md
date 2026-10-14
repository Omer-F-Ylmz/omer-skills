# lab · RT kompozit gürültü geçişi (ref activetheory · eşleşme 7, 4 tur tavanı)
Demo `labs/gecis/` · modül `tools/site-kit/sablon/src/sahne/gecis.js`.
- Mekanizma: A ve B sahneleri ayrı WebGLRenderTarget'a; tam ekran dörtgen `mix(A, B, smoothstep(eşik))`. Eşik = çapraz cephe (%55) + fbm yırtığı (%45).
- Kenar: ince sıcak çekirdek + fbm'li hale + hash kıvılcımları; hale bölgesinde UV kayması ve R/B kromatik ayrışma.
- Parametre: `t` 0→1 kaydırmanın orta üçte biri; t=0/1'de tek sahne çizilir (iki RT maliyeti yalnız geçişte).
- Bütçe: talep üzerine render → boşta 0 kare/sn; geçişte 2 sahne + 1 dörtgen.
- Tuzak: saf fbm eşiği "adacık" lekeler üretir (tur 1) → yönlü cephe ekle. B kamerasını aynı nesneye çevirmek puanı 7→4 düşürdü: geçiş farklı yer göstermeli.
- Kalan fark: referansın parçacık yoğunluğu/3B içerik zenginliği — mekanizma değil sahne içeriği; R3b'de parcacik modülüyle birleşince ölç.
- Mobil düşüş (önerilen, uygulanmadı): RT yarım çözünürlük.
