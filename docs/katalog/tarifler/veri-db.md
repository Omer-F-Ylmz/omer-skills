# Veri ve veritabanı — birleşim tarifi
Ne zaman: Şema tasarımı, migration, yavaş sorgu ya da veri analizi işi.

## Fazlar
1. Keşif: `departman-veri-db` — şema, migration, sorgu ve Supabase/Postgres/EF Core sırası · birlikte: `graphify` veri erişim kodunu bulur.
2. Şema: `ecc:postgres-patterns` — indeks türü, veri tipi, RLS kalıpları · birlikte: `supabase-postgres-best-practices` Postgres'e yazmadan önce yüklenir. MySQL ise `ecc:mysql-patterns`.
3. Migration: `ecc:database-migrations` — ileri yönlü değişiklik, expand-contract, eşzamanlı indeks, toplu backfill · birlikte: `db-migration-planlayici` kesintisiz adımları planlar; EF Core ise `dn-efcore-migration`.
4. Sorgu: `db-sorgu-optimize` — sorgu planı okur, indeks ve join düzeltir · birlikte: EF Core ise `dotnet-data:optimizing-ef-core-queries`.
5. Analiz: `ml-pandas` — join, groupby, zaman serisi, dtype · birlikte: `context-mode:context-mode` büyük çıktıyı bağlama dökmeden işler.
6. Yedek ve kapanış: `db-yedekleme-geri-yukleme` — yedek, PITR ve geri yükleme tatbikatı · birlikte: `superpowers:verification-before-completion`.

## İnceleme ajanları
- `engineering-database-optimizer`: şema, sorgu ve indeks ikinci görüşü.
- `engineering-database-reliability-engineer`: yüksek erişilebilirlik ve kesintisiz göç.

## Güvenlik ve kalite kapıları
- Migration geri alma yolu yazılı; büyük tabloda deneme önce kopyada.
- RLS politikaları test edildi (`ecc:postgres-patterns`).
- Bağlantı dizesi depoda değil: `gitleaks`.
- Kişisel veri: `sec-kvkk-gdpr-kontrol` (saklama, silme).

## Tartışma konseyi
- Karar: şema biçimi, normalize mi denormalize mi, göç stratejisi.
- `ecc:council` — varsayılan Claude personaları: DBA, uygulama geliştirici, operasyon.

## Jeton bütçesi
- Keşif: küçük (~6k, tahmini). Şema: orta (~12k). Migration: orta (~15k). Sorgu: orta (~10k); büyük plan çıktısı `okuyucu` alt ajanına. Analiz: orta (~15k). Kapanış: küçük (~4k). Hepsi tahmini.

## Kaçınılacaklar
- Prisma reset ve drizzle-kit push veriyi silebilir (`ecc:database-migrations` uyarısı).
- MySQL kalıbını MariaDB'de denemeden uygulamak; sürüm farkı vardır.
- Ham sorgu sonucunu bağlama dökmek.

## Aday (kurulu değil)
yok
