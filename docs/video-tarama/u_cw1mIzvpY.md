# Claude Code ile Tek Kişilik Ekip Gibi Çalışma Sistemi
kanal: Burhan Kocabiyik · süre: 12 dk · altyazı: otomatik tr
ana iddia: Claude Code masaüstü uygulamasında değil terminalde, iş alanı başına ayrı klasör ve görev başına ayrı chat ile Apify'dan toplanan veriyle (rakip reklam, sosyal medya) kullanılınca tek kişi büyük ekip işi çıkarır (90.000 $ kâr ve token iddiaları ölçümsüz).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Claude Code: terminal (CLI) kullanımı, masaüstü uygulaması yerine | ZATEN VAR | ELENDİ | bu kurulum zaten CLI'da koşuyor; gerekçe "kod bilgisayarda çalışır, bulutta çoğu çalışmaz"; "%70'ini kullanmıyorsunuz" ölçümsüz |
| Visual Studio Code? | ÇİFT | ELENDİ | sözlü "Visual Studio", "Terminal > yeni terminal" tarifi VS Code'a uyuyor; yalnız terminal barındırıcı, mevcut PowerShell/Git Bash + Claude Code CLI aynı işi yapıyor |
| iş alanı başına ayrı klasör (uygulama, topluluk, içerik, ajans), tek büyük klasör yerine | YENİ | BİLGİ | iddia: tek klasörde bilgi karışır, daha çok dosya aranıp okunur, daha çok token (ölçüm yok); CLAUDE.md'de oturum klasörü kapsamı kuralı yok |
| görev başına ayrı chat, "her chat bir otomasyon" (email bulma, email cevaplama, yeni özellik, teklif) | ZATEN VAR | ELENDİ | CLAUDE.md context disiplini (dalga başı /clear, subagent delegasyonu); "chatlerim hep açık kalıyor" kısmı "uzun aradan sonra yeni oturum" kuralıyla çelişir |
| Apify (Meta reklam, Google reklam, Instagram, LinkedIn, TikTok, web sitesi scraper'ları) | YENİ | ELENDİ | izin kötü: dış hesap + API anahtarı, login'li platform scraping; ihtiyaç pazarlama verisi, kurulu iş setinde yok; web sayfası okuma agent-reach ile kısmen çift |
| rakip reklam/içerik analizi → benzer kreatif ve hazır uygulama üretimi (AdCreative.ai?, Duolingo, Left Flow?, DOA V2) | YENİ | ELENDİ | pazarlama iş akışı, frontend-craft/CLAUDE.md'de hedefi yok; sonuç ("kesin çalışan uygulamalar") ölçümsüz, "çok fazla token yaktık" |
| diğer: Skool (DOA topluluğu), n8n-io/n8n (yalnız açıklamadaki video başlığı), Gold? (kendi uygulaması) | YENİ | ELENDİ | araç önerisi değil: topluluk linki, başka videonun başlığı, kendi ürün adı |
## ölçütler (YENİ)
- iş alanı başına ayrı klasör (teknik): bakım=— (teknik) · çift=kısmen CLAUDE.md context disiplini (/clear, graphify query ile dar keşif), klasör kapsamı yazılı değil · izin=yok · context=kurala yazılırsa ~1 satır · kurulum: —
- Apify: bakım=bilinmiyor (SaaS; videoda repo/MCP anılmadı) · çift=kısmi: web sayfası okuma agent-reach (Jina Reader), reklam/sosyal scraping örtüşme yok · izin=Apify hesabı + API anahtarı (konsol > ayarlar), dış ağ; kota/ücret videoda yok · context=0 (anahtarla çağrılınca; MCP anılmadı) · kurulum: —
- rakip reklam analizi · diğer (Skool, n8n, Gold?): bakım=n8n pushed 2026-09-15, 204.4k yıldız, arşivli değil; diğerleri bilinmiyor · çift=örtüşme yok · izin=analiz akışı Apify'a bağlı; Skool/n8n hesap · context=0 · kurulum: —
## hedefler (BİLGİ)
- oturumu işin kendi klasöründe aç: iş alanı başına ayrı klasör/proje, karışık tek büyük klasörde çalışma (iddia: daha az dosya taranır, daha az token; ölçüm yok) → CLAUDE.md (CONTEXT DİSİPLİNİ)
---
## ek: somut
- ayar: Apify API anahtarı Apify konsolunda alt taraftaki ayarlardan alınır, veri toplaması için Claude Code'a verilir (değer/env değişkeni adı söylenmedi)
- komut: yok (kurulum sözlü: Visual Studio [Code?] indir → yeni klasör → Terminal > yeni terminal → Claude'u kur; kurulum komutu söylenmedi, açıklamadaki uzun videolara yönlendirildi)
- dosya: dosya adı yok; klasörler: uygulama, topluluk, içerik, ajans; "Instagram kaydırmalı içerik üretici" klasörü
- sayı: geçen ay 90.000 $ kâr, Claude Code yoğun kullanılarak — yalnız iddia
- sayı: Instagram 170.000, YouTube ~90.000 takipçi, hepsi Claude Code'la yönetiliyor — yalnız iddia (ekranda Instagram gösterildiği söyleniyor, sayı doğrulanamaz)
- sayı: masaüstü uygulamasında Claude'un "%70'ini bence kullanmıyorsunuz" — yalnız iddia
- sayı: Left Flow? analizinde hesap etkileşimleri %0,20 ve %3 — ekrandaki analiz çıktısında gösterildi (sözlü)
- sayı: ayda 10-20 [ASR "1020"] kreatif yerine 100 kreatif denenebilir — yalnız iddia
- sayı: bu kullanımla rekabetin %0,001'ine girilir; yapılacak 50-70 iş var — yalnız iddia
- sayı: tek büyük klasör ve tek yere bağlı chatler "çok daha fazla token"; DOA V2 için "çok fazla token yaktık" — sayı yok, yalnız iddia
- sayı: sıfırdan kurulum iki adım (Claude Code + Apify API anahtarı); 7/24 çalışan otomasyon şart değil; dört klasör — anlatım
- sayı: açıklamada: 8 saatlik masterclass; 3+ saatlik kurs; "30 dakikada %95"; "23 dakikada 18 ipucu"; "22 kişilik ekip 30'a"; kaynaklar "%100 ücretsiz" — yalnız video başlığı/iddia
