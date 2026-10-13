# ai-marketing-hub-claude-ads — 34 benzersiz kayıt

**Amaç:** Google, Meta, YouTube, LinkedIn, TikTok, Microsoft, Apple, Amazon, Reddit vb. için Claude öncelikli ücretli medya operasyonu: denetim, plan, kreatif, yayın, izleme, raporlama.

**İç yapı:** Ana eklenti claude-ads + claude-ads:ads-<x> alt skill'leri: platforma özel (ads-google, ads-meta...) ve yaşam döngüsü (setup, dna, plan, create, generate, launch, monitor, optimize, report).

## En güçlü parçalar
- `claude-ads:ads-audit` — Tam reklam kontrolü, hesap sağlığı ve ücretli medya teşhisi.
- `claude-ads:ads-setup` — Onboarding, brand DNA, API token/kimlik profili ve keychain yapılandırması; ilk adım.
- `claude-ads:ads-plan` — Medya planı, PPC/paid-social stratejisi, kampanya mimarisi ve kanal yol haritası.
- `claude-ads:ads-math` — Break-even, ROAS, CPA, LTV/CAC, MER hesapları.
- `claude-ads:ads-dna` — Yetkili web sitesinden reklam için herkese açık marka/teklif profili çıkarır.
- `claude-ads:ads-create` — Doğrulanmış brief'ten kaynak temelli kampanya konsepti, metin ve kreatif plan.
- `claude-ads:ads-server-side-tracking` — sGTM, CAPI, Events API, event_id ve pixel hata ayıklama.
- `claude-ads:ads-monitor` — Günlük/haftalık anomali, bütçe hızı ve yayın sonrası doğrulama.
- `claude-ads:ads-test` — A/B deney tasarımı, hipotez, örneklem büyüklüğü, istatistiksel anlamlılık.
- `claude-ads:ads-landing` — Tıklama sonrası deneyim ve reklam-sayfa uyumu denetimi.

## Birlikte kullanım
- ads-setup → ads-dna → ads-plan → ads-create → ads-generate → ads-launch → ads-monitor.
- ads-audit + ads-report: denetimi müşteri/yönetici raporu ya da PDF'e dökmek.
- ads-attribution + ads-server-side-tracking: dönüşüm ölçümünü doğrulamak.
- marketingskills ailesinin ads/ad-creative skill'leriyle konu örtüşür; claude-ads platform operasyonuna iner.

## Tuzaklar
- ads-setup API token/kimlik profili ister; ads-generate açıkça yapılandırılmış görüntü sağlayıcısı gerektirir.
- ads-optimize kampanya duraklatma, arşivleme, silme isteklerini de kapsar; geri dönüşsüz işlemler.
- ads-research/ads-validate eskiyen API/platform iddialarını yeniden doğrulamayı gerektirir.
- marketingskills:ads ve ad-creative ile çakışan kapsam.

## Üyeler
- plugin (1): claude-ads
- skill (33): claude-ads:ads-amazon, claude-ads:ads-apple, claude-ads:ads-attribution, claude-ads:ads-audit, claude-ads:ads-budget, claude-ads:ads-competitor, claude-ads:ads-create, claude-ads:ads-creative, claude-ads:ads-dna, claude-ads:ads-generate, claude-ads:ads-google, claude-ads:ads-landing, claude-ads:ads-launch, claude-ads:ads-linkedin, claude-ads:ads-math, claude-ads:ads-meta, claude-ads:ads-microsoft, claude-ads:ads-monitor, claude-ads:ads-optimize, claude-ads:ads-photoshoot, claude-ads:ads-pinterest, claude-ads:ads-plan, claude-ads:ads-reddit, claude-ads:ads-report, claude-ads:ads-research, claude-ads:ads-server-side-tracking, claude-ads:ads-setup, claude-ads:ads-snapchat, claude-ads:ads-test, claude-ads:ads-tiktok, claude-ads:ads-validate, claude-ads:ads-x, claude-ads:ads-youtube
