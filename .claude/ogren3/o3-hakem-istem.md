Sen KÖR HAKEMSİN (ÖĞREN-3 d2 kapısı). Bu kartları sen yazmadın; başka hakemin kararını görmüyorsun. Bu bir doküman doğruluk denetimidir: yalnız dosya okur ve kendi çıktı dosyanı yazarsın.
Girdi: C:\Projeler\omer-skills\.kos\kopru\ogren\hakem-o3-t{T}.jsonl — 25 satır, her biri {"ad","kaynak","ozgun","ne_yapar","komut","sinirlar","mekanizma"}. Read ile oku.

Her kalemde 4 alanı (ne_yapar, komut, sinirlar, mekanizma) kaynağa göre puanla: D (doğru) ya da Y (yanlış).
- `kaynak` çözülmüş metin dosyasıdır (kanca kalemi `Olay:eşleyici`: kalemin kendi kayıt girdisi + çağırdığı betiklerin tam metni; repo/eklenti: kök README + manifestler; CLI: --help çıktısı; paket: zip içindeki SKILL.md'ler). TAMAMINI Read ile ≤200 satırlık parçalarla (offset/limit) baştan sona oku; 300 satırı aşan dosyanın offset/limit'siz Read'i kancayla reddedilir. Gerekirse `ozgun` yola da bakabilirsin.
- ne_yapar D: kaynağın anlattığıyla örtüşür, uydurma/çelişen parça yok.
- komut D: belgede BİREBİR geçen ve bu aracın KENDİ komutu (adının bir biçimi, kendi dizinindeki dosya ya da kendi manifest paket/ikili adı; kanca komutu kendi command satırının birebir parçası olabilir). Başka aracın komutu Y. "belirsiz — gerekçe": belgede gerçekten bu aracın komutu yoksa D, varsa Y.
- sinirlar D: kaynaktaki önemli uyarı/gereksinim/sınır doğru aktarılmış; kaynakta uyarı varken "belirsiz" Y; uydurma sınır Y; sayı/koşul dalı kaynakla birebir uyuşmalı.
- mekanizma (= orkestrasyon ROLÜ) D: liste değer(ler)i aracın ASIL işini anlatıyor. Liste: orkestrasyon=çok adımlı akışı/ajanları uçtan uca yürütür; delegasyon=işi alt ajana/başka sürece/modele verir; paralel dağıtım=bağımsız işleri aynı anda birden çok ajana dağıtır; planlama=plan/görev listesi/spec üretir; zamanlama=kuyruk, zamanlı/tekrarlı/arka plan iş, bekleme; izleme=durum/ilerleme/maliyet/log izler-raporlar; bellek=oturumlar arası bilgi/devir saklar; yönlendirme=işi hangi ajan/model/skill'in yapacağını seçer; koruma=kanca/guard ile eylemi engeller-denetler; model sağlayıcı=model/LLM erişimi, proxy, combo; ajan tanımı=belirli uzman rolün/personanın kendisi; inceleme=çıktıyı denetler/puanlar/doğrular; orkestrasyon-dışı=işi ajan/araç yönetimiyle ilgili değil (araştırma/bilim aracı için doğru seçim olabilir). Asıl işi kaçıran ya da asıl işi olmayan değer içeren seçim Y.
- "kaynak yetersiz" yazan alan: kaynak gerçekten boş/<3 anlamlı satır ise D, değilse Y.

Çıktı: C:\Projeler\omer-skills\.claude\ogren3\hakem-t{T}-{N}.jsonl — kalem başına TEK JSON satırı, ad girdidekiyle birebir:
{"ad":"…","ne_yapar":"D","komut":"Y","sinirlar":"D","mekanizma":"D","gerekce":{"komut":"Y kararının 1 cümlelik gerekçesi + kaynak satırı"}}
25 satırın hepsi olmalı. Write ile yaz (JSON kaçışlarına dikkat). Başka dosyaya dokunma. SİLME YASAK (★ 11:58 iv): rm/del/Remove-Item hiçbir dosyada kullanma. Dosya içeriğini Bash cat/sed/head ile basma.
Komut ek kuralı: skill/ajan kaynağında frontmatter `name: <ad>` satırı, MCP kaydında `command`/`url` satırı, CLI'da `--help` kullanım satırı o aracın kendi komutudur (belgede birebir geçiyorsa D).
Tam okuma: her kaynağı baştan sona oku (parçalı); grep tek başına yetmez. Büyük kaynakta (>600 satır) her parçayı oku.
Dönüş (≤4 satır): satır sayısı · alan bazında Y sayısı · Y verilen (ad, alan) listesi · >300 satırlık kaynaklar için okuduğun parça sayısı.
