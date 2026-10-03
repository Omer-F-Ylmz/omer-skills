# DERİNLİK-1 — araştırma kapsamı (2026-10-04)
KARAR: R2→R3→R5→R6→R1→R4; her R: kırmızı test commit → kod commit. Tavan 40 çağrı, 35'te commit+push+DUR.
Değişiklik yalnız tools/video (kod+test) ve docs/. claude -p 0. ~/.claude yalnız OKUNUR (R1).
Kabul: kırmızı-önce ayrı commit · R2 mutasyonu (servis atlaması geri → kırmızı → geri al) · eski test değişmez (çelişirse DUR) · tam suit (suite-kosucu) · gitleaks · arşiv · push · graphify update .
R1: gh yok/başarısız → kapsam "güncellik bakılamadı (sebep)", sessiz dönüş yok.
R4: yorum başarısız → kapsam "yorum alınamadı (sebep)".
DURUM: R2 ✓ · R3 ✓ · R5 ✓ (ayrı ## Kapsam, Ömer kararı) · R6 ✓ · R1 ✓ · altı suit yeşil (video 532) · 2. dalga 31 çağrı
SON dalga: R4 ✓ (kare ipucu 3→8 · yorum bağlantıları + Kapsam yorum; f07c23a→89395a5) · R1b ✓ (0fe72b7→6d7fd11) · gitleaks temiz · push
SUİT BEKLİYOR: Kendi oyun modlarim'de koşu var (bash + tail -f, 2026-10-04 01:16); RAM 8.8 GB ok
KALAN: R4b ÇELİŞKİ → Ömer kararı: test_m2d::test_devam_yeniden_tara alt'ı pytest.fail ile yasaklıyor; paket yeniden kurulumu bu eski testi kırar
  seçenek: (a) testi güncelle izni · (b) ayrı bayrak --paket-yeniden · KALAN: R4 prompt metni (tür=prompt aday.md "## Prompt metni", tarama satırı s[4]; yoksa "metin alınamadı") · tam suit · arşiv
NOT R4: Kapsam'da yorum alanı hazır: d["videolar"][v]["yorum"] doldurulunca görünür (şimdi "bakılmadı")
NOT R1: fark + önceki aday.md varsa araştırma yok (aday.md ezilmesin); panel yine UYARLA/güncelle
NOT R5: ana tabloya 9. sütun eski testlerin 8-sütun ayrıştırıcısını (test_m2c._panel, panel_uygula) bozar → ayrı "## Kapsam" bölümü önerilir (Ömer onayı)
NOT R6: parti.py:519 --yeniden yalnız gelistir+panel; R6'da durum/repo_arama sıfırlanıp araştırma yeniden koşulacak
