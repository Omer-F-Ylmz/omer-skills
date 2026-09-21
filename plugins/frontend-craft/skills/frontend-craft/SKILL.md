---
name: frontend-craft
description: Web arayüzü (landing, vitrin, panel) tasarım-uygulama disiplini — marka kararı, referans eşleme, 3 genişlikte screenshot, yasak liste, a11y/perf kabulü. HTML/CSS/Tailwind/Razor işinde önce yükle.
allowed-tools: Bash(node *) Bash(npm *) Bash(npx *)
---

## ÇEKİRDEK (özet; compaction sonrası da bu blok geçerli, ayrıntı ilgili bölümde)
- Adım 0 · Bağımlılık: `${CLAUDE_SKILL_DIR}/node_modules` yoksa önce `npm ci --ignore-scripts` + `node node_modules/puppeteer/lib/puppeteer/node/cli.js browsers install chrome`; hiçbir script bundan önce koşmaz.
- Mod tespiti (tek satır rapor): `reference/` varsa REF — birebir eşleme, referans kazanır, Bölüm 3 uygulanmaz, hex'ler `olc-renk.mjs` ile ölçülür. Yoksa FREE — koddan önce marka kimliği kararı `ana #hex · nötr #hex · vurgu #hex · display font · sans font · ölçek 8px` (ana renk mor/indigo/menekşe olamaz), Bölüm 3 zorunlu. `*.csproj` + `Views/`|`Pages/` → aspnet, değilse static.
- SIRA (yeni proje / yeni ana ekran): yön keşfi (Bölüm 11: üç yön, künye + 1440 PNG, DUR, kullanıcı seçer) → DESIGN.md (Bölüm 7: göster, DUR) → iki-pass (Bölüm 8: token planı → yasak listesine karşı eleştiri → inşa) → kod → screenshot döngüsü (Bölüm 2/9). Mevcut DESIGN.md varsa ya da REF modundaysa yön keşfi atlanır.
- Sunucu şart, `file:///` yasak: static `node ${CLAUDE_SKILL_DIR}/scripts/serve.mjs` (:3000) · aspnet `dotnet run --project <web csproj>`.
- Screenshot döngüsü: `node ${CLAUDE_SKILL_DIR}/scripts/screenshot.mjs <url> [etiket]` → 390/768/1440 PNG, her biri Read ile açılır. Tur = screenshot → sapma tablosu → düzelt; min 2, max 4 tur; 4. tur sonunda sapma kalırsa DUR raporu.
- Kabul: `node ${CLAUDE_SKILL_DIR}/scripts/audit.mjs <url> dev` PASS (FREE'de SLOP boş); ELLE BAKILACAK kalemleri raporda ayrıca yanıtlanır; a11y/perf/etkileşim Bölüm 4.
- UI incelemesinde `references/vercel-web-interface.md` kontrol listesi.
- DESIGN.md tam olarak 6 başlık, fazlası yok:
  1. Stil adı
  2. Token'lar — 3-6 adet `ad: değer`
  3. Renk — 4-6 isimli hex, jenerik ad yok
  4. Tipografi — 2 isimli font + ölçek; Inter, Roboto, Arial, Space Grotesk, Poppins yok
  5. Hareket — süre + easing, en fazla 3 kural (tetikleyici + kütüphane/sürüm/gerekçe)
  6. YASAK LİSTESİ
- Yasak liste özeti (varsayılan; projeninki DESIGN.md'de, seçilen stille çelişen madde çıkar): mor/indigo→mavi gradient · emoji ikon · backdrop-filter blur kart yığını · birebir "h1+p+2 buton" hero · stok illüstrasyon/3D render hissi · özellik/fayda bölümünde eşit kart tekrarı (ürün ızgarası hariç) · her bölümde aynı boşluk · aşırı glow · her yerde ikon · merkezli tek kolon · lorem ipsum · aşırı yuvarlatma · gereksiz shadow.
- Çıktı hedefi: claude.ai/Desktop'ta teslim **Design** artifact türünde, tasarım sistemi gerekiyorsa **Design System** türünde; CC'de mevcut akış değişmez.
- Kütüphane seçimi `omer-kutuphaneler` rafından; CC'de npm, Desktop'ta pinli CDN; DESIGN.md Hareket'te ad+sürüm+gerekçe; gerekçesiz kütüphane yasak.
- Tur raporu (her tur sonu; rapor yazılmadan iş kapanmaz): `Tur N | mod | PNG yolları | sapma tablosu | audit (+SLOP) | KANIT (FREE): ana/nötr/vurgu hangi elemanlarda · font çifti nerede · ölçek hangi bölümlerde | sonraki adım / KAPANIŞ / DUR`

## Adım 0 · Bağımlılık
- `${CLAUDE_SKILL_DIR}/node_modules` yoksa `${CLAUDE_SKILL_DIR}` içinde `npm ci --ignore-scripts` sonra `node node_modules/puppeteer/lib/puppeteer/node/cli.js browsers install chrome` çalıştır. Varsa atla. Bu adım her skill yüklemesinde ilk komuttur, hiçbir script ondan önce koşmaz.

## 0. Mod tespiti (ilk adım, tek satır raporla)
- Tara: `reference/` (png/jpg/pdf) var mı → REF modu; yoksa FREE modu. `brand_assets/` var mı. Proje türü: `*.csproj` + `Views/` veya `Pages/` → aspnet; değilse static.
- `inspiration/` klasörü varsa yön için oku; hiçbir düzeni kopyalama.
- REF: hedef birebir eşleme. Bölüm 3 uygulanmaz; referans her zaman kazanır. Referansta olmayan bölüm/özellik/metin eklenmez, referans "iyileştirilmez".
- Referans hex'leri `node ${CLAUDE_SKILL_DIR}/scripts/olc-renk.mjs <referans.png>` ile ölçülür, elle okunmaz. olc-renk.mjs baskın renkleri ölçer (3-6 adet, pay ≥%0.5); daha az çıkarsa daha az renk vardır, tamamlanmaz.
- Hareketli referans (scroll/hover animasyonu olan site): tek statik PNG yetmez — ekran kaydından kare dizisi ya da aynı öğenin çoklu durum screenshot'ı + "statik değil" notu + davranış dökümü (tetikleyici → ne olur) gerekir; eksikse kullanıcıdan istenir.
- İşten önce var olan sayfaya dokunmadan önce salt-okuma analiz (yapı, bileşenler, animasyonlar) + dokunulmaz alan listesi (ör. hero, mevcut animasyonlar) raporlanır; listedeki alanlara dokunulmaz.
- FREE: koddan önce MARKA KİMLİĞİ KARARI tek satır: `ana #hex · nötr #hex · vurgu #hex · display font · sans font · ölçek 8px`. Ana renk mor/indigo/menekşe olamaz. Sonra Bölüm 3 zorunlu. Kararı vermeden önce `ui-ux-pro-max` varsa `search.py "<sektör> <ürün>" --design-system -p <Proje>` çalıştır, öneriyi aday al; kararı yine tek satır yaz.
- Hedef kitle brief girdisidir: marka kimliği kararından önce yazılır.
- `frontend-design` skill'i listede varsa onu da yükle; yoksa Bölüm 3 onun yerine geçer.

## 1. Sunucu
- static: `node ${CLAUDE_SKILL_DIR}/scripts/serve.mjs` arka planda → http://localhost:3000. Çalışıyorsa ikinci instance açma.
- aspnet: `dotnet run --project <web csproj>` arka planda; URL `Properties/launchSettings.json`'dan.
- `file:///` ile screenshot alınmaz: kök-göreli yollar, fetch ve ES modülleri sunucusuz çalışmaz, ölçülen sayfa gerçek sayfa olmaz.
- UI'a dokunan yeni proje veya yeni ana ekranda sıra — Bölüm 11 (yön keşfi) → DESIGN.md → iki-pass → kod → screenshot döngüsü. Mevcut bir DESIGN.md varsa veya REF modundaysak (`reference/` klasörü var) Bölüm 11 atlanır.

## 2. Screenshot döngüsü
- `node ${CLAUDE_SKILL_DIR}/scripts/screenshot.mjs <url> [etiket]` → `.screens/` altına 390/768/1440 üç PNG. Her PNG'yi Read ile aç ve incele.
- Tur = screenshot → sapma tablosu → düzelt → screenshot. Min 2, max 4 tur.
- Sapma satırı: `genişlik | öğe | ölçülen | beklenen | tolerans dışı?`
- Tolerans: spacing ±2px, font-size ±1px, radius ±1px, hizalama ±2px, renk exact hex, font ailesi/ağırlık exact.
- REF'te beklenen = referans; FREE'de beklenen = Bölüm 0 kararı + Bölüm 3 token'ları.
- Kapanış: 3 genişlikte 0 tolerans-dışı sapma. 4. tur sonunda hâlâ sapma varsa DUR raporu (kalan sapmalar + neden).
- Tüm butonlar/formlar tek bileşen ya da partial'dan gelir; sayfada kopya yok.

## 3. FREE modu guardrail'leri
- Renk: Tailwind default paleti birincil olamaz; tek marka rengi, tint/shade türet, CSS değişkeni.
- `::selection` rengi marka renginden türetilir; tarayıcı varsayılanı kalmaz.
- Tipografi: başlık ≠ gövde ailesi (display/serif + sans). Büyük başlık `letter-spacing:-0.03em`; gövde `line-height:1.7`; 5 kademeli ölçek; h1 belirgin, h2/h3 kademeli.
- Spacing: tek ölçek 8/16/24/32/48/64/96; ölçek dışı değer yok (4px yalnız ince ayar ara değeri olarak kabul); bölümler arası boşluk ölçekten.
- Gölge: düz `shadow-md` yok; katmanlı, marka renginden türetilmiş, düşük opaklık.
- Arka plan bilinçli seçilir: düz zemin + tek radial vignette + yönsüz grain (opaklık ≤0.06) da geçerli bir karardır; katmanlı gradient zorunlu değildir. Zorunlu olan, seçimin DESIGN.md'de yazılı olması.
- Yoğun bölümden (koyu, görsel, video) nötr zemine geçiş bilinçli karardır: geçiş biçimi (sert kesim / gradient / boşluk) DESIGN.md'de yazılır.
- Audit yalnız adında noise/grain geçen ya da feTurbulence kullanan katmanları ölçer; raster grain görseli yakalanmaz, o durumda opaklığı sen beyan et.
- Derinlik: 3 yüzey seviyesi (base → elevated → floating).
- Görsel (logo/ikon hariç): görsel üstü gradient overlay yalnız metin görselin üstüne biniyorsa (overlay'in işi metnin okunması) — o durumda `from-black/60` + `mix-blend-multiply` renk katmanı.
- Animasyon: yalnız `transform`/`opacity`; `transition-all` yasak; easing `cubic-bezier(.22,1,.36,1)`; `prefers-reduced-motion` ile kapanır.
- Kütüphane (GSAP, Three.js, R3F vb.) serbesttir; şart: DESIGN.md Hareket bölümünde ad + sürüm + hangi etkiyi neden karşıladığı yazılı olacak. Gerekçesiz kütüphane yasaktır.
- Interaktif: her `a, button, [role=button], input, select, textarea` için hover + focus-visible + active.
- İkon: tek aile, SVG (Lucide outline); emoji yok.
- Grid: kırık simetri — ≥1 bölüm asimetrik kolon/tam genişlik dışı; her şey ortalı ve eşit genişlik olmaz.
- Yasak (jenerik şablon izi bırakan kalıplar): mor/indigo→mavi gradient · emoji ikon · backdrop-filter blur kart yığını · "h1+p+2 buton" hero kalıbı birebir · stok illüstrasyon/3D render hissi · eşit boyutlu kart tekrarı (özellik/fayda bölümlerinde; ürün ızgarası hariç — orada eşit kart zorunlu, kırık simetri sayfa/başlık düzeyinde aranır) · her bölümde aynı boşluk.
- Bu liste varsayılandır; projenin yasak listesi DESIGN.md'de yazılır ve seçilen stille çelişen maddeler oradan çıkarılır (ör. Glassmorphism seçilen projede blur maddesi geçersiz).

## 4. Her iki modda kabul kriterleri
- `node ${CLAUDE_SKILL_DIR}/scripts/audit.mjs <url> dev` → PASS; FREE modunda SLOP satırı boş.
- Audit'in ELLE BAKILACAK kalemleri tur raporunda ayrıca yanıtlanır; PASS bu kalemleri kapsamaz.
- a11y: `html[lang]`, tek `h1`, `header/main/footer` landmark, her `img` alt+width+height, fold altı `loading="lazy"`, kontrast gövde ≥4.5:1 / büyük başlık ≥3:1 (hex'ten hesapla, çiftleri raporla).
- perf: font ≤2 aile ≤4 dosya, `font-display: swap`, tüm medya boyutlu (CLS 0).
- Performans: ağır 3D/görselde yükleme durumu gösterilir · GLB hedefi ≤2 MB · arka plan videosu mobil ve desktop için ayrı dosya · kabul: animasyon mobil dahil kasmadan akar.
- Etkileşim durum + cihaz başına tarif edilir (hover/focus/active × masaüstü/dokunmatik); hover ya da mouse'a bağlı efektin dokunmatikte karşılığı olur (dokunma durumu ya da kendiliğinden hareket).
- Etkileşim kabulü davranış cümlesiyle yazılır ("menü butonuna tıklanınca panel açılır, Esc kapatır") ve gerçek tarayıcıda tıklanarak doğrulanır. Araç: claude-in-chrome varsa o, yoksa puppeteer; sıra: yükle → keşfet → selector → aksiyon → console kaydı.
- Kırık link 0.
- Dış tasarım aracı (Claude Design, 21st) çıktısı görsel optimizasyon + audit'ten geçmeden teslim edilmez.
- Prod teslim (kullanıcı "prod"/"yayın" dediğinde): Tailwind CDN kaldırılır → `npx @tailwindcss/cli -i src/input.css -o wwwroot/css/site.css --minify`; `audit.mjs <url> prod` PASS.
- Prod teslimde ayrıca: sayfa başına `title` + meta description · favicon · manifest · `robots.txt` · `sitemap.xml` · footer'da KVKK/gizlilik + çerez onayı · kullanıcı hesabı olan sitelerde footer'da "hesabımı sil" (KVKK). REF'te referansta yoksa eklenmez, eksik olarak raporlanır.
- Forms/touch (source: vercel-labs/web-interface-guidelines, MIT):
  - Inputs, selects and textareas render at font-size ≥16px on mobile (390 width), so iOS does not auto-zoom.
  - `<meta name="viewport">` never disables zoom (`maximum-scale=1` / `user-scalable=no` forbidden).
  - Form fields carry a fitting `autocomplete` value (email, name, tel, street-address, one-time-code…).
  - Hit targets ≥24×24px, ≥44×44px on mobile; if the visual is smaller, the hit area is expanded.
  - No double submit: the submit button is disabled while the request is in flight and keeps its label (verify with a puppeteer double click).

## 5. Çıktı ve içerik
- static: `index.html` + `styles.css`; prototipte Tailwind CDN serbest. aspnet: Razor view/partial + `wwwroot/css/*.css`; inline `<style>` yasak; CSS değişkenleri site.css'te. Mobile-first.
- `brand_assets/` varsa logo/palet oradan, hex uydurma yok. Görsel yoksa `https://placehold.co/WxH`.
- İÇERİK: lorem ipsum yok · uydurma sayı/yorum/müşteri logosu yok · bölüm başına tek mesaj · başlıklar markaya özel iddia (jenerik "En iyi çözüm" yok). Metin kullanıcıdan gelmediyse sen yaz, raporda `[ÖNERİ]` işaretle; marka adı kullanıcıdan gelir.
- Sayfa deneyimi planı koddan önce: bölüm sırası + her bölümde medya yeri (görsel/video/3D) tek liste.
- Efekt ayarları (süre, genişlik, gölge, akışkanlık) tek config dosyasında toplanır; bileşenlere dağıtılmaz.

## 6. Tur raporu (her tur sonu, kısa)
Tur N | mod | PNG yolları | sapma tablosu | audit (+SLOP) | KANIT (FREE): ana/nötr/vurgu hangi elemanlarda · font çifti nerede · ölçek hangi bölümlerde | sonraki adım / KAPANIŞ / DUR
- Audit'in ELLE BAKILACAK kalemleri tur raporunda ayrıca yanıtlanır; PASS bu kalemleri kapsamaz.

## 7. Ön adım: DESIGN.md (Bölüm 11 seçiminden sonra; Bölüm 11 atlanıyorsa Bölüm 0'dan sonra; koddan önce)
- Yeni proje veya yeni ana ekranda ilk çıktı Bölüm 11'in yönleridir; DESIGN.md seçim yapıldıktan sonra yazılır. Mevcut DESIGN.md varsa ilk çıktı doğrudan DESIGN.md'dir. `DESIGN.md` proje kökündedir; kod bu dosyadaki kararlara göre yazıldığı için kod yazmadan önce üret, göster, DUR.
- Tam olarak şu 6 başlık, fazlası yok:
  1. **Stil adı** — Minimal | Brutalist | Glassmorphism | Retro | Corporate | Neobrutalism | Bento | Dark/Premium | Editorial — ya da isimli özgün bir yön.
  2. **Token'lar** — 3-6 adet, her biri `ad: değer` (ör. `ölçü-birimi: 8px grid`, `satır-uzunluğu: 65ch`). İsteğe bağlı ek satır: `kadran: deneysellik N · hareket N · yoğunluk N` (1-5).
  3. **Renk** — 4-6 isimli hex. Jenerik ad yasak (`brand-500` değil, `kavrulmuş-bakır` gibi).
  4. **Tipografi** — 2 isimli font + ölçek. Inter, Roboto, Arial, Space Grotesk, Poppins kullanılmaz; en sık görülen seçimler oldukları için sayfayı jenerik gösterir.
  5. **Hareket** — süre + easing, en fazla 3 kural. Her kural = tetikleyici (yükleme/scroll/hover) + teknik tarif (kütüphane + sürüm + hangi etkiyi neden karşıladığı) + scroll anlatısı varsa süreklilik ve geri-scroll davranışı.
  6. **YASAK LİSTESİ** — mor degrade · aşırı glow · üçlü eşit kart (özellik/fayda bölümlerinde; ürün ızgarası hariç) · her yerde ikon · merkezli tek kolon · lorem ipsum · aşırı yuvarlatma · gereksiz shadow.
- DESIGN.md kalıcı hafızadır: sonraki her ekran onu miras alır, yeniden üretilmez. Değişecekse önce DESIGN.md güncellenir, sonra kod.

## 8. İki-pass kuralı
- Pass 1: token planı üret → brief'e karşı kendin eleştir (hangi madde yasak listesine takılıyor?).
- Pass 2: sonra inşa et. Tek pass'te kod yazılmaz: eleştiri koddan önce yapılınca yasak listesine takılan karar koda girmeden elenir.

## 9. Screenshot döngüsü (zorunlu, kapalı çevrim)
- Kendi ürettiğin görseli göremezsin. Render'ı puppeteer ile screenshot al (`scripts/screenshot.mjs`, Bölüm 2), geri besle.
- Somut diff: sıfat değil sayı ("spacing dar" değil → "kart içi padding 16px, 24px olmalı").
- Tur sırası: 1) layout/hiyerarşi 2) renk/spacing 3) detay/hareket. En fazla 4 tur; 3. turdan sonra getiri düşer, gerek yoksa orada DUR.
- Her turda: console temiz mi (Bölüm 4 etkileşim kabulündeki araç sırasıyla: claude-in-chrome varsa o, yoksa puppeteer; yükle → keşfet → selector → aksiyon → console kaydı) · tab sırası doğru mu · kontrast AA mı.

## 10. Referans kaynakları
- Yön ararken önce referans çıkar, sonra dili yaz: 21st.dev · awwwards.com · lapa.ninja · recent.design · dribbble.com · figma.com/community · designprompts.dev
- 21st MCP kuruluysa bileşen araması oradan yapılır, elle yazılmaz. Adım-araç eşlemesi ve kota kapıları: `references/21st-akis.md`.
- Referansı kopyalama — ritim, kontrast, boşluk mantığını çıkar, projeye uygula.
- 3D/WebGL yönü aranırken Three.js resmi örnekleri (threejs.org/examples) referans alınır, kopyalanmaz.

## 11. Yön keşfi (yeni proje / yeni ana ekran; DESIGN.md'den önce)
- DESIGN.md yazılmadan önce üç yön üretilir ve kullanıcıya gösterilir. Amaç kod değil, karar.
- REF modunda (`reference/` klasörü varsa) Bölüm 11 atlanır; yön zaten referansla belirlenmiştir. Yön keşfi yalnız FREE modunda koşar.
- Kapsam — her yön için tek dosya, `.screens/yon/<n>.html`:
  - Yalnız hero + bir içerik bölümü (ürün ızgarası ya da özellik şeridi).
  - Sahte içerik, gerçek veri yok, backend bağlantısı yok.
  - Yalnız 1440 genişlik; responsive, a11y, test, build yok.
  - Proje koduna dokunulmaz, hiçbir dosya import edilmez.
- Üç yön birbirinden ayrı olmalı: üçü de aynı tipografi ailesinden, aynı zemin kararından, aynı yerleşim mantığından olamaz. Aynı fikrin üç tonu değil, üç fikir.
- Her yön için 7 satırlık künye: stil adı · 2 font · 4 hex · zemin kararı · ayırt edici hamle · anlatı konsepti (ürün değil hikâye; her öğe o fikre hizmet eder) · sektör uygunluğu (yönün hangi sektöre uyduğu bilgisi, ör. uzun scroll creative markada evet, e-ticarette hayır; yönler arası kıyas ya da öneri değil).
- Çıktı: puppeteer ile üç PNG (1440, tam sayfa) → `.screens/yon/`: `$env:WIDTHS="1440"; $env:SCREENS_DIR=".screens/yon"; node ${CLAUDE_SKILL_DIR}/scripts/screenshot.mjs http://localhost:3000/.screens/yon/<n>.html yon-<n>` (sunucu: proje kökünden `serve.mjs`, aspnet'te de; `file:///` yasak). Kullanıcıya üç künye + üç PNG yolu verilir, DUR.
  - Ortam değişkenli komut `Bash(node *)` iznine takılabilir; Windows'ta PowerShell aracıyla çalıştır.
- Kullanıcı birini seçer → DESIGN.md o yönden yazılır → seçilmeyen iki yönün HTML dosyaları silinir; üç PNG `.screens/yon/` altında kalır (hangi yönler arasından seçildiğinin kaydı).
- Yönleri kendin değerlendirme, "bence bu daha iyi" yazma; seçim kullanıcınındır.
- Referans: yön üretmeden önce Bölüm 10'daki kaynaklardan dil çıkarılır, kopyalanmaz. 21st kuruluysa referans çıkarma ucu `references/21st-akis.md`'de.
