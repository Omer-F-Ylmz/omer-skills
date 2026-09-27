# Claude Limitine Bir Daha Asla Takılmayacaksın
## Künye
Claude Limitine Bir Daha Asla Takılmayacaksın · İsa Nurdoğdu · süre: 10:12 · tr-orig · https://youtu.be/JNM_rxqtlvY

## Özet
Claude'un mesaj limitine neden hızlı takıldığını "her mesaj tüm sohbeti baştan okuyor" mantığıyla açıklıyor; 10. mesajda ~5000, 30. mesajda ~232.000 token yakıldığını, tokenın %98,5'inin eski sohbeti tekrar okumaya gittiğini söylüyor. Bu fikir üzerine 11 kural sıralıyor: düzeltme mesajı yerine edit/regenerate, 15-20 mesajda yeni sohbet, soruları tek mesajda toplama, token ölçümü (yerel session.jsonl + phuryn/claude-usage dashboard), sık kullanılan dosyaları projeye yükleme, hafıza/tercihleri bir kez kurma, kullanılmayan özellikleri (web search, connectors, tools/research, extended thinking) kapatma, basit işler için Haiku'ya geçme, günü 2-3 seansa yayıp 5 saatlik pencereyi sabah erken başlatma, yoğun olmayan saatlerde çalışma ve güvenlik için overage açma. Ayrıca Caveman adlı bir Agent Skill'i (kısa/süssüz cevap talimatı) %65'e varan tasarruf iddiasıyla öneriyor.

## Bölümler
- 0:00 Giriş — token mantığı: her mesaj sohbeti baştan okuyor, maliyet katlanarak artıyor
- 2:08 Kural 1 — düzeltme mesajı yerine Edit + Regenerate
- 2:52 Kural 2 — her 15-20 mesajda yeni sohbete geç
- 3:26 Kural 3 — soruları tek mesajda topla
- 4:13 Kural 4 — token kullanımını ölç (yerel log + ücretsiz dashboard)
- 5:15 Kural 5 — sık kullanılan dosyaları projeye yükle
- 5:48 Kural 6 — hafıza ve tercihleri bir kez ayarla
- 6:29 Kural 7 — kullanmadığın özellikleri kapat
- 7:03 Kural 8 — basit işler için Haiku'ya geç
- 7:46 Kural 9 — işini gün içine yay (5 saatlik pencere)
- 8:38 Kural 10 — yoğun olmayan saatlerde çalış
- 9:18 Kural 11 — güvenlik için limit aşımını (overage) aç

## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Caveman | JuliusBrussee/caveman (ele, 1.00) | skill | https://github.com/JuliusBrussee/caveman | Claude'a kısa, süssüz konuşma talimatı verip çıktı token'ını düşürür | 2:08 | "Claude'a süslemeyi bırak de" |
| claude-usage (phuryn) | yok | CLI | https://github.com/phuryn/claude-usage | Yerel session loglarını okuyup token kullanımını gösteren ücretsiz dashboard/JSON API | 4:13 | "logları okuyan bir dashboard JSON API" |
| Düzeltme yerine Edit/Regenerate | yok | ipucu | yok | Yanlış cevaba "onu kastetmedim" gibi düzeltme mesajı atmak yerine mesajı düzenleyip yeniden üretmek bağlamı şişirmez | 2:08 | "yanlış cevaba böyle tepki verme" |
| 15-20 mesajda yeni sohbete geç | yok | iş akışı | yok | Sohbet uzadıkça her mesaj geçmişi yeniden okuduğundan belirli aralıkla yeni sohbet açmak token'ı düşürür | 2:52 | "her 15-20 mesajda yeni sohbete geç" |
| Soruları tek mesajda topla | yok | ipucu | yok | Ayrı ayrı sorular yerine tüm soruları tek mesajda sormak bağlam yüklemesini azaltır, cevabı netleştirir | 3:26 | "tek mesajda üç soru sorduğunda tek bağlam yüklüyorsun" |
| session.jsonl'den token ölçümü | yok | ipucu | yerel dosya ~/.claude/projects/.../session.jsonl | Oturum loglarındaki input_tokens/output_tokens/cache_read alanlarından gerçek token tüketimini görmek | 4:13 | "model, input_tokens, output_tokens, cache_read, timestamp" |
| Sık kullanılan dosyaları projeye yükle | yok | iş akışı | yok | Tekrar kullanılan dosyaları (ör. PDF) her seferinde yapıştırmak yerine projeye eklemek tekrarlayan tokeni azaltır | 5:15 | "hepsini buraya atmanda fayda var" |
| Memory/User Settings'i bir kez kur | yok | ipucu | Settings > Memory and User Settings | Rol, iletişim tarzı ve tercihleri her sohbette tekrar yazmak yerine bir kez hafızaya kaydetmek | 5:48 | "sadece bir kez rolünü... yazıyorsun, bitti" |
| Kullanılmayan özellikleri kapat | yok | ipucu | yok | Web search, connectors, tools/research, extended thinking açık kaldığında kullanılmasa da arka planda token yakar | 6:29 | "açık kalan her özellik token yakar" |
| Basit işler için Haiku'ya geç | yok | ipucu | yok | Basit görevlerde daha küçük/ucuz modele geçmek token maliyetini düşürür | 7:03 | "basit işler için Haiku'ya geç" |
| İşi gün içine yay / sabah erken ping | yok | iş akışı | yok | 5 saatlik kullanım penceresini sabah erken saatte küçük bir mesajla başlatıp günü 2-3 seansa bölmek limiti verimli kullandırır | 7:46 | "sabah 6'da tek bir küçük mesaj atan bir zamanlayıcı kuruyorsun" |
| Yoğun olmayan saatlerde çalış | yok | ipucu | yok | Yoğun saatlerde (hafta içi TR saatiyle öğleden sonra 3'ten akşam 10'a kadar) free modellerde limit daha hızlı tükeniyor, bu saatler dışında çalışmak avantajlı | 8:38 | "yoğun saatlerde 5 saatlik limitin daha hızlı tükeniyor" |
| Overage (limit aşımı) açık tut | yok | ipucu | yok | Güvenlik için limit aşımı özelliğini açık bırakmak kritik anda çalışmanın kesilmesini önler | 9:18 | "güvenlik için limit aşımını aç" |

## İddialar
| iddia | zaman | tür |
|---|---|---|
| 10. mesaj ~5000 token, 30. mesajdaki tek mesaj tam 232.000 token tutuyor | 1:00 | sayısal |
| Tokenların %98,5'i eski sohbeti tekrar okumaya, %1,5'i yeni cevabı üretmeye gidiyor | 1:00 | sayısal |
| Caveman kullananlar %65'e varan tasarruf sağlamış | 2:01 | sayısal |
| Arayüzdeki kullanım çubuğu sadece "%63 kullanıldı" gösteriyor, gerçek token sayısını göstermiyor | 4:13 | özellik |
| 26 Mart 2026'dan itibaren yoğun saatlerde (hafta içi TR saatiyle öğleden sonra 3'ten akşam 10'a kadar) free modellerde 5 saatlik limit daha hızlı tükeniyor | 8:38 | özellik |
| Haftalık limit değişmiyor, sadece limitin gün içinde nasıl tükendiği değişiyor | 8:38 | karşılaştırma |

## Kareden okunanlar
- 2:08 GitHub repo: JuliusBrussee/caveman, etiket "Agent Skill"
- 2:30 Arayüzde "Bağlam doluluğu" kırmızı uyarı çubuğu ("her mesaj sohbeti şişiriyor")
- 4:43 Örnek log satırı: model: claude-opus-4-6, input_tokens: 12480, output_tokens: 840, cache_read: 9210, timestamp: 2026-06-02 saat 19.50 (dosya: ~/.claude/projects/.../session.jsonl)
- 6:46 Claude arayüzü menüsü: Skills, Connectors, Add plugins, Research, Web search, Use style; firecrawl connector açık; model "Opus 4.6"

## Belirsizlikler
- Kare 4:43'teki "claude-opus-4-6" model adı ve token değerleri örnek/kurgu veri olabilir, gerçek bir oturumdan alındığı doğrulanamadı
- "26 Mart 2026'dan itibaren yoğun saatlerde limit daha hızlı tükeniyor" iddiası ileri tarihli, video içinde kaynak gösterilmiyor, doğrulanamadı
- phuryn/claude-usage linki açıklamadan alındı, karelerde doğrudan görünmüyor

## Atlanan segment oranı
0/15 (paket tam okuma)
