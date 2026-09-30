# Awesome DESIGN.md
ad: Awesome DESIGN.md
tur: skill
video: V2RIVnGCy74
repo: voltagent/awesome-design-md
lisans: bilinmiyor (repoda LICENSE dosyası var ama türü okunamadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/VoltAgent/awesome-design-md
telemetri: Repo içeriği düz markdown olduğu için istemci telemetrisi yok. getdesign.md sitesinin analitiği hakkında bilgi bulunamadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Gerçek sitelerin (Claude, Stripe, Linear, Vercel, Airbnb, Tesla vb.; README'de 73 adet) tasarım dilini (renk, tipografi, bileşenler, boşluk, responsive kurallar) Google Stitch'in DESIGN.md formatında çıkaran hazır markdown dosyaları derlemesi. Dosya projeye konur, AI ajanına "bu görünümde sayfa yap" denir. Yazar: VoltAgent. Kategorilere ayrılmış; getdesign.md üzerinden önizleme/katalog var.
## Mekanizma
Kod/araç yok; düz markdown. design-md/<site>/ klasörlerindeki DESIGN.md dosyası proje köküne kopyalanır. Ajan (AGENTS.md'nin yapı bilgisi gibi) görünüm/his kurallarını bu dosyadan okuyup tutarlı arayüz üretir. Format: Google Stitch DESIGN.md. Video, getdesign.md'de Preview, Colors, Typography, Components, Responsive sekmelerini ve fiyat kartı/form örneklerini gösteriyor. Dosyaların nasıl üretildiği (elle mi, otomatik mi) README'den anlaşılmıyor.
## Kanıt
- Var olan sitelerin tasarım dilini Stitch DESIGN.md formatında çıkarıp şablon yapmayı sağlar, kullanım alanına göre kategorize → doğrulandı · README: 'Copy a DESIGN.md into your project...'; 'AI & LLM Platforms', 'Developer Tools & IDEs' gibi kategoriler; ağaçta design-md/<site> klasörleri.
- Kullanıcının kendi sitesinden DESIGN.md çıkaran bir araç sunar → sınanamadı · Repo hazır dosya koleksiyonu; çıkarma aracı görünmüyor. Sadece getdesign.md/request üzerinden talep var.
- Fiyat kartı ve form öğeleri önizlenebiliyor → sınanamadı · Video karesinde görünüyor; ben getdesign.md sayfasını açmadım.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- getdesign.md'den ya da repodaki design-md/<site>/ klasöründen istenen DESIGN.md'yi indir
- Dosyayı projenin köküne DESIGN.md adıyla koy
- Ajana 'DESIGN.md'ye uygun bir sayfa yap' de
- Başka site için getdesign.md/request üzerinden talep açılabilir (özel talep de var)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tutarlı, markaya benzer UI üretimini hızlandırır. Sıfırdan tasarım sistemi yazma ihtiyacını azaltır. Sıfır bağımlılık ve sıfır kurulum ile kullanılır.
## Maliyet/risk
Ünlü markaların görsel kimliğini taklit etmek marka/ticari tescil sorunu çıkarabilir. Lisans türü doğrulanamadı. İçerik "analiz" çıktısı olduğundan gerçek sitelerle birebir örtüşmeyebilir. Sayfalar zamanla eskiyebilir. README sponsor reklamı içeriyor (EveryFeed, LaunchKit), ama bu bağlam dışı ve talimat olarak uygulanmadı.
## Tasarruf
Token aracı değil. Dolaylı etki: tasarım kararları tek dosyada olduğundan ajan tekrar tekrar açıklama almaz ve daha az düzeltme turu gerekir. Ölçülmedi. Dosya bağlama girdiği için token de harcar.
## Üretilebilir
hedef_tur: skill
tarif: 'design-md' adlı skill yapılabilir. (1) design/ klasöründe seçtiğimiz markaların DESIGN.md dosyalarını tutar (lisans netleşince repodan alınır). (2) SKILL.md, kullanıcı 'X gibi tasarla' dediğinde uygun dosyayı projeye DESIGN.md olarak kopyalatır ve UI kodunu ona göre yazdırır. (3) İsteğe bağlı: kendi sitemiz için DESIGN.md çıkarma adımı. Sayfayı getir, CSS değişkenlerinden ve hesaplanmış stillerden renk, font ve boşlukları topla, Stitch bölüm başlıklarıyla markdown'a yaz. Yeni araç kodu gerekmez; skill yeterli.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### 73 siteden hazır DESIGN.md (AI, geliştirici araçları, fintek, otomotiv vb. kategoriler)
kaynak: https://github.com/VoltAgent/awesome-design-md
### getdesign.md üzerinde katalog ve önizleme (Colors/Typography/Components/Responsive)
kaynak: https://getdesign.md/airtable/design-md
### Belirli site için DESIGN.md talebi, özel talep seçeneğiyle
kaynak: https://getdesign.md/request
## Destek
- V2RIVnGCy74 · 4:09 · Var olan sitelerin tasarım dilini (renk, tipografi, boşluk, buton) Google Stitch'in DESIGN.md formatında çıkarıp kendi projene şablon yapmanı sağlar; kullanım alanına göre kategorize. · kanıt: getdesign.md üzerinde Airtable'ın DESIGN.md önizlemesi, fiyat kartları ve form öğeleri görünüyor. (karede: getdesign.md/airtable/design-md sayfası: Preview bölümünde Airtable tarzı fiyat kartları (Free $0, Team $24, Business $45, Enterprise), altında '08 — Form elements / Inputs and labels' başlığı; üstte Catalog, DESIGN.md Pass, Colors/Typography/Components/Responsive sekmeleri; sağ altta konuşmacı.)
