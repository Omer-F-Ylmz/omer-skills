# Jev

- tür: arac · durum: KURULU-KANITSIZ · videolar: Dd1jV3AgDiG,Dd1wKuDIO9r,Dd6P9YOB06z,Dd9XQ-QzIIf,Ddh509zOSrT,Ddja2_uDxqr,DdjdN0CCcU8,Ddl7Ss5sS5e,Ddm2r7KkiXU,Ddt16ilkRGB,DdtLoI-mfGB,DdtkBHBiXBj,DdtrqmqgJiN,DdwnD3mkyxm,DdznBJLyoEz,DeAr43JPbqv,DeCjTAWiSMn,DeHMM45NaFt,DeKalHoDNnd,DeOQHqBk9Pz,DfEvZRKJVu8,nT1KPAQL9_g
- bizde: docs/envanter/envanter.tsv

## Özellikler
- Ollaya: yerel karar modellerini çalıştırır; modelleri Ollama gibi model adıyla çeker (alıntı)
- Tek binary: 'ollaya serve' daemon'u çalıştırır; run, pull, list, ps, show, rm, cp, stop, create komutları Ollama gibi çalışır (alıntı)
- TypeSafe uyumlu: POST /v1/systemone, POST /v1/decisions ve GET /v1/models wire-identical (alıntı)
- Resmi SDK değiştirilmeden çalışır; ortam değişkeni TYPESAFE_BA... (alıntı kesik)
- Önerilen model winnow:e4b: tipli kararlarda 0.722 doğruluk, TypeSafe Jev'in 0.738'i karşısında; CPU'da yanıt süresi 89ms (alıntı kesik)
- Lead üretimi kullanım örneği (Treg; 320 kişiyi ~1 sent'e eleme iddiası, video anlatımı)

## Videoda yapılış
curl -fsSL https://ollaya.dev/install.sh | sh ile kurulur. 'ollaya serve' daemon'u başlatır; CLI daemon çalışmıyorsa onu kendisi başlatır. Mevcut Jev istemcileri bir ortam değişkeni değiştirilerek kullanılır.

## Bizdeki karşılık ve fark
docs/envanter/envanter.tsv'de kayıtlı; kurulu olduğu kanıtlanmamış. Fark: alıntıda yerel daemon ve TypeSafe uyumluluğu anlatılıyor, BIZDE alanında yerel çalıştırma kanıtı yok.

## Al
Yerel çalıştırma ve mevcut Jev istemcilerinde yalnızca ortam değişkeniyle geçiş

## At
Yerel modelde doğruluk düşük (0.722 vs 0.738); lead-gen ve maliyet iddiaları video anlatımına dayanıyor, doğrulanmamış
