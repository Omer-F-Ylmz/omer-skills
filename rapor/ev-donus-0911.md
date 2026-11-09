# Eve dönüş sırası (9 Kas 2026)

Durum: 10:30'da kalkan v1 askıdaki 45 süreci aynı anda açtı (borsa 12 işçi dahil), RAM fırladı, Desktop köprüsü dondu.
Arka plan işleri Desktop'tan bağımsız; 10:34'te RAM %77.8 ile kalkan çalışıyordu, sonrası görülemedi.

## 1. Desktop'u kapatıp aç (Ömer)
Görev çubuğundan çık → yanıt vermezse Görev Yöneticisi → Claude → Görevi sonlandır → yeniden aç.

## 2. Ölç (Claude, salt okuma)
    python -I tools\ram\ram_kalkan_v2.py durum
    python -I tools\ram\mcp_olcum.py
    python -I tools\ram\desktop_havuz.py plan

## 3. Kalkanı v2'ye geçir (Claude)
v1 (tmp\ram_kalkan_0911.py) canlıysa sürecini sonlandır; v1'i argümansız ÇALIŞTIRMA (hepsini birden açar). Sonra:
    python -I tools\ram\ram_kalkan_v2.py ac       # askıdakileri birer birer, RAM < %84 iken açar
    python -I tools\ram\ram_kalkan_v2.py baslat   # tek kopya; borsa %85'te ilk durur, en son açılır

## 4. Desktop MCP kopyalarını havuza bağla (Claude yazar, Ömer Desktop'u yeniden açar)
    python -I tools\ram\desktop_havuz.py uygula
Araç kaybı yok: havuzun sunmadığı ya da 0 araç verdiği girdiye dokunulmaz. Geri alma:
    python -I tools\ram\desktop_havuz.py geri

## 5. İşlere devam (Claude)
- kaynak_bul_0911: çalışmıyorsa `--arka` (kaldığı kalemden devam eder).
- kurulum-buyuk v4: is_sirasi durumuna bak; kurulum_d2 tek kopya mı.
- Bu turun yeni YANLIS-ESLESME kalemleri için 2. kaynak_bul turu.
- npm EBUSY HATA'ları TUR2'de (kalem başına --prefix) yeniden denenir.

## 6. Ömer (yönetici PowerShell)
    Stop-ScheduledTask -TaskPath "\Microsoft\Windows\Defrag\" -TaskName "ScheduledDefrag"
    Disable-ScheduledTask -TaskPath "\Microsoft\Windows\Defrag\" -TaskName "ScheduledDefrag"
    Stop-Service defragsvc -Force
Chrome Uzak Masaüstü: remotedesktop.google.com/access → "Uzaktan erişimi ayarla" → indir/kur → bilgisayar adı + 6+ haneli PIN →
telefona "Chrome Remote Desktop" uygulaması, aynı Google hesabı. Böyle bir donmada telefondan Desktop yeniden başlatılabilir.

## 7. Disk C %94
Yer açmadan önce ölç: `python -I tools\ram\disk_bak.py` yok; Claude o an WinDirStat yerine Python ile en büyük 30 klasörü listeler,
silme yok — taşınabilecekler (.kos/karantina, eski klonlar, npm/uv önbellekleri) Ömer'e onaya sunulur.
