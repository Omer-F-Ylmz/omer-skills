# lab · makro sıvı/köpük malzemesi (yeni lab yok — mevcut modül)
Modül `tools/site-kit/sablon/src/sahne/sivi-glsl.js` (TELVE R0d–R2c'de ayarlandı; `fincan.js` onBeforeCompile ile enjekte eder).
- Mekanizma: ağın arka yüzü = yüzey kapağı, ışın eğri yüzeyle kesilip oradan boyanır; yükseklik = advekte dalga dokusu (`uYuk`) + dönme paraboloidi (`uPar`) + köpük kubbesi (fbm).
- Köpük/crema: worley ×38/×90/×110 kabarcık katmanları, merkez açık → kenar koyu altın-fındık; advekte harita (`uSan`) desen ve benekleri akışla gerer.
- Hacim: koyu katman kenarda amber geçirir, süt/köpük saçıcı (neredeyse opak); katman ara yüzü gecikmeli kopyayla dalgalanır, sınırda fbm mermerleşme.
- Duvar köpük izi ayrı saydam geçiş (alfa karışımı); ağız gölgesi analitik.
- Tuzak (TELVE kayıtları F1/E1/E7/T1): dalga tepesi diski aşınca kama → yumuşak min doyum; değer gürültüsü step eşiği tuğla deseni → yumuşak kavisli halka; atan·worley kapakta ±π dikişi.
- Ekran uzayı akışkan (Navier-Stokes ping-pong, lusion/igloo) TELVE'de gerekmez (eksikler.md #5); imleç izi istenirse Dobryakov WebGL-Fluid (MIT).
- Neden lab yok: mekanizma TELVE'de ölçülüp kabul edildi; ayrı demo aynı shader'ı kopyalardı.
