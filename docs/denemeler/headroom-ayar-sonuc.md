# Deneme sonucu: headroom-ayar

2026-09-24 · sonnet · 4 görev (gorevler-okuma) · 3 kol × 2 koşu, karışık sıra · claude -p 24 · Jev istek 24 · hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet $8.7909 (bu koşuda yeni çağrı 24)
Kollar: dogrudan (temel): env ANTHROPIC_BASE_URL=https://api.anthropic.com ; headroom-mevcut: env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 ; headroom-wrap: env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 ENABLE_TOOL_SEARCH=true · gürültü (temel 1-2 kalite farkı ort.) 0.34

## Kol ortalamaları
Karar sıcak (2. koşu) maliyetiyle; soğuk (1. koşu) bilgi.

| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | soğuk $ | sıcak $ |
|---|---|---|---|---|---|---|---|
| dogrudan | 0.88 | 2.50 | 582 | 375977 | 18.3 | 0.4004 | 0.4153 |
| headroom-mevcut | 1.00 | 2.62 | 358 | 235328 | 16.5 | 0.3715 | 0.3543 |
| headroom-wrap | 0.88 | 2.62 | 321 | 225586 | 15.5 | 0.3602 | 0.2959 |

## Görev başına
| görev | kol | başarı 1/2 | kalite 1/2 | çıktı 1/2 | girdi 1/2 |
|---|---|---|---|---|---|
| 1-basarisiz-test | dogrudan | 1/1 | 2.68/2.85 | 285/287 | 213715/216962 |
| 1-basarisiz-test | headroom-mevcut | 1/1 | 2.55/2.83 | 296/256 | 192475/196243 |
| 1-basarisiz-test | headroom-wrap | 1/1 | 2.82/2.88 | 282/242 | 193392/219880 |
| 2-json-alan | dogrudan | 1/1 | 2.51/2.56 | 1153/1037 | 669059/769204 |
| 2-json-alan | headroom-mevcut | 1/1 | 2.50/2.44 | 713/319 | 495652/193394 |
| 2-json-alan | headroom-wrap | 1/1 | 2.37/2.44 | 249/296 | 196240/193371 |
| 3-hatali-diff | dogrudan | 1/1 | 1.41/2.46 | 592/213 | 232350/232343 |
| 3-hatali-diff | headroom-mevcut | 1/1 | 2.61/2.72 | 272/266 | 209012/208800 |
| 3-hatali-diff | headroom-wrap | 1/1 | 2.76/2.53 | 233/282 | 208800/208778 |
| 4-log-zincir | dogrudan | 1/0 | 2.79/2.70 | 528/564 | 327479/346702 |
| 4-log-zincir | headroom-mevcut | 1/1 | 2.61/2.69 | 389/353 | 193623/193429 |
| 4-log-zincir | headroom-wrap | 0/1 | 2.60/2.55 | 470/517 | 292010/292214 |

## Karar
KUR önerisi → ONAY [headroom-mevcut]: çıktı −%38.5 (eşik %-) · kalite 2.50→2.62 (bant 0.34) · başarısı düşen görev: yok · girdi −%37.4 (eşik %5)
headroom-mevcut: KUR önerisi → ONAY: çıktı −%38.5 (eşik %-) · kalite 2.50→2.62 (bant 0.34) · başarısı düşen görev: yok · girdi −%37.4 (eşik %5)
headroom-wrap: KUR önerisi → ONAY: çıktı −%44.8 (eşik %-) · kalite 2.50→2.62 (bant 0.34) · başarısı düşen görev: yok · girdi −%40.0 (eşik %5)
