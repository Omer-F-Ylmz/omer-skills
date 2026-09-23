# hyperagent
ad: hyperagent
tur: uygulama
video: vcU85OrwuV0
repo: yok
lisans: yok
son_commit: yok
arsiv: hayır
kaynak: yok

## Ne
Kapalı kaynak, hesap gerektiren SaaS "ajan filosu" platformu (hyperagent.com, Airtable ile bağlantılı — kurucu ekipten Alex McDonnell'ın bio'su "Hyperagent/Airtable"). Marketplace'inde "Council" adlı hazır bir akış var: 5 kişilik-ajanı (Contrarian/red-team, Expansionist/bull, Logician, Researcher, Buyer) bir fikri paralel olarak savunup çürütüyor, sonra bir "Judge" ajanı tek bir karar veriyor — ipucundaki "council of agents ile fikri stres testine sokan platform" tarifiyle birebir eşleşiyor. Ürün geneli: Slack/Telegram/webhook/zamanlanmış tetikleyicilerle çalışan, her ajanın kendi "gerçek shell + gerçek tarayıcı" hesaplama ortamı olduğu bulut hizmeti.

## Kanıt
- `gh search repos hyperagent` → resmi ürüne ait depo yok; dönen sonuçlar ilgisiz/üçüncü taraf projeler (facebookresearch/HyperAgents, hyperbrowserai/HyperAgent, FSoft-AI4Code/HyperAgent, weluse/hyperagent).
- `alex-hyperagent/hyperagent-public-skills` (1138 yıldız, lisans yok, son push 2026-06-25) Hyperagent ekibinin ayrı bir GitHub hesabı ama içeriği ürünün marketplace JSON'ları (skill-brand-book-generator.json vb.) — "council of agents" akışıyla ilgisi yok, ürünün kendisi değil.
- Web araması + WebFetch (hyperagent.com, hyperagent.com/marketplace, hyperagent.com/docs): kapalı kaynak hosted SaaS; hesap zorunlu (Log in/Sign up → hyperagent.com/login); örnek işler "8m $6.41" gibi kullanım bazlı ücretlendirme gösteriyor ama açık bir fiyat sayfası yok; self-hosting/indirilebilir paket yok.

## Kurulum
Yok — kurulacak yerel paket/kod yok. Akış: hyperagent.com/login üzerinden hesap açma, ardından web arayüzünden "Council" gibi hazır marketplace ajanlarını çalıştırma.

## İzinler
Sayfalarda ayrıntılı listelenmiyor; üründen çıkarım: hesap/oturum açma, ajanların "gerçek shell + gerçek tarayıcı" ile bulutta kod çalıştırması, isteğe bağlı Slack/Telegram/webhook entegrasyon izinleri. Doğrulanmadı.

## Duman testi
Yapılamadı: kapalı kaynak, indirilebilir/klonlanabilir kod yok; kurulum koşulmadı.

## Geri alma
Belirtilmemiş; resmi kaynaklarda hesap kapatma/uninstall talimatı bulunamadı.

## Köprü izni
yok — kurulacak yürütülebilir kod/CLI yok, köprüye bağlanacak salt-okur alt komut söz konusu değil.

## Önerilen katman
RED — repo yok, lisans yok (kapalı kaynak hosted SaaS), kurulum/izin/kaldırma bilgisi doğrulanamıyor; girdideki "tür: plugin" doğrulanmadı, gerçekte hesap gerektiren bir uygulama/platform.
