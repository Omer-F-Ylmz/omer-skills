# codebase-memory-mcp

- tür: arac · durum: KURULU-KANITSIZ · videolar: DaqFZGMIw_N,DbL-SXnMKDF,DcBFIkCNDPy,DdEHh0UoENe,DdO8U92kcyw,DdUELmKktcr,Ddq_d1bDV_Z,De5WbI2sVs3,DeK77UqT6op,DeR3K9LAq97
- bizde: docs/envanter/envanter.tsv; yontem:.kos\kopru\kaynak-dizin\dizin.tsv; ~/.claude.json:docs\katalog\yetenek.tsv

## Özellikler
- Yüksek performanslı kod zekâsı MCP sunucusu
- 158 dil
- Sorgularda %99 daha az token (videodaki iddia)
- Tek statik binary, sıfır bağımlılık
- Saniyeler içinde indeksleme

## Videoda yapılış
Repo readme'sindeki tek satırlık komut terminale yazılıyor, kurulum tamamlanıyor. Ardından çalıştırılacak projenin içinde yapılan adım alıntıda kesik; ayrıntı yok. Agent'a önce haritaya bakması söyleniyor: değişikliğin nereleri etkileyeceği bu haritadan inceleniyor.

## Bizdeki karşılık ve fark
Envanterde ve dizinde kayıtlı: docs/envanter/envanter.tsv; .kos\kopru\kaynak-dizin\dizin.tsv; ~/.claude.json (docs\katalog\yetenek.tsv). Durum KURULU-KANITSIZ. Fark: kayıt var ama token tasarrufu ve harita kullanımı bizde ölçülmemiş.

## Al
Değişikliğin etkilediği dosyaları önceden haritadan bulup token harcamasını azaltmak.

## At
RAM tüketimi yüksek: 32 GB sistemde %96 üstü kullanım ve çökme yaşandığı belirtiliyor. Küçük projelerde kapatılmazsa etki tersine dönebiliyor (yorum).
