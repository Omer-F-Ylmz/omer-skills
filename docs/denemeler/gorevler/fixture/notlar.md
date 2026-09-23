# Sipariş servisi — hafta notları

- Ödeme adımına idempotency anahtarı eklendi; aynı istek iki kez gelirse ikinci kayıt oluşmuyor.
- Kargo ücreti hesabı ayrı modüle taşındı, eski fonksiyon silinmedi (iki yerde çağrılıyor).
- Stok düşümü hâlâ sipariş onayından önce yapılıyor; iptal edilen siparişte stok geri gelmiyor (açık hata #142).
- Entegrasyon testleri 38/40 geçiyor; iki test sahte kargo API'sinin zaman aşımına bağlı olarak kararsız.
- Müşteri bildirim e-postaları kuyruğa alındı ama yeniden deneme sayısı sınırsız.
- Karar: stok düşümü onay sonrasına alınacak, önce #142 için kırmızı test yazılacak.
