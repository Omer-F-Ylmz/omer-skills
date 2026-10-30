---
type: plan
status: active
tags: [postiz, oauth, sosyal-oto, tiktok-audit]
relatedTo: [POSTIZ-KUR-1, SOSYAL-OTO-1]
---
# Ömer şuna tıklasın (Postiz: http://localhost:4007)

Anahtarları sohbete yazma; Postiz `.env` WSL'de `/opt/postiz/.env` (chmod 600). Yönetici girişi: `wsl -d Ubuntu -u root cat /opt/postiz/admin.txt` (e-posta + parola).
Her anahtar için: `wsl -d Ubuntu -u root -e nano /opt/postiz/.env` → boş alanı doldur → `wsl -d Ubuntu -u root -e bash -c "cd /opt/postiz && docker compose up -d --force-recreate postiz"`.

## 1. YouTube (iki kanal; sosyalmdyahesabi1 ve 2 ayrı Google hesabı)
1. console.cloud.google.com → proje "sosyal-oto" → API'ler: YouTube Data API v3 (+ Analytics, Reporting) etkinleştir.
2. OAuth izin ekranı → External → Test kullanıcıları: sosyalmdyahesabi1 ve sosyalmdyahesabi2 (ikisini de ekle). Dikkat: Testing modunda yetki 7 günde düşer; "In production"a alınca düzelir (doğrulama istenebilir).
3. Kimlik bilgileri → OAuth istemci kimliği → Web uygulaması → Yetkili yönlendirme URI: `http://localhost:4007/integrations/social/youtube` → Client ID/Secret → `.env` YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET.
4. Postiz → Add Channel → YouTube → grup 1 kanalı (@freeaidrophq), sonra aynısını grup 2 (@curiositywellhq) için.

## 2. Instagram (profesyonel hesap, iki hesap)
1. Her IG hesabı Profesyonel (Creator); Standalone yolu Sayfa gerektirmez. developers.facebook.com → uygulama (Business) → Instagram ürünü.
2. Uygulama rolleri → Instagram Test Kullanıcısı olarak iki IG hesabını ekle; her hesapta instagram.com/accounts/manage_access → kabul et (yoksa "Insufficient developer role").
3. Yönlendirme URI: `http://localhost:4007/integrations/social/instagram-standalone` → INSTAGRAM_APP_ID/SECRET (Facebook Sayfası yolunu seçersen FACEBOOK_APP_ID/SECRET + `/instagram`).
4. Postiz → Add Channel → Instagram → iki hesabı bağla.
5. Reels yayını için Meta medyayı herkese açık HTTPS URL'den çeker: aşağıdaki tünel (madde 4) şart; taslak denemesi tünelsiz yapılamaz.

## 3. TikTok (iki hesap)
1. developers.tiktok.com → uygulama → ürünler Login Kit + Content Posting API; scope: user.info.basic, video.upload, video.publish. Yönlendirme URI HTTPS olmalı (madde 4'teki tünel adresi + `/integrations/social/tiktok`).
2. Medya domaini/URL öneki doğrulaması (DNS imza ya da dosya) tünel adresi için yapılır.
3. Client key/secret → `.env` TIKTOK_CLIENT_ID / TIKTOK_CLIENT_SECRET. Postiz → Add Channel → TikTok (iki hesap).
4. Denetim öncesi yalnız SELF_ONLY/taslak (inbox); video telefonda TikTok'tan yayınlanır. Denetim metni aşağıda.

## 4. Sabit HTTPS adres (IG medya + TikTok redirect/doğrulama)
cloudflared kurulu. Seçenek A: ngrok ücretsiz statik domain (hesap aç → "Domains" → bir adet ücretsiz). Seçenek B: Cloudflare adlı tünel (alan adı gerektirir; ücretsiz değil olabilir). Adres hazır olunca `MAIN_URL/FRONTEND_URL/NEXT_PUBLIC_BACKEND_URL` o adrese çevrilir (FRONTEND_URL tarayıcı adresiyle birebir aynı olmalı). Bu adım ölçülmedi.

## 5. Sonra
`python -I tools/postiz/yayinci.py esle` (hesapları gruba eşler) → `yayinci.py calistir --kuru` → `yayinci.py calistir` (taslak). Herkese açık yayın yalnız `--zamanla` ile ve Ömer onayından sonra.

## TikTok denetim başvurusu metni (taslak)
Uygulama: kendi sahibi olduğumuz iki TikTok hesabına, kendi ürettiğimiz kısa videoları (yapay zekâ ile üretilmiş, AI etiketli) yönetim panelimizden yüklemek için Content Posting API kullanır. Üçüncü kişi hesabı yok; yalnız hesap sahibi giriş yapar, kullanıcı verisi saklanmaz (yalnız erişim jetonu yerel sunucuda). Her gönderide başlık, gizlilik seçimi ve yapay zekâ bildirimi gösterilir; kullanıcı onayı olmadan yayın yapılmaz (ilk aşama taslak/inbox). Tahmini hacim: hesap başına günde 3 video. Demo videosu: Postiz'de hesap bağlama → video yükleme → gizlilik seçimi → taslak oluşturma ekran kaydı (bu kayıt alınmadı).
