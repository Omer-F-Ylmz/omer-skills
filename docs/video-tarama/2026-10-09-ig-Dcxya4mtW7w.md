# Yatırım tavsiyesi değildir: Claude finans sektörünün yarısını bitirdi.
## Künye
Yatırım tavsiyesi değildir: Claude finans sektörünün yarısını bitirdi. · burakcakir.ai · süre: 0:51 · ? · https://www.instagram.com/reel/Dcxya4mtW7w/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-39 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 91837 tk · claude-haiku-5-5: claude-haiku-5-5 · 48700 tk
## Özet
Burak, Anthropic'in yayımladığı finans eklentilerini (anthropics/financial-services) tanıtıyor. Eklentisiz Claude yüzeysel özet verirken eklentilerle analist işi (3 tablolu model, DCF, çarpanlar, hedef fiyat, senaryolar) yapılabiliyor. /morning-note Tesla (TSLA) örneğinde Claude 10-Q, bilanço toplantısı ve haberleri çekip rapor hazırlıyor. Kurulum rehberi yorumla ya da bio linkiyle veriliyor; videoda kurulum komutu gösterilmiyor.
## Bölümler
- 0:00 Giriş: Claude finans sektörünü bitirdi mi?
- 0:04 Anthropic financial-services eklentileri
- 0:12 Sorun: eklentisiz Claude'un yüzeysel cevabı
- 0:16 Analistin teslim ettikleri ve komutlar
- 0:22 Gerçek analistin değerleme adımları
- 0:29 /morning-note Tesla örneği
- 0:33 Orijinal kaynaklardan veri çekme
- 0:40 Çıktılar, veri kaynakları ve kurulum
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| financial-services | yok | plugin | https://github.com/anthropics/financial-services | Anthropic'in finans için hazır eklenti ve ajan deposu (10 eklenti, 49 skill, MIT). | 0:04 | Ekranda github.com/anthropics/financial-services ve eklenti listesi (karede: kanıttan) Ekranda github.com/anthropics/financial-services ve eklenti listesi |
| Claude | yok | CLI | yok | Eklentileri çalıştıran ana yapay zekâ asistanı. | 0:00 | Cloud'da sadece Morning Note yazın |
| Claude Code | yok | CLI | yok | Komutların çalıştığı terminal aracı. | 0:26 | Ekran metni 'Claude Code· Befehle' (karede: kanıttan) Ekran metni 'Claude Code· Befehle' |
| equity-research | yok | plugin | yok | Hisse araştırması eklentisi: morning-note, earnings-preview, thesis, catalysts. | 0:26 | Ekran metni 'equity-research' (karede: kanıttan) Ekran metni 'equity-research' |
| financial-analysis | yok | plugin | yok | Finansal analiz eklentisi: model-update, comps, DCF. | 0:29 | Ekran metni 'financial-analysis' (karede: kanıttan) Ekran metni 'financial-analysis' |
| /morning-note | yok | skill | yok | Hisse için sabah notu/rapor üreten komut. | 0:31 | Ekran metni '/morning-note Tesla (TSLA)' (karede: kanıttan) Ekran metni '/morning-note Tesla (TSLA)' |
| SEC EDGAR | yok | teknik | yok | 10-Q ve resmi bildirimlerin çekildiği kaynak. | 0:33 | Ekran metni 'SEC EDGAR', 'Quartalsbericht 10-Q' (karede: kanıttan) Ekran metni 'SEC EDGAR', 'Quartalsbericht 10-Q' |
| DCF | yok | teknik | yok | WACC ve duyarlılıkla iskontolu nakit akışı değerlemesi. | 0:16 | Ekran metni 'DCF mit WACC und Sensitivität' (karede: kanıttan) Ekran metni 'DCF mit WACC und Sensitivität' |
| FactSet | yok | teknik | yok | Ekranda kaynak olarak listelenen finansal veri servisi; kullanımı gösterilmedi. | 0:40 | FactSet, S&P Capital IQ (karede: Kare gönderilmedi; OCR: 'Quellen' başlığı altında liste.) |
| S&P Capital IQ | yok | teknik | yok | Ekranda kaynak olarak listelenen finansal veri servisi; kullanımı gösterilmedi. | 0:40 | FactSet, S&P Capital IQ (karede: Kare gönderilmedi; OCR: 'Quellen' listesinde 'S&P Capital IQ'.) |
| Moody's | yok | teknik | yok | Ekranda kaynak olarak listelenen finansal veri servisi; kullanımı gösterilmedi. | 0:40 | Moody's. Daloopa, LSEG (karede: Kare gönderilmedi; OCR: 'Quellen' listesinde 'Moody's'.) |
| Daloopa | yok | teknik | yok | Ekranda kaynak olarak listelenen finansal veri servisi; kullanımı gösterilmedi. | 0:40 | Moody's. Daloopa, LSEG (karede: Kare gönderilmedi; OCR: 'Quellen' listesinde 'Daloopa'.) |
| LSEG | yok | teknik | yok | Ekranda kaynak olarak listelenen finansal veri servisi; kullanımı gösterilmedi. | 0:40 | Moody's. Daloopa, LSEG (karede: Kare gönderilmedi; OCR: 'Quellen' listesinde 'LSEG'.) |
| Hisse için sabah notu raporu | yok | prompt | yok | /morning-note komutu ve yanına hisse adı (Tesla, TSLA); çeyrek verisi, bilanço toplantısı ve haberlerden profesyonel rapor üretir. | 0:31 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /morning-note Tesla (TSLA) | Tesla için sabah notu raporu üretir. (karede: Ekranda /morning-note Tesla (TSLA) yazıyor) | 0:31 | kare |
| /catalysts, /comps, /initiate, /thesis, /earnings-preview, /model-update | Eklentilerin diğer komutları; ekranda listelenir. (karede: Ekranda komut listesi görünüyor) | 0:18 | kare |
| /catalysts | Hisse için katalizörleri (fiyatı etkileyebilecek olayları) listeler. (karede: Kare gönderilmedi; OCR: komut listesinde '/catalysts'.) | 0:18 | kare |
| /comps | Peer karşılaştırma tablosu ve çarpanları (multiples) çıkarır. (karede: Kare gönderilmedi; OCR: komut listesinde '/comps'.) | 0:18 | kare |
| /initiate | Hisse için başlangıç kapsam raporu (initiation) üretir. (karede: Kare gönderilmedi; OCR: komut listesinde '/initiate'.) | 0:18 | kare |
| /thesis | Yatırım tezini ve tezi bozacak riskleri yazar. (karede: Kare gönderilmedi; OCR: komut listesinde '/thesis'.) | 0:18 | kare |
| /earnings-preview | Bilanço öncesi önizleme hazırlar (OCR okunuşu: /earnings-previen). (karede: Kare gönderilmedi; OCR: Claude Code · Befehle listesinde komut.) | 0:26 | kare |
| /model-update | Bilanço sonrası finansal modeli günceller ('update nach den Zahlen'). (karede: Kare gönderilmedi; OCR: komut listesinde '/model-update'.) | 0:29 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Eklentiler gerçek bir analistin kurallarını ve süreçlerini yapılandırılmış olarak içeriyor. | 0:19 | özellik |
| Eklentisiz Claude hedef fiyat, senaryo ve model vermiyor; eklentilerle veriyor. | 0:15 | karşılaştırma |
| Kurulum iki komutla yapılıyor. | 0:40 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude | Claude | Cloud az önce finans sektörünün yarısını bitirdi |
| konuşma 0:00 | Anthropic | aday değil: genel kavram | Antropik kısa süre önce finans eklentileri yayınladı |
| kare 0:04 | GitHub deposu | financial-services | github.com/anthropics/financial-services |
| kare 0:26 | Claude Code | Claude Code | Claude Code· Befehle |
| kare 0:26 | equity-research | equity-research | EQUITY RESEARCH |
| kare 0:29 | financial-analysis | financial-analysis | financial-analysis |
| kare 0:31 | /morning-note | /morning-note | /morning-note Tesla (TSLA) |
| kare 0:33 | SEC EDGAR | SEC EDGAR | SEC EDGAR |
| kare 0:16 | DCF | DCF | DCF mit WACC und Sensitivität |
| kare 0:40 | FactSet, S&P Capital IQ, Moody's, Daloopa, LSEG | aday değil: başka adayın parçası (financial-services) | FactSet, S&P Capital IQ; Moody's. Daloopa, LSEG |
| kare 0:16 | 3-statement, çarpanlar | aday değil: genel kavram | EV/EBITDA, KGV, EV/Umsatz |
| konuşma 0:00 | Tesla | aday değil: konu dışı | Örneğin Tesla |
## Kareden okunanlar
- 0:04: anthropics/financial-services Public; 10 plugin, 49 skill, MIT; eklenti listesi
- 0:23: Değerleme adımları: Zahlen holen, Normalisieren, Treiber setzen, Bewerten, Urteil
- 0:33: Quartalsbericht 10-Q ve Bilanzkonferenz transkripti kartları
## Belirsizlikler
- Kurulum komutları videoda gösterilmiyor; 'iki komut' dendi ama metni yok.
- Yorumlar girişsiz alınamadı.
- Veri sağlayıcılar (FactSet, S&P Capital IQ, Moody's, Daloopa, LSEG) yalnızca 0:40 listesinde, kullanıldığı gösterilmedi.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/anthropics/financial-services | 0:04 | ekran | evet |
## İş akışı
- 1. adım — Eklenti deposunu tanıtma — araçlar: GitHub, financial-services
- 2. adım — Eklentisiz Claude'un yüzeysel cevabını gösterme — araçlar: Claude
- 3. adım — Analist çıktılarını ve komutları sıralama — araçlar: equity-research, financial-analysis
- 4. adım — /morning-note Tesla (TSLA) çalıştırma — araçlar: Claude Code, /morning-note
- 5. adım — 10-Q ve bilanço transkriptini çekme — araçlar: SEC EDGAR
- 6. adım — Rapor ve çıktıları sunma — araçlar: Claude Code
## Promptlar
- Hisse için sabah notu raporu — /morning-note komutu ve yanına hisse adı (Tesla, TSLA); çeyrek verisi, bilanço toplantısı ve haberlerden profesyonel rapor üretir.
