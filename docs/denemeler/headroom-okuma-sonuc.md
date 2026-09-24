# Deneme sonucu: headroom-okuma

2026-09-24 · sonnet · 4 görev (gorevler-okuma) · 2 kol × 2 koşu, karışık sıra · claude -p 16 · Jev istek 16 · hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet $5.4704 (bu koşuda yeni çağrı 16)
Kollar: headroom-mevcut (temel): env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 ; headroom-okuma: env ANTHROPIC_BASE_URL=http://127.0.0.1:8793 · gürültü (temel 1-2 kalite farkı ort.) 0.05

## Kol ortalamaları
Karar sıcak (2. koşu) maliyetiyle; soğuk (1. koşu) bilgi.

| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | soğuk $ | sıcak $ |
|---|---|---|---|---|---|---|---|
| headroom-mevcut | 0.75 | 2.69 | 352 | 233488 | 15.8 | 0.3799 | 0.2840 |
| headroom-okuma | 0.88 | 2.63 | 379 | 273124 | 18.7 | 0.3653 | 0.3384 |

## Görev başına
| görev | kol | başarı 1/2 | kalite 1/2 | çıktı 1/2 | girdi 1/2 |
|---|---|---|---|---|---|
| 1-basarisiz-test | headroom-mevcut | 1/1 | 2.89/2.82 | 458/430 | 290848/292153 |
| 1-basarisiz-test | headroom-okuma | 1/1 | 2.64/2.86 | 296/246 | 192769/216368 |
| 2-json-alan | headroom-mevcut | 1/1 | 2.45/2.45 | 355/335 | 290355/192850 |
| 2-json-alan | headroom-okuma | 1/1 | 2.46/2.48 | 248/708 | 192793/487117 |
| 3-hatali-diff | headroom-mevcut | 1/1 | 2.62/2.68 | 246/185 | 208268/207551 |
| 3-hatali-diff | headroom-okuma | 1/1 | 2.70/2.54 | 196/222 | 208292/208279 |
| 4-log-zincir | headroom-mevcut | 0/0 | 2.75/2.82 | 396/411 | 192871/193011 |
| 4-log-zincir | headroom-okuma | 1/0 | 2.73/2.64 | 457/661 | 290289/389085 |

## Karar
RED(token): çıktı −%-7.7 (eşik %-) · kalite 2.69→2.63 (bant 0.10) · başarısı düşen görev: yok · girdi −%-17.0 (eşik %10)
headroom-okuma: RED(token): çıktı −%-7.7 (eşik %-) · kalite 2.69→2.63 (bant 0.10) · başarısı düşen görev: yok · girdi −%-17.0 (eşik %10)
