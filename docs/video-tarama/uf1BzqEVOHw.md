# Bilgisayar Başında Olmadan Uygulama Geliştirmek: Claude Dispatch Kurulum Rehberi
kanal: Burhan KOCABIYIK · süre: 5 dk · altyazı: otomatik tr
ana iddia: Claude Desktop'taki Dispatch ile telefondaki Claude uygulamasından masaüstü bilgisayara görev verilip dosya, terminal, tarayıcı ve klavye/fare işlemleri yaptırılabilir.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Claude Desktop: Dispatch | ÇİFT | ELENDİ | telefondan yerel oturumu yönetmek Claude Code Remote Control (yerleşik) ile aynı iş; fazlası GUI kontrolü, browser actions + Accessibility + Screen Recording ile tam makine erişimi ister, video riskten söz etmiyor |
| Claude Code for VS Code | ÇİFT | ELENDİ | Dispatch'e "VS Code içindeki Claude'u çalıştır, web sitesi oluştur, lokalde aç" örneği; aynı iş kullanılan Claude Code CLI ile yapılıyor |
| Skool: DOA topluluğu | YENİ | ELENDİ | açıklamadaki topluluk/kurs tanıtımı; geliştirme aracı değil, kurulacak bir şey yok |
| n8n-io/n8n | YENİ | ELENDİ | yalnız açıklamada başka video başlığı ("n8n & Claude Code Masterclass"); bu videoda kullanılmıyor |
## ölçütler (YENİ)
- Skool: DOA topluluğu: bakım=bilinmiyor · çift=örtüşme yok · izin=Skool hesabı/login, DOA üyelik koşulu videoda belirtilmiyor · context=yok (Claude'a yüklenmez) · kurulum: —
- n8n-io/n8n: bakım=pushed_at 2026-09-15, 204368 yıldız, arşiv değil · çift=örtüşme yok · izin=self-host sunucu ya da n8n cloud hesabı · context=yok (videoda MCP/skill olarak geçmiyor) · kurulum: —
## hedefler (BİLGİ)
- yok
---
## ek: test/güvenlik
- araç: Claude Desktop uygulaması, Claude'da sol alttaki "Get Apps" üzerinden indirilir; Code tarafında Dispatch girişi var
- araç: telefondaki Claude uygulaması, masaüstündeki Dispatch'e görev gönderir
- ayar: Ayarlar'da browser actions açılmalı (videoya göre varsayılan kapalı)
- ayar: Accessibility izni verilmeli
- ayar: Screen Recording izni verilmeli
- yöntem: izin istemleri telefonda da çıkar, onay telefondan verilebilir (ekranda anlatıldı)
- yöntem: "bana ne yaptığını bilgisayarda göster, oradaki klavye ve mouse'u kullan" istemiyle görünür klavye/fare kontrolü
- yöntem: bilgisayardaki bir uygulamayı telefondan test ettirme — girişte örnek olarak söylendi, adımları gösterilmedi
- yöntem: terminale çalışan bir şey kurdurma — yalnız söylendi, gösterilmedi
- yöntem: "VS Code içindeki Claude'u çalıştır, web sitesi oluştur, lokalde aç" görevi — sonucu altyazıda doğrulanmıyor
- yöntem: "sürekli çalışsın" denince bilgisayarın uyku moduna geçmemesini sağlama — yalnız iddia
- yöntem: bilgisayar üzerinden internette araştırma — yalnız iddia
- yöntem: e-posta gönderme, sunum kaydı, takvim daveti örneği — girişteki örnek görüntüyle anlatıldı
- komut: terminal komutu yok; istemler: "PC'mi kullanarak sunum oluştur" (satış süreç dokümanı), "terminaldeki bu projemi aç, üzerine bir şeyler yap"
- dosya: yok
- sayı: "Tüm kaynaklar %100 ücretsiz" (skool.com/doa-zero) — yalnız iddia
- sayı: açıklamadaki kurs süreleri: Claude Code Full Kurs 2 saat, Yapay Zeka Ajanları 3 saat, n8n & Claude Code Masterclass 8 saat — yalnız iddia
