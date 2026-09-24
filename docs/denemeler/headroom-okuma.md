# Deneme: headroom-okuma

22 K3: audit-reads Read'in %15'ini bayat (düzenlemeden sonra kalmış, ~886k tok), %7'sini satır no iskeleti buldu. Read lifecycle (bayat/aşılmış Read sıkıştırma) v0.37'de varsayılan açık, ana örnekte de açık. Kapalı iki özellik denenir: `--read-maturation` (taze Read'i önbellek önekinin dışında tutar, dosya durulunca sıkıştırır; beta) ve `--intercept-tool-results` (ast-grep Read outliner; canary).

## Hipotez
İkinci Headroom örneğinde iki okuma özelliği açıkken 4 okuma görevinde girdi token bugünkü Headroom'dan belirgin azalır, doğruluk düşmez.

## Metrik
kol başına girdi token · sıcak $ (karar) · soğuk $ (bilgi) · süre · başarı · Jev kalite.

## Bütçe
`video dene headroom-okuma --gorevler okuma --tavan 16 --istek-tavan 20`: 4 görev × 2 kol × 2 koşu = 16 claude -p, Jev ≤20.

## Proxy
Deneme başında (arka planda, yalnız süreç env'i): `HEADROOM_ROLLOUT_CHANNEL=canary headroom.exe proxy --port 8793 --no-http2 --no-telemetry --read-maturation --intercept-tool-results` (runtime venv, v0.37; `rollout status --channel canary --features read_maturation,tool_result_interceptors` → ikisi enabled=true). Ana örnek (6767→6768) değişmez. Bitince süreç numarasıyla durdurulur, 8793 boş mu bakılır.

## Başarı eşiği
girdi token −%10 (Headroom'a göre) ve kalite kapısı (18).

## Görevler
- 1-basarisiz-test
- 2-json-alan
- 3-hatali-diff
- 4-log-zincir

## Kollar
- headroom-mevcut: temel · env ANTHROPIC_BASE_URL=http://127.0.0.1:6767
- headroom-okuma: env ANTHROPIC_BASE_URL=http://127.0.0.1:8793
