# Claude Fable 5 ile Gezilebilen 3D Müze Portfolyosu Yaptım!
kanal: Yıldız Dikme · süre: 18 dk · altyazı: otomatik tr
ana iddia: Claude Fable 5 ile hazırlatılan detaylı iki prompt (önce ön yüz, sonra backend) Abacus.AI SuperComputer'a verilerek gezilebilen, ziyaret analitikli 3D müze portfolyosu kurulabilir.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Abacus.AI SuperComputer | YENİ | ELENDİ | sponsor; bulutta Ubuntu sanal masaüstü ajanı (terminal, paket, çalıştırma, URL/domain, DB, şifreli /dashboard burada kuruldu); ücretli, işin çoğu Claude Code ile çift |
| Abacus.AI ChatLLM: RouteLLM | YENİ | ELENDİ | promptu hangi modelin yazacağını otomatik seçen yönlendirici; ücretli hesap, videoda kullanılmadı (Fable 5 elle seçildi) |
| pmndrs/react-three-fiber | YENİ | ELENDİ | three.js için React renderer, müzede kullanıldı; proje npm bağımlılığı, skill/plugin değil; frontend-craft "gereksiz kütüphane yok" |
| meta-prompt: paragraf brief'i Claude'a madde listesi prompta çevirtmek, fazlara bölmek | YENİ | ELENDİ | Claude Code'da brief doğrudan ajana gider; plan→eleştir→inşa zaten Bölüm 8 iki-pass ve Bölüm 1 sırası |
| 3D sahnede ışık tonu ve kontrol şemasını açık yazmak | YENİ | BİLGİ | "tatlı sarı ışık, soğuk değil"; E ile detay, ok tuşlarıyla hareket, zıplama kapalı; söylenmezse "düz küp oda" çizer (iddia, karşılaştırma gösterilmedi) |
| diğer: "kopyalama, yalnız atmosferi al" kuralı, 2. promptta "mevcut projeyi asla değiştirme" kısıtı | ZATEN VAR | ELENDİ | frontend-craft Bölüm 10 (referansı kopyalama) ve Bölüm 0 inspiration; CLAUDE.md cerrahi değişiklik |
## ölçütler (YENİ)
- Abacus.AI SuperComputer: bakım=bilinmiyor (kapalı SaaS) · çift=Claude Code (terminal, dosya, çalıştırma); barındırma/DB kısmında örtüşme yok · izin=ücretli hesap (aylık 10 $ iddiası), kredi tüketimi (20.000 kredinin ~13.000'i 3 denemede, sözlü iddia) · context=yok (harici web platformu) · kurulum: —
- Abacus.AI ChatLLM: RouteLLM: bakım=bilinmiyor · çift=örtüşme yok · izin=ücretli Abacus.AI hesabı · context=yok (harici web platformu) · kurulum: —
- pmndrs/react-three-fiber: bakım=pushed 2026-09-13, 32308 yıldız, arşiv değil · çift=örtüşme yok · izin=proje başına npm bağımlılığı (react, three) · context=yok (kütüphane) · kurulum: —
- meta-prompt: bakım=— (teknik) · çift=Bölüm 8 iki-pass (kısmi) · izin=yok · context=yok · kurulum: —
- 3D sahnede ışık tonu ve kontrol şeması: bakım=— (teknik) · çift=kısmi, Bölüm 11 künyesi "zemin kararı" (ışık/kontrol yok) · izin=yok · context=DESIGN.md'de proje başına 1-2 token · kurulum: —
## hedefler (BİLGİ)
- 3D/oyunlaştırılmış sahnede ışık tonu (ör. sıcak sarı) ve kontrol şeması (tuşlar, kapalı hareketler) token olarak yazılır → DESIGN.md şablonu (Token'lar)
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda; tam promptlar açıklamadaki Google Drive klasöründe (açıklama)
1. prompt: 3D web siteler yapan yazılımcıyım; SuperComputer ile 3D müze portfolyosu; gerçek müze atmosferi, tam olarak kopyalama, yalnız atmosferini yap; 6 proje/görsel (sözlü özet, birebir değil)
1. prompt devam: E'ye basınca proje detayı; sağ/sol ok tuşlarıyla hareket; zıplama çalışmamalı; premium portfolyo deneyimi; React + React Three Fiber; sıcak sarı ışık (sözlü özet, birebir değil)
2. prompt: mevcut projeyi asla değiştirme; /dashboard URL'inde şifreli panel; proje adıyla hangi projeye ne kadar bakıldığını database'e kaydet; kurulduğunu bildir (sözlü özet, birebir değil)
referans siteler: supercomputer.abacus.ai/yzd (sponsor), drive.google.com/drive/folders/1LnTm7glNSab3iPy3Y1sS06jivoGOf6ce (promptlar); tasarım referans sitesi anılmadı
stiller: adlandırılmış stil yok; yön ifadeleri: gerçek müze atmosferi, oyunlaştırılmış 3D portfolyo, premium portfolyo
premium kararlar:
1) Klasik sayfa yerine içinde gezilen oyunlaştırılmış 3D müze; "ödül alan sitelerde çok var", "herkes klasik sitelerden bıktı" (iddia, kanıt gösterilmedi)
2) Soğuk yerine tatlı sarı ışık ile gerçek müze havası
3) Promptta premium deneyim, teknoloji (React Three Fiber) ve etkileşim şemasını (zıplama kapalı) detaylı yazmak; "prompt detaylı olmasaydı iyi sonuç alamazdık" (iddia)
