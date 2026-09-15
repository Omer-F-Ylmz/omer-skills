# MiniMax'i Claude Code'a Bağlayıp Token Masrafını 5x Düşürün
kanal: Burhan KOCABIYIK · süre: 12 dk · altyazı: otomatik tr
ana iddia: Tekrarlı ve token yoğun işlerde MiniMax'i ayrı bir komutla (claude-mm) Claude Code'a bağlamak, Opus'a yakın sonuçla maliyeti 5-6 kat düşürür (iddia).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| MiniMax API (MiniMax-M3?) | YENİ | ELENDİ | izin kötü: ücretli bakiye + API anahtarı, kod/görseller üçüncü tarafa gider; kalite kanıtı yok; açıklamada affiliate indirim kodu |
| claude-mm (MiniMax'li ayrı Claude Code başlatma komutu) | YENİ | ELENDİ | MiniMax'e bağlı; komut metni altyazıda yok, açıklama "dosyada" diyor ama dosya linki yok |
| Claude Code: /model | ZATEN VAR | ELENDİ | yerleşik; yeni terminalde modelin Opus kaldığını kontrol için kullanıldı |
| NousResearch/hermes-agent, openclaw/openclaw | ÇİFT | ELENDİ | yalnız "ucuz model kullanan ajan sistemi" örneği; ajan çalışma ortamı olarak Claude Code ile aynı iş |
| iş tipine göre model ayrımı (tekrarlı toplu üretim ucuz modelde, karmaşık iş Opus'ta) | YENİ | BİLGİ | videonun ana tekniği; kalite karşılaştırması yok, kural yazılırsa örneklem kabul kriteri şart |
| görsel girdiden üretim (ekran görüntüsü → e-posta şablonu / arayüz) | ZATEN VAR | ELENDİ | Claude Code yerleşik görsel girdisi; görselden arayüz frontend-craft Bölüm 0 REF modu |
| diğer: OpenRouter, Godbot? (kanalın kendi ajan uygulaması), Fable? (ASR belirsiz model adı), Skool (DOA topluluğu) | YENİ | ELENDİ | yalnız anıldı / demo konusu / tanıtım linki; kurulum önerisi değil |
## ölçütler (YENİ)
- MiniMax API: bakım=bilinmiyor (servis, repo yok) · çift=örtüşme yok (kurulu sette alternatif model sağlayıcı yok) · izin=MiniMax hesabı + login, ön ödemeli bakiye (videoda 25 $), API anahtarı, kod ve ekran görüntüleri MiniMax API'sine gider · context=kalıcı yok (ayrı komutla açılan oturumda çalışır) · kurulum: —
- claude-mm: bakım=bilinmiyor (kaynak yok) · çift=örtüşme yok · izin=MiniMax API anahtarı Claude Code ayarlarına eklenir (açıklama), ücretli MiniMax hesabı · context=kalıcı yok · kurulum: —
- diğer (OpenRouter, Godbot?, Fable?, Skool): bakım=bilinmiyor (repo yok) · çift=örtüşme yok · izin=OpenRouter API anahtarı + bakiye, diğerleri videoda anlatılmıyor · context=yok (kurulmuyor) · kurulum: —
## hedefler (BİLGİ)
- iş tipine göre model ayrımı (tekrarlı toplu üretim ucuz modelde, karmaşık iş Opus'ta; kalite örneklemi kabul kriteri) → CLAUDE.md (CONTEXT DİSİPLİNİ: model seçimi)
---
## ek: test/güvenlik
- yöntem: MiniMax platformunda giriş, küçük bakiye yükleme, API sayfasından yeni API anahtarı oluşturma; "API'de limit yok, yüklenen bakiye kadar" deniyor
- ayar: API anahtarı, açıklamaya konacağı söylenen prompt/kod metnine yapıştırılıp terminalde çalıştırılıyor; metnin içeriği altyazıda yok, açıklamada dosya linki yok
- komut: `claude-mm` (ASR "cloud mm" / "cloud/m") → MiniMax modeliyle Claude Code açılıyor; düz `claude` Opus ile paralel devam ediyor
- komut: `/model` → yeni terminalde MiniMax'in görünmediği, Opus'un kaldığı kontrol ediliyor
- dosya: test için boş bir klasör ("webinar" ile ilgili dosya) açılıyor
- test 1: Godbot? ekran görüntüleri (klasik panel dahil) yapıştırılıp "işi anla, 100 e-posta şablonu oluştur", sonra İngilizce versiyon isteniyor; çıktı göz gezdirilerek "gayet güzel" diye değerlendiriliyor
- test 2: aynı görsellerden opsiyonel arayüz üretimi isteniyor; sonuç altyazıda değerlendirilmiyor, "backend ve testleri de yapar" yalnız tahmin
- güvenlik: API anahtarı prompt metnine düz yazılıp terminale yapıştırılıyor; anahtar saklama ve kod/görsellerin üçüncü taraf sağlayıcıya gitmesi anılmıyor
- sayı: %50 indirimle 1M token yaklaşık 30 cent — yalnız iddia (ekrandaki fiyat sayfasına atıf, altyazıdan doğrulanamaz)
- sayı: MiniMax context limiti 1M token, Opus'a benzer — yalnız iddia
- sayı: 25 $ bakiye yüklendi — gösterildi (ekranda bakiye)
- sayı: e-posta şablonu + görsel okuma işi 5 cent tuttu — gösterildi (kullanım ekranına bakılarak)
- sayı: aynı iş "normalde muhtemelen 202 cent" (ASR belirsiz) — yalnız iddia (tahmin; Opus ile koşulmadı)
- sayı: Opus'a göre 5-6 kat ucuz (başlıkta 5x) — yalnız iddia (benchmark ya da yan yana koşu yok)
- sayı: 100 farklı e-posta şablonu üretildi — yalnız iddia (sayım yapılmadı)
- sayı: mevcut %50 indirim üstüne %12 ek indirim kodu — yalnız iddia (açıklamadaki affiliate link)
performans tavizi var mı: BELİRSİZ — e-posta şablonu ve arayüz üretiminde Opus ile yan yana koşu ya da benchmark yok; kalite yalnız "gayet güzel / Opus'a benzer" izlenimi, arayüz sonucu değerlendirilmiyor; maliyet (5 cent) gösterildi ama karşılığındaki kalite ölçülmedi
