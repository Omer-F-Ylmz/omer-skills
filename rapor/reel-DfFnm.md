# REEL-DfFnm — MOGFIELD tanıtım reeli

- Reel: @dailyaionly, 28,4 sn, 1080x1920, 30 fps, VP9+AAC. İndirme: yt-dlp + .kos/ig-cookies.txt (başarılı). Dosya: .kos/kopru/reel-DfFnm/reel.mp4
- Araç: **MOGFIELD**, "open-source Higgsfield-inspired AI film studio on Comfy" (github.com/Trenchplanet/mogfield, **MIT**, 32 yıldız).
- Yapılış: ekran kaydı + hareketli metin; ffmpeg scdet (0.3) kesim vermedi (akıcı geçiş/wipe). Kontak 2 kare/sn incelendi.
- Akış: logo açılışı (yörünge etiketleri) → "Turn one video into many" → "Paste a link" → "Trim the part you want" → "The cost shows before you spend" → "Character swap" → "Direct a film by talking" (Agent Mode).
- Kanca: üst sabit beyaz kutu "Someone just open-sourced a Higgsfield AI creation platform"; CTA alt: 'Comment "Site" For Direct Link'; el adı sabit.
- Altyazı/metin: büyük tek satır başlık, ikinci kelime mavi; bölümler arası mavi diyagonal ışık wipe'ı.
- Ses: ort. -15,5 dB, max -4,7 dB. TTS mi müzik mi: ölçülemedi (transkript/dinleme yapılmadı). Üretim aracı: kesin değil, ipucu yok (AE/CapCut/Remotion ayırt edilemedi).
- Site: Comfy API anahtarı (Comfy Cloud) ya da yerel ComfyUI; Node app (`npm install`, `npm run build`, `npm start`, :8787); anahtarsız arayüz denenebilir. Ücretsiz arayüz, üretim Comfy kredisi. yt-dlp ile link indirir. API/repo: var.
- Lisans MIT → alınabilir. Güvenlik: README/package.json okundu; child_process yalnız media/motion/depth (ffmpeg/yt-dlp) ve deploy/vps-setup.sh'te; postinstall yok.
- KURULUM (tur3): gitleaks 0 sızıntı; semgrep (p/javascript+typescript, app/nodes/deploy) 0 bulgu; `npm install` EXIT 0 (postinstall yok); `npm run build` geçti (dist/ üretildi). Yol: docs/kaynak-kutuphane/klon/mogfield/app.
- ENGEL: `npm start` Windows'ta çalışmaz (`NODE_ENV=production` söz dizimi cmd'de tanınmıyor; ikinci yol: `tsx server/index.ts` doğrudan). Sunucuyu başlatma auto-mode sınıflayıcısınca [Code from External] ile **reddedildi**; ComfyUI (:8188) bu sırada yanıtsız kaldı. Bağlama ve sahne üretim testi YAPILMADI.

## v4 için teknikler (sosyal-oto-1.json'a eklendi)
1. Kanca + CTA ilk kareden sabit. 2. Tek satır başlık, vurgu kelime mavi. 3. ~4 sn'de bir ışık-wipe geçişi. 4. UI küçük kartta + solda başlık (maskot kartı düzeni). 5. Logo açılışı yörünge etiket bulutu. 6. Tek vurgu renkli koyu palet.

2. beyin notu: tools/beyin.py kaydet ile yazıldı.
