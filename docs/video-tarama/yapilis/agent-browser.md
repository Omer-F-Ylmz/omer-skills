# agent-browser

- tür: arac · durum: KURULU-KANITSIZ · videolar: DXwGMS_jK_B,Da0M8Ipmpxo,DbRGB9QsGtb,Dd4Ama8mnza,DdMIQE6kh8W,Ddcd73yAshV,DdtRDoSCll-,De3S2C3P7yb,DeHiUezkt8m,DePtyBoAOPd
- bizde: docs/envanter/envanter.tsv; yontem:.kos\kopru\kaynak-dizin\dizin.tsv; arac:.kos\kopru\kaynak-dizin\dizin.tsv; baglayici:.kos\kopru\kaynak-dizin\dizin.tsv; npm -g:docs\katalog\yetenek.tsv

## Özellikler
- Ajanın web sitelerini kullanmasını sağlayan skill (alıntı: 'agent-browser - lets the agent use websites')
- Google Maps'ten niş+şehir için veri çekme, web sitesi ve yorumlara göre filtreleme, kişiselleştirilmiş cold email yazma
- Çıktı: email, telefon, skor içeren CSV

## Videoda yapılış
Prompt zinciri: 'Agent-browser kullanarak Google Maps'ten [niş]+[şehir] için veri çek' → 'Web sitesi + yorumlara göre filtrele' → 'Her biri için kişiselleştirilmiş cold email yaz' → 'Çıktı: email, telefon, skor içeren bir CSV'. Lead listesi '[CSV yapıştır]' ile verilir.

## Bizdeki karşılık ve fark
BIZDE: docs/envanter/envanter.tsv; yontem/arac/baglayici: .kos\kopru\kaynak-dizin\dizin.tsv; npm -g: docs\katalog\yetenek.tsv. Durum KURULU-KANITSIZ: kayıtlı, kurulum kanıtı yok; bu oturumda çalıştırılmadı.

## Al
Lead toplama, filtreleme ve kişiselleştirilmiş e-posta akışının tek prompt zincirinde kurulabilmesi.

## At
Alıntıdaki PinchTab benchmark tablosu bozuk; PinchTab ile agent-browser arasında token maliyeti farkının yönü net değil. Apify ile rakip takipçi çekme üçüncü taraf servis gerektiriyor.
