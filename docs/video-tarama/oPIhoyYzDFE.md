# Yapay Zekayla Kod Yazdık, Peki Güvenli Mi?
kanal: Poyraz Avsever · süre: 25 dk · altyazı: otomatik tr
ana iddia: AI ile yazılmış bir proje çalışıyor olsa da fonksiyon, sızma, bağımlılık (audit), otomatik tarama (ZAP), yasal ve SEO/erişilebilirlik kontrol listesinden geçmeden yayınlanmamalı.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| zaproxy/zaproxy (OWASP ZAP) | YENİ | ADAY | Docker ile prod build'e (pnpm build + start, localhost:3000) otomatik güvenlik taraması, zap-report.html raporu |
| npm audit / pnpm audit | YENİ | BİLGİ | yayın öncesi bildirilmiş açık denetimi; Paths sütunu dolaylı paketi gösterir (drizzle→esbuild, better-auth→postcss) |
| istemci doğrulamasını atlatma + SQLi/XSS payload testi | YENİ | BİLGİ | DevTools'ta type=email→text; sunucu şema doğrulaması (Zod) reddetti; form başına payload + beklenen davranış listesi LLM'den |
| yasal sayfalar (KVKK aydınlatma metni, gizlilik politikası, çerez izni, hesabımı sil) | YENİ | BİLGİ | linkler footer'da görünür, ilk girişte çerez onayı |
| sayfa metadata + robots.txt / sitemap.xml | YENİ | BİLGİ | sayfa başına title/description/favicon/manifest/ikon (Next.js generateMetadata); eksikler ZAP uyarısı verdi |
| diğer: klavyeyle form akışı, elle fonksiyon testi | ZATEN VAR | ELENDİ | frontend-craft Bölüm 9 tab sırası + Bölüm 3 focus-visible; CLAUDE.md hedef-güdümlü, kanıtsız "bitti" yok |
| diğer: vercel/next.js, better-auth/better-auth, WiseLibs/better-sqlite3, drizzle-team/drizzle-orm, colinhacks/zod, Framer Motion, jamiebuilds/tailwindcss-animate, Poyraz UI?, pnpm, Docker Desktop, VS Code yerleşik tarayıcı, Hosting Dünyam | YENİ | ELENDİ | proje yığını / ZAP ön koşulu / sponsor hosting; Claude'a kurulacak araç değil |
## ölçütler (YENİ)
- zaproxy/zaproxy: bakım=son push 2026-09-15, 15771 yıldız, arşiv değil · çift=örtüşme yok (yerleşik /security-review kodu inceler, çalışan uygulamayı taramaz) · izin=Docker Desktop, imaj indirme, localhost ağ erişimi · context=0 (Claude dışı araç, yalnız çağrılınca) · kurulum: komut yok (README yalnız zaproxy.org/download linki; videodaki Docker komutu altyazıda okunmuyor, blog yazısına yönlendiriliyor)
- BİLGİ teknikleri (audit, payload testi, yasal sayfalar, metadata): bakım=— (teknik) · çift=payload testi kısmen /security-review, diğerleri örtüşme yok · izin=yok · context=kurala yazılırsa birkaç satır kalıcı, yoksa 0 · kurulum: —
- diğer (proje yığını/sponsor): bakım=next.js, better-auth, drizzle-orm, zod 2026-09 push; better-sqlite3 2026-08; tailwindcss-animate 2024-07 (durgun); diğerleri bilinmiyor · çift=örtüşme yok · izin=proje bağımlılığı (npm/pnpm), Docker Desktop, Hosting Dünyam ücretli hesap · context=0 · kurulum: —
## hedefler (BİLGİ)
- bağımlılık denetimi (npm/pnpm audit, Paths ile dolaylı paket) · istemci doğrulamasını DevTools'la atlatıp SQLi/XSS payload ile sunucu doğrulamasını test → CLAUDE.md (yayın öncesi güvenlik kontrolü)
- footer'da KVKK/gizlilik/çerez linkleri + çerez onayı + hesabımı sil · sayfa başına title/description/favicon/manifest + robots.txt/sitemap.xml → frontend-craft Bölüm 4 (prod teslim)
---
## ek: test/güvenlik
- yöntem: temel fonksiyon testi — tüm akışları (giriş/çıkış, ikinci admin kaydının kapalı olması, müşteri ekleme, sürükle-bırak, portal davet bağlantısı) elle tek tek dene
- komut: pnpm dev (development ortamı; güvenlik taraması için kullanılmaz)
- yöntem: SQLi — giriş formunda e-posta alanına `' OR 1=1 --`, şifreye rastgele değer
- yöntem: F12 DevTools'ta input `type="email"` → `text` yapıp istemci doğrulamasını atlat; sunucudaki Zod doğrulaması Better Auth'a ulaşmadan "invalid format" döndü
- yöntem: XSS — profil soyad alanına `alert('sisteme sızıldı')` içeren script; kaydet + yenile sonrası alert çıkmadı, düz metin saklandı (tam payload yazımı altyazıdan okunmuyor)
- yöntem: ChatGPT / Gemini / Codex / Antigravity'ye teknoloji, dosya yapısı (mümkünse kod) verip form başına sızma testi komutları ve beklenen davranış listesi iste
- sayı: payload listesini elle uygulamak yaklaşık 1–1,5 saat sürer — yalnız iddia
- komut: pnpm audit / npm audit (kullanılan paketlerde bildirilmiş açık kontrolü)
- ayar: audit önem dereceleri low / moderate / high / critical (high: ilgilen, critical: haber çıkar çıkmaz müdahale)
- sayı: pnpm audit 2 açık buldu (esbuild ← drizzle, postcss ← better-auth) — gösterildi
- yöntem: audit çıktısındaki Paths sütunuyla doğrudan kurulmamış (transitive) paketin hangi bağımlılıktan geldiğini bul
- komut: npm audit fix (güncellenebilir paketleri günceller)
- yöntem: pnpm'de fix komutu yok, açıklı paketler elle ya da AI ile güvenli sürüme güncellenir — yalnız iddia, doğrulanmadı
- yöntem: staging/test sunucusunda otomatik tarama, testler geçerse canlıya al; staging yoksa lokalde
- komut: pnpm build + pnpm start (prod benzeri, localhost:3000) — tarama dev sunucusuna değil buna yapılır
- araç: OWASP ZAP, Docker Desktop üzerinden (Docker ZAP araçlarını indirir, 3000 portundaki uygulamaya saldırı simülasyonu yapar); tam komut altyazıda yok
- dosya: zap-report.html (toplam test, geçen/geçmeyen ayrıntılı rapor)
- sayı: ZAP yüzlerce belki binlerce otomatik güvenlik testi yapar — yalnız iddia
- sayı: ZAP taraması 56 test, 56 geçti, 11 uyarı, 0 hata — gösterildi (ekrandaki rapordan okunuyor)
- ayar: ZAP kontrol örnekleri — cookie'ler, cross-domain JavaScript source file, username hash found
- ayar: ZAP uyarıları — robots.txt, sitemap.xml ve forgot password sayfası bulunamadı (404)
- yöntem: uyarıları tek tek incele ya da raporu AI'ya gönder; fail varsa hemen düzelt
- yöntem: yasal — KVKK aydınlatma metni, gizlilik politikası, çerez izni (ilk girişte onay), hesabımı sil butonu; linkler footer'da görünür
- yöntem: hesabımı sil butonu olmadığı için birçok tanıdığın mobil uygulaması yayında reddedildi — yalnız iddia (anekdot)
- dosya: layout.tsx içinde generateMetadata — favicon URL, title, description, manifest, ikonlar; sayfa başına başlık (ör. dashboard · neta)
- yöntem: erişilebilirlik — fare olmadan Tab / Enter / ok tuşlarıyla form doldurma (select, tarih, saat, sayı artır-azalt) ve Enter ile kaydetme
- yöntem: tarayıcılar erişilebilir siteyi algılayıp öne çıkarır — yalnız iddia
- araç/yöntem (yalnız açıklama etiketlerinde, altyazıda işlenmedi): owasp zap docker, host.docker.internal, pnpm overrides, npm audit fix hatası, env dosyası github, zod validation, nextjs middleware, rate limiting, idor, iş mantığı açıkları, lighthouse, aria-label, next image alt, gdpr, unutulma hakkı
- dosya: blog yazısı poyrazavsever.com/tr/blog/yayina-cikmadan-once-dikkat-et (videodaki tüm komutların orada olduğu söyleniyor; okunmadı)
