---
name: departman-veri-db
description: "Veri/DB müdürü: şema, migration, sorgu ve Supabase/Postgres/EF Core sırası. Tablo, SQL, RLS ya da yavaş sorgu işinde oku."
---

# Departman: veri-db — iş sırası

Katalog: `docs/departmanlar/veri-db.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Katalogda bulunmayan, alan dışı ya da emin olunmayan iş: Skill `yetenek-getir` (3.3k araç, işle ilgili her şey, gruplu).

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
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- supabase (2): supabase, supabase-postgres-best-practices · `C:/Users/pc/.claude/plugins/cache/yerel-kurulum7/supabase/0.1.15/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:db-analitik-sorgu
ajan:db-efcore-sql-gecis
ajan:db-indeks-danismani
ajan:db-migration-planlayici
ajan:db-rls-politika
ajan:db-sema-tasarim
ajan:db-sorgu-optimize
ajan:db-supabase-kurucu
ajan:db-veri-kalitesi
ajan:db-veri-modelleme-nosql
ajan:db-veri-tasima
ajan:db-yedekleme-geri-yukleme
ajan:otm-veri-esleme
kb-retriever: 用于从本地知识库目录检索信息和问答；处理PDF/Excel前先读references，用grep、pdfplumber、pandas渐进检索
### yalnız Claude Code
mcp:airtable: Airtable tablo okuma/yazma
mcp:clickhouse: ClickHouse analitik SQL
mcp:drizzle-docs: Drizzle ORM belgeleri
observability-and-instrumentation: adding logging, metrics, tracing, or alerting
pia-generation: Yeni veri işleme faaliyeti için Türk KVKK pratiğine
qual-quant-triangulation: behavioural data and research findings point different ways
<!-- dizin:son -->
