# /review

- tür: arac · durum: KURULU-KANITSIZ · videolar: DYwe8NLjYWo,Db_H8ScP5y-,Dd4C4cEj3Ht,DdFQ-K0AJ0b,Ddb1UVZIakr,DeHbBTZjx5O,DeKv-iWIOOM,Dej0ddaASU6,DeoJn2HkrK4,LbBC5Wew4qs
- bizde: docs/envanter/envanter.tsv; ~/.claude/skills:docs\katalog\yetenek.tsv; kurulu-skill:~/.claude/skills/review

## Özellikler
- gstack eklentisi (alıntıda 'Installing gstack', 'By Garry Tan (CEO, Y Combinator)', '20K+ stars'): 6 skill, 24 komut
- Komutlar arasında /plan-ceo-review, /plan-eng-review, /plan-design-review, /review, /qa, /ship
- Aynı alıntıda security-guidance v2.1.0 (By Anthropic, official) kurulumu da geçiyor

## Videoda yapılış
Alıntıda 'Plugin installed successfully!' mesajı var; tam kurulum komutu net değil ('claude /install ...' bozuk). Komutlar giriş noktası olarak sunuluyor ('The commands above are entrypoints').

## Bizdeki karşılık ve fark
BIZDE: docs/envanter/envanter.tsv; ~/.claude/skills: docs\katalog\yetenek.tsv; kurulu-skill: ~/.claude/skills/review. Durum KURULU-KANITSIZ: yol kayıtlı, kurulum kanıtı yok. Fark: videodaki /review gstack paketinin komutu; bizdeki ~/.claude/skills/review. Paket ilişkisi kayıtta yok.

## Al
Yayın öncesi akış komutlarının (/qa, /ship, plan-review) tek pakette gelmesi.

## At
Alıntıda kurulum komutu bozuk; 'yorumlara skill yaz' ile DM tanıtımı var. Komutların çalıştığına dair kanıt yok.
