# writing — 4 benzersiz kayıt

**Amaç:** Yazım skill'leri: Git commit mesajı, doküman/üslup denetimi, hookify kuralı ve skill yazımı.

**İç yapı:** Ad kalıbı writing-<konu>; 4 bağımsız [skill]: writing-commit-messages, writing-guidelines, writing-rules (hookify), writing-skills.

## En güçlü parçalar
- `writing-commit-messages` — Commit mesajı yazma ya da taslaklama istendiğinde etkinleşir.
- `writing-guidelines` — Dokümanları ve üslubu yazım el kitabına göre denetler.
- `writing-rules` — Hookify kuralı oluşturma ve yapılandırma.
- `writing-skills` — Skill oluşturma, düzenleme ve yayın öncesi doğrulama.

## Birlikte kullanım
- writing-commit-messages + document ailesindeki document (changelog): commit'ten sürüm notuna.
- writing-guidelines + dok ailesindeki dok-icerik-editoru: üslup denetimi ve düzenleme.
- writing-skills + skill ailesindeki skill-scanner.

## Tuzaklar
- Aile adı ortak önekten oluşur; üyeler birbirinden bağımsızdır (writing-rules hookify'a özgü).
- writing-skills, superpowers-writing-skills ile aynı açıklamaya sahip; çift kopya.

## Üyeler
- skill (4): writing-commit-messages, writing-guidelines, writing-rules, writing-skills
