# Gmail

- tür: arac · durum: KURULU-KANITSIZ · videolar: 0i65C2vzjpw,4Hvkv_I8QDE,4r-gw-_XBW4,7XhX8P0ebEU,9VSs2glPECM,DHwB6tduC5z,DIB_Xq5Obop,DKwtekCPHTu,DYT9GQMjOmx,DYh5eS_uB7u,DZI1ok5Ss4b,DaePJBuIOBd,DbI40Ums58-,DbI_v6gMDW1,Dbf53LFPTBz,DbfnLfgP40k,DbukLdmuB2x,DcQwBpXDSXs,Dc_Z3BEgsJN,DcgHbcNjDQO,DcwNfmMtUeq,Dd4C4cEj3Ht,Dd5EehjIG98,DdIELTZD2Uw,DdRd0SNkrW-,DdRnP0TTEJM,DdVWXArCa_T,DdbljkbH5b2,DdgxNnmID16,Ddi5_OkoiDa,Ddn42cHgbu8,DdtP_L9FljV,Ddw7dJEPos6,De-N
- bizde: docs/envanter/envanter.tsv; plugin claude-for-financial-advisors@knowledge-work-plugins:docs\katalog\yetenek.tsv; ~/.claude/skills:docs\katalog\yetenek.tsv; kurulu-skill:~/.claude/skills/gmail

## Özellikler
- Videoda kapsam (scope) seçenekleri görünüyor: Yeni Mail, Delete, Move, Mark as Unread
- Bağlı tek bir posta kutusu (Gmail) var
- Faturaları/abonelikleri Finance klasörüne otomatik taşıyan hazır bir skill bulunamadı; en yakın seçenek olarak 'Invoice Auto-Archiver' topluluk şablonları anılıyor

## Videoda yapılış
Alıntı bozuk ve adım adım kurulum içermiyor. Metinde, her fatura veya abonelik için otomasyon kurulup finance klasörüne konması isteniyor ve bunun kalıcı bir Gmail otomasyonu olarak kurulabileceği söyleniyor.

## Bizdeki karşılık ve fark
Kayıtlarda Gmail için docs/envanter/envanter.tsv, plugin claude-for-financial-advisors@knowledge-work-plugins ve ~/.claude/skills/gmail yer alıyor; durum KURULU-KANITSIZ. Kayıt var ama kurulu skill'in fatura taşıma yapıp yapmadığı alıntıdan doğrulanamıyor.

## Al
Faturaları ve abonelikleri tek klasörde toplamak için kalıcı, sürekli çalışan Gmail otomasyonu fikri.

## At
Delete ve Move gibi yıkıcı kapsamlar; mevcut postalara toplu değişiklik riski (alıntıdaki 'bulk change to existing mail' ifadesi bozuk, tam anlamı belirsiz).
