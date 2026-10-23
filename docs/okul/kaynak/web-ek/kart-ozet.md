# Site incelemesi — ana liste

**Amaç.** Ömer'in kuralı: videolarda gösterilen, etkileyici frontend arayüzlü referans sitelerin kodu, yapısı ve promptları incelenir; oradan **teknik** çıkarılır ve yapacağımız sitelerde kullanılır. Birebir klon yok; izinsiz varlık (görsel, font, metin, logo, kod) kullanımı yok. Öğrenilen şey teknik/desen olarak yeniden yazılır.

**Bu klasör:** yalnız ana liste (`liste.tsv`). İnceleme sonraki ajanlarda yapılır.

**Sınıflar / öncelik:** V tasarım vitrini, ilham galerisi, etkileyici arayüzlü site (1) · K UI kütüphanesi, bileşen, animasyon dokümanı (2) · A araç/SaaS ürün sitesi (3) · B bilgi/makale/rapor (4). Sıra: sınıf, sonra video sayısı.

**Kaynaklar:** `docs/kurulumlar/tur3..5b-sonuc*.tsv` (AYRI-UYGULAMA web satırları), `kacan-adaylar.md` site/ürün satırları, `docs/video-tarama/*.md` raporları (tasarım bağlamlı alan adları). Kurulu araçlar (impeccable, taste-skill) hariç tutuldu.

**Sınırlar:** V/K/A/B ataması alan adı listesinden elle yapıldı; A sınıfındaki satırların çoğu tur sonuçlarından gelen varsayılan sınıftır, incelemede yeniden sınıflanabilir. Ağ isteği yapılmadı, bu yüzden sitelerin canlı olup olmadığı doğrulanmadı. "Neden ilginç" sınıf düzeyinde genel bir gerekçedir.

**Sayılar:** toplam 283 · V 97 · K 31 · A 148 · B 7
## 21st.dev.md
---
site: https://21st.dev
tur: component/animasyon kutuphanesi
kaynak: icerik+teknik
kart-modeli: mistral/ministral-8b-latest
dogrulama: dogrulandi (kanitli=2 kanitsiz=2 hakem=nvidia/nvidia/nemotron-3-ultra-550b-a55b)
---
# 21st.dev


- **Ne sunuyor**: Kopyalanabilir React bileşenleri, animasyonlu UI sablonları, temalar, yapay zeka promptları ve tasarım mühendisleri tarafından hazırlanmış şeffaf UI öğeleri (hero, input, card vs.).
- **Ücretsiz kısım**: Temel bileşenler, temalar ve promptlar ücretsiz erişimle kullanılır; fiyatlandırma sayfasından premium özellikler ayrı.
- **İndirilebilir kaynak**: GitHub depoları yok (kanıt: `github: []`), ancak kod örneği ve bileşenler doğrudan site üzerinden kopyalanabilir. ⚠[kanitsiz]
- **Teknoloji**: React temelli (kanıt: `lib: {"react": false}` yanlış, ancak site UI ve örnekler React ile uyumlu; `framer`, `gsap` gibi animasyon kütüphaneleri desteklenebilir). ⚠[kanitsiz]
- **Bizde kullanım**: Frontend geliştiriciler için UI/UX hızlandırma, tasarım mühendisleri için hazır şablonlar, AI agentleriyle entegrasyon (promptlar).


Tur: [[Siteler/component-animasyon kutuphanesi]]

## REA teknik (inspect_web_page, 23 Eki 2026)
- DOM 2259 dugum, 61 script, canvas=0
- Algilanan altyapi: next
- Kanit: docs/site-inceleme/rea/21st.dev.json
## 60fps.design.md
---
site: https://60fps.design
tur: ilham galerisi
kaynak: icerik+teknik
kart-modeli: mistral/ministral-8b-latest
dogrulama: dogrulandi (kanitli=1 kanitsiz=2 hakem=nvidia/nvidia/nemotron-3-ultra-550b-a55b)
---
# 60fps.design


- **Ne sunuyor**
  UI/UX animasyon örnekleri galerisi (mobil/web). 60fps tarafından hazırlanan interaktif detaylar, 3D animasyonlar, kullanıcı etkileşimleri ve iş akışları.

- **Ücretsiz kısım**
  Örnekler izleme (filtreleme, arama, kategorilerle sınırlı). Ücretsiz kullanım şartları: [lisans](https://60fps.design/terms).

- **İndirilebilir kaynak/kod**
  **Yok**. Örnekler görsel/etkileşimsel olarak sunulur; kod indirilemez (Framer.js kullanılıyor).

- **Teknoloji**
  - **Ana platform**: Framer (interaktif demo). ⚠[kanitsiz]
  - **Kütüphaneler**: GSAP (animasyon), Three.js (3D). ⚠[kanitsiz]
  - **İçerik**: 2110+ UI detayı, 93 site örnekleri, 83 motion snippet.

- **Bizde kullanım**
  - **Skill**: UI/UX animasyon tasarımcılar, front-end geliştiriciler (Framer/GSAP).
  - **İş**: Mobil/web UI prototipleri, interaktif detaylar, 3D etkileşimler.


Tur: [[Siteler/ilham galerisi]]

## REA teknik (inspect_web_page, 23 Eki 2026)
- DOM 7507 dugum, 12 script, canvas=0
- Algilanan altyapi: belirgin kutuphane yok (paketlenmis/ozel)
- Kanit: docs/site-inceleme/rea/60fps.design.json
