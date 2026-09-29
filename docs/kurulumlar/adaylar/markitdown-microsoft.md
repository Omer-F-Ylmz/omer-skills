# MarkItDown (Microsoft)
ad: MarkItDown (Microsoft)
tur: CLI
video: NogIRR1B6gY
repo: microsoft/markitdown
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/microsoft/markitdown
telemetri: README'de telemetri belirtilmiyor. Okuduğum kısımda ağa veri gönderen bir özellik görmedim ama README 288 satır kesildiği için tamamını görmedim, kesin değil. Azure Document Intelligence, YouTube transkripsiyonu ve ses transkripsiyonu gibi isteğe bağlı özellikler dış servis çağırabilir. Dosya ve URL erişimi çalışan sürecin yetkileriyle yapılıyor, README güvenlik uyarısı da bunu belirtiyor.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
Microsoft'un Python aracı. PDF, PowerPoint, Word, Excel, görsel (EXIF ve OCR), ses (transkripsiyon), HTML, CSV/JSON/XML, ZIP, YouTube URL ve EPub dosyalarını LLM'lerin okuyabileceği Markdown'a çevirir. Başlık, liste, tablo ve bağlantı yapısını korur.
## Mekanizma
Format başına bir dönüştürücü var (PDF, docx, pptx, xlsx vb.). Her biri dosyadaki metin ve yapıyı okuyup Markdown üretir. CLI şöyle çalışır: `markitdown dosya.pdf -o dosya.md`. Girdi stdin'den de verilebilir. Python API'si `convert_local` ve `convert_stream` gibi işlevler sunar. Bağımlılıklar isteğe bağlı ekler olarak kurulur: `[pdf,docx,pptx]`. Azure Document Intelligence, OCR eklentisi ve üçüncü taraf eklentiler de var, eklentiler varsayılan olarak kapalı. Repoda ayrıca `markitdown-mcp` paketi (MCP sunucusu), `markitdown-ocr` ve örnek eklenti paketi bulunuyor.
## Kanıt
- PDF, Word ve Excel dosyalarını temiz markdown'a çevirir. → doğrulandı · README'deki desteklenen format listesinde PDF, Word ve Excel var. Amaç, LLM'lere Markdown vermek.
- Sayfa görsellerini kaldırarak token tüketimini azaltır. → sınanamadı · README, Markdown'ın token açısından verimli olduğunu söylüyor. Görsel kaldırma mekanizması ve ölçülmüş tasarruf oranı okuduğum kısımda yok. Bu yüzden sınayamadım.
- Adı 'Market Don'. → çürütüldü · Doğru ad MarkItDown. Videodaki telaffuz ya da çeviri hatası gibi görünüyor.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- python -m venv .venv ve etkinleştir
- pip install 'markitdown[all]' (ya da yalnızca gerekenler: 'markitdown[pdf,docx,pptx]')
- markitdown dosya.pdf -o dosya.md
- MCP için: packages/markitdown-mcp paketi
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ofis belgelerini ve PDF'leri LLM'e ham dosya ya da sayfa görseli olarak vermek yerine temiz metin olarak vermeyi sağlar. Bu hem bağlam maliyetini düşürür hem de tablo ve başlık yapısını korur. Tek CLI ile çok sayıda formatı kapsıyor. MIT lisanslı ve Microsoft tarafından geliştiriliyor.
## Maliyet/risk
Güvenilmeyen girdide süreç yetkileriyle dosya ve ağ erişimi yapabilir (README uyarısı). Girdiyi temizlemek ve en dar `convert_*` işlevini kullanmak gerekir. Taranmış PDF'lerde OCR olmadan metin çıkmayabilir. Çıktı yüksek sadakatli insan okuması için uygun değil. `[all]` kurulumu çok bağımlılık getirir. Eklentiler üçüncü taraf koddur. Python 3.10–3.14 gerekir.
## Tasarruf
Belge ikili biçimden (PDF, DOCX, XLSX) sade Markdown metnine çevrilir. README, Markdown'ı "token açısından verimli" diye tanıtır. Videodaki "sayfa görsellerini kaldırarak token azaltır" iddiası README'de açıkça geçmiyor. Mekanizma, görsel yerine metin çıkarımı yapması olabilir. Ölçülmüş bir tasarruf oranı bilinmiyor.
## Üretilebilir
hedef_tur: skill
tarif: Ayrı bir araç yazmaya gerek yok, markitdown'ı sarmalayan bir skill yeterli. Skill, kullanıcı PDF/DOCX/XLSX/PPTX verdiğinde önce `markitdown <dosya> -o <dosya>.md` komutunu çalıştırır. Sonra ham dosyayı değil .md çıktısını okur. Kurulum adımı olarak `pip install 'markitdown[pdf,docx,pptx,xlsx]'` eklenir. Güvenilmeyen kaynaklar için dosya yolunu doğrulama kuralı konur. İstenirse `markitdown-mcp` paketi MCP olarak bağlanır. Token tasarrufunu, dönüşümden önce ve sonra karakter sayısını karşılaştırarak ölçen bir adım da eklenebilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### PDF, PPTX, DOCX, XLSX/XLS, HTML, CSV/JSON/XML, ZIP ve EPub'ı Markdown'a çevirir
kaynak: https://github.com/microsoft/markitdown
### Görsellerden EXIF ve OCR, seslerden transkripsiyon, YouTube URL'sinden transkript çıkarır
kaynak: https://github.com/microsoft/markitdown
### markitdown-mcp paketiyle MCP sunucusu olarak kullanılır
kaynak: https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp
### Üçüncü taraf eklenti sistemi var (varsayılan kapalı, --list-plugins ile listelenir)
kaynak: https://github.com/microsoft/markitdown
## Destek
- NogIRR1B6gY · 0:22 · PDF, Word ve Excel dosyalarını temiz markdown'a çevirir. Sayfa görsellerini kaldırarak token tüketimini azaltır. · kanıt: Adı Market Don. Araca PDF, Word belgesi veya Excel dosyası veriyorsun.
