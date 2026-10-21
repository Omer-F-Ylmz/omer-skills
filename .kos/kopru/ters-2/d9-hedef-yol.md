# TERS-2 d9 — hedef yolları (KESİNLEŞMEDİ: ground truth yazılmadı, koşu yok)

Koşucu hazır: `kapi_kos.py --hedef <json> --kok <dizin>` (sonuç `sonuc-<ad>.json/md` hedef dosyasının yanına), hedefte `rea_yol` (tek dosyalık js için dizin), kapı = eski eşik YA DA fark gürültü içinde ve skill ≥ zemin − sapma. 8 test yeşil.

## js 5 (REA yalnız dizin kabul eder → her biri için .kos/kopru/ters-2/d9-js/<ad>/ içine tek dosya kopyası = rea_yol; kopyalama yapılmadı, yalnız t1/cortex.ts denendi, REA ts'i okudu)
1. C:/Projeler/uygulamalar/openmontage/ink-theater/ink-theater.js (15.8K)
2. C:/Projeler/uygulamalar/colibri/web/src/lib/cortex.ts (9.6K)
3. C:/Projeler/uygulamalar/colibri/web/src/lib/images.ts (5.2K)
4. C:/Projeler/uygulamalar/colibri/web/src/lib/transcript.ts (2.3K)
5. C:/Projeler/uygulamalar/thinking-orbs/src/presets.ts (3.4K)

## .NET 4 (openclaw yok → FalArsenal tModLoader ister, service-template eksik tip ister: ikisi elendi)
1. templates/jev-dotnet/Jev/bin/Debug/net10.0/Jev.dll (GT taslağı d7-aday.md)
2. templates/jev-dotnet/Jev.Tests/bin/Debug/net10.0/Jev.Tests.dll
3. .kos/kopru/ters-2/d9-dn/nativeaot/bin/Debug/net8.0/NativeAotFixture.dll (rea/tests/fixtures/nativeaot kopyası, PublishAot kapalı dotnet build ile üretildi, 5K; kaynak 39 satır Program.cs)
4. ADAY: templates/jev-dotnet/Jev.Tests/bin/Debug/net10.0/Microsoft.Extensions.Options.ConfigurationExtensions.dll (22K, MIT; üçüncü taraf → yazarın ön bilgisi iki kolda eşit)

## site 3 (`--kok skills`, sayfa = /animasyon-atolyesi/tarifler/<ad>.html; testli)
giris-scroll.html (scroll-timeline), sayfa-gecisi.html (view-transition), parcacik-three.html (CDN three 0.186.1 — ağ gerekir, düz referans/yüklenme DENENMEDİ). Üçü için kare-0/50/100 düzlük probu henüz koşulmadı.

## Kalan (d10): GT 12×5 (ücretsiz taslak → Read), düz-referans probu, sonra d8 koşusu (yazar 56/hakem 80/Haiku ≤20; ≥25 çağrı + 15 tur ayır).

## d10 sonucu
hedef-d9.json: 11 hedef × 5 madde (alıntılar betikle birebir doğrulandı; 8 kod + 3 site, düz referans yok). REA 8/8 kanıt üretti. Koşu (Haiku tek hakem ≤20): skill 0.693 · zemin 0.708 · fark −0.015 GA95 [−0.048,+0.023] · sapma 0.035 · parcacik-three Haiku tavanı bitince atlandı (2 tekrar) → kapı kodu GEÇMEDİ (atlanan≠0); 10 hedefte "kötü değil" kuralı sağlanıyor. Sınıf: site +0.05, js −0.03, dotnet −0.03.
