# JCode
ad: JCode
tur: CLI
video: enFgYQvI1dM
repo: 1jehuang/jcode
lisans: MIT
son_commit: bilinmiyor (README'de master dalı için son commit rozeti var, tarih okunamadı)
arsiv: bilinmiyor
kaynak: https://github.com/1jehuang/jcode
telemetri: Repoda TELEMETRY.md dosyası var, yani telemetri mevcut. İçeriği okunamadı, neyin toplandığı ve kapatma yolu bilinmiyor. Kurulumdan önce bu dosya okunmalı. Kurulum betiği curl / bash ile çalıştığından ayrıca gözden geçirilmeli.
yildiz: Kaynaklar çelişiyor: bir blog ~9.163, bir dizin ~20k gösteriyor. Güncel değer doğrulanmadı.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
Rust ile sıfırdan yazılmış, açık kaynaklı terminal kodlama ajanı harness'ı (TUI). Claude Code, Codex CLI ve OpenCode gibi araçların alternatifi. Linux, macOS ve Windows'ta çalışır. Yazarı Jeremy Huang (1jehuang).
## Mekanizma
Tek bir Rust ikilisi olarak çalışır. Oturum başına RAM ve açılış süresi düşüktür. README'ye göre yerel gömme kapalıyken 27.8 MB PSS, açıkken 167 MB kullanır. Aramaya bilgi katmanları ekler. Grep sonuçlarına dosya yapısı bilgisi ekler, böylece ajan dosyayı okumadan çıkarım yapabilir. Ajanın daha önce gördüklerine göre dönen çıktıyı uyarlanır biçimde keser. Her oturumun turlarını semantik vektörlere gömer ve geçmiş bağlamı otomatik hatırlar. "Swarm" modunda birden çok ajan aynı repoda çalışır, çakışmalar otomatik çözülür ve ajanlar birbirine mesaj gönderir. Ayrıca /update ve jcode update komutları, SDK, .jcode/skills ve MCP yapılandırması var. Bu ayrıntılar arama sonuçlarından ve README'nin görünen kısmından geldi. README 854 satırdı ve kısaltılmış geldi, kaynak koduna bakılmadı.
## Kanıt
- Rust ile yazılmış ücretsiz açık kaynak kodlama ajanı harness'ı → doğrulandı · github.com/1jehuang/jcode: MIT lisanslı, Cargo.toml ve Rust yapısı var. README'de 'The most RAM efficient harness' yazıyor.
- Çok düşük RAM kullanımı (oturum başına 27.8 MB, Claude Code 386 MB) → sınanamadı · README'deki karşılaştırma tablosu üreticinin kendi ölçümü. 27.8 MB, yerel gömme kapalıyken geçerli. Gömme açıkken 167.1 MB. Yerelde çalıştırılmadı.
- Claude Code'dan 245× hızlı, 14 ms açılış → sınanamadı · Yalnızca blog ve arama özetlerinde geçiyor, bağımsız benchmark yapılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- macOS/Linux: curl -fsSL https://jcode.sh/install / bash
- Windows 11 (PowerShell 5.1+): irm https://jcode.sh/install.ps1 / iex
- Güncelleme: TUI içinde /update ya da terminalde jcode update
- Kaynaktan derleme ve sağlayıcı kurulumu: README'deki 'Detailed installation' bölümü (okunmadı)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Çok sayıda paralel ajan oturumunu düşük RAM'le çalıştırmak isteyenler için uygun. Sağlayıcıdan bağımsız, ücretsiz bir Claude Code alternatifi arayanlara da uyar. Bağlam yönetimi özellikleri (uyarlanır kesme, yapılı grep, otomatik hafıza) fikir olarak bizim skill ve hook'larımıza da ilham verebilir.
## Maliyet/risk
Başlıca riskler: (1) Telemetri var, kapsamı doğrulanmadı. (2) Kurulum curl / bash ve irm / iex ile yapılıyor. (3) Ajan kod çalıştırıyor, dosya sistemine yazıyor ve OAuth ile sağlayıcı hesaplarına bağlanıyor (OAUTH.md var). (4) Proje genç ve hızlı sürüm çıkarıyor, kararlılık belirsiz. (5) "245× daha hızlı", "14 ms açılış" gibi performans iddiaları üreticinin kendi ölçümü, bağımsız doğrulanmadı. (6) Yıldız sayıları tutarsız.
## Tasarruf
Token aracı değil, ajan harness'ı. Yine de bağlam tasarrufu sağlar: uyarlanan çıktı kesme (ajanın zaten gördüğü içeriği kısaltma) ve yapı bilgili grep ile gereksiz dosya okuma azalır. Oturum gömmeleri sayesinde bağlam elle taşınmaz. Bunun için ölçülmüş bir token tasarrufu oranı bulunamadı.
## Üretilebilir
hedef_tur: hook
tarif: JCode'un tamamı üretilemez, ama bağlam tasarrufu fikirleri Claude Code hook'u olarak yapılabilir. PostToolUse hook'u yaz. Grep/Read çıktısını oturumdaki görülmüş satır/dosya karma listesiyle karşılaştır ve tekrar eden içeriği 'daha önce görüldü' özetiyle kısalt. Ayrıca grep sonuçlarına dosya başına sembol/yapı özeti ekleyen küçük bir CLI (ctags veya tree-sitter tabanlı) yaz. Oturum hafızası için yerel bir gömme dizini kullanan bir MCP sunucusu düşünülebilir. Swarm modu kapsam dışı.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### Düşük RAM ve hızlı açılış: oturum başına 27.8 MB (yerel gömme kapalı)
kaynak: https://github.com/1jehuang/jcode
### Grep sonuçlarına dosya yapısı bilgisi ekleme, ajanın dosyayı okumadan çıkarım yapması
kaynak: https://ai-tldr.dev/releases/1jehuang-jcode/
### Ajanın gördüklerine göre dönen çıktıyı uyarlanır biçimde kesme (bağlam tasarrufu)
kaynak: https://ai-tldr.dev/releases/1jehuang-jcode/
### Oturum turlarını semantik vektöre gömüp geçmiş bağlamı otomatik hatırlama
kaynak: https://ai-tldr.dev/releases/1jehuang-jcode/
### Swarm modu: aynı repoda birden çok ajan, otomatik çakışma çözümü, ajanlar arası mesajlaşma
kaynak: https://ai-tldr.dev/releases/1jehuang-jcode/
### Uygulama içi güncelleme (/update, jcode update), stable ve main kanalları
kaynak: https://github.com/1jehuang/jcode
### SDK, dokümantasyon ve benchmark sayfaları
kaynak: https://jcode.sh/
## Destek
- enFgYQvI1dM · 0:00 · Rust ile yazılmış ücretsiz açık kaynak kodlama ajanı harness'ı · kanıt: Kareden: “JCode rebuilt it from scratch in rust”; adı ASR'de "J code" · iddia: JCode ücretsiz ve açık kaynak
## Yapım tarifi (Ömer UYARLA, 2026-09-29)
- hedef: PostToolUse hook — aynı oturumda aynı Read (yol + aralık) ya da aynı Grep (desen + yol) tekrarlanırsa çıktı "daha önce görüldü (<çağrı no>)" diye kısaltılır
- anahtar: araç + yol + aralık/desen hash'i; oturum başına geçici dosya; dosya değiştiyse (mtime) kısaltma yok
- Headroom çakışma notu: headroom da çıktıyı sıkıştırır; kısaltma satırı ilk görülen çağrının headroom hash'ini taşımalı, yoksa retrieve yolu kopar
- token: ölçüt tekrar eden Read/Grep oranı; koşulmaz
