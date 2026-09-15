# Claude Code Skills Rehberi: Kendi Yapay Zeka Yeteneklerinizi Sıfırdan Oluşturun
kanal: Burhan KOCABIYIK · süre: 22 dk · altyazı: otomatik tr
ana iddia: Skill, Claude'a bir iş akışını adım adım öğreten paketlenmiş kural setidir (zorunlu SKILL.md + isteğe bağlı script/referans/şablon); MCP yalnız araç bağlantısı verir, net kullanım senaryosu, "ne yapar + ne zaman" açıklaması, test ve skill-creator ile tutarlı çalışan ve Modal'a deploy edilip satılabilen ajanlar kurulur (Anthropic'in 33 sayfalık dokümanının slayt özeti; canlı skill oluşturma gösterilmiyor).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| remotion-dev/skills | YENİ | ADAY | videoda "Remotion aslında bir yetenek", prompt ile video oluşturma ve editleme örneği (demo yok); README'de 12 Remotion skill'i (create, markup, studio, render…); kurulu sette video üretimi yok; yalnız video projesinde anlamlı |
| paperclipai/paperclip | YENİ | ELENDİ | ASR "Paper Clip": "bir sürü ajan eğitebiliyorsunuz, kısmen yetenek kısmen plugin" (sözlü, ayrıntı yok); ayrı ajan yönetim uygulaması, iş akışı kapsamı dışı |
| Pinecone · Modal (modal.com) | YENİ | ELENDİ | Pinecone: 1000 PDF/fatura vektör DB'ye yüklenip skill referansı olur (iddia, demo yok); Modal: skill'i buluta deploy edip saatlik çalıştırma ya da API anahtarıyla çağırma (yalnız site gösterildi); ikisi de hesap + anahtar ister, veri/kod dış servise çıkar |
| token/kredi harcayan ya da çok veri döndüren araç çağrısına sayısal tavan + filtre | YENİ | BİLGİ | sözlü: limitsiz blog görsel/video üretimi tüm token'ı harcar, "günlük maks 20 resim / 30 video" tavanıyla model kalan adedi kendisi sayar; ölçüm yok; ydO2_a97J6g'deki aynı BİLGİ'nin ikinci kaynağı |
| diğer: skill-creator · frontend-design · skill anatomisi (SKILL.md zorunlu + scripts/references/şablon) · description "ne yapar + ne zaman kullanılır" formülü · 10-20 test sorgusuyla tetiklenme sayımı, aynı isteği 3-5 kez koşma · kebab-case klasör adı · taslak → ekran görüntüsü → kontrol → yeniden üret · çoklu MCP koordinasyonu | ZATEN VAR | ELENDİ | kurulu plugin'ler · skill-creator (Anatomy of a Skill, description, 20 trigger eval sorgusu, benchmark) · superpowers:writing-skills (tireli ad) · frontend-craft Bölüm 2/9 · Claude Code yerleşik |
| diğer: talimata uymuyorsa "asla/her zaman" kesin ifadeleri + numaralı adımlar · skill klasörüne README koymama · dosya türüne göre dallanma ("bağlam farkındalığı") · Vercel · n8n · Instantly · Notion/Asana/Linear/Figma/Slack/Google MCP örnekleri · Nano Banana | YENİ | ELENDİ | kesin ifade kurulu skill-creator'ın "ağır MUST'lar yerine nedenini açıkla" önerisiyle çelişir · repo skill klasöründe README zaten yok · genel tavsiye · deploy/otomasyon/satış servisleri ve yalnız adı geçen örnekler, kapsam dışı |
## ölçütler (YENİ)
- remotion-dev/skills: bakım=pushed_at 2026-09-15, 4584 yıldız, archived=false · çift=örtüşme yok · izin=Node + npx skills CLI; skill'ler Remotion (React) projesi ve render için; README'de API anahtarı/lisans satırı yok · context=12 skill; global kurulursa her oturum 12 açıklama, proje kapsamlı kurulursa yalnız o projede · kurulum: npx skills add remotion-dev/skills
- paperclipai/paperclip: bakım=pushed_at 2026-09-15, 80734 yıldız, archived=false, MIT · çift=kısmi: superpowers subagent-driven-development / dispatching-parallel-agents + Claude Code alt-ajanları · izin=ayrı uygulama kurulumu + yönettiği ajanların hesap/erişimi (README okunmadı, ayrıntı bilinmiyor) · context=0 kalıcı (Claude Code dışında uygulama) · kurulum: —
- Pinecone · Modal: bakım=bilinmiyor (servis) · çift=Pinecone kısmen graphify (yerel doküman → sorgulanabilir graf); Modal'ın saatlik çalıştırma kısmı Claude Code /schedule (bulutta cron ajanı) ile çift · izin=ikisi de hesap + API anahtarı, veri/kod dış buluta; ücret planı videoda yok · context=videoda MCP olarak bağlanmıyor, 0 kalıcı · kurulum: —
- teknikler (tavan/filtre, kesin ifade, README'siz klasör, dosya türüne göre dallanma): bakım=— (teknik) · çift=filtre kısmen CLAUDE.md context disiplini (log/CI çıktısı alt-ajana); kesin ifade skill-creator ile çelişir · izin=yok · context=kurala yazılırsa ~1 satır · kurulum: —
- diğer (Vercel, n8n, Instantly, MCP örnekleri, Nano Banana): bakım=bilinmiyor · çift=örtüşme yok · izin=hesap/login/API anahtarı · context=0 (videoda kurulum yok) · kurulum: —
## hedefler (BİLGİ)
- token/kredi harcayan üretim ya da çok veri döndüren araç çağrısı yaptıran prompt'a sayısal tavan (ör. "günde en fazla N görsel, N video") ve çıktı filtresi yaz → CLAUDE.md (ücretli üretim/API çağrıları)
---
## ek: somut
- dosya: skill.md (ana dosya, zorunlu); scripts (isteğe bağlı çalıştırılabilir kod, ör. her saat başı çalışan ajan); references (isteğe bağlı dokümantasyon); şablonlar (isteğe bağlı); README skill klasörünün içine değil; klasör adı kebab-case (tireli)
- ayar: description formülü "bu otomasyon şunu yapar, şu zaman kullanılır"; kötü örnek "proje yönetimi için bana skill oluştur"; iyi örnek "Linear'da sprint planlama ve görev oluşturma; kullanıcı yeni sprint atamak ya da görevleri önceliklendirmek istediğinde kullanın; Linear MCP sunucusunu gerektirir" (sözlü özet)
- ayar: tavan "günlük maksimum 20 resim oluşturabilirsin", "günlük maksimum 30 video oluşturabilirsin"; blog başına en az 2-3 görsel + 2 video (sözlü)
- ayar: kendini düzeltme kuralı "ilk taslağı oluştur, ekran resmini al, kontrol et, doğru değilse tekrar oluştur" (sözlü)
- ayar: sorun giderme: skill yüklenmiyorsa dosya/klasör adlarını kontrol et; talimata uymuyorsa adımları numaralandır ve kesin ifade kullan; yanlış/hiç tetiklenmiyorsa description formülünü düzelt; araçtan çok veri dönüp token sınırı aşılıyorsa filtre koy
- ayar: başlamadan kontrol listesi: görev manuel başarıyla tamamlandı mı · MCP'ler kurulu ve çalışıyor mu · dosya ve klasör adları doğru mu · description "ne yapar + ne zaman" doğru mu · adımlar numaralı mı
- komut: "slash skill" yazarak skill creator'ı çağırma (sözlü, tam komut adı söylenmiyor); prompt "projeyi modal.com'a deploy et"; GitHub'a yükle → Vercel'de deploy et (sözlü, komut gösterilmiyor)
- sayı: Anthropic'in skill dokümanı 33 sayfa — yalnız iddia (doküman adı/linki açıklamada yok)
- sayı: 10-20 test sorgusu çalıştırıp kaç kez otomatik yüklendiğini say; aynı isteği 3-5 kez çalıştır (ASR "1020", "3 be") — öneri, ölçüm gösterilmedi
- sayı: skill-creator ile 15 mesaj + 10 dk + 3 başarısız API yerine 2 mesaj + 1 dk — yalnız iddia (ölçüm yok)
- sayı: MCP server geliştirme "3 ayda yaparız" denen işten 30 dakikaya düştü — yalnız iddia
- sayı: MCP terimi yaklaşık 1 yıl önce çıktı; MCP/skill 3 yıl sonra en başarılı uygulamalar olacak ("23 yıl" ASR, 2-3 yıl?); 3-6 ay sonra Claude Code her şirkette zorunlu olacak — yalnız iddia/öngörü
- sayı: YouTube otomasyonu: her 2 ya da 5 saniyede bir kare, 1000 resim, 1000 × 5 sn = 5.000 sn video — yalnız anlatım, demo yok
- sayı: Pinecone'a 1000 PDF / 1000 fatura yükleme; 100.000 kullanıcı datası ya da 1 milyon session analizinde vektör DB daha iyi çalışır — yalnız iddia
- sayı: rakip içeriğini kopyalayan Instagram carousel otomasyonu aylık 300 dolara satılır — yalnız iddia
- sayı: "1000 araç verin, ne yapacağını bilmiyorsa tutarsız sonuç alır"; power user örneği "saat 9:00'da kontrol et", "her gün YouTube kanalıma iki video at" — sözlü örnek
- sayı: Claude Code sıfırdan 2 saatte öğrenilir, yarım saatte %80-85'i; açıklamada kurslar 2 saat / 3 saat / 8 saat ve "tüm kaynaklar %100 ücretsiz"; yazarın ilk girişimi 4 yıl önce — yalnız iddia
