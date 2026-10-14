# DIST-20 claude.ai (BİRLEŞTİR-20, main e05750a blob'larından)

Yükleme: claude.ai → Settings → Capabilities → Skills → yetenek-getir'in yerine yükle (replace). Canlı kurulum Ömer onayıyla.

- **yetenek-getir** · ID skill_01U5JJT1adSTYHbTgVUALfFN · replace · 122 dosya · 1269 KB · zip_denetle: TEMİZ
  içerik: SKILL.md, katalog_ara.py, yetenek.jsonl/tsv, ogrenim.jsonl + tarifler/ (18) + kilavuz/ (98) + derin.tsv (2670)
- YG-ZIP-FIX: ilk zip claude.ai'de "exactly one SKILL.md, currently 2" ile reddedildi (kilavuz/skill.md, harf duyarsız eşleşme);
  dosya kilavuz/skill-aile.md oldu, zip YG-ZIP-FIX ağacından yeniden üretildi, zip_denetle artık SKILL.md'yi harf duyarsız sayar
- CC: `python onay/envanter_4_uygula.py --kuru` temiz (uygula Ömer onayıyla)
