# Deneme: subagent-haiku

video v-vRYtvWDYs · 15 · bu dalgada koşulmaz (14b)

## Hipotez
CLAUDE_CODE_SUBAGENT_MODEL=haiku dosya arama/düz iş alt ajanlarında $'ı düşürür; okuma görevlerinde (docs/denemeler/gorevler-okuma/) kalite kapısı düşmez.

## Metrik
okuma görevi (alt ajan işinin vekili) başına sıcak koşu $ ve token + kalite kapısı geçen görev sayısı; A: sonnet (CLAUDE:14) · B: haiku.

## Kollar
A: sonnet (CLAUDE:14) · B: haiku (env CLAUDE_CODE_SUBAGENT_MODEL=haiku).

## Görevler
4 okuma görevi (docs/denemeler/gorevler-okuma/; alt ajan işinin vekili).

## Tavan
claude -p en fazla 16 (--gorevler okuma: 4 görev × 2 kol × 2); bu dalgada 0.

## Geri alma
settings.json env'den CLAUDE_CODE_SUBAGENT_MODEL silinir; CLAUDE:14 değişmez (bu dalgada eklenmedi).

## Karar ölçütü
takas tablosu (omer-kurallar 21): kol başına sıcak koşu $, token ve kalite kapısı yan yana; tek eşik yok. Tablo haiku lehineyse CLAUDE:14 yeniden değerlendirilir, değilse aynen kalır (KURULUM-24e-2: eski tek eşik kaldırıldı).

## Not
Ömer kararı 28 Eyl (KURULUM-24e-1-KAPANIŞ): DENE — token. CLAUDE:14 'alt ajan sonnet' kuralı ölçümle yeniden değerlendirilir; çelişki RED sebebi değil (omer-kurallar 21). Bu dalgada koşulmaz. Aday: docs/kurulumlar/adaylar/claude-code-subagent-model-ayari.md
