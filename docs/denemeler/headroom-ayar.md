# Deneme: headroom-ayar

20b1: 20a'daki Headroom +%29 girdi farkı bağlanma biçiminden mi, gürültüden mi? K1: istek başı bağlam iki kolda ~100k, araç araması (ENABLE_TOOL_SEARCH) global ayarda zaten açık, `headroom wrap` istemciye yalnız ANTHROPIC_BASE_URL + ENABLE_TOOL_SEARCH geçirir. headroom-wrap kolu wrap'ın env'ini açıkça verir; headroom-mevcut ile aynı sonuç gelirse iki kol arası fark gürültü bandıdır. --1m modeli opus'a çevirir, sonnet kıyasına girmez.

## Hipotez
4 okuma görevinde Headroom kolları doğrudandan daha az girdi token harcar; 20a farkı tek görevin tur sayısı gürültüsüydü.

## Metrik
kol başına girdi token · soğuk $ · sıcak $ · başarı · kalite.

## Bütçe
`video dene headroom-ayar --gorevler okuma --tavan 24 --istek-tavan 30`: 4 görev × 3 kol × 2 koşu = 24 claude -p (tavan 32).

## Başarı eşiği
girdi token −%5

## Görevler
- 1-basarisiz-test
- 2-json-alan
- 3-hatali-diff
- 4-log-zincir

## Kollar
- dogrudan: temel · env ANTHROPIC_BASE_URL=https://api.anthropic.com
- headroom-mevcut: env ANTHROPIC_BASE_URL=http://127.0.0.1:6767
- headroom-wrap: env ANTHROPIC_BASE_URL=http://127.0.0.1:6767 ENABLE_TOOL_SEARCH=true
