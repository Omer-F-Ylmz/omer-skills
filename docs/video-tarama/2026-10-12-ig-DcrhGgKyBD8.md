# Comment “BOSS” and I’ll send you the free prompt.
## Künye
Comment “BOSS” and I’ll send you the free prompt. · nocodealex · süre: 0:29 · ? · https://www.instagram.com/reel/DcrhGgKyBD8/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-12-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 10574 tk · claude-haiku-5-5: claude-haiku-5-5 · 50478 tk
## Özet
nocodealex'in kısa reel videosu: 'Boss Loop' istem tekniğini anlatıyor. Claude'a bir görev verilir, işçi alt-ajanlar (sub-agent) üretmesi istenir ve üçüncü satırda kodu yazmayan, taze bağlamlı katı bir 'boss' ajan atanır. Boss gerçek çıktıyı açıp çalıştırmayı dener, hataları geri gönderir ve mükemmel puan verene kadar döngü kendiliğinden sürer. Token tüketimi yüksek olduğundan önce basit prototip yapılıp sonra son cilalama için döngü çalıştırılması öneriliyor. Açıklamada maker-checker ayrımı ve Boris Cherny alıntıları var.
## Bölümler
- 0:00 Boss Loop tekniğine giriş
- 0:13 Görev ve işçi ajanlar (loadout / the party)
- 0:19 Boss'un hataları bulup döngüye sokması
- 0:24 Token uyarısı: önce prototip, sonra boss loop
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Boss Loop | yok | prompt | yok | Görev + işçi alt-ajanlar + katı boss ajanı ile kendi kendine döngüleyen istem tekniği | 0:00 | It's called the Boss Loop. |
| Claude | yok | teknik | yok | Görevi alan ve alt-ajanları üreten ana yapay zekâ aracı | 0:00 | Karede 'CLAUDE NEEDS A STRICT BOSS' başlığı (karede: kanıttan) Karede 'CLAUDE NEEDS A STRICT BOSS' başlığı |
| Claude Code | yok | CLI | yok | Açıklamada anılan kodlama ajanı aracı; Boris Cherny'nin geliştirdiği | açıklama | Boris Cherny, who built Claude Code |
| Sub-agents | yok | teknik | yok | İşçi alt-ajanların üretilmesi ve boss'un ayrı ajan olarak atanması | 0:00 | spawn a team of worker sub-agents |
| Maker-checker split | yok | teknik | yok | Yapan ile doğrulayanı ayıran, taze bağlamlı denetçi yaklaşımı | açıklama | Claude Code team call this the maker checker split |
| Boss Loop ile işçi ajanlar ve katı denetçi boss kullanarak uygulama/site üretmek | yok | prompt | yok | Claude'a görev ver ve iyi sonucun çıtasını gösteren gerçek bir örnek ekle; görevi bağımsız değerlendirilebilir en küçük parçalara böl, her parçaya bir işçi alt-ajan ata; kodu yazmamış, taze bağlamlı katı bir boss ajan ata: gerçek çıktıyı açıp çalıştırmayı denesin, geri göndersin, mükemmel puana kadar kullanıcı olmadan döngüde kalsın. | 0:13 | kaynak: kare |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Kodlama ajanını iyi yapan daha iyi model değil, yazan ile bitti kararını verenin ayrı olmasıdır. | açıklama | özellik |
| Boss Loop token'ı hızla tüketir; önce basit prototip yapılıp sonra son cilalama için tetiklenmeli. | 0:24 | öneri |
| Boss Loop ile tek istemde komple uygulama ve web siteleri üretilebilir. | 0:03 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Boss Loop tekniği | Boss Loop | It's called the Boss Loop. |
| kare 0:00 | Claude | Claude | CLAUDE NEEDS A STRICT BOSS |
| altyazı 0:00 | Worker sub-agents | Sub-agents | spawn a team of worker sub-agents |
| açıklama | Claude Code | Claude Code | Boris Cherny, who built Claude Code |
| açıklama | Maker checker split | Maker-checker split | call this the maker checker split |
| açıklama | Anthropic | aday değil: genel kavram | Anthropic's own Claude Code team |
| açıklama | Boris Cherny | aday değil: genel kavram | Boris Cherny, who built Claude Code |
| açıklama | #claudeai #claude #claudetips #claudecode hashtagleri | aday değil: genel kavram | hashtag listesi |
| altyazı 0:24 | Token tüketimi / prototip | aday değil: genel kavram | This burns through tokens fast |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamıyor |
## Kareden okunanlar
- 0:00: Başlık 'CLAUDE NEEDS A STRICT BOSS'; piksel tarzı işçi karakterler ve takım elbiseli boss; altyazı 'prompting technique that's'
- 0:13: 'THE LOADOUT' paneli, 'THE TASK' satırı; dört işçi karakter; altyazı 'But the secret'
- 0:14: 'THE LOADOUT' altında 'THE TASK' ve 'SPAWN THE PARTY'; altyazı 'line of the prompt'
## Belirsizlikler
- Yorumlar girişsiz alınamadı; 'BOSS' yorumuyla verilen ücretsiz istemin metni görülemedi.
- Prompt metni kare ve açıklamadan özetlendi; üçüncü satır başlığı (ASSIGN...) tam okunamadı.
- Altyazıdaki 'Cloud' büyük olasılıkla Claude; sözlükteki Codex/agent-sdk-dev eşleşmeleri bulanık ve videoda anlatılmıyor.
- Videoda kurulum/terminal komutu yok.
- Boris Cherny alıntıları yalnız açıklamada, videoda söylenmiyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Görevi ve beklenen kalite çıtasını (örnek) Claude'a yaz — araçlar: Claude
- 2. adım — Claude'a worker sub-agent takımı kurmasını söyle (Spawn the party) — araçlar: Claude
- 3. adım — Üçüncü satırla ayrı, taze bağlamlı bir boss agent ata — araçlar: Claude
- 4. adım — Önce basit prototipi ürettir (düşük token harcaması için) — araçlar: Claude
- 5. adım — Worker agent'lar kodu yazar — araçlar: Claude
- 6. adım — Boss agent çıktıyı açıp çalıştırmaya çalışır ve reddeder — araçlar: Claude
- 7. adım — Döngü: hataları otomatik düzelt, yeniden dene; boss tam puan verene kadar sürdür — araçlar: Claude
- 8. adım — Boss tam puan verdikten sonra nihai ürünü cilala — araçlar: Claude
## Promptlar
- Boss Loop ile işçi ajanlar ve katı denetçi boss kullanarak uygulama/site üretmek — Claude'a görev ver ve iyi sonucun çıtasını gösteren gerçek bir örnek ekle; görevi bağımsız değerlendirilebilir en küçük parçalara böl, her parçaya bir işçi alt-ajan ata; kodu yazmamış, taze bağlamlı katı bir boss ajan ata: gerçek çıktıyı açıp çalıştırmayı denesin, geri göndersin, mükemmel puana kadar kullanıcı olmadan döngüde kalsın.
ikinci göz KAPALI: --ikinci-goz yok
