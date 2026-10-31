# Agent Reach

- tür: arac · durum: KURULU-KANITSIZ · videolar: DaDTgsJsdDk,Db3iw6NMPrO,Db_7HChtxFW,DcGJhY3qdnt,DdZQ5SaDxDV,DdZQr4OAVe5,DdZmPY4u-xd,De10iPOiB6V,De14ifUEh-N,De9mZYXCGeB,DeKFBr0vRpv,DeKuUWUKp7J,DeNy_grv_AM,DeR3K9LAq97,DeRwKUAsJW9,DeYmzg6NTer,DeaEzfQI7cv,DeddnBCCSv4,Deo4zimOeWn,DertHe1RiL5,DfA-nQWiPKz,DfC8uCmNo_Q,DfCtGNgiWeb,DfDAxN1Rex-,DfDvhU7opmg
- bizde: docs/envanter/envanter.tsv; yontem:.kos\kopru\kaynak-dizin\dizin.tsv; uv tool:docs\katalog\yetenek.tsv; ~/.claude/skills:docs\katalog\yetenek.tsv

## Özellikler
- Claude Code gibi agent'lara 15 kanaldan canlı internet okuma/arama yeteneği kazandırır
- YouTube transkriptleri, Reddit thread'leri, Twitter, RSS ve Bilibili, Xiaohongshu, Instagram gibi platformları kapsar (alıntıda '10+ diğer' platform da geçiyor)
- Resmi ücretli API gerektirmediği, ücretsiz ve açık kaynak olduğu belirtiliyor
- Komut satırı arayüzü (CLI) olarak tanımlanıyor
- Orkestratör: araçları kurar, sağlık kontrolü yapar ve istekleri en iyi kullanılabilir açık kaynak araca yönlendirir
- Alıntıda GitHub'da 62.683 yıldız (Şubat 2026 çıkışından sonraki beş ay) yazıyor

## Videoda yapılış
Kurulum: agent'a tek bir cümle yapıştırılıyor, kurulumu agent kendisi yapıyor (alıntı: 'agent'ına tek bir cümle yapıştırıyorsun, gerisini o hallediyor'). Kullanım: Claude Code üzerinden agent'a içerik istenir (YouTube özeti, Reddit/Twitter araması vb.). Komut satırı adımları alıntıda kesik geçiyor.

## Bizdeki karşılık ve fark
docs/envanter/envanter.tsv kaydı var; yöntem: .kos\kopru\kaynak-dizin\dizin.tsv; uv tool kaydı ve ~/.claude/skills kaydı docs\katalog\yetenek.tsv'de. Durum KURULU-KANITSIZ, yani kayıt var ama kurulumu doğrulayan kanıt yok. FARK: videoda tek cümleyle kurulum anlatılıyor, bizde kurulum doğrulanmamış.

## Al
Tek cümleyle agent-güdümlü kurulum; API anahtarı/ücretli API olmadan platform okuma; sağlık kontrolü ve otomatik yönlendirme.

## At
Alıntıda açık bir kötü yan yok. Alıntıda resmi API'lerin platform başına ayrı anahtar/abonelik gerektirdiği belirtiliyor; Agent Reach bunu atlamayı vaat ediyor, bu vaadin sürdürülebilirliği alıntıdan doğrulanamaz.
