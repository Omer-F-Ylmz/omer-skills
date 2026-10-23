# DERS KİTABI, Web S1: Temel (tasarım yönü → DESIGN.md → kalite kapısı → erişilebilirlik)
Kaynak: docs/okul/kaynak/web-s1/ (skill-frontend-craft.md, skill-departman-frontend.md, resmi-mdn-prm.md). Her madde bağlamdan birebir alıntıyla başlar; alıntılar `tools/okul/alinti_denetle.py` ile alt dize olarak doğrulanır.

## A. En iyi yöntemler + tarif kartları

**Kart A1, İş sırası (yeni proje / yeni ana ekran)**
> "yön keşfi (Bölüm 11: üç yön, künye + 1440 PNG, DUR, kullanıcı seçer) → DESIGN.md (Bölüm 7: göster, DUR) → iki-pass (Bölüm 8: token planı → yasak listesine karşı eleştiri → inşa) → kod → screenshot döngüsü (Bölüm 2/9)" (skill-frontend-craft.md)
1. Yön keşfi: üç yön, her biri künye + 1440 PNG; kullanıcı seçer.
2. DESIGN.md yazılır, gösterilir, DUR.
3. İki-pass: token planı → yasak listesine karşı eleştiri → inşa. Sonra kod.
Mevcut DESIGN.md ya da REF modu varsa yön keşfi atlanır.

**Kart A2, Mod tespiti (ilk adım, tek satır rapor)**
> "birebir eşleme, referans kazanır" (skill-frontend-craft.md)
> "koddan önce marka kimliği kararı `ana #hex · nötr #hex · vurgu #hex · display font · sans font · ölçek 8px`" (skill-frontend-craft.md)
REF'te referans kazanır ve hex'ler ölçülür; FREE'de marka kararı koddan önce yazılır (ana renk mor/indigo/menekşe olamaz).

**Kart A3, DESIGN.md (tam 6 başlık)**
> "DESIGN.md tam olarak 6 başlık, fazlası yok" (skill-frontend-craft.md)
Stil adı · Token'lar (3-6 adet) · Renk (4-6 isimli hex) · Tipografi (2 isimli font + ölçek) · Hareket (süre + easing, en fazla 3 kural) · YASAK LİSTESİ.

**Kart A4, Screenshot döngüsü (kapalı çevrim)**
> "Tur = screenshot → sapma tablosu → düzelt; min 2, max 4 tur; 4. tur sonunda sapma kalırsa DUR raporu." (skill-frontend-craft.md)
> "Sunucu şart, `file:///` yasak" (skill-frontend-craft.md)
Üç genişlik: 390/768/1440; her PNG Read ile açılır.

**Kart A5, Butonlar tek bileşenden**
> "bütün butonlar tek bileşenden varyantla türetilir; hover/focus/active o bileşende tanımlıdır, sayfada tek tek buton stili yok" (skill-frontend-craft.md)

**Kart A6, Hazır tasarım promptunu mevcut siteye uygulama**
> "dokunulmaz alanlar (ör. hero, mevcut animasyonlar) adıyla listelenir; prompttan yalnız ilgili bölüm alınır" (skill-frontend-craft.md)

**Kart A7, Departman sırası (araç zinciri)**
> "`DESIGN.md` yoksa önce o" (skill-departman-frontend.md)
> "`pixeljury` (görsel regresyon), akış/etkileşim `playwright-cli`" (skill-departman-frontend.md)
Sıra: tasarım kararı → yığın → referans/bileşen → … → screenshot → erişilebilirlik (axe) → performans → görsel QA → güvenlik → kapanış.

## B. Hata kataloğu

| Hata | Nereden çıkar | Teşhis | Düzeltme |
|---|---|---|---|
| Jenerik "AI görünümü" | Yasak listesi yok / kontrol edilmedi | `slop.mjs` bayrakları | > "`node ${CLAUDE_SKILL_DIR}/scripts/slop.mjs <url>` → TEMİZ (≤1 bayrak; çıkış 0)" (skill-frontend-craft.md); tek bayrak bilinçli imzaysa DESIGN.md'de gerekçelendirilir |
| Yakınsama (her projede aynı font/zemin) | Marka kararı geçmişe bakmadan verildi | Bölüm 3a geçmiş denetimi | > "Oradaki font aileleri ve zemin sınıfı bu projede kullanılmaz" (skill-frontend-craft.md) |
| iOS giriş alanında otomatik zoom | Mobilde küçük font | 390 genişlikte input font-size | > "Inputs, selects and textareas render at font-size ≥16px on mobile (390 width), so iOS does not auto-zoom." (skill-frontend-craft.md) |
| Zoom'u kapatan viewport | `maximum-scale=1` / `user-scalable=no` | meta viewport okunur | > "`<meta name="viewport">` never disables zoom" (skill-frontend-craft.md) |
| Çift gönderim | Submit butonu açık kalır | puppeteer çift tıklama | > "the submit button is disabled while the request is in flight and keeps its label" (skill-frontend-craft.md) |
| Dokunmatikte çalışmayan hover efekti | Yalnız mouse için tasarım | hover/focus/active × masaüstü/dokunmatik tablosu | > "hover ya da mouse'a bağlı efektin dokunmatikte karşılığı olur" (skill-frontend-craft.md) |
| Hareket hastalığı tetikleyen animasyon | `prefers-reduced-motion` yok sayıldı | OS ayarı açıkken sayfa | > "Animations such as scaling or panning large objects can be vestibular motion triggers." (resmi-mdn-prm.md); `@media (prefers-reduced-motion: reduce)` dalında hareketi kaldır/azalt |

## C. Kalite kapısı kontrol listesi
- [ ] > "DESIGN.md olmadan kod yok (REF modunda referans kazanır)." (skill-departman-frontend.md)
- [ ] > "Screenshot turu sayıyla raporlanır; 4 turu aşmak yasak." (skill-departman-frontend.md)
- [ ] > "PASS; FREE modunda SLOP satırı boş." (skill-frontend-craft.md), yalnız bu kalem doğrulama için elle yeniden yazıldı; kaynaktaki tam komut: `node ${CLAUDE_SKILL_DIR}/scripts/audit.mjs <url> dev`
- [ ] > "`html[lang]`, tek `h1`, `header/main/footer` landmark, her `img` alt+width+height" (skill-frontend-craft.md)
- [ ] > "kontrast gövde ≥4.5:1 / büyük başlık ≥3:1" (skill-frontend-craft.md)
- [ ] > "font ≤2 aile ≤4 dosya, `font-display: swap`, tüm medya boyutlu (CLS 0)" (skill-frontend-craft.md)
- [ ] > "Kırık link 0." (skill-frontend-craft.md)
- [ ] > "a11y 0 hata ve performans sayısı olmadan görsel QA'ya geçilmez; görsel QA geçmeden kapanış yok." (skill-departman-frontend.md)
- [ ] > "GLB hedefi ≤2 MB" (skill-frontend-craft.md)
- [ ] Prod teslim: > "sayfa başına `title` + meta description · favicon · manifest · `robots.txt` · `sitemap.xml`" (skill-frontend-craft.md)
- [ ] Tur raporu yazılmadan iş kapanmaz: > "rapor yazılmadan iş kapanmaz" (skill-frontend-craft.md)

## D. Ucuz yol
- Ölçüm/denetim betiktir, model değil: `audit.mjs`, `slop.mjs`, `screenshot.mjs`, `olc-renk.mjs` ($0, yerel). > "hex'ler `olc-renk.mjs` ile ölçülür" (skill-frontend-craft.md)
- Referans ve bileşen önce hazır kaynaktan: > "`21st-ui` (get_inspiration · get_component · get_theme · search_logo)" (skill-departman-frontend.md)
- Kütüphane seçimi raftan, gerekçesiz yok: > "gerekçesiz kütüphane yasak" (skill-frontend-craft.md)
- Dış araç çıktısı doğrulamasız teslim edilmez: > "Dış tasarım aracı (Claude Design, 21st) çıktısı görsel optimizasyon + audit'ten geçmeden teslim edilmez." (skill-frontend-craft.md)

## E. Proje bağlantısı: freelance sitesi, TELVE
- Her UI işi `frontend-craft` ile açılır; TELVE/freelance sitesi için ilk çıktı DESIGN.md (6 başlık), ikinci çıktı üç genişlikte PNG + tur raporu.
- Referans site verildiyse REF modu: > "birebir eşleme, referans kazanır" (skill-frontend-craft.md), sapma kararını yalnız Ömer verir.
- Yayın: Prod teslim maddeleri (C bölümü) + KVKK: > "footer'da KVKK/gizlilik + çerez onayı" (skill-frontend-craft.md).
