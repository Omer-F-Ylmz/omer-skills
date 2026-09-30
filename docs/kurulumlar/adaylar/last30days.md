# last30days
ad: last30days
tur: skill
video: V2RIVnGCy74
repo: mvanhorn/last30days-skill
lisans: MIT
son_commit: bilinmiyor (README v3.11.1, Temmuz 2026 diyor; kesin commit tarihi alınamadı)
arsiv: bilinmiyor
kaynak: https://github.com/mvanhorn/last30days-skill
telemetri: Arama özeti 'izleme ve analitik yok, araştırma makinende kalır' diyor. Kaynak kodda doğrulamadım. Sorgular yine de bağlanan üçüncü taraf API'lere (X, Perplexity, OpenRouter vb.) ve LLM sağlayıcısına gider.
yildiz: ~63k (arama sonuçları 61.5k–63.2k gösteriyor; kesin güncel değer doğrulanamadı)
alt_tur: araç
skillspector: koşmadı: SkillSpector raporu yok
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Verilen bir konu, kişi ya da şirket için son 30 gündeki topluluk ve sosyal sinyalleri (Reddit, X, YouTube transkriptleri, TikTok, Instagram Reels, Hacker News, Polymarket, GitHub, Bluesky, Threads, LinkedIn, arXiv, Techmeme, Perplexity, web vb.) paralel tarayıp etkileşime göre puanlayan ve tek bir özet brifing üreten araştırma skill'i. Keşif modu (yükselen konular), karşılaştırma (A vs B) ve --hiring-signals gibi kullanım biçimleri var.
## Mekanizma
Motor kaynakları paralel sorgular. Sonuçlar upvote, beğeni, izlenme ve Polymarket hacmi gibi gerçek etkileşim sinyaline göre puanlanıp kaynaklar arası sıralanır. Sonra ajanın LLM'i yargıç olarak adayları eler, sentezler ve brifing yazar. Reddit, HN, Polymarket ve GitHub anahtarsız çalışır. X, YouTube, TikTok gibi kaynaklar için kurulum sihirbazı kullanıcının kendi anahtarlarını ya da tarayıcı oturumlarını bağlar. arXiv, Techmeme ve Digg, PATH'te ilgili *-pp-cli aracı varsa otomatik açılır. Ayrıntılar docs/how-search-works.md içinde (okumadım).
## Kanıt
- Reddit, X, YouTube, TikTok, Reels, HN, Polymarket gibi birçok kaynakta derin araştırma yapıyor (video iddiası) → doğrulandı · README'deki kaynak tablosu bu kaynakların hepsini listeliyor. Çalıştırıp sınamadım.
- Sıfır yapılandırmayla Reddit, HN, Polymarket ve GitHub çalışıyor → sınanamadı · README'de yazıyor. Kurup çalıştırmadım.
- İzleme ve analitik yok → sınanamadı · Yalnızca arama özetinde geçiyor. Kaynak kod okunmadı.
- MIT lisanslı → doğrulandı · Arama sonucu MIT diyor ve ağaçta LICENSE dosyası var. Dosya metnini görmedim.
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok
## Kurulum
- Claude Code: /plugin marketplace add mvanhorn/last30days-skill
- Claude Code: /plugin install last30days
- Diğer Agent Skills istemcileri (Codex, Cursor, Copilot, Gemini CLI vb.): npx skills add mvanhorn/last30days-skill -g
- İlk çalıştırmada kurulum sihirbazı X, YouTube, TikTok, arXiv, Techmeme gibi ek kaynakları açar
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Web aramasının ulaşamadığı topluluk yorumlarını, transkriptleri ve tahmin piyasası oranlarını tek komutla toplar. Toplantı ya da satış görüşmesi öncesi, rakip karşılaştırma ve yükselen konu keşfi için günlük brifing üretir.
## Maliyet/risk
Çok büyük bir yüzey: çok sayıda kaynak, API anahtarı ve tarayıcı oturumu (X, TikTok, LinkedIn vb.) gerektirebilir, bu da kimlik bilgisi yönetimi ve hesap/ToS riski getirir. Sosyal kaynaklardan gelen içerik güvenilmez veridir, prompt injection taşıyabilir. Token maliyeti yüksek olabilir. Yıldız sayısı ve trend rozetleri pazarlama niteliğinde. Kurulum sihirbazı ek CLI'lar kurabilir, ilk çalıştırmada neyi kurduğu incelenmeli.
## Tasarruf
Token aracı değil. Çok kaynaklı tarama ve sentez token tüketir. Tasarruf iddiası yok.
## Üretilebilir
hedef_tur: skill
tarif: Hafif bir 'topluluk nabzı' skill'i: (1) anahtarsız kaynaklar için Reddit arama JSON/RSS, HN Algolia API, Polymarket Gamma API ve GitHub API'yi çağıran küçük bir Python/Node betiği yaz; (2) sonuçları tarih penceresi (30 gün) ve etkileşim sayısına (puan, yorum, hacim) göre normalize edip sırala; (3) SKILL.md'de ajana üst sonuçları eleyip kaynak belirterek kısa brifing yazmasını söyle. Anahtar gerektiren kaynaklar (X, TikTok) ilk sürüme dahil edilmez.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### 20'den fazla kaynakta paralel arama ve etkileşime göre puanlama (Reddit, X, YouTube, TikTok, Reels, HN, Polymarket, GitHub, Bluesky, Threads, LinkedIn, arXiv, Techmeme, Perplexity, web)
kaynak: https://github.com/mvanhorn/last30days-skill
### Keşif modu: yükselen konuları hız sırasıyla listeler, her birine hazır takip komutu verir
kaynak: https://github.com/mvanhorn/last30days-skill
### --hiring-signals: iş ilanlarından şirket odak kaymasını kaynaklı kanıt olarak çıkarır
kaynak: https://github.com/mvanhorn/last30days-skill
### Çoklu istemci desteği: Claude Code marketplace, Codex, Cursor, Gemini CLI, Agent Skills (npx skills add)
kaynak: https://github.com/mvanhorn/last30days-skill
## Destek
- V2RIVnGCy74 · 11:07 · Reddit, Twitter, YouTube, TikTok, Reels, Hacker News, Polymarket gibi kaynaklarda derin araştırma yapan skill; günlük brifing için uygun, /deep research'e alternatif. · kanıt: Basit web aramasının ötesinde birçok spesifik kaynakta derinlemesine araştırma yapıyor. (karede: İlgili kare yok; altyazıdan.)
