Sen YAZARSIN (ÖĞREN-3 ajan-orkestrasyon). Girdi: C:\Projeler\omer-skills\.claude\ogren3\o3-paket-{P}.md — her kalem `## <ad>` ile başlar: çözülmüş kaynak dosyası, satır sayısı, aracın adları, başlıklar. Taslak YOK: her kalemin alanlarını kaynaktan sen yazarsın.

Her kalemde `kaynak` dosyasının TAMAMINI Read ile ≤200 satırlık parçalarla (offset/limit) baştan sona oku; 300 satırı aşan dosyanın offset/limit'siz Read'i kancayla reddedilir. Bu dosya çözülmüş metindir: kanca kalemi (ad `Olay:eşleyici`) için kalemin kendi kayıt girdisi + çağırdığı betiklerin tam metni; repo/eklenti için kök README + package.json/pyproject/plugin.json; CLI için --help çıktısı. Alıntılar BU dosyadan birebir olmalı.

d2: 1000+ satırlık kaynak da (ecc, OmniRoute, office-hours…) ≤200 satırlık parçalarla SONUNA KADAR okunur; atlamak sapmadır. Kategorisi araştırma/bilim/diğer olan kalemde orkestrasyon rolü yoksa "orkestrasyon-dışı" doğru seçimdir.

Alanlar (Türkçe, ≤2 cümle; alıntılar özgün dilde):
- ne_yapar: aracın kaynakta anlatılan işi; uydurma/çelişen parça yok.
- komut: kaynakta BİREBİR geçen, bu aracın KENDİ komutu/çağrısı (kopyala; kendi ifadenle/birleştirerek/açıklama ekleyerek YAZMA). Kanca kaydının KENDİ command satırı (ya da ≥8 karakterlik birebir parçası: betik yolu) o kancanın komutudur. Ürünün kendi komut şablonu komuttur. Araç adının yalnız başka bir komutun ARGÜMANI olarak geçmesi sahiplik DEĞİLDİR. Kaynakta gerçekten yoksa "belirsiz — <gerekçe>".
- sinirlar: kaynaktaki önemli uyarı/gereksinim/sınır; kapsam/koşul dalını BİREBİR koru; kaynakta uyarı varken "belirsiz" yazma; uydurma yok. Gerçekten yoksa "belirsiz — <gerekçe>".
- ne_zaman: kaynağın kendi tetik/kullanım koşulu ("Use when…", description) Türkçe ≤1 cümle; kaynakta yoksa "belirsiz". (alıntısız; sert denetime girmez)
- rol: aracın orkestrasyondaki ASIL işi, 1-2 değer YALNIZ şu listeden: orkestrasyon | delegasyon | paralel dağıtım | planlama | zamanlama | izleme | bellek | yönlendirme | koruma | model sağlayıcı | ajan tanımı | inceleme | orkestrasyon-dışı. Tanımlar: orkestrasyon=çok adımlı akışı/ajanları uçtan uca yürütür; delegasyon=işi bir alt ajana/başka sürece/modele verir; paralel dağıtım=bağımsız işleri aynı anda birden çok ajana dağıtır; planlama=plan/görev listesi/spec üretir; zamanlama=kuyruk, zamanlı/tekrarlı/arka plan iş, bekleme; izleme=durum/ilerleme/maliyet/log izler-raporlar; bellek=oturumlar arası bilgi/devir/süreklilik saklar; yönlendirme=işi hangi ajan/model/skill'in yapacağını seçer; koruma=kanca/guard ile aracı/eylemi engeller-denetler; model sağlayıcı=model/LLM erişimi, proxy, combo sunar; ajan tanımı=belirli bir uzman rolün/personanın kendisi (alt ajan tanımı); inceleme=çıktıyı denetler/puanlar/doğrular (hakem, review); orkestrasyon-dışı=aracın işi ajan/araç yönetimiyle ilgili değil (kategori hatası). Birden çok uyuyorsa ASIL işi anlatanları seç.
- alinti (ne_yapar/komut/sinirlar için) ve kanit (rol için): kaynaktan BİREBİR kopya, 15-200 karakter, TEK satırın içinden, satır no'suz. "belirsiz" alanda alıntı = ilgili bölümün birebir başlık satırı (yoksa "").
- KAYNAKSIZ kalem (boş dosya ya da <3 anlamlı satır): ne_yapar/komut/sinirlar HEPSİ tam "kaynak yetersiz", rol ["orkestrasyon-dışı"] değil — rol yine listeden en olası, kanit "".

Çıktı: C:\Projeler\omer-skills\.claude\ogren3\o3-yazar-{P}.jsonl — kalem başına TEK JSON satırı (ad `## ` sonrası birebir):
{"ad":"…","ne_yapar":{"deger":"…","alinti":"…"},"komut":{"deger":"…","alinti":"…"},"sinirlar":{"deger":"…","alinti":"…"},"ne_zaman":"…","rol":["…"],"kanit":"…"}
Write ile yaz (JSON kaçışlarına dikkat; ters eğik çizgi \\ olarak). Sonra `cd C:/Projeler/omer-skills && python -X utf8 .claude/ogren3/o3.py birlestir 2>&1 | grep -v "yazar satırı yok"` koş (diğer partilerin RET'leri onlarındır, yok say). KENDİ kalemlerinde:
- RET satırı (alıntı/kanıt birebir değil, komut birebir değil, <8 kr parça, rol liste dışı) → kaynaktan yeniden BİREBİR kopyala, yeniden koş; en fazla 3 tur.
Başka dosyaya dokunma; dosya içeriğini Bash cat/sed/head ile basma.
Dönüş (≤4 satır): kalem sayısı · kendi kalemlerinde kalan RET · orkestrasyon-dışı sayısı.
