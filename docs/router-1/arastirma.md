# ROUTER-1 araştırma (d3, 12 Eki)

Ölçüt (Ömer 12 Eki): tasarruf artarken kalite artmalı; **model düşürmek tasarruf yolu değil**; ANTHROPIC_BASE_URL değişirse uygula koşulmaz, Headroom 127.0.0.1:6767 zinciri bozulmaz.
Kanıt: "yerel" = bu makinede denendi; "bilgi" = model bilgisi (Haz 2026), canlı doğrulanmadı — lisans satırları KUR'dan önce `ara-lisans-kontrol` ile doğrulanmalı.

| Araç | Ne yapar | CC entegrasyonu | Gizlilik / maliyet | Karar |
|---|---|---|---|---|
| OmniRoute 3.8.50 | 237 sağlayıcı, 14 strateji (priority, cost-optimized, auto 9 etken), fallback zinciri | **yerel**: global npm, 20128 ayakta (anahtarsız 401); video F1 `yonlendir.py` OpenRouter modelleriyle kullanıyor; MCP 11b/K0'da kaldırıldı, 44 omni-*/cli-* skill kapalı | istem 3. tarafa (OpenRouter vb.), API $ | REF — zaten kurulu; Claude adımları için model değiştirir → kural dışı |
| claude-code-router (musistudio) | CC isteklerini başka sağlayıcı/modele yönlendiren proxy | ANTHROPIC_BASE_URL → Headroom zincirini bozar | istem 3. tarafa | RED (BASE_URL + model düşürme) |
| LiteLLM proxy | 100+ sağlayıcı için tek OpenAI uyumlu ağ geçidi, fallback, bütçe | ANTHROPIC_BASE_URL ya da betik içi | kendi barındırma; sağlayıcı $ | REF (OmniRoute aynı işi yapıyor) |
| RouteLLM (lm-sys) | Öğrenilmiş güçlü/zayıf model yönlendirici | betik içi | yerel; zayıf modele düşürür | RED (model düşürme) |
| Not Diamond / OpenRouter auto | İstem başına model seçen SaaS | API anahtarı | istem 3. tarafa, API $ | RED |
| OpenRouter ücretsiz modeller | Kota sınırlı ücretsiz modeller | OmniRoute üzerinden (mevcut) | istem 3. tarafa | REF (yalnız video ön-eleme, mevcut) |
| Portkey / Helicone | Gateway + gözlem (maliyet, gecikme) | BASE_URL proxy | gözlem kaydı | REF (gözlem Headroom+ccusage'ta var) |
| Martian | Ticari model yönlendirici | API | 3. taraf | RED |
| IG-40 devri (7 aday, devir/router-1.tsv) | LiteLLM, MoE routing, GPT-5.4/Gemini 3.1/Llama 3.1 örnek modeller, OpenRouter, Manifest (oturum maliyet takibi) | — | — | REF; Manifest = gözlem, ccusage/claude-monitor zaten kurulu |
| Yerel 9router-paket, cli-routing, omni-* (synced) | 9router/OmniRoute HTTP istemci talimatları | sunucuya bağlı | — | REF (istemci; yeni yetenek getirmez) |

## Sonuç
Dış yönlendiricilerin hepsi tasarrufu **ucuz modele geçerek** ya da **BASE_URL proxy** ile yapıyor; ikisi de bu görevin sınırı dışında.
UYARLA edilen fikir: OmniRoute'un *priority + fallback zinciri* ve *auto skorlaması* → kendi `claude -p` çağrılarımızda
model sabit, **bağlam** (yalın oturum) ve **effort** sınıfa göre; başarısızlıkta zincir bir üst kademe. Tasarım: `tasarim.md`.
