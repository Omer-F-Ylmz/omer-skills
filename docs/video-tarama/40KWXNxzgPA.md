# Uygulamana Kendin Saldır: Strix Açıkları Kanıtlıyor
kanal: İsa Nurdoğdu · süre: 1 dk · altyazı: otomatik tr
ana iddia: Strix, farklı uzmanlıklara sahip yapay zeka ajanlarından oluşan bir ekiple uygulamana hedefli saldırılar düzenleyip gerçek istismar edilebilir açıkları kanıtla (PoC) buluyor ve düzeltme önerisi sunuyor.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| usestrix/strix | YENİ | ADAY | açık kaynak AI pentest ajanı (Apache-2.0); kurulu sette örtüşme yok; açıklamada link yok, "yoruma hacker yaz, DM'den göndereyim" etkileşim çağrısı |
## ölçütler (YENİ)
- usestrix/strix: bakım=aktif (62668 yıldız, archived=false, son push 2026-09-13) · çift=örtüşme yok (SkillSpector plugin/skill tarar, Strix çalışan uygulamayı pentest eder) · izin=Docker (çalışır halde) + STRIX_LLM + LLM_API_KEY (yerelde LLM_API_BASE; "ücretsiz" iddiası LLM kullanım maliyetini saymıyor), kurulum betiği bash (curl | bash), hedef kod dizinine ve docker sandbox'a erişiyor; opsiyonel bulut yolu strix cloud login · context=CLI yolunda yalnız çağrılınca; README'deki ajan yolu (npx skills add usestrix/strix) 9 skill açıklaması ekler · kurulum: curl -sSL https://strix.ai/install | bash
## hedefler (BİLGİ)
- yok
---
## ek: test/güvenlik
- araç/yöntem: Strix (usestrix/strix) — farklı uzmanlıklara sahip yapay zeka ajanlarından oluşan ekip uygulamayı çalıştırıp zayıf noktalara hedefli saldırı yapıyor, açığın kullanılabildiğini kanıtlıyor, düzeltme önerisi sunuyor (sözlü)
- ayar: araç kendi modelini getirmiyor; Claude Code?, GPT, Gemini veya yerel model (altyazı: "Loud Code GPT, Cemini") API anahtarı bağlanıyor (sözlü)
- performans tavizi var mı: BELİRSİZ — videoda modeller arası karşılaştırma/benchmark yok, yalnız "API anahtarını bağlayabiliyorsun" deniyor
