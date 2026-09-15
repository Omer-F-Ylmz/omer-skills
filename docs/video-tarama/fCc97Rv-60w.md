# Claude Fable 5.1 İnanılmaz Web Siteleri Tasarlıyor… Ama Bedeli Var
kanal: Yıldız Dikme · süre: 13 dk · altyazı: otomatik tr
ana iddia: Aynı yarım proje, aynı prompt ve aynı dört tasarım skill'iyle Fable 5.1, Fable 5'ten daha bütünlüklü ve scroll boyunca süren bir site kurguluyor ama çok daha fazla kredi ve süre yiyor, bu yüzden yalnız kritik işlere değer (kredi/süre sözlü yaklaşık değer, kıyas yalnız görsel).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| singhharsh1708/scrollcraft? | YENİ | ELENDİ | açıklamadaki 4 skill'den biri; owner videoda yok, aynı adlı Claude Code plugin'i ad eşleşmesiyle bulundu; ffmpeg dış kurulumu ister (izin kötü), 60 yıldız |
| zanwei/design-dna? | ÇİFT | ELENDİ | referans UI (görsel/URL) → Design DNA JSON (token, stil, efekt) → UI; frontend-craft REF modu + Bölüm 10 + DESIGN.md token'ları ve impeccable extract aynı işi yapıyor |
| Leonxlnx/taste-skill (design-taste-frontend)? | ÇİFT | ELENDİ | jenerik "slop" tasarımı engelleyen zevk skill'i; kurulu frontend-design + impeccable + frontend-craft Bölüm 3 YASAK listesiyle aynı iş |
| Scroll anlatısı: süreklilik ipi + geri dönen geçiş | YENİ | BİLGİ | tek çizgi/border scroll boyunca kaybolmadan bölümleri bağlıyor, portal geri scroll'da eski yerine dönüyor; "ödüllü sitelerin ödül sebebi" iddiası, kanıt yok |
| Sektör uygunluğu (uzun scroll deneyimi) | YENİ | BİLGİ | dinamik uzun scroll creative / uluslararası "kendini ispat" sektörlerine öneriliyor, e-ticarete önerilmiyor; Bölüm 11 künyesinde sektör uygunluğu yok |
| En pahalı modeli kritik işe ayırma | YENİ | BİLGİ | Fable 5.1 yalnız yeni projenin ana tasarımı / çözülemeyen bug için; iddia: ilk prompt ~%40 kredi (Fable 5 ~%25-30), ~38-45 dk (Fable 5 ~30 dk), sözlü yaklaşık |
| diğer: frontend-design, Awwwards seviyesi hedefi, korunacak bölümü prompta yazma ("ilk girişi bozma"), font/görsel/boşluğa dikkat şablonu | ZATEN VAR | ELENDİ | frontend-design@claude-plugins-official kurulu; awwwards.com Bölüm 10; CLAUDE.md cerrahi değişiklik; Bölüm 3 tipografi/spacing + Bölüm 7 token'lar |
| diğer: kısa prompt + tasarımı tamamen modele bırakma, aynı prompt/skill ile model A/B kıyası | YENİ | ELENDİ | ilki Bölüm 0 marka kararı + Bölüm 11 "seçim kullanıcınındır" ile çelişir; ikincisi tek seferlik deney, kural/kurulum değil |
## ölçütler (YENİ)
- singhharsh1708/scrollcraft?: bakım=pushed_at 2026-09-11, 60 yıldız, archived=false (gh search ad eşleşmesi) · çift=kısmi: verify.mjs/serve.mjs frontend-craft screenshot/audit/serve ile örtüşür, canvas kare dizisiyle scroll-scrub site üretimi kurulu sette yok · izin=ffmpeg dış ikili kurulumu + Node 22+; skill için API anahtarı yok (hosted editörün metin asistanı opsiyonel SARVAM_API_KEY) · context=plugin: 1 skill açıklaması + 2 slash komut (/scrollcraft-new, /scrollcraft-build) her oturum · kurulum: —
## hedefler (BİLGİ)
- Scroll anlatısı (tek çizgi/border bölümler arası taşınır ve kaybolmaz; scroll'a bağlı geçiş geri scroll'da tersine döner) → DESIGN.md şablonu (Hareket)
- Sektör uygunluğu (uzun scroll/dinamik anlatım yalnız creative/uluslararası marka; e-ticarette yok) → frontend-craft Bölüm 11 (yön künyesi)
- En pahalı modeli yalnız ilk ana tasarım ve çözülemeyen bug'a ayırma → CLAUDE.md (CONTEXT DİSİPLİNİ, model maliyeti)
---
## ek: tasarım
prompt:
metin altyazı/açıklamada yok — yalnız ekranda; anlatılan içerik aşağıda
"her iki modelden de yarım kalan bir web sitesini kendi tasarım kararlarıyla tamamlamasını ve projeyi Awwwards seviyesinde, premium ve etkileşimli bir web deneyimine dönüştürmesini istiyorum" (açıklama)
ilk girişi (portal girişini) bozma, oradan sonrasını tamamla; şirket tüm dünyaya hizmet ediyor (sözlü özet, birebir değil)
ana tasarımdaki fontlara, görsellere, boşluklara çok dikkat et (sözlü özet, birebir değil)
Awwwards seviyesinde, ödül alacak seviyede yap; oradaki tasarım kurallarını kullan (sözlü özet, birebir değil)
skill'ler: design-dna, frontend-design, design-taste-frontend, scrollcraft (açıklama)
Fable 5'e aynı prompt, farklılık yok, yalnız model 5 seçildi (sözlü özet, birebir değil)
referans siteler: awwwards.com ("Awwwards seviyesi" hedefi); adı verilmeyen büyük uluslararası para transferi sitesi yalnız ekranda gösteriliyor (scroll'da bilgisayarın içine giriş, sağa kayan panel, partner logoları)
stiller: Awwwards style (sözlü: "Awards style seviyesi"), minimal (sözlü, kişisel tercih: çapraz yazı, görselsiz ülke listesi); premium, etkileşimli (açıklama, hedef)
premium kararlar:
1) Sitede "devam hikayesi": tek çizgi/border scroll boyunca kaybolmadan portaldan karta ve para birimlerine kadar tüm akışı taşıyor — "ödül alan web sitelerin genellikle ödül almasının sebebi bu" (iddia, kanıt yok)
2) Korunan portal girişi scroll'a bağlı: ileri scroll'da border görselin üstüne oturuyor, geri scroll'da eski yerine dönüyor, kasılmadan smooth ("akılda kalıcı")
3) Sektöre özgü etkileşimli öğeler: yansımalı üç boyutlu kredi kartı, scroll'la kayan para birimi slaytı ve değişen ülke adları (Fable 5'te ülke saatleri) — "krediyi hak etti" (yalnız görsel kıyas)
