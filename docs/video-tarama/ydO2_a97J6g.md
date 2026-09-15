# CLAUDE CODE İLE 1 SAATTE PROFESYONEL WEB SİTESİ YAP VE SAT: 2026 REHBERİ
kanal: Burhan KOCABIYIK · süre: 24 dk · altyazı: tr manuel
ana iddia: Claude Code'a referans sitenin PDF'i, araç/deploy tarifli bir md dosyası, frontend-design skill'i ve fal.ai anahtarı verilip bypass modunda bırakılınca Framer/Webflow'suz profesyonel, çok dilli site üretip Vercel'e çıkarır ve bu hizmet Apify ile bulunan şirketlere e-postayla satılır (iddialar: ~25 dk üretim, 99 sayfa, %7-12 e-posta dönüşü, 2.000-3.000 dolarlık site değeri; bağımsız ölçüm yok, deploy ilk denemede gerçekleşmedi).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| davila7/claude-code-templates (aitmpl.com) | ÇİFT | ELENDİ | "claude skills" kataloğu; Claude Code plugin marketplace'leriyle (claude-plugins-official, omer-skills) aynı iş; videoda buradan alınan tek skill frontend-design zaten kurulu (30.7k yıldız, aktif) |
| fal.ai + Nano Banana 2 (görsel, image edit) + Veo 3 (video) | YENİ | ELENDİ | ücretli API anahtarı Claude'a veriliyor; videonun kendi uyarısı: limitsiz 100 istek 100 dolarlık işlem başlatabilir; Bölüm 5 görsel yoksa placehold.co |
| Vercel (GitHub bağlantılı otomatik deploy) | YENİ | ELENDİ | deploy frontend-craft kapsamı dışı, hesap+login ister; ajan "canlıya aldım" dedi ama son deploy 2 gün önceydi, elle redeploy gerekti; "her değişiklikte GitHub'a push" önerisi push-yalnız-istenince ilkesiyle çelişir |
| ücretli üretim çağrısına prompt'ta adet tavanı ("maksimum 30 görsel veya 10 video") | YENİ | BİLGİ | limitsiz istekte kontrolsüz maliyet (sözlü uyarı, ölçüm yok) |
| animasyonlu açılış + animasyonlu logo + Veo 3 videoları (v2 "daha profesyonel" sürüm) | YENİ | ELENDİ | proje-özgü stil kararı, genel kural değil; Bölüm 3 "gereksiz animasyon yok" ile gerilimli |
| diğer: frontend-design skill · 21st.dev bileşen/animasyon prompt'u kopyalama · referans siteyi PDF (print) ya da layout/stil kodu olarak verip birebir kopyalatma · proje başında araç/yetki/deploy tarifli md dosyası · Claude Code izin modları (auto-accept edits, bypass permissions, plan) + VS Code eklentisi · "deploy ettim" iddiasını Deployments zamanıyla doğrulama | ZATEN VAR | ELENDİ | sırasıyla: kurulu plugin · 21st plugin+MCP ve Bölüm 10 · Bölüm 0 REF (pdf/png), başka sitenin kodu/görseli Bölüm 10 "kopyalama" ile çelişir · CLAUDE.md + Bölüm 7 DESIGN.md · yerleşik · CLAUDE.md "kanıtsız bitti yok" |
| diğer: Google Antigravity · Apify (Google Maps scraper) · Instantly · n8n · Calendly · Framer/Webflow | YENİ | ELENDİ | IDE değişikliği / satış-lead / otomasyon / site içi takvim / videoda "artık gereksiz" denen site kurucular; tasarım disiplini kapsamı dışı |
## ölçütler (YENİ)
- fal.ai + Nano Banana 2 + Veo 3: bakım=bilinmiyor (servis/model, repo verilmedi) · çift=örtüşme yok (kurulu sette görsel/video üretimi yok) · izin=FAL API anahtarı, istek başına ücretli kullanım · context=0 kalıcı, yalnız çağrılınca · kurulum: —
- Vercel: bakım=bilinmiyor (servis) · çift=örtüşme yok · izin=Vercel hesabı + tek seferlik kodla login, GitHub repo bağlantısı · context=0 kalıcı, yalnız çağrılınca · kurulum: —
- adet tavanı / animasyonlu açılış-logo (teknikler): bakım=— (teknik) · çift=örtüşme yok (animasyon kısmen Bölüm 3) · izin=yok · context=yalnız kural satırı · kurulum: —
- diğer (Antigravity, Apify, Instantly, n8n, Calendly, Framer/Webflow): bakım=bilinmiyor · çift=örtüşme yok · izin=hesap/login (Webflow ücretli: "euro para veriyordum"), IDE kurulumu · context=0 (Claude Code'a bağlanmıyor) · kurulum: —
## hedefler (BİLGİ)
- ücretli üretim/API çağrısı yaptıran prompt'a adet tavanı yaz (ör. "en fazla N görsel, fazlasını oluşturma") → CLAUDE.md (ücretli üretim/API çağrıları)
---
## ek: tasarım
prompt:
- v1 (md dosyası üretimi): metin altyazı/açıklamada yok — yalnız ekranda; anlatılan: md dosyası oluştur, Nano Banana ve fal.ai kullan, çok kaliteli bir web sitesi yap, arayüz için frontend-design skill'ini kullan, fal ile en fazla 30 görsel veya 10 video, bitince Vercel'de canlıya al (sözlü özet, birebir değil)
- v2 (ertesi gün): metin altyazı/açıklamada yok — yalnız ekranda; anlatılan: her şey aynı kalsın, Nano Banana ve Veo 3 kullan, Leftflow logosunu animasyonlu yap, beğendiğim ajans sitesine bak, form otomasyonunu bağla (sözlü özet, birebir değil)
- "Bu web sitesinin birebir aynısını yapmasını istiyorum. Yapmanı istiyorum diyelim." (sözlü)
- "Kendin birebir Horizons'ı oluştur. Öncekiyle alakası olmasına gerek yok. Bir de AI generated e görseller birazcık aslında biraz kalitesiz duruyor. Onları da düzelt. Yerine daha profesyonel gerçek insan resimleri koy. E nado banana 2'yi kullan. görseller olsun. Hatta birebir aynılarını nanı banana image edit ile oluş. Bunun için de fay kullan." (sözlü)
- videoda açıklamalara detaylı prompt ve hazır MD dosyası konacağı söyleniyor; açıklamada prompt/MD yok, yalnız ücretli Gumroad ürün linkleri var (açıklama)
referans siteler: Leftflow? (yazarın kendi şirket sitesi, v1'de PDF olarak verildi), Horizons? (v2'de birebir kopyalatılan ajans sitesi; ad yalnız promptta geçiyor), 21st.dev, aitmpl.com
stiller: yok
premium kararlar:
1) Arayüzün "vibe coded gibi durmaması" için UI kit / frontend-design skill'ini md proje dosyasına eklemek (iddia; skill'li-skill'siz karşılaştırma yok)
2) İlk sürüm "benim için yeterli değil" denip beğenilen ajans sitesi referans verilerek birebir kopyalatıldı: animasyonlu açılış, animasyonlu logo, Veo 3 ile videolar, takvimden toplantı alma
3) "Kalitesiz duran" AI görseller yerine "daha profesyonel gerçek insan resimleri"; referans görsellerin birebir benzerleri Nano Banana 2 image edit ile (sonuç altyazıda gösterilmiyor, işlem ~30 dk sürecek denip video bitiyor)
4) "Yarışmaya katılabilecek kadar güzel" site için 21st.dev'den arka plan/animasyon prompt'unu kopyalayıp vermek; gerekçe: "yapay zeka her zaman kısa yolu düşünür" (iddia, örnek sonuç yok)
