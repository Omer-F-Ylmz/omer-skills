---
name: departman-belge
description: "Belge müdürü: docx/pptx/pdf/xlsx, rapor ve doküman üretim sırası. Sunum, PDF, proje dokümantasyonu ya da metin düzeltme işinde oku."
---

# Departman: belge — iş sırası

Katalog: `docs/departmanlar/belge.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

## Adımlar
1. **Tür** — proje dokümanı `document-generate` / `project-documenter`; karar kaydı `documentation-and-adrs`; ortak yazım `doc-coauthoring`.
2. **Biçim** — markdown → PDF `make-pdf`; diyagram `diagram`; sunum `wowerpoint`.
3. **Dil** — AI izi temizliği `humanizer`, yazım kılavuzu `writing-guidelines`.
4. **Yayın sonrası** — `document-release`.
5. **Girdi dönüşümü** — PDF/docx/pptx/xlsx'ten metin gerekiyorsa `markitdown <dosya> -o <dosya>.md`; süreç yetkisiyle okur, güvenilmeyen dosyayı temizlemeden verme. Yazım denetimi `writing-guidelines`: kuralları her seferinde kaynak URL'den çeker (WebFetch), dosya verilmezse hangi dosyaların bakılacağını sorar. Kaynak: `docs/ogren/g3.md`.

## Kapılar
- Belge koddan türetilir; kodla çelişen iddia yazılmaz.
- Talimat metni STE ölçüsüyle: cümle ≤20 kelime, etken çatı, kelime başına tek anlam, adım başına tek eylem (IG-40 DeXJQ-kGKUY).
- Biçim/sunum/Artifact seçimi ve iş sırası: `docs/atlas/belge-sunum.md` (ATLAS kararları `docs/atlas/kart.jsonl`).

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- phoenix-docs-research (3): notebooklm, phoenix-research-pipeline, project-documenter · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-docs-research/1.0.0/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->


Slash katalog (iş türü → /komut·skill): `yetenek-getir/reference/slash-katalog.md` — Read; oturuma yüklenmez.

<!-- dizin:bas -->
## Dizin: adımdaki araç işe uymuyorsa `references/dizin.md` dosyasını oku, listeden adla çağır.
<!-- dizin:son -->
