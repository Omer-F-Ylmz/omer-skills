# convex — 34 benzersiz kayıt

**Amaç:** Convex reaktif arka uç: hızlı başlangıç, şema/fonksiyon tasarımı, auth/yetki, Stripe faturalama, cron, göç provası, yedek tatbikatı, maliyet ve insights izleme, üretim hatasını kendiliğinden onarma.

**İç yapı:** Tümü [skill], convex-<iş>; giriş convex, yaşam döngüsü (quickstart → design → add → test/verify → deploy-guard → launch-readiness), operasyon (insights, monitor, cost, backup), convex-paket 33 skill.

## En güçlü parçalar
- `convex` — Proje Convex kullanıyorsa ya da herhangi bir arka uç/kalıcılık gerekiyorsa giriş.
- `convex-deploy-guard` — Dağıtım etkili komut öncesi hedefi sınıflar; prod için yeni açık onay ister.
- `convex-launch-readiness` — authz, reviewer, advisor, insights denetimlerini tek puanlı rapora toplar.
- `convex-authz` — Argümandan kimlik taklidi, belge sahipliği kontrolü eksikliği gibi yetki açıklarını sertleştirir.
- `convex-migrate-rehearse` — Şema değişikliği + backfill'i snapshot'lı önizlemede prova edip sonra terfi ettirir.
- `convex-backup` — Yedek kurar ve geri yüklemeyi atılabilir önizlemede tatbikatla kanıtlar.
- `convex-verify` — Seed + convex-test ile çok kullanıcılı, negatif durumlu özellik kanıtı.
- `convex-cost` — Fonksiyonları okunan bayt/belge × çağrı hacmine göre sıralayıp harcamayı öngörür.
- `convex-self-heal` — Üretim hatasını triyaj, kök neden, onarım ve sertifikalı fix PR'ına çevirir.

## Birlikte kullanım
- convex-quickstart → convex-design → convex-add → convex-test → convex-verify.
- convex-migrate-rehearse → convex-migrate: önce prova, sonra canlı göç.
- convex-launch-readiness = convex-authz + convex-reviewer + convex-advisor + convex-insights.
- convex-sentinel + convex-monitor + convex-self-heal: hata yakalama ve onarım.

## Tuzaklar
- convex-improve-convex-plugin oturum transkriptini Convex ekibine gönderir; gizlilik riski.
- convex-billing Stripe gerektirir; convex-cost harcama öngörür, Convex ücretli kullanım içerir.
- convex-paket ile tekil skill'ler çakışan kopya; convex-expert açıklamada 'agent' der ama [skill].
- Prod dağıtımında convex-deploy-guard atlanırsa onay kapısı devre dışı kalır.

## Üyeler
- skill (34): convex, convex-add, convex-advisor, convex-agent, convex-auth, convex-authz, convex-backup, convex-billing, convex-cost, convex-create-component, convex-crons, convex-deploy-guard, convex-design, convex-docs, convex-domains, convex-env, convex-expert, convex-explain-app, convex-improve-convex-plugin, convex-insights, convex-launch-readiness, convex-migrate, convex-migrate-rehearse, convex-monitor, convex-optimize, convex-paket, convex-quickstart, convex-reviewer, convex-seed, convex-self-heal, convex-sentinel, convex-suggest, convex-test, convex-verify
