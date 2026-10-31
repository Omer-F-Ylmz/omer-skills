# Backtesting

- tür: yontem · durum: KURULU-KANITSIZ · videolar: DcOhWbqm3vK,Dd0ZDPRjIWA,Dd9RvQDiUVH,DdEv5OwBZ6f,De2EFbZjBHi,De7NqmHkbzU,Der12cMk0_N,DerRB3pEwMX,DerUSfFE14i,Dewvyk2E2Je,DewybS0FC3V,DfD4q2sDyNN,DfEbFKtj1xR
- bizde: docs/envanter/envanter.tsv; ~/.claude/skills:docs\katalog\yetenek.tsv; kurulu-skill:~/.claude/skills/backtesting

## Özellikler
- Çoklu venue, enstrüman ve strateji aynı anda backtest
- Tarihsel quote tick, trade tick, bar, order book ve özel veri; nanosaniye çözünürlük
- Araştırma ve canlı dağıtımda aynı strateji kodu
- Rust çekirdek, mimalloc allocator
- Herhangi bir REST API için modüler adaptörler
- Time in force: IOC, FOK, GTC, GTD, DAY; post-only, reduce-only, iceberg; OCO, OUO, OTO
- Bileşenleri cache ve message bus ile sıfırdan kurma
- TradingAgents: küresel piyasa ve kripto backtest (meow.codes videosu)

## Videoda yapılış
Videoda kurulum veya komut adımı yok; framework özellikleri okunuyor.

## Bizdeki karşılık ve fark
Kayıt: docs/envanter/envanter.tsv, ~/.claude/skills:docs\katalog\yetenek.tsv, ~/.claude/skills/backtesting; durum KURULU-KANITSIZ. Fark: kurulu ama kanıt yok. Videodaki özellikler (nanosaniye, OCO/OUO/OTO vb.) bizde doğrulanmadı.

## Al
Aynı strateji kodunu araştırma ve canlı ortamda kullanma. Çok venue'lu tarihsel simülasyon.

## At
Videoda ölçüm veya benchmark yok; yalnızca özellik listesi.
