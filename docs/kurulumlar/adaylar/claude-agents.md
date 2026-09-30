# claude agents
ad: claude agents
tur: CLI
video: ZAaxx3qyT8g
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Claude Code'un genel telemetri ayarları geçerli olabilir, ama bu özelliğe özel bir telemetri bulgusu yok.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Zaten Claude Code'un içinde yerleşik. Kurulum gereği Claude Code v2.1.139+ sürümüdür, ayrıca kurulacak bir şey yok. Kendi skill/plugin/hook'umuzla yeniden üretmek anlamlı değil, çünkü supervisor süreci ve oturum yönetimi çekirdeğe ait.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-3)
## Ne
Claude Code'un yerleşik komutudur. `claude agents` agent view ekranını açar. Bu ekran, birçok arka plan Claude Code oturumunu tek listede gösterir ve yönetir. Her satırda oturum, girdi bekleyip beklemediği, son yanıtın içeriği ve son etkileşim zamanı görünür.
## Mekanizma
Arka plan oturumları, kullanıcı başına çalışan bir supervisor süreci tarafından barındırılır. Bu yüzden terminal bağlı olmasa da çalışmaya devam ederler. Oturumlar varsayılan olarak `.claude/worktrees/` altındaki izole git worktree'lerde düzenleme yapar. Böylece birkaç oturum aynı dosyalarla çakışmadan paralel çalışır. İlgili komutlar: `claude --bg "<görev>"`, `/bg`, `claude attach`, `claude logs`, `claude stop`, `claude rm`. Bu bilgiler arama sonuçlarındaki özetlerden geliyor. Resmî dokümanın tam metnini ben okumadım.
## Kanıt
- Taze bir terminalde `claude agents` yazınca agent view açılır. → doğrulandı · Video alıntısı ve Claude Code dokümanı (code.claude.com/docs/en/agent-view) arama özeti aynı şeyi söylüyor. Komutu kendim çalıştırmadım.
- Arka plan oturumları izole git worktree'lerde çalışır. → doğrulandı · Arama sonuçlarındaki özetlerde `.claude/worktrees/` varsayılanı belirtiliyor. Birincil doküman tam metni okunmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code'u v2.1.139 veya daha yeni bir sürüme güncelleyin.
- Terminalde `claude agents` çalıştırın.
- Yeni arka plan görevi için `claude --bg "<görev>"` kullanın. Açık oturumu arka plana almak için `/bg` yazın.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Birçok Claude Code oturumu tek ekrandan başlatılır, izlenir ve yönetilir. Hangi oturumun girdi beklediği bir bakışta görülür. Worktree yalıtımı sayesinde paralel işler çakışmaz.
## Maliyet/risk
Düşük. Özellik Anthropic'in kendi ürününün parçası, ama kapalı kaynak ve sürüme bağlı (v2.1.139+). Paralel oturumlar kullanım kotasını daha hızlı tüketebilir, bu bir çıkarım. Başıboş arka plan oturumları izin ve onay davranışı açısından izlenmeli.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-3/panel.md → Ömer sütunu
## Özellikler
### `claude agents` ile tüm arka plan oturumlarını tek listede görme (durum, girdi bekleme, son yanıt, son etkileşim).
kaynak: https://code.claude.com/docs/en/agent-view
### `claude --bg`, `/bg`, `attach`, `logs`, `stop`, `rm` ile oturum yaşam döngüsü yönetimi.
kaynak: https://claude.com/blog/agent-view-in-claude-code
### Oturumlar supervisor süreciyle terminalsiz çalışır ve varsayılan olarak izole worktree kullanır.
kaynak: https://www.mindstudio.ai/blog/claude-code-bg-command-background-agent-sessions
## Destek
- ZAaxx3qyT8g · 4:20 · Taze bir terminalden agent view'u açan komut. · kanıt: in a fresh terminal, you could do Claude agents and that would open up that view
