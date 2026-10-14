# DIST-19 claude.ai zip'leri (fa2750d commit içeriği, git archive; değişiklik tabanı 6acd6bd)

Yükleme: claude.ai → Settings → Capabilities → Skills → aynı adlı skill'in yerine yükle (yetenek-getir yeni).
plan-kur HARİÇ (ENVANTER-3 kör kapı 2× RET). CC'deki departman-* claude.ai senkron kopyasından gelir → bu yükleme CC'yi de günceller.
zip_denetle: TEMİZ 14 zip

- **departman-arastirma-ogrenme** · ID 01CZAK3UC5fg1HqwizEh4okW · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1); TOKEN-12 ajan açıklama onarımı 2 (ara-arac-degerlendirme, ara-repo-karsilastirma; zip'e giren 2) · 25 dosya, 22.7 KB · description 130 kr · TEMİZ
- **departman-backend-dotnet** · ID 01Psv9rXkPXbBJ8kapxJEB2J · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 23 dosya, 18.3 KB · description 115 kr · TEMİZ
- **departman-belge** · ID 01SrhWAeW8Lu5th8mHnmu94d · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 18 dosya, 13.2 KB · description 131 kr · TEMİZ
- **departman-guvenlik** · ID 01JK2Lu5hfQpz5LiALKgpGBS · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 23 dosya, 16.9 KB · description 126 kr · TEMİZ
- **departman-surec-ajan-arac** · ID 01AF1LNfpQdrjfGHj74bHVQ7 · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 23 dosya, 18.8 KB · description 115 kr · TEMİZ
- **departman-surec-git-yayin** · ID 01H7z8utXE1GMfeCZiNooyjb · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 10 dosya, 9.0 KB · description 116 kr · TEMİZ
- **departman-surec-inceleme** · ID 011gD4KdpyVKRDJkbwCaqnxt · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 9 dosya, 8.0 KB · description 101 kr · TEMİZ
- **departman-surec-plan** · ID 01HB9k9eaPDHk4gU7vFsfzsk · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 17 dosya, 12.5 KB · description 100 kr · TEMİZ
- **departman-test-qa** · ID 011YWGaXHF3BMtAFg16A6cY2 · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 17 dosya, 14.2 KB · description 131 kr · TEMİZ
- **departman-veri-db** · ID 012npkZd1AbuwbrcxkahhqpM · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 15 dosya, 9.9 KB · description 121 kr · TEMİZ
- **departman-verimlilik** · ID 018Kpf8nP4rjacdZjDhH28WV · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 11 dosya, 8.5 KB · description 134 kr · TEMİZ
- **departman-frontend** · ID skill_01CHBvYpGKTyed5UPh3usNUp · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 45 dosya, 37.4 KB · description 125 kr · TEMİZ
- **departman-diger** · ID skill_01VFvgDetg9eeeWf7UHKqoak · SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1) · 124 dosya, 108.8 KB · description 184 kr · TEMİZ
- **yetenek-getir** · ID bilinmiyor (verilmedi) → claude.ai'de yoksa YENİ YÜKLEME · ARA SÜRÜM (ENVANTER-4 tarif/kılavuz ekleyecek) — yeni skill: katalog_ara + yetenek.jsonl/tsv + ogrenim.jsonl (öğrenim kataloğu); docs/katalog/ek.jsonl adayları yetenek.jsonl içinde (130/130) · 5 dosya, 615.8 KB · description 254 kr · TEMİZ

## CC canlı tarafı (yalnız --kuru koşuldu; uygula KOŞULMADI)
- departman-* (13): CC claude.ai senkron kopyasını görür → yukarıdaki yükleme CC'yi de günceller; ayrı onay betiği yok.
- yetenek-getir → `onay/envanter_2_uygula.py --kuru`: ~/.claude/skills/yetenek-getir ← 5 dosya (SKILL.md, katalog_ara.py, ogrenim.jsonl, yetenek.jsonl/tsv) · mevcut yok · yazmadı. Önerilen yol bu (yalnız skill kurar).
- `onay/envanter_3_uygula.py --kuru`: plan-kur + yetenek-getir kurar + global CLAUDE.md +1 KOŞULLU satır (51 jeton, ~981/1300). DİKKAT: plan-kur kapı RET → bu betik uygulanmamalı (ya da plan-kur'suz düzeltilmeli). --kuru izli dist/envanter-3'ü yeniden yazıyor (DIST-19'da git checkout ile geri alındı).
- `onay/katalog_kanca_uygula.py --kuru`: yetenek-getir + katalog_kanca.py kurar ve settings.json UserPromptSubmit'e kanca ekler. DİKKAT: karar "kanca kurulmaz" (14 Eki 03:25) → uygulanmamalı.
- `onay/token_12_uygula.py --kuru`: değişecek 0 · bulunmayan 0 → arastirma ajan açıklama onarımı (ara-arac-degerlendirme/ara-repo-karsilastirma) canlıda zaten var.
