# DERİNLİK-2 ARAŞTIRMA DOĞRULUĞU
KARAR: sıra S1 → S4 → S5 → S6 → S10 → S2 → S3 → S7; S8, S9 → KALAN (DERİNLİK-3). Tavan 45 çağrı, 40'ta commit+push.
S1 kuralı: anahtar kelime (claude|skill|agent|mcp|plugin) her zaman — açıklama, boşsa topics + README ilk 30 satır;
sahip şartı yalnız videoda/karede sahip adı varsa. Sağlanmazsa "olası: <repo> (doğrulanmadı)", araştırmaya girmez.
Kurulu araç: repo kurulum kaydından (installed_plugins + known_marketplaces + marketplace.json), arama yok.
Ömer onayı: test_r3_repo_bulunur sahte gh sonucuna açıklama eklendi (ayrı commit).
Kanıt: docs/kurulumlar/parti/2026-10-03-short/panel.md (ECC→worldflowai, stack→commercialhaskell).
Kabul: kırmızı-önce ayrı commit · eski test değişmez · tam suit (suite-kosucu) · gitleaks · arşiv · push · graphify update.
Model çağrısı 0 · gh istekleri arası ≥2 sn · ~/.claude yalnız okunur.

## Durum
- S1 ✓ (399dcd2 test onayı · 05f009d kırmızı · yeşil) · S4 ✓ (kırmızı + yeşil) · video suite 542 yeşil
- S5 Ömer kararı (uygulanmadı): test_24c.py:115 güncellenir — "tam klon yok" iddiası kalır, beklenen "seyrek tarama (repo 195 MB)";
  seyrek klon (--filter=blob:none --sparse; SKILL.md/hooks/commands/agents) + skillspector serbest; seyrek içerik >20 MB → "atlandı (sebep)";
  atlanan tarama Kapsam'da ✓ değil. Ayrı commit, mesaj: "Ömer onayı: S5, K5'in amacı korunarak".
Tanımlar (asıl tariften, 13a71ece transcript satır 12):
- S6 lisans yalnız gh api repos/<r>/license ya da okunan LICENSE; okunamazsa "bilinmiyor"; "hatırlanan bilgi" türü lisans reddedilir.
- S10 akıl önerisi kurulu aracı kapatma/kaldırma önermez (yükleme yönetimi TOKEN-3 profilleri); ihlal panelde işaretlenir.
- S2 marketplace'ten kurulu plugin: repo + alt yol kayıttan; güncellik o alt yol için. S3 son commit tarihi gh api; Kapsam'da tarih.
- S7 aynı repo ya da ad benzerliği ≥0.8 + aynı video → tek aday (ruflo ×3, ECC ×3 tek satır).
- S5 ✓ (d87de05 kırmızı · a97dc33 K5 onaylı güncelleme · 1a6646b yeşil) · video 545 yeşil; başlangıç 6-suite yeşil (542·81·314·178·40·22)
- S6 ✓ (4e81727 · caafdd9) · S10 ✓ (adaea41 · 43c64fa) · S2+S3 ✓ (2fb4146 · 1f0ce33) · video 550 yeşil · gitleaks temiz · push
  S6 notu: servis/ürün lisans API'sine gitmez (test_r3 u.n==[2]); API okunamazsa form lisansı, yalnız lisans_kaynak='hatırlanan bilgi' → bilinmiyor.
  S3 notu: sürüm (version) ile kurulu plugin'de tarih yok — yalnız sha yolunda commits çağrısı var.
- S7 ✓ (b8f11e6 · 2833231; bulanık yalnız parantezli adda) · S6b ✓ (35ed471 r3 onaylı · 65befef · c461630) · video 553 yeşil · gitleaks temiz
  SON oturumu: tam suit koşulmadı (boş RAM 4,4 GB, GenshinImpact 4,3 GB) → arşiv bekliyor. S8/S9 tanımı derinlik-3.md'de yok (transcript yasak).
- KAPANIŞ: 6f642e8 S8/S9 tanımları (push edilmedi) · gitleaks temiz (f52ce16..HEAD) · tam suit 553·81·313/314·178·40·22 →
  kırmızı test_bpy_kontrol (tests/test_blender_arac.py:126, kod 2 beklenen 1; DERİNLİK-2 dışı, bpy_kontrol ortamı şüpheli) → arşiv bekliyor.
- BPY-TEST TEŞHİS: tek başına yeşil; test/bpy_kontrol son değişim e52df56 (10-01) → kod değil. Kod 2 = bpy_kontrol.py:31-32 "pyright çıktısı
  çözülemedi" (uv run pyright alt süreci geçici hata; Blender kapalı, 9876 boş, bpy yok). Yeniden tam suit 553·81·314·178·40·22 yeşil → arşiv.
KALAN (eski): S7 · tam 6-suite (suite-kosucu; 45 tavanında koşulmadı) · arşiv (dalga-arsiv/DERİNLİK-2.md) · S8, S9 → docs/video-tarama/derinlik-3.md
