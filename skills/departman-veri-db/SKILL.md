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

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- `supabase:supabase` · Use when doing ANY task involving Supabase · `C:/Users/pc/.claude/plugins/cache/yerel-kurulum7/supabase/0.1.15/skills/supabase/SKILL.md`
- `supabase:supabase-postgres-best-practices` · Postgres best practices maintained by Supabase, for Postgres running anywhere · `C:/Users/pc/.claude/plugins/cache/yerel-kurulum7/supabase/0.1.15/skills/supabase-postgres-best-practices/SKILL.md`
<!-- profil-disi:son -->
