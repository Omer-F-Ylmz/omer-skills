# claude.ai skill yükleme rehberi · 2026-09-17
Kaynak: support.claude.com/en/articles/12512198 · platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Zip'ler `dist/` altında (gitignore'da).

## Önkoşul
1. Settings → Capabilities → "Code execution and file creation" açık (custom skill için zorunlu; Pro/Max/Team/Enterprise).
2. Zip yapısı `<ad>.zip → <ad>/SKILL.md`, klasör adı frontmatter `name` ile aynı (5 zip'te kontrol edildi). SKILL.md'nin zip kökünde olması dokümanda "yanlış yapı".

## Yükleme: Customize → Skills (claude.ai/customize/skills) → Add → zip yükle; sıra
1. `frontend-craft.zip` — UI işlerinin disiplin skill'i.
2. `ui-ux-pro-max-claudeai.zip` — tüm data/ + scripts/ (Python) dahil.
3. `impeccable-claudeai.zip` — SKILL.md + reference/ + LICENSE + NOTICE.md (Apache-2.0).
4. `sdp-claudeai.zip`, `surec-claudeai.zip` — Divisima tarifleri için.
5. `understand-*.zip` (9 adet, Understand-Anything 2.9.7, MIT; LICENSE içinde) — yalnız skill dosyaları; `/understand` pipeline'ı agents/ ve derlenmiş çekirdek paketini ister, zip'te yoktur → claude.ai'de pipeline çalışmaz, CC'de kullanılır.
frontend-design yüklenmez: anthropics/skills'te var, claude.ai Directory'den eklenir.

## Açıklama sınırı
- claude.ai açıklama sınırı 200 karakter (platform dokümanı 1024 der). Zip'lerde: frontend-craft 195 (kaynakta, 1.5.1) · ui-ux-pro-max 185 · impeccable 192 (bu ikisi yalnız zip kopyasında; kaynak 495/895) · sdp 94 · surec 105 · understand 236 · understand-figma 258 · understand-domain 215 (kısaltılmadı, >200 yükleme reddedebilir).

## claude.ai'de çalışmayacak parçalar
- frontend-craft: `screenshot.mjs`, `audit.mjs`, `olc-renk.mjs` puppeteer ister (sandbox'ta tarayıcı belgelenmemiş, npm ağ ayarına bağlı); `serve.mjs` localhost:3000 açar, sandbox dışından görülmez. 3 genişlik screenshot döngüsü ve audit PASS kabulü yapılamaz.
- impeccable: scripts/ pakette yok → adım 1 `scripts/impeccable context` CLI'ı ve `live` modu çalışmaz; komut tablosundaki reference/ dosyaları okunabilir.
- ui-ux-pro-max: komutlar `~/.claude/skills/ui-ux-pro-max/scripts/search.py` yolunu verir; claude.ai'de skill başka dizinde, yol düzeltilerek çalıştırılır.
- surec: `dotnet build/test/format/run`, `git checkout`, `ci-izle.py` Divisima reposu + yerel araç ister; yalnız süreç metni işe yarar. sdp: `git diff` adımı aynı.
- sdp/surec'teki proje yolu referansları olduğu gibi bırakıldı.
- Yeni klonlar `git clone -c core.autocrlf=false <url>` ile alınır; sistem gitconfig autocrlf=true bash script'lerini CRLF yapar, claude.ai sandbox'ında (Linux) `bash -n` kırılır.

## LINK27 paketleri (27 Eki 21:20, D1)
- `dist/link27-paket/link27-paket.zip` (40 dosya, 69 KB): parsel-video · roast-room · blender-uretim (Hunyuan3D metin→3D bölümü dahil) · reel-kinetik · teach · archify-review · claude-to-deerflow. Aile paketi: tek kayıt, alt skill'ler `skills/<ad>/TALIMAT.md` (1000 skill kaydı sınırı için 7 skill = 1 kayıt).
- `dist/link27-archify/archify.zip` (13 dosya, 2,4 MB): archify (büyük mod; `.venv`/node_modules/mp4 hariç tutuldu).
- `zip_denetle.py`: TEMİZ (2 zip). Yükleme Ömer'in elinde (claude.ai → Skills → Upload).
- Çalışmayanlar claude.ai'de: roast-room persona ajanları CC alt ajanıdır (claude.ai'de yalnız metin); blender-uretim araçları (`uret.py`, `varlik_temizle.py`) yerel/CC; reel-kinetik render'ı Node+Chrome+SAPI ister; claude-to-deerflow DeerFlow servisi ister.
- BEKLİYOR: chief-of-staff / strategic-partner skill'i bu makinede `~/.claude/skills` altında yok (plugin olarak kurulu olabilir), paketlenmedi. OpenMontage `om-` skill'leri paketlenmedi: OpenMontage AGPL-3.0, zip'e koymak lisans metni + kaynak yükümlülüğü getirir; Ömer onayı bekleniyor.
- Aile paketi eklemek için: `python tools/skill-paket/ekle.py [--uzerine] dist/link27-paket/link27-paket.zip <çıktı> <skill_dizini>...`

## OpenMontage paketi (27 Eki 21:40, D1-OM)
- `dist/link27-openmontage/openmontage-paket.zip`: 49 skill (`om-` önekliler dahil), 81 zip girdisi, 769 KB. Tek kayıt; 200 dosya sınırının altında, 10 MB'ın çok altında, bölmeye gerek kalmadı.
- Aile yapısı: `paketle.py --buyuk` ile; metin dosyaları skill başına `REFERANS.md`/`KAYNAK-n.md` içinde birleşik (içerik atılmadı), alt skill girişleri `skills/<ad>/TALIMAT.md`.
- `zip_denetle.py`: 1 uyarı — `om-remotion-best-practices/REFERANS.md` içinde U+2060 (WORD JOINER), kaynakta da var (`rules/maps.md`, mapbox stil URL'si içinde). Kaynak değiştirilmedi; kopyalanan kodda bu karakter URL'yi bozar, kaynağın düzeltilmesi ayrı iş.
- Kaynakta png/jpg/webp/mp4/mov yok (sayım 0); hiçbir dosya hariç tutulmadı. Kaynak yolu `araclar/link27/calesthio__OpenMontage/.claude/skills/`.
- Lisans: OpenMontage AGPL-3.0. Ömer iç kullanım onayladı; zip içinde lisans metni yok (pakette lisans dosyası yeri yok). Dışarı dağıtımda AGPL yükümlülükleri (kaynak açma) geçerli olur.


## Kalıcı düzen: aile paketi (KARAR-30 m1, 30 Eki)
- claude.ai kayıt tavanı 1000. Yeni gelen skill tek başına yüklenmez: mevcut aile paketine eklenir, paket yeniden üretilir, claude.ai'de "Upload and replace" ile DEĞİŞTİRİLİR (yeni kayıt açılmaz).
- Ekleme: `python tools/skill-paket/ekle.py [--uzerine] <mevcut-paket.zip> <çıktı.zip> <skill_dizini>...`; yeni aile için `tools/skill-paket/paketle.py` (`--buyuk`); eksik envanterden toplu üretim `tools/skill-paket/yukle23_uret.py`. Her zip `tools/skill-paket/zip_denetle.py` ile TEMİZ olmalı.
- Silme yok: tekil kayıt + paket içi kopya (fark listesi b: `dist/paket-2/fark3/b-kopya.tsv`, 82 ad) CC tarafında silinmez; Ömer paketi yükleyince tekil kaydı kendisi kaldırır ya da bırakır. Kayıt sayısı kararı Ömer'in UI sayısıyla verilir (sayaç yerel değil).
- Yükleme sırası ve zip listesi her turda rapora yazılır (Ömer elle yükler).
