# test — 4 benzersiz kayıt

**Amaç:** Test yazma ve test kalitesi: yeni koda test takımı, değeri düşük/çift testleri bulma, test güdümlü geliştirme disiplini.

**İç yapı:** Tümü [skill]; test (/test), test-audit (gstack), test-driven-development.

## En güçlü parçalar
- `test-driven-development` — Her mantık, hata düzeltme ya da davranış değişikliğinde.
- `test` — Yeni yapılan ya da değişen koda /test ile test takımı.
- `test-audit` — Değeri düşük/çift testleri ve yalnız onların yaşattığı kodu bulur.

## Birlikte kullanım
- test-driven-development → test → test-audit.
- dotnet-agent-skills dotnet-test:* skill'leri .NET'e özel karşılık.

## Tuzaklar
- test-driven-development çok geniş tetikleyicili; her değişiklikte devreye girer.
- Dil/çerçeve kapsamı katalog metninde belirtilmemiş.

## Üyeler
- skill (4): test, test-audit, test-driven-development, test-playable-web-games
