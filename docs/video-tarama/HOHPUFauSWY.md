# Claude Code'da Loop ile Kendini Test Eden Otomasyon Kurmak
kanal: Burhan KOCABIYIK · süre: 11 dk · altyazı: otomatik tr
ana iddia: Prompt iyileştirmek yerine işi tetikleyici, stop koşulu, plan.md hafızası ve TestSprite doğrulamasıyla Claude Code döngüsüne alınca sistem kendini test edip iyileştirir.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| TestSprite/testsprite-cli (TestSprite) | YENİ | ADAY | canlı uygulamayı bulutta kullanıcı gibi test eden servis + CLI; videoda loop'un feedback adımı, testleri panelde raporluyor |
| Claude Code: /loop? | ZATEN VAR | ELENDİ | yerleşik loop skill; videoda komut adı söylenmiyor, "hedef tamamlanana kadar döngüde çalış" promptu |
| Claude Code: Skills (SKILL.md) | ZATEN VAR | ELENDİ | yerleşik; videoda "yetenek dosyası" olarak loop akışını tarif ediyor |
| Loop anatomisi: plan.md hafıza + açık stop koşulu | YENİ | BİLGİ | tetikleyici/stop/iş/hafıza/feedback; her iterasyon önce plan.md okur, stop koşulunda durur |
| Feedback = verification (sonraki adımdan önce test) | ZATEN VAR | ELENDİ | CLAUDE.md Hedef-güdümlü ("kanıtsız bitti yok") + superpowers verification-before-completion |
| Vercel; Webflow? | YENİ | ELENDİ | yalnız deploy/yayın hedefi, Claude aracı değil; "Left Flow" ASR, site adı da olabilir |
| diğer: CoderCup (codercup.ai), VS Code terminali, Skool (DOA) | YENİ | ELENDİ | CoderCup yalnız açıklamada link, videoda anlatılmıyor; VS Code ortam; Skool kanal tanıtımı |
## ölçütler (YENİ)
- TestSprite/testsprite-cli: bakım=pushed 2026-09-14, 3205 yıldız, arşiv değil · çift=örtüşme yok (superpowers verification-before-completion yalnız disiplin, test servisi değil) · izin=TestSprite hesabı + API anahtarı, kredi tabanlı (ücretsiz kredi sonra ücretli), global npm (npx alternatif), uygulama buluta açık URL ya da --local tünel, setup repo'ya skill dosyası yazar · context=proje başına 1 skill açıklaması her oturum; MCP şeması yok, CLI yalnız çağrılınca · kurulum: npm install -g @testsprite/testsprite-cli && testsprite setup
- Vercel; Webflow?; diğer: bakım=bilinmiyor (servis/ürün) · çift=örtüşme yok · izin=hesap/login (Vercel, Webflow, Skool) · context=yok (skill/MCP değil) · kurulum: —
## hedefler (BİLGİ)
- Loop/gece koşusu: plan.md'de ölçülebilir hedef + stop koşulu, her iterasyon önce plan.md oku, sonunda doğrulama → CLAUDE.md (Hedef-güdümlü)
---
## ek: somut
- ayar: loop bileşenleri tetikleyici, stop koşulu (altyazıda "iki stop koşulu", ASR olabilir), iş, hafıza, feedback
- ayar: plan.md hedefi: Webflow? sitesine her gün yeni blog yazısı; blog altyapısı ve yazı üretim sistemi belli; yazılar Webflow?'a ve SEO'ya uygun olmalı; tek tek onay istemiyor
- ayar: TestSprite panelinde "API anahtarları" altında yeni anahtar (adı altyazıda "Cloud block", Claude blog?) oluşturulup Claude oturumuna yapıştırılıyor
- komut: prompt "plan.md dosyasına hedef tamamlanana kadar döngüde çalış"; skill akışı: her iterasyonda önce plan.md oku → hafızayı ilerlet → kur/oluştur → Vercel'de çalış → TestSprite yeteneğiyle davranış testi oluştur/kontrol et → plan.md stop koşullarında dur
- komut: TestSprite kurulum komutu altyazıda okunmuyor; sitedeki butondan kopyalanıp VS Code yeni terminaline yapıştırılıyor
- dosya: SKILL.md (yetenek dosyası); plan.md
- sayı: kurulum 4 paket yüklüyor — gösterildi (canlı kurulum anlatımı)
- sayı: ~2 saatlik koşu, testler 3.29 / 3.47 / 3.58'de çalışmış — gösterildi (TestSprite paneli)
- sayı: geçen test 19'da 10 → 16 → 18 (altyazıda karışık: "10 taneden 19") — sayılar panelde gösterildi; "kendini iyileştirdi" nedenselliği yalnız iddia
- sayı: 50 YouTube videosunun kapak analizi; 10.000 sayfalık kitap 20-30 ajana bölünür; 500 dolarlık reklam kaybı; 50-100+ otomasyon kontrolü; 7/24 hatasız çalışma — örnek/yalnız iddia
- sayı: TestSprite ücretsiz kredi veriyor; açıklamada "tüm kaynaklar %100 ücretsiz" — yalnız iddia
- sayı: açıklamadaki 10:30 "hangi işe hangi model — token tasarrufu" bölümü — altyazıda karşılığı yok (yalnız bölüm başlığı)
