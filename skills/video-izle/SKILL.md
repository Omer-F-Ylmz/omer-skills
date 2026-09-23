---
name: video-izle
description: "YouTube videosunu kademeli izler: altyazı özeti → Jev ile süzme/soru → yalnız gereken anların karesi. CC'de PATH'te, Desktop'ta cc-kopru komut ile; claude.ai sandbox'ında koşmaz."
---

# video-izle — videoyu tümüyle okumadan izle

`video` CLI'si ham altyazıyı ve kareleri önbelleğe (`C:\Projeler\.video-cache\<id>\`, repo dışı) yazar;
ajana yalnız kompakt çıktı döner. Her kademe bir öncekinin önbelleğini kullanır, önbellek varsa ağa çıkılmaz.

## Kademeler (sırayla, gerektiği kadar)

```text
video izle <url|id> "<soru>" [-k 3]      # tek çağrı: ozet (önbellekli) + sor + görüntü gerekirse tek kare yolu; Jev ≤2, suz yok
video ozet <url|id|playlist>          # ≤6 satır: başlık, süre, segment, ~token; playlist tavanı 8
video suz <id> [--istek-tavan N]      # segment başına 1 Jev isteği; kesin "araç yok" atlanır, belirsiz okunur
video sor <id> "<soru>" [-k 5]        # tam 2 Jev isteği; ilgili k segment (≤2500 token) + görüntü gerekli mi
video kare <id> --t 12:30,14:05       # yalnız istenen anlar; --pencere 8 (sn, ±), 0 = tek kare
video kare <id> --suzgecten --en-fazla 3   # suz'un ekran olasılığı en yüksek anlar
video temizle [--gun 14]              # eski önbellek klasörlerini siler
```

Karar sırası:

0. Tek bir soru varsa (özellikle Desktop'ta) `izle` yeter: ozet satırları, ilgili segmentler ve gerekiyorsa tek kare yolu tek çıktıda.
1. Kademeli gidilecekse `ozet` ile başla. Altyazı yoksa çıktı `video --whisper <id>` önerir (yalnız CC, CPU, dakika tavanlı).
2. Belirli bir soru varsa `sor`; genel tarama gerekiyorsa `suz`. İkisi de Jev ister (TYPESAFE_API_KEY).
3. `sor` "görüntü gerekli" derse ya da `suz` ekran adayı listelerse, yalnız o zamanlar için `kare`.
4. Kareleri `Read` ile aç (görsel başına ~442 token, 768 px genişlik tavanı).

## kare nasıl çalışır

- `yt-dlp -g` ile doğrudan akış URL'si alınır; URL'deki `expire` süresine dek önbellekte tutulur.
- ffmpeg girişte atlar (`-ss` `-i`'den önce): yalnız istenen pencere okunur. Ölçüm: 16 sn pencere ~1 MB,
  tek kare ~0.3 MB. Video dosyası hiç yazılmaz.
- Pencere içinde ilk kare + sahne değişimleri (en çok 3); aHash ile tekrar kareler atılır, `--en-fazla` tavanı.
- Akış URL'si hiçbir çıktıya, hata mesajına ya da loga yazılmaz; hatada `<akış-url>` görünür.

## Desktop'ta cc-kopru koprusu ile

```text
komut(arac="video", args=["izle", "<url|id>", "<soru>"], cwd="C:/Projeler/omer-skills")
komut(arac="video", args=["ozet", "<id>"], cwd="C:/Projeler/omer-skills")
komut(arac="video", args=["kare", "<id>", "--t", "05:00", "--pencere", "0"], cwd="C:/Projeler/omer-skills")
```

- İzinli alt komutlar: `izle`, `ozet`, `suz`, `sor`, `kare`, `temizle`, `oku`, `paket`, `adlar`, `rapor-denetle`. `whisper` köprüde kapalı (uzun CPU işi).
- Jev anahtarları yalnız `jev` ve `video`'ya geçer (envGecir); öteki araçlardan silinir.
- Kare yolunu `oku` ya da dosya aracıyla aç; köprü yoksa kullanıcıdan CC'de koşturup çıktıyı yapıştırmasını iste.

## Yapma

- Tam altyazıyı ya da tüm segmentleri bağlama dökme; `sor`/`suz` çıktısıyla yetin.
- `kare`'yi zaman listesi olmadan tüm videoya yayma; önce `sor`/`suz` ile an seç.
- `--istek-tavan` olmadan uzun videoda `suz` koşarken tavanı (segment+10) kontrol et; ücretli istektir.
- Akış URL'sini ya da `akis.url` dosyasını okuyup yazdırma.

## Çıkış kodları

`0` tamam · `1` hata (mesaj tek satır) · `2` whisper kurulu değil (kurulum komutu basılır) · `3` altyazı yok.
