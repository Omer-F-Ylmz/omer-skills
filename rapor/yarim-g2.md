# YARIM-G2 rapor (24 Eki), 35 iş, durum taraması + 1 kod düzeltmesi

Kanıt kaynağı: `.kos/kopru/ara/yarim-g2-scan.txt` (git log --grep, rapor/, ajan-sira result). Canlı yeniden doğrulama yapılmadı (yalnız beyin-fix-2 testi koşuldu).

- beyin-fix-2: BİTTİ, kök neden 1661e71d (dizgi `t` TypeError) + bu oturum: kocluk_oku Desktop `not` alanını okur; kırmızı→yeşil, tests/test_beyin_dusun.py 59 geçti.
- beyin-1: ZATEN BİTMİŞ, bcda7af9, rapor/beyin-1*.
- beyin-2: ZATEN BİTMİŞ (kapı <%92 geçmedi), bf138f65. ÖMER: kapı/token kararı Desktop'ta.
- beyin-3: ZATEN BİTMİŞ (kapı geçmedi), 491ea91c. ÖMER: aynı karar.
- beyin-4: ZATEN BİTMİŞ (doğruluk ≥%92, token hedefi tutmadı), 70c544e2. ÖMER: aynı karar; MAKARA-1 bu karara bağlı.
- code-mode-1: ZATEN BİTMİŞ, 259dc02c.
- her-adim-1: ZATEN BİTMİŞ, 31ca757e (+ tests/test_cagri_sayac.py).
- kanca-sayac-1: ZATEN BİTMİŞ, rapor/kanca-sayac-1.md BİTTİ; tools/cagri_sayac.py session_id başına sayaç repoda.
- dans-1: ZATEN BİTMİŞ, Desktop\dans\dans-5sn.mp4 (1080x1920, ajan-sira sonucu).
- sleep-1: ZATEN BİTMİŞ, d3 raporu `.kos/kopru/rapor/sleep-1-d3.md`.
- ogren-4: ZATEN BİTMİŞ, ÖMER: zip'leri claude.ai'ye yükle; Desktop tarafı doğrulanmadı.
- ogren-ortak: ZATEN BİTMİŞ (yöntem belgesi, işi yok), fc71d0bd.
- beyin-canli-1b: DEVAM, 46f5439c (tetikler) var, rapor yok; canlı olay sayımı doğrulanmadı (önce yonetici_yenile.py, ders #88).
- beyin-canli-1b-a2, beyin-fix-1, beyin-fix-1-a, code-mode-rea-1-a: DEVAM, rapor/commit kanıtı bulunamadı; gorev-yarim-g2-devam.md.
- hook-3: DEVAM, HOOK-3-devam-2 commit'i var, rapor yok.
- kalite-1: DEVAM, rapor/kalite-1.md; ÖMER: dist/kalite-1 zip'lerini yükle, sonra kosucu.py yeniden ölçüm (tavan $35, ayrı onay).
- kalite-2: DEVAM, d3 raporu var (azure telemetri hook bulguları uygulanmadı).
- kalite-3-d14, kalite-3-hiz: DEVAM, koşucu sürüyordu; devir/kalite-3-hiz-devam.md.
- makara-1, makara-plan: DEVAM, beyin-4 kapı kararına bağlı; ÖMER: `Omer-F-Ylmz/omer-makara` repo/çalıştırma onayı.
- ogren-0b: DEVAM, 15 ajan koşusu, "diğer" kalanı kapanmadı.
- ogrenme-2b: DEVAM, sınav aracı yazıldı, canlı sınav 429/zaman aşımı; havuz düzelmeden ölçüm yok.
- ogren-5, 7, 8, 9, 10, 11, 12, 13, 14: DEVAM, kuyruğa hiç girmedi; her biri ayrı kategori oturumu (ogren-ortak.md'yi uygular), bu oturumda yapılmadı (kapsam: tek oturum/$4 tavan).

Atlanan: Ömer BEKLEMEDE işleri (TELVE, logo, NEFFEX, Mai, REA Desktop uyarısı, 10 karar) bu listede yoktu; görülmedi.
Sapma: 35 işin tamamı bitirilmedi; 12 işte bitmişlik kanıtı, 1 işte kod düzeltmesi, 22 iş devir dosyasında.
