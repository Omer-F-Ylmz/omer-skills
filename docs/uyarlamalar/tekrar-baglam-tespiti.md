# Uyarlama: tekrar-baglam-tespiti

20b-devam K5 · kaynak: caveman learn `recurring_context:repaste` (docs/mekanizmalar/caveman.md) · kod yazılmaz; Desktop tarif verir · kod kopyalanmaz

## Fikir
Kullanıcı mesajlarındaki büyük blokları (≥2k token) normalize edip hash'le; aynı hash ≥3 oturumda geçiyorsa "tekrar kurulan bağlam" say. Blok kalıcı bir yere (skill, omer-kurallar, dalga şablonu) taşınıp tarifte yalnız adıyla anılabilir.

## Hedef araç/dosya
tools/video/video/cli.py `video durum` (ölçüm bulguları bölümüne tek satır) · departman-verimlilik müdürü

## Beklenen etki
learn ölçümü: ~38k token'lık 3 blok 9-16 oturumda yeniden kurulmuş (tarif yapıştırmaları). Blok başına oturum açılışında ~38k girdi yerine birkaç yüz token; önbellek önekini de sabitler.

## Kapsam
salt-okur tespit + öneri; tarif metni ya da hafıza otomatik değişmez.
