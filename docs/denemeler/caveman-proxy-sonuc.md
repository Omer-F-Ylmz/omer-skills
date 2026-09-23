# Deneme sonucu: caveman-proxy

2026-09-24 · sonnet · 4 görev (gorevler-okuma) · 2 kol × 2 koşu, karışık sıra · claude -p 16 · Jev istek 16 · hook kapalı (JEV_SKILL_HOOK=0) · toplam maliyet $6.2579 (bu koşuda yeni çağrı 16)
Kollar: headroom (temel): env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 ; caveman-mcp: env ANTHROPIC_BASE_URL=http://127.0.0.1:8788 · mcp docs/denemeler/caveman-mcp.json · gürültü (temel 1-2 kalite farkı ort.) 0.29
mcp çağrı: headroom 0 · caveman-mcp 0

## Kol ortalamaları
Karar sıcak (2. koşu) maliyetiyle; soğuk (1. koşu) bilgi.

| kol | başarı | kalite 0-3 | çıktı | girdi | süre sn | soğuk $ | sıcak $ |
|---|---|---|---|---|---|---|---|
| headroom | 1.00 | 2.55 | 291 | 219880 | 15.5 | 0.3549 | 0.3542 |
| caveman-mcp | 0.88 | 2.65 | 414 | 351549 | 15.5 | 0.4259 | 0.4294 |

## Görev başına
| görev | kol | başarı 1/2 | kalite 1/2 | çıktı 1/2 | girdi 1/2 |
|---|---|---|---|---|---|
| 1-basarisiz-test | headroom | 1/1 | 2.79/2.68 | 244/251 | 190862/191141 |
| 1-basarisiz-test | caveman-mcp | 1/1 | 2.86/2.89 | 199/230 | 238368/238443 |
| 2-json-alan | headroom | 1/1 | 2.39/2.48 | 384/436 | 287710/288467 |
| 2-json-alan | caveman-mcp | 1/1 | 2.35/2.33 | 892/846 | 654780/655226 |
| 3-hatali-diff | headroom | 1/1 | 2.67/1.81 | 181/318 | 206966/207136 |
| 3-hatali-diff | caveman-mcp | 1/1 | 2.77/2.70 | 226/238 | 230742/230759 |
| 4-log-zincir | headroom | 1/1 | 2.84/2.72 | 229/283 | 195070/191689 |
| 4-log-zincir | caveman-mcp | 1/0 | 2.65/2.68 | 373/307 | 329086/234989 |

## Karar
KARAR YOK: sıkıştırma devreye girmedi (mcp çağrısı 0)
caveman-mcp: KARAR YOK: sıkıştırma devreye girmedi (mcp çağrısı 0)

## Neden (20b-devam)
- Proxy açılış satırı: "subscription and OAuth logins stay byte-identical pass-through here: local compression needs the caveman MCP retrieve tool to recover elided detail — run `caveman mcp install <agent>`". Karar açılışta, ajanın kalıcı MCP kaydına bakılarak verilir; o çağrıya özel `--mcp-config` ve `CAVEMAN_SUBSCRIPTION_COMPRESS=true` yetmez.
- `caveman stats --json` (30 gün, 32 istek, auth_mode subscription): before_tokens = after_tokens = 2028741, saved_tokens 0.
- caveman-mcp kolunun +%60 girdisi sıkıştırmadan değil: Headroom'un sıkıştırması yok (doğrudan yukarı akış) + fazladan MCP sunucusu; 2-json-alan'da daha çok tur.
- Max'ta ölçmenin tek yolu `caveman mcp install claude` (global MCP kaydı) → bu dalgada yasak; Ömer kararı gerekir. Proxy 48340 durduruldu, 8788 boş, parmak izi eşit.
