# sepia — 8 benzersiz kayıt

**Amaç:** De-AI yazım paketi: metni insanlaştırma, AI tadını silme; yazma, inceleme, minimal düzeltme, tam yeniden yazım ve Hemingway üslubu ayrı girişler.

**İç yapı:** sepia [plugin] + genel yönlendirici sepia:sepia ve beş işlem girişi (write, review, refactor, recreate, hemingway); ayrıca sepia-paket.

## En güçlü parçalar
- `sepia:sepia` — Humanize/de-AI/unslop isteklerinde genel yönlendirici.
- `sepia:sepia-review` — Düzenlemeden yalnız düzyazıyı teşhis eder.
- `sepia:sepia-refactor` — Yerinde minimal düzyazı düzeltmesi.
- `sepia:sepia-hemingway` — Hemingway tarzı kurgu ya da hikâyede güçlü de-AI.

## Birlikte kullanım
- sepia:sepia-review → sepia:sepia-refactor: önce teşhis, sonra minimal düzeltme.
- linkedin-agent:li-human ile sosyal metinlerde.

## Tuzaklar
- write/review/refactor/recreate yalnız açıkça adıyla istendiğinde tetiklenir.
- sepia-paket ile sepia eklentisi çakışan kopya.

## Üyeler
- plugin (1): sepia
- skill (7): sepia-paket, sepia:sepia, sepia:sepia-hemingway, sepia:sepia-recreate, sepia:sepia-refactor, sepia:sepia-review, sepia:sepia-write
