# Figma plugin
ad: Figma plugin
tur: plugin
video: uuUo7gWuH9w
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor. Sunucu Figma tarafında barındırıldığı için tasarım verisi istekleri Figma'ya gider. Telemetri politikasını doğrulamadım.
yildiz: bilinmiyor
alt_tur: ürün
ucretsiz_katman: Arama sonucuna göre uzak sunucu her planda ve koltukta çalışır, ama limitler var. Ayrıntısını doğrulamadım.
bizde_karsilik: Yok. Figma MCP sunucusu Figma'nın kendi hizmeti olduğu için kopyalanamaz. Bizim tarafta yalnızca ince bir skill yazılabilir: Figma MCP çıktısını proje bileşen kurallarına göre koda çeviren bir talimat seti. Bu yüzden hedef tür 'yok' bırakıldı.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Figma'nın resmi Claude Code eklentisi (figma@claude-plugins-official). Figma MCP sunucusu ayarlarını ve sık iş akışları için Agent Skills'i bir arada kurar; Claude Code'un Figma tasarımını okuyup koda çevirmesini ve web uygulamasından Figma'ya sayfa göndermesini sağlar.
## Mekanizma
Eklenti, Figma'nın barındırdığı uzak MCP sunucusunu (https://mcp.figma.com/mcp) Claude Code'a bağlar. Kurulumdan sonra /plugin menüsünden OAuth yetkilendirmesi yapılır. Claude, MCP araçlarıyla tasarım bağlamını çeker ve HTML/CSS gibi koda çevirir. Tuvale yazma araçları da var. Skills tipik akışların talimatlarını verir. Kaynak kod ve araç listesinin ayrıntısını doğrulayamadım.
## Kanıt
- Figma tasarımını okuyup Claude Code ile koda çevirir. → doğrulandı · Figma yardım sayfası ve arama sonuçları, eklentinin Figma MCP sunucusunu ve iş akışı skill'lerini kurduğunu belirtiyor. Video içeriğini izleyemedim.
- Eklenti aranıp kuruluyor. → doğrulandı · Arama sonuçlarında kurulum komutu claude plugin install figma@claude-plugins-official olarak geçiyor.
- Uçuş uygulaması Figma'sı HTML/CSS'e çevriliyor. → sınanamadı · Video transkripti getirilemedi, yalnızca YouTube altbilgisi döndü. Bu gösterimi sınayamadım.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- claude plugin install figma@claude-plugins-official (ya da Claude Code içinde /plugin install figma@claude-plugin-directory)
- Claude Code'u yeniden başlat
- /plugin yazıp figma sunucusuna gir, yetkilendirmeyi başlat
- Açılan tarayıcı sayfasında 'Allow access' ile Figma hesabına izin ver
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tasarımdan koda geçişi hızlandırır. Ekran görüntüsünü elle tarif etmek yerine Claude yapılandırılmış tasarım verisini doğrudan okur. Videoda uçuş uygulaması Figma'sı HTML/CSS'e çevriliyor.
## Maliyet/risk
Figma hesabına OAuth erişimi verilir. Tasarım içeriği üçüncü taraf uzak sunucu üzerinden geçer. Kapalı kaynak; hız limitleri plana göre değişir. Lisans ve kaynak deposu doğrulanamadı.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### Claude Code için tek komutla kurulum: MCP sunucusu ayarları ve Agent Skills birlikte gelir
kaynak: https://help.figma.com/hc/en-us/articles/39888612464151-Claude-Code-and-Figma-Set-up-the-MCP-server
### Figma'nın barındırdığı uzak sunucu (mcp.figma.com/mcp); masaüstü uygulaması gerekmez, tuvale yazma araçları içerir
kaynak: https://developers.figma.com/docs/figma-mcp-server/remote-server-installation
### Yerel web uygulamasındaki sayfayı Figma'ya gönderme
kaynak: https://www.threads.com/@claudeai/post/DU56ZDODhxt/to-get-started-install-the-figma-mcp-server-plugin-install-figma-claude-plugin
## Destek
- uuUo7gWuH9w · 19:59 · Figma tasarımını okuyup Claude Code ile koda çevirir. · kanıt: Plugin aranıp kuruluyor; uçuş uygulaması Figma'sı HTML/CSS'e çevriliyor.
