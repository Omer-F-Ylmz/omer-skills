# Subagent

- tür: yontem · durum: KAYITSIZ · videolar: 1Jb517FRX7I,2n84xa99FRY,3XIGcM7VICc,DV4V4fCDPsV,DVyqBiejOh8,DYf-n9PguD5,DZ-ZlbQFZy2,DaagbUMP8Tg,DapwbVQAoiY,Dc7G9Pxu_1O,Dc_cgg-ETAF,Dd1766JOkfR,Dd8wLKzn7fK,DdolgdJjHMc,Ddrki7GugWV,DdzDB3Jq6K9,De5b0gljdOZ,De82MvBGH8X,DeBVRjpny1m,DeBl1GmsVLJ,DeKFBr0vRpv,Debf2CdhWCE,DecgPILOtoL,DeddnBCCSv4,Dee3AxgN_th,DefSWyWpABP,DegASWXxIDY,DehEgnEAaPn,DehQ41UoYHy,DekAh-5oM_m,DelHsxgBq13,DelQS4sE2Id,DemxJYzHB0n,DepN
- bizde: yok

## Özellikler
- Keşif ve kod okuma işini alt ajanlara yaptırıp ana bağlama yalnızca gerekli veriyi aktarmak
- Video'ya göre subagent'lar Opus ile çalıştırılırsa Fable'ın ek haftalık limitinden yemiyor
- Fable'ın ek limiti toplam haftalık limitin yarısı kadar
- Alt ajan kullanımı yaklaşık 150.000 token bağlam avantajı sağlıyor (videodaki tahmini)

## Videoda yapılış
Karar öncesi gereken veriyi almak için codebase'i alt ajanlara taratmak; alt ajanlar farklı dosyaları okuyup ilişkileri çıkarıyor ve ana ajana yalnızca ihtiyaç duyulan veriyi döndürüyor. Ana ajan Fable, alt ajanlar Opus olarak planlanıyor.

## Bizdeki karşılık ve fark
yok

## Al
Ara okuma ve araştırmayı alt ajana yaptırıp ana bağlamı küçük tutmak

## At
Alt ajan Fable olarak çalışırsa Fable'ın ek haftalık limitinden tüketir
