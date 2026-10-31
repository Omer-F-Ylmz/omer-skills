# CLAUDE.md

- tür: varlik · durum: KURULU-KANITSIZ · videolar: 1Jb517FRX7I,5LLLxHxkCnI,7XhX8P0ebEU,8NSyI-npJCU,DVyqBiejOh8,DXvgZqaNXvp,DYKXe-YjOrd,DYnMgwUup9N,DYpUIoEsne4,DYwe8NLjYWo,DZ-ZlbQFZy2,DZDfQLkAvWq,DZU07JYgtX3,DaDTgsJsdDk,DaWTq7aKSKq,DaagbUMP8Tg,DapwbVQAoiY,Db6E5RXgupy,DbUcU4Jjm1p,Db_7HChtxFW,Dc1NYVJA8A2,Dc84Z0-iY5s,DcN-pkGBLHE,DcQjXeuyFfJ,DcY-csFDG6f,Dcd3eY1iOMA,DcoaU2yjNOj,Dd15NcHvlNl,Dd7WYSniFvP,DdA-QjwAMh_,DdL6Q0rox-Z,DdUk0Lrx0rw,DdW9enHTUDb,DdWS
- bizde: docs/envanter/envanter.tsv

## Özellikler
- Hatalardan ders çıkarma: Claude aynı hatayı iki kez yaparsa bunu CLAUDE.md'ye kural olarak ekle
- Ders kuralı kısa tutulmalı; transkriptte 'maksimum 15 kelime' geçiyor (metin bozuk okunuyor)
- API isteklerinde daima try/catch kullan
- Tarih formatı her zaman ISO 8601 olsun
- Sorun limit değil, bağlam (context) problemidir
- Ağır prompt ile verilen ekstrede model 7 gizli sorunun hiçbirini söylemedi; kısa brifle iki denemede de 7'sini buldu
- Uzun prompt, şişmiş CLAUDE.md/AGENTS.md ve gereksiz skill'ler sonucu bozuyor (konuşmacı Anthropic ve OpenAI rehberlerine ve ETH Zürih ölçümüne atıf yapıyor)

## Videoda yapılış
Tekrarlayan hata görülünce kural CLAUDE.md'ye eklenir. Konuşmacı dosyalarını sadeleştirirken bir yöntem kullandığını söylüyor ama ayrıntı alıntıda yok.

## Bizdeki karşılık ve fark
docs/envanter/envanter.tsv (KURULU-KANITSIZ); fark bu alıntıdan doğrulanamadı

## Al
Hatayı kurala çevirme alışkanlığı; kısa ve odaklı CLAUDE.md

## At
Şişmiş CLAUDE.md/AGENTS.md ve gereksiz skill'ler sonucu bozuyor
