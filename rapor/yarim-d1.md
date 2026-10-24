# YARIM-D1 — Video veri boşlukları (24 Eki)

- derin-tamamla-1: DEVAM. Karusel/post: 126 bekleyen /p gönderisinin 125'i gallery-dl ile TÜM slaytlarla işlendi (derin/<kod>.json, kare_sayisi dolu); 1 kalıcı HTTP 400 (Dd1LC_5jPfM, video-atla'da). Kalan 901 YouTube linki: arka-istek/yarim-d1-yt.json (gözetmenli, --es 3). IG tarafı bitti (kalan 0). ig-silinen.txt'ye ekleme YOK: HTTP 400 nedenleri Chrome'da doğrulanmadı.
- derin-toplu-7: BİTTİ. ig-42-kalan 24 linkin 16'sı çerezle artık işlendi; 8'i HTTP 400 (kalıcı) → video-atla.txt'e eklendi (126→134 kod).
- link-sayim-1: ZATEN BİTMİŞ + yenilendi (link_durum.py): 15349 kod; ig-post bekliyor 126→~1; post kare_sayisi dolu 344/480 (sayım yenilenmedi, işlem sonrası artar).
- ig-toplu-2: ZATEN BİTMİŞ (c4c90926, d3d0d144): 8/16 video ok + 8 karusel; 8 HTTP 400 kalıcı.
- video-denetim-1: ZATEN BİTMİŞ (b65abddb).
- ig-42: ZATEN BİTMİŞ (bf932bfc). ig-ornek-1: ZATEN BİTMİŞ (47b4e1d7, 73d17214).
- ig-giris-1: çerez .kos/ig-cookies.txt geçerli; değer yazılmadı.
- Kod değişikliği yok (test gerekmedi); d1-run.py yalnız .kos/ (gitignore) içinde, ATLA_DOSYA'yı geçersiz kılıp /p gönderilerini isle_post'a verir.
- Devam: 901 YT için `.kos/kopru/yarim-d1-yt.log` (DURUM/BITIS) izle; bitmezse `gorev-yarim-d1-devam.md`.
