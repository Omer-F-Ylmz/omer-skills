# Claude Limitine Bir Daha Asla Takılmayacaksın
kanal: İsa Nurdoğdu · süre: 10 dk · altyazı: otomatik tr
ana iddia: Claude Code limiti mesaj sayısına değil token'a bağlı; tek mesajda 232.000 token'ın %98,5'i çöpe gidebiliyor (iddia); 11 kural (edit yerine regenerate, 15-20 mesajda yeni sohbet, soruları tek mesajda toplama, kullanım dashboard'u, dosya yükleme, hafıza ayarı, özellik kapatma, Haiku'ya geçiş, işi gün içine yayma, yoğun olmayan saatlerde çalışma, overage açma) token/limit tasarrufu sağlıyor.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| phuryn/claude-usage | YENİ | KUR | yerel Python tabanlı Claude Code token/maliyet/oturum dashboard'u (CLI + VS Code eklentisi); "ücretsiz dashboard" (Kural 4) |
| JuliusBrussee/caveman | YENİ | ELE | "mağara adam" tarzı yanıtla %65 token azaltma iddiası; kurulu RTK ile aynı niş (token azaltımı) — çift |
| settings.json hafıza/tercih ayarı (Kural 6) + kullanılmayan özellik kapatma (Kural 7) | ZATEN VAR | BEKLE | genel Claude Code ayarları, kurulum gerektirmiyor; CLAUDE.md/memory disiplinine zaten yakın |
| basit işlerde Haiku'ya geçiş (Kural 8) | ZATEN VAR | BEKLE | model kademesi fikri CLAUDE.md'deki "subagent model kademesi" ilkesiyle örtüşüyor |
## ölçütler (KUR / ELE)
- phuryn/claude-usage: bakım=pushed 2026-07-10 (≤3 ay, 2226 yıldız — gerçekçi ölçek), archived=false, MIT · çift=örtüşme yok, kurulu sette kullanım-izleme dashboard'u yok · izin=yerel; API anahtarı istemiyor, yalnız Claude Code'un kendi log/veritabanını okuyor; Windows/Docker/uv tool/pipx/brew/VS Code Marketplace seçenekleri var · context=CLI/VSCode eklentisi, yalnız çağrılınca/sidebar açılınca çalışır, sohbete tool şeması eklemiyor · kurulum: `uv tool install git+https://github.com/phuryn/claude-usage` (KURMA, yalnız rapor)
- JuliusBrussee/caveman: bakım=pushed 2026-09-16 ama 105984 yıldız niş bir "rule file" için şüpheli derecede yüksek · çift=RTK ile aynı kategori · izin=NOASSERTION lisans; Windows PowerShell kurulumu `irm ... | iex` (uzaktan script çalıştırma) · context=skill+proxy, oturuma ekleniyor · kurulum: `npx skills add JuliusBrussee/caveman -g`
## hedefler (BİLGİ)
- yok
