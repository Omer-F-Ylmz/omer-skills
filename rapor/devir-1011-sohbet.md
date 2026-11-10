# Devir — 10 Kas 2026 03:20 (önceki sohbet: 9 Kas insta-video kurulum + PC donma + disk temizliği)

## Kurallar (Ömer, 9-10 Kas)
- Aynı anda TEK ağır iş; biri bitmeden diğeri başlamaz. İşler "pat küt" toplu başlatılmaz; sırayı Ömer'e yaz, onayla başlat.
- Silme ve sistem ayarı: önce doğrula, kesin liste getir, Ömer onaylayınca sil.
- Borsayı Ömer kapatırsa kendiliğinden açılmaz; açmak için Ömer söyler.
- Nihai kurallar (C:\Projeler\omer-kurallar.md) her zaman.

## Araç durumu
- Desktop'ta mcp-filesystem aracı düşebiliyor (açılışta havuz hazır değilken köprüler bağlanamıyor). Yedek yol ÇALIŞIYOR:
  betiği GitHub `ram-opt-2` dalına commit+push et, `tools/ram/indir.txt`'e yolu yaz, PC'de:
  cc-kopru komut: uv run --no-project https://raw.githubusercontent.com/Omer-F-Ylmz/omer-skills/<SHA>/tools/ram/indir.py <SHA>
  Çıktı okumak: cc-kopru `oku` (mod=aralik). cc-kopru python yalnız dosya + `--bayrak` kabul eder (konumsal argüman reddedilir).
- Kalıcı düzeltme YAPILMADI: tools/ram/mcp_koprusu.py açılışta havuz hazır olana kadar beklemeli.

## Bu sohbette yapılanlar
- RAM-OPT-2 (dal ram-opt-2): tools/ram/ram_kalkan_v2.py, desktop_havuz.py (Desktop'ta 10 MCP havuz köprüsüne alındı; yedek .kos/kopru/yedek/desktop-mcp/), mcp_olcum.py, oyun_modu.py, olcum_pc.py, olcum_derin.py, dogrula_sil.py, temizle_1.py, indir.py.
- Masaüstünde "Oyun Modu AC.cmd" / "Oyun Modu KAPAT.cmd" — HENÜZ DENENMEDİ. Kapsam dışı: HKCU Run (omer-kopru-bekci, Headroom, omer-headroom-guncelle) ve Başlangıç klasörü (omer-mcp-paylasim.vbs, OmniRoute.vbs).
- .kos/kopru/yetim.py: omer-skills tools/*.py süreçleri artık yetim sayılmıyor (test geçti).
- kurulum_d2.py: yalnız kaynağı değişen kalem yeniden işlenir; TUR2 yalnız tekrar edilebilir HATA; daha eski kurulum_d2 varsa bekler.
- borsa egit_surekli.py: kayit/DURDURULDU bayrağı. AÇIK HATA: Ömer "Python (14)" grubunu kapatınca bekçi de ölüyor, bayrak yazılmıyor, Görev Zamanlayıcı 10 dk'da bir geri açıyor → çözüm Oyun Modu (görevleri devre dışı bırakır) ya da ayrı "Borsa Kapat/Aç".
- defragsvc + ScheduledDefrag kapatıldı (Ömer, yönetici).
- Disk temizliği 1 (onaylı): boş 80,2 → 111,3 GB. Go önbelleği +12,1 · npm +6,5 · Temp +5,6 · NetBeans +2,5 · Thunderstore +1,9 · DriverHub +1,8 · pip +1,0. uv önbelleği kilitli, temizlenemedi.

## Çalışıyor olabilir (kontrol et)
- temizle_1.py arka planda: silme BİTTİ; model kullanım taraması + C:\AI / Program Files / Epic / Steam / Riot tam ölçümü sürüyordu → rapor/temizle-1.txt (L14+).
- borsa eğitimi (egit_surekli + 12 işçi), tasima_izle.
- Bu sohbetin zamanlanmış kontrolü SİLİNDİ.

## Bekleyen kararlar (Ömer)
- araclar/indir/ComfyUI_windows_portable_nvidia.7z (1,9 GB): ComfyUI kuruluysa silinsin mi.
- Modeller (~100 GB): temizle-1.txt'teki kullanım taramasına göre hiçbir işte geçmeyenler silme adayı; Ömer "kullanmadıklarımızı sil" dedi, liste görünce onay.
- Eski kayıt/log (CC projects 15+ gün 4,5 GB · köprü log 4,9 GB · köprü rapor 3,2 GB): önce 2. beyne işlenmiş mi kontrol et, sonra öner.
- Karantina 4 GB; u3d-venv + tts-venv 9,9 GB; Flashpoint 3,9 GB.
- Liste 1 (açılış programları) ve Liste 3 (servisler; yönetici komutu Ömer çalıştırır) henüz onaylanmadı.
- Maxun pip paketi (denetim YANLIS) kaldırılsın mı.
- DOKUNULMAZ: araclar/link27 (20 kurulu araç kullanıyor), link30eki, link30eki-2, ana-liste-npm-2.

## Insta-video kurulum durumu (9 Kas 21:55 ölçümü)
- 3.930 video, ana-liste-v2 6.933 kalem; kurulabilir 3.067: KURULU 437 · ZATEN 203 · HİÇ İŞLENMEDİ 851 · YANLIŞ EŞLEŞME 604 · HATA 308 · kaynak bulunamadı 297 · model 155 · yol yok 109 · güvenlik 73 · genel terim 14.
- kaynak-bul: 624 karar (BULUNDU 167 → rapor/kaynak-bul-0911-coz.tsv kurulmayı bekliyor). Hakem-coz 46, denetim-coz 22, derin-coz 4 ADAY.
- TUR2 20:50'de durduruldu (PC donmalarının şüphelisi: büyük klon + derleme + Defender).
- Onaylı iş sırası (hafiften ağıra, tek tek): 3 güvenlik/genel-terim incelemesi → 4 doğrulanamayan 40 + belirsiz 25 → 5 ana liste durum sütunu + kategori dizini → 7 bulunan ~239 kaynağın kurulumu (tek iş parçacığı) → 851 işlenmemiş kalemin kaynak çözmesi + kurulumu → 8 yol-yok/bulunamayan yeniden arama → 6 yöntemler (1.158) kurallara/skill'lere → 9 claude.ai paketi + CC doğrulama → 10 borsa → 11-13 sıkıştırma / silme / TUR2 (2 GB+ repo ve uygulamalar Ömer'e sorulur).
- Görev dosyası tools/gorev-kurulum-buyuk-v5.md; is_sirasi'nın CC oturumu ve bekçisi durdurulmuş olabilir.

## Borsa botu
- Eğitim (genetik) tıkalı: en iyi skor -0,020, hiç artıya geçmedi, sürekli "durgunluk → yeniden başlat". Taşıma (fonlama) stratejisi sanal parada küçük artıda. Kurulum işinden sonra strateji/eğitim yöntemi ayrıca ele alınacak.
