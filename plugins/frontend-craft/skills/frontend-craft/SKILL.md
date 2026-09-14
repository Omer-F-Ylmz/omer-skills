---
name: frontend-craft
description: Web arayüzü (landing, vitrin, panel ekranı) tasarım ve uygulama disiplini — marka kimliği kararı, referans eşleme, 3 genişlikte screenshot döngüsü, anti-generic + yasak liste, a11y/perf kabul kriterleri. HTML/CSS/Tailwind/Razor'a dokunan her işte önce bunu yükle.
allowed-tools: Bash(node *) Bash(npm *) Bash(npx *)
---

## 0. Mod tespiti (ilk adım, tek satır raporla)
- Tara: `reference/` (png/jpg/pdf) var mı → REF modu; yoksa FREE modu. `brand_assets/` var mı. Proje türü: `*.csproj` + `Views/` veya `Pages/` → aspnet; değilse static.
- `inspiration/` klasörü varsa yön için oku; hiçbir düzeni kopyalama.
- REF: hedef birebir eşleme. Bölüm 3 UYGULANMAZ; referans her zaman kazanır. Referansta olmayan bölüm/özellik/metin eklenmez, referans "iyileştirilmez".
- FREE: koddan önce MARKA KİMLİĞİ KARARI tek satır: `ana #hex · nötr #hex · vurgu #hex · display font · sans font · ölçek 8px`. Ana renk mor/indigo/menekşe olamaz. Sonra Bölüm 3 zorunlu. Kararı vermeden önce `ui-ux-pro-max` varsa `search.py "<sektör> <ürün>" --design-system -p <Proje>` çalıştır, öneriyi aday al; kararı yine tek satır yaz.
- `frontend-design` skill'i listede varsa onu da yükle; yoksa Bölüm 3 onun yerine geçer.

## 1. Sunucu
- static: `node ${CLAUDE_SKILL_DIR}/scripts/serve.mjs` arka planda → http://localhost:3000. Çalışıyorsa ikinci instance açma.
- aspnet: `dotnet run --project <web csproj>` arka planda; URL `Properties/launchSettings.json`'dan.
- `file:///` ile screenshot YASAK.

## 2. Screenshot döngüsü
- `node ${CLAUDE_SKILL_DIR}/scripts/screenshot.mjs <url> [etiket]` → `.screens/` altına 390/768/1440 üç PNG. Her PNG'yi Read ile aç ve incele.
- Tur = screenshot → sapma tablosu → düzelt → screenshot. Min 2, max 4 tur.
- Sapma satırı: `genişlik | öğe | ölçülen | beklenen | tolerans dışı?`
- Tolerans: spacing ±2px, font-size ±1px, radius ±1px, hizalama ±2px, renk exact hex, font ailesi/ağırlık exact.
- REF'te beklenen = referans; FREE'de beklenen = Bölüm 0 kararı + Bölüm 3 token'ları.
- Kapanış: 3 genişlikte 0 tolerans-dışı sapma. 4. tur sonunda hâlâ sapma varsa DUR raporu (kalan sapmalar + neden).

## 3. FREE modu guardrail'leri
- Renk: Tailwind default paleti birincil olamaz; tek marka rengi, tint/shade türet, CSS değişkeni.
- Tipografi: başlık ≠ gövde ailesi (display/serif + sans). Büyük başlık `letter-spacing:-0.03em`; gövde `line-height:1.7`; 5 kademeli ölçek; h1 belirgin, h2/h3 kademeli.
- Spacing: tek ölçek 8/16/24/32/48/64/96; ölçek dışı değer yok; bölümler arası boşluk ölçekten.
- Gölge: düz `shadow-md` yok; katmanlı, marka renginden türetilmiş, düşük opaklık.
- Arka plan bilinçli seçilir: düz zemin + tek radial vignette + yönsüz grain (opaklık ≤0.06) da geçerli bir karardır; katmanlı gradient zorunlu değildir. Zorunlu olan, seçimin DESIGN.md'de yazılı olması.
- Derinlik: 3 yüzey seviyesi (base → elevated → floating).
- Görsel (logo/ikon hariç): görsel üstü gradient overlay YALNIZ metin görselin üstüne biniyorsa — o durumda `from-black/60` + `mix-blend-multiply` renk katmanı.
- Animasyon: yalnız `transform`/`opacity`; `transition-all` yasak; easing `cubic-bezier(.22,1,.36,1)`; `prefers-reduced-motion` ile kapanır; gereksiz animasyon/kütüphane yok.
- Interaktif: her `a, button, [role=button], input, select, textarea` için hover + focus-visible + active.
- İkon: tek aile, SVG (Lucide outline); emoji yok.
- Grid: kırık simetri — ≥1 bölüm asimetrik kolon/tam genişlik dışı; her şey ortalı ve eşit genişlik olmaz.
- YASAK: mor/indigo→mavi gradient · emoji ikon · backdrop-filter blur kart yığını · "h1+p+2 buton" hero kalıbı birebir · stok illüstrasyon/3D render hissi · eşit boyutlu kart tekrarı (özellik/fayda bölümlerinde; ürün ızgarası hariç — orada eşit kart zorunlu, kırık simetri sayfa/başlık düzeyinde aranır) · her bölümde aynı boşluk.
- Bu liste varsayılandır; projenin YASAK listesi DESIGN.md'de yazılır ve seçilen stille çelişen maddeler oradan çıkarılır (ör. Glassmorphism seçilen projede blur maddesi geçersiz).

## 4. Her iki modda kabul kriterleri
- `node ${CLAUDE_SKILL_DIR}/scripts/audit.mjs <url> dev` → PASS; FREE modunda SLOP satırı boş.
- a11y: `html[lang]`, tek `h1`, `header/main/footer` landmark, her `img` alt+width+height, fold altı `loading="lazy"`, kontrast gövde ≥4.5:1 / büyük başlık ≥3:1 (hex'ten hesapla, çiftleri raporla).
- perf: font ≤2 aile ≤4 dosya, `font-display: swap`, tüm medya boyutlu (CLS 0).
- Prod teslim (kullanıcı "prod"/"yayın" dediğinde): Tailwind CDN kaldırılır → `npx @tailwindcss/cli -i src/input.css -o wwwroot/css/site.css --minify`; `audit.mjs <url> prod` PASS.

## 5. Çıktı ve içerik
- static: `index.html` + `styles.css`; prototipte Tailwind CDN serbest. aspnet: Razor view/partial + `wwwroot/css/*.css`; inline `<style>` yasak; CSS değişkenleri site.css'te. Mobile-first.
- `brand_assets/` varsa logo/palet oradan, hex uydurma yok. Görsel yoksa `https://placehold.co/WxH`.
- İÇERİK: lorem ipsum yok · uydurma sayı/yorum/müşteri logosu yok · bölüm başına TEK mesaj · başlıklar markaya özel iddia (jenerik "En iyi çözüm" yok). Metin kullanıcıdan gelmediyse sen yaz, raporda `[ÖNERİ]` işaretle; marka adı kullanıcıdan gelir.

## 6. Tur raporu (her tur sonu, kısa)
Tur N | mod | PNG yolları | sapma tablosu | audit (+SLOP) | KANIT (FREE): ana/nötr/vurgu hangi elemanlarda · font çifti nerede · ölçek hangi bölümlerde | sonraki adım / KAPANIŞ / DUR

## 7. ZORUNLU ÖN ADIM: DESIGN.md (Bölüm 0'dan sonra, koddan önce)
- Her UI işinin ilk çıktısı proje kökünde `DESIGN.md`. Kod yazmadan önce üret, göster, DUR.
- Tam olarak şu 6 başlık, fazlası yok:
  1. **Stil adı** — Minimal | Brutalist | Glassmorphism | Retro | Corporate | Neobrutalism | Bento | Dark/Premium | Editorial — ya da isimli özgün bir yön.
  2. **Token'lar** — 3-6 adet, her biri `ad: değer` (ör. `ölçü-birimi: 8px grid`, `satır-uzunluğu: 65ch`).
  3. **Renk** — 4-6 İSİMLİ hex. Jenerik ad yasak (`brand-500` değil, `kavrulmuş-bakır` gibi).
  4. **Tipografi** — 2 isimli font + ölçek. Inter, Roboto, Arial, Space Grotesk, Poppins YASAK.
  5. **Hareket** — süre + easing, en fazla 3 kural.
  6. **YASAK LİSTESİ** — mor degrade · aşırı glow · üçlü eşit kart · her yerde ikon · merkezli tek kolon · lorem ipsum · aşırı yuvarlatma · gereksiz shadow.
- DESIGN.md kalıcı hafızadır: sonraki her ekran onu miras alır, yeniden üretilmez. Değişecekse önce DESIGN.md güncellenir, sonra kod.

## 8. İKİ-PASS KURALI
- Pass 1: token planı üret → brief'e karşı KENDİN eleştir (hangi madde yasak listesine takılıyor?).
- Pass 2: sonra inşa et. Tek pass'te kod yazma.

## 9. SCREENSHOT DÖNGÜSÜ (zorunlu, kapalı çevrim)
- Kendi ürettiğin görseli göremezsin. Render'ı puppeteer ile screenshot al (`scripts/screenshot.mjs`, Bölüm 2), geri besle.
- Somut diff: sıfat değil SAYI ("spacing dar" değil → "kart içi padding 16px, 24px olmalı").
- Tur sırası: 1) layout/hiyerarşi 2) renk/spacing 3) detay/hareket. En fazla 4 tur; 3. turdan sonra getiri düşer, gerek yoksa orada DUR.
- Her turda: console temiz mi · tab sırası doğru mu · kontrast AA mı.

## 10. REFERANS KAYNAKLARI
- Yön ararken önce referans çıkar, sonra dili yaz: 21st.dev · awwwards.com · lapa.ninja · recent.design · dribbble.com · figma.com/community · designprompts.dev
- 21st MCP kuruluysa bileşen araması oradan yapılır, elle yazılmaz.
- Referansı kopyalama — ritim, kontrast, boşluk mantığını çıkar, projeye uygula.
