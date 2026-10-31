# security-audit skill

- tür: arac · durum: CALISIYOR · videolar: Dd1gnAPCMGd,Dd_wlJNqYVv,DdccgmSG8E9,De2j7BToUy4,DeCixT6ilL7,DeJxR3-hR5b,DeVyGbyJGcl,DesJpohI7VN,DfAdjJnIapp,DfFkcR3JumL
- bizde: ogren/video-izle-kur-1/envanter.tsv; kaynak-kutuphane/envanter:docs/envanter/envanter.tsv; kaynak-kutuphane/envanter:.kos/kopru/ogren/video-izle-kur-1/envanter.tsv

## Özellikler
- Tam repo güvenlik denetimi yapan skill (video açıklamasında Cloudflare Security Audit Skill olarak geçiyor)
- Altı adım: [1/6] Recon·girdileri eşle; [3/6] Validate·taze verifier; [6/6] Report·confirmed / needs_validation / rejected
- Çıktı dosyası: findings.json

## Videoda yapılış
Videodaki istem: 'security-audit skill ile tam güvenlik denetimi çalıştır; bitince findings.json'u aç; yalnız confirmed bulguları düzelt; her bulgu için ayrı commit ve önce başarısız, sonra geçen bir test ekle; needs_validation işaretli şeylere dokunma.' Video denetimi iki kez çalıştırmayı öneriyor (Run1 yaklaşık yarısı, Run2 kalanı).

## Bizdeki karşılık ve fark
Envanterde kayıtlı: ogren/video-izle-kur-1/envanter.tsv; docs/envanter/envanter.tsv; .kos/kopru/ogren/video-izle-kur-1/envanter.tsv. Durum: CALISIYOR. Fark: transkriptte bizdeki kurulumla karşılaştırma yok.

## Al
Bulguları confirmed / needs_validation / rejected olarak ayırma; bulgu başına commit ve önce-başarısız-sonra-geçen test disiplini

## At
Tek çalıştırma tüm bulguları yakalamayabilir (video iki çalıştırma öneriyor). Transkriptteki 'Run1 yarısı, Run2 kalanı' ifadesi ve '%97' bağlamı açıklanmamış.
