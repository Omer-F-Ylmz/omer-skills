# lab · ses tasarımı (kullanıcı açar, varsayılan kapalı)
Modül `tools/site-kit/sablon/src/sahne/ses.js`, lab `labs/ses/` (kamera yolu sahnesi + sağ üst düğme; referans shopify/igloo "Sound: Off" düğmesi).
- Mekanizma: AudioContext yalnız düğme tıkında doğar; köz uğultusu = 3 detune testere (55/55/82 Hz) → alçak geçiren; seyrek dürtülü gürültü tamponu = çıtırtı. `ayarla(p)` kaydırmayı filtre kesimine (240→2440 Hz, p²) ve çıtırtı düzeyine bağlar; `tik()` etkileşim sesi.
- Sentez Web Audio: ses dosyası, lisans, Tone/howler bağımlılığı yok (Freesound CC0 öğe gerekirse `AudioBufferSourceNode` ile aynı `ana` düğümüne bağlanır).
- Parametre: `ses(dugme, { duzey = 0.4 })`; açma/kapama `setTargetAtTime` 0.25 sn sönüm.
- Bütçe: kapalıyken 0 DSP (bağlam yok ya da suspend); açıkken 4 kaynak + 1 filtre.
- Tuzak: kapatınca yalnız gain 0 yetmez → sönüm bitince `suspend()`; sekme gizlenince suspend/resume. Düğme `aria-pressed` + metin durumu taşır.
- Kabul (görsel yargı uygulanamaz → `lab.olc()` öz-denetimi, headless): önce bağlam yok ✓, açınca RMS 0.042 ✓, kaydırma sonu spektral merkez 247→7471 Hz ✓, kapanınca `suspended` ✓.
- Mobil: iOS sessiz anahtarı Web Audio'yu susturur — düğme metni yine doğru; ek iş yok.
