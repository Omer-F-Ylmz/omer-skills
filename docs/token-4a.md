# TOKEN-4a — tur + araç çıktısı: ölçüm ve tasarım (L7 · L8 · L14)

Ayar, hook, skill, plugin ve MCP dosyalarına dokunulmadı. Bu dalgada yalnız ölçüm ve tasarım yapıldı. Tüm sayılar `python tools/token_olc.py olc --arac-dokum --cikti olcum/token-4a.json` çıktısından alındı. Ölçüm 14 günü kapsıyor: 2150 dosya, toplam 508.0 M ağırlıklı token, günde ≈36.3 M. İnsan tablosu: `olcum/token-4a.md`. Testler: `tests/test_token_olc_dokum.py` (13 test, mutasyon kırmızı).

## Yöntem
- **Katkı.** Formül: n·(w + 0.1·(R−1)).
  - n: sonucun token sayısı (karakter/4).
  - R: sonucu taşıyan istek sayısı, compact sınırına kadar.
  - w: yazma katsayısı. Oturumda 1h yazma baskınsa 2, değilse 1.25.
- **Headroom kalibrasyonu.** k = Σ(Δctx − çıktı) / Σ sonuç token'ı, temiz adımlarda hesaplanır. Temiz adım, arasına yalnız tool_result giren iki ardışık istektir.
  - 2039 temiz adım, 211 oturum. Medyan k 2.04, genel k 1.37.
  - Temiz adımı olmayan oturuma genel k uygulanır.
  - Düzeltilmiş değer (düz) = ham × k.
- **k > 1 ne demek.** Transcript'teki karakter/4 tahmini usage'ın altında kalıyor. Sebepler: tokenizer (kod, Türkçe ve JSON metni karakter başına daha çok token tutuyor) ve tool_result sarmalı. Headroom'un kestiği kısım bu net değerin içinde kalıyor, ayrıca ölçülemiyor. Bu yüzden "Headroom örtüşmesi" satırı (ham − düz) negatif çıkıyor: ham değer Headroom kesintisini saklamıyor, gerçeğin altında kalıyor. Tasarruflar düzeltilmiş değerle verildi.
- **Kategoriler örtüşür.** Tekrar okuma, retrieve-read ve limitsiz okuma kategorilerinin hepsi Read'in alt kümesi. Bu yüzden payları toplanmaz.

## En büyük 10 kaynak (düz katkı, 14 gün · toplam ağırlıklıya pay)
1. Bash `sed`: 753 çağrı, 4.568 M, %0.90
2. Bash `cat`: 543 çağrı, 4.151 M, %0.82
3. Bash `python`: 1276 çağrı, 2.525 M, %0.50
4. Bash `grep`: 1013 çağrı, 2.506 M, %0.49
5. Read, >300 satır, aralıksız, rehber dışı: 300 okuma, 2.439 M, %0.48
6. Aynı dosyanın tekrar okunması: 538 okuma, 2.093 M, %0.41
7. Bash `echo`: 1.815 M, %0.36
8. Bash `ls`: 1.623 M, %0.32
9. Bash `for`: 1.094 M, %0.22
10. Bash `wc`: 0.714 M, %0.14

headroom_retrieve'i tetikleyen Read'ler listeye giremedi: 29 dosya, 50 okuma, 0.675 M. Araç sonuçlarının tamamı toplam ağırlıklının küçük bir kesri. Read düz katkısı 11.19 M, payı %2.2.

## L8a — Read aralık kuralı (PreToolUse Read hook'u)
- **Mekanizma.** Dosya eşiğin üstündeyse ve offset/limit/pages verilmemişse hook okumayı reddeder. Ret mesajı satır sayısını ve şu önerileri içerir: `graphify query`, `Grep -n`, `Read limit`.
  - Muaf olanlar: skill rehberleri (skills/**, plugins/**/skills/**, references/**; SINIR, Blender dersi) ve eşik altındaki dosyalar.
  - Satır sayısı diskten okunur.
  - Görsel ve PDF uzantıları muaf tutulur. Gerekçe: >2000 satır kovasında 129 okuma var, katkıları yalnız 0.027 M. Bunlar büyük olasılıkla ikili dosyalar; satır sayısı diskteki baytlardan geliyor ve anlamsız.
- **Eşik: 300 satır.** Seçim K2 verisine dayanıyor. Limitsiz okumaların ham katkısının 1.70 M'i (14 günde) 301–1000 satır bandında. Ret sonrası okumanın aralıklı okumaların medyanı (350 token) kadar olacağı varsayıldı.
  - Eşik >300: 0.119 ham / **0.165 düz M/gün**, 300 okuma.
  - Eşik >500: 0.068 / 0.096, 238 okuma.
  - Eşik >1000: 0.004 / 0.006.
  - KB eşiği eklenmedi. Satır sayısı yeterli ayrımı veriyor.
- **Kalite riski.** Tam bağlam gereken işte (bütün dosyayı yeniden yazmak) okuma eksik kalabilir ve her ret +1 tur getirir. Rehberler muaf olduğu için Blender tipi bir kayıp beklenmiyor.
- **Kapı.** TOKEN-4b orta görev. Koşul: görev başarısı eşit kalmalı, ağırlıklı token düşmeli, tur artışı ≤%10 olmalı.

## L8b — Bash çıktı aileleri
- **rtk ölçümü.** rtk'lı ve rtk'sız çağrıların medyan çıktısı karşılaştırıldı. sed %5 küçülüyor, grep %40, cat, python ve ls %0.
  - rtk kapsamını genişletmenin gerçekçi kazancı 0.021 ham / **0.030 düz M/gün**.
  - Üst sınır, rtk'sız çıktının tamamı sıfırlansa: 0.317 / 0.457.
- **Hedefli çözüm.** rtk'nın küçültemediği en büyük aileler (sed, cat) aslında Bash üzerinden dosya okuması. Bu kural zaten yazılı, ama 14 günde 753 sed ve 543 cat çağrısı yapıldı.
  - Mekanizma: L8a ile aynı eşiği kullanan bir PreToolUse Bash hook'u. İlk kelimesi cat, sed, head ya da tail olan, bir dosyayı hedefleyen (pipe girdisi olmayan) komutu reddeder ve Read offset/limit önerir.
  - Hedef katkı (rtk'sız, düz, 14 gün): sed 2.727 M, cat 0.609 M. Tasarruf bu tutarların L8a oranındaki kısmı olur.
  - python ailesi (rtk'sız 2.208 M) betik çıktısıdır. Hook yerine tarif kuralı önerilir: araç yalnız sayı ve özet satırı döndürsün.
- **Kalite riski.** Pipe ya da üretici komut yanlışlıkla reddedilebilir. Bunu önlemek için hook yalnız dosya argümanı varken tetiklenmeli.
- **Kapı.** L8a ile aynı.

## L8c — Değişmemiş dosyanın tekrar okunması
- **Ölçüm.**
  - 162 dosya tekrar okundu, toplam 538 tekrar.
  - 502 tekrar arada düzenleme olmadan yapıldı, ama farklı aralıklarla. Bu meşru dar okumadır ve L8a'nın beklenen yan etkisi.
  - 70 tekrar aynı aralıktan.
  - Aynı aralık katkısı 0.002 ham / **0.004 düz M/gün**. Değişmemiş tekrarların tamamı (üst sınır) 0.104 / 0.141.
- **Mekanizma (önerilmez).** Read hook'u oturumdaki (dosya, aralık, mtime) üçlüsünü hatırlar; aynı üçlü gelirse "zaten bağlamda" diye reddeder.
- **Karar: uygulanmaz.** Kazanç ihmal edilebilir düzeyde. Ayrıca Headroom eski sonucu "compressed after use" diye sıkıştırdıktan sonra tekrar okumak tek kurtarma yolu; hook bu yolu kapatırdı.

## L7 — Paralellik ve betik+parametre
- **Ölçüm.**
  - 13 962 istek var. 12 294'ü araçlı, 2410'u paralel (%19.6). 9884 istek tek araçlı.
  - Küçük Read dizisi: art arda gelen tek ve küçük (<2000 token) Read istekleri. 50 dizi, 110 istek. Birleştirilse 60 istek kazanılırdı (1.040 M usage, 14 gün): **0.074 M/gün**, günde 4.3 istek.
  - Arşivlerde gerçek/tavan tur oranı genelde 0.62–0.85. İki aşım var: TOKEN-1'de 59/40, TOKEN-3b'de 17/12.
- **Tarif şablonu kuralları (Desktop uygular).**
  1. Okunacak dosyalar baştan biliniyorsa hepsi tek yanıtta paralel okunur.
  2. Aynı adım ≥3 kez tekrarlanacaksa scratchpad'e betik yazılır ve parametreyle tek çağrıda koşulur.
  3. Tur tavanı ölçülen orana göre konur (gerçek ≈ tavanın 0.85'i). Her 5 turda sayaç tutulur; tavanın %85'inde kalan iş yazılıp DUR denir.
- **Tasarruf.** Ölçülen kısım 0.074 M/gün, küçük Read birleştirmesi. token-0 tahmini ~2.0 M/gün idi ve tur azaltmanın tamamını kapsıyordu; bu kısım ancak TOKEN-4b A/B koşusuyla ölçülebilir.
- **Kalite riski.** 0. Paralel çağrılarda bağımlılık hatası olabilir. **Kapı:** TOKEN-4b, tur metriği.

## L14 — Uzun oturum
- **Ölçüm.** 200k'yı aşan ana oturum 85 tane. 77'si (%91) tek dalga, 8'i çok dalga.
- **Dalga bölme.** Her dalga başında /clear yapılsaydı kazanç 0.1 × (dalga başı ctx − taban) × dalga istekleri olurdu: 7.020 M / 14 gün = **0.501 M/gün**. Kural zaten var ("/clear mandatory at dalga start"); bu 8 oturum kuralı ihlal ediyor.
- **Tek dalga.** 77 tek dalgalı oturumda bölme işe yaramaz. Kaldıraç dalga içinde /compact olur. Kalite etkisi negatif ve ölçülmedi; TOKEN-4b orta görevde denenecek.
- **Kapı.** Görev başarısı + tur.

## headroom_retrieve ilişkisi (TOKEN-6'ya not)
- **Ölçüm.**
  - 14 günde 229 retrieve çağrısı.
  - Retrieve'dan hemen önceki araç: ToolSearch 68, Read 64, Bash 61, mcp-filesystem 12, Grep 11.
  - Retrieve'a kadar geçen süre medyan 1 tur / 7.7 sn. Yani sıkıştırılan sonuç neredeyse hemen geri isteniyor ve iki kez ödeniyor.
- **TOKEN-6 maddeleri.**
  1. ToolSearch ve şema çıktıları sıkıştırma dışında bırakılmalı.
  2. "compressed after use" eski mesajı değiştiriyor. Bunun prefix cache'i bozup bozmadığı, sıkıştırmadan sonraki cache_creation sıçramalarıyla ölçülmeli.
  3. Sıkıştırma işareti modele `headroom_retrieve`'i öneriyor, ama araç ertelenmiş olarak `mcp__headroom__headroom_retrieve` adıyla duruyor. Bu oturumda doğrudan çağrı "No such tool" hatası verdi; bu fazladan bir tur demek.
  4. k > 1 olduğu için Headroom'un net etkisi transcript/usage oranından ayrılamıyor. Headroom açık/kapalı A/B koşusu gerekli.

## TOKEN-4b kapısı
- **Kısa görev.** rtk-ab (C:\Users\pc\Desktop\rtk-ab), Opus 5.5 ile yeni taban. 2 taban + 2 kaldıraçlı koşu.
- **Orta görev.** K2 verisinden tipik bir omer-skills görevi: tools/video/video modülünde (cli.py, uygula.py ve kur.py en çok limitsiz ve tekrar okunan dosyalar) bir değişiklik ve testi. Ayrı git worktree'de 1 taban + 1 kaldıraçlı koşu.
- **Kaldıraç seti.** L8a (300 satır), L8b sed/cat hook'u, L7 tarif kuralları, L14 dalga başı /clear. L8c dışarıda kalır.
- **Metrikler.** Görev başarısı (kabul ve testler), ağırlıklı token, $, tur. Karar madde 21'e göre verilir: görev başarısı düşerse RED.
- **Tavan.** En fazla 6 `claude -p` koşusu (2+2+1+1).
