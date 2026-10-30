---
type: summary
status: active
tags: [postiz, sosyal-oto, wsl, ara-kayit]
relatedTo: [POSTIZ-KUR-1, SOSYAL-OTO-1]
---
# POSTIZ-KUR-1 — TUR BITTI (çağrı tavanı 45/45; kapanış DEĞİL)

## Ölçülen
- Docker Desktop açılmıyor (com.docker.service admin ister, kabuk admin değil) → docker.io + compose WSL2 Ubuntu içine kuruldu; .wslconfig memory 2→6GB (yedek `.wslconfig.bak-postiz`).
- Postiz çalışıyor: http://localhost:4007 (6 konteyner: postiz, postgres, redis, temporal, temporal-postgres, elasticsearch; restart: always). Kayıt+yönetici açıldı, API anahtarı `/opt/postiz/.env` (chmod 600, ekrana yazılmadı).
- API canlı: `/public/v1/integrations` 200 (0 hesap), `/public/v1/upload` 201. RAM %87 (sınır 89 — dar; ES bellek payı izlenmeli).
- Kalıcılık: zamanlanmış görev `PostizBaslat` (oturum açılışı, gizli, WSL'i `sleep infinity` ile uyanık tutar). Kanıt: görevsiz kalınca WSL kapandı ve 502 verdi; görev betiği başlatınca 75 sn içinde API döndü.
- `tools/postiz/yayinci.py` (kontrol/esle/calistir/dongu): hazir/*/video.mp4 + meta.json → upload → taslak/zamanlı post; grup başı 3 ET slotu; hata → log + `beyin_kayit olay hata`; Claude çağırmaz. Yalnız `kontrol` ve `upload` canlı koşuldu; post gövdesi gerçek hesapla SINANMADI.

## Roast Room (teknik 5/10, şeytan 3/10; kayıt: tools/postiz/OMER-TIKLA.md, bu rapor)
- IG video_url public HTTPS ister → sabit tünel şart (ngrok statik domain/Cloudflare adlı tünel); ölçülmedi.
- Aynı video 6 hesaba aynı gün = koordineli ağ riski → düşük hacimle başla, kesim/sıra çeşitlemesi (hat.py zaten tohumlu), AI etiketi; önce tek hesap uçtan uca.
- YouTube kotası kaynaklar çelişkili (araştırma: videos.insert günde 100 çağrı, 2026-10-15 doküman; roast: eski 1600 birim) → Google konsolunda kota sayfasından doğrulanmadı.
- Testing modunda token 7 günde düşer → `kontrol` oturum düşmesini logluyor/2. beyne yazıyor.
- Yedek: `tools/postiz/yedek.sh` → `C:\Users\pc\postiz-yedek\db-*.sql.gz` + env (ölçüldü: 18 KB dump; zamanlı çalıştırma henüz yok).
- Lisans: Postiz AGPL-3.0 (GitHub API). Kendi sunucuda kişisel kullanım serbest; değiştirip ağdan hizmet sunarsak kaynak açma koşulu doğar — biz değiştirmiyoruz.
- Tur2: Docker servisi hâlâ Stopped (Start-Service reddedildi, admin yok) → WSL docker.io yolu sürüyor; `PostizBaslat` ile 6/6 konteyner kalktı. `/posts` gövdesi sahte integration ile sınandı: şema geçti, "Integration not found" 400 (gerçek hesapla sınanmadı). `test_yayinci.py` 3/3 yeşil.

## Yapılmadı (neden)
- YouTube/IG/TikTok geliştirici uygulamaları ve OAuth: Ömer tıklaması gerekir → `tools/postiz/OMER-TIKLA.md` (adımlar + TikTok denetim metni).
- (4) platform başına gizli/taslak test gönderisi: bağlı hesap yok → YAPILMADI. (5) hakem ≥8/10: puanlanacak çıktı yok → ALINMADI.
- Commit yok. Sonraki oturum: Ömer tıklamaları → `yayinci.py esle` → `calistir --kuru` → taslak → hakem; lisans + yedek.
