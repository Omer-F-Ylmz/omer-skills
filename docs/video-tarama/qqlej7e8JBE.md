# Claude Code Memory 2.0: Yeni Auto Dream Modu ile Token Masrafını Düşürün
kanal: Burhan KOCABIYIK · süre: 8 dk · altyazı: otomatik tr
ana iddia: Claude Code'un Auto Dream (Memory 2.0) modu arka planda bir alt-ajanla bellek dosyalarını tarayıp gereksizi silerek ve özetleyerek her döngüde checkpoint oluşturur, büyük projelerde token kullanımını düşürür (yalnız iddia; demoda bellek boştu, token ölçümü gösterilmedi).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Claude Code: Auto Dream (/dream?) | ZATEN VAR | ELENDİ | yerleşik alt-ajan: önceki oturumların MD/memory dosyalarını tarar, gereksizi siler, özetler, küçültür; /memory menüsünde varsayılan kapalı, Enter ile açılır; kurulum yok, istenirse tek toggle |
| Claude Code: /memory (auto memory) | ZATEN VAR | ELENDİ | yerleşik; videoda auto memory zaten açık, oturumdaki önemli kararları ve proje yapısını kaydeder; user/project memory konumu menüde görünür; bu oturumda MEMORY.md mevcut |
| Oturum log dosyası (ajan yaptığı her değişikliği kaydeder) | ÇİFT | ELENDİ | sunucunun Auto Dream öncesi elle yöntemi; oturumlar arası bağlamı yerleşik auto memory (MEMORY.md) zaten taşıyor |
| diğer: Visual Studio Code, Google Antigravity | YENİ | ELENDİ | VS Code (ASR "Visual Studio") yalnız `claude` çalıştırılan terminal/eklenti host'u; Antigravity (ASR "an gravity") ücretsiz alternatif, sunucuya göre "Claude Code kadar iyi çalışmaz" |
| diğer: n8n-io/n8n, Instantly | YENİ | ELENDİ | yalnız açıklamada affiliate link; video konusu (bellek/token) ile ilgisiz |
## ölçütler (YENİ)
- diğer (Visual Studio Code, Google Antigravity): bakım=bilinmiyor (repo videoda yok) · çift=VS Code host olarak Claude Code CLI'ın zaten çalıştığı terminalle; Antigravity ajan IDE olarak Claude Code'un kendisiyle · izin=yerel masaüstü uygulaması kurulumu; hesap şartı videoda yok · context=yok (kurulmuyor) · kurulum: —
- diğer (n8n-io/n8n, Instantly): bakım=n8n pushed_at 2026-09-15, 204367 yıldız, archived=false; Instantly bilinmiyor (ticari servis) · çift=örtüşme yok · izin=Instantly ücretli hesap + login; n8n hesap ya da self-host sunucu · context=yok (harici servis, Claude Code'a bağlanmıyor) · kurulum: —
## hedefler (BİLGİ)
- yok
---
## ek: somut
- ayar: /memory menüsü: auto memory açık (varsayılan), auto-dream kapalı → seçip Enter ile açılır, kapatmak için yine /memory; menü user ve project memory konumlarını gösterir, dosyalar buradan açılır
- ayar: Auto Dream tetiklemesi oturum sayısına dayalı (eşik videoda yok); tamamen boş oturumda çalışmaz, dolu session içinde başlatılmalı (sunucunun çıkarımı, gösterilmedi)
- komut: `claude` (VS Code'da yeni terminal); `/memory`; `/dream?` (ASR "slashdam", boş oturumda hemen çalışmadı, sonradan geldi); prompt "run your auto dream"
- komut: VS Code kurulumu için "iki tane prompt" + authentication — metin altyazı/açıklamada yok, yalnız ekranda
- dosya: MEMORY.md (demo çıktısı "Memory is empty. No MEMORY.md"); önceki oturumlardan kalan MD dosyaları; elle tutulan log dosyası (ör. "web sitesini mavi yaptım, giriş sayfası ekledim"); demo projesi "YouTube Codex projesi"
- sayı: çok büyük projede yalnız projeyi çalıştırmak 20.000-30.000 token — yalnız iddia
- sayı: Goat projesi (ASR "Gold", bölüm başlığı "Goat") 30'dan fazla özellik; her seferinde Auto Dream + checkpoint ile daha az token — yalnız iddia
- sayı: Auto Dream çalışırken token harcar ama toplamda kullanımı azaltır — yalnız iddia, ölçüm gösterilmedi
- sayı: açıklamada "Tüm kaynaklar %100 ücretsiz"; kurs videoları 2 saat, 3 saat, 8 saat — promosyon, yalnız iddia
