# expo-plugins — 26 benzersiz kayıt

**Amaç:** Resmi Expo skill'leri: Expo/React Native uygulama kurma, yönlendirme, native UI, EAS derleme/güncelleme/mağaza gönderimi, yükseltme ve web'den native'e taşıma.

**İç yapı:** expo [plugin] + expo [mcp] (mcp.expo.dev) ve expo:<konu> alt skill'leri; expo-* geliştirme, eas-* bulut hizmetleri; expo:expo-overview yönlendirici giriş noktası.

## En güçlü parçalar
- `expo:expo-overview` — Her Expo/EAS işinde kod yazmadan ve başka skill seçmeden önce yüklenen yönlendirici.
- `expo:eas-app-stores` — eas.json, imzalama, sürüm/build numarası ve mağaza gönderimi.
- `expo:eas-update` — OTA güncelleme kurulumu ve preview/staging/production kanallarına yayın.
- `expo:expo-router` — Dosya tabanlı rota, grup, dinamik rota ve Link ile navigasyon.
- `expo:expo-ui` — @expo/ui ile iOS'ta gerçek SwiftUI, Android'de Jetpack Compose.
- `expo:expo-upgrade` — Expo SDK sürüm yükseltme ve bağımlılık sorunları.
- `expo:expo-data-fetching` — Her ağ isteği/API çağrısında fetch, React Query, SWR.
- `expo:expo-web-to-native` — Web sitesini mobil uygulamaya çevirme, Next.js/Vite/CRA'yı React Native'e taşıma.
- `expo:eas-workflows` — Expo projeleri için EAS workflow YAML ile CI/CD.

## Birlikte kullanım
- expo:expo-overview → expo:expo-project-structure → expo:expo-router.
- expo:expo-dev-client → expo:eas-app-stores → expo:eas-update → expo:eas-update-insights.
- expo:expo-native-ui + expo:expo-ui + expo:expo-animation: native his ve hareket.
- yerel-diger'deki animate-expo ile expo:expo-animation aynı açıklamayı paylaşır.

## Tuzaklar
- animate-expo (yerel-diger) ile expo:expo-animation çakışan kopya.
- EAS hizmetleri (simulator, hosting, observe, update) Expo hesabı ister; ücret koşulu katalog metninde belirtilmemiş.
- expo-module mevcut Swift modülünü göç ettirmek için değil; remotion gibi port işleri ayrı skill'de.
- expo [mcp] web app için değil.

## Üyeler
- mcp (1): expo
- plugin (1): expo
- skill (24): expo:eas-app-stores, expo:eas-hosting, expo:eas-observe, expo:eas-simulator, expo:eas-update, expo:eas-update-insights, expo:eas-workflows, expo:expo-animation, expo:expo-app-clip, expo:expo-brownfield, expo:expo-data-fetching, expo:expo-design-system, expo:expo-dev-client, expo:expo-dom, expo:expo-examples, expo:expo-module, expo:expo-native-ui, expo:expo-overview, expo:expo-project-structure, expo:expo-router, expo:expo-skill-feedback, expo:expo-ui, expo:expo-upgrade, expo:expo-web-to-native
