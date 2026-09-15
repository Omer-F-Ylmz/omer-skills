# Claude Code Token Hackleri: 23 Dakikada 18 İpucu
kanal: Burhan KOCABIYIK · süre: 23 dk · altyazı: otomatik tr
ana iddia: 18 kullanım alışkanlığıyla (clear, gereksiz MCP kapatma, önce planlama, compact, Opus+Sonnet hibrit model) Claude Code token kullanımı %80-90 azaltılabilir.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| kullanılmayan MCP'yi kapat (/mcp, etkisini /context ile ölç) | YENİ | BİLGİ | kurulu 4 MCP var (21st, claude-design yalnız UI işinde lazım); CLAUDE.md'de MCP kapatma kuralı yok |
| hibrit model: Opus iskelet/plan, Sonnet tekrarlı doldurma (/model) | YENİ | BİLGİ | CLAUDE.md'de model seçimi kuralı yok; "%80 daha az token" yalnız iddia |
| yerleşik: /clear, /context, /cost, /stats, statusline, /compact, /memory (auto memory, Auto Dream?), /btw, Remote Control, plan modu, VS Code eklentisi context çubuğu, claude.ai/Console usage + harcama limiti | ZATEN VAR | ELENDİ | Claude Code / platform yerleşik; planı MD'ye kaydetme superpowers:writing-plans ile var |
| göreve geçişte /clear, ~%60'ta manuel /compact, molasız bitir | ZATEN VAR | ELENDİ | CLAUDE.md CONTEXT DİSİPLİNİ: /clear zorunlu, /compact tavsiye, cache TTL 1 saat; %60 eşiği yalnız iddia |
| CLAUDE.md sade tut (<200 satır, yalnız kural); nokta atışı dosya referansı | ZATEN VAR | ELENDİ | claude-md-management kurulu ("Keep it concise"); CLAUDE.md: önce graphify query, dosya yalnız kanıt satırı için |
| az ajan (tek/iki), izinleri kıs, bypass modu yok | ZATEN VAR | ELENDİ | CLAUDE.md subagent delegasyonu çıktı şişkinliğini karşılıyor; video subagent'i paralel terminalle karıştırıyor, izin↔token bağı kanıtsız |
| diğer: tek prompt'ta birleştir, peak hour'dan kaçın, n8n-io/n8n, remotion-dev/remotion, Instantly, DOA (Skool)/Gumroad ürünleri | YENİ | ELENDİ | kullanıcı alışkanlığı / peak hour konuşmacı test etmedi / konu dışı, yalnız örnek ya da affiliate-promo |
## ölçütler (YENİ)
- kullanılmayan MCP'yi kapat: bakım=— (teknik, repo yok) · çift=örtüşme yok · izin=yok · context=CLAUDE.md'ye 1 satır (her oturum) · kurulum: —
- hibrit model: bakım=— (teknik, repo yok) · çift=örtüşme yok · izin=yok · context=CLAUDE.md'ye 1 satır (her oturum) · kurulum: —
- diğer: bakım=n8n-io/n8n pushed 2026-09-15, 204367★, arşiv değil; remotion-dev/remotion pushed 2026-09-15, 59347★, arşiv değil; Instantly/DOA/Gumroad bilinmiyor; teknikler — · çift=örtüşme yok · izin=n8n self-host ya da hesap; Remotion npm paketi; Instantly, DOA, Gumroad ücretli hesap · context=kurulmadıkça yok · kurulum: —
## hedefler (BİLGİ)
- UI dışı işte kullanılmayan MCP'yi /mcp ile kapat, etkisini /context ile ölç → CLAUDE.md (CONTEXT DİSİPLİNİ)
- plan/iskelet güçlü modelde, tekrarlı toplu içerik (ör. çok sayfa doldurma) Sonnet'te → CLAUDE.md (CONTEXT DİSİPLİNİ: model seçimi)
---
## ek: somut
- ayar: /memory'de Auto memory her zaman açık, Auto Dream? açılabilir, kayıt yeri seçilebilir
- ayar: Console'da otomatik bakiye (auto-reload) ve harcama limiti (ör. 20 $'da dur), yalnız API kullanımında; abonelikte gereksiz
- ayar: bypass izin modunu kullanma, komutları tek tek onayla; statusline'a anlık token kullanımı ekle
- komut: claude (terminalde başlat); /clear; /mcp; /context; /cost (abonelikte "subscription kullanıyorsun" der); /stats (konuşmacı: statusline yerine "aynı şey")
- komut: /model (Haiku 4.5, Sonnet, Opus); /compact; /memory; /btw ("şu anda neler yapıyorsun", "ne kadar kaldı"); Remote Control ile telefondan izleme; sesli giriş
- dosya: CLAUDE.md (kural dosyası, veri deposu değil); plan MD dosyası olarak kaydedilip sonraki oturumda kural olarak kullanılır; oturum logları/memory dosyaları
- sayı: 18 hack = 9 kolay + 5 orta + 4 ileri — videonun yapısı
- sayı: token kullanımı %80 azalır (ilk 9 hack), kapanışta %80-90, açıklamada "%80'e kadar" — yalnız iddia
- sayı: web sitesi ≈200.000 token ≈3 $ (Opus), dışarıda yaptırması 300/500/1000 $ — yalnız iddia
- sayı: konuşma büyümesi: ilk mesaj 500, 10 mesaj 5.000, sonra 30.000; 500→15.000→250.000; ileride prompt başına 100.000-200.000 token; 1 kelime ≈ 1 token — yalnız iddia (şema, ölçüm yok)
- sayı: hedef prompt başına ~1.500 token'da sabit kalmak — yalnız iddia
- sayı: /clear önerisinde "300.000 token kazanırsın" uyarısı — yalnız iddia (örnek terminal bulunamadı)
- sayı: her MCP her mesajda binlerce token; /context örneği MCP 34.000, memory dosyaları 10.000, sistem prompt 1.500 token — gösterildi? (altyazıdan kesin değil)
- sayı: /stats: son 30 günde 4,6 milyon token, en uzun seri? 27 gün, 10 gün kesintisiz kullanım — gösterildi (kendi hesabı)
- sayı: usage sayfasında %6-7 kullanım — gösterildi
- sayı: Max planı "70 ya da 90 $" — yalnız iddia, konuşmacı emin değil
- sayı: API kullanımında her 20-40 dakikada kontrol; limitler haftalık yenilenir — yalnız iddia
- sayı: CLAUDE.md/sistem promptu 200 satırın altında — yalnız iddia
- sayı: context ~%60'ta manuel compact; ~%95'te önceki context görülmez — yalnız iddia
- sayı: Opus iskelet + Sonnet ile 100 blog sayfası → %80 daha az token, benzer sonuç — yalnız iddia
- sayı: ajan maliyeti lineer değil (1000/2000/3000 değil) ama ajan arttıkça artar; tek ya da en fazla 2 ajan; 7-8 terminal örneği — yalnız iddia
- sayı: follow-up yerine tek prompt "iki kat daha net" — yalnız iddia
- sayı: peak hour'da limitler hızlı tükenir (hack 17) — yalnız iddia, konuşmacı test etmediğini söylüyor
- sayı: konuşmacıda 4-5, bazen 6-7 terminal açık; çökmede session gider, yeniden başlatmak token yakar — anekdot, yalnız iddia
