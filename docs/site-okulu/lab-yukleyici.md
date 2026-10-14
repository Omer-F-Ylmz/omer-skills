# lab · yükleyici % sayacı + giriş koreografisi (ref lando · mekanizma 9: nemotron ×2 + kendi bakış; Gemini kota 429, 4 tur kapalı)
Demo `labs/yukleyici/` · modül `tools/site-kit/sablon/src/sahne/yukleyici.js`.
- Mekanizma: three LoadingManager `onProgress` → GSAP ile yumuşatılan, geri gitmeyen 000–100 sayaç + ilerleme çubuğu; 100'de giriş bir kez çalışır. `enAz` (2 sn): önbellekte sayaç görünmeden bitmesin.
- Sayaç: basamak başı 0–9+0 şeridi, kilometre sayacı gibi kayar; konum `floor(p/b)%10 + max(0, p%b − (b−1))` (üst basamak taşımada birlikte döner).
- Koreografi: perde = SVG yolu, alt kenarı sıvı dalgası (orta geride kalır, genlik `sin(kπ)` ile geçişin ortasında tepe) yukarı → 0.25 sn sonra kamera dolly (power3.out 2.6 sn) → başlık harfleri (stagger 0.05) → alt başlık.
- Bütçe: giriş sürekli döngüde 60 fps; varlık yükü gerçek bayt (kitaplık dosyaları).
- Tuzak: varlıkları kademeli başlatmak `onLoad`'u ilk dosyada tetikler (sayaç 20'de 100'e atlar) → hepsini aynı anda kuyruğa koy. Sonradan eklenen varlık `onLoad`'u yeniden çağırır → `acildi` bayrağı.
- Tuzak: sayfanın `#yuk span` seçicisi sayaç şeritlerini de yakalayıp 16 px yaptı → `#yuk > span`. Örnek kare zamanı sayfa yüküne göre kayar; perde ≈ p .40–.70.
- Kamera hedefi başlıktan uzak tutulmalı (tur 1'de cezve başlığın altında kaldı).
- Kalan fark (Gemini): referansta tipografi sahnesi ve renk geçişi daha cesur; 3B ↔ DOM katman koreografisi.
- Mobil düşüş (önerilen, uygulanmadı): dolly kısalır.
