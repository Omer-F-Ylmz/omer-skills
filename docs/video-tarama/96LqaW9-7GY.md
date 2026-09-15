# Claude token Maliyetini %80 Düşürün (Codex + Claude code)
kanal: Burhan KOCABIYIK · süre: 14 dk · altyazı: otomatik tr
ana iddia: Claude Code API fiyatıyla Codex/Gemini'den 4-5 kat pahalı ama Opus+Sonnet karışımı ve token optimizasyonuyla maliyet düşer, çıkardığı iş değeri de farkı haklı çıkarır (fiyat hesabı, kalite ölçümü yok).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Claude Code: /model | ZATEN VAR | ELENDİ | yerleşik; videoda "model yazarak" Opus/Sonnet değiştirme olarak geçiyor |
| Görev tipine göre model karışımı (Opus %20 / Sonnet %80, test işi ucuz modele) | YENİ | BİLGİ | iddia: 1M token 33 $ → 11 $; testte Codex/Gemini "gayet güzel"; kalite etkisi ölçülmedi; CLAUDE.md'de model seçimi kuralı yok |
| OpenAI Codex | YENİ | ELENDİ | ayrı ücretli OpenAI hesabı; Claude Code'dan test devretme yolu gösterilmedi; video kodlamada "aynı sonucu vermez" diyor |
| Google Gemini 2.5 / Google Antigravity? | YENİ | ELENDİ | ASR "Cemin 2.5", "Gravity"; ayrı hesap, yalnız fiyat karşılaştırması ve "testte güzel" izlenimi, entegrasyon yok |
| diğer: Claude Code'a güvenlik açığı kontrolü, token optimizasyonu (başka videoya atıf), kural listesi, Claude Pro/Max/Max 20x | ZATEN VAR | ELENDİ | yerleşik /security-review; CLAUDE.md CONTEXT DİSİPLİNİ ve genel kurallar; platform planı, bu videoda somut yöntem yok |
| diğer: DOA topluluğu (skool.com/doa), benburhan.gumroad.com, ChatGPT Plus/Pro, Google AI Pro? | YENİ | ELENDİ | tanıtım ya da abonelik planı; kurulacak araç değil |
## ölçütler (YENİ)
- Görev tipine göre model karışımı: bakım=bilinmiyor (teknik, repo yok) · çift=örtüşme yok (/model ile uygulanır; CLAUDE.md'de model seçimi kuralı yok) · izin=yok · context=CLAUDE.md'ye tek kural satırı, her oturum · kurulum: —
- OpenAI Codex: bakım=openai/codex pushed 2026-09-15, 124.362 yıldız, arşiv değil · çift=kurulu eklenti yok; işi Claude Code'un kendisiyle aynı · izin=ücretli OpenAI hesabı (video ChatGPT Plus/Pro üzerinden anıyor) ya da API anahtarı, ayrı araç kurulumu · context=Claude oturumuna kalıcı yük yok (ayrı araç) · kurulum: —
- Google Gemini 2.5 / Antigravity?: bakım=bilinmiyor (videoda repo yok) · çift=işi Claude Code'un kendisiyle aynı · izin=Google hesabı, Google AI Pro? ücretli abonelik · context=Claude oturumuna kalıcı yük yok (ayrı araç) · kurulum: —
- diğer (DOA, Gumroad, ChatGPT Plus/Pro, Google AI Pro?): bakım=bilinmiyor · çift=örtüşme yok · izin=hesap/üyelik, abonelikler ücretli · context=yok · kurulum: —
## hedefler (BİLGİ)
- Mimari/kritik işte Opus, rutin işte Sonnet; test/sayfa kontrolü gibi rutin doğrulamayı ucuz modele ver → CLAUDE.md (CONTEXT DİSİPLİNİ: model seçimi)
---
## ek: test/güvenlik
- yöntem: uygulama içi testlerde (sayfaların doğru çalışıp çalışmadığını anlamak için) Codex ya da Gemini kullan; nasıl bağlanacağı, hangi komutla çalışacağı gösterilmedi
- yöntem: Claude Code'a güvenlik açıklarını kontrol ettirme; araç/komut adı verilmedi, sonuç gösterilmedi
- yöntem: YouTube otomasyon projesinde hata ayıklama ve test süreçleri Claude Code içinde yapıldı (ayrıntı yok)
- yöntem: kural listesi iyiyse Claude Code "tek seferde doğru yazar", ucuz modellerle aynı kodu "beş kere düzeltmek" gerekir (sözlü)
- yöntem: token optimizasyonu yapılmazsa hangi model olursa olsun tokenler hızlı biter; yöntem başka videoya bırakıldı
- komut: Claude Code içinde "model" yazarak Opus/Sonnet değiştirme (/model); başka komut geçmiyor
- ayar: yok (videoda ayar adı geçmiyor)
- dosya: yok (videoda dosya adı geçmiyor)
- sayı: 1M token API fiyatı Opus 33 $, Opus+Sonnet 11 $, Codex ~3 $, Gemini 4 $, Sonnet 3.7 6 $ — yalnız iddia (tabloyu yapay zekaya çıkarttırdığını, Nisan 2026 web verisi olduğunu söylüyor, "hata yoktur diye düşünüyorum")
- sayı: 750 kelime ≈ 1000 token — yalnız iddia
- sayı: %20 Opus + %80 Sonnet ile 33 $ → 11 $ — yalnız iddia (hesap yöntemi gösterilmedi)
- sayı: token optimizasyonuyla %80 azalma (başlık ve sözlü) — yalnız iddia (yöntem bu videoda yok)
- sayı: kurumsal web sitesi ~150.000 token, 1.78 $; Gemini'yle 50 cent, Codex'le 40 cent olurdu — yalnız iddia (site ekranda gösterildiği anlaşılıyor; token sayacı ve Codex/Gemini çalıştırması yok, "-saydım" kalıbıyla varsayımsal)
- sayı: YouTube otomasyon sistemi ~200.000 token, 2.40 $; Codex'le 57 cent, Gemini'yle 80 cent olurdu — yalnız iddia (aynı bölümde "40 cente mal oldu" deniyor, 2.40 $ ile çelişiyor, ASR olabilir)
- sayı: Prototipal? UGC factory + sinematik bölüm ~1M token, 12 $; Gemini'yle 4 $, OpenAI ile 3 $ olurdu — yalnız iddia
- sayı: yalnız Opus ile web sitesi 5 $, YouTube botu 6 $, uygulama 33 $ — yalnız iddia
- sayı: Claude Code Codex'ten 4-5 kat pahalı — yalnız iddia (fiyat oranı, kalite karşılaştırması yok)
- sayı: test işini Codex/Gemini'ye vermek token kullanımını "yarı yarıya etkileyebilir" — yalnız iddia
- sayı: 50M token ≈ 50 uygulama; 20-50M token harcanacaksa başka modeller ve daha kompleks sistem gerekir — yalnız iddia
- sayı: ChatGPT Plus 256.000 token context, 3 saatte 160 mesaj, Claude Code erişimi yok, kod gücü orta; ChatGPT Pro GPT-5 + o3, kod gücü yüksek — yalnız iddia (yapay zekaya hazırlatılmış tablo)
- sayı: Claude Pro ~5 saatlik çalışma, kod gücü çok yüksek; Max 20x aylık 200 $ ve 15M token; API'de 1M token ~12 $, abonelik daha avantajlı — yalnız iddia
- sayı: 2,5 yılda 50.000 € yazılım masrafı; aynı iş normalde 6 hafta ve Türkiye'de 2.000-3.000 $ (2.500 $ proje) yerine 12 $ ve 2 gün — yalnız iddia
- sayı: Claude Code'la web sitesi 2 saatte çıkar, 300-500 $'a satılır; 5/10/25 $ harcama farkı önemsiz — yalnız iddia
- sayı: video Nisan 2026'da çekildi, 3 ay sonra geçerli olmayabilir — yalnız iddia (konuşmacı uyarısı)
- sayı: açıklamada "tüm kaynaklar %100 ücretsiz", "30 dakikada Claude Code'un %95'i", "Claude Code Full Kurs (2 saat)" — yalnız iddia (tanıtım listesi)
performans tavizi var mı: EVET — kodlama/mimari/güvenlikte Codex ve Gemini'nin Claude Code'la "aynı sonucu vermediği", ucuz modelde aynı kodu tekrar düzeltmek gerektiği söyleniyor, fark sayıyla verilmiyor; test işinde taviz söylenmiyor ("gayet güzel"); dayanağı: yalnız izlenim (örneklerde Codex/Gemini yalnız fiyatla hesaplandı, yan yana çıktı ya da benchmark yok)
