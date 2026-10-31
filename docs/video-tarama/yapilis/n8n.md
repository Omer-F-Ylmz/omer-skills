# n8n

- tür: arac · durum: KURULU-KANITSIZ · videolar: 1Jb517FRX7I,1nzxcq61Ffw,3XIGcM7VICc,4r-gw-_XBW4,7tInlFRcTEQ,8NSyI-npJCU,DKwtekCPHTu,DQwPHoljyij,DRzxUxOAuVF,DSm-QQ_Dxh3,DVQd446DxqG,DVzLhsUDB2U,DXmLNzLjKCe,DY8EtIPtKLC,DYkKKKDiKHs,DZ29oQwDBlV,DZ3PUfYlK6z,DZGGQPHgtDI,DZU07JYgtX3,DZ_jVqnGTT0,DZffvsLiUvz,DaFXZ1mAsAZ,Daqywx1SqYM,DbOUP9OPDAQ,DbsSDgAm5JX,DcI7RhdKVXC,DcQwBpXDSXs,DcvZMSqtFRQ,Dd5EehjIG98,DdVWXArCa_T,DdWcPoADJK3,DdbljkbH5b2,DddrOAliOMK,DdjV
- bizde: docs/envanter/envanter.tsv

## Özellikler
- Self-host n8n'de webhook URL'lerinin dışarıdan erişilemeyebileceği belirtiliyor (localhost sınırlaması)
- Webhook'ları dış dünyaya açmak için ngrok ile localhost'u geçici olarak internete açma yöntemi
- Alternatif olarak Render.com üzerinde barındırma

## Videoda yapılış
ngrok ile localhost'taki n8n geçici olarak internete açılır; alternatif olarak n8n Render.com'da self-host edilir. Ayrıntılı komut alıntıda yok.

## Bizdeki karşılık ve fark
Envanter kaydı: docs/envanter/envanter.tsv. Durum KURULU-KANITSIZ; kurulumu/çalıştığı kanıtlanmamış. Fark karşılaştırılamadı.

## Al
Webhook erişim sorununa iki alternatif (ngrok geçici, Render kalıcı) sunulması

## At
ngrok ile yerel n8n'i internete açmak güvenlik riski taşır; alıntıda kimlik doğrulama/koruma anlatılmıyor. Alıntıdaki Claude Code token videosu n8n ile ilgisi olmadığı için dahil edilmedi.
