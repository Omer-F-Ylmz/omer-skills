# FFmpeg

- tür: arac · durum: KURULU-KANITSIZ · videolar: 4cE9t4rE0-0,DX2ubACJYRN,DY8EtIPtKLC,DYf-n9PguD5,DaLGdlHuOKh,DbEIoM4Fd08,DbLROjmkXwp,DclpFAJiyuv,DdWwZhgTnY_,DdY-K9oDbHl,Dd_2M8njh_2,DdnQtgBCUZu,De2TJpwjJWX,De2kpfnCFeH,De3v2qwj7fo,De5b0gljdOZ,De6jpQyDAhc,De9D5Z9kx9a,DeEHG3cgL8h,DeHGj-mG-5V,DeRvxD6gDCu,DeSCS3FigUS,DeSW9GFBQvF,DeSYR9fxKbV,DeWrlJkyGJt,DeXAMs2Eqgh,DeYZpq3gthM,DeZRVmkvhiR,DebqfLMkiPf,Deey9KZEYG8,DehjgOtDn77,Deidr7QOet0,Dej2ynmEjOD,Deke
- bizde: tablo13.tsv; yontem:.kos\kopru\kaynak-dizin\dizin.tsv; cc-kopru izinli:docs\katalog\yetenek.tsv; kaynak-kutuphane/envanter:docs/envanter/envanter.tsv; kaynak-kutuphane/envanter:.kos/kopru/ogren/video-izle-kur-1/tablo13.tsv

## Özellikler
- Kaynak videoyu ALL-KEYFRAME MP4'e önceden kodlama (her kare keyframe)
- Videoyu parçalayıp kareleri (screenshot) çıkarma ve Claude Code'a verme (Cloud Video reposu)

## Videoda yapılış
Claude Code ile yapılan yacht sitesi videosunda, kaydırmayla sürülen hero videosu için kaynak dosya ffmpeg ile ALL-KEYFRAME MP4'e kodlanıp o dosya kullanılıyor (kural a). Gerekçe alıntıda 'reverse/in-...' diye kesilmiş; komut ve parametreler yok. Cloud Video reposunda video FFmpeg ile parçalanıp kareler Claude Code'a veriliyor.

## Bizdeki karşılık ve fark
FFmpeg, kayıt dosyalarında geçiyor (tablo13.tsv, yetenek.tsv, envanter.tsv); durum KURULU-KANITSIZ. Kurulum kanıtı yok; video kare/keyframe iş akışı bizde doğrulanmamış.

## Al
Kaydırmayla sürülen videoda akıcılık için tüm karelerin keyframe olduğu MP4 kullanımı; videodan kare çıkarıp AI'ye verme yaklaşımı.

## At
-
