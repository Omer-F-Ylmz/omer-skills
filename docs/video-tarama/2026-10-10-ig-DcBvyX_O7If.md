# How I made an arm fall apart 👇🏼
## Künye
How I made an arm fall apart 👇🏼 · vfx.by.adrian · süre: 0:33 · ? · https://www.instagram.com/reel/DcBvyX_O7If/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short · claude-sonnet-5-5 · hafif claude -p
kareler: yok
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 9876 tk · claude-haiku-5-5: claude-haiku-5-5 · 13112 tk
## Özet
Houdini ile bir kolun parçalanması efektinin dökümü. Altyazı, kare, açıklama bağlantısı ve yorum yok. Tek kaynak açıklama metni. Akış: büyüme haritaları, Vellum simülasyonu, deri kırılması, birden çok Pyro geçişi, hacimden POP simülasyonu, döküntü yayıcı, Nuke'ta kompozit ve Karma XPU ile render. Kırılma rastgele gürültüyle değil, Growth Curves ile yönlendiriliyor.
## Bölümler
- yok
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Houdini | yok | CLI | yok | Efektin üretildiği 3B/VFX yazılımı. Açıklamada yalnız #houdini ve #houdinifx etiketleriyle anılıyor. | açıklama | #houdini #vfxbreakdown #vfx #houdinifx #3d |
| Growth Maps | yok | teknik | yok | Kırılma ve büyüme davranışını yönlendiren harita tabanlı ilk adım. | açıklama | Growth Maps → Vellum sim → Skin fracturing |
| Growth Curves | yok | teknik | yok | Deri kırılmasını rastgele gürültü yerine eğrilerle yönlendiren teknik. | açıklama | driven by Growth Curves, so the skin breaks where it should |
| Vellum | yok | teknik | yok | Houdini'de kumaş/yumuşak cisim benzeri simülasyon; burada deri için kullanılmış. | açıklama | Growth Maps → Vellum sim → Skin fracturing |
| Pyro | yok | teknik | yok | Duman/ateş benzeri hacim efekti; birden çok geçiş halinde üretilmiş. | açıklama | Multible Pyro passes → POP Sims from Volume |
| POP Sims | yok | teknik | yok | Hacimden üretilen parçacık simülasyonları. | açıklama | POP Sims from Volume → Debris Emitter |
| Nuke | yok | CLI | yok | Son kompozit için kullanılan yazılım. | açıklama | Debris Emitter → Comp in Nuke. |
| Karma XPU | yok | teknik | yok | Sahnenin render edildiği Houdini render motoru. | açıklama | Rendered in Karma XPU. |
| Debris Emitter | yok | teknik | yok | Kırılan parçalardan enkaz (debris) üreten emitter kurulumu. | açıklama | Debris Emitter |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Kırılma rastgele gürültüyle değil Growth Curves ile yönlendiriliyor; deri çözücünün keyfine göre değil olması gereken yerden kopuyor. | açıklama | özellik |
| Efekt sırası: Growth Maps, Vellum, deri kırılması, Pyro geçişleri, POP, döküntü yayıcı, Nuke kompozit. | açıklama | özellik |
| Final Karma XPU ile render edildi. | açıklama | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| açıklama | Growth Maps | Growth Maps | Growth Maps → Vellum sim |
| açıklama | Vellum sim | Vellum | Growth Maps → Vellum sim → Skin fracturing |
| açıklama | Skin fracturing | aday değil: genel kavram | Vellum sim → Skin fracturing → Multible Pyro passes |
| açıklama | Multiple Pyro passes | Pyro | Skin fracturing → Multible Pyro passes |
| açıklama | POP Sims from Volume | POP Sims | Multible Pyro passes → POP Sims from Volume |
| açıklama | Debris Emitter | aday değil: başka adayın parçası (POP Sims) | POP Sims from Volume → Debris Emitter |
| açıklama | Comp in Nuke | Nuke | Debris Emitter → Comp in Nuke. |
| açıklama | Karma XPU | Karma XPU | Rendered in Karma XPU. |
| açıklama | Growth Curves | Growth Curves | driven by Growth Curves, so the skin breaks |
| açıklama | #houdini ve #houdinifx etiketleri | Houdini | #houdini #vfxbreakdown #vfx #houdinifx #3d |
| açıklama | #vfxbreakdown, #vfx, #3d etiketleri | aday değil: genel kavram | #houdini #vfxbreakdown #vfx #houdinifx #3d |
| yorum | Yorumlar | aday değil: konu dışı | Yorumlar girişsiz alınamıyor |
## Kareden okunanlar
- yok
## Belirsizlikler
- Video görüntüsü, ses ve altyazı yok; her şey yalnız açıklama metnine dayanıyor.
- Yorumlar girişsiz alınamadı.
- Houdini adı yalnız hashtag olarak geçiyor; kullanıldığı açıklamadan çıkarıldı.
- Growth Maps ve Growth Curves'ün Houdini'de hangi node ya da araç olduğu belli değil.
- Reel'in kendi URL'si açıklamada geçmediği için urller'e yazılmadı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Büyüme haritalarını (Growth Maps) hazırla — araçlar: Houdini, Growth Maps
- 2. adım — Kırılma yönünü Growth Curves ile belirle — araçlar: Houdini, Growth Curves
- 3. adım — Deri için Vellum simülasyonunu çalıştır — araçlar: Houdini, Vellum
- 4. adım — Deriyi kırıp parçala — araçlar: Houdini, Vellum
- 5. adım — Birden çok Pyro geçişi üret — araçlar: Houdini, Pyro
- 6. adım — Hacimden POP simülasyonları oluştur — araçlar: Houdini, POP Sims
- 7. adım — Döküntü yayıcıyı ekle — araçlar: Houdini, POP Sims
- 8. adım — Sahneyi render et — araçlar: Karma XPU, Houdini
- 9. adım — Geçişleri kompozit et — araçlar: Nuke
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
