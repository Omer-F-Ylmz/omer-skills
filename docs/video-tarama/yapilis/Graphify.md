# Graphify

- tür: arac · durum: KURULU-KANITSIZ · videolar: DX2ubACJYRN,DYKXe-YjOrd,DYpUIoEsne4,DbOoGjsCo50,Db_GVNhOnQF,Dcwzo9BuTcd,Dd0PFtECZvj,Dd4-QQgO-Hx,Dd9XQ-QzIIf,DdCs5vOiHRY,DdO1UioAHAS,Dd_dybEMDog,Dd_wlJNqYVv,Ddb1UVZIakr,Ddcd73yAshV,DdmQWJzqP8H,DdxDGbogAZV,De2kpfnCFeH,De5LuzmRWv0,De5WbI2sVs3,De92kC5ob3a,De95N60JYG2,De96ZEuvmbc,De9D5Z9kx9a,De9mZYXCGeB,DeAf-XgiK_a,DeCfWoGMIET,DeCixT6ilL7,DeHbBTZjx5O,DeHz9pjRytv,DeJk1lVs32y,DePUywkjHEz,DeUkYfLn4n5,DeVy
- bizde: ogren/video-izle-kur-1/envanter.tsv; yontem:.kos\kopru\kaynak-dizin\dizin.tsv; cc-kopru izinli:docs\katalog\yetenek.tsv; ~/.claude/skills:docs\katalog\yetenek.tsv; kaynak-kutuphane/envanter:docs/envanter/envanter.tsv

## Özellikler
- Dosyaları bir kez tarayıp bir knowledge graph oluşturur; oturumlar arasında kalıcıdır
- Sonraki oturumlarda Claude, tek bir dosya okumadan graph'ı sorgular
- Videoda bildirilen token düşüşü 71,5 kat
- Videoya göre Obsidian ile tam RAG arasında bir yerde konumlanır
- Oturum başında projeyi sıfırdan okumak 15-20 bin token harcıyor (video iddiası)

## Videoda yapılış
Kurulum: pip install graphifyy && graphify install. Ardından ~/.claude klasöründe /graphify ~/.claude komutu çalıştırılıyor; graph bir kez oluşuyor ve sonraki oturumlarda kullanılıyor.

## Bizdeki karşılık ve fark
Kayıtlarda ogren/video-izle-kur-1/envanter.tsv, cc-kopru izinli docs\katalog\yetenek.tsv, ~/.claude/skills ve docs/envanter/envanter.tsv geçiyor; durum KURULU-KANITSIZ. Yani kurulu görünüyor ama kanıt yok; graph'ın gerçekten oluşturulup kullanılıp kullanılmadığı bu kayıtlardan anlaşılmıyor.

## Al
Projeyi bir kez indeksleyip oturumlar arası kalıcı bir graph kullanma; her oturumda tüm dosyaları yeniden okumamak.

## At
71,5 kat tasarruf iddiası videonun kendi raporu; bağımsız doğrulaması yok. Kurulum komutundaki paket adı 'graphifyy' (çift y) alıntıda böyle geçiyor; kullanmadan önce doğrulanmalı. ~/.claude gibi kullanıcı yapılandırma dizinine komut uygulamak da dikkat gerektirir.
