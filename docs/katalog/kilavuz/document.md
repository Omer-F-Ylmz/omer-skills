# document — 4 benzersiz kayıt

**Amaç:** İnsana yönelik doküman yazımı: PR açıklaması, changelog, sürüm notu, postmortem, API uç noktası dokümanı ve eksik doküman üretimi.

**İç yapı:** Tümü [skill], ad kalıbı document-<konu>: document (/document pr|changelog|release-note|postmortem), document-api-endpoint, document-generate ve document-release (gstack).

## En güçlü parçalar
- `document` — PR, changelog, sürüm notu ya da postmortem için insana yönelik metni tek komutla yazar.
- `document-api-endpoint` — Uç nokta dokümanı, OpenAPI ve @extend_schema ekleme/düzeltme, yanıt tipleme.
- `document-generate` — Özellik, modül ya da proje için eksik dokümanı sıfırdan üretir.
- `document-release` — Sürüm dokümantasyonu denetimi.

## Birlikte kullanım
- document-generate → document-release: dokümanı üret, sürümde denetle.
- document-api-endpoint + dok ailesindeki dok-dokuman-sapmasi: API dokümanını kodla uyumlu tutmak.
- document (changelog) + writing-commit-messages: commit'ten sürüm notuna.

## Tuzaklar
- document-api-endpoint @extend_schema'ya dayanır; o kalıbı kullanmayan projelerde kısmen geçerli.
- document-generate ve document-release gstack kaynaklıdır; açıklamaları çok kısa, kapsam girdide belirtilmemiş.

## Üyeler
- skill (4): document, document-api-endpoint, document-generate, document-release
