# Prompt Değil, Skill! Claude ile Ödüllü Web Sitesini Böyle Yaptım | Yazılımcı Gözüyle
kanal: Yıldız Dikme · süre: 17 dk · altyazı: otomatik tr
ana iddia: Uzun teknik prompt yerine dört Claude skill'i (Design DNA, Frontend Design, Taste Skill, Scrollcraft) ve AI ile üretilmiş bir kaynak video verilince pear.no'dan ilham alan, scroll ile ilerleyen ödül kalitesinde site çıkar; "en fazla 10 skill yeter" (yalnız ekran gösterimi, ölçüm yok).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| zanwei/design-dna | YENİ | ADAY | referans görsel/URL'den token + stil + efekt JSON'u çıkarıp ona göre üretir; videodaki "video atın" iddiası README'de yok (görsel/screenshot/URL); k-means ile ölçülmüş hex, REF modunda böyle bir araç yok |
| nateherkai/scroll-craft | YENİ | ADAY | videodaki scroll'la ilerleyen sitenin bununla yapıldığı iddia; README: scroll'a bağlı video scrub, 8 sayfa grameri, headless tarayıcıyla scroll konumlarında doğrulama |
| Leonxlnx/taste-skill | ÇİFT | ELENDİ | anti-slop + yarım projenin dilini okuyup sürdürme = frontend-design + impeccable + frontend-craft Bölüm 3/7 (DESIGN.md mirası); kadran fikri aşağıda BİLGİ |
| Seedance 2.5? | YENİ | ELENDİ | ASR "CDNs 2.5": scroll sitesinin kaynak videosunu üreten AI video modeli, "çok güçlü" iddia; Claude Code dışı, kurulum kalemi değil |
| Tasarım kadranları (deneysellik / hareket / yoğunluk) | YENİ | BİLGİ | sitenin "hareketli mi klasik mi" davranışını belirleme; DESIGN.md'de bu karar alanı yok, Bölüm 7 Hareket yalnız süre + easing |
| Yoğun sahneden nötr zemine geçiş (zemin ritmi) | YENİ | BİLGİ | mavi-sarı dinamik bölüm sonrası beyaz: göz yormuyor, dikkati toparlıyor (iddia, yalnız görsel); Bölüm 3 zemini tek karar sayıyor, bölümler arası geçişi değil |
| diğer: anthropics/skills (frontend-design), Awwwards ödüllü siteleri inceleme, referansı kopyalamadan analiz edip ilham alma, promptun başında skill'leri adıyla anma, responsive'i promptta isteme, hatayı ekran görüntüsüyle geri besleme | ZATEN VAR | ELENDİ | frontend-design@claude-plugins-official kurulu; Bölüm 10; CLAUDE.md /frontend-craft yükle + Bölüm 0; Bölüm 2 (390/768/1440); Bölüm 2/9 screenshot döngüsü |
## ölçütler (YENİ)
- zanwei/design-dna: bakım=pushed_at 2026-08-28, 1778 yıldız, archived=false · çift=kısmi: frontend-craft REF modu (Bölüm 0/2) + Bölüm 10 dil çıkarma; ölçülmüş renk yok · izin=Node + npx skills CLI, global (-g) kurulum; opsiyonel ölçüm scriptleri için npm install; API anahtarı yok (README) · context=her oturum 1 skill açıklaması · kurulum: npx skills add zanwei/design-dna -a claude-code -g -y
- nateherkai/scroll-craft: bakım=pushed_at 2026-09-04, 2454 yıldız, archived=false · çift=örtüşme yok; kendi refuse listesi ve 4px taban spacing frontend-craft Bölüm 3 8px ölçeğiyle çakışır · izin=Node 18+, tam ffmpeg, build klasörüne npm i playwright-core + Chrome; opsiyonel KIE_AI_API_KEY (üretilen video ücretli, README) · context=her oturum 1 plugin skill açıklaması, references yalnız çağrılınca · kurulum: /plugin marketplace add nateherkai/scroll-craft + /plugin install nateherk-design
- Seedance 2.5?: bakım=bilinmiyor (repo yok, harici servis) · çift=örtüşme yok · izin=harici AI video servisi hesabı (videoda ücret/login ayrıntısı yok) · context=yok (Claude Code'a bağlanmıyor) · kurulum: —
## hedefler (BİLGİ)
- Tasarım kadranları: deneysellik / hareket / yoğunluk seviyesi açıkça yazılır (taste-skill README'de 1-10 kadran) → DESIGN.md şablonu (Token'lar)
- Yoğun renkli/dinamik bölümden nötr zemine geçiş bilinçli karar olarak yazılır → frontend-craft Bölüm 3 (Arka plan maddesi)
---
## ek: tasarım
prompt:
Türkçe + İngilizce prompt ekranda gösterildi, "aşağıya da bırakacağım" dendi ama açıklamada yok: metin altyazı/açıklamada yok — yalnız ekranda
ilk cümleler dört skill'i aktif kullanmasını söylüyor; skill kurulu olsa da anmak Claude'a hatırlatma (sözlü özet, birebir değil)
pear sayfasını aynısını yapmadan örnek alıp ilham alması, analiz ederek sıfırdan kurması (sözlü özet, birebir değil)
scroll davranışıyla tetiklenen, video scroll yaptıkça ilerleyen, ardından sahneyle ilgili yazıların geldiği kesintisiz akış; promptta kod yok (sözlü özet, birebir değil)
responsive, bütün cihazlara uyumlu yapması (sözlü özet, birebir değil)
düzeltme örneği: "burayı düzelt" "scroll yaptığında kaybolmasın" (sözlü)
mobil giriş düzeltme örneği: "buradan başlamasın da kadına doğru biraz daha başlasın" (sözlü)
referans siteler: https://pear.no/, Awwwards (awwwards.com)
stiller: Awwwards tarzı scroll odaklı premium, scroll ile anlatılan hikaye, minimal (beyaz bölüm); kaçınılan: generic AI landing page, neon renkler, template görünüm
premium kararlar:
1) Scroll'a bağlı ilerleyen video sahneleri + sahneyle gelen metinler + sayfada konumu gösteren navigation ile kesintisiz hikaye; önkoşul elde AI ile üretilmiş bir video olması
2) Yoğun mavi-sarı dinamik bölümden beyaz zemine geçiş; göz yormuyor, dikkati toparlıyor, minimal his veriyor (iddia, yalnız görsel gösterim)
3) Bütünlük: sahnedeki dairesel çizgilere uyan daire gösterge (mobilde küçültülmüş), hero ile aynı tam ekran footer, yazı fontu/rengi üst bölümle bağlantılı, videodan çarpıcı sahneleri kendisi seçmesi; footer'da mouse ile ışık efekti promptta yoktu, Claude'un kararı
