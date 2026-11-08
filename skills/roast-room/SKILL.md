---
name: roast-room
description: Bir kararı, planı ya da iş fikrini 7 persona ajanla 3 turda "kızartır" (puan → çürütme → ağırlıklı karar) ve .roast-room/<tarih>.md'ye kaydeder. "roast et", "bu fikri kızart", "şeytanın avukatı", "karar vermeden önce eleştir", "roast room" isteklerinde kullan.
---

# roast-room

Kaynak: IG Roast Room yapısı (repo yok, kur-ozet.md:138), şef skill + 7 persona alt ajan + brains/<ajan>/hot.md, 3 tur.

## Personalar (`.claude/agents/roast-*.md`, model haiku)
| ajan | soru |
|---|---|
| roast-geri-donus | Geri alınabilir mi, geri almanın bedeli ne? |
| roast-nakit | Para nereden çıkar, nakit akışı ve geri dönüş süresi? |
| roast-musteri | Müşteri bunu gerçekten ister mi, kanıt ne? |
| roast-teknik | Teknik risk, bağımlılık, bakım yükü? |
| roast-zaman | Zaman/fırsat maliyeti; bunun yerine ne yapılmaz? |
| roast-hukuk | Hukuk/KVKK/sözleşme/lisans riski? |
| roast-seytan | Şeytanın avukatı: en güçlü karşı tez. |

## Akış
1. Konuyu tek paragrafa indir (karar + bağlam + kısıt). Eksikse kullanıcıya tek soru sor.
2. **Tur 1, puan:** 7 ajanı paralel çağır (Agent, `subagent_type: roast-<ad>`). Her biri `skills/roast-room/brains/<ad>/hot.md`'yi okur, 0-10 puan + en fazla 3 gerekçe döner.
3. **Tur 2, çürütme:** Tur 1 özetini (ajan başı 1 satır) tüm ajanlara ver; her biri başka bir ajanın en zayıf gerekçesini çürütür ya da kendi puanını günceller.
4. **Tur 3, karar:** Şef (sen) ağırlıklı ortalama alır. Ağırlık varsayılanı eşit; geri-dönüş ve hukuk puanı ≤3 ise "veto adayı" işaretle. Çıktı: GİT / KOŞULLU GİT / GİTME + koşullar + en büyük 3 risk.
5. Kayıt: `.roast-room/<YYYY-MM-DD-HHMM>.md` (konu, 3 tur tablosu, karar). PDF istenirse `make-pdf` skill.
6. Her ajanın tur 2 sonunda öğrendiği tek satırı `brains/<ad>/hot.md` sonuna ekle (en fazla 20 satır; eskisini sil değil, en eskiyi kırp).

## Kurallar
- Ajan çıktısı ajan başı ≤120 kelime; şef tüm metni değil özetleri taşır.
- Ajanlar dosya yazmaz; hot.md güncellemesini şef yapar.
- Oturum ortası yeni eklenen ajan tanımı yüklenmez: ilk kullanım yeni oturumda. O zamana dek `general-purpose` + persona metni (ajan dosyasının gövdesi) ile çağır.
