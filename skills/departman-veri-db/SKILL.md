---
name: departman-veri-db
description: "Veri/DB müdürü: şema, migration, sorgu ve Supabase/Postgres/EF Core sırası. Tablo, SQL, RLS ya da yavaş sorgu işinde oku."
---

# Departman: veri-db — iş sırası

Katalog: `docs/departmanlar/veri-db.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

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


Slash katalog (iş türü → /komut·skill): `yetenek-getir/reference/slash-katalog.md` — Read; oturuma yüklenmez.

Kombo adayları (A/B ölçümü geçmedi; önerme, yalnız ipucu): vb-ef-sorgu-optimizasyon, vb-build-teshis, vb-api-gozlemlenebilirlik, vb-supabase-sorgu.

<!-- dizin:bas -->
## Dizin: adımdaki araç işe uymuyorsa `references/dizin.md` dosyasını oku, listeden adla çağır.
<!-- dizin:son -->
Yeni aileler (SKILL-YUKLE-1, 32): `references/yukle-1-aileler.md` — Read.
