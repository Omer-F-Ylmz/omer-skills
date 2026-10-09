# Tasarım skill'i (design overhaul)
ad: Tasarım skill'i (design overhaul)
tur: skill
video: BiEvvC_66AQ
repo: nextlevelbuilder/ui-ux-pro-max-skill
lisans: MIT (doğrulanmadı: LICENSE dosyası var, içeriği okunamadı; MIT olduğu hatırlanan bilgi)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
telemetri: Bilinmiyor. İncelenen README bölümünde telemetri ifadesi görülmedi, kod taranmadı. Betikler yerel Python çalıştırır, ağ çağrısı yapıp yapmadığı doğrulanmadı. Google Fonts ve ikon kataloğu yenileme betikleri (refresh-*) ağa erişir.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Videoda adı verilmeyen, "60'tan fazla stille genel yapay zeka çıktısını profesyonel gösteren" bir tasarım skill'i anlatılıyor. Video ayrıntısı alınamadı (video getir hata verdi; yalnızca video kimliği verildiği için URL gerekiyordu). Aramada bu tanıma uyan ve en çok kurulan aday UI UX Pro Max çıktı. Eşleşme KESİN DEĞİL, varsayım. Bu skill, yapay zeka ajanına UI/UX tasarım kararları için aranabilir bir bilgi tabanı ve tasarım sistemi üretici veriyor. Arama sonuçları 67 stil, 161 palet, 57 yazı tipi eşleşmesi ve 99 UX kuralı diyor. Repo README rozetleri 79 aranabilir stil ve 192 muhakeme kuralı diyor; sürümler arasında sayı değişiyor.
## Mekanizma
Skill, CSV tabanlı bir tasarım veri seti (stil, renk paleti, yazı tipi çifti, UX kuralı, grafik türü, teknoloji yığını) ve bir Python arama betiği içerir. Ajan proje tanımını verir. Muhakeme motoru ürün türüne göre sayfa deseni, stil, renkler, tipografi, efektler ve kaçınılacak anti-desenleri (ör. mor-pembe yapay zeka gradyanları) seçer. Çıktı, teslim öncesi kontrol listesiyle birlikte tam bir tasarım sistemidir. Claude Code'da eklenti olarak ya da npm CLI ile kurulur. Repoda .claude-plugin, src/ui-ux-pro-max, cli (npm paketi ui-ux-pro-max-cli), gallery ve doğrulama betikleri var.
## Kanıt
- 60'tan fazla stille genel yapay zeka çıktılarını profesyonel gösterir → sınanamadı · Video içeriği alınamadı. Arama sonuçları UI UX Pro Max için 67 stil, repo rozeti 79 stil diyor. Kalite etkisi denenmedi, yalnızca stil sayısı kaynaklarda destekleniyor.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- /plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
- /plugin install ui-ux-pro-max@ui-ux-pro-max-skill
- Alternatif: npm paketi ui-ux-pro-max-cli (adı README rozetinden; kurulum komutu doğrulanmadı)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Genel yapay zeka görünümlü arayüzleri, ürün türüne uygun stil, palet ve tipografiyle daha tutarlı hâle getirir. Anti-desen listesi ve teslim kontrol listesi vardır.
## Maliyet/risk
Kimlik belirsiz: video skill'in adını vermedi, eşleşme varsayımdır. Lisans ve yıldız sayısı doğrulanmadı. Sürümler arası stil sayısı tutarsız (60+, 67, 79). Üçüncü taraf eklenti ve Python betikleri çalıştırır, kurmadan önce incelenmeli. Kod incelenmedi. Çıktı kalitesi bağımsız ölçülmedi. README'de bağış ve tanıtım bağlantıları var.
## Tasarruf
Token aracı değil. Dolaylı etki: ajan, tasarım kararlarını uzun deneme-yanılma yerine hazır veri setinden aratarak aldığı için yeniden yazım turları azalabilir. Ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: Kendi tasarım skill'imizi yazın. (1) skills/tasarim/ altında SKILL.md oluşturun. (2) CSV'lerle ürün türü→stil/palet/yazı tipi/anti-desen eşleştirme tablosu ekleyin. (3) Anahtar kelime aramalı küçük bir Python betiği ekleyin. (4) Teslim öncesi kontrol listesi ekleyin: emoji yerine SVG ikon, kontrast, cursor-pointer, duyarlılık. Veriyi sıfırdan, bizim projelerimize uyarlayın. Yukarıdaki repo yalnızca fikir kaynağı olsun, lisansı doğrulanmadan veri kopyalanmasın.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### Tasarım sistemi üretici: ürün türüne göre desen, stil, renk, tipografi, efekt ve anti-desen önerir
kaynak: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
### 67+ UI stili, 161 palet, 57 yazı tipi çifti, 99 UX kuralı (sayılar arama sonucuna göre)
kaynak: https://mcpmarket.com/tools/skills/ui-ux-pro-max-8
### Claude Code eklentisi olarak marketplace üzerinden kurulum
kaynak: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
## Destek
- BiEvvC_66AQ · 0:24 · 60'tan fazla stille genel yapay zeka çıktılarını profesyonel gösterir. · kanıt: design overhaul skill with over 60 styles that makes generic AI outputs look professionally done
