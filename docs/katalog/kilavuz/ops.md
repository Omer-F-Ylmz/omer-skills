# ops — 29 benzersiz kayıt

**Amaç:** Altyapı ve operasyon ajanları: Kubernetes/Helm/GitOps, IaC (Terraform, Pulumi), mesaj kuyrukları (Kafka, RabbitMQ, NATS, MQTT, SQS), gözlemlenebilirlik, sunucu sorun giderme, felaket kurtarma, maliyet.

**İç yapı:** Tümü [ajan], ops-<konu>; gruplar: kuyruk/mesaj, gözlem (prometheus, grafana, loki, elk, izleme, log şeması), K8s/IaC, sunucu sorunları (disk, fd, dns-tls, sertifika, ssh, systemd), Windows kurulum.

## En güçlü parçalar
- `ops-dagitim-sorun-giderme` — Başarısız deploy'u log, health check, config'den teşhis edip rollback ya da düzeltme kararı.
- `ops-dns-tls-sorun` — DNS, yayılım, sertifika zinciri ve yenilemeyi dig/openssl ile; yalnız belirtiyle çalışır.
- `ops-disk-dolu` — Sunucu diskini dolduranı bulup log, inode, silinmiş-açık dosyalarda güvenle boşaltır.
- `ops-k8s-is-yuku` — Probe, request/limit, autoscaling, PDB, rollout ayarı.
- `ops-terraform` — Remote state, locking, değişken ve güvenli plan/apply ile modüller.
- `ops-prometheus` — Makul kardinaliteyle metrik, PromQL ve alarm kuralı.
- `ops-felaket-kurtarma` — RTO/RPO hedefi, yedek, failover ve tatbikat planı.
- `ops-yapisal-log-semasi` — Seviye, korelasyon alanı, kararlı olay adlarıyla JSON log şeması.
- `ops-winget-kurulum` — Windows geliştirici makinesini winget manifest ve sürüm sabitleme ile kurar.

## Birlikte kullanım
- ops-yapisal-log-semasi → ops-loki-log / ops-elk-log → ops-grafana-pano.
- ops-prometheus + ops-grafana-pano + ops-dagitik-izleme: metrik, pano, iz.
- ops-terraform/ops-pulumi → ops-helm-chart → ops-gitops → ops-k8s-is-yuku.
- ops-sertifika-yenileme + ops-dns-tls-sorun: TLS kesintisi.

## Tuzaklar
- Kuyruk ajanları çok: bullmq, kafka, rabbitmq, nats, mqtt, sns-sqs; doğru broker seçimi ön koşul.
- ops-terraform ile ops-pulumi, ops-loki-log ile ops-elk-log alternatif; birlikte değil.
- ops-sertifika-yenileme ile ops-dns-tls-sorun kapsamı örtüşür.
- be ailesindeki be-mesaj-guvenilirligi ile mesajlaşma konusu çakışır.

## Üyeler
- ajan (29): ops-bullmq-kuyruk, ops-dagitik-izleme, ops-dagitim-sorun-giderme, ops-disk-dolu, ops-dns-tls-sorun, ops-dosya-tanimlayici-siniri, ops-elk-log, ops-felaket-kurtarma, ops-gitops, ops-grafana-pano, ops-helm-chart, ops-k8s-is-yuku, ops-kafka, ops-loki-log, ops-maliyet-optimize, ops-mqtt, ops-nats, ops-nginx-ters-vekil, ops-prometheus, ops-pulumi, ops-rabbitmq, ops-sertifika-yenileme, ops-serverless, ops-sns-sqs, ops-ssh-sertlestirme, ops-systemd-birim, ops-terraform, ops-winget-kurulum, ops-yapisal-log-semasi
