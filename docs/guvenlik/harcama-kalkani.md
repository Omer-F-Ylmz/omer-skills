---
type: guide
status: active
tags: [guvenlik, anahtar, harcama, sinir]
relatedTo: [ANAHTAR-KALKAN-1, departman-guvenlik]
---

# Harcama kalkanı, sağlayıcı başına tek sayfa (Ömer hesaba girip ayarlar)

Menü adları sağlayıcı arayüzünde değişebilir; amaç aynı: **(1) aylık harcama tavanı, (2) uyarı eşiği, (3) anahtarı kapsamla kısıtla, (4) proje başına ayrı anahtar.**
Önerilen tavan: toplam ≈ 50 $/ay başlangıç; her sağlayıcıda uyarı %50 / %90.

| Sağlayıcı | Tavan / uyarı | Anahtar kısıtı |
|---|---|---|
| OpenRouter | Keys → anahtar başına **Credit limit** + reset (günlük/haftalık); auto-top-up kapalı | Proje başına ayrı anahtar; kullanılmayanı sil |
| Google AI Studio / Cloud | Cloud Console → Billing → **Budgets & alerts** (%50/90/100); AI Studio'da proje harcama tavanı varsa aç | APIs & Services → Credentials → anahtar → **API restrictions** (yalnız Generative Language API) + **HTTP referrer** (web) ya da **IP** (sunucu) |
| Anthropic Console | Settings → **Limits** → aylık spend limit + bildirim; iş yüküne göre Workspace + workspace limiti | Workspace başına ayrı anahtar |
| OpenAI (varsa) | Settings → Limits → budget + alert; Project bazlı limit | Project anahtarı, izin kapsamı "restricted" |
| Groq | Console → Billing → harcama limiti (ücretli plan varsa) | Anahtar başına ayrı ad; sızarsa sil/yenile |
| Vercel (takım omer) | Team Settings → Billing → **Spend Management**: tutar + bildirim + "projeleri duraklat" | Env değişkenlerini "Sensitive" işaretle; Preview'e prod anahtarı verme |
| Supabase | Org → Billing → **Spend Cap** açık | Tüm tablolarda RLS açık (Advisors → Security); `service_role` hiçbir istemci/`NEXT_PUBLIC_` kodunda olmaz; sızıntıda JWT secret döndür |
| fal | Dashboard → Billing/Usage → harcama limiti, auto-recharge kapalı | Anahtar kapsamı "API"; admin anahtarı sunucudan çıkmaz |
| Modal | Settings → Usage/Billing → workspace spend limit | Token'ı ortam başına ayrı; sızarsa Settings → Tokens'tan iptal |
| Hugging Face | Endpoint/Jobs için bütçe uyarısı | Fine-grained token, yalnız gereken repo/izin, son kullanma tarihi |
| Apify | Account → Limits → **max monthly usage** (USD) | Anahtar başına Actor kapsamı |
| Oxylabs / Composio / Higgsfield / Tripo / Sketchfab / Meta | Panelde kredi/üst limit; yoksa aylık elle kontrol takvimi | Dashboard'da anahtar listesi; kullanılmayanı iptal |
| Telegram |, | @BotFather → `/revoke` ile token yenile (sızıntıda) |
| GitHub |, | Public repolarda **Secret scanning + Push protection** aç (Settings → Code security); PAT'lar fine-grained + son kullanma tarihli |
| Cloudflare / Hostinger | Plan sabit; API token'ı kapsam + IP filtreli | Global API Key yerine kapsamlı token |

## Her sızıntıda sıra (anahtar → Ömer)
1. Sağlayıcıda anahtarı **döndür** (yenile), eski anahtar anında ölür; silmek/geçmişi temizlemek anahtarı kurtarmaz.
2. Yeni anahtarı yalnız ortam değişkenine / Vercel env'e koy (HKCU, `.env` git dışı).
3. Faturayı/kullanımı sağlayıcı panelinde gözden geçir (şüpheli istek var mı).
4. Git geçmişi temizliği (`git-filter-repo`) yalnız Ömer onayıyla; temizlense de eski anahtar geçersiz sayılmalı.

## Kural
Müşteriye giden istemci koduna (`NEXT_PUBLIC_*`, `VITE_*`, mobil/Unity) gizli anahtar girmez; sağlayıcı çağrısı sunucu/edge tarafından yapılır.
