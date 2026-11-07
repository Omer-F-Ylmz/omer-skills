# KUR-HEPSI-1 raporu
Ömer'in TEK komutu: `powershell -ExecutionPolicy Bypass -File C:\Projeler\omer-skills\tools\kur_hepsi.ps1`  (önce `-Deneme`; sonuç rapor\kur-hepsi-sonuc.tsv)

Betik satırı: 199 → 188 (KURULABILIR/OMER-SOR önce → sonra; sayım rapor/kur-hepsi-sayim.json).
- OMER-SOR 139 yorum → 49 BELİRSİZ + 9 >2 GB + 28 satır-yok + 3 hata10 (kalan 117 → 89 ile 2 GB/belirsiz sorulur).
- Lisans/uygulama gerekçesiyle geri alınıp KURULABİLİR'e geçen: 26 (rapor/kur-hepsi-lisans-geri.tsv); bunun 4'ü uygulama ≤2 GB (Eigent, EasySpider, artcraft, Orchestrator).
- KÜTÜPHANE'ye taşınan (npm view bin boş): 15 (rapor/kur-hepsi-kutuphane.tsv); yinelenenler tekilleştirildi (46 satır).
- Kur5Rel eklendi: 21 "asset URL yok" RELEASE satırı gh release latest ile indirilir (28 RELEASE, exe/msi'yi Ömer çalıştırır).
- Belirsiz 12 repo gh repo view + README ile yeniden doğrulandı (tmp/kh1/belirsiz-sonuc.tsv): TARS, hbot dahil; adı tutmayan/eski/riskli olanlar OMER-SOR kaldı.
- WINGET: `winget search/show` bu makinede 90 sn+ takıldı; kimlik doğrulaması ÖLÇÜLEMEDİ (6 kalem denendi hepsi zaman aşımı). 14 satır "WINGET-OLCULEMEDI" diye işaretli, -Sistem ile en sonda koşar.
- Sıkıştırma: mevcut omer-sikistir-gunluk görevi (.kos\kopru\sikistir_tum.py) `schtasks /run` + BelowNormal ile adım 0'da; adımlar arası boş alan <60 GB ise bekler/durur.

-Deneme (kur_hepsi.ps1): DENEME=8, ATLANDI=1 (kurulum_gurultu.ps1 henüz yok), HATA=0. kurulum_omer2.ps1 -Deneme -Sistem: DENEME=139 ZATEN=49 HATA=0. Atomic Chat SHA256 eşleşti, lightpanda ikilisi var.
Gerçek kurulum KOŞULMADI (sınıflandırıcı kuralı). Adım 3 -Deneme yalnız kapıları 3 kalemde çalıştırır.
Kullanılan: gh, npm view, winget (zaman aşımı), schtasks, mevcut üreticiler. Kullanılmayan: xerj/graphify/jev (betik düzenleme işi, katalog gerekmedi).
>2 GB tablo: rapor/omer-sor-2gb.md (9 kalem; Forge'un repo'su 0.05 GB, >2 GB olan model ağırlıkları).
