# M4b — gürültü + kare-luna ölçümü

Ölçütler (yüksek ≥%90 · genel ≥%75 · dayanmayan ≤%5) ve altın set değişmedi. Dört sonnet koşusu aynı eşleme (det + Jev K2/K3) ve görsel yargıçla ölçüldü.
Koşu-2: aynı motor, aynı paket; m3b-2 7a550e3 worktree'sinde. Gürültü = |koşu-1 − koşu-2|; ortalama iki koşunun havuzu, ± yarı fark.

## Koşular
| koşu | yüksek | genel | dayanmayan | okunamıyor | ölçülemedi | düşen video | motor kalem | çağrı | $ | jeton |
|---|---|---|---|---|---|---|---|---|---|---|
| m3b-1 | %90 (71/79) | %81 (130/160) | %4 (5/127) | 0 | 0 | 0 | 127 | 8 | 0.860 | 174039 |
| m3b-2 | %89 (70/79) | %76 (122/160) | %5 (7/129) | 0 | 0 | 0 | 129 | 9 | 0.817 | 154433 |
| m4-1 | %88 (51/58) | %77 (96/125) | %4 (4/108) | 0 | 0 | 1 | 108 | 11 | 1.116 | 214670 |
| m4-2 | %90 (52/58) | %74 (92/125) | %9 (10/106) | 0 | 0 | 1 | 106 | 11 | 1.197 | 254831 |
| m3b+kare-luna | %87 (69/79) | %82 (131/160) | %23 (56/248) | 0 | 0 | 0 | 248 | 24 | 1.085 | 174039 |

## Tavanlar (koşu-2 = koşu-1 gerçek ×1,2)
- k1-sonnet: {"onceki": {"cagri": 5, "usd": 0.7}, "harcanan": [5, 0.5942], "ek": [3, 0.2142], "hedef_usd": 0.32}
- m3b2: {"gruplar": [[1, 0.0474], [7, 0.7966], [2, 0.1875]], "toplam": [10, 1.0315], "kaynak": "M3b-1 (onar dahil) ×1,2", "motor": "7a550e3"}
- k1-luna: {"onceki": {"cagri": 5, "usd": 0.055}, "harcanan": [4, 0.0417], "ek": [2, 0.0167], "hedef_usd": 0.03}
- m42: {"gruplar": [[1, 0.0495], [9, 0.9752], [4, 0.3149]], "toplam": [14, 1.3396], "kaynak": "M4-1 (K1 dahil) ×1,2"}
- m3b2-L9c-yeniden: {"ek": [1, 0.12], "neden": "hata (ilk çağrı), Σ 10/1.0315 içinde"}
- kare-luna: luna 11 çağrı $0.0417 (tavan (20, 0.15)) · görsel yargıç 5 çağrı $0.184 (tavan (5, 0.2))

## Gürültü ve ortalamalar (ölçütlere ortalama ile)
| motor | metrik | koşu-1 | koşu-2 | fark (puan) | ortalama ± gürültü | ölçüt |
|---|---|---|---|---|---|---|
| m3b | yüksek | %90 (71/79) | %89 (70/79) | 1.3 | %89.2 ± 0.6 | KALDI |
| m3b | genel | %81 (130/160) | %76 (122/160) | 5.0 | %78.8 ± 2.5 | GEÇTİ |
| m3b | dayanmayan | %4 (5/127) | %5 (7/129) | 1.5 | %4.7 ± 0.7 | GEÇTİ |
| m4 | yüksek | %88 (51/58) | %90 (52/58) | 1.7 | %88.8 ± 0.9 | KALDI |
| m4 | genel | %77 (96/125) | %74 (92/125) | 3.2 | %75.2 ± 1.6 | GEÇTİ |
| m4 | dayanmayan | %4 (4/108) | %9 (10/106) | 5.7 | %6.5 ± 2.9 | KALDI |

## Ortak videolar (4: L9c49WVG_ho, kHtOSJRUkLs, g89FJiNAlEs, JfmAm3sxCSc) — eşit kıyas
| koşu | yüksek | genel |
|---|---|---|
| m3b-1 | %86 (50/58) | %79 (99/125) |
| m3b-2 | %88 (51/58) | %76 (95/125) |
| m4-1 | %88 (51/58) | %77 (96/125) |
| m4-2 | %90 (52/58) | %74 (92/125) |
| m3b+kare-luna | %83 (48/58) | %80 (100/125) |

## Kategori (genel yakalama)
| kategori | m3b-1 | m3b-2 | m4-1 | m4-2 | m3b fark | m4 fark | m4−m3b ort (puan) | kare-luna |
|---|---|---|---|---|---|---|---|---|
| Araç/servis/ürün | %91 (31/34) | %82 (28/34) | %84 (21/25) | %76 (19/25) | 9 | 8 | -7 | %94 (32/34) |
| Açıklama bağlantıları | %100 (11/11) | %100 (11/11) | %100 (9/9) | %100 (9/9) | 0 | 0 | +0 | %100 (11/11) |
| Kareden bilgi | %53 (17/32) | %56 (18/32) | %50 (13/26) | %58 (15/26) | 3 | 8 | -1 | %59 (19/32) |
| Kural/ipucu/iş akışı | %86 (19/22) | %73 (16/22) | %62 (10/16) | %62 (10/16) | 14 | 0 | -17 | %68 (15/22) |
| Kurulum/komutlar | %83 (15/18) | %83 (15/18) | %89 (16/18) | %83 (15/18) | 0 | 6 | +3 | %89 (16/18) |
| Promptlar | %100 (6/6) | %67 (4/6) | %100 (3/3) | %100 (3/3) | 33 | 0 | +17 | %100 (6/6) |
| Teknikler | %84 (31/37) | %81 (30/37) | %86 (24/28) | %75 (21/28) | 3 | 11 | -2 | %86 (32/37) |

## Kategori × önem (iki koşu havuzu)
| kategori | önem | m3b | m4 | m3b+kare-luna |
|---|---|---|---|---|
| Araç/servis/ürün | yüksek | %94 (32/34) | %81 (21/26) | %94 (16/17) |
| Araç/servis/ürün | orta | %85 (22/26) | %78 (14/18) | %100 (13/13) |
| Araç/servis/ürün | düşük | %62 (5/8) | %83 (5/6) | %75 (3/4) |
| Açıklama bağlantıları | yüksek | %100 (14/14) | %100 (12/12) | %100 (7/7) |
| Açıklama bağlantıları | orta | %100 (6/6) | %100 (4/4) | %100 (3/3) |
| Açıklama bağlantıları | düşük | %100 (2/2) | %100 (2/2) | %100 (1/1) |
| Kareden bilgi | yüksek | %60 (6/10) | %75 (6/8) | %40 (2/5) |
| Kareden bilgi | orta | %50 (18/36) | %40 (12/30) | %67 (12/18) |
| Kareden bilgi | düşük | %61 (11/18) | %71 (10/14) | %56 (5/9) |
| Kural/ipucu/iş akışı | yüksek | %89 (16/18) | %70 (7/10) | %78 (7/9) |
| Kural/ipucu/iş akışı | orta | %68 (15/22) | %61 (11/18) | %55 (6/11) |
| Kural/ipucu/iş akışı | düşük | %100 (4/4) | %50 (2/4) | %100 (2/2) |
| Kurulum/komutlar | yüksek | %90 (18/20) | %100 (20/20) | %90 (9/10) |
| Kurulum/komutlar | orta | %67 (8/12) | %58 (7/12) | %83 (5/6) |
| Kurulum/komutlar | düşük | %100 (4/4) | %100 (4/4) | %100 (2/2) |
| Promptlar | yüksek | %83 (10/12) | %100 (6/6) | %100 (6/6) |
| Teknikler | yüksek | %90 (45/50) | %91 (31/34) | %88 (22/25) |
| Teknikler | orta | %67 (16/24) | %64 (14/22) | %83 (10/12) |

## Video (genel)
| video | m3b-1 | m3b-2 | m4-1 | m4-2 | m3b+kare-luna |
|---|---|---|---|---|---|
| L9c49WVG_ho | %77 (10/13) | %77 (10/13) | %77 (10/13) | %92 (12/13) | %85 (11/13) |
| kHtOSJRUkLs | %85 (34/40) | %78 (31/40) | %78 (31/40) | %82 (33/40) | %82 (33/40) |
| g89FJiNAlEs | %89 (25/28) | %82 (23/28) | %86 (24/28) | %71 (20/28) | %82 (23/28) |
| 86HM0RUWhCk | %89 (31/35) | %77 (27/35) | %0 (0/0) | %0 (0/0) | %89 (31/35) |
| JfmAm3sxCSc | %68 (30/44) | %70 (31/44) | %70 (31/44) | %61 (27/44) | %75 (33/44) |

## Kaçırma sebepleri (yüksek/orta)
| sebep | m3b-1 | m3b-2 | m4-1 | m4-2 | m3b+kare-luna |
|---|---|---|---|---|---|
| (a) | 10 | 13 | 12 | 13 | 8 |
| (b) | 3 | 3 | 2 | 3 | 2 |
| (c) | 12 | 17 | 11 | 14 | 14 |
| (d) | 0 | 0 | 0 | 0 | 0 |

## K4 — m3b+kare-luna (sonnet-m3b koşu-1 + luna kare okuma)
- eklenen kalem 121: {'eşleşti': 29, 'dayanıyor': 47, 'dayanmıyor': 45, 'okunamıyor': 0, 'kare-doğrulanamadı': 0, 'ölçülemedi': 0}
- altın isabet: +12 yeni yakalanan · −11 (eşleme gürültüsüyle kaybolan) · yüksek %90 (71/79) → %87 (69/79) · genel %81 (130/160) → %82 (131/160) · dayanmayan %4 (5/127) → %23 (56/248)
- ek maliyet: luna $0.0417 + görsel yargıç $0.184 (sonnet-m3b koşu-1 $0.860 üstüne %26)

## Kural 21 takası (iki koşu ortalaması)
- m4 / m3b: çağrı 8.5 → 11.0 · $ 0.838 → 1.157 (%+38) · jeton 164236 → 234750 (%+43) · genel -3.5 puan (gürültü m3b ±2.5, m4 ±1.6)

## M4 özellik önerileri

**Karar kuralı.** m4 ile m3b ortalaması arasındaki fark koşudan koşuya değişimden büyük değilse öneri BELİRSİZ.

**Bu turda en önemli bulgu: 86HM0RUWhCk M4 motorunda taranamıyor.** Bu bir tavan sorunu değil, motor kusuru. Sonnet üç denemenin üçünde de aynı form_red hatasını verdi (m4-1, K1 devamı, m4-2): `adaylar[i].karede_gorulen: kare gönderildi, karede görülen boş olamaz`. Luna'nın hatası farklı: `kanit_zamani eksik`. Tavanlar yetti (m4-2'de 11 çağrı / $1,197, tavan 14 / $1,34). Bu yüzden m4 iki koşuda da 4 videoyla ölçüldü. Eşit kıyas "Ortak videolar" tablosunda:

| | m3b | m4 | Fark |
|---|---|---|---|
| Yüksek önem | %87,1 | %89,2 | +2,1 puan |
| Genel | %77,6 | %75,2 | −2,4 puan |

İkisi de gürültü içinde; gürültü m3b'de ±2,5, m4'te ±1,6 puan.

- **K1 (Kurulum/komutlar) — BELİRSİZ.**
  - Kategori ortalaması m3b %83, m4 %86 (+3 puan). m4'ün kendi koşu farkı 6 puan, yani artış gürültü içinde.
  - Maliyeti yok denecek kadar az (akil.birlestir'de komutlar). Geri almak için de gerekçe yok.
- **K2 (tam altyazı + sahne/eşit aralık kare) — GERİ AL.**
  - Kural 21 takası: $ %+38, jeton %+43.
  - Buna karşılık kazanç yok:
    - (a) kaynak motora gitmedi sayısı düşmedi: m3b 10/13, m4 12/13, m4'te bir video eksikken.
    - Kareden bilgi değişmedi: m3b %53/%56, m4 %50/%58.
    - Ortak videolarda genel −2,4 puan.
- **K3 (kare başına zorunlu kayıt + oz_denetim) — GERİ AL, ya da doğrulayıcı dilim yolunda gevşetilsin.**
  - Dayanmayan m3b'de %4,7 ± 0,7, m4'te %6,5 ± 2,9. m4 ortalamada ≤%5 ölçütünü KALDI.
  - Kareden bilgi kazancı yok.
  - 86HM'nin sistematik form_red hatası bu doğrulayıcıdan çıkıyor.
- **K4 (bölme) — BELİRSİZ.**
  - 86HM'nin tek yararlanıcısı, ama K3 doğrulayıcısı yüzünden hiç tamamlanmadı; K4'ün katkısı ölçülemedi.
  - Dilim çağrıları maliyeti artırıyor.
  - K3 geri alındıktan sonra yalnız 86HM ile yeniden ölçülmeli.

**K4 kare-luna ekinin sonucu: ALMA.**
- Genel %81'den %82'ye çıktı (+1 puan, gürültü içinde; +12 yeni isabet, −11 kayıp). Yüksek önem %90'dan %87'ye düştü.
- Dayanmayan %4'ten %23'e çıktı: eklenen 121 kalemin 45'i görsel yargıçta dayanmıyor. Ek, uydurmayı artırıyor.
- Maliyeti düşük: luna $0,042 ve görsel yargıç $0,19.

**Ölçütler, ortalamayla:**

| Motor | Yüksek önem (≥%90) | Genel (≥%75) | Dayanmayan (≤%5) |
|---|---|---|---|
| m3b | %89,2 ± 0,6 · KALDI | %78,8 ± 2,5 · GEÇTİ | %4,7 ± 0,7 · GEÇTİ |
| m4 (4 video) | %88,8 ± 0,9 · KALDI | %75,2 ± 1,6 · GEÇTİ, sınırda | %6,5 ± 2,9 · KALDI |
