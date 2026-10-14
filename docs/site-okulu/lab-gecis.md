# lab · RT kompozit gürültü geçişi (ref activetheory · mekanizma Gemini med 7 / nemotron 8, 4 tur kapalı)
Demo `labs/gecis/` · modül `tools/site-kit/sablon/src/sahne/gecis.js`.
- Mekanizma: A ve B sahneleri ayrı WebGLRenderTarget'a; tam ekran dörtgen `mix(A, B, smoothstep(eşik))`. Eşik = merkezden açılan portal (en-boy düzeltmeli yarıçap + fbm kenar); lab'da portal %70 + A'ya dalış / B'de geri çekilme dolly (d3).
- Kenar: ince sıcak çekirdek + fbm'li hale + hash kıvılcımları; hale bölgesinde UV kayması ve R/B kromatik ayrışma.
- Parametre: `t` 0→1 kaydırmanın orta üçte biri; t=0/1'de tek sahne çizilir (iki RT maliyeti yalnız geçişte).
- Bütçe: talep üzerine render → boşta 0 kare/sn; geçişte 2 sahne + 1 dörtgen.
- Tuzak: saf fbm eşiği "adacık" lekeler üretir (tur 1) → yönlü cephe ekle. B kamerasını aynı nesneye çevirmek puanı 7→4 düşürdü: geçiş farklı yer göstermeli.
- Kalan fark: referansın parçacık yoğunluğu/3B içerik zenginliği — mekanizma değil sahne içeriği; R3b'de parcacik modülüyle birleşince ölç.
- d5 tur 5: parçacık/sis geçişin parçası sayıldı → shader'a halka çevresi duman bandı (dışa sürüklenen fbm), kutupsal hücrelerde dışa uçan közler, t'de kayan çarpık yırtık + ivme eğrisi (mix(t, smoothstep, .65)); ek RT/çağrı yok. Yargı 15 Eki 10:00 sonrası.
- Mobil düşüş (önerilen, uygulanmadı): RT yarım çözünürlük.
