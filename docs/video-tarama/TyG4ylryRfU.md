# Hermes Agent'ı Böyle Çalıştırıyorum: Workflow'larımı Paylaşıyorum
kanal: Avenox · süre: 33 dk 26 sn · altyazı: tr (manuel/resmi)
ana iddia: NousResearch/hermes-agent'ı 4 gün boyunca tam zamanlı sanal bir çalışan gibi kendi server'ında izole bir sanal bilgisayarda çalıştırıp (Obsidian vault + GitHub senkronu, mail/GitHub erişimi, hafıza protokolleri, iş ilanı eleme, Typefully onaylı içerik akışı) kişisel asistan/otomasyon için önerir; kodlama tarafında yazar kendisi Claude Code + Codex dışına çıkmadığını, sistem içindeki "Fable" modelinin (API kredisiyle) çok pahalı olduğunu ve karşılaştırmaların ölçümsüz anekdot olduğunu ekliyor.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| NousResearch/hermes-agent | ÇİFT | ELENDİ | önceki taramada Gg35_iQWx7g, hAYPvExWmCw, XemheY_aM1g, 2n84xa99FRY, EezLdmm8l1c (6. anılış); videonun kendisi bu ajan hakkında, ayrı sürekli çalışan agent süreci + model sağlayıcı hesabı, Claude Code'un/auto memory'nin yerini alan rakip ürün, kurulacak eklenti değil |
| Typefully (typefully.com) | YENİ | ELENDİ | X/Twitter içerik taslağı+onay akışı; ücretli/hesaplı SaaS, Claude Code'a bağlanmıyor, yazarın kendi Hermes akışının çıktısını gönderdiği harici platform (bkz. ölçütler) |
| openai/codex | ÇİFT | ELENDİ | önceki taramada 96LqaW9-7GY, LbBC5Wew4qs, EezLdmm8l1c, 2n84xa99FRY (aynı kanalın önceki videosu); burada Hermes içinde alt-ajan olarak "kodekse istek yolladı" — Claude Code'a alternatif/rakip ajan, kurulum önerisi yok |
| "Fable" (Claude model, ASR/kod adı belirsiz) | ÇİFT | ELENDİ | önceki taramada 1TI4Fd89fuw, as1W0ijkCqA, aa84rWKk8kw, fCc97Rv-60w, Yunu27g7sLw, 2n84xa99FRY, Gg35_iQWx7g, XemheY_aM1g — burada "inanılmaz pahalı" (API kredisiyle, ~50 cent/prompt) denip "kesinlikle kullanmayın" deniyor; kurulacak araç değil, model seçimi |
| Exa (arama tool'u) | ZATEN VAR | ELENDİ | "eksa tool'u filan da verdim" — ASR "eksa"; agent-reach skill'i içinde Exa zaten kurulu |
| diğer: Cloudflare (mail routing sorunu), Obsidian vault + GitHub senkron (kişisel "ikinci beyin"), kendi yazdığı hook/plugin, VALS (yazarın kendi adlandırdığı kişisel işletim sistemi) | YENİ | ELENDİ | hepsi yazarın kendi kişisel/özel altyapısı, isim/repo verilmiyor veya genel bilinen servis (Cloudflare); kurulum talimatı yok, doğrulanabilir bir "araç" değil |
## ölçütler (YENİ)
- Typefully (typefully.com): bakım=SaaS, GitHub reposu yok (gh api ile doğrulanamaz) · çift=örtüşme yok (kurulu sette X/Twitter içerik taslak-onay aracı yok) · izin=hesap + ücretli plan, X/Twitter API erişimi, Claude Code'a entegre değil (video: Cloud/Hermes içerikleri manuel/webhook ile Typefully'ye gönderiyor) · context=yok (Claude Code'a bağlanmıyor, harici web SaaS) · kurulum: — (ADAY değil; Teable/2n84xa99FRY-tarzı harici SaaS emsaliyle aynı gerekçe)
## hedefler (BİLGİ)
- yok
---
## ek: somut
- prompt: metin altyazıda yok — sistem kurulumu/promptlar "açıklamadaki link"te (X post, https://x.com/Avenoxai/status/2087479148608737602) paylaşılıyor, video içinde birebir prompt metni gösterilmiyor
- ayar: Docker container'dan kendi server'ında ayrı bir "sanal bilgisayar" altyapısına geçiş — gerekçe: Docker'ın modeli fazla sınırladığı gözlemi (sözlü, ölçümsüz)
- ayar: iş ilanlarından fırsat eleme "421 → 4" (sözlü iddia, ekranda gösterilmiyor)
- ayar: %99 iş modele bırakılıyor, %1 onay katmanı Telegram üzerinden korunuyor (draft + "ulaşayım mı?" onayı)
- ayar: 3 farklı hafıza katmanı kurulu (sözlü, detay ekranda; VALS = yazarın kişisel "işletim sistemi" adlandırması)
- ayar: gece boyunca birkaç "loop" bırakılıp kod yazdırılmadan yalnız plan/PRD topladırılıyor — haftalık limit resetlenme zamanlamasına göre (sözlü taktik)
- sayı: bir Fable promptu ~50 cent; Fable denemesi için ~25 dolarlık kredi harcandığı söyleniyor — yalnız iddia, fatura gösterilmiyor
- sayı: hermes-agent güncel repo durumu (kanıt: gh api) — pushed_at 2026-09-17, 246.422 yıldız, archived=false, MIT lisans, 43.806 açık issue
- not: açıklamadaki link (x.com/Avenoxai/status/...) "server kurulum rehberi" olarak tanıtılıyor ama içeriği bu taramada açılmadı/doğrulanmadı (X paylaşımı, video dışı kaynak); talimat "yalnız yt-dlp ile altyazı/metadata" kapsamının dışında kaldığı için okunmadı
