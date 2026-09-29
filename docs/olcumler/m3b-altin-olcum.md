# M3b — altın set ölçümü (güncel motor)

| kol | yüksek-önem | genel | dayanmayan (alt–üst) | motor kalem | hafif çağrı | jeton | $ |
|---|---|---|---|---|---|---|---|
| sonnet | %90 (71/79) | %81 (130/160) | %3 (4/127) – %9 (11/127) | 127 | 8 | 174039 | 0.8596 |
| luna | %82 (65/79) | %72 (116/160) | %4 (6/139) – %9 (13/139) | 139 | 6 | 239824 | 0.0425 |
| qwen | %96 (24/25) | %77 (37/48) | %3 (1/32) – %12 (4/32) | 32 | 6 | 124974 | 0.0000 |

## Ölçütler (önceden sabit; sonnet = güncel motor)
- yüksek-önem ≥%90: KALDI (%90 (71/79))
- tüm kalemler ≥%75: GEÇTİ (%81 (130/160))
- dayanmayan ≤%5: alt sınır GEÇTİ (%3 (4/127)) · üst sınır (kare-doğrulanamadı + ölçülemedi dahil) KALDI (%9 (11/127))
- sonuç: motor mükemmel DEĞİL → kaçırma sebepleri M4 düzeltme listesine

## Kategori × önem yakalama (sonnet)
| kategori | önem | yakalama |
|---|---|---|
| Araç/servis/ürün | düşük | %75 (3/4) |
| Araç/servis/ürün | orta | %92 (12/13) |
| Araç/servis/ürün | yüksek | %94 (16/17) |
| Açıklama bağlantıları | düşük | %100 (1/1) |
| Açıklama bağlantıları | orta | %100 (3/3) |
| Açıklama bağlantıları | yüksek | %100 (7/7) |
| Kareden bilgi | düşük | %56 (5/9) |
| Kareden bilgi | orta | %50 (9/18) |
| Kareden bilgi | yüksek | %60 (3/5) |
| Kural/ipucu/iş akışı | düşük | %100 (2/2) |
| Kural/ipucu/iş akışı | orta | %82 (9/11) |
| Kural/ipucu/iş akışı | yüksek | %89 (8/9) |
| Kurulum/komutlar | düşük | %100 (2/2) |
| Kurulum/komutlar | orta | %67 (4/6) |
| Kurulum/komutlar | yüksek | %90 (9/10) |
| Promptlar | yüksek | %100 (6/6) |
| Teknikler | orta | %75 (9/12) |
| Teknikler | yüksek | %88 (22/25) |

## Video yakalama
| video | sonnet | luna | qwen |
|---|---|---|---|
| L9c49WVG_ho | %77 (10/13) | %69 (9/13) | %54 (7/13) |
| kHtOSJRUkLs | %85 (34/40) | %85 (34/40) | %0 (0/0) |
| g89FJiNAlEs | %89 (25/28) | %75 (21/28) | %0 (0/0) |
| 86HM0RUWhCk | %89 (31/35) | %80 (28/35) | %86 (30/35) |
| JfmAm3sxCSc | %68 (30/44) | %55 (24/44) | %0 (0/0) |

## Kaçırma sebepleri (kaçırılan yüksek/orta kalem, sonnet)
- (c) model atladı (girdide + formda yeri vardı): 12 · örn. L9c49WVG_ho · Liste yalnız meşru servisleri içerir · 00:06 kare [tekil] "This list explicitly excludes a
- (a) kaynak motora gitmedi (segment/kare/link girdide yok): 10 · örn. kHtOSJRUkLs · Önbellek slaytı: bozan 7 madde / güvenli 3 madde iki sütun · 06:03 kare "CHANGE IT AND YOU
- (b) formda alan/kategori yok: 3 · örn. g89FJiNAlEs · ponytail plugin kurulumu · 10:37 kare "/plugin marketplace add DietrichGebert/ponytail" + 
- (d) sonraki aşama düşürdü (rapor adayı panel birleşiminde yok): 0

## Ucuz kollar (kural 21 takası: kur.takas)
| kol | yakalama düşüşü | tasarruf ($) | ölçütler | öneri |
|---|---|---|---|---|
| luna | %11 | %95 | KALDI | AL — düşüş ≤%15 & tasarruf ≥%30 |
| qwen | %60 | %100 | GEÇTİ | SOR — düşüş >%20 & tasarruf ≥%50 |

## Altın sete ek aday listesi (K3 'dayanıyor'; altın set ölçüm sırasında değiştirilmedi)
- sonnet · L9c49WVG_ho · [İddialar] Repoda tamamen ücretsiz kullanılabilen yüzlerce farklı API var. · 0:00 · sayısal
- sonnet · L9c49WVG_ho · [İddialar] Üretilen anahtar Claude Code veya Cursor'a verilince ajan tamamen ücretsiz çalışıyor. · 0:17 · özellik
- sonnet · L9c49WVG_ho · [İddialar] Uygulamadaki basit işlemler ücretsiz modelle halledilebilir. · 0:25 · öneri
- sonnet · kHtOSJRUkLs · [İddialar] Kullanım limitinin yalnızca %0,01'i yazılan metinden geliyor. · 0:00 · sayısal
- sonnet · kHtOSJRUkLs · [İddialar] 3.000 tokenlık bir dosya, 40 turluk oturumun 4. turunda okunursa 37 kez daha yeniden ödenir. · 0:58 · sayısal
- sonnet · kHtOSJRUkLs · [İddialar] Harcamasının %96'sı geçmişin yeniden okunmasıydı. · 3:49 · sayısal
- sonnet · kHtOSJRUkLs · [İddialar] Model cache anahtarının parçasıdır. Model değişince cache geçersiz olur. Opus 5'te 200 bin tokenda tur 10 sentten 1 dolara çıkar. · 4:32 · s
- sonnet · kHtOSJRUkLs · [İddialar] Konuşmacı, denetim promptunu her hafta ya da hızlı token yandığında çalıştırmayı öneriyor. · 19:03 · öneri
- sonnet · g89FJiNAlEs · [Adaylar] RTK kuruluyken Claude Code'a git işlemi yaptırıp `rtk gain` ile tasarrufu ölçmek. · yok · prompt · yok · commit the changes and push it onto
- sonnet · g89FJiNAlEs · [Açıklama bağlantıları] https://github.com/Graphify-Labs/graphify — Graphify GitHub reposu · aday: evet (Graphify) · Videoda tanıtılan dördüncü repo.
- sonnet · g89FJiNAlEs · [Açıklama bağlantıları] https://github.com/headroomlabs-ai/headroom — Headroom GitHub reposu · aday: evet (Headroom) · Videoda tanıtılan ikinci repo.
- sonnet · g89FJiNAlEs · [Açıklama bağlantıları] https://github.com/rtk-ai/rtk — RTK GitHub reposu · aday: evet (RTK) · Videoda tanıtılan birinci repo.
- sonnet · g89FJiNAlEs · [Açıklama bağlantıları] https://www.skool.com/erictech/about — Yazarın Skool topluluğu · aday: hayır · Araç değil, ücretli topluluk tanıtımı. · erişilemez: ücretli 
- sonnet · g89FJiNAlEs · [İddialar] RTK, büyük dil modeline giden token tüketimini %60-90 azaltır. · 0:20 · sayısal
- sonnet · g89FJiNAlEs · [İddialar] `git status` çıktısı yaklaşık 600 token iken RTK ile yaklaşık 300 token'a iner. · 0:50 · sayısal
- sonnet · g89FJiNAlEs · [İddialar] Ponytail daha az satır kod üreterek token, para ve inceleme süresinden tasarruf sağlar. · 9:17 · özellik
- sonnet · g89FJiNAlEs · [İddialar] Graphify kod tabanını haritalayarak grep/bash gidiş-gelişini azaltır ve token tasarrufu sağlar. · 12:51 · özellik
- sonnet · 86HM0RUWhCk · [Adaylar] frontend-design skill · yok · skill · yok · Claude'a daha modern, profesyonel, az 'vibe-coded' görünen arayüzler ürettiren skill; küresel ol
- sonnet · 86HM0RUWhCk · [Açıklama bağlantıları] https://get.glaido.com/nate — Glaido (sponsor/affiliate) · aday: hayır · Sponsor bağlantısı; videoda anlatılan bir araç değil.
- sonnet · 86HM0RUWhCk · [Açıklama bağlantıları] https://podcast.nateherk.com/apply — Podcast başvuru sayfası · aday: hayır · Tanıtım/başvuru sayfası, araç değil.
- sonnet · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.hostinger.com/vps/claude-code-hosting — Hostinger VPS Claude Code barındırma · aday: hayır · Sponsor/reklam; videoda geçmiyor.
- sonnet · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.instagram.com/nateherk/ — Instagram profili · aday: hayır · Sosyal medya profili.
- sonnet · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.linkedin.com/in/nateherkelman/ — LinkedIn profili · aday: hayır · Sosyal medya profili.
- sonnet · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.skool.com/ai-automation-society-plus/about?el=building-beautiful-websites-with-claude-code-is&hcategory=youtube-videos&utm_campa
- sonnet · 86HM0RUWhCk · [Açıklama bağlantıları] https://x.com/nateherk — X profili · aday: hayır · Sosyal medya profili.
- sonnet · 86HM0RUWhCk · [Site/UI teknikleri] Butona CSS parlama (glow) efekti · 'Join the community' butonuna parlayan nabız efekti eklendi; localhost'ta görülüp sonra push edildi. · 25
- sonnet · 86HM0RUWhCk · [İddialar] Skill'siz Claude Code siteyi yaklaşık %40, frontend-design skill ile yaklaşık %60 seviyesine getirir (kabaca tahmin). · 8:01 · sayısal
- sonnet · 86HM0RUWhCk · [İddialar] Claude Code için ücretli Pro veya Max hesabı gerekir; ücretsiz planda erişim yoktur. Pro ile başlanması, limite takılınca Max önerilir. · 0:
- sonnet · 86HM0RUWhCk · [İddialar] Claude, skill kütüphanesinde ilgili skill var mı diye bakar; varsa kullanır, yoksa genel bilgiyle yanıtlar. · 4:10 · özellik
- sonnet · 86HM0RUWhCk · [Kareden okunanlar] 0:30: Kare 1: VS Code Welcome ekranı; Recent'te Website Building YT gibi klasörler.
- sonnet · 86HM0RUWhCk · [Kareden okunanlar] 2:25: Kare 3: 'Claude Code Visuals' şeması: CLAUDE.md → System Prompt → Claude Code Agent.
- sonnet · 86HM0RUWhCk · [Kareden okunanlar] 4:10: Kare 5: Skills şeması: Path A skill yükler, Path B genel bilgi.
- sonnet · JfmAm3sxCSc · [Site/UI teknikleri] Scroll ile beliren metin, hover geri itme efekti · Yazılar scroll'da yumuşak gelir; galeri görsellerinde hover'da geriye gitme. · 8:09 · alt
- sonnet · JfmAm3sxCSc · [İddialar] Hero başlığı 187.2px'ten 138.24px'e küçüldü. · 6:37 · sayısal
- luna · L9c49WVG_ho · [İddialar] Kimi, DeepSeek ve Gemini gibi modellere ücretsiz erişim sunulduğu ileri sürülüyor. · 0:00 · özellik
- luna · L9c49WVG_ho · [İddialar] Videoya göre seçilen sağlayıcıdan API anahtarı oluşturup bunu kodlama aracına veya uygulamaya vermek mümkün. · 0:00 · öneri
- luna · L9c49WVG_ho · [İddialar] Yapay zeka ajanının bu yöntemle tamamen ücretsiz çalışabileceği iddia ediliyor. · 0:00 · özellik
- luna · kHtOSJRUkLs · [İddialar] Konuşmacı, kendi kullanımında yazdığı promptların toplam tüketimin yalnızca yüzde 0,01’i olduğunu söylüyor. · 0:00 · sayısal
- luna · kHtOSJRUkLs · [İddialar] Konuşmacı, uzun bir oturumda daha önce okunan dosyaların sonraki turlarda yeniden bağlama eklenebileceğini ve maliyetin bu nedenle birikebil
- luna · kHtOSJRUkLs · [İddialar] Konuşmacı, kendi harcamasının yüzde 96’sının geçmişi yeniden okumaktan kaynaklandığını belirtiyor. · 3:49 · sayısal
- luna · kHtOSJRUkLs · [İddialar] Konuşmacı, örneğin 200.000 token bağlamda bir turun 10 sentten 1 dolara çıkabileceğini; bunu 10 kat artış olarak sunuyor. · 4:32 · sayısal
- luna · kHtOSJRUkLs · [İddialar] Konuşmacı, araç çıktısı filtrelemenin bağlam tüketimini on binlerce tokendan yüzlerce tokene indirebildiğini söylüyor. · 7:20 · sayısal
- luna · kHtOSJRUkLs · [İddialar] Konuşmacıya göre ertelemeli araç yükleme, araçların tüm açıklamalarını baştan yüklemeye kıyasla bağlam maliyetini yüzde 85 azaltıyor. · 8:39
- luna · kHtOSJRUkLs · [İddialar] Konuşmacının aktardığı örnekte bir alt ajan yaklaşık 9.800 token harcarken ana bağlamda 5.700 token tasarruf sağlıyor; toplamda alt ajan kul
- luna · kHtOSJRUkLs · [İddialar] Konuşmacı, alt ajanların ancak yüksek hacimli çıktı, ayrıntılara tekrar ihtiyaç duymama ve ana oturumda çok sayıda tur kalması koşullarında 
- luna · kHtOSJRUkLs · [İddialar] Konuşmacıya göre bir saatten daha seyrek çalışan zamanlanmış görevler, abonelikte önbellek süresi dolduğu için her çalışmada bağlamı tam mal
- luna · kHtOSJRUkLs · [Kareden okunanlar] 0:29: Konuşmacının görüntüsünün üzerinde kırmızı renkte “0.01%” yazısı görülüyor.
- luna · g89FJiNAlEs · [Adaylar] Ajanla değişiklikleri commit edip uzak dala göndermeyi örneklemek. · yok · prompt · yok · Hey, I want you to actually start committing thing
- luna · g89FJiNAlEs · [Açıklama bağlantıları] https://github.com/Graphify-Labs/graphify — Graphify deposu · aday: evet (Graphify) · Videoda kod tabanını bilgi grafiğine dönüştüren araç o
- luna · g89FJiNAlEs · [Açıklama bağlantıları] https://github.com/headroomlabs-ai/headroom — Headroom deposu · aday: evet (Headroom) · Videoda konuşma geçmişini sıkıştıran araç olarak tan
- luna · g89FJiNAlEs · [Açıklama bağlantıları] https://github.com/rtk-ai/rtk — RTK deposu · aday: evet (RTK) · Videoda Bash çıktısını filtreleyen CLI proxy/hook olarak tanıtılıyor.
- luna · g89FJiNAlEs · [Açıklama bağlantıları] https://www.skool.com/erictech/about — Eric Tech Skool topluluğu hakkında sayfası · aday: hayır · Video topluluğu ve canlı oturumları tanıtı
- luna · g89FJiNAlEs · [İddialar] RTK'nin token tüketimini yüzde 60–90 azaltabileceği ileri sürülüyor. · 0:20 · sayısal
- luna · g89FJiNAlEs · [İddialar] Ponytail'in daha az kod satırıyla aynı uygulamayı üreterek çıktı tokenlarını ve kod inceleme yükünü azaltabileceği ileri sürülüyor. · 9:17 ·
- luna · g89FJiNAlEs · [İddialar] Graphify'nin kod tabanını haritalayıp ajanların dosya ve işlevleri daha az arama turuyla bulmasına ve token kullanımını azaltmasına yardımcı
- luna · g89FJiNAlEs · [Kareden okunanlar] 0:50: Claude Code'dan çıkan komutun doğrudan Bash'e gittiği alt yol “~600 tokens”; RTK hook üzerinden Bash'e giden üst yol “~300 tokens” ola
- luna · 86HM0RUWhCk · [Adaylar] Claude Code VS Code uzantısı · yok · plugin · yok · Claude Code’u VS Code içinde kullanmak için uzantıyı yükleme ve hesapla oturum açma akış
- luna · 86HM0RUWhCk · [Adaylar] CLAUDE.md proje yönergeleri · yok · ipucu · yok · Projeye özgü kuralları ve hedefleri kısa bir Markdown dosyasında tutup Claude Code’un çalı
- luna · 86HM0RUWhCk · [Adaylar] Front-end design skill · yok · skill · yok · Ön yüz kodlamadan önce tasarım skill’ini çağırarak daha tutarlı ve özenli arayüzler üretme yakl
- luna · 86HM0RUWhCk · [Adaylar] Referans siteyi klonlama iş akışı · yok · iş akışı · yok · Bir referans sitenin tam sayfa ekran görüntüsünü ve stil bilgilerini Claude Code’
- luna · 86HM0RUWhCk · [Adaylar] Yerelde test edip sonra yayımlama · yok · ipucu · yok · Değişiklikleri önce yerel sürümde kontrol ettirip yalnızca açıkça onaylandıktan sonr
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://get.glaido.com/nate — Video açıklamasında verilen Glaido bağlantısı. · aday: hayır · Videoda bu hizmetin web sitesi geliştirme iş ak
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://podcast.nateherk.com/apply — Podcast başvuru bağlantısı. · aday: hayır · Bir araç veya videoda anlatılan teknik kaynak değil, başvur
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.hostinger.com/vps/claude-code-hosting — Claude Code barındırma konulu Hostinger VPS bağlantısı. · aday: hayır · Açıklamadaki tan
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.instagram.com/nateherk/ — Nate Herk’in Instagram profili. · aday: hayır · Sosyal medya profili; videoda anlatılan bir araç veya 
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.linkedin.com/in/nateherkelman/ — Nate Herk’in LinkedIn profili. · aday: hayır · Sosyal medya profili; videoda anlatılan bir araç
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.skool.com/ai-automation-society-plus/about?el=building-beautiful-websites-with-claude-code-is&hcategory=youtube-videos&utm_campa
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.skool.com/ai-automation-society/about?el=building-beautiful-websites-with-claude-code-is&hcategory=youtube-videos&utm_campaign=f
- luna · 86HM0RUWhCk · [Açıklama bağlantıları] https://x.com/nateherk — Nate Herk’in X profili. · aday: hayır · Sosyal medya profili; videoda anlatılan bir araç veya iş akışı değil.
- luna · 86HM0RUWhCk · [Site/UI teknikleri] VS Code başlangıç ekranı ve klasör açma · VS Code içindeki başlangıç sayfası, dosya açma ve yakın zamanda kullanılan klasörler gösteriliyor.
- luna · 86HM0RUWhCk · [Site/UI teknikleri] Skill seçimi diyagramı · İsteğe uygun skill bulunursa uzman yönergelerinin, bulunmazsa genel bilginin kullanılmasını anlatan görsel. (karede
- luna · 86HM0RUWhCk · [Site/UI teknikleri] Üretilen açılış sayfası · Koyu lacivert zemin, açık mavi vurgular, üst gezinme menüsü ve topluluğa katılma çağrısı içeren sayfa görünümü. (k
- luna · 86HM0RUWhCk · [İddialar] Sunucu tarafı, front-end design skill’in tasarım kalitesini genel kullanıma kıyasla iyileştirdiğini söylüyor; bu değerlendirme videodaki örn
- luna · 86HM0RUWhCk · [İddialar] İlk açılış sayfası üretiminde araç 10 ekran görüntüsü almış. · 8:01 · sayısal
- luna · 86HM0RUWhCk · [İddialar] Sunucu, geçici ekran görüntülerinin site üretiminden çok Claude Code’un incelemesine yaradığını söylüyor. · 13:46 · özellik
- luna · 86HM0RUWhCk · [İddialar] Claude Code için ücretsiz hesap yerine ücretli abonelik gerektiği; Pro ve Max seçeneklerinin kullanılabildiği söyleniyor. · 0:00 · özellik
- luna · 86HM0RUWhCk · [Kareden okunanlar] 0:30: VS Code başlangıç ekranında New File, Open File, Open Folder ve Recent listesi görünüyor.
- luna · 86HM0RUWhCk · [Kareden okunanlar] 2:25: CLAUDE.md proje yönergelerinin sistem promptuna aktarıldığı ve ajanın bunları kullandığı bir diyagram.
- luna · 86HM0RUWhCk · [Kareden okunanlar] 4:10: Diyagram, isteğe uygun skill varsa uzman yanıtı; yoksa genel bilgi yolunu gösteriyor.
- luna · 86HM0RUWhCk · [Kareden okunanlar] 6:12: brand_assets klasöründe AIS Brand Guidelines ve AIS PNG dosyaları, istem alanında landing page talebi var.
- luna · 86HM0RUWhCk · [Kareden okunanlar] 9:23: VS Code proje ağacında temporary screenshots klasörü ve web projesine ait dosyalar listeleniyor.
- luna · JfmAm3sxCSc · [Adaylar] İkinci düzenleme promptu · yok · prompt · yok · Mevcut galeri ve tasarımı bozmadan büyük başlığı küçültme ve kalan metinlere scroll ile yumu
- luna · JfmAm3sxCSc · [Açıklama bağlantıları] https://github.com/YildizDikme/3D-threejs-spiral-gallery — Oluşturulan 3D galeri sitesinin GitHub deposu. · aday: evet (3D-threejs-spiral-ga
- luna · JfmAm3sxCSc · [Site/UI teknikleri] Hover ve yakınlaştırma geçişleri · Görselin üzerine gelince görselin yavaşça geriye gittiği ve geçişlerin yumuşak olduğu belirtiliyor. · 8:0
- luna · JfmAm3sxCSc · [Kareden okunanlar] 6:37: Claude arayüzünde kod/uygulama yanıtı ve sağda site önizlemesi açık; yanıtta değişiklik ve doğrulama maddeleri listelenmiş.
- qwen · 86HM0RUWhCk · [Açıklama bağlantıları] https://get.glaido.com/nate — Sponsor/kısaltma yönlendirme linki (Glaido). · aday: hayır · Üçüncü taraf sponsor linki; videoda demo edilen s
- qwen · 86HM0RUWhCk · [Açıklama bağlantıları] https://podcast.nateherk.com/apply — Podcast başvuru/uygulama sayfası. · aday: hayır · Sunucunun podcast başvuru sayfası; video ile ilgili f
- qwen · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.hostinger.com/vps/claude-code-hosting — Hostinger'in Claude Code hosting tanıtım sayfası. · aday: hayır · Üçüncü taraf hosting t
- qwen · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.instagram.com/nateherk/ — Nate Herk'in Instagram profili. · aday: hayır · Sosyal medya profili; site/landing içerik örneği değil
- qwen · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.linkedin.com/in/nateherkelman/ — Nate Herk'in LinkedIn profili. · aday: hayır · Sosyal medya profili; site/landing içerik örneği
- qwen · 86HM0RUWhCk · [Açıklama bağlantıları] https://www.skool.com/ai-automation-society-plus/about?el=building-beautiful-websites-with-claude-code-is&hcategory=youtube-videos&utm_campa
- qwen · 86HM0RUWhCk · [Açıklama bağlantıları] https://x.com/nateherk — Nate Herk'in X (Twitter) profili. · aday: hayır · Sosyal medya profili; site/landing içerik örneği değil.
- qwen · 86HM0RUWhCk · [İddialar] front-end design skill'i çağrıldığında çıktı, çağrılmadığına göre belirgin şekilde daha modern/profesyonel olur. · 3:40 · karşılaştırma
- qwen · 86HM0RUWhCk · [İddialar] GitHub push + Vercel otomatik deploy ile canlı site anında güncellenir; local değişiklik push'a kadar canlıya yansımaz. · 25:18 · karşılaştı
- qwen · 86HM0RUWhCk · [Kareden okunanlar] 4:10: Skills diyagramı: Step 1 istek → Step 2 skill kontrolü → Path A (YES, expert skill) / Path B (NO, general knowledge); 'Claude Skills e

## Dayanmayan kalemler (sonnet)
- 86HM0RUWhCk · [Site/UI teknikleri] Kayan teknoloji logoları (marquee), animasyonlu arka plan, yüzen logo · Sayfada n8n, Make, Claude, GPT-4o, Zapier, Airtable logoları kayıyor
- 86HM0RUWhCk · [Site/UI teknikleri] 21st.dev hero dalga arka planı · Hero arkasına animasyonlu arka plan eklendi; ilk sürüm bulanık/pikselliydi, başlık okunurluğu, renk ve arka
- JfmAm3sxCSc · [İddialar] Sayfada 23 reveal-text öğesi algılandı. · 6:37 · sayısal
- JfmAm3sxCSc · [İddialar] Konsol hatası yok, canvas 1440x900'de hazır. · 6:37 · özellik

Jev: K2 146/146 durum · K3 {'sonnet': 45, 'luna': 64, 'qwen': 14} · tavan dışı (ölçülemedi) {'sonnet': 0, 'luna': 0, 'qwen': 0} · tavan 300.
Tarama sonucu (video başına): sonnet L9c49WVG_ho tamam · sonnet kHtOSJRUkLs tamam · sonnet g89FJiNAlEs tamam · sonnet 86HM0RUWhCk tamam · sonnet JfmAm3sxCSc tamam · luna L9c49WVG_ho tamam · luna kHtOSJRUkLs tamam · luna g89FJiNAlEs tamam · luna 86HM0RUWhCk tamam · luna JfmAm3sxCSc tamam · qwen L9c49WVG_ho tamam · qwen kHtOSJRUkLs hata · qwen g89FJiNAlEs hata · qwen 86HM0RUWhCk tamam · qwen JfmAm3sxCSc hata
Ölçülemedi (tarama hata/bitmedi, metriğe girmez): qwen kHtOSJRUkLs · qwen g89FJiNAlEs · qwen JfmAm3sxCSc
Not: sonnet m3b-sonnet-uzun 86HM0RUWhCk ilk koşuda tavanla form_red; motorun kuyruk akışındaki gibi bir kez --form-red-yeniden (+1 çağrı) → tamam.
Tarama: sonnet-0 m3b-sonnet-short {'L9c49WVG_ho': 'tamam'} · sonnet-1 m3b-sonnet-uzun {'kHtOSJRUkLs': 'tamam', 'g89FJiNAlEs': 'tamam', '86HM0RUWhCk': 'tamam'} · sonnet-2 m3b-sonnet-uzun-2 {'JfmAm3sxCSc': 'tamam'} · luna-0 m3b-luna-short {'L9c49WVG_ho': 'tamam'} · luna-1 m3b-luna-uzun {'kHtOSJRUkLs': 'tamam', 'g89FJiNAlEs': 'tamam', '86HM0RUWhCk': 'tamam'} · luna-2 m3b-luna-uzun-2 {'JfmAm3sxCSc': 'tamam'} · qwen-0 m3b-qwen-short {'L9c49WVG_ho': 'tamam'} · qwen-1 m3b-qwen-uzun {'kHtOSJRUkLs': 'hata', 'g89FJiNAlEs': 'hata', '86HM0RUWhCk': 'tamam'} · qwen-2 m3b-qwen-uzun-2 {'JfmAm3sxCSc': 'hata'}
Eşleme tabloları: docs/olcumler/m3b-esleme/<id>.md
