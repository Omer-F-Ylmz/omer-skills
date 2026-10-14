# Oyun modu — birleşim tarifi
Ne zaman: Bozuk 3DMigoto modu onarımı, yeni mod, Lua betiği ya da model/doku aktarımı.

## Fazlar
1. Keşif: `universal-modder:game-recon` — motoru ve modlama yolunu bulur, MODDING_PLAN.md üretir · birlikte: `universal-modder:game-research-websearch` önceki mod çalışmalarını ve ölü bağlantıları arar.
2. Güvenlik: `oyn-mod-guvenlik-kontrol` — indirilen modda şüpheli betik, çalıştırılabilir ve DLL arar.
3. Onarım (3DMigoto): `mod-atolyesi` — Genshin/ZZZ/HSR/WuWa için bozuk mod, ini, hash/slot, yeşil doku · birlikte: `oyn-mod-onarim` güncelleme sonrası ini, hash ve logdan teşhis.
4. Model ve doku: `bl-mod-modeli-blender` — Blender ile oyun formatı arasında ölçek, kemik, vertex group · birlikte: `blender:blender-uretim` Blender üretim hattı.
5. Betik ve birleştirme: `oyn-lua-betik` — mod için hızlı Lua · birlikte: çakışan modlar için `oyn-mod-birlestirici` hash ve slot yeniden eşler.
6. Oyunda doğrulama: `universal-modder:game-automation` — modu oyunda doğrular, tekrar edilebilir test sahnesi kurar.
7. Paketleme: `oyn-mod-paketleme` — klasör düzeni, readme, sürüm notu · birlikte: `universal-modder:share-field-notes` öğrenileni not eder.

## İnceleme ajanları
- `oyn-mod-guvenlik-kontrol`: paylaşım öncesi ikinci tarama.
- `universal-modder:reverse-engineering`: oyun iç yapısı gerektiğinde.

## Güvenlik ve kalite kapıları
- İndirilen her mod `oyn-mod-guvenlik-kontrol`'den geçer.
- Oyunda görsel doğrulama yapıldı; yalnız ini değişikliği yetmez.
- Paylaşılan pakette kişisel yol ya da sır yok: `gitleaks`.

## Tartışma konseyi
- Karar: onarım mı baştan yapım mı; hangi mod yöneticisi (standalone/XXMI).
- `ecc:council` — varsayılan Claude personaları: modcu, oyuncu, güvenlik.

## Jeton bütçesi
- Keşif: orta (~12k, tahmini); forum ve log okuması `okuyucu` alt ajanına. Güvenlik: küçük (~4k). Onarım: orta (~15k). Model: büyük (~30k). Betik: orta (~10k). Doğrulama: orta (~10k). Paketleme: küçük (~4k). Hepsi tahmini.

## Kaçınılacaklar
- Taranmamış modu çalıştırmak.
- `oyun-mod-paket` ile tekil universal-modder:* skill'lerini aynı anda yüklemek.
- `blender-uretim` ile `blender:blender-uretim` kopyasını birlikte yüklemek.

## Aday (kurulu değil)
yok
