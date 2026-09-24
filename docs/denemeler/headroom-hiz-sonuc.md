# Deneme sonucu: headroom-hiz

2026-09-24 · sonnet · 4 görev (gorevler-okuma) · 2 kol × 2 koşu, karışık sıra · claude -p 16 · Jev istek 16 · hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet $6.0203 (bu koşuda yeni çağrı 8)
Kollar: headroom-mevcut (temel): env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 ; headroom-hiz: env ANTHROPIC_BASE_URL=http://127.0.0.1:8794 · gürültü (temel 1-2 kalite farkı ort.) 0.08

## Kol ortalamaları
Karar sıcak (2. koşu) maliyetiyle; soğuk (1. koşu) bilgi.

| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | soğuk $ | sıcak $ |
|---|---|---|---|---|---|---|---|
| headroom-mevcut | 0.75 | 2.68 | 352 | 233488 | 15.8 | 0.3799 | 0.2840 |
| headroom-hiz | 0.75 | 2.71 | 446 | 310816 | 17.6 | 0.4571 | 0.3841 |

## Görev başına
| görev | kol | başarı 1/2 | kalite 1/2 | çıktı 1/2 | girdi 1/2 |
|---|---|---|---|---|---|
| 1-basarisiz-test | headroom-mevcut | 1/1 | 2.90/2.75 | 458/430 | 290848/292153 |
| 1-basarisiz-test | headroom-hiz | 1/1 | 2.82/2.86 | 270/490 | 216606/290910 |
| 2-json-alan | headroom-mevcut | 1/1 | 2.45/2.43 | 355/335 | 290355/192850 |
| 2-json-alan | headroom-hiz | 1/1 | 2.31/2.47 | 719/594 | 571006/389274 |
| 3-hatali-diff | headroom-mevcut | 1/1 | 2.62/2.71 | 246/185 | 208268/207551 |
| 3-hatali-diff | headroom-hiz | 1/1 | 2.77/2.77 | 207/229 | 208438/208438 |
| 4-log-zincir | headroom-mevcut | 0/0 | 2.74/2.81 | 396/411 | 192871/193011 |
| 4-log-zincir | headroom-hiz | 0/0 | 2.84/2.82 | 573/489 | 310446/291410 |

## Karar
RED(token): çıktı −%-26.8 (eşik %-) · kalite 2.68→2.71 (bant 0.10) · başarısı düşen görev: yok · girdi −%-33.1 (eşik %0)
headroom-hiz: RED(token): çıktı −%-26.8 (eşik %-) · kalite 2.68→2.71 (bant 0.10) · başarısı düşen görev: yok · girdi −%-33.1 (eşik %0)
