# Devir — 28 Eki 2026 06:00 (TR)

## Zorunlu kural (Ömer, tekrar)
Claude + bütün ajanlar CC'yi Ömer gibi kullanır: iş başına TEK kalıcı oturum, iş bloklar halinde aynı oturuma (--resume), gereksiz yeni oturum yok; bağlam ~120k'yı geçince ya da oturum kirlenince (sarkık tool_use) taze oturum + devir brief'i.
- tools/arka_ajan.py (28 Eki 06:00): her iş .kos/kopru/arka/<isim>.oturum'a session_id yazar; sonraki tur temiz bittiyse ve girdi <120k ise otomatik --resume. Taze oturum için json'a "yeni_oturum": true.
- Uzun ajanlar köprüden DEĞİL Görev Zamanlayıcı ile: .kos/kopru/arka/<isim>.json → komut aracıyla `python C:/Projeler/omer-skills/tools/arka_ajan.py baslat <isim>` (Ömer 28 Eki 00:44 onayı; köprü 60 sn'de cc-kopru'yu yeniden başlatıp çocukları öldürüyordu). Kısa (<60 sn) işler köprüden. docs/cc-kullanim-kurali.md "ARKA-AJAN".
- Durum okuma: .kos/kopru/arka/<isim>.log (son satır "BITTI hh:mm kod"), <isim>.kilit (çalışıyor), <isim>-ilerleme.md, .kos/kopru/son-durum.md. Asılı eski kilitler: skill-mode.kilit, yaka-d2.kilit (iş bitti, süreç askıda; PC yeniden başlayınca temizlenir, yeni kilitler Popen düzeltmesiyle sorunsuz).

## Çalışan işler (05:40'ta başladı)
1. karar-14 — 14 ÖMER-KARARI işi, geri alınabilirlerin hepsine EVET (Ömer yetkisi). Soru kalırsa .kos/kopru/arka/karar-14-soru.md.
2. yarim-216 — KOŞMUŞ-BİTMEMİŞ 216 iş (rapor/yarim-tara-27eki.md).
3. hic-122 — HİÇ GİRMEMİŞ 122 iş.
4. video-kaynak — 178 video linki + 275 ek kaynak (araçlar kurulur, yöntemler uygulanır).
Her biri 60 turda "TUR BITTI" yazar → aynı adla yeniden baslat (oturum + ilerleme dosyasından sürer). 20-25 dk'da bir kontrol; RAM ≤%89 (yetim.log).

## İLİK (yaka-cicegi) — BİTTİ, yayın YOK (örnek/portföy sunumu)
C:\Users\pc\Desktop\Claude ile yapılanlar\yaka-cicegi\ · site commit 764b057 · kapanis.md (Lighthouse mobil 98/100/100/100, masaüstü 99/100/100/100; ZAP Docker kapalı → atlandı). İletişim/alan adı/KVKK veri sorumlusu yer tutucu KALIR (yayın yok).
- Bekleyen: 28 Eki 20:55 TR HF ZeroGPU kotası sıfırlanınca yaka-3d-4t.json (çok açılı doku + No.3 yeniden kırpma) → v3 GLB daha iyiyse YAKA-D1d (vitrin/hero ±20° kısıtı gevşer). Cila: Kur sahnesi prosedürel güller, vitrin kart hizası.
- Ders: tek önden projeksiyon doku yandan bozuk; TRELLIS/H3D-2.1 ZeroGPU günlük kota; NVIDIA hosted trellis yalnız example_id; 2mv PyMeshLab hatası.

## Diğer
- SKILL-MODE bitti: açılış 149k → ~126k (agents-lazy + ajan-getir; 171 skill geri açıldı).
- STRIX daha uzun timeout ile yeniden koşulacak.
- Desktop'ın cc-kopru şemasında yeni_oturum artık var.
