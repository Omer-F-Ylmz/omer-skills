# motionsites-ai
ad: motionsites-ai
tur: uygulama
video: JfmAm3sxCSc
repo: yok
lisans: yok
son_commit: yok
arsiv: hayır
kaynak: yok
telemetri: açık

## Ne
motionsites.ai — Lovable/Bolt/Cursor/Claude gibi AI kod üreticilerine yapıştırılmak üzere hazırlanmış, kategoriye göre filtrelenen ("Hero", "SaaS", "Portfolio", "3D", "Ecommerce", "Fintech" vb.) landing-page/animasyon prompt kartları galerisi. Slogan "Just copy, paste, and launch." Design Rocket (designrocket.io) markasıyla çapraz tanıtılıyor. Kapalı, hesap/ödeme katmanlı hosted web ürünü; indirilebilir paket veya API yok.

## Kanıt
- WebFetch motionsites.ai (2026-09-24): kategori etiketli prompt kartları + "Go Unlimited" ücretli üst katman var, fiyat gösterilmiyor; /pricing ayrı sayfa değil (404), muhtemelen ana sayfa sekmesi.
- WebFetch: "Powered by DESIGN ROCKET" birebir ifadesi bu içerikte görülmedi (statik fetch tüm bölümleri yakalamamış olabilir), ama designrocket.io'ya çapraz tanıtım ve paylaşılan logo dosyası marka bağlantısını doğruluyor.
- `gh search repos motionsites` (2026-09-24): resmi ürüne ait repo yok. "motionsites" adını taşıyan >10 depo bulundu (ör. xianxian-sensen/motionsites-prompts 90 yıldız, giglianepefrei/motionsites.ai-prompt-library 35 yıldız — açıklama "LIVE PREVIEW HEAR 👇"), hepsi Mayıs–Eylül 2026 arası açılmış. giglianepefrei deposunda pushed_at (2026-05-03) created_at'ten (2026-05-12) önce — geriye tarihlenmiş/sahte commit geçmişi, bilinen yıldız-şişirme + tık-tuzağı repo deseni. Hiçbiri resmi ürünle ilgisi olmayan üçüncü taraf klon/kazıma.
- Twitter/X reklam-izleme pikselleri sayfada mevcut (WebFetch gözlemi); telemetri açıklaması/kapatma kontrolü yok.

## Kurulum
Yok — kurulacak yerel paket/CLI/API yok. Akış: motionsites.ai üzerinden (isteğe bağlı) hesap açma, prompt kartını kopyalama, hedef AI builder'a (Bolt/Lovable/Cursor/Claude) yapıştırma. Serbest metin/URL tabanlı bir kurulum komutu yok, dolayısıyla Kurulum alanı boş.

## İzinler
Sayfada ayrıntılı izin listesi yok. Sign up akışı e-posta/hesap istiyor olabilir (doğrulanmadı — login sayfası açılmadı). Kurulacak yürütülebilir kod olmadığı için sistem/dosya izni söz konusu değil.

## Duman testi
Yapılamadı: kapalı kaynak hosted web ürünü, CLI/paket yok.

## Geri alma
Belirtilmemiş; hesap kapatma/veri silme talimatı sitede bulunamadı.

## Köprü izni
yok — bağlanacak CLI/salt-okur alt komut yok.

## Önerilen katman
RED — repo yok, lisans yok (kapalı SaaS), fiyatlandırma belirsiz ("Go Unlimited" ücretli katman), kurulacak/köprülenecek yürütülebilir yok. Ek güvenlik notu: ürün adını taşıyan GitHub deposu havuzu sahte-yıldız/backdated-commit deseniyle işaretli — bu depolardan hiçbiri KLONLANMADI, klonlanmamalı.

## Telemetri kapatma
Ürün içi toggle bulunamadı; tarayıcı düzeyinde reklam/izleme engelleyici (uBlock, Safari/Firefox izleme koruması) dışında kapatma yolu yok.

## Özellikler
### prompt-galerisi
ne: kategoriye göre filtrelenen, 3D sahne/animasyon/geçiş içeren hazır landing-page prompt kartları.
kurulum: yok (web sayfası, kopyala-yapıştır); bizde eşdeğer katalog yok.
lisans: yok
etiket: teknik
karar: RED
gerekce: güvenlik: ürün kapalı kaynak/hosted, kurulacak paket yok; "motionsites" adlı resmi olmayan depolar sahte-yıldız/tık-tuzağı deseni taşıyor (bkz. Kanıt) — indirip incelemek risk.

### kopyala-yapistir-prompt
ne: hazır prompt'u tek tıkla kopyalayıp doğrudan AI builder'a yapıştırma akışı; sıfırdan prompt yazma turunu atlar.
kurulum: yok (web butonu); bizde eşdeğer yok.
lisans: yok
etiket: token
karar: ÖĞREN
gerekce: prompt anatomisi → docs/kurulumlar/adaylar/motionsites-ai-kopyala-yapistir-prompt.md (23c-B: DENE ölçümü yerine kalıp çıkarımı; eski hipotez orada).

### mcp-entegrasyonu
ne: nav çubuğunda "MCP" (etiketli "New") — açıklama sayfada yok, işlevi doğrulanamadı.
kurulum: bilinmiyor.
lisans: yok
etiket: -
karar: ÖĞREN
gerekce: kanıt yetersiz (tek nav linki, içerik açılmadı); kurulmadan/aboneliksiz doğrulama yapılamadı.

## Mekanizma
### prompt-galerisi
nasıl: prompt, animasyon/3D-sahne/scroll/tipografi kararlarını (ör. framer-motion geçiş süresi, tailwind yerleşim sınıfları, 3D hero sahne parametreleri) tek bloklu doğal dilde önceden sabitler; AI builder açık uçlu istek yerine bu spec'i alır.
neden: bitmiş spec, aç-üret-eleştir-yeniden-üret turlarının çoğunu tek isteğe indirir; belirsizlik prompt metninde zaten çözülmüş olduğundan ek tur/token harcanmaz.
koşul: projenin kendine özgü marka/bileşen kısıtları varsa yine düzeltme turu gerekir; hedef model zaten ilk turda iyi animasyon/3D üretiyorsa kazanç marjinal.
bizde: frontend-craft skill'inde karşılığı yok; fikir olarak "hazır UI-teknik prompt şablonu" kataloğu eklenebilir (uyarlama, kod kopyalanmaz — RED olduğu için şimdilik uygulanmıyor).

### kopyala-yapistir-prompt
nasıl: kullanıcı filtrelenmiş karttan metni kopyalar, doğrudan AI builder'a yapıştırır; sıfırdan yazım/deneme-yanılma turu atlanır.
neden: sıfırdan prompt genelde ilk taslak → eksik detay → yeniden isteme turlarını gerektirir; test edilmiş hazır prompt bunu tek isteğe indirir.
koşul: prompt genel amaçlı tasarlandığından proje-özel gereksinim (mevcut bileşen kütüphanesi/marka/içerik) varsa yine uyarlama turu gerekir.
bizde: departman-frontend `## Yapım promptu şablonu` + docs/departmanlar/frontend-promptlar.md; kalıplar oraya işlendi.

## Bağımsız kanıt
- GitHub API (gh search/api, 2026-09-24) — "motionsites" adını taşıyan üçüncü taraf depoların çoğu Mayıs–Eylül 2026'da açılmış, yüksek yıldız/düşük yaş oranı ve en az bir depoda pushed_at < created_at (backdated commit) — sahte-yıldız/tık-tuzağı deseniyle uyumlu, ürünle resmi bağlantısı yok.

## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| hazır AI landing-page prompt kütüphanesi | https://motionsites.ai (WebFetch 2026-09-24) | doğru | kategori etiketli kart galerisi "Just copy, paste, and launch" sloganıyla örtüşüyor | - |
| "copy prompt" butonu (video 8:09) | https://motionsites.ai (WebFetch 2026-09-24) | doğrulanamadı | statik fetch'te birebir buton metni görülmedi, yalnız yakın slogan var; video anı doğrulanmadı | - |
| "Powered by DESIGN ROCKET" ibaresi (video 9:42) | https://motionsites.ai (WebFetch 2026-09-24) | doğrulanamadı | birebir ifade sayfa içinde bulunamadı; marka bağlantısı (çapraz tanıtım, paylaşılan logo) dolaylı olarak var | - |
