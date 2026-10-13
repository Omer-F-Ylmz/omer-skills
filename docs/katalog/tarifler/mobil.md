# Mobil uygulama — birleşim tarifi
Ne zaman: React Native/Expo ile iOS/Android uygulaması geliştirme ve mağaza yayını.

## Fazlar
1. Keşif ve plan: `ecc:react-native-patterns` — RN/Expo ekran, bileşen, gezinme, veri katmanı · birlikte: `expo` (MCP) Expo derleme ve dokümanına bağlanır.
2. Arayüz: `expo:expo-native-ui` — Apple HIG, yerel kontroller, duyarlı yerleşim · birlikte: `expo:expo-router` dosya tabanlı rota ve gezinme.
3. Veri ve izinler: `expo:expo-data-fetching` — ağ isteği, önbellek, çevrimdışı · birlikte: `mob-calisma-izni` kamera/konum/bildirim izinleri; push için `mob-push-bildirim` (APNs/FCM).
4. Test ve dahili dağıtım: `expo:expo-dev-client` — geliştirme istemcisini yerelde ya da TestFlight ile dağıtır · birlikte: takılma için `mob-rn-performans`.
5. İzleme: `sentry-react-native-sdk` — hata izleme, tracing, oturum.
6. Yayın: `expo:eas-app-stores` — eas.json, imzalama, sürüm, mağaza gönderimi · birlikte: `engineering-mobile-release-engineer` kademeli yayın; mağaza görselleri `app-store-screenshots`.

## İnceleme ajanları
- `mob-rn-performans`: liste sanallaştırma, Hermes, yeniden çizim.
- `mob-uygulama-boyutu`: indirme boyutunu küçültür.
- `superpowers:requesting-code-review`: birleştirme öncesi.

## Güvenlik ve kalite kapıları
- İzin reddi yolları test edildi (`mob-calisma-izni`).
- Derin bağlantılar uygulamayı açıyor: `mob-derin-baglanti`.
- API anahtarı depoda değil: `gitleaks`; statik analiz `semgrep`.
- Kişisel veri: `sec-kvkk-gdpr-kontrol`.

## Tartışma konseyi
- Karar: Expo yönetilen akış mı native modül mü, yayın kanalı.
- `ecc:council` — varsayılan Claude personaları: mobil geliştirici, ürün, yayın mühendisi.

## Jeton bütçesi
- Plan: küçük (~8k, tahmini). Arayüz: büyük (~35k). Veri/izin: orta (~15k). Test: orta (~12k); derleme logu `okuyucu` alt ajanına. İzleme: küçük (~5k). Yayın: orta (~10k). Hepsi tahmini.

## Kaçınılacaklar
- `gstack-ios-clean` ve diğer gstack iOS skill'leri macOS ve xcrun ister; Windows'ta koşmaz.
- `expo:eas-hosting`'i yerel derleme için kullanmak; web/API içindir.
- `expo-mobil-paket` ile tekil expo skill'lerini aynı anda yüklemek.

## Aday (kurulu değil)
yok
