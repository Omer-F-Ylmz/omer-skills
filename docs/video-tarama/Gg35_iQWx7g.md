# Yapay Zekayı Verimli Kullanmak: Skills, MCP, Ajanlar ve Token Tasarrufu
kanal: Burhan KOCABIYIK · süre: 14 dk · altyazı: otomatik tr
ana iddia: Claude Code terminalde bir ekosistem olarak kurulup skill, iş türüne göre ucuz model, otonom ajan, MCP bağlantıları, "beyin" (veri tabanı) ve on slash komutla kullanılınca işler vakit almadan otomatikleşir (sözlü, ölçüm yok).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| NousResearch/hermes-agent | YENİ | ELENDİ | ASR "Hermes"; terminalde çalışan, hafızasını kendisi iyileştiren ajan; video kendisi "çok token yakar, ucuz modelle çalıştırılır" diyor; otonom tekrar Claude Code /loop + schedule ile çift |
| openclaw/openclaw | YENİ | ELENDİ | ASR "Open Club"; Hermes'le "benzer çalışan, kendini geliştiren" ajan olarak yalnız adı geçiyor; Claude Code /loop + schedule ile çift, ayrı sürekli ajan + model maliyeti |
| İş zorluğuna göre model/effort seçimi | YENİ | BİLGİ | kolay işe (e-posta yazma, görsel/video) ucuz model, kodlamaya Opus; /effort basit işte low, genelde xhigh; CLAUDE.md'de effort/model kuralı yok |
| Claude Code: /btw, /loop, /goal?, /resume, /plugin, /mcp, /compact, /context, /effort, /model | ZATEN VAR | ELENDİ | yerleşik ("ilk 10 komut"); /goal? yerleşikliği bu oturumda doğrulanmadı; /compact ve /resume CLAUDE.md'de kural, video /resume öneriyor ama CLAUDE.md "uzun aradan sonra /resume değil yeni oturum" diyor |
| diğer: frontend-design, Claude Code'u terminalde (Visual Studio Code?) çalıştırma, claude.ai connector'larının /mcp'de görünmesi | ZATEN VAR | ELENDİ | frontend-design@claude-plugins-official kurulu; CLI zaten terminalde; connector yansıması yerleşik davranış |
| diğer: GitHub MCP (şemada) + projeyi sürekli GitHub'a yükleme, "beyin": ClickHouse / Supabase / Obsidian / vektör DB | ÇİFT | ELENDİ | GitHub: gh CLI + git, CLAUDE.md "önce CLI (gh), sonra MCP"; hafıza: graphify + auto-memory (MEMORY.md); videoda Obsidian/CRM de "vektör database" sayılıyor, kavram gevşek |
| diğer: Xiaomi MiMo-V2.5?, OpenRouter, Gmail/Google Takvim connector'ı, ChatGPT modelleri için Claude Code plugin'i (adı yok), skill dizini sitesi (adı yok), SEO/copywriting/ürün videosu skill'leri, OpenAI Codex, Google Antigravity, Cursor, Fable? modeli, rakip reklam analiz ajanı | YENİ | ELENDİ | ad/repo verilmeyenler değerlendirilemez; model/connector'lar API anahtarı ya da geniş posta/takvim erişimi ister; Codex/Antigravity/Cursor Claude Code ile çift; reklam ajanı kişisel iş akışı, kapsam dışı |
## ölçütler (YENİ)
- NousResearch/hermes-agent + openclaw/openclaw: bakım=hermes-agent pushed 2026-09-15, 245.762 yıldız, arşiv değil; openclaw pushed 2026-09-15, 389.756 yıldız, arşiv değil · çift=otonom/tekrarlı iş Claude Code /loop + schedule, hafıza graphify + auto-memory · izin=ayrı sürekli çalışan ajan süreci, model sağlayıcı hesabı + token maliyeti (video: "çok fazla token yakar"), bilgisayarda terminal erişimi · context=Claude Code oturumuna yük yok (ayrı süreç) · kurulum: —
- İş zorluğuna göre model/effort seçimi: bakım=— (teknik) · çift=örtüşme yok (CLAUDE.md "basit işlerde bu ağırlık uygulanmaz" süreç ağırlığı, model/effort değil) · izin=yok · context=CLAUDE.md'ye tek kural satırı · kurulum: —
- diğer (MiMo-V2.5?, OpenRouter, Gmail/Takvim connector'ı, ChatGPT plugin'i, skill dizini, Codex, Antigravity, Cursor, Fable?): bakım=bilinmiyor (repo videoda yok) · çift=Codex/Antigravity/Cursor Claude Code; ChatGPT plugin'i /model; skill dizini plugin marketplace + skill-creator · izin=MiMo/OpenRouter API anahtarı + ücretli token; Gmail/Takvim Google login + posta/takvim okuma; ChatGPT modelleri OpenAI hesabı · context=connector MCP tool şemaları her oturum (sayı videoda yok), diğerleri yok · kurulum: —
## hedefler (BİLGİ)
- Mekanik/basit işte /effort low ya da subagent'e ucuz model; kod ve tasarım kararında üst model + yüksek effort → CLAUDE.md (CONTEXT DİSİPLİNİ: model/effort seçimi)
---
## ek: somut
- ayar: /effort — "Ultra" (ASR "Ultra Koda") daha fazla düşünür, daha fazla token harcar; öneri xhigh (ASR "XI"); çok basit işte low (sözlü)
- ayar: /model — konuşmacı şu an Opus 5 kullanıyor; Fable?, Sonnet, Haiku (ASR "HKQu") ya da plugin ekleyerek ChatGPT modelleri seçilebilir (sözlü)
- komut: /btw (ASR "slbtv") ajan çalışırken yan soru; /loop "durma, sürekli yeni bir şey oluştur" tarzı tekrarlı iş; /goal? (ASR "slashgo") hedefe ulaşana kadar tekrar, örnek: "benim için profesyonel bir web sitesi oluştur, aynı rakibim ... gibi olsun"
- komut: /resume önceki chat'i bulur (bilgisayar kapanınca chat kaybolur iddiası); /plugin(s) yüklü skill ve plugin'ler; /mcp bağlı uygulamalar, claude.ai'de bağlanan connector'lar (ör. Gmail) burada da görünür; /compact chat'i özetler, sonraki mesajlarda daha az token; /context token kullanımı
- komut: kurulum — aramada "claude terminal" ile çıkan ilk siteden prompt kopyalanıp terminale yapıştırılır, hata için sayfada kopyala-yapıştır komutlar var (komut metni altyazı/açıklamada yok)
- dosya: yok (videoda dosya adı geçmiyor)
- sayı: arkada yaklaşık 16 terminal (e-posta takibi, reklam üretimi, topluluk verisi) — ekranda gösterildiği söyleniyor, altyazıdan doğrulanamaz
- sayı: skill sitesinde 1 milyondan fazla skill — yalnız iddia
- sayı: Xiaomi modeli Opus'tan yaklaşık 11 kat ucuz, e-posta yazmada Opus ile aynı sonuç — yalnız iddia
- sayı: reklam ajanı geçen hafta (27 Temmuz) 1013 rakip reklamı tespit etti; günlük hedef 10 kazanan reklam; haftalık müşteri başı 30 euro hedefi, geçen hafta 32-33 ise bu hafta 30'a çekiliyor; 7/24 çalışıyor — rapor ekranda örnek olarak açıldı (sözlü), sonuç ölçümü yok
- sayı: saatler alacak e-posta işi 15 dakikada — yalnız iddia; MCP ile "binlerce" uygulama bağlanabilir — yalnız iddia
- sayı: OpenRouter'da Hermes kullanımında Opus modelleri çok az görünür, sebep token maliyeti — ekranda gösterildiği söyleniyor, sayı yok
- sayı: "ilk 10 slash komut" — videoda sayılan 10: btw, loop, goal, resume, plugins, mcp, compact, context, effort, model
