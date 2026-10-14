# Oyun kitabı — video içerik (ATLAS-2)

Karar kaynağı: `docs/atlas/kart.jsonl` (`karar` · `kosul`); aynı karar `docs/katalog/yetenek.jsonl` satırında. VARSAYILAN = her uygun işte; GEREKİNCE = koşulu kartta; KULLANMA = kurulu kalır, seçilmez.

## 0. Hangi skill (ayrım satırı — seçimde en sık kaçan yer)
- Tek video/reel izle, anlat, "hangi aracı gösteriyor, nasıl kurulur" → `video-izle` (kurulum soruysa raporun "nasıl kurulur" bölümü yeter; aday dosyası açılmaz).
- Birden çok link / kuyruk / toplu tarama → `video-tarama` (link başına `video-tarayici` alt ajanı).
- İzlenen videodaki aracı/tekniği **projeye uygula, aday dosyasına çevir, kur** → `video-uygula` (aday başına `aday-arastirici`).
- Video **üret** (reel, kısa, açıklayıcı) → C. bölüm; izleme skill'i değil.

## A. İzleme / tarama hattı (VARSAYILAN)
| Adım | Araç | Komut | Kapı |
|---|---|---|---|
| A1 İndir + kare | `video` CLI (`video-cli`) · `ffmpeg` | `video paket <url>` (yt-dlp + kare + Whisper) | RAM kapısı CLI içinde |
| A2 Görsel okuma | `gemini-omni-flash-api` | `video kisa <id...>` (kısa, Gemini önce; Claude yalnız eksik kısım) | Gemini 429 → kuyrukta bekle, Claude'a düşme |
| A3 Rapor | `video-tarayici` alt ajanı | paket.md + kareler → rapor; `video rapor-denetle` | Denetim temiz değilse rapor yok sayılır |
| A4 Toplu | `video-tarama` | `video parti baslat <kuyruk.md> --short --cagri-tavan N --usd-tavan X` · `video parti durum/devam <pid>` | Tavan sayısı zorunlu |
| A5 Uygula | `video-uygula` + `aday-arastirici` | `video on --repo` → `video uret <ad>` | Lisans satırı (MIT/Apache değilse koşul raporda) |

## B. Kısa video hattı (VİDEO-KISA kuyruğu)
1. Kuyruk: `video parti kuyruk --short --en-fazla N --usd-tavan X` (180 link sırada; parti başına N ≤ 20).
2. `video kisa` Gemini kolu; Claude adımı yalnız birleştirme/karar (VİDEO-KISA-TOKEN-1 ölçüsü: hedef ≤%30 jeton).
3. `video parti akil <pid>` → teknik/araç satırları `video teknik <rapor>` ile kataloga.
4. Kapanış `video parti kapat <pid>`; regresyon `video t0-regresyon`.

## C. Video üretimi (GEREKİNCE)
- `remotion-best-practices` → Remotion ile kodla video; ayrıntı `remotion-*` (render, captions, multimedia).
- `hyperframes:hyperframes` → HTML/CSS kompozisyonla video (Remotion alternatifi; ikisi birden seçilmez).
- `vid-*` ajanları → hat içi tek adım (ffmpeg dönüştür, altyazı/ses düzeni, kanca merdiveni, senaryo).
- `autoclip-paket` → uzun videodan otomatik kısa klip; `reel-plan` → reel senaryo planı.
- `moneyprinter-paket` → stok + TTS ile tam otomatik deneme; marka işi değil.

## KULLANMA
- `video-tarayici-haiku` — TOKEN-DENEME-2a deneme kolu; varsayılan `video-tarayici`.
- `ecc:remotion-video-creation` yerine `remotion-best-practices` (ATLAS-1 kararı).
- `*-paket` kaynak paketleri doğrudan değil; asıl skill yetmezse tarif kaynağı.

## İş sırası
izle/tara (A) → teknik çıkar (A5/B3) → gerekirse üret (C) → doğrula (kare + süre + ses seviyesi) → rapor.

## Token ipucu
- Görsel okuma Gemini'de; Claude kareyi yalnız çelişkide açar (≤4 kare).
- Alt ajan tek satır prompt (id · paket · kareler · rapor) alır, ≤5 satır döner.
- Uzun transkript ana bağlama girmez; `video ozet` / `video oku` dar bölüm.
- Paralel parti yerine tek parti + tavan; 429'da bekle, model değiştirme.
