# Önek kayması (21a K1)

## Ölçüm
- Son 3 gün, 233 oturumun ilk isteği (transcript usage): cache_creation medyan 76.192, ortalama 49.818; cache_read medyan 7.426. Read kümeleri: 0 (87 oturum, önbellek soğuk/başka proje), ~17k (44), ~7k (27), ~29k (16).
- Kontrollü deneme (2 × `claude -p "ok de"`, sonnet, aynı dizin, art arda, toplam $0.62): ikisinde de **cache_read = 17.565**, cache_creation 76.167 / 77.444. Saniyeler arayla aynı istem bile 17.565. token'dan sonrasını paylaşamıyor.
- headroom perf: 233/4115 istekte write > 2×read; "First 5 avg read=20.7k write=30.9k".

## Ayrışma noktası
17.565. token: araç bloğunun sonu / sistem metninin başı. Aynı dizin ve aynı istemle bile kayma olduğuna göre sebep oturuma özel bir alan. Sistem metnindeki Environment bölümü oturum kimliği taşıyan scratchpad yolunu içeriyor (`...\Temp\claude\<proje>\<oturum-id>\scratchpad`). Bu yüzden sistem kırılım noktası her oturumda ıskalanıyor ve önbellek araç kırılım noktasına düşüyor. Tarih, gitStatus, claude-mem bağlamı ve CLAUDE.md mesajlarda (system-reminder) yer alıyor; bunlar yalnız mesaj önbelleğini etkiliyor.
Güven: ayrışma konumu yüksek (iki bağımsız ölçümde bayt bayt aynı sayı). Sebep orta: istek gövdesi karşılaştırılmadı, çünkü Headroom `--log-messages` açık değil ve 8787'yi caveman tutuyor (bkz. bekleyen/caveman-otobaslat.md).

## Oturum başına yeniden yazılan token
~76k (claude -p ve etkileşimli oturum medyanı aynı). Bunun ~17.5k'sı paylaşılıyor, geri kalan ~58.6k'nın sistem metni kısmı gereksiz yere yeniden yazılıyor.

## Sabitleme önerisi
1. Sebebi kesinleştir: iki oturumun istek gövdesini `headroom capture` ile yakala ve sistem bloklarını diff'le (docs/kurulumlar/bekleyen/onek-sabitle.md, KOŞULMAZ).
2. Scratchpad yolu doğrulanırsa CC tarafında oturumdan bağımsız bir yol ya da kapatma ayarı aranır; ayar yoksa CC'ye hata/istek bildirilir. Repo içinde yapılacak bir değişiklik yok.
