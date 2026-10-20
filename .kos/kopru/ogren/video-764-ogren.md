# VIDEO-764 ÖĞREN özeti (karar-v2 ÖĞREN gerekçelerinden; kurulum yok, ÖĞREN 2. turun girdisi)

## Bağlam yönetimi ve hafıza
- CLAUDE.md'yi şişirme, nadir adımları skill'e böl; /init, ~200 satır sınırı, içe aktarma (ig-DeeFTVpCS8L, ig-DeptwfDkdN3)
- Yeni modele göre CLAUDE.md sadeleştirme / prompt-audit (ig-DeHkZbfSi-D)
- Context rot için handoff.md + /clear; prompt cache süresi, /compact, /context kullanımı (ig-DeRgZlhJngj, ig-DepyR86P1ml)
- CLAUDE.md, compaction, subagent ve memory karşılaştırması (ig-DeBl1GmsVLJ)
- Obsidian vault ile hafıza: raw/wiki/output yapısı, proje başına 4 dosyalık desen, klasör haritası, ikinci beyin (ig-DeXye75gGlo, ig-DYYaA1LKtoO, ig-DZ75f-Upik9, ig-DdO9AXNgVz-)
- Marka sesi/audience/business dosyalarıyla bağlam kurma; Claude Projects ile marka DNA'sı (ig-DenWTNwIG50, ig-DeMbHNWErWX)
- Bağlamı MCP sunucusunda tutma, kod tabanını bilgi grafiğine çevirme ile token tasarrufu (ig-DXt9VG5DwNV, ig-DaqFZGMIw_N)
- Araçlar arası ortak hafıza, paylaşılan canlı bilgi tabanı, ajanlar arası iş devri (ig-DdQ72JnIaIy, ig-DdRCQVVSIHT)
- Oturumlar arası self-healing /dream skill fikri (ig-DbS8PgjEsVm)

## Talimat dosyası kuralları (CLAUDE.md / agents.md)
- Yapmama kurallarına dayalı talimat dosyası: basit çözüm, bağımlılıkları koru, dokümana bak, aşırı mühendislikten kaçın, varsayım yapma, doğrula (F86ovkAsu0I, fSrZfx32-nw, ig-Dc84Z0-iY5s)
- Sızdırılan sistem prompt'ları ve prompt derlemelerinden araç kullanımı/güvenlik kuralı öğrenme (AHqd07eSfX8, ig-Dei2Xs-k6hk)
- Aşırı mühendisliği azaltan eklentilerin eleştirel testi (ig-DenU5zmu20l)
- Claude Code için kısa prompt ifadeleri: sub-agents, "interview me", verify (ig-Dd9L7YVgpKs, ig-Dee3AxgN_th)
- Prompt kütüphanesi, Plan Mode, slash komutları pratikleri (ig-DefRPnlkU6x)

## Skill yazımı ve organizasyonu
- SKILL.md boyutu, hook kullanımı, referans dosyalara içindekiler tablosu (ig-Def1nTHD0aW, ig-DePMsSOxhFs)
- Claude'un yerleşik skill-builder özelliği; sohbet geçmişinden skill üretme; ekran kaydından skill üretme (ig-DefQYOsNuan, ig-Deh3cvbxFnv, yVQ4g0ueKzg)
- Sohbet geçmişinden otomasyon adayı bulma (ig-DejukzmtsEz)
- Skill'leri role göre organize etme ve birleştirme (ig-DeDszy_stV9, ig-DenIklFh8TC, ig-DerbZP1jRsN)
- Rol bazlı plugin/skill paketleri ve resmi skill depoları karşılaştırması (ig-Dd1LC_5jPfM, ig-Dep3eEgmIVe, ig-DeHUaCoPFTV, ig-DeqGkciIB21, ig-DepR08lCqU8)
- Marka DNA'sı çıkaran ve görsel üreten skill akışı (ig-Deb6a1su1Pz, ig-Debhj5guuoI)
- Büyük skill/ajan koleksiyonlarını mevcut yapıyla karşılaştırma (ig-Dar76wns2Iv, ig-Dci2tkEsmrJ, ig-DekAh-5oM_m, ig-DeCSMxroRMi, ig-DZDUd0kS7lw)

## Ajan mimarisi ve orkestrasyon
- Agentic döngü: hedef ver, araç kullan, doğrula-düzelt (ig-Dd6JvVin1Gz)
- Agentic engineering akışı: grill me, spec, ticket, build, review (ig-DdFQ-K0AJ0b)
- Koordinatör ajan, ortak hafıza, Telegram ile çok ajanlı yapı; çok ajanlı ofis/ajans/council desenleri (ig-DeelntGS8Ku, ig-DeV1fyFiA8A, ig-Dec9HN_Pzj8, ig-DeryUtBOY7R)
- Claude Projects: paralel thread, koordinatör, paylaşılan bellek; çoklu oturum yönetimi ve oturum devri (ig-DeenuUwM0Zx, ig-DehEgnEAaPn, ig-DeVf6OdDHUW, ig-DeXa0zYt80y)
- Merkezi yönerge + skill + doğrulayıcı ajan kurulumu (ig-Dd8wJp4SIhM)
- Alt ajan yönlendirme kuralını CLAUDE.md'ye yazma; ajan uzmanlaştırma (ig-DdzDB3Jq6K9, ig-DeqnjjQI-Oc, ig-DegoA6qhiPi)
- Onay panelli otomasyon deseni; zamanlı rakip takip ajanı (ig-DeToMLxtdSV, ig-DeSS3EIDQYq, ig-DeZ6LQmCvsm)
- Web sitelerini ajan API'sine çevirme; uygulamaya ajan butonu; tarayıcı otomasyonu (ig-DecRLzKj1pj, ig-DekBuQpgVDG, ig-DXkUQQqCRxS)
- Ajan/Claude Certified Architect müfredatı, ajan sertifika yol haritası (ig-DYjnDAADBo3, ig-DeQa-mgjwEK)

## Model yönlendirme ve maliyet
- Basit işleri Haiku'ya, zor işleri Opus'a yönlendirme; CLAUDE.md ile model seçimi (ig-DefOjSZgifD, ig-DegASWXxIDY, ig-DesB8QSAfV9, ig-DecuVEOlAx_)
- Görev zorluğuna göre model ve çaba seçen router, maliyet karşılaştırması (ig-DeHdXeWsgph)
- Model cascade: ucuzdan başla, güven düşükse yükselt (ig-DdjUihCs77b)
- Claude Code "mods": oturumlar arası iletişim, panel, ucuz modele yönlendirme (ig-Dee9GkoRqKM, ig-DeeA90AASHf, ig-DeeUZo9TMAa, ig-DeohAJhNMw1)
- Claude Code'u ücretsiz/alternatif modellere yönlendiren router fikri ve kısıtları (1YLwZQAfzjE, ig-Ddw8JXnM3g0, ig-Dertf_QNKyu, ig-DZdZtEhMvgX)
- Token tasarrufu komut ve pratikleri (ig-DenHUw1CiQy, ig-DehcRpWkhTu)

## Ajan doğrulama ve kendini geliştirme
- Ajanın kendi prompt/skill değişikliklerini doğrulaması; Harness² (harness katmanlarını optimize etme) (ig-DeobIAIkRfV, ig-DeoQ9gtAn2N)
- Dene-puanla-iyileştir döngüsü, kontrolcü puanı (ig-Deq4x0pDurV)
- Backtest veri sızıntısı dersi, veri birleştirme ve back-test (ig-Dd8zpBVEinT, ig-DeHGRXvg6Xm)
- Claude ile hata ayıklama pratiği (ig-DefL97Uupu6)
- Yayın öncesi kontrol listesi (20 madde) ve SEO kontrol listesi (ig-DeZ4dMPBi3F, ig-Dbje8dMhOkJ)
- Aşamalı çalışma ve doğrulama ile site geliştirme (ig-Ddx3MdJRLd5)
- Uygulama davranışını kaynak kodsuz inceleme (ig-DeoTZa6IusJ)

## Ticaret / finans ajanı desenleri
- LLM'i emir yolundan ayırma, güven eşiği, benchmark fallback (ig-DcD1vwCtGGX)
- Veri akışı + Kelly + işlem mimarisi; risk kontrolü (ig-Dd5_1SBPda_, ig-DeqrGwHAfoN)
- Blok başı karar/simülasyon deseni (ig-Ddja2_uDxqr)
- Claude'u harici veri/işlem servislerine bağlama, MCP/çoklu ajan desenleri (ig-Dd4Ca8oiiyB, ig-DdEv5OwBZ6f, ig-DdNjyfNyx2e, ig-DzGPvzIN4C, ig-DeAYuSDIweJ, ig-Dejzt54pZ0A)

## Web/UI üretimi ve tasarım iş akışı
- Hazır prompt kütüphanesini kod editörüne yapıştırarak site üretme (ig-DcRkjmRjKO6, ig-DectyxhCV8I, ig-DemfQBUDDv9, ig-DefSnrOgeFc)
- UI bileşen adlarını bilip prompt'ta kullanma (ig-Dbu-pe6IOHa)
- design.md / DESIGN.md ile marka tasarım sistemi besleme (ig-DebPmJFgIbs, ig-DemwcsvI1kW, ig-DbZrFEQTouG)
- 6 adımlı site yapım promptu; hedef-tasarım-kodlama-test akışı (ig-DeuD6IVEYOa, ig-DbLgANVRgZ_)
- Bileşen MCP'siyle UI üretme; şablonla başlama (ig-DeesHfYAZfN, ig-DekoCYllGp7)
- Site klonlama iş akışı, ekran görüntüsünden koda dönüşüm (ig-DaA2s3vo_7k, ig-Deec1cgindT)
- Avatar repo + prompt ile UI örneği; Canva'dan Claude ile prototip (ig-Dc5YDjKI9ta, ig-DenPR0tPbxi)
- Tasarım ilham/referans kütüphanelerini skill çıktısına referans yapma (ig-DepbQHOInrG, ig-DeFLfJco13J, ig-DeIFnLIiFhm)

## 3D, animasyon ve video teknikleri
- Kare dizisiyle scroll animasyonu; Flow/EasyGIF akışı (ig-DasLm6opzIO, ig-DdyqkyqvuUM)
- Three.js + GSAP ile 3D kaydırmalı site; GSAP snap scroll + CLAUDE.md pratiği (ig-DaiJw_5h8Gf, ig-DXvgZqaNXvp, ig-DelsVQJR6ZE, ig-DemSGaSObxw)
- Opus ile tek prompt'tan açıklayıcı animasyon; Claude Motion beta (ig-Ded-wGdmOio, ig-Deg6MtVCcYk, ig-DeQ6wBIh7Zc)
- Kodla video üretimi, ajan tabanlı uçtan uca video hattı, transkriptten otomatik montaj (ig-DeD1binjWea, ig-DePnhO5Ran0, ig-DejoN2ZBZmT)
- Video karelerini yerelde çıkarıp Claude'a gösterme / video görme (ig-Da1vl5dtj1q, ig-Deey9KZEYG8)
- Claude'u Unreal Engine/Blender'a bağlama (ig-DehO5O3kXA1)

## İçerik, SEO ve otomasyon iş akışları
- llms.txt ve schema.org pratiği (ig-DdN0DWaRFUY)
- SEO için çok ajanlı otomasyon akışı (ig-Dd_cB-QThC_)
- Claude Code ile sosyal medya/içerik hattı, veri odaklı içerik akışı (ig-DdscwJUROKo, ig-DeSW9GFBQvF, ig-DeSYR9fxKbV)
- Ajanın reel izleyip uyarlaması (ig-Dd8v6ygNZeI)
- Hazır araçları birleştirip otomasyon hizmeti satma (ig-DcSzjwxh9N_, ig-Dd7pn4nSh2t)

## Model/ML teknikleri
- Kimi K3: CPU'da SSD'den uzman yükleme tekniği (ig-DcjlgleALHo)
- bitnet.cpp ile CPU'da yerel LLM çıkarımı (ig-DeWlTIZGdZF)
- Sıfırdan GPT eğitimi; özel LLM oluşturma; yerel model eğitimi (ig-DdlyT_dIiT7, ig-DeFu5m4PCkq, ig-DepJQ7bDrhw)
- Kalibre sınıflandırma modeli (nVNQUzpw3Nw)
- System Design Primer ile sistem tasarımı öğrenme (ig-DcDfnzsM2wL)
