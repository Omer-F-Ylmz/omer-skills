# infographic-builder skill
ad: infographic-builder skill
tur: skill
video: zKBPwDpBfhs
repo: yok
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: Skill'in kendisi telemetri yapmaz (bilinen yok); ancak istemler ve görseller harici görsel üretim API'sine gönderilir. Sağlayıcı kaydı bilinmiyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Claude Code skill'i: Nano Banana (Google Gemini görsel modeli, "Key AI" API üzerinden) ile markaya uygun 1:1 PNG infografik üretir ve şeffaf logoyu üstüne bindirir. Bilgi yalnızca video özetinden; repo yok.
## Mekanizma
Videoya göre: SKILL.md içinde iş akışı, marka rehberi (renk, font, ton) ve API referansı markdown dosyalarında tutulur. Claude konudan istem üretir, Nano Banana API'sine çağrı yapar, dönen 1:1 PNG'ye şeffaf logoyu (muhtemelen betikle, örn. Pillow) üstte bindirir. Kesin uygulama ayrıntısı doğrulanamadı; video sayfası metni (transkript) alınamadı.
## Kanıt
- Nano Banana ile markalı 1:1 PNG infografik üretir, şeffaf logo bindirir → sınanamadı · video getir yalnızca YouTube altbilgi/bağlantılarını döndürdü; transkript yok, repo yok.
- Logo üstte, marka rehberi ve API referansı markdown dosyasında → sınanamadı · Yalnızca aday bulgusunda belirtiliyor; bağımsız doğrulama yapılamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Kaynak repo yok; kurulum paketi bilinmiyor.
- Elle: .claude/skills/infographic-builder/SKILL.md oluştur, brand-guide.md ve api-reference.md ekle, logo.png (şeffaf) koy, API anahtarını ortam değişkeninde tut.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tekrarlanabilir, marka tutarlı infografik üretimi; logo bindirme manuel tasarım işini azaltır.
## Maliyet/risk
Kaynak kod yok, doğrulanamaz. Harici ücretli API anahtarı gerekir ve "Key AI" aracı üçüncü taraf olabilir (veri/maliyet belirsiz). Görsel modellerde metin hataları olabilir. Kanıt yalnızca video özetine dayanıyor.
## Üretilebilir
hedef_tur: skill
tarif: skills/infographic-builder/ altında: SKILL.md (tetik: infografik iste; adımlar: konu→yapı→istem), brand-guide.md (renk/font/ton), api-reference.md (Gemini görsel modeli uç noktası, anahtar ortam değişkeninden), scripts/overlay_logo.py (Pillow ile şeffaf PNG logoyu üst köşeye oranlı yapıştırır, 1:1 kırpma/doğrulama). Anahtar koda gömülmez.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### Nano Banana ile 1:1 PNG infografik üretimi
kaynak: https://www.youtube.com/watch?v=zKBPwDpBfhs
### Şeffaf logoyu görselin üstüne bindirme
kaynak: https://www.youtube.com/watch?v=zKBPwDpBfhs
### Marka rehberi ve API referansı markdown dosyalarında
kaynak: https://www.youtube.com/watch?v=zKBPwDpBfhs
## Destek
- zKBPwDpBfhs · 22:54 · Nano Banana (Key AI API) ile markalı 1:1 PNG infografik üretir, şeffaf logoyu üstüne bindirir. · kanıt: Logo üstte, marka rehberi ve API referansı markdown dosyasında.
