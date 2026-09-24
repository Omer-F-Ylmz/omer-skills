# Suite süresi (21a K3)

## Önce
- 28 dk'lık koşu: ajan a84667b (oturum 00ca9a44, general-purpose), 1701 s, 45 araç çağrısı, 10.3M kümülatif token. Kök suite'i `uv run --no-project --with pytest python -m pytest tests` ile koştu. İlk çağrı 182 s sürdü; ardından Monitor ile ~11 dk bekledi, süreci taskkill ile öldürdü, 92 s'lik bir yeniden deneme yaptı ve en sonunda `python -m pytest tests` ile 13 s'de bitirdi.
- 21a'da yeniden üretildi: `uv run --with pytest pytest tests` 03:08'de başladı, 03:10'da hâlâ `gstack_browse.py goto` bekliyordu (süreç ağacı kanıtı); süreç öldürüldü.

## Kök neden
uv'nin izole ortamında playwright kurulu değil. `tools/gstack_browse.py` `--serve` sunucusunu stderr DEVNULL ile başlatıyor; sunucu ImportError ile sessizce ölüyor, istemci `_sunucu_ac` içinde bağlantı için 120 sn bekliyor (`tools/gstack_browse.py:361-366`). ~20 test × 120 s ≈ 40 dk.
Suite'lerin kendisi yavaşlamadı: video 247 test 11 s, jev 81 test 1.1 s (`--durations=25` ile ölçüldü; en yavaş test 1.21 s).

## Düzeltme (test davranışı değişmedi)
suite-kosucu kök suite'i ortam python'uyla koşuyor (`python -m pytest -q -p no:cacheprovider tests`, playwright ve pytest kurulu): 44 test, 16 s. Testlere, shim'e ya da zaman aşımlarına dokunulmadı.

## Sonra
Tam suit (6 suite) suite-kosucu ile: docs/olcumler/suite-kosucu.md.
