# MCP sunucu listesi ile kullanılmayanları kapatma
ad: MCP sunucu listesi ile kullanılmayanları kapatma
tur: MCP
video: kHtOSJRUkLs
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Yok; yerel yapılandırma işlemi. Ek bileşen kurulmuyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-uzun)
## Ne
Ayrı bir araç değil, bir iş akışı tekniği: Claude Code'da bağlı tüm MCP sunucularını/araçlarını listeleyip son bir ayda kullanılmayanları kapatmak; ardından /context çıktısında tools satırının 'deferred' olduğunu doğrulamak.
## Mekanizma
Bağlı her MCP sunucusunun araç tanımları bağlamı (context) doldurur. Kullanılmayan sunucuları anahtarla (toggle) kapatmak bu tanımların bağlama yüklenmesini engeller. /context komutu, tools satırının 'deferred' (gerektiğinde yüklenen) olup olmadığını gösterir. Video sayfasından yalnızca başlık alınabildi; ayrıntılar videonun özet bulgusuna dayanıyor, doğrulanmadı.
## Kanıt
- Ay içinde kullanılmayan bağlı araçları kapatmak token tasarrufu sağlar → sınanamadı · Video sayfası getirildi ama yalnızca başlık/bağlantılar geldi; transkript yok. Bulgu: 'turn off anything you have not used in the last like month'.
- /context'te tools satırı 'deferred' görünmelidir → sınanamadı · Yalnızca video bulgusunda geçiyor; yerelde çalıştırılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code içinde /mcp ile bağlı sunucuları listele
- Son ayda kullanılmayan sunucuları kapat/devre dışı bırak
- /context çalıştırıp tools satırının 'deferred' olduğunu kontrol et
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Bağlam ve token tüketimini düşürür, araç seçimi karmaşasını azaltır; sıfır maliyetli.
## Maliyet/risk
Düşük. Gerekli bir sunucuyu kapatırsan görev sırasında araç eksik kalır; yeniden açmak gerekir. Video iddiaları bağımsız doğrulanmadı.
## Tasarruf
Kapatılan sunucuların araç şemaları bağlama girmez; her oturumda sabit token yükü azalır. Miktar bilinmiyor, sunucu sayısına bağlı.
## Üretilebilir
hedef_tur: skill
tarif: 'mcp-temizlik' skill'i: adımlar olarak /mcp listesini al, her sunucunun son 30 gündeki kullanımını (oturum kayıtlarından/kullanıcıdan) sor, kullanılmayanları kapatmayı öner, ardından /context ile tools satırını kontrol ettir. Kod gerektirmez; salt talimat metni yeterli.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-uzun/panel.md → Ömer sütunu
## Özellikler
### Kullanılmayan MCP sunucularını anahtarla kapatma
kaynak: https://www.youtube.com/watch?v=kHtOSJRUkLs
### /context ile tools satırının 'deferred' durumunu doğrulama
kaynak: https://www.youtube.com/watch?v=kHtOSJRUkLs
## Destek
- kHtOSJRUkLs · 8:39 · Tüm bağlı araçları anahtarlarla listeleyen panelde ay içinde kullanılmayanları kapatmak; /context'te tools satırının 'deferred' olduğunu kontrol etmek. · kanıt: turn off anything you have not used in the last like month
