# Deneme: subagent-haiku

video v-vRYtvWDYs · 15 · bu dalgada koşulmaz (14b)

## Hipotez
CLAUDE_CODE_SUBAGENT_MODEL=haiku dosya arama/düz iş alt ajanlarında $'ı düşürür; okuma görevlerinde (docs/denemeler/gorevler-okuma/) kalite kapısı düşmez.

## Metrik
okuma görevi (alt ajan işinin vekili) başına sıcak koşu $ ve token + kalite kapısı geçen görev sayısı; A: sonnet (CLAUDE:14) · B: haiku.

## Bütçe
claude -p en fazla 16 (--gorevler okuma: 4 görev × 2 kol × 2); bu dalgada 0.

## Geri alma
settings.json env'den CLAUDE_CODE_SUBAGENT_MODEL silinir; CLAUDE:14 değişmez (bu dalgada eklenmedi).

## Başarı eşiği
sıcak koşu $ ≥%20 düşüş VE kalite kapısı düşüşsüz; geçerse CLAUDE:14 yeniden değerlendirilir, geçmezse aynen kalır.

## Not
Ömer kararı 28 Eyl (KURULUM-24e-1-KAPANIŞ): DENE — token. CLAUDE:14 'alt ajan sonnet' kuralı ölçümle yeniden değerlendirilir; çelişki RED sebebi değil (omer-kurallar 21). Bu dalgada koşulmaz. Aday: docs/kurulumlar/adaylar/claude-code-subagent-model-ayari.md
