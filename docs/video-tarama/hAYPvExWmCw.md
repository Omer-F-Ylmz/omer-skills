# Hafızayı Sıfırdan Anlattım - Claude Code, Obsidian, NotebookLM, Hermes
kanal: Selma Kocabıyık · süre: 52 dk · altyazı: otomatik tr
ana iddia: Ajan hatırlamaz, doğru dosyayı okur; hafıza sistemi yazma+okuma yolu ile depo / harita (index.md) / kural dosyası (CLAUDE.md) kurmaktır, Claude Code'da bunu Karpathy'nin LLM Wiki deseni (INGEST/QUERY/LINT) elle, Hermes Agent her turda otomatik yapar; Obsidian yalnız görselleştirir, NotebookLM keşif için yeter ama kısıtlıdır (token tasarrufu ölçümsüz iddia).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| selmakcby/claude-obsidian-kit (+ selmakcby/knowledge-pipeline, Karpathy llm-wiki gist) | ÇİFT | ELENDİ | LLM Wiki deseni: CLAUDE.md şema + index.md harita + log.md, INGEST/QUERY/LINT skill'i, vault linter; graphify (girdi → kalıcı bilgi grafı + query) aynı işi yapıyor; kit push 2026-09-04, 9★ |
| selmakcby/vault-radar | YENİ | ELENDİ | ajanın vault'ta hangi notları gerçekten okuduğunu canlı gösterir; Obsidian vault'u yok, graphify kullanılıyor, 8★ tek geliştirici |
| NousResearch/hermes-agent | YENİ | ELENDİ | her turdan sonra arka plan kopyası öğrenileni memory/skill'e yazar (SOUL.md, skills, memories); ayrı ajan çalışma ortamı, Claude Code'un yerine geçer, kurulacak eklenti değil |
| notebooklm-mcp (npm; PleasePrompto/notebooklm-mcp?) · PleasePrompto/notebooklm-skill | YENİ | ELENDİ | Claude Code'dan NotebookLM defterine soru; iki repo da arşivli, Google oturumu + tarayıcı otomasyonu, video: MCP ayrıca token yakar, kodda NotebookLM işe yaramaz |
| Claude Code: auto memory (/memory, MEMORY.md), cleanupPeriodDays; grep/find/wc | ZATEN VAR | ELENDİ | yerleşik: auto memory user/feedback/project/reference yazar, transkript saklama süresi ayarı; kullanıcıda MEMORY.md zaten aktif; grep/find/wc Bash'te mevcut |
| kalıcı hafıza notuna sabit boyut sınırı, dolunca eskiyi sil/birleştir (Hermes deseni) | YENİ | BİLGİ | Hermes not defteri 2200 karakter, her tur enjekte, dolunca temizlik zorunlu (iddia); global CLAUDE.md CONTEXT DİSİPLİNİ'nde hafıza dosyası boyut kuralı yok |
| diğer: Obsidian, NotebookLM, Anthropic Memory Tool (API), sentence-transformers (Hugging Face) | YENİ | ELENDİ | Obsidian yalnız görselleştirir, bağlantı kuramaz, içeriği anlamaz (video); NotebookLM yükleme kısıtlı, kodda işe yaramaz (video); Memory Tool API geliştirme aracı (yalnız açıklamada link); sentence-transformers yalnız RAG anlatımında örnek |
## ölçütler (YENİ)
- selmakcby/vault-radar · NousResearch/hermes-agent: bakım=vault-radar push 2026-08-31, 8★, MIT; hermes-agent push 2026-09-15, 245.8k★, MIT; ikisi de arşiv değil · çift=örtüşme yok (hermes-agent kurulu setle değil, Claude Code'un kendisi ve auto memory ile rakip) · izin=vault-radar Obsidian vault + Claude Code'a bağlanma (mekanizma doğrulanmadı); hermes-agent ayrı ajan kurulumu, arka planda sürekli servis + zamanlanmış görev (video), model sağlayıcı erişimi · context=vault-radar bilinmiyor; hermes-agent Claude Code'a kalıcı yük yok · kurulum: —
- notebooklm-mcp · PleasePrompto/notebooklm-skill: bakım=ikisi de arşivli (son push 2026-09-10; mcp 3.4k★, skill 7.8k★, MIT); npm paketi ↔ repo eşleşmesi doğrulanmadı · çift=örtüşme yok · izin=Google hesabıyla kalıcı oturum ve tarayıcı otomasyonu (repo açıklaması), npm paketi · context=MCP tool şemaları her oturum (sayı bilinmiyor); skill açıklaması her oturum · kurulum: —
- hafıza notuna boyut sınırı: bakım=uygulanmaz · çift=kısmi: Claude Code auto memory MEMORY.md'nin yalnız ilk 200 satır / 25 KB'ını yükler (kesme, temizlik değil) · izin=yok · context=CLAUDE.md'de tek satır, her oturum · kurulum: —
- diğer: bakım=bilinmiyor · çift=Memory Tool kısmen Claude Code auto memory; diğerleri örtüşme yok · izin=Obsidian masaüstü uygulaması; NotebookLM Google hesabı; Memory Tool API anahtarı; sentence-transformers Python paketi · context=0 · kurulum: —
## hedefler (BİLGİ)
- kalıcı hafıza/not dosyasına (ör. MEMORY.md) üst sınır koy; yeni not eklemeden önce eskimiş notu sil ya da birleştir → CLAUDE.md (CONTEXT DİSİPLİNİ: hafıza dosyası)
---
## ek: somut
- ayar: Claude Code /memory ekranında "Auto memory: on" ve otomatik kayıtlar listeleniyor; cleanupPeriodDays ile transkript saklama süresi (varsayılan 30 gün, değiştirilebilir); wiki kurulumunda Claude Code otomatik moda alındı
- ayar: Obsidian graph görünümünde oklar açıldı; yetim düğüm elle bağlandı (MCP videosu yorumları → ses problemi, anlatım temposu)
- ayar: Hermes'e verilen görev "her sabah 9'da Twitter içeriği hazırlayan otomasyon" → sürekli çalışan servis + her sabah tetiklenen görev + skill dosyası; skill adımları: sabah takvimini oku, gün tipine bak, hazır paket varsa logla yoksa ham malzeme üret, hiçbir şeyi otomatik yayınlama
- ayar: Hermes arka plan kopyası her turdan sonra "bu konuşmada öğrenilecek bir şey var mı?" diye sorar, varsa diske yazar yoksa siler; yalnız memory ve skill araçlarına izinli, ana sohbete dokunmaz; yazar + gözden geçirici iki ajan, her yazım kim/ne zaman/hangi dosya ile deftere işlenir
- ayar: auto memory kayıt örneği "504 hatası aldık, çok uzun düşündüm" iken Hermes "Selma'ya kısa cevap ver" biçiminde işleyiş kaydeder; auto memory koddan/git'ten çıkarılabileni (mimari, dosya yolu, hata düzeltmesi) yazmaz, CLAUDE.md'ye istenmedikçe dokunmaz
- komut: (kurulum istemi, sözlü özet) bu klasörü LLM Wiki olarak kur; üç cümlelik CLAUDE.md yaz (klasörde ne var, ne zaman buraya bakılır); index'i ve log.md'yi hazırla; verdiğim ham kaynaklara asla dokunma
- komut: (INGEST istemi, sözlü özet) kaynak altına özet sayfası yaz; konu sayfalarını aç ya da güncelle; tekrar eden talepleri kendi sayfası yap; index'i güncelle, yeni sayfaları kataloğa ekle; log.md'ye tarihli değişiklik yaz; sayfalar arasında çapraz bağlantı kur
- komut: (QUERY istemi) izleyicilerimin en çok sorduğu soru neydi ve hangisini cevaplamamışım? cevabı iki kaynak sayfasıyla destekle; cevabı sentez sayfası olarak wiki'ye yaz, index.md'ye ekle
- komut: (LINT istemi) kırık bağlantı, yetim sayfa, index.md'ye eklenmemiş sayfa, sayfalar arası çelişen iddia / bağlam kayması, sayfada geçip kendi sayfası olmayan kavram; bulduklarını önce liste halinde göster, onaylamadan düzenleme yapma (videoda sonra "gerek yok, düzeltebilirsin" denildi)
- komut: arşiv denetimi için grep, find, wc (açıklama); istemlerin temiz hâli repo'daki PROMPTS.md'de (açıklama)
- dosya: CLAUDE.md (şema/kural dosyası, grafta yetim düğüm); index.md (harita); log.md (yıl-ay-gün formatı); ham kaynak klasörü (raw); sentez sayfası "izleyici soru haritası" .md; MEMORY.md (auto memory indeksi); AGENTS.md (başka ajanlardaki karşılığı)
- dosya: Hermes: SOUL.md (kişilik, tek paragraf); skill dosyaları (davranış); memories klasörü (notlar)
- dosya: NotebookLM defteri "Hafıza 2"; piksel macera oyunu proje dosyaları yüklenemedi, tasarım ve database dizaynı dosyaları yüklendi, veri tablosu üretildi
- sayı: MEMORY.md her oturum başında ilk 200 satır ya da 25 KB yüklenir — yalnız iddia (dokümandan aktarım, ölçülmedi)
- sayı: transkriptler varsayılan 30 gün sonra silinir — ayar ekranda gösterildi, silinme gösterilmedi
- sayı: Hermes not defteri toplam 2200 karakter, her tur başında enjekte — yalnız iddia (sunucu önce "Claude Code araştırdı, ne kadar doğru bilmiyorum", sonra "kodda yazıyor" diyor)
- sayı: LLM Wiki token problemini "büyük ölçüde çözdü" — yalnız iddia, ölçüm yok
- sayı: LINT normalden fazla token harcar, günlük değil haftalık yapılmalı — yalnız iddia
- sayı: LINT raporu 4 çelişen iddia buldu — gösterildi
- sayı: NotebookLM MCP ile Claude Code'un okuyacağı 40 dosya azaltılabilir ama MCP ek token yakar — yalnız iddia (örnek sayı)
- sayı: Karpathy'nin llm-wiki postu 2 Nisan'da (~5 ay önce) — gösterildi (post tarihi ekranda)
- sayı: ilk video 4 ay önce, 32 bin kişiye ulaştı; Obsidian bağlantısı sorusu bir düzineye yakın yorumda, "hafızayı nasıl çağıracağım" 7 kişi; token problemi 6 aydır — yalnız iddia (açıklama/sözlü)
- sayı: Claude Code + LLM Wiki + Obsidian (+ Hermes) kombinasyonu "kusursuz hafıza sistemi" çıkarır — yalnız iddia
