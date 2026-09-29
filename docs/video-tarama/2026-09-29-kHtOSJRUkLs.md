# Paste This Into Claude Code, Never Run Out Of Tokens Again
## Künye
Paste This Into Claude Code, Never Run Out Of Tokens Again · Sharbel A. · süre: 19:47 · en-orig · https://youtu.be/kHtOSJRUkLs
motor: parti 2026-09-29-uzun · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
## Özet
Sharbel A., Claude Code'da token limitinin çoğunun (%96) yazdıklarından değil, her mesajda konuşma geçmişinin yeniden gönderilmesinden geldiğini anlatıyor. Açıklamada verdiği (ücretsiz) denetim promptunu ve yedi düzeltmeyi sıralıyor: işler arasında /clear, oturum ortasında model/effort değiştirmemek (önbelleği bozar), araç çıktısını filtrelemek, kullanılmayan MCP sunucularını kapatmak, subagent'ları doğru kullanmak, doğru modeli baştan seçmek ve zamanlanmış görev tuzağı. İşe yaramayan tavsiyeler (kısa prompt, compact, ekran görüntüsü, PDF) ve izleme araçları (/context, /usage, /cost, yanma hızı göstergesi) de anlatılıyor.
## Bölümler
- 0:00 Claude Code neden token'ı bitiriyor
- 0:58 Bağlam her mesajda nasıl katlanıyor
- 1:52 Token kullanımını denetleme
- 2:47 Düzeltme 1: İşler arasında /clear
- 4:32 Düzeltme 2: Oturum ortasında model değiştirme
- 6:20 Düzeltme 3: Büyük araç çıktısını filtrele
- 7:39 Düzeltme 4: Kullanılmayan MCP sunucularını kapat
- 10:17 Subagent'lar ne zaman kazandırır, ne zaman israf eder
- 12:28 Başlamadan önce doğru modeli seç
- 12:55 Gece token yakan zamanlanmış görev tuzağı
- 14:39 İşe yaramayan tavsiyeler
- 16:24 Bağlam, kullanım, maliyet ve yanma hızını izleme
- 18:10 Tam token tasarruf sistemi
- 19:03 Denetimi düzenli çalıştır
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Token kullanım denetim promptu | yok | prompt | yok | Claude Code'a yapıştırılınca bağlam dökümünü, tool deferral durumunu, bellek dosyalarını, cache hit oranını ve zamanlanmış görevleri denetleyen prompt. | 1:52 | Paste it into Claude code and it will audit your actual configuration. |
| /clear | yok | ipucu | yok | İş değişince konuşmayı sıfırlar; mesaj bağlamı %0'a döner. Önce /rename ile adlandırıp /resume ile geri dönülebilir. | 2:47 | When you finish a job and start with a different one, use /clear. |
| Model/effort'u oturum başında sabitle | yok | ipucu | yok | Model, effort veya fast mode değişimi cache'i geçersiz kılar; baştan seçip dokunmamak gerekir. | 4:32 | the model is part of the cache key. Change the model, and none of your history matches |
| Çıktı filtreleme hook/dosyası | yok | teknik | yok | Ajanla komut arasına çıktıyı kısaltan küçük bir dosya (filtre) yazdırmak; 800 satırlık kurulum çıktısı bağlama girmez. | 6:20 | It will create one small file that sits between your agent and the command |
| MCP sunucu listesi ile kullanılmayanları kapatma | yok | MCP | yok | Tüm bağlı araçları anahtarlarla listeleyen panelde ay içinde kullanılmayanları kapatmak; /context'te tools satırının 'deferred' olduğunu kontrol etmek. | 8:39 | turn off anything you have not used in the last like month |
| Subagent'ı Haiku'ya ayarlama | yok | ipucu | yok | Yüksek hacimli izole işlerde subagent modelini Haiku yapmak ana oturum cache'ine dokunmadan maliyeti düşürür. | 12:19 | set the sub-agents model to Haiku. That is a five times reduction |
| /rewind | yok | ipucu | yok | Birkaç turu geri almak için compact yerine kullanılır; cache'in bildiği noktaya döner. | 15:39 | use /rewind instead. Rewind takes you back to a point your cash already knows |
| /context, /usage, /cost ve yanma hızı göstergesi | yok | CLI | yok | Pencere içeriğini, plan tüketimini (hangi skill/araç/ajan yaktı) ve oturum maliyetini gösteren izleme komutları. | 16:24 | It shows you what is in your window right now, line by line |
| Claude Code yapılandırmasını token tüketimi açısından denetlemek | yok | prompt | yok | Denetim promptunun tam metni videoda okunmuyor; açıklamada olduğu söyleniyor ama açıklama bağlantısı yok. | 1:52 | kaynak: altyazı |
| Araç çıktısını ajan görmeden önce filtrelemek | yok | prompt | yok | Kurulum çıktısını kısaltan filtre dosyası oluşturmasını isteyen prompt (ekranda gösterildiği söyleniyor, metni okunmuyor). | 7:20 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Yazdıklarının token kullanımındaki payı yalnızca %0,01. | 0:00 | sayısal |
| Harcamanın %96'sı geçmişi yeniden okumaktı. | 3:49 | sayısal |
| Opus'ta 200.000 token bağlamda model değişimi 10 sentlik turu 1 dolarlık tura çevirir (10 kat). | 4:32 | sayısal |
| GitHub MCP tek başına 26.000, Slack 21.000 token yükler; tool deferral ile maliyet %85 düşer. | 7:39 | sayısal |
| Örnek subagent yaklaşık 9.800 token harcayıp ana bağlamda 5.700 kazandırdı; izole bakınca kayıp. | 11:19 | karşılaştırma |
| Abonelikte cache 1 saat sürer; saatten seyrek çalışan zamanlanmış görev her seferinde cache'i kaçırır (10 kat maliyet). | 12:55 | sayısal |
| Compact token tasarrufu değildir; en pahalı mesajlardan biridir ve cache'i siler. | 14:39 | öneri |
| Ekran görüntüsü metinden ucuz değil: Opus'ta ~2.700 token, 4K ~5.000; PDF'i düz metne çevirmek maliyeti yaklaşık çeyreğe düşürür. | 15:39 | sayısal |
| Arka planda açık Claude Code oturum başına 4 sentten az maliyetli; asıl sorun zamanlanmış görevler ve canlı ajan ekipleri. | 13:55 | karşılaştırma |
## Kareden okunanlar
- 3 (2:19): Konuşmacı, altta kırmızı '0.01%' yazısı.
- 4: 'Every turn re-sends the whole conversation', 'Tokens sent so far 572,000, turn 20 of 20', 'What you just typed' etiketi, artan çubuk grafik.
- 5: Konuşmacı yakın plan, ekranda bilgi yok.
## Belirsizlikler
- Açıklama bağlantısı yok; denetim promptunun metni videodan okunamıyor.
- Kare listesinde 3 görsel var ama 5 giriş görünüyor; ilk iki kare yolu yalnızca ('[yol]'), içerikleri doğrulanamadı.
- 'Opus 5' ve 'Sonnet' fiyat/token rakamları konuşmacının iddiası; bağımsız doğrulanmadı.
- Transkriptte bozuk ifadeler var (ör. 'cloth code', 'cash'); MCP paneli komutu metinde eksik (muhtemelen /mcp).
- Aday kanıtlarının çoğu altyazıdan; karede görülen doğrulama yok.
## Atlanan segment oranı
0/24 (paket tam okuma, motor)
