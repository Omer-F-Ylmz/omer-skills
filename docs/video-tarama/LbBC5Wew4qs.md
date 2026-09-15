# Claude Code + OpenAI Codex İki Dev Yapay Zekayı Aynı Anda Kullan
kanal: Burhan KOCABIYIK · süre: 14 dk · altyazı: tr manuel
ana iddia: Codex plugin'i Claude Code içine kurulup mimari ve ilk kod Opus'a, inceleme ve hata tespiti daha az token harcayan Codex'e (GPT-5.4) yaptırılırsa token azalır, hata payı düşer (ölçüm gösterilmedi).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| openai/codex-plugin-cc (Codex plugin for Claude Code) | YENİ | ADAY | resmi OpenAI plugin'i; videoda kurulum, Codex status ve review komutu anlatıldı; README'de ayrıca adversarial-review/rescue/transfer; aynı model değil GPT ile çapraz review; ChatGPT hesabı (Free dahil) ya da API anahtarı |
| review bulgu dosyası akışı (Codex tüm projeyi tarar, hataları log dosyasına yazar; Claude Code plan modunda yalnız o dosyadaki hataları çözer) | YENİ | BİLGİ | proje tekrar tekrar taranmadığı için token azalır (iddia); CLAUDE.md delege+özet diyor ama kalıcı bulgu dosyası ve "yalnız listelenenleri çöz" adımı yok |
| iş türüne göre model yönlendirme (mimari/plan/ilk kod Opus; inceleme, test, küçük değişiklik Codex; token limiti dolunca Codex) | YENİ | BİLGİ | CLAUDE.md'de model seçimi kuralı yok; videodaki oranlar (%30/70, %80/20, %40/60) birbiriyle çelişiyor, kanıtsız, kurala girmez |
| diğer: Claude Code /plugin marketplace add + kurulum kapsamı (project/local) + /reload-plugins + /plugin ekranı (MCP listesi), Claude Code VS Code eklentisi, plan modu, /compact, MD dosyaları | ZATEN VAR | ELENDİ | Claude Code yerleşik özellikleri; /compact zaten CLAUDE.md CONTEXT DİSİPLİNİ'nde |
| diğer: Sora 2 (OpenAI), VS Code, Instantly, n8n, "Codex prompt yazmada daha iyi" ve "Claude Code terminalde eklentiden iyi" iddiaları | YENİ | ELENDİ | Sora 2 video üretim modeli, geliştirme akışı dışı; VS Code yalnız terminal kabuğu; Instantly/n8n açıklamada affiliate link, videoda kullanılmadı; iddialar yalnız izlenim |
## ölçütler (YENİ)
- openai/codex-plugin-cc: bakım=pushed_at 2026-07-08, 33.185 yıldız, archived=false · çift=kısmen /code-review (yerleşik) ve superpowers:requesting-code-review (aynı iş, aynı model); farklı modelle çapraz review ve Codex'e görev devri örtüşmüyor · izin=ChatGPT hesabı ya da OpenAI API anahtarı + codex login, Node 18.18+, global npm (@openai/codex), SessionStart hook, opsiyonel Stop hook review gate (README: kullanım limitini hızla tüketebilir), Codex'in yerel repo erişimi · context=her oturum 8 slash komut + codex:codex-rescue alt-ajan açıklaması; Codex işi yalnız çağrılınca · kurulum: /plugin marketplace add openai/codex-plugin-cc → /plugin install codex@openai-codex → /reload-plugins → /codex:setup (README'den doğrulandı)
- teknikler (bulgu dosyası akışı, model yönlendirme): bakım=yok (teknik) · çift=bulgu dosyası kısmen CLAUDE.md CONTEXT DİSİPLİNİ (delege + özet) ve /code-review --fix (aynı oturumda uygular, kalıcı dosya yok); model yönlendirme örtüşme yok · izin=yok · context=CLAUDE.md'ye birer satır, her oturum · kurulum: —
- diğer YENİ (Sora 2, VS Code, Instantly, n8n, iddialar): bakım=bilinmiyor (ürün/servis, repo verilmedi) · çift=VS Code terminali Claude Code CLI ile aynı iş; diğerleri örtüşme yok · izin=Sora 2 ChatGPT hesabı; Instantly/n8n hesap; VS Code masaüstü kurulum · context=0 (kurulmaz) · kurulum: —
## hedefler (BİLGİ)
- tam proje review'unu bir kez ayrı ajana yaptırıp bulguları kalıcı dosyaya yazdır; düzeltme oturumu plan modunda yalnız o dosyadaki maddeleri çözsün, projeyi yeniden taramasın → CLAUDE.md (CONTEXT DİSİPLİNİ: review bulgu dosyası)
- mimari/plan/ilk iskelet güçlü modelde; inceleme, test, küçük değişiklik daha ucuz model ya da ajanda; limit dolunca devret → CLAUDE.md (CONTEXT DİSİPLİNİ: delege edilen işte model seçimi)
---
## ek: test/güvenlik
- araç: openai/codex-plugin-cc — Claude Code içinde Codex; video 1 Nisan'da "iki gün önce çıktı" diyor
- araç: Codex güçlü yönleri (izlenim): mevcut kodu analiz, hata tespiti, mantıksal şeyleri kaçırmama, prompt yazma (YouTube otomasyonu, e-ticaret, Sora 2 promptları); zayıf: büyük resim/mimari planlama, eksik bilgide doğru soru soramama, sıfırdan kodda Opus kadar iyi değil, kuralcı, halüsinasyon/körlük
- araç: Claude Code güçlü yönleri (izlenim): sıfırdan planlama, değişen gereksinime uyum; zayıf: çok token, uzun oturumda bağlam kaybı, istisnalarda gözden kaçırma/AI slop, kendi kodundaki hatayı bulamama ("çözdüm diyor ama çözmüyor"; nadir, büyük ve iyi planlanmamış projede)
- yöntem: mimari + ilk kod taslağı Claude Code (Opus 4.6); Codex yazılan kodu inceler, hataları tespit eder, sonra üretime/canlıya almaya odaklanır
- yöntem: Codex'e istem "Projeyi tamamen kontrol et, yeni bir log dosyası oluştur, bulduğun hataların hepsini yaz" → Claude Code plan modunda "o dosyadaki hatalara bak, sadece bu hataları çöz"
- yöntem: token limiti dolunca, ya da proje bir yere geldikten sonra küçük değişiklik ve yalnız test işlerinde Codex'e geç
- yöntem: uzun oturumda bağlam kaybına karşı compact
- komut: /plugin marketplace add openai/codex-plugin-cc (ASR "plugin marketplace open AI codex CC"); ilk denemede yanlış yazıldı ("kod değil codex olacaktı"), marketplace'te bulunamadı, düzeltilince geldi
- komut: /reload-plugins (birkaç kez), ardından plugin yeniden yüklendi; kurulum komutunun metni altyazıda okunmadı
- komut: Codex status sorgusu ("her şey çalışıyor mu" kontrolü; ASR "Codex'in statüsünü sorabilirim")
- komut: Codex review komutu — derinlemesine hata tespiti, ardından detaylı inceleme raporu
- ayar: kurulum kapsamı — project scope olabilir dendi, local scope seçildi
- ayar: VS Code'da yeni klasör açılınca "Trust" onaylandı; Claude Code eklenti yerine VS Code entegre terminalinde claude ile çalıştırıldı ("daha iyi çalışır", izlenim)
- ayar: kurulumdan sonra Codex hata verdi çünkü API yok; Codex'e bağlanmak (API anahtarı) gerekiyor, anahtar alma adımı gösterileceği söylendi ama altyazıda yok
- ayar: /plugin ekranında marketplace altında OpenAI Codex görünmeli; aynı ekranda MCP'ler de listeleniyor
- ayar: ChatGPT aboneliği Codex için çalışıyor, ekstra ücret yok (iddia); yazar Claude Max kullandığı için token limitini kolay doldurmuyor
- dosya: demo klasörü "YouTube Codex"; yazarın mevcut web sitesi projesi; Codex'in yazacağı hata log dosyası (adı verilmedi); Claude Code'a yüklenen MD dosyaları
- sayı: GPT-5.4 bazı konularda Opus 4.6'yı benchmark'ta geçiyor — yalnız iddia (ekrandaki benchmark'a atıf var, rakam ve kaynak altyazıda yok)
- sayı: Codex ile Claude Code projeleri 10X iyileşir — yalnız iddia
- sayı: müşteri projesinde token masrafı 30 dolardan fazla değil (satış fiyatı ASR'de kayıp, ".00 dolar"); "10 dolar daha indirimli" diye Codex'e geçmeye değmez — yalnız iddia
- sayı: ideal oran %30 Claude / %70 Codex; başlangıçta %80 Claude / %20 Codex; projeye göre %40 Claude / %60 Codex — yalnız iddia (oranlar birbiriyle çelişiyor)
- sayı: aynı istemde Claude Code daha hızlı ve daha çok token, Codex daha yavaş ama çok daha az token — yalnız iddia (karşılaştırma koşusu gösterilmedi)
- sayı: context penceresi 2,5 / 3 / 5 milyon tokene çıkınca halüsinasyon ve körlük sorunları kendiliğinden çözülecek — yalnız iddia (tahmin)
- sayı: plugin kayıttan 2 gün önce çıktı, kayıt tarihi 1 Nisan (açıklama: 1 Nisan 2026), izleyici gördüğünde ~5 gün — yalnız iddia
performans tavizi var mı: EVET — Codex'e devredilen işte hız tavizi (aynı istemde daha yavaş) ve mimari/planlama/sıfırdan kodda Opus'tan zayıf kalite, karşılığında daha az token ve daha iyi hata tespiti iddiası; miktar verilmedi; dayanağı: yalnız izlenim (benchmark'a atıf var, rakam yok)
