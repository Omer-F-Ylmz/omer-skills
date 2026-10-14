# db — 34 benzersiz kayıt

**Amaç:** Veritabanı ajan kadrosu: şema ve indeks tasarımı, sorgu optimizasyonu, migration, kilitlenme/şişme teşhisi, yedekleme ve motor bazlı (Postgres, MongoDB, Redis, ClickHouse vb.) modelleme.

**İç yapı:** 34 [ajan], db-<konu> adlı; gruplar: genel tasarım (sema-tasarim, indeks-danismani, sorgu-optimize), migration (migration-planlayici, flyway, liquibase, veri-tasima), teşhis (kilitlenme, postgres-sisme, replika-gecikmesi), motora özel (cassandra, dynamodb, mongodb, neo4j, sqlite...), ORM (efcore-sql-gecis, mongoose-odm, sequelize).

## En güçlü parçalar
- `db-sorgu-optimize` — Sorgu planını okuyup yavaş SQL'i daha iyi indeks ve join'le yeniden yazar.
- `db-indeks-danismani` — Erişim kalıbına göre indeks seçer, kullanılmayan/yinelenen indeksleri bulur.
- `db-migration-planlayici` — Expand-contract adımlarıyla kesintisiz canlı şema göçü planlar.
- `db-sema-tasarim` — Yeni tablolar için anahtar, kısıt ve adlandırmalı normalize ilişkisel şema.
- `db-kilitlenme` — Deadlock ve kilit beklemelerini (40P01, MySQL 1213) teşhis edip sıra/işlem/yeniden deneme düzeltir.
- `db-yedekleme-geri-yukleme` — Yedek, zamanda noktaya geri dönüş ve geri yükleme tatbikatını gözden geçirir.
- `db-veri-kalitesi` — İçe aktarma öncesi basit SQL kontrolleriyle yinelenen, boş ve aralık dışı değerleri bulur.
- `db-rls-politika` — Postgres satır düzeyi güvenlik politikalarını yazar ve inceler (Supabase, açık API).

## Birlikte kullanım
- db-sema-tasarim → db-indeks-danismani → db-sorgu-optimize: tasarla, indeksle, yavaş sorguyu düzelt.
- db-migration-planlayici + db-flyway / db-liquibase: kesintisiz göç planını araç değişiklik kümesine dök.
- db-veri-kalitesi + db-veri-tasima: taşıma öncesi temizlik, sonrası doğrulama sayımı.
- db-supabase-kurucu + db-rls-politika: Supabase projesi ve satır düzeyi güvenlik.

## Tuzaklar
- db-analitik-sorgu iş sorusu sorguları içindir; performans için db-sorgu-optimize.
- Motora özel ajanlar (db-cassandra, db-dynamodb, db-cockroachdb, db-neo4j) yalnız o motor kullanılıyorsa seçilmeli.
- db-veri-modelleme-nosql ile db-mongodb modelleme kapsamı örtüşür.

## Üyeler
- ajan (34): db-analitik-sorgu, db-bi-rapor, db-cassandra, db-clickhouse-sorgu, db-cockroachdb, db-dynamodb, db-efcore-sql-gecis, db-elasticsearch, db-flyway, db-indeks-danismani, db-json-sutun, db-kilitlenme, db-liquibase, db-migration-planlayici, db-mongodb, db-mongoose-odm, db-neo4j, db-pglite, db-postgres-sisme, db-redis-yapi, db-replika-gecikmesi, db-rls-politika, db-sema-tasarim, db-sequelize, db-sorgu-optimize, db-sqlite, db-supabase-kurucu, db-utf8mb4-karakter, db-vektor-veritabani, db-veri-kalitesi, db-veri-modelleme-nosql, db-veri-tasima, db-yedekleme-geri-yukleme, db-zaman-damgasi
