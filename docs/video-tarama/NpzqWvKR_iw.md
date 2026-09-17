# Bu Yapay Zeka Her Sohbete Sıfırdan Başlamıyor.
kanal: Avenox · süre: 13 dk · altyazı: otomatik tr
ana iddia: Avenox kendi "İkinci Beyin" projesini V3'e çıkarıyor: Claude Code, Codex ve Antigravity'de aynı şekilde çalışan, oturum başında hook ile bağlam basan (kimlik, en son yapılanlar, açık kalanlar), agent'ın hangi konuşmanın kayda değer olduğuna kendi karar verdiği, standart güncelleme/yedekleme akışı olan bir not klasörü (Obsidian ile görüntülenebilir, isteğe bağlı); vektörleme veya lokal model şart değil, GitHub'da açık kaynak ve PR'a açık.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| avenoxai/avenoxbeyin (İkinci Beyin V3) | ÇİFT | ELENDİ | videonun kendi projesi, GitHub avenoxai/avenoxbeyin (MIT, 95★, push 16 Eyl 2026, açıklama: "Obsidian + Claude Code system with persistent cross-session memory"); önceki taramada 2n84xa99FRY'de "beyin.md ikinci beyin (Obsidian benzeri)" ÇİFT/ELENDİ — graphify + auto-memory (MEMORY.md) zaten aynı işi görüyor; hook + skill + 3 harness desteği yeni ama işlev örtüşmesi değişmedi |
| NousResearch/hermes-agent | ÇİFT | ELENDİ | "Hermes Agent'ı da senkron kullanıyorum, rakip değil" (sözlü); önceki taramada Gg35_iQWx7g, hAYPvExWmCw, XemheY_aM1g, EezLdmm8l1c, 2n84xa99FRY'de çoklu ELENDİ (ayrı sürekli ajan süreci, Claude Code'un kendisi/auto-memory ile örtüşme) |
| Obsidian | ZATEN VAR | ELENDİ | yalnız not klasörünü bağlantı grafiği olarak görselleştirmek için, kullanım opsiyonel ("neredeyse hiç bakmıyorum" — sözlü); önceki taramada Gg35_iQWx7g, hAYPvExWmCw, docs/kaynak-tarama/3.md'de defalarca ELENDİ (yalnız görselleştirme, masaüstü uygulaması) |
| openai/codex, Google Antigravity | ÇİFT | ELENDİ | 3 desteklenen ajan harness'ından ikisi (Claude Code zaten kurulu); önceki taramada 2n84xa99FRY (codex), EezLdmm8l1c (Antigravity) ELENDİ — Claude Code ile aynı işi gören alternatif harness |
| Karpathy yöntemi (sözlü referans) | ÇİFT | ELENDİ | "Karpathy'nin yöntemine benzer, oradan esinlenilen" (sözlü, repo/link verilmedi); önceki taramada hAYPvExWmCw'de Karpathy llm-wiki gist zaten ELENDİ (graphify aynı işi görüyor) |
| mem0ai/mem0 (ASR "Mem0") | YENİ | ELENDİ | V2'de "bazen gerekli olabiliyordu" (geçmiş zaman, V2'nin çözülmüş sorunlarından biri olarak anılıyor); V3'te ihtiyaç kaldırıldığı belirtiliyor, video kurulum önermiyor; kurulsaydı da auto-memory/graphify ile işlev örtüşmesi olurdu |
| Luna Agent (ASR, doğrulanamadı) | YENİ | BİLGİ | "YouTube yorumlarını çekerken Luna Agent'ları kullan, daha az limit yesin diye" (sözlü); repo/araç adı doğrulanamadı, muhtemelen Avenox'un kendi iç alt-ajan adlandırması — genel kullanılabilir bir dış araç olarak teyit edilemedi |
## ölçütler (YENİ)
- yok (tüm YENİ kalemler ilk bakışta ELENDİ/BİLGİ; ADAY adayı çıkmadı, gh api ile ayrıca doğrulama gerekmedi)
## hedefler (BİLGİ)
- yok
---
## ek: somut
- ayar: sistemde 3 ana katman — "beyin" (normal kullanım), "beyin doktor" (veri tazeliği/tekrar kayıt kontrolü), "güncelleme" (versiyon kontrolü → yedek al → güncelle, notlar korunur, yalnız "motor" değişir)
- ayar: iki mod — normal mod ve "ekonomi modu" (daha az token tüketimi için)
- ayar: hook oturum başında agent'a bağlam basıyor (kimlik, en son çalışılanlar, açık kalan işler); agent okumasa da bu bilgi zorla enjekte ediliyor
- ayar: vektörleme şart değil ("agent'ler zaten sistemin içinde bulacaktır"); lokal model kullanımı model gücüne bağlı, önerilmiyor/test edilmesi gerekiyor deniyor
- ayar: veri gizliliği — veri Avenox'a gitmiyor, kullanılan yapay zeka modeline (model sağlayıcısına) gidiyor; hassas veri vault'ta tutulmayabilir veya modelin erişemeyeceği formatta saklanabilir (kullanıcı kararı)
- dosya: klasör yapısı — agent'a özel notlar (Claude versiyonu ve diğer ajanların ortak versiyonu aynı içerik iki dosya), basit bir python script, günlük not alanı, genel bilgi notu alanı, "iş kanıtlama" alanı (modelin bir işi tamamladığını kanıtladığı yer)
- komut: kurulum — avenox.lol/beyin.md linkindeki talimatı agent'a kopyala-yapıştır ile ver, agent indirme/kurulumu kendisi tamamlıyor; manuel ZIP indirme seçeneği de var
- not: video kendi projesinin V3 sürümü, sponsor değil (önceki 2n84xa99FRY videosunda aynı proje "Serai" bağlamında farklı geçmişti); GitHub'da PR ile topluluk katkısı açık, videoda "arkadaşlar PR açtı" deniyor
- sayı: süre 768 sn (12 dk 48 sn); V1→V2→V3 evrimi anlatılıyor, V2'nin bazı kullanıcılarda Codex'te sorun çıkardığı ve Mem0'a bazen ihtiyaç duyulduğu (geçmiş sorun, sayı yok) — yalnız iddia
