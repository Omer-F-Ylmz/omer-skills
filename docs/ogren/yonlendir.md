# ROUTER-1 (20 Eki) — görev başı kademe yönlendirici: ölçüm ve karar

Yönlendirici `tools/yonlendir.py` + `tools/yonlendir-kurallar.json` (20 tür, T0–T4), kayıt `.kos/kopru/yonlendir-kayit.jsonl`,
kart `skills/is-akisi/references/calisma-karti.md` (FABLE-1 protokolü + Opus/Fable tarzı), ölçüm `tools/olcum/yonlendir_olc.py`,
ham çıktı `docs/ogren/yonlendir-olcum/`. Önceki iş: ROUTER-1 d3 (12 Eki) `model_sec` (yalın oturum + effort sınıfı) — bayraklar ondan.

## d3 (20 Eki 11:55) — KAPI GEÇTİ
(a) kod-oku/regex/alan-cikar T1'e (kural tablosu; T1 zinciri son çare Haiku 5.5). (b) Sabit yük: d2 kullanımından çözülen
fiyat (Sonnet 5.5 girdi $2/M, yazım 1h $4/M, okuma $0.1/M, çıktı $10/M) → tek atımlık çağrıda en ucuz `FORCE_PROMPT_CACHING_5M=1`
(yazım $2.5/M); `--resume` YALIN'daki `--no-session-persistence` ile çakışır, seçilmedi. Koşuda 5m yazımı doğrulandı (iki kol).
(c) Karışım = son 7 gün köprü iş kaydı (112 iş: ogren 34 · video 26 · token 21 · atlas 11 · graphify+diğer 20; yonlendir-kayit
yalnız ölçüm satırı içeriyor) → ogren 4 (G01 sayim, G05 lisans, G06 etiket, G09 alan-cikar) · video 3 (G13 etiket, G14 alan-cikar,
G15 video-rapor) · token 2 (G07 kod-oku, G10 kod-yaz) · atlas 1 (G03 birlestir) · graphify+diğer 2 (G08 regex, G11 hata-duzelt).
Kademe: T0 2 · T1 7 · T2 1 · T3 2. Varsayım: iş ailesi → tür eşlemesi oturum düzeyinde, alt görev dağılımı ölçülmedi.

| çağrı | A (USD) | B koşu 1 | B koşu 2 |
|---|---|---|---|
| T1 toplu (7) | 0.0445 (Sonnet high) | 0 (Groq) | 0.0018 (Haiku; Groq kota, nemotron 404, ollama hata) |
| T2 toplu | 0.0254 (high) | 0.0045 (medium, A önbelleğini okudu) | 0.0323 (medium) |
| T3 toplu (ortak) | 0.0476 | 0.0476 | 0.0476 |
| toplam / başarı | 0.1175 · 12/12 | 0.0521 (−%56) · 12/12 | 0.0818 (−%30.4) · 12/12 |

Ham jeton: A 32 712 · B1 23 655 (−%28) · B2 33 949 (+%4, Haiku'nun 14k girdisi). claude -p 6 · ücretsiz 16 · sınıflayıcı 3/12.
Adil olan B2 (B1 d2'deki gibi A önbelleğinden yararlandı); B2 eşiği ancak geçiyor: ücretsiz kota düşünce kazanç ~%30'a iner.
Ham: `docs/ogren/yonlendir-olcum-d3/`.

ogren-ortak.md satır taslağı (Desktop yazar): "Alt görev kademesi: `python tools/yonlendir.py sec <tür>` → T0 betik · T1
`yonlendir.t1` (Groq→nemotron→ollama→Haiku) · T2 Sonnet medium · T3 Sonnet high; kabul mekanikse doğrulama light, başarısızlıkta
+1 kademe (≤2); claude -p çağrılarında `FORCE_PROMPT_CACHING_5M=1`; her koşu `yonlendir.kaydet` ile kayda."

## d2 (20 Eki 11:10) — adil ölçüm: iki kol aynı çağrı yapısı, kapı = USD eşdeğeri
Yapı: T0 betik · T1 toplu · T2 toplu · T3 toplu, kart (461 karakter, ~165 jeton kestirimi: d1 kartı 1 963 kr ≈ 700 jeton) her
istemde. A: T1–T3 Sonnet high. B: T1 `yonlendir.t1` zinciri (Groq gpt-oss-120b → nemotron :free → ollama qwen3.5:4b → Haiku 5.5),
T2 Sonnet medium, T3 Sonnet high. claude -p ≤6 için T3 toplusu iki kolda birebir aynı çağrı (bir kez koştu, iki kola yazıldı),
A bir kez koştu, B iki koşu. Ham: `docs/ogren/yonlendir-olcum-d2/`. claude -p 5 · ücretsiz 14 · ücretli 0.

| çağrı | A (USD) | B koşu 1 | B koşu 2 |
|---|---|---|---|
| T1 toplu | 0.0181 (Sonnet high) | 0 (Groq, 1 061 jeton) | 0 (Groq) |
| T2 toplu | 0.0358 (high, düşünme 1 369) | 0.0140 (medium, A'nın önbelleğini okudu) | 0.0305 (medium, düşünme 825) |
| T3 toplu (ortak) | 0.0947 | 0.0947 | 0.0947 |
| toplam / başarı | 0.1486 · 12/12 | 0.1087 (−%27) · 12/12 | 0.1252 (−%16) · 12/12 |

Ham jeton: A 26 843 · B1 21 600 (−%20) · B2 21 572 (−%20). Sınıflayıcı yan ölçü (zincir, tür etiketsiz): 4/12, 4 419 jeton.

**KAPI GEÇMEDİ** (başarı eşit, USD −%27 / −%16 < %30). Iska sınıfı: **kademe** — (1) T3 toplusu A maliyetinin %64'ü ve iki
kolda aynı; T1+T2 bedava olsa bile tavan −%36. (2) Sonnet medium high'dan yalnız −%15 ucuz: her claude -p ~4.4k jeton 1 saatlik
önbellek yazımı (≈$0.016) sabit yükü düşünme farkını yutuyor. Kota ıskası yok (Groq ilk denemede, `sebep` boş); doğrulama ıskası
yok (yükseltme 0); kart etkisi ihmal edilebilir (~165 jeton/çağrı). B1'in −%27'si A-T2 önbelleğini okumasından; adil olan B2.

d3 önerisi: (a) T2 türlerini (kod-oku, regex, alan-cikar — kabulü mekanik) T1 zincirine indir, kalan +1 T2'ye; ölçümde T2 Sonnet
çağrısı kalkar → kestirim B ≈ 0.095 (−%36). (b) Sabit yük: claude -p yalın oturumun önbellek yazımını ölç/kıs (5 dk önbellek ya da
tek oturumda kademe başına --resume). (c) Görev karışımı gerçek iş dağılımına göre (zor iş kütlesi kapıyı belirliyor).

## d1 ölçüm (12 görev: 3 T0 · 3 kolay · 3 orta · 3 zor; kabul yerel ve mekanik)
| | başarı | jeton (girdi+önbellek+çıktı) | USD eşdeğeri | claude -p |
|---|---|---|---|---|
| A: hepsi Sonnet high, tek toplu çağrı | 12/12 | 17 748 (girdi 10 606 · çıktı 7 142) | 0.1138 | 1 |
| B: T0 betik · T1 ücretsiz · T2/T3 ayrı toplu | 12/12 (yükseltme 0) | 21 368 (Sonnet 19 555 + ücretsiz 1 813) | 0.1008 | 2 |
| fark | = | **+%20 (kapı ≥−%30)** | −%11 | |

Koşu 2 (yalnız T0+T1; Sonnet kısmı claude -p ≤4 tavanına sığmadı): G05 (MIT lisansı) kaldı — nemotron "JSON yok", ollama ve
gemma 429, combo "JSON yok". Gerçek akışta T2'ye yükselirdi; kararlılık ölçütü yine de tutmadı.
Sınıflayıcı yan ölçüsü (tür etiketsiz, tek ücretsiz çağrı): 3/12 doğru, jeton 0 → gemma 429; sınıflayıcı **ölçülemedi**.

## Neden kapı tutmadı (çağrı dökümünden)
- Çıktı jetonu B'de −%22 (5 546 ↔ 7 142): T0/T1 görevlerini Sonnet'ten almak gerçekten kazandırıyor.
- Girdi B'de +%32 (14 007 ↔ 10 606): iki ayrı çağrı = sabit yük iki kez (önbellekli sistem 1 370/çağrı) + kart ~700/çağrı.
- Toplu tasarım A'yı kayırıyor: A tek çağrıda sabit yükü bir kez öder. Görev başı gerçek kullanımda (her görev ayrı çağrı) A 12×,
  B 6× sabit yük öder — bu ölçülmedi (12+6 claude -p tavanı aşar).
- Görev kütlesi zor kod işlerinde (G10–G12); onlar iki kolda da Sonnet high. Kazanç payı küçük görevlerle sınırlı.

## Karar
**KAPI GEÇMEDİ** (başarı eşit, jeton +%20, kararlılık tutmadı). Yönlendirici + kayıt + yükseltme mekanizması hazır ve testli
(tests/test_yonlendir.py 6/6); ÖĞREN-2+/video hattına bağlanmadı. Sonraki ölçüm için: görev başı ayrı çağrı (her iki kol),
kart yalnız T2/T3'te ve kısaltılmış, T1 zincirinde lisans için ücretsiz kota boşken koşu.

## Alt ajan model/effort (keşif)
- code.claude.com/docs/en/sub-agents: frontmatter `model:` ve `effort:` destekli; Agent aracı çağrıda `effort` alır.
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` kullanıcı settings.json'unda AÇIK, `CLAUDE_CODE_SUBAGENT_MODEL` yok. Belge: FORCE açıkken
  "Claude Code ignores the `model` field in subagent definitions" → alt ajanlarda kademe tablosu işlemez (model yerine hangi
  modelin geldiği ölçülmedi). Onay: `python onay/router_1b_force.py --kuru|uygula|--geri` (Ömer koşar).
