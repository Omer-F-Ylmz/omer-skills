# WebCMD
ad: WebCMD
tur: skill
video: bS6IlkUozAI
repo: agentrhq/webcmd
lisans: Apache-2.0
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/agentrhq/webcmd
telemetri: Doğrulanamadı ayrıntı: repoda PRIVACY.md var ama içeriği okunamadı. README'ye göre ilk erişimde WebCMD Cloud seed'i kullanılabilir (ağ erişimi var), sonraki öğrenme yerel kalıyor. Kullanım telemetrisi olup olmadığı bilinmiyor; kurmadan önce PRIVACY.md okunmalı.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
AI ajanları için kendi kendine öğrenen tarayıcı altyapısı. Gerçek (oturum açılmış, adlandırılmış profilli) bir tarayıcıyı ajana açar; ajanların gezdiği sitelerin gezinti bağlamını yerel hafızaya kaydeder ki sonraki ajanlar siteyi baştan keşfetmesin.
## Mekanizma
İki katman: (0) canlı tarayıcı kontrolü, `webcmd browser` ile sayfayı inceleme, tıklama, yazma, veri çıkarma, ağ çağrılarını yakalama; profil/oturum (`--profile`, `session create`) ve sandbox'lı Playwright tarzı program çalıştırma (`browser run --file/--stdin`). (1) Sitemap hafızası: gözlenen sayfalar, durumlar, eylemler, iş akışları, API'ler, tuzaklar ve yedek yolları içeren ajan odaklı site haritası. Öğrenme sessiz ve seçici: canlı tarayıcı her zaman doğru kabul edilir, sırf öğrenmek için keşif yapılmaz, hafıza hatası görevi engellemez. İlk erişimde WebCMD Cloud'dan "seed" alınabilir, sonraki öğrenme yerelde kalır. Ajan `webcmd-browser` skill'ini yalnız canlı tarayıcı işi için yükler.
## Kanıt
- Masaüstünde kullandığın tarayıcıyı AI ajanları için dönüştürür → doğrulandı · README: oturum açılmış adlandırılmış profillerle gerçek tarayıcıda çalışır (`--profile work`).
- Siteleri alan adı bazında hatırlar / öğrenir → doğrulandı · README: sitemap hafızası, gözlenen sayfa/eylem/iş akışı/API kaydı, ilk seed sonra yerel öğrenme. 'Alan adı bazında' ifadesi açıkça geçmiyor ama site bazlı hafıza.
- Stealth sürücülü → sınanamadı · README'de 'stealth' yalnızca 'sessiz öğrenme' anlamında geçiyor; bot tespitinden kaçınan sürücü kanıtı görülmedi.
- Açık kaynak → doğrulandı · Apache-2.0 lisansı (README rozeti ve LICENSE dosyası).
- Token harcamasını %90'a kadar düşürür → sınanamadı · README iddiası; benchmarks/ klasörü var ama sonuçlar çalıştırılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Node.js 20.6+ gerekir
- npm install -g @agentrhq/webcmd
- webcmd skills add (Claude/Codex/özel yol seçilir; yalnız webcmd-browser skill'i kurulur)
- Alternatif: ajana 'Fetch and follow https://raw.githubusercontent.com/agentrhq/webcmd/main/start.md to set up Webcmd end to end.' demek
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Sık kullanılan sitelerde (giriş yapılmış hesaplarla) daha hızlı, ucuz ve güvenilir tarayıcı otomasyonu; kullanıcının mevcut profil/oturumlarıyla çalışma; Claude ve Codex için hazır plugin/skill paketi.
## Maliyet/risk
Oturum açılmış gerçek profillere ajan erişimi (hesap ele geçirme/istenmeyen eylem riski, read-only istemi gerekir); Cloud seed ve gizlilik davranışı doğrulanmadı; hafıza zehirlenmesi/eski bilgi riski (canlı tarayıcı doğru kabul edilse de); global npm kurulumunda postinstall betiği var; skill kurulumu harici start.md'yi çekip izletebilir (prompt injection yüzeyi). Aynı adla çok sayıda fork/kopya repo var, resmi olan agentrhq/webcmd.
## Tasarruf
Ajanların her çalıştırmada siteyi yeniden keşfetmesini önleyen yerel sitemap hafızası ile tarayıcı-ajan token harcamasını "%90'a kadar" azaltma iddiası (README; benchmarks/ dizini var ama sonuçlar doğrulanmadı). Mekanizma: bilinen sayfa/eylem/API yollarını hazır vermek, keşif adımlarını ve DOM/ekran okuma turlarını kısaltmak.
## Üretilebilir
hedef_tur: skill
tarif: Kendi 'site-hafizasi' skill'imiz: ajan bir siteyi gezdikten sonra alan adı başına bir markdown dosyası (~/.claude/site-memory/<domain>.md) yazsın: giriş/arama URL'leri, çalışan seçiciler, bulunan iç API uçları, tuzaklar, yedek yollar. Görev başında skill o alan adı dosyasını okur, yoksa normal keşfeder; bitince yalnız doğrulanmış yeni bilgiyi ekler (canlı sayfa esas kabul edilir). Tarayıcı kontrolü için mevcut Playwright/Chrome MCP kullanılır; ek olarak SessionEnd/Stop hook'u ile öğrenme notu hatırlatılabilir. Bulut seed ve stealth kısmı yapılmaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### Canlı tarayıcı kontrolü: inceleme, tıklama, yazma, veri çıkarma, ağ çağrısı yakalama (webcmd browser)
kaynak: https://github.com/agentrhq/webcmd
### Sitemap hafızası: sayfalar, durumlar, eylemler, iş akışları, API'ler, tuzaklar, yedek yollar
kaynak: https://github.com/agentrhq/webcmd
### Adlandırılmış profil ve oturumlar; sandbox'lı Playwright tarzı program (browser run --file/--stdin)
kaynak: https://github.com/agentrhq/webcmd
### Tek skill (webcmd-browser) kurulumu; Claude ve Codex plugin manifestleri
kaynak: https://github.com/agentrhq/webcmd
### Memory hatası görevi engellemez; canlı tarayıcı esas doğru kaynak
kaynak: https://github.com/agentrhq/webcmd
## Destek
- bS6IlkUozAI · 0:12 · Mevcut masaüstü tarayıcıyı AI ajanları için siteleri alan adı bazında hatırlayan, stealth sürücülü, öğrenen bir tarayıcıya dönüştüren açık kaynaklı araç/skill. · kanıt: The tool is called WebCMD. It transforms the desktop browser you already use · iddia: Ajanlar her web erişiminde sıfırdan başlayıp binlerce token harcıyor; WebCMD bunu bellekle önlüyor.; Site değişince WebCMD değişikliği doğrular, eski bilgiyi günceller, sonraki çalıştırma düzeltilmiş bilgiyi kullanır.
## Yapım tarifi (Ömer UYARLA, 2026-09-29)
- hedef: site-hafızası skill (yalnız md) — ziyaret edilen sitenin yapısı/komutları docs/site-hafizasi/<alan>.md'de tutulur
- akış: siteye gitmeden önce hafıza okunur; yeni öğrenilen gezinme adımı hafızaya eklenir; 30 günden eski kayıt tazelenir
- koşulmaz; yapım ayrı dalga
