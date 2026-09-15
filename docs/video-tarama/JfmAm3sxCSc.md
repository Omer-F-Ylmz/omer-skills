# Claude’a Ödüllü Siteler Gibi 3D Website Yaptırdım | Yazılımcı Gözüyle
kanal: Yıldız Dikme · süre: 11 dk · altyazı: otomatik tr
ana iddia: Ödüllü bir sitenin atmosferini kopyalamadan; teknolojileri, dosyaları ve config parametrelerini (görsel sayısı, hız, boşluk) veren detaylı İngilizce prompt'la Claude (Opus 4.7) ~5 dakikada sıfırdan 3D Three.js spiral galerili site üretir, "diğerlerini bozma" kısıtlı ikinci prompt ince ayarı yapar (aynı prompt farklı sonuç verdi; ölçüm yok).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| mrdoob/three.js, greensock/GSAP | YENİ | ELENDİ | 3D spiral galeri Three.js ile istendi, GSAP yalnız açıklamada; proje başına JS bağımlılığı, ortama kurulacak araç değil |
| Motion Sites? | ÇİFT | ELENDİ | ASR "Motion Size", URL yok; Claude için site örnekleri + "copy prompt", premium abonelik, login yapılamadı; 21st MCP (inspiration) ve Bölüm 10 designprompts.dev ile aynı iş |
| prompt'u Türkçe yaz, AI'a İngilizceye çevirt | YENİ | ELENDİ | "AI agentlar İngilizceyi çok daha iyi anlıyor" iddiası, videoda ölçüm/kanıt yok; SKILL.md ve CLAUDE.md Türkçe |
| teknikler: ilhamı kopyalamadan atmosferi al · detaylı prompt (teknolojiler, dosyalar, config'te görsel sayısı/hız/boşluk) · düzeltmede "diğerlerini bozma" · boyutu sayıyla söyle · aynı prompt farklı sonuç | ZATEN VAR | ELENDİ | Bölüm 10 (kopyalama) · Bölüm 5 + Bölüm 7 Token'lar (`ad: değer`) · CLAUDE.md cerrahi değişiklik · Bölüm 9 (sıfat değil SAYI) · Bölüm 11 (üç yön) |
| seçili metin vurgusu (CSS ::selection) marka renginde | YENİ | BİLGİ | videoda "ince detaylar sitenin kalitesini gösteriyor" örneği (sözlü övgü, ölçüm yok); Bölüm 3 Renk maddesinde yok |
| hareket kuralına tetikleyiciyi yaz (yükleme / scroll / hover) | YENİ | BİLGİ | ilk çıktıda yazılar direkt geldi, scroll ile tetiklenen yavaş giriş ikinci prompt'la istendi; Bölüm 7 Hareket yalnız süre + easing istiyor |
| diğer: YildizDikme/3D-threejs-spiral-gallery, Hostinger, Netlify, Google Drive, yazarın prompt paylaşım projesi | YENİ | ELENDİ | demo kaynak kodu / sponsor / barındırma / prompt klasörü; ortam aracı değil, proje henüz fikir |
## ölçütler (YENİ)
- mrdoob/three.js, greensock/GSAP: bakım=three.js pushed 2026-09-15, 115552 yıldız; GSAP pushed 2026-04-13, 28425 yıldız; ikisi de arşivli değil · çift=örtüşme yok (ui-ux-pro-max'ta yalnız GSAP preset verisi) · izin=projeye npm/CDN bağımlılığı · context=0 (ortama yüklenmez) · kurulum: —
- İngilizce prompt / ::selection / hareket tetikleyicisi (teknikler): bakım=— (teknik) · çift=örtüşme yok (tetikleyici kısmen Bölüm 3 Animasyon, Bölüm 7 Hareket) · izin=yok · context=yalnız kural satırı, skill yüklenince · kurulum: —
- diğer (demo repo, Hostinger, Netlify, Google Drive, prompt projesi): bakım=demo repo pushed 2026-05-12, 19 yıldız, arşivli değil; diğerleri bilinmiyor · çift=örtüşme yok · izin=hesap/login (Hostinger ücretli) · context=0 · kurulum: —
## hedefler (BİLGİ)
- seçili metin vurgusunu (::selection) marka renginden türet → frontend-craft Bölüm 3 (Renk)
- her hareket kuralına tetikleyici yaz (yükleme / scroll'da görünme / hover) → DESIGN.md şablonu (Hareket)
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda (açıklamada yalnız Google Drive prompt linki)
- masaüstünde "new video" dosya yolu; orijinal, yaratıcı bir ajans web sitesi, tasarımı başka yerden alma, sıfırdan; üç boyutlu spiral görsel galeri (sözlü özet, birebir değil)
- kullanılacak teknolojiler: JavaScript, Three.js, CSS dosyaları, diğer JS dosyaları; config dosyasında genel ayarlar: toplam görsel sayısı, hız, görseller arası boşluk; sayfanın diğer kısımları (yazılar) için açıklama (sözlü özet, birebir değil)
- ikinci prompt (Claude'a İngilizce yazdırıldı): diğer yaptıklarını, görsel galeriyi kesinlikle bozma; yalnız en baştaki büyük yazıyı küçült; sayfanın geri kalanındaki yazılar scroll ile tetiklenen yavaş yüklenmeyle gelsin (sözlü özet, birebir değil)
referans siteler: studiodialect.com (ilham; "günün web sitesi seçildi" iddiası, ödül kurumu adı geçmiyor), stately-naiad-8f0d7f.netlify.app (videoda üretilen site), Motion Sites? (prompt galerisi, URL verilmiyor), github.com/YildizDikme/3D-threejs-spiral-gallery (kaynak kod)
stiller: yaratıcı ajans sitesi, 3D spiral görsel galeri (Three.js/WebGL), premium hero (açıklama)
premium kararlar:
1) Basit slider yerine mouse ve scroll'a tepki veren 3D spiral galeri: mouse ile döner, ne kadar hızlı kaydırılırsa o kadar hızlı döner
2) Yumuşak akış: scroll ile tetiklenen yavaş metin girişleri (ikinci prompt'la), açılışta bir anda yüklenmeyen geçiş, hızlı kaydırmada bile yavaş inen sayfa; hero'daki aşırı büyük yazı küçültüldü
3) İnce detaylar: hover'da görselin yavaşça geriye gitmesi (Claude'un kendi fikri), yakınlaştırma/hover efektleri, seçilen metnin site renkleriyle uyumlu olması ("sitenin kalitesini bu ince detaylar gösteriyor", ölçüm yok)
