---
name: departman-belge
description: "Belge müdürü: docx/pptx/pdf/xlsx, rapor ve doküman üretim sırası. Sunum, PDF, proje dokümantasyonu ya da metin düzeltme işinde oku."
---

# Departman: belge — iş sırası

Katalog: `docs/departmanlar/belge.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

Skill dizini: bu klasördeki `dizin.md` — alandaki TÜM kurulu skill'ler (ad — ne zaman). Adımdaki araç işe tam uymuyorsa dizin.md'de Grep ile işin anahtar kelimesini ara (Read etme), bulunan adı Skill aracıyla çağır; listede yalnız adı görünen skill de çağrılabilir.

## Adımlar
1. **Tür** — proje dokümanı `document-generate` / `project-documenter`; karar kaydı `documentation-and-adrs`; ortak yazım `doc-coauthoring`.
2. **Biçim** — markdown → PDF `make-pdf`; diyagram `diagram`; sunum `wowerpoint`.
3. **Dil** — AI izi temizliği `humanizer`, yazım kılavuzu `writing-guidelines`.
4. **Yayın sonrası** — `document-release`.

## Kapılar
- Belge koddan türetilir; kodla çelişen iddia yazılmaz.

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- phoenix-docs-research (3): notebooklm, phoenix-research-pipeline, project-documenter · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-docs-research/1.0.0/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->
