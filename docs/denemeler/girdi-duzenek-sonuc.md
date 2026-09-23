# Deneme sonucu: girdi-duzenek

2026-09-24 · sonnet · 1 görev (gorevler-okuma) · 2 kol × 2 koşu, karışık sıra · claude -p 4 · Jev istek 4 · hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet $1.7334 (bu koşuda yeni çağrı 4)
Kollar: dogrudan (temel): env ANTHROPIC_BASE_URL=https://api.anthropic.com ; headroom: env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 · gürültü (temel 1-2 kalite farkı ort.) 0.21

## Kol ortalamaları
Karar sıcak (2. koşu) maliyetiyle; soğuk (1. koşu) bilgi.

| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | soğuk $ | sıcak $ |
|---|---|---|---|---|---|---|---|
| dogrudan | 0.50 | 2.73 | 530 | 270106 | 12.2 | 0.4874 | 0.3530 |
| headroom | 0.50 | 2.50 | 542 | 348414 | 38.5 | 0.4797 | 0.4133 |

## Görev başına
| görev | kol | başarı 1/2 | kalite 1/2 | çıktı 1/2 | girdi 1/2 |
|---|---|---|---|---|---|
| 4-log-zincir | dogrudan | 1/0 | 2.84/2.63 | 497/562 | 323544/216669 |
| 4-log-zincir | headroom | 0/1 | 2.46/2.54 | 349/736 | 209892/486937 |

## Karar
RED(token, kalite): çıktı −%-2.5 (eşik %-) · kalite 2.73→2.50 (bant 0.21) · başarısı düşen görev: yok · girdi −%-29.0 (eşik %5)
headroom: RED(token, kalite): çıktı −%-2.5 (eşik %-) · kalite 2.73→2.50 (bant 0.21) · başarısı düşen görev: yok · girdi −%-29.0 (eşik %5)
