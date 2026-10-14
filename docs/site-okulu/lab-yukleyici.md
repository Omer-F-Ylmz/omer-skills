# lab · yükleyici % sayacı + giriş koreografisi (ref lando · eşleşme 7)
Demo `labs/yukleyici/` · modül `tools/site-kit/sablon/src/sahne/yukleyici.js`.
- Mekanizma: three LoadingManager `onProgress` → GSAP ile yumuşatılan, geri gitmeyen 000–100 sayaç + ilerleme çubuğu; 100'de giriş bir kez çalışır.
- Koreografi: perde (clip-path inset, alt kenarı yuvarlak) yukarı → 0.25 sn sonra kamera dolly (power3.out 2.6 sn) → başlık harfleri (stagger 0.05) → alt başlık.
- Bütçe: giriş sürekli döngüde 60 fps; varlık yükü gerçek bayt (kitaplık dosyaları).
- Tuzak: varlıkları kademeli başlatmak `onLoad`'u ilk dosyada tetikler (sayaç 20'de 100'e atlar) → hepsini aynı anda kuyruğa koy. Sonradan eklenen varlık `onLoad`'u yeniden çağırır → `acildi` bayrağı.
- Kamera hedefi başlıktan uzak tutulmalı (tur 1'de cezve başlığın altında kaldı).
- Kalan fark (Gemini): referansta tipografi sahnesi ve renk geçişi daha cesur; 3B ↔ DOM katman koreografisi.
- Mobil düşüş (önerilen, uygulanmadı): dolly kısalır.
