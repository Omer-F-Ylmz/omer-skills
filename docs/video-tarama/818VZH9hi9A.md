# Kendi "Vibe Coding" Sistemimi Kurdum (Adım Adım Rehber)
kanal: Poyraz Avsever · süre: 27 dk · altyazı: otomatik tr
ana iddia: Vibe coding dört aşamada (planlama → görselleştirme → inşa → yayın) yapılmalı; AI kodu yazsa da çıktıyı doğrulama sorumluluğu geliştiricide kalır.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| TestSprite/testsprite-cli | YENİ | ELENDİ | sponsor; ajan build sırasında uygulamayı gerçek kullanıcı gibi test edip hatayı ekran görüntüsüyle döndürüyor; izin ağır (API anahtarı + kredili bulut koşu + tünel), kısmen çift |
| model kademelendirme (iş zorluğuna göre model) | YENİ | BİLGİ | plan/mimari frontier (GPT 5.5, Claude Opus 4.8), uzun doküman Gemini 3.1 Pro, günlük iterasyon Claude Sonnet 4.6, ufak düzeltme DeepSeek V4 Flash; CLAUDE.md'de model kuralı yok |
| MVP planı + PRD dokümanı (mvp.md, prd.md; ajana @ ile etiketleme) | ZATEN VAR | ELENDİ | superpowers:brainstorming (spec) + writing-plans (plan dosyası) aynı işi yapıyor; @ dosya etiketleme Claude Code yerleşik |
| AI görsel üreticiyle referans mockup (ChatGPT) → koda verme | ZATEN VAR | ELENDİ | amaç jenerik AI görünümünden kaçmak: frontend-craft Bölüm 0 REF modu (reference/) + Bölüm 11 yön keşfi karşılıyor; videoda görsel isteği tam tutmadı |
| diğer: Claude Design, çıktıyı doğrulama sorumluluğu (sahte log/mock veri uyarısı), kodu tek dosyaya yığmama | ZATEN VAR | ELENDİ | claude-design MCP kurulu; CLAUDE.md "kanıtsız bitti yok" + Bölüm 5 "uydurma yok"; dosya yapısı Bölüm 5'te belirli |
| diğer: Cursor, Windsurf, zed-industries/zed, openai/codex (CLI + VS Code eklentisi), Google Antigravity, Lovable (Supabase entegrasyonu), Bolt.new, Replit Agent | ÇİFT | ELENDİ | AI kodlama ortamı / uygulama üretici: Claude Code ile aynı iş |
| diğer: Google Stitch, Figma AI | ÇİFT | ELENDİ | AI arayüz tasarımı: claude-design MCP + design skill ile aynı iş |
| diğer: CoderCup, vercel/next.js, flutter/flutter, radix-ui/primitives, Vercel, Dokploy/dokploy, coollabsio/coolify, Railway | YENİ | ELENDİ | Claude Code'a kurulacak araç değil (framework, UI kütüphanesi, barındırma servisi, liderlik tablosu) |
## ölçütler (YENİ)
- TestSprite/testsprite-cli: bakım=pushed 2026-09-14, 3205★, arşiv değil · çift=kısmi: frontend-craft Bölüm 2/9 screenshot döngüsü + claude-in-chrome (tarayıcıda doğrulama); kalıcı E2E suite onlarda yok · izin=README: global npm (Node 20.19+), `testsprite setup` API anahtarı ister, koşular kredi harcar (rerun 0.5 FE / 0.2 BE), yerel uygulama TestSprite tüneliyle buluta açılır, projeye skill dosyası yazar · context=proje skill açıklaması her oturum · kurulum: —
- model kademelendirme: bakım=bilinmiyor (teknik) · çift=örtüşme yok (CLAUDE.md'de kural yok; yerleşik /model opusplan ve subagent model alanı yalnız araç) · izin=yok · context=CLAUDE.md'ye 1 satır, her oturum · kurulum: —
- diğer YENİ: bakım=next.js 2026-09-15 142318★ · flutter 2026-09-15 178951★ · radix-ui/primitives 2026-08-08 19271★ · dokploy 2026-09-14 37305★ · coolify 2026-09-15 61800★ (hiçbiri arşiv değil); CoderCup, Vercel, Railway bilinmiyor · çift=örtüşme yok · izin=Vercel/Railway hesap + GitHub bağlantısı, Dokploy/Coolify sunucu, Next.js/Flutter npx/SDK · context=yok (Claude Code'a yüklenmez) · kurulum: —
## hedefler (BİLGİ)
- model kademelendirme (plan/mimari güçlü model, delege edilen mekanik iş ucuz model) → CLAUDE.md (CONTEXT DİSİPLİNİ: delege edilen işte model seçimi)
---
## ek: somut
- ayar: Codex VS Code eklentisi, model GPT 5.5, akıl yürütme "ekstra yüksek"; Codex'te dosya etiketleme @, Antigravity'de #
- ayar: ChatGPT görsel üretimi 16:9 oran; Gemini'den görsel değil yalnız görsel üretim promptu istendi
- ayar: inşa promptu: 3 panelli dashboard (sol input + animasyon, orta referans görsel, sağ Radix UI kodu + canlı render), dark mode, karanlık tema + şeffaf cam efekti, "kodları tek dosyaya yığma, panel/buton parçalarına böl"
- ayar: Next.js kurulumu varsayılan ayarlarla onaylandı; Vercel import ekranında env (.env gizli anahtarlar/API key) ve build/output ayarları varsayılan bırakıldı
- ayar: GitHub yeni repo "vibe coding video", açıklamasız, public; Vercel: Add New → Project → Import Git Repository → Import → Deploy → Continue to Dashboard → Domains
- komut: npx create-next-app@latest projenizin-adi (açıklama); npx create-next-app . (videoda, nokta = bulunduğun klasöre kur)
- komut: flutter create projenizin_adi (açıklama)
- komut: git add .; git commit -m "ilk commit"; git push (öncesinde GitHub'ın repo sayfasında verdiği komutlar yapıştırıldı)
- dosya: mvp.md; prd.md; public/ altına referans görsel ("referans")
- sayı: süreç 4 aşama; planlamada 2 doküman (MVP, PRD); no-code / AI IDE / CLI kategorilerinde 3'er araç — gösterildi (ekrandaki araç haritası)
- sayı: MVP "10 dakikada kodlanabilecek kadar" daraltıldı, Gemini sprint planı dakika 03 / 35 adımları (ASR belirsiz); fikir çekimden 10-15 dk önce düşünüldü — gösterildi (sonuçta sahte terminal logu, skeleton loader, mock kod çıktı)
- sayı: Codex çalışma süresi yaklaşık 11-11,5 dk — gösterildi (demo koşusu)
- sayı: Cursor 2 milyondan fazla aktif kullanıcı — yalnız iddia
- sayı: Zed 100.000 satırlık dosyayı 0,8 sn'de tarıyor (üretici iddiası) — yalnız iddia
- sayı: Gemini 3.1 Pro 2 milyon token context — yalnız iddia
- sayı: DeepSeek V4 Flash önbelleklemeyle %98 indirim — yalnız iddia
- sayı: frontier modellerde 5 saatlik ve haftalık kullanım hakkı bitiyor; 20 dolarlık uygulama 3 günde bitiyor — yalnız iddia
- sayı: TestSprite CLI kurulumu "üç basit komut", "tamamen ücretsiz", ajanın gece 03:00'te tek başına çalıştığını varsayıyor — yalnız iddia (README ile çelişiyor, bkz. ölçütler)
- sayı: Vercel GitHub repolarını "tek bir komutla" yayına alıyor — yalnız iddia (videoda arayüzden tıklamayla yapıldı)
