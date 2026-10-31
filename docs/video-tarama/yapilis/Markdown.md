# Markdown

- tür: arac · durum: KURULU-KANITSIZ · videolar: 4Hvkv_I8QDE,7XhX8P0ebEU,8NSyI-npJCU,DX1v6a1hqUf,DYYaA1LKtoO,DYd19cHDBaH,Dbm200gvDsG,Dbs-uI9sY2w,DbxCyfHAddF,DcTI5sfoLGR,DcgHbcNjDQO,DcvkRl6j2ux,Dcw20sWpLgs,DdFVkR3vIni,DdKLqdkKcjp,DdWfVfbErk3,Ddc1db7Cj_D,DdhP3u5gDci,Ddj_aUfK1Dh,De1IdFfjpAL,De1fLVOkpiu,DeCixT6ilL7,DeKv-iWIOOM,DePMsSOxhFs,DePUywkjHEz,DeXye75gGlo,DeaxjcMBKBy,DebPmJFgIbs,DecQ0rOAtzu,Dee_oBzIPmy,DehQ41UoYHy,DejXvdWvojK,DemNWrcvzCI,Denr
- bizde: ~/.claude/skills; kurulu-skill:~/.claude/skills/markdown

## Özellikler
- Üç katmanlı mimari: değiştirilmeyen ham kaynaklar, LLM'in sahip olduğu markdown wiki, ve yönlendirme katmanı
- LLM kaynağı okuyup ana bilgiyi çıkarır, wiki sayfalarını oluşturur/günceller, sayfalar arası bağlantı kurar
- Sorgu anında ham belgelerden sıfırdan derleme yerine birikmiş wiki kullanılır
- Obsidian ile görüntülenir

## Videoda yapılış
Yeni kaynak eklenir; LLM onu okur, özetler, varlık/kavram sayfalarını günceller ve çapraz bağlar. Kullanıcı kaynak seçer ve soru sorar; yazım işini LLM yapar.

## Bizdeki karşılık ve fark
Kurulu skill: ~/.claude/skills/markdown (durum KURULU-KANITSIZ, yani çalıştığı kanıtlanmamış). Alıntı, skill'in içeriğini karşılaştırmak için yeterli değil; fark tespit edilemedi.

## Al
Kaynak (ham, değiştirilmez) ile LLM'in yazdığı wiki katmanını ayırma ve birikmiş bilgi tutma fikri

## At
Alıntı üç katmanın üçüncüsünü tam göstermiyor; eksik kalan kısım tahmin edilmedi.
