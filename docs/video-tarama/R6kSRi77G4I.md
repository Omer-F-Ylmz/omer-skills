# Prompt Yazma Devri Bitti: Karşınızda Loop Engineering
kanal: Poyraz Avsever · süre: 11 dk · altyazı: otomatik tr
ana iddia: Prompt → context → harness mühendisliğinden sonra artık her adımda prompt yazmak yerine tetikleyici, hedef, iş, hafıza ve doğrulamadan oluşan kendi kendini yürüten döngüler kurulur; doğrulama ajanın kendi mock testleriyle değil TestSprite gibi dış bir doğrulayıcıyla yapılmalı (sponsorlu video, tek demo ilk turda geçti, döngü tekrar etmedi).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| TestSprite/testsprite-cli | YENİ | ELENDİ | sponsor (#işbirliği); tarayıcıda kullanıcı gibi adım adım test, hata aşamasını ekran görüntüsü + videoyla raporlar, panelde AI chat; izin kötü: global npm + testsprite.com hesabı + API anahtarı + kredi |
| Loop engineering döngüsü: tetikleyici (GitHub issue / her sabah 09:00 / manuel) → hedef → iş → hafıza → doğrulama, doğrulama geçince bitir | ZATEN VAR | ELENDİ | CLAUDE.md hedef-güdümlü (doğrulanabilir hedef, kabul kriteri, kanıtsız bitti yok) + frontend-craft Bölüm 2/9 kapalı çevrim; zamanlı tetikleyici Claude Code /schedule, tekrar /loop, hafıza auto-memory; videodaki döngüde tur tavanı yok, Bölüm 2'de max 4 + DUR var |
| OpenAI Codex: /goal? | ÇİFT | ELENDİ | ASR "slash go", "hedef dediğimiz ayar"; hedefi kaydedip doğrulama geçene kadar tekrarlar; Claude Code /loop (yerleşik, self-paced) aynı işi yapıyor |
| bağımsız doğrulayıcı: işi yapan ajanın kendi yazdığı mock unit/integration testi kanıt sayılmaz | YENİ | BİLGİ | iddia: test kodu yanlışsa döngü anlamsız, "insan gibi" doğrulayan dış ajan/CLI gerekir (ölçüm yok); CLAUDE.md "önce kırmızı test" testi aynı ajanın yazmasını ayırt etmiyor |
| etkileşim kabul kriteri tarayıcıda tıklanarak doğrulanır (dropdown: tıkla → profil, ayarlar, çıkış yap görünür mü, tek tek) | YENİ | BİLGİ | frontend-craft Bölüm 2/9 yalnız statik screenshot, Bölüm 4'te davranış kriteri yok; demo tek deneme, yazar ayrıca light/dark modda elle baktı |
| diğer: poyraz-ui (yazarın UI kütüphanesi, demo projesi), Codex VS Code eklentisi, Google Antigravity, prompt/context/harness engineering kavramları, yazarın loop engineering blog yazısı, Addy Osmani / Peter Steinberger / Boris Cherny yazıları | YENİ | ELENDİ | demo hedefi, alternatif ajan platformu (Claude Code ile çift) ya da kavramsal anlatım; repo/link verilmiyor (blog linki açıklamada yok) |
## ölçütler (YENİ)
- TestSprite/testsprite-cli: bakım=pushed 2026-09-14, 3.205 yıldız, arşiv değil, Apache-2.0 · çift=kısmi: frontend-craft Bölüm 2/9 puppeteer screenshot döngüsü + superpowers:verification-before-completion; tıklama testi ve video kaydı örtüşmüyor · izin=global npm paketi, testsprite.com üyeliği + API anahtarı, kredi (ücretsiz 150, ücretli 19-69 $), raporlar TestSprite panelinde, yerel canlıya yazarın IP adresi üzerinden erişti (sözlü) · context=setup projeye skill dosyaları yazdı (her oturum skill açıklaması; ad/sayı gösterilmedi) · kurulum: —
- teknikler (bağımsız doğrulayıcı, etkileşim kabul kriteri): bakım=— (teknik) · çift=kısmen CLAUDE.md hedef-güdümlü + frontend-craft Bölüm 2/4 · izin=yok · context=kurala ~1'er satır · kurulum: —
- diğer (poyraz-ui, Codex eklentisi, Antigravity, kavramlar, blog, yazılar): bakım=bilinmiyor (repo/link videoda yok) · çift=Codex/Antigravity Claude Code; kavramlar CLAUDE.md context disiplini · izin=ayrı ajan platformu hesabı · context=0 · kurulum: —
## hedefler (BİLGİ)
- işi yapan ajanın kendi yazdığı mock/unit test tek başına "bitti" kanıtı değildir; kabul kriteri uygulamayı gerçekten çalıştıran, yazandan bağımsız bir doğrulayıcıyla kanıtlanır → CLAUDE.md (hedef-güdümlü: doğrulama kaynağı)
- etkileşimli bileşende kabul kriteri davranış cümlesi olarak yazılır ("tıklayınca alt öğeler görünür") ve gerçek tarayıcıda tıklanıp her öğe tek tek doğrulanır; statik screenshot yetmez → frontend-craft Bölüm 4
---
## ek: somut
- ayar: döngü tetikleyicisi — GitHub issue ("repoda issue açılınca döngüyü tekrarla" prompt'u), her gün sabah 09:00 zamanlı iş (Claude Code / Antigravity / Codex uygulaması üzerinden ayarlanır, sözlü) ya da manuel; demoda manuel
- ayar: Codex VS Code eklentisinde /goal? (ASR "slash go") açılıp prompt yapıştırıldı; Codex hedefi kaydetti
- ayar: döngü prompt'u (sözlü, birebir değil): "Poyraz UI için dropdown menü bileşeni oluştur. Kod yazdıktan sonra lokal sunucuda canlıya al. Kabul kriteri: menüye tıklandığında alt seçeneklerin görünür olması. Doğrulama olarak bu kriteri test etmek için terminalde testsprite test komutunu kullan. TestSprite hata paketi döndürürse hata paketi ortadan kalkana kadar döngüyü tekrarla."
- ayar: API anahtarı — testsprite.com'a üye ol → API anahtarları → sağ üstten yeni anahtar oluştur (ad: "video") → testsprite setup'a yapıştır
- komut: npm install --global ile TestSprite CLI (ASR "npmın install çizgi global ... test sprite cala"; paket adı birebir duyulmuyor); testsprite setup (API anahtarı ister, kurulumu kendisi yapar); testsprite test (doğrulama); pnpm dev? (ASR "PMPM dev")
- dosya: TestSprite setup sonrası projeye skill dosyaları yazılmış (ad/yol altyazıda yok); açıklama linkleri: github.com/TestSprite/testsprite-cli, testsprite.com/?via=poyraz (referans linki); "aşağıda verilecek" blog yazısının linki açıklamada yok
- sayı: ücretsiz sürüm 150 kredi, ücretli planlar 19 $'dan 69 $'a — yalnız iddia (bir yerde "150 dolarlık ücretsiz versiyon" diyor, 150 kredi kastı?)
- sayı: kurulum 3 saniye (daha önce kurulu olduğu için), npm 1 paket ekledi — gösterildi (terminal çıktısı, altyazıdan doğrulanamaz)
- sayı: 4 aşamalı evrim (prompt → context → harness → loop engineering); döngü 5 aşama — kavramsal, kanıt yok
- sayı: TestSprite 3 menü öğesini (profil, ayarlar, çıkış yap) tek tek doğruladı, test ilk turda geçti, döngü tekrar etmedi — gösterildi (tek demo, video kaydı ekranda)
- sayı: TestSprite raporu kaç test yapıldığını / kaç hata olduğunu verir — panel gösterildi, sayı söylenmedi
