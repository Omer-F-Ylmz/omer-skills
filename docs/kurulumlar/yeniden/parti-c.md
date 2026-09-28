# Parti C — ilk 15'in 8-10'u (2026-09-28)

Hat: SERTİFİKA-1 (kayit --yeniden → ozet → paket → tarama → toplu → on → araştırıcı → bizde → katman → teknik → brief). Karar kaynağı: docs/kurulumlar/kayit.jsonl satır 164-200 (37 satır). Toplu: docs/video-tarama/2026-09-28-toplu-2.md (24b: Parti A toplu'su ezilmedi) · rapor: docs/kurulumlar/2026-09-28-uygula.md Koşu 6 · brief: docs/kurulumlar/yeniden/parti-c-brief.md. Etiket: `yeniden:parti-c`.

## b-LZ_Y9wor8 (Yıldız Dikme · jeskojets esinli sinematik 3D portföy)
- karar dağılımı: ÖĞREN 8 · ZATEN VAR 4 · UYARLA 3 · KUR 1 (bekleyen kural, ONAY) · departman frontend / surec-ajan-arac / arastirma-ogrenme
- T0: kural 1 · prompt 3 (UYARLA) · çift 2 (omer-kurallar:25, :27)
- Site/UI: `video teknik` UYARLA 7 (bekleyen/teknik-*) · ÖĞREN 0; prompt UYARLA 3 (uzun-detaylı prompt · loading screen · globe footer)
- prompt kalıbı: 1 aday (blz-sinematik-portfoy-promptu, anatomi dolu, 2 özellik ZATEN VAR) + 3 UYARLA kalıp → frontend-promptlar.md
- ÜRETİLEBİLİR: 0 · ayrıştırma: 0
- araştırıcı: blz-sinematik-portfoy-promptu 84.1k token · 12 çağrı · tam (rapor döndü; 12-tur bildirimi de geldi). Awwwards SOTD iddiası doğrulandı, sayısal iddialar doğrulanamadı.
- güvenlik ön taraması: yok (prompt adayı, repo yok; on.md `--rapor`)
- tarayıcı: 69.8k token · 13 çağrı · kare 5

## iYwCzKy6W40 (Yıldız Dikme · LUMEN 3D kamera landing, R3F + Sketchfab GLB)
- karar dağılımı: ÖĞREN 8 · KUR 5 (bekleyen kural, ONAY) · UYARLA 1 · ZATEN VAR 1 · departman frontend / test-qa / surec-git-yayin / surec-ajan-arac (+ sketchfab arastirma-ogrenme, iki videoda)
- T0: kural 5 · prompt 1 (UYARLA) · çift 1 (CLAUDE:4)
- Site/UI: `video teknik` ÖĞREN 4 · UYARLA 1; prompt UYARLA 1 (teknik prompt yazımı)
- prompt kalıbı: 1 aday (lumen-sitesi-promptu, anatomi 7 alan + 5 kalıp, altyazıdan 5:04; kabul alanı doğrulanamadı) → frontend-promptlar.md
- ÜRETİLEBİLİR: 0 · ayrıştırma: 0
- araştırıcı: lumen-sitesi-promptu 45.5k token · 12 çağrı · **yarım** (12 turda dosya yazmadan durdu; aday.md'yi ana ajan on.md'den yazdı, `arastirma: yarım` işaretli → DENE yok, ÖĞREN)
- güvenlik ön taraması: lighthouse `video on --repo GoogleChrome/lighthouse` 600 sn'de bitmedi, durduruldu → on.md yok, araştırılmadı (DevTools yerleşik paneli, ÖĞREN)
- tarayıcı: 76.1k token · 15 çağrı · kare 5

## LbBC5Wew4qs (Burhan KOCABIYIK · Claude Code + Codex plugin)
- karar dağılımı: ÖĞREN 3 · ZATEN VAR 2 · RED 1 · departman surec-inceleme / surec-plan / verimlilik
- T0: çift 1 toplu'da (log dosyası, CLAUDE:15) → katman ÖĞREN (şüpheli, aşağıda)
- Site/UI: yok (frontend içerik değil)
- prompt kalıbı: 0
- ÜRETİLEBİLİR: 0 · ayrıştırma: 0
- araştırıcı: codex-plugin-cc 29.8k token · 12 çağrı · **yarım** (yalnız iskelet; alanları ana ajan on.md + klon LICENSE/git log'dan yazdı: Apache-2.0, db52e28 2026-07-07). Özellik: codex-review / adversarial-review ZATEN VAR (gstack codex skill), rescue-transfer RED.
- güvenlik ön taraması: openai/codex-plugin-cc SkillSpector --no-llm HIGH/CRITICAL 4 → RED kanıtı
- tarayıcı: 54.3k token · 9 çağrı · kare 2

## T0 şüpheli sınıflamalar (K3)
- 6 "kural"ın altısı da davranış kuralından çok ipucu/prompt kalıbı: glb-dosya-boyutu-seçimi (asset ipucu) · yerelde-ayağa-kaldırma-isteği (kullanım ipucu) · github-da-kod-paylaşımı (iş akışı ipucu) · aşırı-sade-tasarım (tasarım ipucu) · asla-sözümden-çıkma ve ayrı-mobil-masaüstü-performans (prompt kalıbı). Desktop'ta ayıklanır.
- log-dosyası-üzerinden-hata-çözme: toplu ÇİFT (CLAUDE:15) → katman ÖĞREN, bilgi/sub-agent-ile-token-tasarrufu.md'ye destek (yanlış eşleşme şüphesi).
- T0 kullanım ipucu / araca özel ayrımı kayıtta ayrı alan olarak yok; dağılım doğrulanamadı.

## Ölçüm (K3)
- araştırıcı: 3 · toplam 159.4k token · 36 çağrı · yarım 2/3 (Parti A 2/4, B 1/2 → hedef 0 tutmadı). Belirti: iki ajan 12 çağrıyı bulguyu dosyaya işlemeden harcadı.
- Jev: paket 47 · toplu 58 · bizde 6 · katman 122 = 233 (tavan 450; teknik adımı sayı basmadı) · claude -p 0 · kare 12 (≤10/video).
- tarayıcı: 3 · 200.2k token · 37 çağrı.
- departman: frontend 21 · surec-inceleme 3 · surec-ajan-arac 3 · test-qa 3 · arastirma-ogrenme 2 · surec-git-yayin 2 · verimlilik 2 · surec-plan 1 · belirsiz 0.

## Düzeltme / kusur (sonraki dalga, kod değişmedi)
- aday-arastirici yarım 2/3: 24b'de klon/tarama kalktığı halde 12 tur yetmedi; tur disiplini (bulgu anında dosyaya) tutulmuyor.
- `video on --repo` büyük repoda (lighthouse) zaman aşımı yok; 600 sn bekledi.
- `video brief` bu koşuda 4 bölüm üretti (Özellik kararları · Departman · İddialar · Linkler); Site/UI ve prompt anatomisi brief'e düşmedi (kaynakları frontend.md `## Teknikler`, frontend-promptlar.md, aday.md).
- Ana ajan iskelet listesi write_text ile CRLF yazıldı → ilk `video katman` koşusu OSError ile kayda yazmadan düştü; `tr -d '\r'` ile yeniden koşuldu.

## YÜKLENECEK ZIP
- yok (skills/ değişmedi)
