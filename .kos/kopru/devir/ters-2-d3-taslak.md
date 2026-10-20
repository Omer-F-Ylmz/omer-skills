# ★ d3 TASLAK — TERS-2 kapı (d2 yarım kaldı, 20 Eki 21:30)
Durum: dotnet/js hedefleri tamam (Fiyat, Fiyat.Tests, ink-puppet, markdown-table; 2 tekrar × 2 kol). Site hedefi yalnız parcacik tekrar 1 (skill 0.726, zemin 0.677). 5 site hedefi + 3 yeni hedef (11 ses, 12 ortak-js, 13 Halka; hedefler.json'da, koşuya girmedi) kalan.
Duran neden: hakem sayacı 70/70 (sayac-hakem.json, %TEMP%\ters-kapi); hakem çağrılarının çoğu 'hata meta' (Cloudflare kota) + google/alibaba hatası → hata çağrıları da sayılıyor, Haiku üçüncü sürekli devrede.
d3 adımları: (1) hakem tavanını artırmadan önce Ömer'e/DUR: tavan 70 → karar gerek (öneri: hata dönen çağrıyı sayma, yalnız başarılıyı say; tavan aynı kalır). (2) RAM <%88 bekle (Headroom ~2 GB baskın). (3) python tools/ters/kapi_kos.py (önbellek: yazar 26/60) arka.py ile. (4) kapı geçerse kapanış.
Koşucu değişikliği (d2): hedefler tarayıcısızdan başlar; RAM 10 dk×3 sonra RamYok → site atlanan yarım bırak; YARGIC'a mistral eklendi.
