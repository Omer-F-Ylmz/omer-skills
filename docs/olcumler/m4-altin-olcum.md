# M4 — altın set ölçümü (M3c: M4 motoru, M3b ile yan yana)

Ölçütler ve altın set M3b ile aynı. Dayanmayan = K3 'dayanmıyor' + görsel yargıcın 'hayır' dediği kare kalemleri; 'okunamıyor' ayrı sayılır (K5b).
M3b satırları aynı görsel yargıçla yeniden hesaplandı (m3b-altin-olcum.md'deki alt/üst sınır yerine tek değer).

| kol | yüksek-önem | genel | dayanmayan | okunamıyor | ölçülemedi | motor kalem | hafif çağrı | girdi jeton | çıktı jeton | $ |
|---|---|---|---|---|---|---|---|---|---|---|
| sonnet (M3b) | %90 (71/79) | %81 (130/160) | %4 (5/127) | 0 | 0 | 127 | 8 | 127724 | 46315 | 0.8596 |
| luna (M3b) | %82 (65/79) | %72 (116/160) | %4 (6/139) | 0 | 0 | 139 | 6 | 182860 | 56964 | 0.0425 |
| qwen (M3b) | %96 (24/25) | %77 (37/48) | %3 (1/32) | 0 | 0 | 32 | 6 | 54411 | 70563 | 0.0000 |
| sonnet-m4 | %88 (51/58) | %77 (96/125) | %4 (4/108) | 0 | 0 | 108 | 11 | 150220 | 64450 | 1.1163 |
| luna-m4 | %84 (49/58) | %74 (93/125) | %5 (7/139) | 0 | 1 | 139 | 9 | 292753 | 119314 | 0.0828 |
| karma-m4 | %86 (50/58) | %75 (94/125) | %5 (7/136) | 0 | 1 | 136 | 10 | 224690 | 95669 | 0.5276 |

## Ölçütler (sonnet-m4 = M4 motoru)
- yüksek-önem ≥%90: KALDI (%88 (51/58)) · M3b %90 (71/79)
- tüm kalemler ≥%75: GEÇTİ (%77 (96/125)) · M3b %81 (130/160)
- dayanmayan ≤%5: GEÇTİ (%4 (4/108); okunamıyor 0) · M3b %4 (5/127) (okunamıyor 0)
- sonuç: motor mükemmel DEĞİL

## Kategori yakalama (sonnet)
| kategori | M3b | M4 |
|---|---|---|
| Araç/servis/ürün | %91 (31/34) | %84 (21/25) |
| Açıklama bağlantıları | %100 (11/11) | %100 (9/9) |
| Kareden bilgi | %53 (17/32) | %50 (13/26) |
| Kural/ipucu/iş akışı | %86 (19/22) | %62 (10/16) |
| Kurulum/komutlar | %83 (15/18) | %89 (16/18) |
| Promptlar | %100 (6/6) | %100 (3/3) |
| Teknikler | %84 (31/37) | %86 (24/28) |

## Kategori × önem (sonnet)
| kategori | önem | M3b | M4 |
|---|---|---|---|
| Araç/servis/ürün | düşük | %75 (3/4) | %100 (3/3) |
| Araç/servis/ürün | orta | %92 (12/13) | %78 (7/9) |
| Araç/servis/ürün | yüksek | %94 (16/17) | %85 (11/13) |
| Açıklama bağlantıları | düşük | %100 (1/1) | %100 (1/1) |
| Açıklama bağlantıları | orta | %100 (3/3) | %100 (2/2) |
| Açıklama bağlantıları | yüksek | %100 (7/7) | %100 (6/6) |
| Kareden bilgi | düşük | %56 (5/9) | %57 (4/7) |
| Kareden bilgi | orta | %50 (9/18) | %47 (7/15) |
| Kareden bilgi | yüksek | %60 (3/5) | %50 (2/4) |
| Kural/ipucu/iş akışı | düşük | %100 (2/2) | %50 (1/2) |
| Kural/ipucu/iş akışı | orta | %82 (9/11) | %67 (6/9) |
| Kural/ipucu/iş akışı | yüksek | %89 (8/9) | %60 (3/5) |
| Kurulum/komutlar | düşük | %100 (2/2) | %100 (2/2) |
| Kurulum/komutlar | orta | %67 (4/6) | %67 (4/6) |
| Kurulum/komutlar | yüksek | %90 (9/10) | %100 (10/10) |
| Promptlar | yüksek | %100 (6/6) | %100 (3/3) |
| Teknikler | orta | %75 (9/12) | %73 (8/11) |
| Teknikler | yüksek | %88 (22/25) | %94 (16/17) |

## Video yakalama (genel)
| video | sonnet (M3b) | luna (M3b) | qwen (M3b) | sonnet-m4 | luna-m4 | karma-m4 |
|---|---|---|---|---|---|---|
| L9c49WVG_ho | %77 (10/13) | %69 (9/13) | %54 (7/13) | %77 (10/13) | %85 (11/13) | %85 (11/13) |
| kHtOSJRUkLs | %85 (34/40) | %85 (34/40) | — | %78 (31/40) | %78 (31/40) | %78 (31/40) |
| g89FJiNAlEs | %89 (25/28) | %75 (21/28) | — | %86 (24/28) | %75 (21/28) | %75 (21/28) |
| 86HM0RUWhCk | %89 (31/35) | %80 (28/35) | %86 (30/35) | — | — | — |
| JfmAm3sxCSc | %68 (30/44) | %55 (24/44) | — | %70 (31/44) | %68 (30/44) | %70 (31/44) |

## Kaçırma sebepleri (yüksek/orta, sonnet)
| sebep | M3b | M4 |
|---|---|---|
| (a) kaynak motora gitmedi | 10 | 12 |
| (b) formda alan/kategori yok | 3 | 2 |
| (c) model atladı | 12 | 11 |

## Maliyet / jeton (K6: kural 21 kendi değişikliğimize)
- sonnet girdi jetonu M3b 127724 → M4 150220 (%+18; K2 tam altyazı + yoğun kare 1568 px + K3 form alanları + K4 dilim çağrıları) · çıktı %+39 · çağrı 8 → 11 · $ 0.8596 → 1.1163 (%+30)
- görsel yargıç (ayrı satır, sonnet tavanına dahil değil): 8 hafif çağrı · $0.1077 · tavan 12 / $0.4

## Kural 21 takası (kur.takas)
| kol | taban | yakalama düşüşü | tasarruf | ölçütler | karar |
|---|---|---|---|---|---|
| sonnet-m4 | sonnet (M3b) | %20 | %-30 | KALDI | RED(takas) — düşüş %15–20 & tasarruf <%50 |
| luna-m4 | sonnet-m4 | %20 | %93 | KALDI | AL — düşüş %15–20 & tasarruf ≥%75 |
| karma-m4 | sonnet-m4 | %20 | %53 | KALDI | SOR — düşüş %15–20 & tasarruf %50–75 |

Tarama (M4): sonnet-0 m4-sonnet-short {'L9c49WVG_ho': 'tamam'} · sonnet-1 m4-sonnet-uzun {'kHtOSJRUkLs': 'tamam', 'g89FJiNAlEs': 'tamam_eksik', '86HM0RUWhCk': 'form_red'} · sonnet-2 m4-sonnet-uzun-2 {'JfmAm3sxCSc': 'tamam_eksik'} · luna-0 m4-luna-short {'L9c49WVG_ho': 'tamam'} · luna-1 m4-luna-uzun {'kHtOSJRUkLs': 'tamam', 'g89FJiNAlEs': 'tamam', '86HM0RUWhCk': 'form_red'} · luna-2 m4-luna-uzun-2 {'JfmAm3sxCSc': 'tamam'}
karma-m4 bileşik: 86HM0RUWhCk, JfmAm3sxCSc sonnet-m4, diğerleri luna-m4 raporu (ek çağrı yok; tek örnek, yeniden koşu değil).
