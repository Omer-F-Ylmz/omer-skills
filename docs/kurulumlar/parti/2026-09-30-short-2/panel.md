# Karar paneli — 2026-09-30-short-2

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| figma | CLI | 2 | — | koşmadı: kurulu | ZATEN VAR | kurulu: figma · alt tür çakışması (kurulu > ürün) | ZATEN VAR |
| blender | CLI | 2 | GPL-3.0-or-later | atlandı (repo 1333 MB) | SOR | eksik: son_commit | AL |
| codex-sesli-sohbet-gpt-6-astra | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| image-generation-skill | skill | 1 | bilinmiyor | koşmadı: repo yok | SOR | eksik: lisans, son_commit | ERTELE |
| blender-ile-codex | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| web-sitesine-3d-model-entegrasyonu | teknik | 1 | — | koşmadı: ürün | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| hero-bolumu-icin-alti-mock-up-uretmek | prompt | 1 | — | koşmadı: ürün | ÖĞREN | prompt: kurulabilir araç değil | ZATEN VAR |
| remotion | skill | 1 | bilinmiyor (SPDX değil: özel "Remotion License"; LICENSE.md; bazı durumlarda şirket lisansı gerekir) | atlandı (repo 4257 MB) | SOR | eksik: son_commit | ERTELE |
| sub-agent-lar-ile-baglam-temizligi | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| claude-md-de-sub-agent-tercihleri-ve-exe | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| agent-view | CLI | 1 | yok | koşmadı: ürün | SOR | ürün: kurulum gereği · bizde karşılığı | ÖĞREN |
| strix | CLI | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: strix | ZATEN VAR |
| obsidian-ikinci-beyin-notlari | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |

## form_red
- yok
## Eksik alanlar
- yok
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- blender: hedef_tur: skill tarif: 'blender-headless' adında bir skill yaz. Kullanıcı isteğinden bpy betiği üretsin (küp, Array modifier, Simple Deform, metin nesnesi). Sonra `blender -b -P betik.py -- --render-output ... -f 1` ile çalıştırıp çıktı görüntüsünü döndürsün. Blender yolunu ve sürümünü ortam değişkeninden okusun. Bu tarif denenmedi.
- image-generation-skill: hedef_tur: skill tarif: SKILL.md yaz: (1) tetikleyici: 'mock-up/hero görseli üret'; (2) girdi: sayfa amacı, marka/renk, stil, adet N; (3) her varyasyon için farklı istem üretip kullanıcının seçtiği görsel API'sini (anahtar ortam değişkeninden okunur, dosyaya yazılmaz) çağıran küçük bir script (scripts/generate.py); (4) çıktıları mockups/hero-01..N.png olarak kaydet ve index.md ile istemleri listele; (5) maliyet uyarısı ve adet üst sınırı ekle.
- remotion: hedef_tur: skill tarif: Remotion'un kendisi yeniden yazılmaz. Onun üzerine ince bir skill yazılır: SKILL.md içinde npx create-video ile proje iskelesi, kompozisyon ve animasyon kalıpları (interpolate, spring, Sequence), remotion render komutu ve markaya özel şablon kuralları anlatılır. Resmi Agent Skills içeriği referans alınır. Lisans şartı kontrol edilmelidir.
## Kural önerileri (T0)
- codex-sesli-sohbet-gpt-6-astra: Codex'te sesli sohbetle mock-up, 3D model, site ve deploy adımlarının klavyesiz yapılması
- blender-ile-codex: Codex referans görselden Blender'da 3D model üretir
- sub-agent-lar-ile-baglam-temizligi: Görevleri sub-agent'lara verip sonuçları ana oturuma geri almak.
- claude-md-de-sub-agent-tercihleri-ve-exe: claude.md içinde paralel/sıralı tercihleri; Claude soruya göre öneri sunar.
- obsidian-ikinci-beyin-notlari: Kişisel bilgi ve standartları notlarda tutup AI'ın bunlara bakarak çalışması.
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- yok
## Araştırılmadı
- yok
## Site/UI teknikleri
- Figma çerçeve/panel düzeni · eKnpRVgqXR8 · 0:00 (altyazı) → docs/departmanlar/frontend.md
- Blender 3B metin (extrude), eğri + Array + Simple Deform, ışık/kamera/render · eKnpRVgqXR8 · 1:02 (kare) → docs/departmanlar/frontend.md
- Figma çerçeve + Blender node materyalleri · 9opJeH9j9qs · 0:47 (kare) → docs/departmanlar/frontend.md
- 3D model, fare hareketine duyarlılık ve kaydırma animasyonları · -_S3KD0ZIfI · 0:30 (altyazı) → docs/departmanlar/frontend.md
## Anatomi bekliyor
- yok
## Geliştirme önerileri
- figma · video: Figma'da koyu gri çerçeve hazırlanıp çerçeve rengi değiştiriliyor (eKnpRVgqXR8 0:00, 9opJeH9j9qs 0:09); arayüz tasarımı ilk aşama, ardından Blender'da ikinci aşama. Videoda MCP kullanımı görünmüyor, elle arayüz işi. · bizde: Figma MCP kurulu (frontend departmanı, açıklama boş, p=1.0, kaynak jev). · fark: Videoda Figma elle kullanılan bir tasarım aracı olarak geçiyor. MCP, Figma'nın bizdeki kullanım biçimini aşıyor ve videodan bizde olmayan bir yan çıkmıyor. Figma→Blender aşamalı iş akışı bizde tanımlı değil, ama videoda buna dair araç ya da yapılandırma ayrıntısı yok. · yok: Değişiklik önerilmiyor. İstenirse figma kaydının boş açıklaması doldurulabilir, ancak bu videodan gelen bir gelişme değil. · kanıt: 
- strix · video: Ücretsiz, açık kaynaklı güvenlik aracı; yapay zeka ajanlarıyla uygulamaya saldırıp açığı kanıtlıyor (40KWXNxzgPA 0:07). Karede rate limiting yokluğu, açık admin rotası, zayıf parola politikası ve gömülü API anahtarı işaretli. Altyazı adı 'Citrix' diyor, bu büyük olasılıkla yanlış çıkarım. · bizde: strix CLI olarak kurulu (güvenlik departmanı, açıklama boş, p=1.0, kaynak elle). · fark: Videoda bizde olmayan bir kullanım ayrıntısı yok: komut, bayrak, model ya da CI entegrasyonu gösterilmiyor. Yalnızca bulgu kategorileri mockup üzerinde etiketli. Altyazıdaki ad tutarsız ve aracın kimliği videodan doğrulanamıyor. · yok: Değişiklik yok. İleride strix kayıt açıklaması doldurulabilir ya da `video repo` ile deposu incelenebilir. Videodan somut bir yapılandırma çıkmadığı için şimdi işlem gerekmiyor. · kanıt: 
## Defter
12 çağrı · $0.6890 · 150405 jeton
