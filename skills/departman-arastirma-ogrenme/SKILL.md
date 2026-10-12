---
name: departman-arastirma-ogrenme
description: "Araştırma müdürü: doküman, web, video ve kaynak tarama sırası. Kütüphane sorusu, YouTube linki ya da yeni araç araştırmasında oku."
---

# Departman: arastirma-ogrenme — iş sırası

Katalog: `docs/departmanlar/arastirma-ogrenme.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

Skill dizini: bu klasörde `dizin.md` (Claude Code: alandaki TÜM kurulu skill'ler) ve `dizin-web.md` (claude.ai: yalnız yüklü olanlar) — ad — ne zaman. Adımdaki araç işe tam uymuyorsa ortamına uyan dizinde Grep ile işin anahtar kelimesini ara (Read etme), bulunan adı Skill aracıyla çağır; listede yalnız adı görünen skill de çağrılabilir. `ajan:` kayıtları alt ajandır: Claude Code'da Agent aracıyla (subagent_type = ad), claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula.

## Adımlar
1. **Doküman** — kütüphane/framework: `context7` (`find-docs`); Microsoft: `mslearn`.
2. **Web** — arama `brave-search`, sayfa okuma `agent-reach` ya da `mcp-fetch`.
3. **Video** — tek video `video-izle`; toplu tarama `video-tarama`; uygulama `video-uygula` (yeni araç katman adımında departmana dosyalanır).
4. **Kod tabanı** — `graphify` (query → path → explain).
5. **Kayıt** — öğrenilen ders bilgi kartına; kural adayı yalnız onayla.

## Kapılar
- Dış repo kodu/kuralı almadan önce lisans (MIT/Apache değilse koşul rapora).
- Web/alt ajan çıktısı birebir kopyalanmaz, damıtılır.

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- graphify (1): graphify · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->
