# pln — 26 benzersiz kayıt

**Amaç:** Planlama ajanları: belirsiz isteği kabul ölçütüne çevirme, PRD/teknik spec, mimari ve sistem tasarımı, görev bölme, kapsam kesme, tahmin, risk ve karar kaydı, legacy göç planı.

**İç yapı:** Tümü [ajan], pln-<konu>; akış: niyet/fikir → gereksinim (prd, kabul, nfr, kullanım senaryosu) → tasarım (mimari, sistem, spec) → bölme/öncelik/tahmin → kayıt (adr, risk).

## En güçlü parçalar
- `pln-niyet-netlestirme` — En az soruyla belirsiz isteği net kabul ölçütüne çevirir.
- `pln-kapsam-kesici` — Planı değer/efor sıralamasıyla en küçük yayınlanabilir dilime (MVP) indirir.
- `pln-dalga-plani` — Dokunulacak dosyalar ve adım başına doğrulamayla adım adım uygulama planı.
- `pln-kabul-olcutleri` — Bitiş ölçütü olmayan hikâyelere test edilebilir given/when/then.
- `pln-islevsel-olmayan-gereksinim` — Belirsiz kalite isteklerini yüzdelik ve hedeflerle ölçülebilir NFR'ye çevirir.
- `pln-bogucu-incir-gocu` — Yönlendirme cephesi ve eşlik kontrolleriyle big bang'siz legacy değiştirme.
- `pln-tahmin-araligi` — Üç noktalı aralık, referans sınıfı ve risk tamponuyla tahmin.
- `pln-karar-kaydi` — Bağlam, seçim ve gerekçeyle tek kısa ADR girdisi.
- `pln-teknik-spec` — Uygulamadan önce arayüz, uç durum ve açık sorular.

## Birlikte kullanım
- pln-niyet-netlestirme → pln-prd-yazar → pln-kabul-olcutleri → pln-dalga-plani.
- pln-gorev-bolme + pln-bagimlilik-haritasi: kritik yol ve paralel iş.
- pln-mimari-plan + pln-karar-kaydi + pln-risk-kaydi.
- omer-skills departman-surec-plan bu ajanların sırasını belirler.

## Tuzaklar
- pln-mimari-plan ile pln-sistem-tasarimi, pln-gorev-bolme ile pln-sprint-hikaye örtüşür.
- pln-sparc-asama kendi aşama kapılarını dayatır; başka plan akışıyla çakışabilir.
- pln-proje-iskelet kod/CI üretir; plan değil yapım işidir.

## Üyeler
- ajan (26): pln-bagimlilik-haritasi, pln-bogucu-incir-gocu, pln-dalga-plani, pln-fikir-olgunlastir, pln-gorev-bolme, pln-hedef-planlayici, pln-islevsel-olmayan-gereksinim, pln-kabul-olcutleri, pln-kapsam-kesici, pln-karar-kaydi, pln-kullanim-senaryosu, pln-mimari-plan, pln-niyet-netlestirme, pln-ozellik-onceliklendirme, pln-prd-yazar, pln-proje-iskelet, pln-proje-yonetimi, pln-risk-kaydi, pln-sistem-tasarimi, pln-sokulebilir-entegrasyon, pln-sozde-kod-algoritma, pln-sparc-asama, pln-sprint-hikaye, pln-tahmin-araligi, pln-teknik-spec, pln-temiz-mimari-sinir
