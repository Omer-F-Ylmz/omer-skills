---
name: departman-veri-db
description: "Veri/DB müdürü: şema, migration, sorgu ve Supabase/Postgres/EF Core sırası. Tablo, SQL, RLS ya da yavaş sorgu işinde oku."
---

# Departman: veri-db — iş sırası

Katalog: `docs/departmanlar/veri-db.md`.

## Adımlar
1. **Kurallar** — Postgres'e dokunmadan önce `supabase-postgres-best-practices`.
2. **Şema** — mevcut tabloları incele, sonra migration; Supabase projesinde `supabase`.
3. **Sorgu** — EF Core yavaşlığı `optimizing-ef-core-queries`; analitik `clickhouse-io`.
4. **Güvenlik** — RLS ve kiracı izolasyonu testi → `departman-guvenlik`.
5. **Test** — migration ve sorgu testleri → `departman-test-qa`.

## Kapılar
- Üretim veritabanına migration yalnız yerelde denendikten sonra ve onayla.
- Geri alma adımı olmayan migration yok.
