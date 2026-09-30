# Claude Code (terminalde, VS Code içinde)
ad: Claude Code (terminalde, VS Code içinde)
tur: CLI
video: j7Fyi5gQ85k
repo: yok
lisans: yok (kapalı kaynak; Anthropic ticari şartları geçerli, SPDX kimliği yok)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Bilinmiyor (bu turda doğrulanmadı). Genel bilgiye göre kullanım metrikleri ve hata raporlama vardır ve ortam değişkenleriyle kapatılabilir. İstemler ve kod modele gönderildiği için Anthropic API'sine gider. Kesin ayrıntı için resmi veri kullanımı dokümanına bakılmalı.
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Bizde zaten var: bu çalışma ortamı Claude Code (Claude Agent SDK tabanlı). Yeni bir şey üretmeye gerek yok. Yapılacak tek iş, dışarıdan kurulum komutu yapıştırırken kaynağı doğrulamak.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-4)
## Ne
Anthropic'in terminalde (ve VS Code eklentisi/IDE entegrasyonuyla) çalışan ajan tabanlı kodlama aracı. Videoda, bir kurulumu (Jev) terminalden yaptırmak için kullanılıyor; Codex alternatif olarak anılıyor.
## Mekanizma
Terminalde çalışan ajan döngüsü: kullanıcı istemini Claude modeline gönderir. Model dosya okuma/yazma, kabuk komutu çalıştırma, arama gibi araçları çağırır. Araç çağrıları izin sistemiyle onaylanır. Bağlam dosyaları (CLAUDE.md), skill, hook, MCP sunucuları ve eklentilerle genişletilir. Model çıkarımı Anthropic API'sinde uzaktan yapılır. Videoda kullanım: 'claude' komutu açılır, web sitesindeki kurulum komutu kopyalanıp yapıştırılır ve ajan adımları yürütür. Bu bilgi genel bilgiye dayanır, bu turda doğrulanmadı.
## Kanıt
- Claude Code terminalde çalışıp Jev kurulumunu yapabiliyor (videoda 'terminal yazıyorum, web sitesine basıp kopyalıyorum, yapıştırıyorum'). → sınanamadı · Yalnızca video alıntısı var. Bu turda video getirilmedi ve kurulum denenmedi.
- Codex, Claude Code'a alternatiftir. → sınanamadı · Videodaki sözlü ifade. Karşılaştırma yapılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Kurulum gereği: Anthropic hesabı (Pro/Max aboneliği ya da API/Console kredisi) veya desteklenen bulut sağlayıcısı gerekir.
- Kurulum (resmi dokümana göre, doğrulanmadı): npm install -g @anthropic-ai/claude-code ya da resmi yükleyici betiği.
- Proje dizininde 'claude' çalıştırılır, ilk açılışta giriş yapılır.
- VS Code: eklenti pazarından Claude Code eklentisi ya da entegre terminalde 'claude'.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Kurulum, yapılandırma ve kodlama işlerini doğal dille terminalden yaptırır. Kopyala-yapıştır adımlarını ajana devrederek el emeğini azaltır. Zaten kullandığımız ortam olduğundan ek kurulum gerektirmez.
## Maliyet/risk
Kabuk komutu çalıştırıp dosya değiştirebilir. Videodaki gibi bilinmeyen web sitesinden kurulum komutu yapıştırmak tedarik zinciri riskidir. İzinleri dikkatli verilmeli. Kod bağlamı dışarıya (API) gider. Abonelik veya token maliyeti oluşur. Kapalı kaynak olduğundan iç işleyiş denetlenemez.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-4/panel.md → Ömer sütunu
## Özellikler
### Terminalde ajan tabanlı kodlama: dosya okuma/yazma, komut çalıştırma, izin onayı (genel bilgi, doğrulanmadı)
kaynak: https://docs.anthropic.com/en/docs/claude-code/overview
### VS Code entegrasyonu ve terminal kullanımı (video bulgusu)
kaynak: https://www.youtube.com/watch?v=j7Fyi5gQ85k
## Destek
- j7Fyi5gQ85k · 32:45 · Jev kurulumunu terminalde yapmak için kullanılan kodlama aracı; Codex de alternatif. · kanıt: Cloud code terminal yazıyorum. Çıkan web sitesine basıyorum. Kopyalıyorum, yapıştırıyorum.
