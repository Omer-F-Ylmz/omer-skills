# HubSpot

- tür: arac · durum: KURULU-KANITSIZ · videolar: CKHDBlGK3vo,DYT9GQMjOmx,Da8rBJszhPG,Dbf53LFPTBz,DbukLdmuB2x,DcTU_tLgujm,Dd64BawjBBx,Dd6Nj25AudW,DdbljkbH5b2,DdrEmDHkouJ,De4GsI7N9Wl,DeB6QU6N4Ec,DeFSkT6t05p,DeHUaCoPFTV,DeL-w7yxAS9,DeXJcXmFLMv,DepBDzoIjKW,DepEqC0kVog,DeqGkciIB21,Ders6b5z3cD,Detx5PHtW_R
- bizde: docs/envanter/envanter.tsv; plugin hubspot-sales@knowledge-work-plugins:docs\katalog\yetenek.tsv; ~/.claude/skills:docs\katalog\yetenek.tsv; kurulu-skill:~/.claude/skills/hubspot

## Özellikler
- Claude for Small Business paketinde HubSpot bağlantısı var (Pro planına dahil, 15 iş akışı)
- Anthropic Marketing eklentisi tek kurulumla 6 komut veriyor; HubSpot, Slack, Canva, Klaviyo'ya bağlanıyor
- /monday-brief: nakit, satış hattı, yeni lead, geciken görevler ve haftanın 3 önceliği

## Videoda yapılış
/run-campaign komutu: Claude kampanya metnini yazar, Canva varlığı üretir, HubSpot'tan e-posta listesi oluşturur ve gönderimi zamanlar. Her adım kullanıcı onayından geçer.

## Bizdeki karşılık ve fark
docs/envanter/envanter.tsv; plugin hubspot-sales@knowledge-work-plugins (docs\katalog\yetenek.tsv); ~/.claude/skills (docs\katalog\yetenek.tsv); kurulu skill ~/.claude/skills/hubspot. Durum: KURULU-KANITSIZ; bu çalışmada kurulum doğrulanmadı.

## Al
Her adımda kullanıcı onayı (kampanya gönderimi öncesi denetim) ve tek komutla haftalık özet.

## At
Transkriptte HubSpot API ayrıntısı yok; bilgi pazarlama iddiası düzeyinde. Otomatik e-posta gönderimi riski, onaysız çalışırsa veri/itibar kaybı.
