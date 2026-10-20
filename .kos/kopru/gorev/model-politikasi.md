# MODEL POLİTİKASI — bütün köprü oturumları ve alt ajanlar (Ömer 20 Eki 12:15, haftalık %7'de; bağlayıcı)
★ 20 Eki 14:40 Ömer: YEREL MODEL YASAK (ollama/llama-server/yerel whisper RAM yiyor). Ücretsiz basamak yalnız BULUT: Gemini → OpenRouter :free → GitHub Models → Groq (+ hesap açılınca Ollama Cloud -cloud · Cerebras · Mistral). STT: Groq whisper. Yerel yalnız bulut kotası dolarsa VE RAM <%70, tek seferde tek.
★ 20 Eki 17:06 Ömer: ücretsiz katman = `tools/ucretsiz_havuz.py` (tüm sağlayıcılar: Gemini · Groq · OpenRouter :free · OmniRoute halkası; yük dağıtımlı, 429'da bekleme yok, Haiku yalnız çağıranın tavanıyla). OmniRoute/OpenRouter tek kapı değildir.
Ömer: "Elimizdeki beleşleri kullanalım (OmniRoute vb., milyarlarca ücretsiz token); iş zorlaştıkça Haiku'ya, Sonnet'e; yalnız en en zor işte Opus. Opus 5 / Fable 5.1 çalışma ve düşünme tarzını Haiku/Sonnet'e verdik (çalışma kartı) — Opus'a bile gerek kalmayabilir."

## Merdiven (aşağıdan başla, yalnız başarısızlıkta bir basamak çık — ROUTER mantığı)
0. BETİK (model yok): sayım, biçim, birleştirme, dosya taşıma, grep, şema/test denetimi, kart iskeleti.
1. ÜCRETSİZ: OmniRoute `cc-ucuz-free` / `tools/ucuz_alt` zinciri (Groq curl UA → OpenRouter `:free` → Gemini free → ollama yerel RAM<%80). Claude aboneliği OmniRoute'tan GEÇMEZ. İş: sınıflama, özet taslağı, çeviri, etiket, ilk geçiş çıkarım, ikinci görüş. ÇIKTI HER ZAMAN MEKANİK DENETİMDEN geçer (birebir alıntı/komut, şema, test); geçmezse → 2.
2. HAIKU 5.5 (+ çalışma kartı `skills/is-akisi/references/calisma-karti.md`): kolay yargı, düzeltme, kısa kod, rapor biçimleme.
3. SONNET 5.5 medium → high: kod, kart yazımı, kapı hakemliği, oturum yöneticisi (köprü oturumlarının VARSAYILAN modeli).
4. OPUS 5.5 medium: yalnız iki Sonnet denemesi başarısızsa, mimari/inatçı hata, hakem ayrışmasında son karar. Gerekçe rapora tek satır.

## Yönlendirici (ROUTER-1 KAPI GEÇTİ 20 Eki d3: USD −%56 / −%30.4, başarı 12/12 eşit)
Alt görev kademesi: `python tools/yonlendir.py sec <tür>` → T0 betik · T1 `yonlendir.t1` (Groq→nemotron→ollama→Haiku) · T2 Sonnet medium · T3 Sonnet high; kabul mekanikse doğrulama light, başarısızlıkta +1 kademe (≤2); claude -p çağrılarında `FORCE_PROMPT_CACHING_5M=1`; her koşu `yonlendir.kaydet` ile kayda (SLEEP/MAKARA girdisi). Not: ücretsiz zincir kırılgan (d3 koşu 2: Groq kota, nemotron 404, ollama hata) → kazanç ~%30'a iner; zincir bakımı çağrı başı borç `ogren/bakim.tsv`.

## Uygulama
- Köprü kuyruğu (ajan-sira.tsv) satırlarında `model=` açık: varsayılan `model=sonnet`; `model=opus` yalnız Desktop gerekçesiyle.
- Agent aracında model alanı HER ZAMAN açık (FORCE kalktı; modelsiz alt ajan = Opus'a düşer = YASAK).
- Rapora: kullanılan basamaklar + her basamakta çağrı/token + kaç kez yükseltme ve neden.
- Ücretsiz kota (429/404) → bekleme yok, zincirde sonraki ücretsiz; hepsi düşerse Haiku.
